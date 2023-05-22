import pandas as pd
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
import time
from ccxt.base.errors import RequestTimeout
import requests
from typing import Optional

from data import getExchange as exchange

ex = exchange.binanceExchange()


def get_historical_data(symbol: str, timeframe: str, hours_ago=None) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given symbol and timeframe.

    Parameters:
    symbol (str): Symbol for which to fetch data
    timeframe (str): Timeframe for which to fetch data

    Returns:
    pd.DataFrame: DataFrame with historical data
    """
    while True:
        try:
            if hours_ago is not None:
                since = ex.milliseconds() - hours_ago * 60 * 60 * 1000
            else:
                since = None
            ohlcv = ex.fetch_ohlcv(symbol, timeframe, since=since)
            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df.set_index("timestamp", inplace=True)
            return df
        except (ReadTimeout, ReadTimeoutError, RequestTimeout) as e:
            print(f"Error occurred: {e}. Retrying in 3 seconds...")
            time.sleep(3)

def get_market_price(symbol: str) -> Optional[float]:
    """
    Fetch the last market price for a given symbol.

    Parameters:
    symbol (str): Symbol for which to fetch the price

    Returns:
    float: Last market price
    """
    while True:
        try:
            ticker = ex.fetch_ticker(symbol)
            return ticker["last"]
        except requests.exceptions.HTTPError as e:
            print(f"Error occurred: {e}. Retrying in 3 seconds...")
            time.sleep(3)


def get_balance(symbol: str) -> Optional[float]:
    """
    Fetch the total balance for a given symbol.

    Parameters:
    symbol (str): Symbol for which to fetch the balance

    Returns:
    float: Total balance
    """
    try:
        balance = ex.fetch_balance()
        total_balance = balance["total"][symbol.split("/")[1]]
        return total_balance
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
