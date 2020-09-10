import datetime
import io
import json
import os
import time
from base64 import b64encode

import configparser
import pytemperature
import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, render_template

GITHUB_USERNAME = "saumiko"
GITHUB_REPO = "weather-readme-widget"
GIT_BRANCH = "master"

CONFIG_FILE_URL = "https://raw.githubusercontent.com/{}/{}/{}/api/config.ini".format(GITHUB_USERNAME,
                                                                                     GITHUB_REPO,
                                                                                     GIT_BRANCH)

CONFIGURATION = requests.get(CONFIG_FILE_URL).text

config_buffer = io.StringIO(CONFIGURATION)

config = configparser.ConfigParser()
config.read_file(config_buffer)

load_dotenv(find_dotenv())

app = Flask(__name__)

OPENWEATHERMAP_KEY = os.getenv("OPENWEATHERMAP")
OPENWEATHERMAP_API_URL = config["api"]["openweathermap"].format(config["timezone"]["city"],
                                                                config["timezone"]["country"],
                                                                OPENWEATHERMAP_KEY)
ICON_URL = config["icon"]["openweathermap"]
UTC_PLUS = int(config["timezone"]["utc_plus"])
UTC_MINUS = int(config["timezone"]["utc_minus"])
UTC_BALANCE = UTC_PLUS + UTC_MINUS

"""
This program will give wrong output in local.
This is configured for Vercel deployment.
Since it runs on UTC..
"""


def set_sys_time():
    os.environ["TZ"] = config["timezone"]["sys"]
    time.tzset()


def load_image_b64(url):
    response = requests.get(url)
    return b64encode(response.content).decode("ascii")


def get_weather_widget():
    weather_data = json.loads(requests.get(OPENWEATHERMAP_API_URL).text)
    current_time = datetime.datetime.fromtimestamp(weather_data["dt"] + UTC_BALANCE).strftime("%d %B, %Y - %I:%M:%S %p")
    temperature = pytemperature.k2c(weather_data["main"]["temp"])
    feels_like = pytemperature.k2c(weather_data["main"]["feels_like"])
    max_temperature = pytemperature.k2c(weather_data["main"]["temp_max"])
    min_temperature = pytemperature.k2c(weather_data["main"]["temp_min"])
    weather_type = weather_data["weather"][0]["main"]
    sunrise = datetime.datetime.fromtimestamp(weather_data["sys"]["sunrise"] + UTC_BALANCE).strftime("%I:%M:%S %p")
    sunset = datetime.datetime.fromtimestamp(weather_data["sys"]["sunset"] + UTC_BALANCE).strftime("%I:%M:%S %p")
    city = weather_data["name"]
    country = weather_data["sys"]["country"]
    icon = weather_data["weather"][0]["icon"]
    w_data = {
        "city": city,
        "country": country,
        "current_time": current_time,
        "weather_type": weather_type,
        "temperature": int(temperature),
        "feels_like": int(feels_like),
        "max_temperature": int(max_temperature),
        "min_temperature": int(min_temperature),
        "sunrise": sunrise,
        "sunset": sunset,
        "image": load_image_b64(ICON_URL.format(icon))
    }
    return render_template("widget.html", **w_data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    svg = get_weather_widget()
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


if __name__ == "__main__":
    app.run(debug=True)
