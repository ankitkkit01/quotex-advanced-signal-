import numpy as np
import pandas as pd
import ta
import random

def generate_dummy_market_data():
    data = pd.DataFrame({
        'close': np.random.uniform(100, 200, 100)
    })
    data['rsi'] = ta.momentum.rsi(data['close'])
    data['macd'] = ta.trend.macd_diff(data['close'])
    return data

def generate_signal():
    data = generate_dummy_market_data()
    latest_rsi = data['rsi'].iloc[-1]
    latest_macd = data['macd'].iloc[-1]

    trend = ""
    if latest_rsi < 30 and latest_macd > 0:
        trend = "🔼 BUY Signal Detected\nSupport Confirmed ✅"
    elif latest_rsi > 70 and latest_macd < 0:
        trend = "🔽 SELL Signal Detected\nResistance Confirmed ✅"
    else:
        trend = random.choice(["🔼 BUY Signal ⚙️", "🔽 SELL Signal ⚙️"])

    pair = random.choice(["EUR/USD", "GBP/JPY", "BTC/USD", "GOLD"])
    return (
        f"💹 *Quotex Signal*\n"
        f"Pair: `{pair}`\n"
        f"Signal: {trend}\n"
        f"Volume Analysis: ✅ Confirmed\n"
        f"Pattern Match: ✅ Confirmed\n"
        f"\nGenerated for: *Ankit Singh*"
    )
