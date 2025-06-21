import numpy as np import pandas as pd import ta

def calculate_pivots(df): """Calculate Pivot Points, Support & Resistance Levels""" last = df.iloc[-2]  # Previous candle for pivot

pivot = (last['high'] + last['low'] + last['close']) / 3
r1 = (2 * pivot) - last['low']
s1 = (2 * pivot) - last['high']
r2 = pivot + (last['high'] - last['low'])
s2 = pivot - (last['high'] - last['low'])

return {'pivot': pivot, 'r1': r1, 's1': s1, 'r2': r2, 's2': s2}

def analyze_pair(pair, df): """Perform advanced analysis on the given trading pair."""

# Indicators
df['rsi'] = ta.momentum.rsi(df['close'], window=14)
df['macd'] = ta.trend.macd(df['close'])
df['macd_signal'] = ta.trend.macd_signal(df['close'])

pivots = calculate_pivots(df)
last = df.iloc[-1]

# Signal Zones
support_zone = pivots['s1'] <= last['close'] <= pivots['s2']
resistance_zone = pivots['r1'] >= last['close'] >= pivots['r2']

# RSI Zones
rsi_overbought = last['rsi'] > 70
rsi_oversold = last['rsi'] < 30

# MACD Trend
macd_bullish = last['macd'] > last['macd_signal']
macd_bearish = last['macd'] < last['macd_signal']

analysis = []

# Support & Resistance analysis
if support_zone:
    analysis.append("Near Support Zone")
if resistance_zone:
    analysis.append("Near Resistance Zone")

# RSI Analysis
if rsi_overbought:
    analysis.append("RSI Overbought")
elif rsi_oversold:
    analysis.append("RSI Oversold")

# MACD Analysis
if macd_bullish:
    analysis.append("MACD Bullish")
elif macd_bearish:
    analysis.append("MACD Bearish")

# Final Signal Suggestion (Basic Logic)
signal = None
if rsi_oversold and macd_bullish and support_zone:
    signal = 'UP'
elif rsi_overbought and macd_bearish and resistance_zone:
    signal = 'DOWN'

return {
    'pair': pair,
    'signal': signal,
    'analysis': analysis,
    'pivot_levels': pivots
}

if name == "main": # Demo Example data = { 'time': pd.date_range(end=pd.Timestamp.now(), periods=100, freq='T'), 'open': np.random.rand(100) * 100, 'high': np.random.rand(100) * 100 + 0.5, 'low': np.random.rand(100) * 100 - 0.5, 'close': np.random.rand(100) * 100, 'volume': np.random.randint(1000, 5000, size=100) } df = pd.DataFrame(data)

result = analyze_pair("EURUSD", df)
print(result)

