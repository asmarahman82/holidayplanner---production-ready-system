# tools/weather_tool.py
import os, requests, logging
from config.settings import OPENWEATHER_API_KEY

def get_weather(city: str):
    if not OPENWEATHER_API_KEY:
        logging.warning("No OpenWeather API key set")
        return {"error": "No API key"}
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        d = r.json()
        return {
            "description": d["weather"][0]["description"],
            "temp": d["main"]["temp"],
            "humidity": d["main"]["humidity"],
        }
    except Exception as e:
        logging.error(f"weather_tool: error fetching weather for {city}: {e}")
        return {"error": str(e)}
