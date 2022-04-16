from dataclasses import dataclass
from typing import Optional

import requests
from django.conf import settings


@dataclass
class ParsedAddress:
    x: float
    y: float


class AddressParser:
    @classmethod
    def from_string(cls, address: str) -> Optional[ParsedAddress]:
        try:
            params = {"apikey": settings.YANDEX_API_KEY, "geocode": address, "format": "json"}
            response = requests.get("https://geocode-maps.yandex.ru/1.x/", params=params).json()["response"]
            point = response["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]
            location = list(map(float, point["pos"].split(" ")))

            return ParsedAddress(x=location[0], y=location[1])
        except:  # noqa
            return None
