import sys
import pycrskrun.all_input
import pandas as pd
import plotly.express as px

sys.argv += ("/Users/yomura/p15-16_mc_x100",)
fn = sys.argv[1]

ai = pycrskrun.all_input.all_input(fn)
telescopes = pd.DataFrame(
    ai["TELESCOPE"]["args"].to_numpy([("x", float), ("y", float), ("z", float), ("r", float)])
)
telescopes["names"] = ai["TELESCOPE"]["comment"].to_numpy(str)
telescopes["numbers"] = [str(i) for i in range(len(telescopes) // 14) for _ in range(14)]

telescopes["x"] /= 100
telescopes["y"] /= 100

axes_layout = dict(
    xaxis=dict(
        title="X",
        ticksuffix=" m",
        dtick=100
    ),
    yaxis=dict(
        title="Y",
        ticksuffix=" m",
        dtick=100
    )
)

px.scatter(telescopes, x="x", y="y", color="names").update_layout(axes_layout).show()
px.scatter(telescopes, x="x", y="y", color="numbers").update_layout(axes_layout).show()
