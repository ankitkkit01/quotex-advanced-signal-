# utils/time_utils.py

from datetime import datetime, timedelta

def get_adjusted_entry_time():
    now = datetime.utcnow() + timedelta(minutes=1)
    adjusted_time = now.replace(second=30, microsecond=0)
    return adjusted_time.strftime("%H:%M:%S")
