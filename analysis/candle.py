import talib as ta 
import pandas as pd

def analysis_engulfing(open, high, low, close):
    engulfing = ta.CDLENGULFING(open, high, low, close)
    return engulfing


# TODO: get more candle stick pattern 