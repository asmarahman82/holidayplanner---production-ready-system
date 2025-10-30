# tools/yelp_tool.py
import os, requests, logging
from config.settings import YELP_API_KEY
from config.constants import YELP_RESULT_LIMIT

def get_places(city: str, term: str, limit: int = YELP_RESULT_LIMIT):
    if not YELP_API_KEY:
        logging.warning("No Yelp API key set")
        return []
    try:
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
        params = {"location": city, "term": term, "limit": limit}
        r = requests.get(url, headers=headers, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        results = []
        for b in data.get("businesses", []):
            results.append({
                "name": b.get("name"),
                "rating": b.get("rating"),
                "address": ", ".join(b.get("location", {}).get("display_address", []))
            })
        return results
    except Exception as e:
        logging.error(f"yelp_tool: error getting places for {term} in {city}: {e}")
        return []
