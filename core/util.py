import re


def strip_html(text: str):
    return re.sub(re.compile('<.*?>'), '', text)
