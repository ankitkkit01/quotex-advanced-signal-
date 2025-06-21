import random

def generate_signal():
    pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'GOLD', 'BTC/USD']
    trends = ['🔼 BUY', '🔽 SELL']
    confidences = ['✅ Strong Signal', '⚠️ Medium Confidence']

    pair = random.choice(pairs)
    trend = random.choice(trends)
    confidence = random.choice(confidences)

    return pair, trend, confidence

def get_market_analysis(pair):
    return (
        f"• Support & Resistance: ✅ Confirmed\n"
        f"• RSI Level: 🔵 Neutral\n"
        f"• MACD: 📊 Positive\n"
        f"• Volume: 📶 High"
    )
