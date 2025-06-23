from quotexapi.client import Quotex

def get_client(arhimanshya@gmail.com):
    client = Quotex(12345678an)
    client.connect()
    return client

def get_payout(client, asset):
    return client.get_all_profit()[asset]["turbo"]
