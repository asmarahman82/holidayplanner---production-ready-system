# agents/result_agent.py
import logging

class ResultAggregator:
    def run(self, data: dict):
        logging.info("ResultAggregator: composing final summary")
        return {
            "destination": data.get("city"),
            "summary": data.get("destination_info", {}).get("summary"),
            "weather": data.get("weather"),
            "places": data.get("destination_info", {}).get("places"),
            "itinerary": data.get("itinerary_text"),
            "budget": data.get("budget_estimate")
        }
