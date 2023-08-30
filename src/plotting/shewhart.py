import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

from .timeseries import TimeSeries


class Shewhart(TimeSeries):
    """Base class for Shewhart time series.

    This class sets up all Shewhart time series plots.
    """

    WARNING = 2
    ACTION = 3

    def __init__(self, pd_ts, title, xlab, ylab, label, y_format, filter_iqr=False):
        """The initialisation of basic time series.

        This is the initialisation of a basic time series plot.

        Args:
            pd_ts (pd.Series): Series, index dated.
            title (str): Main title of plot
            xlab (str): X-axis title
            ylab (str): Y-axis title
            label (str): label in legend
            y_format (str): format of the y axis: 'pct', 'pound','integer' or 'numeric'
            filter_iqr (bool, optional): Choice if we filter for IQR or not. Defaults to False.
        """
        if filter_iqr:
            upper_q = pd_ts.quantile(0.75)
            lower_q = pd_ts.quantile(0.25)
            iqr = upper_q - lower_q
            pd_ts = pd_ts[
                (pd_ts >= (lower_q - 1.5 * iqr)) & (pd_ts <= (upper_q + 1.5 * iqr))
            ]

        ts = TimeSeries(pd_ts, title, xlab, ylab, label, y_format)

        self.pd_ts = ts.pd_ts
        self.title = ts.title
        self.xlab = ts.xlab
        self.ylab = ts.ylab
        self.label = ts.label
        self.y_format = ts.y_format

        m = pd_ts.mean()
        s = pd_ts.std()

        # uppers
        upper_warning = m + self.WARNING * s
        upper_action = m + self.ACTION * s

        # lowers
        lower_warning = m - self.WARNING * s
        lower_action = m - self.ACTION * s

        y_max = max(m + 5 * s, pd_ts.max())
        y_min = min(m - 5 * s, pd_ts.min())

        # if same, we make just y_max slightly higher (should never happen)
        if y_max == y_min:
            y_max += 0.00001

        fig = ts.fig

        # add the average, action and warning lines
        fig.add_hline(y=m, line_width=2, line_dash="solid", line_color="darkgreen")
        fig.add_hline(
            y=upper_warning, line_width=2, line_dash="dash", line_color="darkorange"
        )
        fig.add_hline(
            y=lower_warning, line_width=2, line_dash="dash", line_color="darkorange"
        )
        fig.add_hline(y=upper_action, line_width=2, line_dash="dash", line_color="red")
        fig.add_hline(y=lower_action, line_width=2, line_dash="dash", line_color="red")

        self.fig = fig
