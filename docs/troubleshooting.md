### 🧰 **docs/troubleshooting.md**

```markdown
# 🧰 Troubleshooting Guide

Common issues and how to fix them when running or deploying HolidayPlanner.

---

## 🧩 1. Import Errors

**Error:**

1. ModuleNotFoundError: No module named 'agents'
Fix:
Ensure your project root is in `PYTHONPATH`:
export PYTHONPATH=$(pwd)

2. API Not Starting
Address already in use: 8000
Fix:
Free the port or run on another one:
uvicorn api.main_api:app --port 8080

3. Railway Deployment Fails
Cause: Missing environment variables or port exposure.
Fix:
Ensure .env values are added in Railway dashboard.
Expose both ports 8000 (FastAPI) and 8501 (Streamlit) in Docker.

4. Weather or Budget Data Empty
Cause: Invalid API keys or quota exhausted.
Fix:
Check OPENWEATHER_KEY validity.
Add error handling in weather_agent.py.

5. Metrics or Logs Not Updating
Cause: Missing logs/ directory.
Fix:
mkdir -p logs
touch logs/agent_logs.txt

6. Streamlit Fails to Connect to API
Fix:
Ensure Streamlit calls FastAPI on the same host (localhost:8000) or via the deployed Railway domain.
Run docker logs <container_id> for debugging live containers.
Enable verbose logging in .env:
LOG_LEVEL=DEBUG
Always check API docs at /docs before testing endpoints.

