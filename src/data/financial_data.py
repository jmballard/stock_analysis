import time

import numpy as np
import pandas as pd
import yfinance as yf
from tqdm import tqdm


class FinancialData:
    """Class for the financial data. One object contains all the details for a company."""

    def __init__(self, name_company):
        """Initialisation.

        We initialise our data for a specific company name.

        Args:
            name_company (string): name of the company we will download
        """
        self.name_company = name_company
        self.ticker = yf.Ticker(self.name_company)
        self.info = self.ticker.info

        # get the historical data
        history = self.ticker.history(period="max")
        history.index = pd.to_datetime(history.index)
        history["Company"] = self.name_company
        self.history = history

        # get the up to date data by minute
        live_data = yf.download(tickers=self.name_company, period="max", interval="1m")
        if live_data.shape[0] > 0:
            live_data["date_raw"] = pd.to_datetime(live_data.index)
            live_data["date"] = live_data["date_raw"].dt.date
            live_data["time"] = live_data["date_raw"].dt.time
            live_data["second_full"] = (
                live_data["date_raw"].dt.second
                + live_data["date_raw"].dt.minute * 60
                + live_data["date_raw"].dt.hour * 60 * 60
            )

            opening_time = live_data["time"].min()
            closing_time = live_data["time"].max()

            print(opening_time)

            opening_time_secs = (
                opening_time.hour * 3600
                + opening_time.minute * 60
                + opening_time.second
            )
            closing_time_secs = (
                closing_time.hour * 3600
                + closing_time.minute * 60
                + closing_time.second
            )

            live_data["days_in_sec"] = live_data["date"].apply(
                lambda x: time.mktime(x.timetuple())
            )
            live_data["corrected_second_full"] = (
                np.floor(
                    (live_data["second_full"] - opening_time_secs)
                    / (closing_time_secs - opening_time_secs)
                    * 60
                    * 60
                    * 24
                )
                + live_data["days_in_sec"]
            )
            live_data["corrected_time"] = pd.to_datetime(
                live_data["corrected_second_full"], unit="s"
            )

        self.live_data = live_data

    def update_info(self):
        """Update info.

        We update all info on the company.
        """
        self.ticker = yf.Ticker(self.name_company)
        self.info = self.ticker.info

    def update_history(self):
        """Update history.

        We update all history on the company.
        """
        self.ticker = yf.Ticker(self.name_company)
        history = self.ticker.history(period="max")
        history.index = pd.to_datetime(history.index)
        history["Company"] = self.name_company
        self.history = history

    def update_live_values(self):
        """Update live values.

        We update all live values on the company, by the minute.
        """
        self.live_data = yf.download(
            tickers=self.name_company, period="max", interval="1m"
        )

    def get_info(self):
        """Get information.

        We get the information of the company.

        Returns:
            dict: information on company
        """
        return self.info

    def get_history(self):
        """Get history.

        We get the history of the company.

        Returns:
            pd.DataFrame: history of company
        """
        return self.history

    def get_live(self):
        """Get live data.

        We get the live data of the company.

        Returns:
            pd.DataFrame: live data of company
        """
        return self.live_data

    def save_live_data(self, file_path):
        """Save live data in CSV file.

        We save the live data into a csv file to possibly be reused later.

        Args:
            file_path (string): path to where we save the file - with filename and extension.
        """
        self.live_data.to_csv(file_path)
