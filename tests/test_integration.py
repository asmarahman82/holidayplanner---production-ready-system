import pytest
from unittest.mock import patch
from tools.metrics_tool import MetricsTracker
from orchestration.agent_manager import run_holiday_planner

@pytest.fixture
def metrics():
    return MetricsTracker()

@patch("orchestration.agent_manager.run_holiday_planner")
def test_integration_agent_metrics(mock_run, metrics):
    # Mock the return value to match your current holiday planner output
    mock_run.return_value = {
        "destination": "Tokyo",
        "itinerary": "Sample itinerary",
        "budget": {"estimate": "$900.00", "limit": "$1,200.00", "status": "✅ Within Budget"},
        "weather": {"description": "Sunny", "temperature": "25°C", "humidity": "50%"},
        "places": {"museums": [], "food": [], "culture": []},
        "notes": "Sample notes"
    }

    # Call the function (mocked)
    result = run_holiday_planner("Tokyo", 1200)

    # Log the event
    metrics.log_event("test_integration", {"result": result})

    # Assertions
    assert result is not None
    assert "itinerary" in result
    assert "budget" in result
    assert result["destination"] == "Tokyo"

