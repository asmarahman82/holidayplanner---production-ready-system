### 📡 **docs/api_reference.md**

markdown
# 📡 API Reference

The HolidayPlanner backend is built with **FastAPI** and exposes three main endpoints.

## Base URL
http://localhost:8000

## 🧭 Endpoints

| Method | Endpoint | Description |
|---------|-----------|-------------|
| GET | `/` | Root welcome message |
| POST | `/plan` | Generate holiday itinerary |
| GET | `/status` | Health and uptime check |


### plan (POST)
Generate a complete plan given a destination and budget.

**Example:**
curl -X POST "http://localhost:8000/plan?destination=Tokyo&budget=2000"
Response:
{
  "destination": "Tokyo",
  "budget": 2000,
  "plan": {
    "itinerary": "...",
    "weather": "...",
    "budget_breakdown": "..."
  }
}

### status (GET)
Check API uptime and system health.
Response:
{
  "status": "ok",
  "uptime_seconds": 234.22,
  "message": "HolidayPlanner API is healthy ✅"
}

🧩 Notes:

All requests are JSON-based.
For authentication or rate-limiting, extend FastAPI middleware.
The API can be consumed by your Streamlit frontend or external apps.