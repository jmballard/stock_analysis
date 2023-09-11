import numpy as np
import pandas as pd
from sktime.forecasting.arima import ARIMA
from sktime.forecasting.base import ForecastingHorizon
from sktime.performance_metrics.forecasting import MeanAbsolutePercentageError
import plotly.graph_objects as go

from ..plotting.timeseries import TimeSeries


class ARIMAModel:
    def __init__(self, p=1, d=1, q=1):
        """Initialize an ARIMA model with the specified order.

        Args:
            p (int): The order of autoregressive (AR) component.
            d (int): The order of differencing.
            q (int): The order of moving average (MA) component.
        """
        self.p = p
        self.d = d
        self.q = q
        self.model = None

    def fit(self, train_series):
        """Fit the ARIMA model to the training time series data.

        Args:
            train_series (pd.Series): The training time series data.

        Returns:
        - None
        """
        self.model = ARIMA(order=(self.p, self.d, self.q))
        self.model.fit(train_series)

    def predict(self, test):
        """Make predictions for future time periods.

        Args:
            test (pd.Series): The test time series data.

        Returns:
            pd.Series: The forecasted values.
        """
        if self.model is None:
            raise ValueError(
                "Model has not been fitted. Please call 'fit' method first."
            )
        fh = ForecastingHorizon(test.index, is_relative=False)
        forecast = self.model.predict(fh=fh)
        return forecast

    def predict_interval(self, test, coverage):
        """Predict the confidence interval for future time periods.

        Args:
            test (pd.Series): The test time series data.
            coverage (float): nominal coverage of the prediction interval(s) queried

        Returns:
            pd.Series: The forecasted values.
        """
        if self.model is None:
            raise ValueError(
                "Model has not been fitted. Please call 'fit' method first."
            )
        fh = ForecastingHorizon(test.index, is_relative=False)
        forecast = self.model.predict_interval(fh=fh, coverage=coverage)
        return forecast

    def evaluate(self, test):
        """Evaluate the model's performance on a test time series using MAPE.

        Args:
            test (pd.Series): The test time series data.

        Returns:
            float: The MAPE (Mean Absolute Percentage Error) score.
        """
        if self.model is None:
            raise ValueError(
                "Model has not been fitted. Please call 'fit' method first."
            )
        predictions = self.predict(test)
        mape = MeanAbsolutePercentageError(test, predictions)
        return mape

    def plot(self, test, title, xlab, ylab, label, yformat):
        """Plot the forecasted values.

        Args:
            steps (int): Number of steps to forecast into the future and plot.

        Returns:
            None
        """
        if self.model is None:
            raise ValueError("You must fit the model before plotting the forecast.")

        # train subset
        pd_ts = pd.concat([self.model._y, test])
        if ~isinstance(pd_ts.index, pd.DatetimeIndex):
            try:
                # Try to convert the index to a datetime index
                pd_ts.index = pd_ts.index.to_timestamp()
            except ValueError:
                print(
                    "Unable to convert the index to a datetime index. Please check the format of the index."
                )

        ts = TimeSeries(pd_ts, None, title, xlab, ylab, label, yformat)

        forecast_values = self.predict(test)
        forecast_intervals = self.predict_interval(test, coverage=0.9)
        forecast_values.index = forecast_values.index.to_timestamp()
        ts.fig.add_trace(
            go.Scatter(
                x=forecast_values.index,
                y=forecast_values,
                mode="lines",
                line=dict(color=TimeSeries.COLOURS[1], width=2, dash="dot"),
                showlegend=True,
                name="Forecast",
            )
        )

        ts.fig.add_trace(
            go.Scatter(
                x=forecast_values.index,
                y=forecast_intervals[("Open", 0.9, "lower")],
                mode="lines",
                line=dict(color=TimeSeries.COLOURS[3], width=1, dash="dash"),
                showlegend=False,
            )
        )
        ts.fig.add_trace(
            go.Scatter(
                x=forecast_values.index,
                y=forecast_intervals[("Open", 0.9, "upper")],
                mode="lines",
                line=dict(color=TimeSeries.COLOURS[3], width=1, dash="dash"),
                fill="tonexty",
                fillcolor="rgba(255, 0, 0, 0.2)",
                showlegend=False,
            )
        )

        return ts.fig
