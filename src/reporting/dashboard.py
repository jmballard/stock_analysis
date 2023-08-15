import datetime
import os
import sys
from pathlib import Path

import dash
import plotly
from dash import Dash, Input, Output, State, callback, dash_table, dcc, html

# get the folder of this analysis
sys.path.append(os.path.abspath(Path(__file__).parents[2]))
from config import parameters  # noqa
from src.data.financial_data import FinancialData  # noqa
from src.plotting.timeseries import TimeSeries  # noqa

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    html.Div(
        [
            html.H1("My finance dashboard"),
            dcc.Dropdown(
                id="choice_company",
                options=parameters.companies_of_interest,
                value="ROO.L",
                clearable=False,
                searchable=True,
            ),
            html.P("Results:"),
            html.Div(id="info-header"),
            dcc.Graph(id="live-update-graph"),
            dcc.Interval(
                id="interval-component",
                interval=100 * 1000,  # in milliseconds
                n_intervals=0,
            ),
        ]
    )
)


@callback(
    Output("info-header", "children"),
    Input("interval-component", "n_intervals"),
    State("choice_company", "value"),
)
def update_data(n, name):
    company = FinancialData(name)

    latest = company.live_data.index.max()

    info_data = company.live_data.head().reset_index(drop=False)

    columns = [{"name": i, "id": i} for i in info_data.columns]
    return [
        html.Span(f"Latest data is: {latest}", style={"color": "red"}),
        dash_table.DataTable(info_data.to_dict("records"), columns),
    ]


@callback(
    Output("live-update-graph", "figure"),
    Input("interval-component", "n_intervals"),
    State("choice_company", "value"),
)
def update_graph_live(n, name):
    company = FinancialData(name)

    live_data = company.live_data.reset_index(drop=False).set_index("corrected_time")

    fig = TimeSeries(
        live_data["Open"], "Live Data", "Date", "Opening value", "Value", "pound"
    )

    fig.update_xaxis_frequency(frequency="daily")

    return fig.fig


if __name__ == "__main__":
    app.run(debug=True)
