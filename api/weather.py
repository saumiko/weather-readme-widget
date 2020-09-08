import datetime
import json
import os
import time

import pytemperature
import requests
from flask import Flask, Response, render_template

app = Flask(__name__)

OPENWEATHERMAP_KEY = os.getenv("OPENWEATHERMAP")

URL = "http://api.openweathermap.org/data/2.5/weather?q=Dhaka,bd&APPID=" + OPENWEATHERMAP_KEY


def set_sys_time():
    os.environ["TZ"] = "Asia/Dhaka"
    time.tzset()


def get_weather_data():
    data = json.loads(requests.get(URL).text)
    celsius = pytemperature.k2c(data["main"]["temp"])
    feels_like = pytemperature.k2c(data["main"]["feels_like"])
    weather_type = data["weather"][0]["main"]
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%I:%M:%S %p')
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%I:%M:%S %p')
    current_time = time.strftime('%I:%M:%S %p')
    city = data["name"]
    country = data["sys"]["country"]
    w_data = {
        "temp": int(celsius),
        "weather_type": weather_type,
        "feels_like": int(feels_like),
        "city": city,
        "country": country,
        "current_time": current_time,
        "sunrise": sunrise,
        "sunset": sunset,
        "new_l": ""
    }
    return w_data


def make_svg():
    data = get_weather_data()
    return render_template("template.html", **data)


@app.route("/")
def catch_all():
    svg = make_svg()
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"
    return resp


if __name__ == "__main__":
    set_sys_time()
    app.run(debug=True)
