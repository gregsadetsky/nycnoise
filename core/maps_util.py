import requests
import re
from typing import Optional, Tuple

coordinates_regex = re.compile(
    r"APP_INITIALIZATION_STATE=\[\[\[(-?\d*[.]\d*),(-?\d*[.]\d*),(-?\d*[.]\d*)"
)


def fetch_coordinates(url: Optional[str]) -> Tuple[Optional[float], Optional[float]]:
    headers = {"User-Agent": "Wget/1.21"}

    if url:
        respone = requests.get(url, headers=headers)
        data = respone.text
        match = coordinates_regex.search(data)

        if match:
            lon = float(match.group(2))
            lat = float(match.group(3))
            return (lat, lon)

    return (None, None)


def main():

    tv_eye = "https://maps.app.goo.gl/wgWefEqTU4VLEHAC8"
    print(f"I love tv eye: {tv_eye}")
    print(fetch_coordinates(tv_eye))
    venues_list = [
        "https://maps.app.goo.gl/5B6wJmsggeQAQHJf8",
        "https://maps.app.goo.gl/atAmED6wkPLdMoC38",
        "https://maps.app.goo.gl/HypPmXet1HZvFB2KA",
        "https://maps.app.goo.gl/86ZdyDin9rL9NdvA8",
        "https://maps.app.goo.gl/cDJvH7NMvJ1JtoLBA",
        "https://maps.app.goo.gl/kNcqeTHbRzs4ej8r9",
        "https://maps.app.goo.gl/wgWefEqTU4VLEHAC8",
        "https://goo.gl/maps/F7U6DBssH7m4ZBbD7",
        "https://goo.gl/maps/kPbrM8ccdHBvRrQu7",
        "https://maps.app.goo.gl/pFjgWhi7U48J1Cb27",
        "https://maps.app.goo.gl/rV7mzttz1WA9J6dF7",
        "https://maps.app.goo.gl/ZVc2YzAQAawSKB6m8",
        "https://maps.app.goo.gl/VNHBMSLpkg8UJY7D7",
        "https://maps.app.goo.gl/ai55Cqy1xY46jLEi8",
        "https://goo.gl/maps/CJsuNbJiYcogrcie9",
        "https://maps.app.goo.gl/V6xSxhTtUKsWCEQR8",
        "https://goo.gl/maps/zrmoaX6oGikWZKmN9",
        "https://goo.gl/maps/NFGUZYCsZqBhvgEU8",
        "https://goo.gl/maps/8EbgtAhUi2HoCPA26",
        "https://goo.gl/maps/8EbgtAhUi2HoCPA26",
        "https://goo.gl/maps/g2vobB6yucgUdqWo6",
        "https://goo.gl/maps/x3q4Ccc4FV9bhHkq9",
        "https://maps.app.goo.gl/Bn2gVYMFx6Miga3c8",
        "https://goo.gl/maps/RbGMaKKAwJ4TDVbF6",
        "https://goo.gl/maps/HGZBPiMMX9n5EXyD8",
        "https://maps.app.goo.gl/tQc4CBw9RAkft2Uj8",
        "https://goo.gl/maps/atLFaJvMGEEzinFY6",
        "https://maps.app.goo.gl/WTQLQA7h4L9AFjc7A",
        "https://maps.app.goo.gl/TSuXLrwihAicmahq9",
        "https://maps.app.goo.gl/Dtw5cR1c9jpbaTHJ8",
        "https://goo.gl/maps/GSBayW2P4q7XjHok6",
        "https://goo.gl/maps/SkQMxcLovix4nN6X9",
        "https://maps.app.goo.gl/4YUuMmmCZPNURtFE9",
        "https://maps.app.goo.gl/2qmpdD5U4GAuiimBA",
        "https://goo.gl/maps/ZTscF5ufD53FKQ278",
        "https://goo.gl/maps/euAmEEYkcAb2s1338",
        "https://maps.app.goo.gl/j59kfWekKqxoeo8T8",
        "https://maps.app.goo.gl/B8CLrwhgCjpzkDww7",
        "https://goo.gl/maps/66i4iQTAG8swrQ6NA",
        "https://goo.gl/maps/ShP3hzCMqJZ2SiE96",
    ]
    for v in venues_list:
        print(f"Url: {v}")
        lat, lon = fetch_coordinates(v)
        print(f"Coordinates: {lat, lon}")
        print(f"Conrol URL: http://maps.google.com/?ll={lat},{lon}")
        print("-------------")


if __name__ == "__main__":
    main()
