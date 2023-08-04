import os

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import scipy.stats

from .timeseries import TimeSeries


class Cusum(TimeSeries):
    WARNING = 2.0
    ACTION = 3.0

    BETA = 0.01
    DELTA = 1.0

    def __init__(self, pd_ts, title, xlab, ylab, label, y_format, filter_iqr=False):
        m = pd_ts.mean()

        # print(S_lo)
        # calculate running cusum
        running_cusum = pd_ts.cumsum() - [n * m for n in range(1, 1 + len(pd_ts))]

        self.pd_ts = pd_ts
        self.title = title
        self.xlab = xlab
        self.ylab = ylab
        self.label = label
        self.y_format = y_format

        # Create figure with secondary y-axis
        fig = sp.make_subplots(specs=[[{"secondary_y": True}]])

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
        fig.add_hline(
            y=m,
            line_width=2,
            line_dash="dash",
            line_color=TimeSeries.COLOURS[1],
            annotation_text="Average",
            annotation_position="top right",
            annotation_font_size=14,
            annotation_font_color=TimeSeries.COLOURS[1],
        )
        fig.add_trace(
            go.Scatter(
                x=pd_ts.index,
                y=running_cusum,
                line=dict(color=TimeSeries.COLOURS[2], width=2, dash="solid"),
                showlegend=False,
            ),
            secondary_y=True,
        )

        fig.update_layout(
            plot_bgcolor="white",
            legend=dict(
                x=0.9,
                xanchor="auto",
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
            yaxis2=dict(
                title="Cumulative sum vs average",
                titlefont=dict(color=TimeSeries.COLOURS[2]),
                tickfont=dict(color=TimeSeries.COLOURS[2]),
                side="right",
            ),
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
                x=0.9,
                xanchor="auto",
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
            yaxis2=dict(
                title="Cumulative sum vs average",
                titlefont=dict(color=TimeSeries.COLOURS[2]),
                tickfont=dict(color=TimeSeries.COLOURS[2]),
                side="right",
            ),
            xaxis_tickformat="%Y-%m",
            xaxis_dtick="M1",
        )
