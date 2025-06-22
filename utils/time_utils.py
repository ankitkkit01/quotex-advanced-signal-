# utils/time_utils.py

from datetime import datetime, timedelta
import pytz

# Function to get India Standard Time
def get_india_time():
    utc_now = datetime.utcnow()
    india_time = utc_now + timedelta(hours=5, minutes=30)
    return india_time

# Function to check if current time is exactly at specific second
def is_exact_time():
    india_time = get_india_time()
    return india_time.second in [0, 10, 20, 30, 40, 50]
