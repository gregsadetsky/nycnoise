import re
from typing import Optional, Tuple

import requests

coordinates_regex = re.compile(
    r"APP_INITIALIZATION_STATE=\[\[\[(-?\d*[.]\d*),(-?\d*[.]\d*),(-?\d*[.]\d*)"
)


def fetch_coordinates(url: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    if not url:
        return (None, None)

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except:
        return (None, None)
    data = response.text
    match = coordinates_regex.search(data)

    if not match:
        return (None, None)

    lon = float(match.group(2))
    lat = float(match.group(3))
    return (lat, lon)
