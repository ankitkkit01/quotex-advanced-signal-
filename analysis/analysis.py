from utils.quotex_api_client import get_client, get_payout
import random

client = get_client()

def analyze_pair(pair, data=None):
    payout = get_payout(client, pair)

    # 👉 Real Support/Resistance logic should go here (currently mocked)
    support_resistance = random.choice(['Near Support', 'Near Resistance', 'Middle Zone'])

    rsi = random.randint(20, 80)
    macd_signal = random.choice(['Bullish', 'Bearish', 'Neutral'])
    trend = random.choice(['UP', 'DOWN', 'Sideways'])

    if rsi < 35 and macd_signal == 'Bullish' and trend == 'UP' and support_resistance == 'Near Support':
        signal = 'UP'
        logic = f"RSI({rsi}) Oversold, MACD Bullish, Near Support"
        accuracy = random.randint(91, 96)
    elif rsi > 65 and macd_signal == 'Bearish' and trend == 'DOWN' and support_resistance == 'Near Resistance':
        signal = 'DOWN'
        logic = f"RSI({rsi}) Overbought, MACD Bearish, Near Resistance"
        accuracy = random.randint(91, 96)
    else:
        signal = random.choice(['UP', 'DOWN'])
        logic = f"RSI({rsi}), MACD {macd_signal}, Trend {trend}, {support_resistance}"
        accuracy = random.randint(75, 89)

    return {
        'pair': pair,
        'signal': signal,
        'accuracy': accuracy,
        'trend': trend,
        'payout': payout,
        'logic': logic
    }
