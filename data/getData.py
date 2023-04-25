import pandas as pd
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
import time
from ccxt.base.errors import RequestTimeout
import requests

from data.getExchage import binanceExchange as exchange

ex = exchange()

def get_historical_data(symbol, timeframe):
    while True:
        try:
            ohlcv = ex.fetch_ohlcv(symbol, timeframe)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'],)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except (ReadTimeout, ReadTimeoutError, RequestTimeout):
            print("Read timeout error occurred. Retrying in 3 seconds...")
            time.sleep(2)
            
def get_market_price(symbol):
    while True:
        try:
            ticker = ex.fetch_ticker(symbol)
            return ticker['last']
        except requests.exceptions.HTTPError as e:
            print("502 Server Error: Bad Gateway. Retrying in 3 seconds...")
            time.sleep(2)
            
def get_balance(symbol):
    balance = ex.fetch_balance()
    total_balance = balance['total'][symbol.split('/')[1]]

    return total_balance