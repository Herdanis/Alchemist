import ccxt
from ccxt.base.errors import RequestTimeout
import pandas as pd
import time
from dotenv import load_dotenv
import os
import ta
from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError
import talib
from datetime import datetime

# Load API key and secret from .env file (optional)
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Initialize Binance Futures API connection
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})
position_status = None
entry_price = None
exchange.set_sandbox_mode(True)
amount_usdt = 100 

# Main trading loop
symbol = 'ETH/USDT'
timeframe = '1m'
leverage = 25  # Set the desired leverage value
take_profit_pct = 0.02  # 2%
stop_loss_pct = 0.01  # 1%

def get_historical_data(exchange, symbol, timeframe):
    while True:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except (ReadTimeout, ReadTimeoutError, RequestTimeout):
            print("Read timeout error occurred. Retrying in 3 seconds...")
            time.sleep(2)

def set_leverage(exchange, symbol, leverage):
    params = {'symbol': exchange.market_id(symbol), 'leverage': leverage}
    return exchange.fapiPrivate_post_leverage(params)

def get_market_price(exchange, symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker['last']

def strategy(df, position_status, entry_price, take_profit_pct, stop_loss_pct):
    # Calculate SMA with periods of 20, 50, and 100
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    df['sma_100'] = df['close'].rolling(window=100).mean()

    # Calculate MACD
    exp12 = df['close'].ewm(span=12, adjust=False).mean()
    exp26 = df['close'].ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()
    df['macd_hist'] = macd - signal

    # Add Open Interest (OI) data
    # Note: Replace this with actual Open Interest data from the exchange
    df['open_interest'] = pd.Series([0] * len(df), index=df.index)

    last_close = df['close'].iloc[-1]

    # Implement your trading strategy using the indicators
    buy_signal = (
        df['sma_20'].iloc[-1] > df['sma_50'].iloc[-1] and
        df['sma_50'].iloc[-1] > df['sma_100'].iloc[-1] and
        df['macd_hist'].iloc[-1] > 0
    )

    sell_signal = (
        df['sma_20'].iloc[-1] < df['sma_50'].iloc[-1] and
        df['sma_50'].iloc[-1] < df['sma_100'].iloc[-1] and
        df['macd_hist'].iloc[-1] < 0
    )

    if position_status is None:
        if buy_signal:
            return "open_long", last_close
        elif sell_signal:
            return "open_short", last_close
    elif position_status == "long":
        take_profit = entry_price * (1 + take_profit_pct)
        stop_loss = entry_price * (1 - stop_loss_pct)
        close_long = (
            last_close >= take_profit or
            last_close <= stop_loss
        )
        if close_long:
            return "close_long", last_close
    elif position_status == "short":
        take_profit = entry_price * (1 - take_profit_pct)
        stop_loss = entry_price * (1 + stop_loss_pct)
        close_short = (
            last_close <= take_profit or
            last_close >= stop_loss
        )
        if close_short:
            return "close_short", last_close

    return position_status, entry_price

def get_balance():
    balance = exchange.fetch_balance()
    usdt_balance = balance['total']['USDT']
    coin_balance = balance['total'][symbol.split('/')[0]]

    return usdt_balance, coin_balance

# Load markets for the exchange
exchange.load_markets()

# Set leverage for the trading pair
set_leverage(exchange, symbol, leverage)

# Main trading loop
while True:
    df = get_historical_data(exchange, symbol, timeframe)
    position_status, entry_price = strategy(df, position_status, entry_price, take_profit_pct, stop_loss_pct)
    usdt_balance, coin_balance = get_balance()
    
    market_price = get_market_price(exchange, symbol)
    position_size_base = amount_usdt / market_price
    
    # datetime object containing current date and time
    get_time = datetime.now()
    now = get_time.strftime("%H:%M:%S")
    
    print(f"USDT Balance: {usdt_balance:.2f}")
    print(f"{symbol.split('/')[0]} Balance: {coin_balance:.8f}")
    print(f"{now} at {market_price} USDT")
    
    if position_status == "open_long":
        market_price = get_market_price(exchange, symbol)
        position_size_base = amount_usdt / market_price
        order = exchange.create_market_order(symbol, 'buy', position_size_base)
        position_status = "long"
        print("Opening long position at", entry_price)
    elif position_status == "close_long":
        market_price = get_market_price(exchange, symbol)
        position_size_base = amount_usdt / market_price
        order = exchange.create_market_order(symbol, 'sell', position_size_base)
        position_status = None
        print("Closing long position at", entry_price)
    elif position_status == "open_short":
        market_price = get_market_price(exchange, symbol)
        position_size_base = amount_usdt / market_price
        order = exchange.create_market_order(symbol, 'sell', position_size_base)
        position_status = "short"
        print("Opening short position at", entry_price)
    elif position_status == "close_short":
        market_price = get_market_price(exchange, symbol)
        position_size_base = amount_usdt / market_price
        order = exchange.create_market_order(symbol, 'buy', position_size_base)
        position_status = None
        print("Closing short position at", entry_price)

    # time.sleep(exchange.parse_timeframe(timeframe) * 60)
    time.sleep(1)

