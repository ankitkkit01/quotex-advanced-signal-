import random

def get_live_candle_data(pair, limit=50):
    """
    Dummy live candle data for testing.
    Replace with Selenium scraping or real API integration later.
    """
    candles = []
    price = random.uniform(1.0, 2.0)
    for _ in range(limit):
        candle = {
            'open': round(price + random.uniform(-0.05, 0.05), 5),
            'close': round(price + random.uniform(-0.05, 0.05), 5),
            'high': round(price + random.uniform(0, 0.1), 5),
            'low': round(price - random.uniform(0, 0.1), 5),
            'volume': random.randint(100, 1000),
            'timestamp': random.randint(1600000000, 1700000000),
        }
        candles.append(candle)
    return candles


def start_browser_login(email, password):
    """
    Dummy placeholder for Selenium browser login.
    Replace with actual Selenium login code if required.
    """
    print(f"Logging into Quotex with {email} / {password} (Dummy Function)")
