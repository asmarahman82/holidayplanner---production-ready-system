# tests/test_fairness.py
import pytest
from agents.itinerary_agent import ItineraryAgent

@pytest.mark.parametrize("budget,expected_preference", [
    (1000, "budget"),   # low budget -> affordable options
    (5000, "mixed"),    # medium budget -> mix of options
    (10000, "luxury")   # high budget -> luxury options
])
def test_budget_fairness(budget, expected_preference):
    """
    Ensure that itinerary generation adapts fairly based on budget
    and doesn't always favor luxury or specific destinations.
    """
    agent = ItineraryAgent()
    response = agent.generate_itinerary("Paris", budget=budget, days=3)

    # Basic fairness rules
    response_text = response.lower()
    if expected_preference == "budget":
        assert "hostel" in response_text or "affordable" in response_text or "cheap" in response_text, \
            f"For low budget, itinerary should contain affordable suggestions. Got: {response_text[:200]}"

    elif expected_preference == "luxury":
        assert "hotel" in response_text or "luxury" in response_text or "resort" in response_text, \
            f"For high budget, itinerary should contain premium suggestions. Got: {response_text[:200]}"

    else:
        assert any(word in response_text for word in ["affordable", "mid-range", "luxury"]), \
            "For medium budget, itinerary should show a mix of options."

def test_destination_diversity():
    """
    Ensure system doesn't always recommend the same popular destinations,
    even with different user preferences.
    """
    agent = ItineraryAgent()
    destinations = []
    for _ in range(5):
        itinerary = agent.generate_itinerary("Random", budget=2000, days=3)
        for city in ["Paris", "London", "Dubai", "Tokyo", "New York"]:
            if city.lower() in itinerary.lower():
                destinations.append(city)

    diversity = len(set(destinations))
    assert diversity >= 3, f"Expected diverse destinations, got only: {set(destinations)}"
