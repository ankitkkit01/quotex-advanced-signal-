import datetime
import random

def analyze_pair(pair, _):
    directions = ['UP', 'DOWN']
    trend_options = ['Strong UP', 'Strong DOWN', 'Sideways', 'Weak UP', 'Weak DOWN']

    return {
        "pair": pair,
        "entry_time": (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).strftime('%H:%M:%S'),
        "signal": random.choice(directions),
        "trend": random.choice(trend_options),
        "accuracy": random.randint(80, 95),
        "payout": random.randint(75, 90)
    }
