# agents/destination_agent.py
import logging
from tools.yelp_tool import get_places
from tools.huggingface_tool import HuggingFaceTool

class DestinationAgent:
    def __init__(self):
        self.hf = HuggingFaceTool()

    def run(self, data: dict):
        city = data.get("city")
        logging.info(f"DestinationAgent: enriching {city}")

        # Gather top places for each preference (first preference only to keep results compact)
        preferences = data.get("preferences", [])
        places_summary = {}
        for pref in preferences[:3]:
            try:
                places = get_places(city, pref)
            except Exception as e:
                logging.error(f"DestinationAgent: yelp error for {pref} in {city}: {e}")
                places = []
            places_summary[pref] = places

        # Create a textual description for summarization
        raw_text = f"{city} highlights: "
        for k, v in places_summary.items():
            raw_text += f"{k} - {', '.join([p['name'] for p in v[:3]])}. "

        # Use HuggingFace to summarize highlights (optional)
        summary = self.hf.summarize(raw_text) if raw_text else ""
        data["destination_info"] = {
            "summary": summary,
            "places": places_summary
        }

        logging.info("DestinationAgent: enrichment complete")
        return data
