from django.template.defaulttags import register

# https://github.com/gregsadetsky/nycnoise/issues/462

NYC_NOISE_DAYS = ["mon", "tues", "weds", "thurs", "fri", "sat", "sun"]
NYC_MONTHS = [
    "jan",
    "feb",
    "march",
    "april",
    "may",
    "june",
    "july",
    "aug",
    "sept",
    "oct",
    "nov",
    "dec",
]


@register.filter
def nyc_noise_day_with_parens(date):
    # given date is a datetime object
    return f"({NYC_NOISE_DAYS[date.weekday()]})"


@register.filter
def nyc_noise_navigation_bar_month(date):
    return f"{NYC_MONTHS[date.month - 1]}"
