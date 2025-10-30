from fastapi.testclient import TestClient
from api.main_api import app

client = TestClient(app)

def test_health_check():
    res = client.get("/status")
    assert res.status_code == 200

def test_plan_route():
    res = client.post("/plan/?destination=paris&budget=500&duration=3")
    assert res.status_code == 200
    assert "plan" in res.json()
