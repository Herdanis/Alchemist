import talib as ta 

def analysis_sma(close_price, periode):
    sma = ta.SMA(close_price,periode)
    return sma

def analysis_ema(close_price, periode):
    ema = ta.EMA(close_price,periode)
    return ema

def analysis_macd(close_price):
    macd_line, signal_line, histogram = ta.MACD(close_price,12,26,9)
    return macd_line, signal_line, histogram

# TODO: get open interest



def analysis_rsi(close_price):
    rsi = ta.RSI(close_price)
    return rsi