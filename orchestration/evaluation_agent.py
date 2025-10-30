# orchestration/evaluation_agent.py
def evaluate_plan(plan):
    issues = []
    if plan["budget_estimate"] > 1.2 * plan["budget"]["estimate"]:
        issues.append("Plan exceeds budget limit")
    if len(plan.get("itinerary", {})) < 3:
        issues.append("Itinerary is too short")
    if not plan.get("weather", {}).get("description"):
        issues.append("Weather data missing")

    score = max(0, 10 - len(issues)*2)
    return {"score": score, "issues": issues or ["All good!"]}
