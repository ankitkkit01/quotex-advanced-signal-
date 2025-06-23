from quotexapi.client import Quotex

EMAIL = "arhimanshya@gmail.com"       # Quotex login email
PASSWORD = "12345678an" # Quotex login password

def get_client():
    client = Quotex(EMAIL, PASSWORD)
    client.connect()
    if client.check_connect():
        print("✅ Connected to Quotex")
        return client
    else:
        raise Exception("❌ Failed to connect")

def get_balance(client):
    return client.get_balance()

def get_payout(client, asset):
    return client.get_all_profit().get(asset, 0)
