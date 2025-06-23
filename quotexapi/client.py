from quotexapi.client import Quotex

def get_client():
    email = "arhimanshya@gmail.com"
    password = "12345678an"

    qx = Quotex(email, password)
    qx.connect()
    if qx.check_connect():
        print("✅ Connected to Quotex successfully!")
        return qx
    else:
        raise Exception("❌ Failed to connect to Quotex.")

def get_payout(asset):
    return 95  # Static payout, real dynamic payout ka code later add karenge
