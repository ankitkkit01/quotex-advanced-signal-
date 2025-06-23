from datetime import datetime, timedelta

def get_adjusted_entry_time():
    ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
    entry_time = ist_now + timedelta(minutes=1)
    adjusted_time = entry_time.replace(second=5, microsecond=0)
    return adjusted_time.strftime("%H:%M:%S")
