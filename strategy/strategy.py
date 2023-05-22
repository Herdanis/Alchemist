import pandas as pd
from typing import Tuple, Optional
from analysis import analysis_sma, analysis_macd, analysis_rsi

def strategy(df: pd.DataFrame, position_status: Optional[str], entry_price: Optional[float], take_profit_pct: float, stop_loss_pct: float) -> Tuple[Optional[str], Optional[float]]:
    """
    Implement a trading strategy based on SMA, MACD, and RSI indicators.

    Parameters:
    df (pd.DataFrame): DataFrame with historical data
    position_status (str): Current position status ("long", "short", or None)
    entry_price (float): Entry price for the current position
    take_profit_pct (float): Take profit percentage
    stop_loss_pct (float): Stop loss percentage

    Returns:
    tuple: Updated position status and entry price
    """
    # Calculate SMA with periods of 20 and 50
    df['sma_20'] = analysis_sma(df['close'], 20)
    df['sma_50'] = analysis_sma(df['close'], 50)

    # Calculate MACD
    df['macd_line'], df['signal_line'], df['macd_hist'] = analysis_macd(df['close'])

    # Calculate RSI
    df['rsi'] = analysis_rsi(df['close'])

    last_close = df['close'].iloc[-1]

    # Implement your trading strategy using the indicators
    buy_signal = (
        df['sma_20'].iloc[-1] > df['sma_50'].iloc[-1] and
        df['macd_hist'].iloc[-1] > 0 and
        df['rsi'].iloc[-1] < 30
    )

    sell_signal = (
        df['sma_20'].iloc[-1] < df['sma_50'].iloc[-1] and
        df['macd_hist'].iloc[-1] < 0 and
        df['rsi'].iloc[-1] > 70
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
            last_close <= stop_loss or
            df['rsi'].iloc[-1] > 70
        )
        if close_long:
            return "close_long", last_close
    elif position_status == "short":
        take_profit = entry_price * (1 - take_profit_pct)
        stop_loss = entry_price * (1 + stop_loss_pct)
        close_short = (
            last_close <= take_profit or
            last_close >= stop_loss or
            df['rsi'].iloc[-1] < 30
        )
        if close_short:
            return "close_short", last_close

    return position_status, entry_price
