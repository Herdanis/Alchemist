import ccxt
import os
from dotenv import load_dotenv
from typing import Any

# Load API key and secret from .env file (optional)
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
sandbox = os.getenv("TEST_NET")


def binanceExchange() -> Any:
    """
    Initialize Binance Futures API connection.

    Returns:
    ccxt.binance: Binance Futures API connection
    """
    try:
        exchange = ccxt.binance(
            {
                "apiKey": api_key,
                "secret": api_secret,
                "enableRateLimit": True,
                "options": {"defaultType": "future"},
            }
        )
        exchange.set_sandbox_mode(False)
        return exchange
    except Exception as e:
        print(f"An error occurred: {e}")
        return None