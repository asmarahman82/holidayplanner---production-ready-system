import json
import logging
from tools.groq_tool import GroqTool
from tools.weather_tool import get_weather
# from tools.places_tool import get_places   # Uncomment if you have this
from config.settings import DEFAULT_CITY, DEFAULT_BUDGET, DEFAULT_DURATION, DEFAULT_PREFERENCES

logging.basicConfig(level=logging.INFO)

def get_user_input(prompt, default):
    user_input = input(f"{prompt} (default: {default}): ").strip()
    return user_input if user_input else default

def main():
    print("✈️ Welcome to HolidayPlanner! Let us design your perfect trip.")

    city = get_user_input("Destination city", DEFAULT_CITY)
    budget = float(get_user_input("Budget in USD", DEFAULT_BUDGET))
    duration = int(get_user_input("Duration in days", DEFAULT_DURATION))
    preferences = get_user_input("Preferences (comma-separated)", ",".join(DEFAULT_PREFERENCES)).split(",")

    logging.info(f"User request: {city}, {duration} days, budget ${budget}")

    groq = GroqTool()

    # --- Weather ---
    try:
        weather = get_weather(city)
        weather_data = {
            "description": weather["weather"][0]["description"],
            "temperature": weather["main"]["temp"],
            "humidity": weather["main"]["humidity"]
        }
    except Exception as e:
        logging.warning(f"Weather fetch failed: {e}")
        weather_data = {"description": "unavailable", "temperature": None, "humidity": None}

    # --- Itinerary ---
    prompt = f"""
    Generate a complete {duration}-day itinerary for {city}.
    Include daily schedule (morning-afternoon-evening),
    activities, cultural highlights, food suggestions, and travel tips.
    Structure as 'Day 1', 'Day 2', ... up to {duration}.
    """
    try:
        itinerary = groq.generate_text(prompt)
    except Exception as e:
        logging.error(f"Itinerary generation failed: {e}")
        itinerary = "Unable to generate itinerary."

    try:
         places = get_places(city)
    except Exception as e:
         logging.warning(f"Places fetch failed: {e}")
         places = {"museums": [], "food": [], "culture": []}

    holiday_plan = {
        "destination": city,
        "summary": f"A personalized {duration}-day trip plan for {city}.",
        "weather": weather_data,
        "places": {"museums": [], "food": [], "culture": []},
        "itinerary": itinerary,
        "budget": {
            "estimate": f"${budget:,.2f}",
            "flagged": False
        }
    }

    print("\n=== Final Holiday Plan ===")
    print(json.dumps(holiday_plan, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
