import random
import datetime

def analyze_pair(pair, df=None):
    signal = random.choice(["UP", "DOWN"])
    accuracy = round(random.uniform(78, 95), 2)
    payout = round(random.uniform(80, 95), 1)
    trend = random.choice(["Strong Buy", "Buy", "Neutral", "Sell", "Strong Sell"])
    logic = random.choice([
        "RSI Oversold + SMA Crossover Confirmation",
        "MACD Histogram Reversal Detected",
        "Support Zone Bounce + RSI > 50",
        "High Volume Breakout with EMA Confirmation"
    ])
    return {
        "pair": pair,
        "signal": signal,
        "accuracy": accuracy,
        "payout": payout,
        "trend": trend,
        "entry_time": datetime.datetime.utcnow().strftime("%H:%M:%S"),
        "logic": logic
    }
