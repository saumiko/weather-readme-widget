import datetime
import json
import os
import time
from base64 import b64encode

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import pytemperature
import requests
from flask import Flask, Response, render_template

weather_icons = os.path.join('static')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = weather_icons

OPENWEATHERMAP_KEY = os.getenv("OPENWEATHERMAP")

URL = "http://api.openweathermap.org/data/2.5/weather?q=Dhaka,bd&APPID=" + OPENWEATHERMAP_KEY
TIME_URL = "http://worldtimeapi.org/api/timezone/Asia/Dhaka"
ICON_URL = "http://openweathermap.org/img/wn/{}@2x.png"


def set_sys_time():
    os.environ["TZ"] = "Asia/Dhaka"
    time.tzset()


def load_image_b64(url):
    response = requests.get(url)
    return b64encode(response.content).decode("ascii")


def get_weather_data():
    data = json.loads(requests.get(URL).text)
    curr_time = datetime.datetime.fromtimestamp(data["dt"] + 21600).strftime("%d %B, %Y - %I:%M:%S %p")
    celsius = pytemperature.k2c(data["main"]["temp"])
    feels_like = pytemperature.k2c(data["main"]["feels_like"])
    max_temp = pytemperature.k2c(data["main"]["temp_max"])
    min_temp = pytemperature.k2c(data["main"]["temp_min"])
    weather_type = data["weather"][0]["main"]
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"] + 21600).strftime("%I:%M:%S %p")
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"] + 21600).strftime("%I:%M:%S %p")
    city = data["name"]
    country = data["sys"]["country"]
    icon = data["weather"][0]["icon"]
    w_data = {
        "city": city,
        "country": country,
        "curr_time": curr_time,
        "weather_type": weather_type,
        "temp": int(celsius),
        "feels_like": int(feels_like),
        "max_temp": int(max_temp),
        "min_temp": int(min_temp),
        "sunrise": sunrise,
        "sunset": sunset,
        "image": load_image_b64(ICON_URL.format(icon))
    }
    return w_data


def make_svg():
    data = get_weather_data()
    return render_template("widget.html", **data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    svg = make_svg()
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


if __name__ == "__main__":
    app.run(debug=False)
