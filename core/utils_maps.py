import requests
import re
from typing import Optional, Tuple

coordinates_regex = re.compile(
    r"APP_INITIALIZATION_STATE=\[\[\[(-?\d*[.]\d*),(-?\d*[.]\d*),(-?\d*[.]\d*)"
)


def fetch_coordinates(url: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    headers = {"User-Agent": "Wget/1.21"}

    if url:
        response = requests.get(url, headers=headers)
        data = response.text
        match = coordinates_regex.search(data)

        if match:
            lon = float(match.group(2))
            lat = float(match.group(3))
            return (lat, lon)

    return (None, None)
