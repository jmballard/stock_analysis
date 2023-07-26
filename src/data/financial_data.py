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
        self.live_data = yf.download(
            tickers=self.name_company, period="max", interval="1m"
        )

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
