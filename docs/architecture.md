# 🧩 HolidayPlanner Architecture

HolidayPlanner is a **multi-agent travel planning system** built with **FastAPI**, **Streamlit**, and a modular orchestration flow using **LangGraph-style chaining**.


## 🔷 System Overview

User → Streamlit UI → FastAPI API → Orchestration Layer → Agents → Response


Each request flows through a coordinated chain of specialized agents, ensuring modularity and clean separation of concerns.


## 🧠 Core Components

| Layer | Description |
|--------|--------------|
| **UI (Streamlit)** | User-friendly interface for entering trip preferences and displaying itineraries. |
| **API (FastAPI)** | Exposes REST endpoints (`/plan`, `/status`) for external or frontend integration. |
| **Orchestration (LangGraph Flow)** | Controls the multi-agent pipeline with logging, retries, and graph visualization. |
| **Agents** | Each agent performs one task — input cleaning, weather lookup, budgeting, itinerary generation, etc. |
| **Metrics & Logging** | `MetricsAgent` measures runtime performance; `logger.py` logs all agent events. |

---

## 🔗 Data Flow Between Agents

1. **UserInputAgent** → Cleans and validates user input.  
2. **DestinationAgent** → Suggests destinations or enriches location info.  
3. **WeatherAgent** → Fetches and attaches real-time weather data.  
4. **BudgetAgent** → Estimates total and daily costs.  
5. **ItineraryAgent** → Builds a multi-day plan based on interests, weather, and budget.  
6. **ResultAgent** → Combines all data into a final, readable output.  
7. **MetricsAgent** → Records performance and completion metrics for observability.  

---

## 🧩 Key Files

| Path | Purpose |
|------|----------|
| `orchestration/langgraph_flow.py` | Builds and runs the agent chain. |
| `orchestration/graph_visualizer.py` | Visualizes the execution flow graph. |
| `agents/metrics_agent.py` | Tracks timing and logs performance metrics. |
| `api/main_api.py` | Entry point for FastAPI backend. |
| `ui/app.py` | Streamlit interface for user interaction. |

---

## 🧭 Observability
- **MetricsAgent** → logs event durations and counts.  
- **Logger** (`utils/logger.py`) → structured log files (`logs/agent_logs.txt`).  
- **Graph Visualizer** → renders agent execution order for debugging.
