import json
import os
import random
import time
from pathlib import Path

import dash
import folium
import MySQLdb
from dash import html
from folium.features import DivIcon

loc = (55.75, 37.6)
m = folium.Map(location=loc, zoom_start=12)


def add_data_point(location, cpl_value):
    print(f"!!!!!!! add_data_point({location}, {cpl_value})")
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

map_path = dir_prefix + "index.html"


def _open_map_file():
    return open(map_path, "r").read()


def _decode_point_from_mysql(value):
    coords = value[6:-1]
    coord_tuple = list(reversed(coords.split(" ")))

    return tuple([float(v) for v in coord_tuple])


DATA_LOCATION = Path(__file__).parent.resolve() / "map_location_info.json"


def _load_data_from_file():
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


def generate_cpl(seed=1):
    return random.Random(seed).uniform(150, 400)


env = os.getenv("ENV")


def _db_connection():
    if env != "DOCKER":
        db = MySQLdb.connect(passwd="thesis_password_12345", db="thesis", user="thesis_user", host="localhost")
        return db
    else:
        i = 0
        while True:
            try:
                db = MySQLdb.connect(
                    passwd="thesis_password_12345", db="thesis", user="thesis_user", host="db", port=3306
                )
                return db
            except MySQLdb.Error:  # noqa
                if i == 0:
                    print("wait for db start")
                else:
                    print(".")
                i += 0.5
                time.sleep(2**i)


def _load_data_from_db():
    db = _db_connection()
    print("!!!!!!!!!!! LOADING")
    with db.cursor() as c:
        c.execute("select ST_X(location), ST_Y(location) from thesis_address")
        coordinates = set(c.fetchall())
    result = []
    for coord in coordinates:
        result.append({"cpl": generate_cpl(coord[0] + coord[1]), "location": (coord[1], coord[0])})
    return result


def load_data():
    res = _load_data_from_db()
    print("len of fetched result: ", len(res))
    from pprint import pprint

    pprint(res)
    return res


def prettify_text(cpl, **kwargs):
    formatted_cpl = f"{cpl:.0f}₽"

    return f"{formatted_cpl}"


def draw_the_map(data_):
    for point in data_:
        pretty_text = prettify_text(**point)
        add_data_point(point["location"], pretty_text)

    m.save(dir_prefix + "index.html")


def reload_map_file():
    print("reloading map file...")
    draw_the_map(load_data())


def serve_layout():
    reload_map_file()
    return html.Div(
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
                        id="map-div",
                        children=[
                            html.Iframe(
                                id="map",
                                srcDoc=_open_map_file(),
                                width="100%",
                                height="600",
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )


app.layout = serve_layout


def run_server():
    # app.run_server(host="0.0.0.0", port=4258)
    if env == "DOCKER":
        host = "0.0.0.0"
    else:
        host = "localhost"
    port = 8005
    print(f"Listen on {host}:{port}")
    app.run_server(host=host, port=port, debug=True)


if __name__ == "__main__":
    data = load_data()
    draw_the_map(data)
    run_server()
