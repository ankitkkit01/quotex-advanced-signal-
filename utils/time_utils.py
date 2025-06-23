import datetime
import pytz

def get_adjusted_entry_time(seconds_before=15):
    now = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    next_minute = now + datetime.timedelta(minutes=1)
    entry_time = next_minute.replace(second=0, microsecond=0) - datetime.timedelta(seconds=seconds_before)
    return entry_time.strftime("%H:%M:%S")
