import talib as ta
import sys
from pathlib import Path
from typing import List, Tuple, Optional

sys.path.append(str(Path(__file__).parent.parent))

from data import getExchange as exchange


def analysis_sma(close_price: List[float], periode: int) -> List[float]:
    """
    Calculate Simple Moving Average (SMA) for given close prices and period.

    Parameters:
    close_price (List[float]): List of close prices
    periode (int): Period for which SMA is calculated

    Returns:
    List[float]: SMA for the given close prices and period
    """
    sma = ta.SMA(close_price, periode)
    return sma


def analysis_ema(close_price: List[float], periode: int) -> List[float]:
    """
    Calculate Exponential Moving Average (EMA) for given close prices and period.

    Parameters:
    close_price (List[float]): List of close prices
    periode (int): Period for which EMA is calculated

    Returns:
    List[float]: EMA for the given close prices and period
    """
    ema = ta.EMA(close_price, periode)
    return ema


def analysis_macd(
    close_price: List[float],
) -> Tuple[List[float], List[float], List[float]]:
    """
    Calculate Moving Average Convergence Divergence (MACD) for given close prices.

    Parameters:
    close_price (List[float]): List of close prices

    Returns:
    Tuple[List[float], List[float], List[float]]: MACD line, signal line, and histogram
    """
    macd_line, signal_line, histogram = ta.MACD(close_price, 12, 26, 9)
    return macd_line, signal_line, histogram


def analysis_oi(symbol: str) -> Optional[float]:
    """
    Get open interest for a given symbol from Binance Exchange.

    Parameters:
    symbol (str): Symbol for which to get open interest

    Returns:
    float: Open interest for the given symbol
    """
    try:
        ex = exchange.binanceExchange()
        ex.load_markets()
        response = ex.fapiPublic_get_openinterest({"symbol": ex.market_id(symbol)})
        open_interest = float(response["openInterest"])
        return open_interest
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def analysis_rsi(close_price: List[float]) -> List[float]:
    """
    Calculate Relative Strength Index (RSI) for given close prices.

    Parameters:
    close_price (List[float]): List of close prices

    Returns:
    List[float]: RSI for the given close prices
    """
    rsi = ta.RSI(close_price)
    return rsi
