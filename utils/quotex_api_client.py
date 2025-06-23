from quotexapi.client import Quotex
import logging
import time

logging.basicConfig(level=logging.INFO)

EMAIL = "arhimanshya@gmail.com"
PASSWORD = "12345678an"

def get_client():
    client = Quotex(EMAIL, PASSWORD)
    client.connect()
    client.login()

    if client.check_connect():
        logging.info("✅ Connected to Quotex API")
        return client
    else:
        raise Exception("❌ Failed to connect Quotex API")

def get_candles(client, asset, timeframe="1m", count=50):
    """
    Fetch recent candle data for the given asset.
    Returns list of dict: [{'open': ..., 'close': ..., 'high': ..., 'low': ..., 'volume': ..., 'timestamp': ...}]
    """
    candles = []
    client.subscribe_candles(asset, timeframe)

    time.sleep(2)  # Wait to receive data
    raw_candles = client.get_candles(asset, timeframe)
    client.unsubscribe_candles(asset, timeframe)

    for candle in raw_candles[-count:]:
        candles.append({
            'open': candle['open'],
            'close': candle['close'],
            'high': candle['max'],
            'low': candle['min'],
            'volume': candle.get('volume', 0),
            'timestamp': candle['from']
        })

    return candles
