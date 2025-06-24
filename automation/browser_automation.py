def get_live_candle_data(asset, timeframe="1m"):
    """
    Dummy candle data generator.
    Replace this with real API/websocket later.
    """
    import random, time

    candles = []
    current_price = random.uniform(1.1000, 1.3000)

    for i in range(50):
        open_price = current_price + random.uniform(-0.01, 0.01)
        close_price = open_price + random.uniform(-0.01, 0.01)
        high = max(open_price, close_price) + random.uniform(0, 0.005)
        low = min(open_price, close_price) - random.uniform(0, 0.005)
        timestamp = int(time.time()) - (50 - i) * 60

        candles.append({
            'open': round(open_price, 5),
            'close': round(close_price, 5),
            'high': round(high, 5),
            'low': round(low, 5),
            'timestamp': timestamp
        })

    return candles
