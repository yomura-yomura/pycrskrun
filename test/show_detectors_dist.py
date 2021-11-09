#!/usr/bin/env python3
import sys
import pycrskrun.all_input
import pandas as pd
import plotly.express as px
import plotly
plotly.io.renderers.default = "browser"


def main(fn, auto_open=True):
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
            title="X (West to East)",
            ticksuffix=" m",
            dtick=150,
            scaleanchor="y",
            constrain="domain",
            zeroline=True,
            zerolinewidth=3
        ),
        yaxis=dict(
            title="Y (South to North)",
            ticksuffix=" m",
            dtick=150,
            scaleanchor="x",
            constrain="domain",
            zeroline=True,
            zerolinewidth=3
        )
    )

    fig1 = px.scatter(telescopes, x="x", y="y", color="names").update_layout(axes_layout)
    fig2 = px.scatter(
        telescopes, x="x", y="y", color="numbers",
        color_discrete_sequence=px.colors.qualitative.Alphabet
    ).update_layout(axes_layout)
    fig2.update_layout(width=1000, height=1000)
    if auto_open:
        fig1.show()
        fig2.show()
    return fig1, fig2


if __name__ == "__main__":
    sys.argv += ("p_1e15-1e16_mc8x8_x100_v2",)
    fn = sys.argv[1]
    main(fn, auto_open=True)
