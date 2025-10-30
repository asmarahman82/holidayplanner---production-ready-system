# orchestration/agent_manager.py
from orchestration.langgraph_flow import orchestrate_holiday_planner
from orchestration.safety_guardrails import validate_user_input

def run_holiday_planner(destination: str, budget: float):
    user_input = {"destination": destination, "budget": budget}
    validate_user_input(user_input)
    return orchestrate_holiday_planner(user_input)
