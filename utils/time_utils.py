from datetime import datetime, timedelta

def get_current_ist_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

def get_next_minute_entry_time():
    now = get_current_ist_time()
    next_minute = now + timedelta(minutes=1)
    return next_minute.strftime("%H:%M")

def is_exact_time():
    now = get_current_ist_time()
    return now.second == 0
