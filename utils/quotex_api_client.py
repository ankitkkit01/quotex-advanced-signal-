from quotexapi.client import Quotex
import logging

logging.basicConfig(level=logging.INFO)

EMAIL = "arhimanshya@gmail.com"
PASSWORD = "12345678an"

def get_client():
    client = Quotex(EMAIL, PASSWORD)
    client.connect()
    client.login()

    if client.check_connect():
        logging.info("✅ Connected to Quotex")
        return client
    else:
        raise Exception("❌ Quotex connection failed")

def subscribe_to_candles(client, asset, timeframe, callback):
    client.subscribe_candles(asset, timeframe)
    client.set_candle_callback(callback)
