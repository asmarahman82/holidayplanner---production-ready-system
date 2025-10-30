# orchestration/agent_manager.py
# orchestration/agent_manager.py
import logging
from tools.groq_tool import GroqTool
from tools.weather_tool import get_weather

logger = logging.getLogger(__name__)

def run_holiday_planner(destination: str, budget: float, duration: int = 5):
    """
    Generates a complete holiday plan including weather, itinerary, places, and budget evaluation.
    Raises ValueError if budget or duration is invalid.
    """
    # --- INPUT VALIDATION ---
    if budget <= 0:
        raise ValueError("Budget must be positive")
    if duration <= 0:
        raise ValueError("Duration must be positive")

    preferences = ["museums", "food", "culture"]
    groq = GroqTool()

    logger.info(f"Starting holiday planner for {destination}, {duration} days, budget ${budget}")

    # --- WEATHER HANDLING ---
    try:
        weather_data = get_weather(destination)
        if weather_data and "temperature" in weather_data:
            temp = weather_data["temperature"]
            if not isinstance(temp, str):
                weather_data["temperature"] = f"{temp}°C"
            elif "°" not in temp:
                weather_data["temperature"] = f"{temp}°C"
    except Exception as e:
        logger.warning(f"Weather API failed: {e}")
        weather_data = {"description": "Unavailable", "temperature": "-", "humidity": "-"}

    # --- ITINERARY GENERATION ---
    try:
        prompt = (
            f"Create a {duration}-day itinerary for {destination} including "
            f"{', '.join(preferences)}. Provide times, activities, and travel tips."
        )
        itinerary = groq.generate_text(prompt)
    except Exception as e:
        logger.error(f"GroqTool failed to generate itinerary: {e}")
        itinerary = "Itinerary generation failed. Please try again later."

    # --- BUDGET LOGIC ---
    avg_cost_per_day = 180  # baseline assumption
    est_cost = duration * avg_cost_per_day
    budget_status = (
        "✅ Within Budget" if est_cost <= budget
        else "⚠️ Over Budget – consider increasing your budget"
    )

    # --- MAIN PLAN OUTPUT ---
    holiday_plan = {
        "destination": destination,
        "summary": f"A personalized {duration}-day trip plan for {destination} including {', '.join(preferences)}.",
        "weather": weather_data,
        "places": {
            "museums": [],
            "food": [],
            "culture": []
        },
        "itinerary": itinerary,
        "budget": {
            "estimate": f"${est_cost:,.2f}",
            "limit": f"${budget:,.2f}",
            "status": budget_status,
        },
        "notes": "Plan optimized for cultural and culinary experiences. Adjust duration or budget for more premium options.",
    }

    logger.info(f"Holiday plan generated for {destination}")
    return holiday_plan


# --- HEALTH CHECK ---
def get_status():
    """
    Lightweight health check endpoint for observability.
    """
    try:
        GroqTool()  # simple init check
        return {"status": "ok", "agents": ["GroqTool", "WeatherTool"]}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "degraded", "error": str(e)}
