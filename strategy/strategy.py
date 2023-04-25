import pandas as pd

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