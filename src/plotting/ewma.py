import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

from .timeseries import TimeSeries


class Ewma(TimeSeries):
    """Base class for EWMA time series.

    This class sets up all EWMA time series plots.
    """

    def __init__(
        self,
        pd_ts,
        title,
        xlab,
        ylab,
        label,
        y_format,
        control_multiple=5,
        smoothing_factor=0.3,
    ):
        """The initialisation of EWMA series.

        This is the initialisation of a EWMA time series

        Args:
            pd_ts (pd.Series): Series, index dated.
            title (str): Main title of plot
            xlab (str): X-axis title
            ylab (str): Y-axis title
            label (str): label in legend
            y_format (str): format of the y axis: 'pct', 'pound','integer' or 'numeric'
            control_multiple (int or float, optional): Scalar multiple applied to control limits. Defaults to 5.
            smoothing_factor (float, optional): Smoothing factor or weight applied to most recent observation. Defaults to 0.3.
        """
        m = pd_ts.mean()
        s = pd_ts.std()

        n = len(pd.date_range(pd_ts.index.min(), pd_ts.index.max(), freq="M"))

        # tolerance
        i = pd.Series([j for j in range(1, len(pd_ts) + 1)], index=pd_ts.index)
        tolerance = ((control_multiple * s) / np.sqrt(n)) * np.sqrt(
            (smoothing_factor / (2 - smoothing_factor))
            * (1 - (1 - smoothing_factor) ** (2 * i))
        )

        # controls
        control_upper = pd.Series(m + tolerance)
        control_lower = pd.Series(m - tolerance)

        ewma = pd.Series(index=pd_ts.index, dtype=float)
        ewma[0] = pd_ts[0]

        for j in range(1, len(pd_ts)):
            ewma[j] = smoothing_factor * pd_ts[j] + (1 - smoothing_factor) * ewma[j - 1]

        ts = TimeSeries(ewma, title, xlab, ylab, label, y_format)
        self.pd_ts = ts.pd_ts
        self.title = ts.title
        self.xlab = ts.xlab
        self.ylab = ts.ylab
        self.label = ts.label
        self.y_format = ts.y_format

        # now create the plot
        fig = ts.fig

        # add the average and control lines
        fig.add_hline(y=m, line_width=2, line_dash="solid", line_color="darkgreen")
        fig.add_trace(
            go.Scatter(
                x=pd_ts.index,
                y=control_upper,
                mode="lines",
                line=dict(color="darkorange", width=2, dash="dash"),
                showlegend=False,
            )
        )
        fig.add_trace(
            go.Scatter(
                x=pd_ts.index,
                y=control_lower,
                mode="lines",
                line=dict(color="darkorange", width=2, dash="dash"),
                showlegend=False,
            )
        )
        self.fig = fig
