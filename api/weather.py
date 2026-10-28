import datetime
import os
from zoneinfo import ZoneInfo

import requests
from dotenv import find_dotenv, load_dotenv
from flask import Flask, Response, render_template

load_dotenv(find_dotenv())
app = Flask(__name__)
KEY = os.getenv("OPENWEATHERMAP")
LAT, LON = 53.35, 6.26
CITY = "Dublin, IE"
TZ = ZoneInfo("Europe/Dublin")
BASE = "https://api.openweathermap.org/data/2.5"
ONECALL = "https://api.openweathermap.org/data/3.0/onecall"


def get_json(url, params):
    response = requests.get(url, params=params, timeout=8)
    response.raise_for_status()
    return response.json()


def weather_icon(code, night, wind_speed):
    if 200 <= code < 600:
        return "rain"
    if 600 <= code < 700:
        return "snow"
    if 700 <= code < 800:
        return "fog"
    if code == 800:
        return "moon" if night else "sun"
    if code == 801:
        return "cloud-moon" if night else "cloud-sun"
    if 802 <= code <= 804:
        return "cloud"
    return "wind" if wind_speed >= 10 else "cloud"


def get_weather_widget():
    if not KEY:
        raise ValueError("OPENWEATHERMAP environment variable missing")
    params = {"lat": LAT, "lon": LON, "appid": KEY, "units": "metric"}
    weather = get_json(BASE + "/weather", params)
    observed = datetime.datetime.fromtimestamp(weather["dt"], TZ)
    now = datetime.datetime.now(TZ)
    sunrise = weather["sys"]["sunrise"]
    sunset = weather["sys"]["sunset"]
    night = not (sunrise <= weather["dt"] < sunset)
    code = int(weather["weather"][0]["id"])
    wind = float(weather.get("wind", {}).get("speed", 0)) * 3.6
    rain_probability = None
    rain_window = "Next 3h"
    alerts = []

    # Forecast endpoint is part of OpenWeather's standard 5-day/3-hour API.
    try:
        forecast = get_json(BASE + "/forecast", {**params, "cnt": 2})
        entries = forecast.get("list", [])
        if entries:
            rain_probability = round(float(entries[0].get("pop", 0)) * 100)
    except (requests.RequestException, KeyError, TypeError, ValueError):
        app.logger.warning("Forecast unavailable; rain probability hidden")

    # One Call 3.0 is subscription-dependent. Fail gracefully when not enabled.
    if os.getenv("OPENWEATHER_ONECALL_ALERTS", "").lower() in ("1", "true", "yes"):
        try:
            detail = get_json(ONECALL, {**params, "exclude": "minutely,hourly,daily"})
            alerts = detail.get("alerts", []) or []
        except (requests.RequestException, KeyError, TypeError, ValueError):
            app.logger.warning("One Call alerts unavailable; warning indicator hidden")

    alert = alerts[0].get("event", "Weather alert") if alerts else ""
    if len(alert) > 25:
        alert = alert[:24] + "…"
    return render_template(
        "widget.html",
        city=CITY,
        current_time=observed.strftime("%d %b %Y, %H:%M %Z"),
        fetched_time=now.strftime("%H:%M %Z"),
        temperature=round(weather["main"]["temp"]),
        feels_like=round(weather["main"]["feels_like"]),
        weather_type=weather["weather"][0]["description"].title(),
        wind_speed=round(wind),
        rain_probability=rain_probability,
        rain_window=rain_window,
        icon=weather_icon(code, night, wind / 3.6),
        night=night,
        alert=alert,
    )


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    try:
        svg = get_weather_widget()
        response = Response(svg, mimetype="image/svg+xml")
        response.headers["Cache-Control"] = "public, s-maxage=300, max-age=60"
        return response
    except (requests.RequestException, ValueError, KeyError, TypeError):
        app.logger.exception("Weather widget unavailable")
        return Response("Weather temporarily unavailable", status=502, mimetype="text/plain")


if __name__ == "__main__":
    app.run()
