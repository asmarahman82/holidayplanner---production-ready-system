from fastapi import FastAPI
from api.routes import planner_routes, status_routes

app = FastAPI(
    title="HolidayPlanner API",
    version="1.0.0",
    description="Multi-agent holiday planning API built for production readiness."
)

# Include routes
app.include_router(planner_routes.router, prefix="/plan", tags=["Planner"])
app.include_router(status_routes.router, prefix="/status", tags=["Status"])

@app.get("/", summary="Root endpoint")
async def root():
    return {"message": "Welcome to the HolidayPlanner API 🚀"}

