import random
import pandas as pd
from utils.browser_automation import get_live_candle_data  # ✅ Corrected import path

def analyze_pair(pair, data=None):
    """
    Advanced analysis using live candle data and mock technical indicators.
    """

    # 🔗 LIVE candle data fetch
    candles = get_live_candle_data(pair, limit=50)

    # Calculate mock RSI (demo purpose)
    closes = [c['close'] for c in candles]
    rsi = random.randint(25, 75)

    # Random mock values for demo (replace with actual calculation)
    macd_signal = random.choice(['Bullish', 'Bearish', 'Neutral'])
    trend = random.choice(['UP', 'DOWN', 'Sideways'])
    support_resistance = random.choice(['Near Support', 'Near Resistance', 'Middle Zone'])

    # 🎯 Signal decision based on combined indicators
    if rsi < 35 and macd_signal == 'Bullish' and trend == 'UP' and support_resistance == 'Near Support':
        signal = 'UP'
        logic = f"RSI({rsi}) Oversold, MACD Bullish, Near Support"
        accuracy = random.randint(91, 95)
    elif rsi > 65 and macd_signal == 'Bearish' and trend == 'DOWN' and support_resistance == 'Near Resistance':
        signal = 'DOWN'
        logic = f"RSI({rsi}) Overbought, MACD Bearish, Near Resistance"
        accuracy = random.randint(91, 95)
    else:
        signal = random.choice(['UP', 'DOWN'])
        logic = f"RSI({rsi}), MACD {macd_signal}, Trend {trend}, {support_resistance}"
        accuracy = random.randint(75, 89)

    # Sideways filter → reduce accuracy if sideways
    if trend == 'Sideways':
        accuracy = random.randint(60, 74)
        logic += " ⚠️ Sideways Market Detected"

    return {
        'pair': pair,
        'signal': signal,
        'accuracy': accuracy,
        'trend': trend,
        'payout': random.randint(80, 95),
        'logic': logic
    }
