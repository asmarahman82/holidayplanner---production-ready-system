# orchestration/validators.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Itinerary(BaseModel):
    Day_1: Optional[str] = Field(None, alias="Day 1")
    Day_2: Optional[str] = Field(None, alias="Day 2")
    Day_3: Optional[str] = Field(None, alias="Day 3")

class HolidayPlanSchema(BaseModel):
    destination: str
    weather_summary: str
    budget_estimate: float
    activities: List[str]
    itinerary: Dict[str, str]
    notes: str
