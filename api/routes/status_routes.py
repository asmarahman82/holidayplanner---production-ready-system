from fastapi import APIRouter
import time

router = APIRouter()
start_time = time.time()

@router.get("/", summary="Check API status and uptime")
async def get_status():
    uptime = round(time.time() - start_time, 2)
    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "message": "HolidayPlanner API is healthy ✅"
    }
