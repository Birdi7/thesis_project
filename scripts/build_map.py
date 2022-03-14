from cmath import log10
from pickle import decode_long
from wsgiref.handlers import format_date_time
import folium
import os
from dash import dcc
from dash import html
from folium.features import DivIcon
import subprocess
from pathlib import Path

import json
import dash


loc = (55.75, 37.6)
m = folium.Map(location=loc, zoom_start=10)


def add_data_point(location, cpl_value):
    # cpl_value = f"{cpl_value}₽"
    folium.Marker(
        location=location,
        tooltip=cpl_value,
        icon=folium.Icon(
            color="blue",
        ),
        radius=10,
    ).add_to(m)

    folium.Marker(
        location,
        icon=DivIcon(
            icon_size=(250, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 10pt">{}</div>'.format(cpl_value),
        ),
    ).add_to(m)


dir_prefix = os.path.dirname(os.path.abspath(__file__)) + "/"


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, compress=False)


app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    [
                        html.H1(children="CPL per district"),
                    ],
                    className="six columns",
                ),
                html.Div(
                    [
                        html.Iframe(
                            id="map",
                            srcDoc=open(dir_prefix + "index.html", "r").read(),
                            width="100%",
                            height="600",
                        ),
                    ]
                ),
            ]
        ),
    ]
)


def _decode_point_from_mysql(value):
    coords = value[6:-1]
    # assert False, coords
    coord_tuple = list(reversed(coords.split(" ")))
    # assert False, coord_tuple

    return tuple([float(v) for v in coord_tuple])


DATA_LOCATION = Path(__file__).parent.resolve() / "map_location_info.json"


def load_data():
    with open(DATA_LOCATION, "r") as fp:
        result = json.load(fp)

    transformed = list()
    recorded_locations = set()
    for value in result:
        if value["location"] is None:
            continue
        decoded_location = _decode_point_from_mysql(value["location"])

        if decoded_location in recorded_locations:
            continue

        recorded_locations.add(decoded_location)

        decoded_value = {
            # "ctime": datetime.strptime(
            #     value["ctime"].split(".")[0], "%Y-%m-%d %H:%M:%S"
            # ),
            "location": decoded_location,
            "cpl": value["cpl"],
        }
        transformed.append(decoded_value)

    return transformed


from datetime import datetime


def prettify_text(cpl, **kwargs):
    # formatted_date = ctime.strftime("%Y-%m-%d %H:%M:%S")
    formatted_cpl = f"{cpl:.0f}₽"

    return f"{formatted_cpl}"


def draw_the_map():
    data = load_data()
    for point in data:
        pretty_text = prettify_text(**point)
        add_data_point(point["location"], pretty_text)

    m.save(dir_prefix + "index.html")


def run_server():
    subprocess.run(f"{dir_prefix}/kill_server.sh")
    app.run_server(host="0.0.0.0", port=4258)


if __name__ == "__main__":
    draw_the_map()
    run_server()
