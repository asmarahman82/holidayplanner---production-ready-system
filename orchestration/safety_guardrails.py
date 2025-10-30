# orchestration/safety_guardrails.py
from fastapi import HTTPException

def validate_user_input(data: dict):
    destination = data.get("destination")
    budget = data.get("budget")

    if not destination or not isinstance(destination, str):
        raise HTTPException(status_code=400, detail="Invalid destination provided.")
    if not isinstance(budget, (int, float)) or budget <= 0:
        raise HTTPException(status_code=400, detail="Budget must be a positive number.")
    return True
