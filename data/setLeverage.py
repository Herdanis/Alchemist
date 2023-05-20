from typing import Any, Dict


def set_leverage(exchange: Any, symbol: str, leverage: int) -> Dict[str, Any]:
    """
    Set leverage for a given symbol.

    Parameters:
    exchange (ccxt.binance): Binance Futures API connection
    symbol (str): Symbol for which to set the leverage
    leverage (int): Leverage to set

    Returns:
    dict: Response from the Binance Futures API
    """
    try:
        params = {"symbol": exchange.market_id(symbol), "leverage": leverage}
        return exchange.fapiPrivate_post_leverage(params)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
