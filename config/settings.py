# config/settings.py
from dotenv import load_dotenv
import os

# Load .env specifically from config folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
YELP_API_KEY = os.getenv("YELP_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Paris")
DEFAULT_BUDGET = int(os.getenv("DEFAULT_BUDGET", 1000))
DEFAULT_DURATION = int(os.getenv("DEFAULT_DURATION", 5))
DEFAULT_PREFERENCES = os.getenv("DEFAULT_PREFERENCES", "museums,food,culture").split(",")

MCP_ENABLED = os.getenv("MCP_ENABLED", "True").lower() in ("1", "true", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

