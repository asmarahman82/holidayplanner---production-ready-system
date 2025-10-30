import os
import json
import datetime
import jsonschema
from jsonschema import validate
from pathlib import Path

# ✅ Ensure metrics directory exists
metrics_dir = Path("data/metrics")
metrics_dir.mkdir(parents=True, exist_ok=True)

# 🎯 Define schema for ItineraryAgent output
itinerary_schema = {
    "type": "object",
    "properties": {
        "destination": {"type": "string"},
        "days": {"type": "integer"},
        "budget": {"type": "number"},
        "itinerary": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["destination", "days", "budget", "itinerary"]
}

# 🎯 Define schema for WeatherAgent output
weather_schema = {
    "type": "object",
    "properties": {
        "destination": {"type": "string"},
        "forecast": {"type": "string"},
        "temperature": {"type": "number"},
        "condition": {"type": "string"}
    },
    "required": ["destination", "forecast", "temperature", "condition"]
}

# 🎯 Define schema for BudgetAgent output
budget_schema = {
    "type": "object",
    "properties": {
        "total_budget": {"type": "number"},
        "daily_spending": {"type": "number"},
        "currency": {"type": "string"}
    },
    "required": ["total_budget", "daily_spending", "currency"]
}

schemas = {
    "itinerary_agent": itinerary_schema,
    "weather_agent": weather_schema,
    "budget_agent": budget_schema
}

def validate_output(agent_name: str, data: dict):
    """
    Validate the output of an agent against its schema.
    """
    if agent_name not in schemas:
        print(f"⚠️ No schema registered for {agent_name}, skipping validation.")
        return True

    try:
        validate(instance=data, schema=schemas[agent_name])
        print(f"✅ {agent_name} output valid.")
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"❌ {agent_name} output validation failed: {e.message}")
        return False


def log_evaluation(agent_name: str, data: dict, is_valid: bool):
    """
    Store evaluation results in a JSON log for auditing.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = metrics_dir / f"evaluation_{timestamp}.json"

    log_entry = {
        "timestamp": timestamp,
        "agent": agent_name,
        "valid": is_valid,
        "output_sample": data,
    }

    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=2, ensure_ascii=False)

    print(f"🪶 Evaluation log saved at: {log_path}")


def run_evaluation_pipeline(agent_name: str, data: dict):
    """
    Combine validation + logging into one call for easy integration.
    """
    print(f"\n🔍 Evaluating output from {agent_name}...")
    valid = validate_output(agent_name, data)
    log_evaluation(agent_name, data, valid)
    return valid
