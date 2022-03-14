import random
from pathlib import Path
import json


MOSCOW_BOUNDS = (
    {"lon": 36.622504, "lat": 53.753215},
    {"lon": 38.622504, "lat": 57.753215},
)

_N = 150

POINT_WRITE_FORMAT = "POINT({lon} {lat})"

DESTIONATION = Path(__file__).parent.resolve() / "map_location_info.json"


def generate_new_point():
    return {
        "lon": random.uniform(MOSCOW_BOUNDS[0]["lon"], MOSCOW_BOUNDS[1]["lon"]),
        "lat": random.uniform(MOSCOW_BOUNDS[0]["lat"], MOSCOW_BOUNDS[1]["lat"]),
    }


def generate_cpl():
    return random.uniform(150, 400)


def generate_data():
    result = []
    for _ in range(_N):
        result.append({"location": generate_new_point(), "cpl": generate_cpl()})
    return result


def write_data(data):
    def _format_point_to_write(point):
        return POINT_WRITE_FORMAT.format(lon=point["lon"], lat=point["lat"])

    result = [
        {"cpl": v["cpl"], "location": _format_point_to_write(v["location"])}
        for v in data
    ]
    with open(DESTIONATION, "w") as fp:
        json.dump(result, fp, indent=4)


def run():
    data = generate_data()

    write_data(data)


if __name__ == "__main__":
    run()
