import talib as ta
import pandas as pd
from typing import List, Dict


def analyze_candlestick_patterns(
    open: List[float], high: List[float], low: List[float], close: List[float]
) -> pd.DataFrame:
    """
    Analyze given candlestick patterns.

    Parameters:
    open (List[float]): List of open prices
    high (List[float]): List of high prices
    low (List[float]): List of low prices
    close (List[float]): List of close prices

    Returns:
    pd.DataFrame: DataFrame with analysis results
    """
    pattern_functions: Dict[str, callable] = {
        "engulfing": ta.CDLENGULFING,
        "doji": ta.CDLDOJI,
        "harami": ta.CDLHARAMI,
    }

    patterns = list(pattern_functions.keys())

    results = pd.DataFrame(index=open.index)

    for pattern in patterns:
        try:
            pattern_function = pattern_functions.get(pattern)
            if not pattern_function:
                raise ValueError(f"Invalid pattern name: {pattern}")
            results[pattern] = pattern_function(open, high, low, close)
        except ValueError as e:
            print(e)

    return results
