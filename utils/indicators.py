import pandas as pd

def calculate_rsi(candles, period=14):
    df = pd.DataFrame(candles)
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi.iloc[-1], 2)

def calculate_macd(candles, short_period=12, long_period=26, signal_period=9):
    df = pd.DataFrame(candles)
    ema_short = df['close'].ewm(span=short_period, adjust=False).mean()
    ema_long = df['close'].ewm(span=long_period, adjust=False).mean()

    macd = ema_short - ema_long
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal

    return round(macd.iloc[-1], 4), round(signal.iloc[-1], 4), round(histogram.iloc[-1], 4)
