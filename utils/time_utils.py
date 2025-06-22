from datetime import datetime, timedelta

def get_entry_time(offset_minutes=1):
    """
    Returns the entry time in IST (UTC+5:30) in HH:MM format.
    
    :param offset_minutes: How many minutes ahead from the current time you want
    """
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    entry_time = ist_time + timedelta(minutes=offset_minutes)
    return entry_time.strftime('%H:%M')

def get_current_ist_time():
    """
    Returns the current IST time in HH:MM format.
    """
    ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return ist_time.strftime('%H:%M')
