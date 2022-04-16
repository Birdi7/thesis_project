import json
import random
from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand

from thesis.models import Address

DESTINATION = Path(settings.BASE_DIR) / "scripts" / "map_location_info.json"


POINT_WRITE_FORMAT = "POINT({lon} {lat})"


def generate_cpl():
    return random.uniform(150, 400)


def write_data(data):
    def _format_point_to_write(point):
        return POINT_WRITE_FORMAT.format(lon=point["lon"], lat=point["lat"])

    result = [{"cpl": v["cpl"], "location": _format_point_to_write(v["location"])} for v in data]
    with open(DESTINATION, "w") as fp:
        json.dump(result, fp, indent=4)


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        qs = Address.objects.all()
        locations = [(i.location.x, i.location.y) for i in qs]

        data = [{"cpl": generate_cpl(), "location": {"lon": item[0], "lat": item[1]}} for item in locations]

        write_data(data)
