import random

def analyze_pair(pair, df=None):
    # Simulated price and support/resistance levels
    current_price = round(random.uniform(1.1000, 1.5000), 4)
    support = current_price - round(random.uniform(0.0050, 0.0100), 4)
    resistance = current_price + round(random.uniform(0.0050, 0.0100), 4)

    # Trend simulation using SMA100 (temporary logic)
    trend = random.choice(["Buy", "Sell"])

    # RSI logic
    rsi = random.randint(35, 65)

    # Support/Resistance based signal direction
    if abs(current_price - support) < 0.003:
        sr_logic = "Support Zone"
        signal = "UP"
    elif abs(current_price - resistance) < 0.003:
        sr_logic = "Resistance Zone"
        signal = "DOWN"
    else:
        sr_logic = "Mid Zone"
        signal = "UP" if trend == "Buy" else "DOWN"

    return {
        "pair": pair,
        "signal": signal,
        "accuracy": round(random.uniform(89, 96), 2),
        "payout": round(random.uniform(85, 95), 1),
        "trend": trend,
        "logic": f"{sr_logic} • SMA100 {trend} • RSI {rsi}"
    }
