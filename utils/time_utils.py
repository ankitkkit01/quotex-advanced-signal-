# utils/time_utils.py

from datetime import datetime, timedelta

def get_current_ist_time():
    """
    Returns current time in IST (UTC+5:30)
    """
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

def is_exact_time():
    """
    Returns True if current IST time's seconds == 0
    Useful for signaling exactly on start of minute
    """
    now = get_current_ist_time()
    return now.second == 0
