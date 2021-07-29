#!/usr/bin/env python3
from pycrskrun import niche_all_input, particle_type
import sys
import niche_lib


particle_type_table_without_isotopes = {
    k: v for k, v in particle_type.particle_type_table.items() if "isotope" not in k
}

i_start_seed = 20
particle_type = "p"
# particle_type = "Fe"
min_zenith = 0
max_zenith = 40


# min_energy = 1e15  # eV
# max_energy = 1e16  # eV
# n_shower = 100

min_energy = 1e16
max_energy = 10e16
n_shower = 100


if particle_type not in particle_type_table_without_isotopes:
    print("Available particle types:")
    print(", ".join(particle_type_table_without_isotopes.keys()))
    sys.exit(1)


fn = "{particle}_{emin}-{emax}_x{nshow}".format(
    particle=particle_type.lower(),
    emin="{:.0e}".format(min_energy).replace("+", ""),
    emax="{:.0e}".format(max_energy).replace("+", ""),
    nshow=n_shower
)

array = niche_lib.niche_detector_array.load_location_data()
array.position.x -= (array.position.x.max() + array.position.x.min()) / 2
array.position.y -= (array.position.y.max() + array.position.y.min()) / 2

array.position.x *= 100
array.position.y *= 100


n_det_x = n_det_y = 4
spacing_x = (array.position.x.max() - array.position.x.min()) / (n_det_x - 1)
spacing_y = (array.position.y.max() - array.position.y.min()) / (n_det_y - 1)

spacing_x *= 1.5
spacing_y *= 1.5

f = niche_all_input.niche_all_input()


def set_seeds(i=1):
    def set_seeds(hadron=1, egs4=2, che_photons=3, che_tel_scat=4):
        f.append("SEED", (hadron, 0, 0))
        f.append("SEED", (egs4, 0, 0))
        f.append("SEED", (che_photons, 0, 0))
        f.append("SEED", (che_tel_scat, 0, 0))
    set_seeds(i, i+1, i+2, i+3)


set_seeds(i_start_seed)

x_data = []
y_data = []

# n = 3
n = 2

for i_y in reversed(range(-n, n_det_y + n)):
    for i_x in range(-n, n_det_x + n):
        x = array.position.x.min() + i_x * spacing_x
        y = array.position.y.min() + i_y * spacing_y

        f.append("NICHE_COREPOS", (x, y))

        x_data.append(x)
        y_data.append(y)

xscatt = spacing_x / 2
yscatt = spacing_y / 2

f.append("NSHOW", (n_shower,))
f.append("PRMPAR", (particle_type_table_without_isotopes[particle_type],))
f.append("ERANGE", (min_energy/1e9, max_energy/1e9))
f.append("PHIP", (0, 360))
f.append("THETAP", (min_zenith, max_zenith))
f.append("CSCAT", (20, xscatt, yscatt))
f.append("TELFIL", (f"data/no_thin/iact/{fn}.dat",))

all_input = f.get_extracted()

print(f"save as {fn}")
all_input.save(fn)

# if True:
if False:
    import plotly
    import plotly.express as px
    import numpy as np
    import numpy_utility as npu
    plotly.io.renderers.default = "browser"

    x_reused = (x_data + array.position.x[:, np.newaxis]).flatten()
    y_reused = (y_data + array.position.y[:, np.newaxis]).flatten()

    np.random.seed(0)
    x_scattered = (x_reused + (2 * xscatt * np.random.random(size=20))[:, np.newaxis]).flatten()
    y_scattered = (y_reused + (2 * yscatt * np.random.random(size=20))[:, np.newaxis]).flatten()

    fig = px.scatter(
        npu.to_tidy_data({
            "Orignal": zip(array["position"]["x"], array["position"]["y"]),
            "Reused": zip(x_reused, y_reused),
            "Scattered": zip(x_scattered, y_scattered)
        }, "type", ["x", "y"]),
        x="x", y="y", color="type",
        marginal_x="histogram", marginal_y="histogram"
    )
    fig.update_xaxes(scaleanchor="y", scaleratio=1, constrain="domain", row=1, col=1)
    fig.update_yaxes(scaleanchor="x", scaleratio=1, constrain="domain", row=1, col=1)
    fig.show()

    # data = [
    #     dict(
    #         name="Original",
    #         mode="markers",
    #         x=array.position.x,
    #         y=array.position.y,
    #         marker=dict(
    #             color="red"
    #         )
    #     ),
    #     dict(
    #         name="Reused",
    #         mode="markers",
    #         x=x_reused,
    #         y=y_reused,
    #         marker=dict(
    #             color="blue"
    #         )
    #     ),
    #     dict(
    #         name="Scattered",
    #         mode="markers",
    #         x=x_scattered,
    #         y=y_scattered,
    #         marker=dict(
    #             color="green"
    #         )
    #     )
    # ]
    #
    # import plotly.graph_objects as go
    # fig = go.Figure(data=data)
    # fig.update_xaxes(scaleanchor="y", scaleratio=1, constrain="domain")
    # fig.update_yaxes(scaleanchor="x", scaleratio=1, constrain="domain")
    # fig.show()
