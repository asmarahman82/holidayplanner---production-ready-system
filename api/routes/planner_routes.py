# api/routes/planner_routes.py
from fastapi import APIRouter, HTTPException, Query
from orchestration.agent_manager import run_holiday_planner

router = APIRouter()

@router.post("/", summary="Generate a complete holiday plan")
async def create_plan(
    destination: str = Query(..., description="Travel destination"),
    budget: float = Query(..., gt=0, description="Budget in USD"),
    duration: int = Query(5, gt=0, description="Trip duration in days")
):
    """
    Returns a structured holiday plan with weather, places, itinerary, and budget flag.
    """
    try:
        result = run_holiday_planner(destination, budget, duration)

        response = {
            "destination": destination,
            "budget": budget,
            "plan": {
                "summary": result.get("summary", ""),
                "weather": result.get("weather", {}),
                "places": result.get("places", {}),
                "itinerary": result.get("itinerary", ""),
                "budget": result.get("budget", {}),
            },
            "status": "ok"
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning failed: {str(e)}")

@router.get("/status", summary="Health check endpoint")
async def health_check():
    return {"status": "healthy", "message": "Planner API is running"}
