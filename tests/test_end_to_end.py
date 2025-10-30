import pytest
from unittest.mock import patch
import requests

API_URL = "http://127.0.0.1:8000"  # Ensure API is running

@patch("orchestration.agent_manager.run_holiday_planner")
def test_api_plan_endpoint(mock_planner):
    # Mock the planner
    mock_planner.return_value = {"destination": "London", "plan": "sample plan"}
    
    # Send request as query parameters since your endpoint uses Query
    resp = requests.post(f"{API_URL}/plan/?destination=London&budget=500")
    assert resp.status_code == 200
    data = resp.json()
    assert data["plan"] is not None


