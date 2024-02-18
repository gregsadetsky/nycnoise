from datetime import datetime

from dateutil import relativedelta, tz

# DO NOT USE PYTZ <> DO NOT USE PYTZ <> DO NOT USE PYTZ
# https://blog.ganssle.io/articles/2018/03/pytz-fastest-footgun.html
NYCTZ = tz.gettz("America/New_York")


def get_current_new_york_datetime():
    return datetime.now().astimezone(NYCTZ)


def first_day_of_month(dt):
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def get_previous_current_next_month_start(dt):
    current_month_start = first_day_of_month(dt)

    return (
        current_month_start - relativedelta.relativedelta(months=1),
        current_month_start,
        current_month_start + relativedelta.relativedelta(months=1),
    )
