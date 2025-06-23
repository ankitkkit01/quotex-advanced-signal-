import datetime
import pytz

def get_future_entry_time(mins_ahead=1):
    now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    next_entry = (now + datetime.timedelta(minutes=mins_ahead)).replace(second=0, microsecond=0)
    return next_entry.strftime("%H:%M:%S")
