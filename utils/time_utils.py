from datetime import datetime, timedelta

def get_adjusted_entry_time():
    now = datetime.utcnow() + timedelta(minutes=1)
    adjusted_time = now.replace(second=5, microsecond=0)  # ✅ ENTRY BEFORE CANDLE START
    return adjusted_time.strftime("%H:%M:%S")
