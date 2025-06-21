import numpy as np
import pandas as pd
import ta

def calculate_pivots(df):
    last = df.iloc[-2]
    pivot = (last['high'] + last['low'] + last['close']) / 3
    r1 = (2 * pivot) - last['low']
    s1 = (2 * pivot) - last['high']
    r2 = pivot + (last['high'] - last['low'])
    s2 = pivot - (last['high'] - last['low'])
    return {'pivot': pivot, 'r1': r1, 's1': s1, 'r2': r2, 's2': s2}

def detect_double_top(df):
    highs = df['high'].rolling(window=5).max()
    recent_highs = highs[-10:]
    if recent_highs.max() == recent_highs.iloc[-1] and recent_highs.max() == recent_highs.iloc[-5]:
        return True
    return False

def detect_double_bottom(df):
    lows = df['low'].rolling(window=5).min()
    recent_lows = lows[-10:]
    if recent_lows.min() == recent_lows.iloc[-1] and recent_lows.min() == recent_lows.iloc[-5]:
        return True
    return False

def analyze_pair(pair, df):
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    df['macd'] = ta.trend.macd(df['close'])
    df['macd_signal'] = ta.trend.macd_signal(df['close'])
    pivots = calculate_pivots(df)
    last = df.iloc[-1]
    support_zone = pivots['s1'] <= last['close'] <= pivots['s2']
    resistance_zone = pivots['r1'] >= last['close'] >= pivots['r2']
    rsi_overbought = last['rsi'] > 70
    rsi_oversold = last['rsi'] < 30
    macd_bullish = last['macd'] > last['macd_signal']
    macd_bearish = last['macd'] < last['macd_signal']
    analysis = []
    if support_zone:
        analysis.append("Near Support Zone")
    if resistance_zone:
        analysis.append("Near Resistance Zone")
    if rsi_overbought:
        analysis.append("RSI Overbought")
    elif rsi_oversold:
        analysis.append("RSI Oversold")
    if macd_bullish:
        analysis.append("MACD Bullish")
    elif macd_bearish:
        analysis.append("MACD Bearish")
    if detect_double_top(df):
        analysis.append("Double Top Pattern Detected (Bearish)")
    if detect_double_bottom(df):
        analysis.append("Double Bottom Pattern Detected (Bullish)")
    signal = None
    if (rsi_oversold and macd_bullish and support_zone) or detect_double_bottom(df):
        signal = 'UP'
    elif (rsi_overbought and macd_bearish and resistance_zone) or detect_double_top(df):
        signal = 'DOWN'
    return {'pair': pair, 'signal': signal, 'analysis': analysis, 'pivot_levels': pivots}
