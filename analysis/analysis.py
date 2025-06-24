import random
from automation.browser_automation import get_live_candle_data  # ✅ FIXED PATH

def analyze_pair(pair, data=None):
    """
    Professional analysis using mock indicators for demonstration.
    """
    # 🎯 Mocked realistic indicator readings (Replace with real-time analysis)
    rsi = random.randint(20, 80)
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
