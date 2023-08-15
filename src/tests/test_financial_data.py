import os
import sys

import pandas as pd
import yfinance as yf
from dateutil import parser

# Add the parent directory of this file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from data.financial_data import FinancialData  # noqa: E402


def test_init():
    """test initialisation of FinancialData.

    We test initialisation of FinancialData.
    """
    test_fd = FinancialData("test")

    assert test_fd.name_company == "test"
    #    assert test_fd.ticker == yf.Ticker("test") # we cannot match these with a simple ==
    assert test_fd.info == {
        "exchange": "YHD",
        "quoteType": "MUTUALFUND",
        "symbol": "TEST",
        "underlyingSymbol": "TEST",
        "firstTradeDateEpochUtc": 1528810200,
        "timeZoneFullName": "America/New_York",
        "timeZoneShortName": "EDT",
        "uuid": "033bd94b-1168-37e4-b0d6-44c3c95e35bf",
        "gmtOffSetMilliseconds": -14400000,
        "maxAge": 86400,
        "trailingPegRatio": None,
    }

    to_match = pd.DataFrame(
        {
            "Date": [parser.parse("2018-06-12 00:00:00 -0400")],
            "Open": [0.5],
            "High": [0.5],
            "Low": [0.4399999976158142],
            "Close": [0.4449999928474426],
            "Volume": [173850],
            "Dividends": [0.0],
            "Stock Splits": [0.0],
            "Capital Gains": [0.0],
            "Company": ["test"],
        }
    ).set_index("Date")
    assert all(
        test_fd.history.reset_index(drop=False) == to_match.reset_index(drop=False)
    )

    to_match = pd.DataFrame(
        {
            "Date": [],
            "Open": [],
            "High": [],
            "Low": [],
            "Close": [],
            "Adj Close": [],
            "Volume": [],
        }
    ).set_index("Date")

    assert all(
        test_fd.live_data.reset_index(drop=False) == to_match.reset_index(drop=False)
    )


def test_update_info():
    """Test update_info.

    We test update_info.
    """
    test_fd = FinancialData("test")
    test_fd.update_info()
    assert test_fd.info == {
        "exchange": "YHD",
        "quoteType": "MUTUALFUND",
        "symbol": "TEST",
        "underlyingSymbol": "TEST",
        "firstTradeDateEpochUtc": 1528810200,
        "timeZoneFullName": "America/New_York",
        "timeZoneShortName": "EDT",
        "uuid": "033bd94b-1168-37e4-b0d6-44c3c95e35bf",
        "gmtOffSetMilliseconds": -14400000,
        "maxAge": 86400,
        "trailingPegRatio": None,
    }


def test_update_history():
    """Test update_history.

    We test update_history.
    """
    test_fd = FinancialData("test")
    test_fd.update_history()

    to_match = pd.DataFrame(
        {
            "Date": [parser.parse("2018-06-12 00:00:00 -0400")],
            "Open": [0.5],
            "High": [0.5],
            "Low": [0.4399999976158142],
            "Close": [0.4449999928474426],
            "Volume": [173850],
            "Dividends": [0.0],
            "Stock Splits": [0.0],
            "Capital Gains": [0.0],
            "Company": ["test"],
        }
    ).set_index("Date")

    assert all(
        test_fd.history.reset_index(drop=False) == to_match.reset_index(drop=False)
    )


def test_update_live_values():
    """Test update_live_values.

    We test update_live_values.
    """
    test_fd = FinancialData("test")
    test_fd.update_live_values()

    to_match = pd.DataFrame(
        {
            "Date": [],
            "Open": [],
            "High": [],
            "Low": [],
            "Close": [],
            "Adj Close": [],
            "Volume": [],
        }
    ).set_index("Date")

    assert all(
        test_fd.live_data.reset_index(drop=False) == to_match.reset_index(drop=False)
    )


def test_get_info():
    """Test get_info.

    We test get_info.
    """
    test_fd = FinancialData("test")
    assert all(test_fd.get_info == pd.DataFrame())


def test_get_history():
    """Test get_history.

    We test get_history.
    """
    test_fd = FinancialData("test")
    assert all(test_fd.get_history == pd.DataFrame())


def test_get_live():
    """Test get_live.

    We test get_live.
    """
    test_fd = FinancialData("test")
    assert all(test_fd.get_live == pd.DataFrame())
