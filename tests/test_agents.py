# tests/test_agents.py
import pytest
from orchestration.agent_manager import run_holiday_planner

def test_run_holiday_planner_valid():
    sample_input = {"destination": "Paris", "budget": 1000.0}
    result = run_holiday_planner(sample_input["destination"], sample_input["budget"])

    # Check the returned structure
    assert result is not None
    assert "itinerary" in result
    assert "budget" in result
    assert "destination" in result
    assert result["destination"] == sample_input["destination"]
    # Budget status should indicate within budget if 5-day default * 180/day < 1000
    assert "status" in result["budget"]

def test_run_holiday_planner_invalid_budget():
    # Negative budget should raise a ValueError
    with pytest.raises(ValueError):
        run_holiday_planner("Paris", -100)

def test_run_holiday_planner_zero_budget():
    # Zero budget should also raise ValueError
    with pytest.raises(ValueError):
        run_holiday_planner("Paris", 0)
