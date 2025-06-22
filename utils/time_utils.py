# utils/time_utils.py

import datetime

def is_exact_time(interval_sec=10):
    now = datetime.datetime.utcnow()
    return (now.second % interval_sec) == 0