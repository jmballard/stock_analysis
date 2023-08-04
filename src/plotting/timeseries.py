import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp


class TimeSeries:
    """Base class for all our future time series.

    This class sets up all our future time series plots.
    """

    # main colours to be used by our plots
    COLOURS = ["purple", "darkgreen", "mediumslateblue", "darkorange", "red"]

    def __init__(self, pd_ts, title, xlab, ylab, label, y_format):
        """The initialisation of basic time series.

        This is the initialisation of a basic time series plot.

        Args:
            pd_ts (pd.Series): Series, index dated.
            title (str): Main title of plot
            xlab (str): X-axis title
            ylab (str): Y-axis title
            label (str): label in legend
            y_format (str): format of the y axis: 'pct', 'pound','integer' or 'numeric'
        """
        if not isinstance(pd_ts.index, pd.core.indexes.datetimes.DatetimeIndex):
            raise TypeError(
                "The array index does not have an appropriate date-time format."
            )

        self.pd_ts = pd_ts
        self.title = title
        self.xlab = xlab
        self.ylab = ylab
        self.label = label
        self.y_format = y_format

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=pd_ts.index,
                y=pd_ts,
                mode="lines",
                line=dict(color=TimeSeries.COLOURS[0], width=2, dash="solid"),
                showlegend=True,
                name=label,
            )
        )

        fig.update_layout(
            plot_bgcolor="white",
            legend=dict(
                x=0.5,
                xanchor="center",
                yanchor="auto",
            ),
            title={
                "text": title,
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "bottom",
                "font": dict(size=20, color="black"),
            },
            xaxis={
                "title": xlab,
                "showgrid": True,
                "gridwidth": 1,
                "gridcolor": "lightgrey",
                "linecolor": "black",
                "mirror": True,
                "ticks": "outside",
                "showline": True,
                "titlefont": dict(size=16, color="black"),
            },
            yaxis={
                "title": ylab,
                "showgrid": True,
                "gridwidth": 1,
                "gridcolor": "lightgrey",
                "linecolor": "black",
                "mirror": True,
                "ticks": "outside",
                "showline": True,
                "titlefont": dict(size=16, color="black"),
            },
            xaxis_tickformat="%Y-%m",
            xaxis_dtick="M1",
        )

        if y_format == "pct":
            fig.update_layout(yaxis_tickformat="~%")
        elif y_format == "pound":
            fig.update_layout(yaxis_tickprefix="£ ")
        if y_format == "integer":
            fig.update_layout(yaxis_tickformat="~s")
        if y_format == "numeric":
            fig.update_layout(yaxis_tickformat="~s")
        else:
            fig.update_layout(yaxis_tickformat="~s")

        self.fig = fig

    def defaut_layout(self):
        """Set the layout back to default.

        Used to set the layout to default - in case we did too many changes and want to go back to default.
        """
        self.fig.update_layout(
            plot_bgcolor="white",
            legend=dict(
                x=0.5,
                xanchor="center",
                yanchor="auto",
            ),
            title={
                "text": self.title,
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "bottom",
                "font": dict(size=20, color="black"),
            },
            xaxis={
                "title": self.xlab,
                "showgrid": True,
                "gridwidth": 1,
                "gridcolor": "lightgrey",
                "linecolor": "black",
                "mirror": True,
                "ticks": "outside",
                "showline": True,
                "titlefont": dict(size=16, color="black"),
            },
            yaxis={
                "title": self.ylab,
                "showgrid": True,
                "gridwidth": 1,
                "gridcolor": "lightgrey",
                "linecolor": "black",
                "mirror": True,
                "ticks": "outside",
                "showline": True,
                "titlefont": dict(size=16, color="black"),
            },
            xaxis_tickformat="%Y-%m",
            xaxis_dtick="M1",
        )

    def update_xaxis_frequency(self, frequency):
        """Update frequency of x-axis.

        We update frequency of x-axis. Values can be: 'default', 'monthly', 'weekly', or 'quarterly'.

        Args:
            frequency (str): frequency for the x-axis
        """
        if frequency.lower() == "default":  # default is same as monthly
            self.fig.update_layout(xaxis_tickformat="%Y-%m", xaxis_dtick="M1")
        if frequency.lower() == "monthly":
            self.fig.update_layout(xaxis_tickformat="%Y-%m", xaxis_dtick="M1")
        elif frequency.lower() == "weekly":
            self.fig.update_layout(
                xaxis_tickformat="%Y-%m-%d",
                xaxis_dtick=7 * 24 * 60 * 60 * 1000,
                xaxis_tick0="2021-01-04",
            )
        elif frequency.lower() == "quarterly":
            self.fig.update_layout(xaxis_tickformat="%Y-%m", xaxis_dtick="M3")
        else:
            self.fig.update_layout(xaxis_tickformat="%Y-%m", xaxis_dtick="M1")

    def update_yaxis_format(self, y_format):
        """Update format of the y-axis ticks.

        We update the format of the y-axis ticks

        Args:
            y_format (str): format of the y axis: 'pct', 'pound','integer' or 'numeric'
        """
        # change y axis format
        if y_format in ("freq", "pct"):
            self.fig.update_layout(yaxis_tickformat="~%")
        elif y_format in ("severity", "£"):
            self.fig.update_layout(yaxis_tickprefix="£ ")
        elif y_format == "integer":
            self.fig.update_layout(yaxis_tickformat="~s")
        elif y_format == "numeric":
            self.fig.update_layout(yaxis_tickformat="~s")
        else:
            self.fig.update_layout(yaxis_tickformat="~s")

    def update_legend(self, **kwargs):
        """Update legend.

        We update the legend of the plot. Use similar inputs to plotly.
        """
        new_layout = {}
        for var, val in locals()["kwargs"].items():
            new_layout[var] = val
        self.fig.update_layout(legend=new_layout)

    def update_title(self, **kwargs):
        """Update title.

        We update the title of the plot. Use similar inputs to plotly.
        """
        # update the title
        if "text" in locals()["kwargs"].keys():
            self.title = locals()["kwargs"]["text"]

        new_layout = {}
        for var, val in locals()["kwargs"].items():
            new_layout[var] = val

        self.fig.update_layout(title=new_layout)

    def update_axis(self, axis, **kwargs):
        """Update axis.

        We update an axis of the plot. Use similar inputs to plotly.

        Args:
            axis (str): Name of the axis we update (x or y)

        Raises:
            ValueError: if axis is None
            ValueError: if axis is not 'x' or 'y'
        """
        if axis is None:
            raise ValueError(
                "You need to at least give the axis you want to update (x or y)"
            )

        # update the title of the axis in object too
        if "title" in locals()["kwargs"].keys():
            if axis == "x":
                self.xlab = locals()["kwargs"]["title"]
            if axis == "y":
                self.ylab = locals()["kwargs"]["title"]

        new_layout = {}
        for var, val in locals()["kwargs"].items():
            new_layout[var] = val

        if axis == "x":
            self.fig.update_layout(xaxis=new_layout)
        elif axis == "y":
            self.fig.update_layout(yaxis=new_layout)
        else:
            raise ValueError(f"The axis should be 'x' or 'y' ({axis})")

    def breakdown_traces(self):
        """Breaks all the traces.

        This functions breaks all the traces from a plotly figure.

        Returns:
            list: traces of a figure
        """
        traces = []
        for trace in range(len(self.fig["data"])):
            traces.append(self.fig["data"][trace])
        return traces

    def show(self):
        """Show the plot.

        Show the timeseries plot
        """
        self.fig.show()
