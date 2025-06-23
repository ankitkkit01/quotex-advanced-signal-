from quotexapi.core import Quotex

EMAIL = "arhimanshya@gmail.com"
PASSWORD = "12345678an"

def get_client():
    qx = Quotex(EMAIL, PASSWORD)
    qx.connect()
    qx.login()
    if qx.check_connect():
        print("✅ Connected to Quotex successfully!")
        return qx
    else:
        raise Exception("❌ Failed to connect to Quotex.")

def get_payout(client, asset):
    # Currently static payout → Replace with real logic later
    return 95
