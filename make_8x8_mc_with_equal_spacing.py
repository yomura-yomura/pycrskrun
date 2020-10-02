#!/usr/bin/env python3
import sys
from simu.corsika.iact import niche_eventio
# Remove isotopes, Switch keys and values
particle_type_table = {v: k for k, v in niche_eventio.particle_type.table.items() if "isotope" not in v}

version = 2  # will change seeds, starts from 1

particle_type = "p"
#particle_type = "Fe"
if particle_type not in particle_type_table:
    print("Available particle types:")
    print(", ".join(particle_type_table.keys()))
    sys.exit(1)

min_energy = 1e15  # eV
max_energy = 1e16  # eV

#min_energy = 1e16
#max_energy = 5e16

n_shower = 100

fn = "{particle}_{emin}-{emax}_mc8x8_x{nshow}_v{version}".format(
    particle=particle_type.lower(),
    emin="{:.0e}".format(min_energy).replace("+", ""),
    emax="{:.0e}".format(max_energy).replace("+", ""),
    nshow=n_shower,
    version=version
)

min_zenith = 0
max_zenith = 20
# max_zenith = 50


import niche_lib
array = niche_lib.niche_detector_array.load_location_data()
array.position.x -= (array.position.x.max() + array.position.x.min()) / 2
array.position.y -= (array.position.y.max() + array.position.y.min()) / 2

array.position.x *= 100
array.position.y *= 100


n_det_x = n_det_y = 4
spacing_x = (array.position.x.max() - array.position.x.min()) / (n_det_x - 1)
spacing_y = (array.position.y.max() - array.position.y.min()) / (n_det_y - 1)


from simu.corsika.pycrskrun import niche_all_input
f = niche_all_input.niche_all_input()


def set_seeds(i=1):
    def set_seeds(hadron=1, egs4=2, che_photons=3, che_tel_scat=4):
        f.append("SEED", (hadron, 0, 0))
        f.append("SEED", (egs4, 0, 0))
        f.append("SEED", (che_photons, 0, 0))
        f.append("SEED", (che_tel_scat, 0, 0))
    set_seeds(i, i+1, i+2, i+3)


set_seeds(version)
    
x_data = []
y_data = []

# for i_y in reversed(range(-1, n_det_y + 1 + 1)):
#     for i_x in range(-1, n_det_x + 1 + 1):
for i_y in reversed(range(-2, n_det_y + 2)):
    for i_x in range(-2, n_det_x + 2):
        x = array.position.x.min() + i_x * spacing_x
        y = array.position.y.min() + i_y * spacing_y

        f.append("NICHE_COREPOS", (x, y))
        
        x_data.append(x)
        y_data.append(y)


f.append("NSHOW", (n_shower,))
f.append("PRMPAR", (particle_type_table[particle_type],))
f.append("ERANGE", (min_energy/1e9, max_energy/1e9))
f.append("PHIP", (0, 360))
f.append("THETAP", (min_zenith, max_zenith))
f.append("CSCAT", (20, spacing_x/2, spacing_y/2))
f.append("TELFIL", (f"data/no_thin/iact/{fn}.dat",))

all_input = f.get_extracted()

print(f"save as {fn}")
all_input.save(fn)

if False:
    data = [
        dict(
            mode = "markers",
            x = array.position.x,
            y = array.position.y,
            marker = dict(
                color = "red"
                )
            ),
        dict(
            mode = "markers",
            x = x_data,
            y = y_data,
            marker = dict(
                color = "blue"
                )
            )
        ]

    import plotly.graph_objects as go
    fig = go.Figure(data=data)
    fig.show()
