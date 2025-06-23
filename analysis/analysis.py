import random

def analyze_pair(pair, timeframe):
    # Mock analysis with higher chance of good accuracy during certain conditions
    accuracy = random.randint(88, 97)
    trend = random.choice(['Uptrend', 'Downtrend', 'Sideways'])

    # Avoid sideways trend automatically for better signals
    while trend == 'Sideways' or accuracy < 90:
        accuracy = random.randint(90, 99)
        trend = random.choice(['Uptrend', 'Downtrend'])

    signal = 'UP' if trend == 'Uptrend' else 'DOWN'

    # Generate a fake payout (between 80% and 95%)
    payout = random.randint(80, 95)

    # Generate a professional analysis logic description
    logic = f"Price near {'support' if signal == 'UP' else 'resistance'} zone, {trend} confirmed, RSI & MACD aligned."

    return {
        'pair': pair,
        'signal': signal,
        'trend': trend,
        'accuracy': accuracy,
        'payout': payout,
        'logic': logic
    }
