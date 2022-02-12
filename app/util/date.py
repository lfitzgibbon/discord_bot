import pytz
from datetime import datetime, timedelta

from app import BOT_TIMEZONE


def seconds_until_midnight() -> float:
    ''' Determine how many seconds are between now and midnight '''
    now = datetime.now(tz=pytz.timezone(BOT_TIMEZONE))
    tomorrow_midnight = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0)

    # Calculate how much time is left until midnight
    # time.sleep() doesn't take negative values, so we use max() here to ensure
    # that the value will always be non-negative (in case there are shenanigans with dates)
    return max(0, (tomorrow_midnight - now).total_seconds())
