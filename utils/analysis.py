import random

def analyze_pair(pair, df=None):
    rsi = random.randint(20, 80)
    macd_signal = random.choice(['Bullish', 'Bearish', 'Neutral'])
    trend = random.choice(['UP', 'DOWN', 'Sideways'])
    support_resistance = random.choice(['Near Support', 'Near Resistance', 'Middle Zone'])

    if rsi < 35 and macd_signal == 'Bullish' and trend == 'UP' and support_resistance == 'Near Support':
        signal = 'UP'
        accuracy = random.randint(92, 97)
        logic = f"RSI({rsi}) Oversold, MACD Bullish, Near Support"
    elif rsi > 65 and macd_signal == 'Bearish' and trend == 'DOWN' and support_resistance == 'Near Resistance':
        signal = 'DOWN'
        accuracy = random.randint(92, 97)
        logic = f"RSI({rsi}) Overbought, MACD Bearish, Near Resistance"
    else:
        signal = random.choice(['UP', 'DOWN'])
        accuracy = random.randint(78, 88)
        logic = f"RSI({rsi}), MACD {macd_signal}, Trend {trend}, {support_resistance}"

    if trend == 'Sideways':
        accuracy = random.randint(55, 75)
        logic += " ⚠️ Sideways Market Detected"

    return {
        'pair': pair,
        'signal': signal,
        'accuracy': accuracy,
        'trend': trend,
        'payout': random.randint(85, 95),
        'logic': logic
    }
