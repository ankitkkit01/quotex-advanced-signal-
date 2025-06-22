# strategies/final_strategy.py

import pandas as pd
import numpy as np
import ta

def generate_trade_signal(df):
    """
    df = Pandas DataFrame with columns: open, high, low, close, volume
    """

    # Calculate Indicators
    df['sma_100'] = ta.trend.sma_indicator(df['close'], window=100)
    df['wma_25'] = ta.trend.wma_indicator(df['close'], window=25)
    df['sma_10'] = ta.trend.sma_indicator(df['close'], window=10)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    df['demarker'] = ta.momentum.demarker(df['high'], df['low'], window=14)
    df['macd'] = ta.trend.macd_diff(df['close'])

    latest = df.iloc[-1]

    # Trend Condition → Above 100 SMA → UP preference, Below → DOWN
    trend = "UP" if latest['close'] > latest['sma_100'] else "DOWN"

    # RSI Confirmation
    if latest['rsi'] < 30:
        signal = "UP"
    elif latest['rsi'] > 70:
        signal = "DOWN"
    else:
        signal = trend  # Default to trend direction

    # Extra Filter with MACD
    if latest['macd'] > 0 and signal == "UP":
        confidence = "HIGH"
    elif latest['macd'] < 0 and signal == "DOWN":
        confidence = "HIGH"
    else:
        confidence = "MEDIUM"

    return {
        "signal": signal,
        "confidence": confidence,
        "trend": trend,
        "rsi": round(latest['rsi'], 2),
        "macd": round(latest['macd'], 2),
        "demarker": round(latest['demarker'], 2)
  }
