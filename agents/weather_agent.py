# agents/weather_agent.py
import logging
from tools.weather_tool import get_weather

class WeatherAgent:
    def run(self, data: dict):
        city = data.get("city")
        logging.info(f"WeatherAgent: fetching weather for {city}")
        weather = get_weather(city)
        data["weather"] = weather
        logging.info(f"WeatherAgent: weather -> {weather}")
        return data
