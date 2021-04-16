#!/usr/bin/env python3
import sys
import pycrskrun.all_input
import pandas as pd
import plotly.express as px
import plotly
plotly.io.renderers.default = "browser"


sys.argv += ("p_1e15-1e16_mc8x8_x100_v2",)
fn = sys.argv[1]

ai = pycrskrun.all_input.all_input(fn)
telescopes = pd.DataFrame(
    ai["TELESCOPE"]["args"].to_numpy([("x", float), ("y", float), ("z", float), ("r", float)])
)
telescopes["names"] = ai["TELESCOPE"]["comment"].to_numpy(str)
telescopes["numbers"] = [str(i) for i in range(len(telescopes) // 14) for _ in range(14)]

telescopes["x"] /= 100
telescopes["y"] /= 100

telescopes[["x", "y"]] = telescopes[["y", "x"]]
telescopes["x"] *= -1

axes_layout = dict(
    xaxis=dict(
        title="X (to East)",
        ticksuffix=" m",
        dtick=100
    ),
    yaxis=dict(
        title="Y (to North)",
        ticksuffix=" m",
        dtick=100
    )
)

px.scatter(telescopes, x="x", y="y", color="names").update_layout(axes_layout).show()
px.scatter(telescopes, x="x", y="y", color="numbers").update_layout(axes_layout).show()
