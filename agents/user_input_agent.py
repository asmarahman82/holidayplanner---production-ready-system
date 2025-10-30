# agents/user_input_agent.py
import logging
from config.settings import DEFAULT_CITY, DEFAULT_BUDGET, DEFAULT_DURATION, DEFAULT_PREFERENCES

class UserInputAgent:
    def run(self, data: dict):
        logging.info("UserInputAgent: validating input")
        # fill missing with defaults
        data.setdefault("city", DEFAULT_CITY)
        data.setdefault("budget", DEFAULT_BUDGET)
        data.setdefault("duration", DEFAULT_DURATION)
        data.setdefault("preferences", DEFAULT_PREFERENCES)
        # basic validation
        if data["duration"] <= 0:
            raise ValueError("Duration must be >= 1")
        if data["budget"] < 0:
            raise ValueError("Budget must be non-negative")
        logging.info(f"UserInputAgent: validated {data}")
        return data
