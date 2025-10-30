# run_full_pipeline.py
import os
from datetime import datetime
import logging

# ------------------- Logger Setup -------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=f"logs/holidayplanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ------------------- Imports -------------------
from orchestration.langgraph_flow import run_holiday_planner
from orchestration.graph_visualizer import generate_flow_diagram
from tools.metrics_tool import MetricsTracker

# ------------------- Ensure Data Folders -------------------
os.makedirs("data/metrics", exist_ok=True)
os.makedirs("data/graphs", exist_ok=True)

# ------------------- Main Execution -------------------
def main():
    logger.info("Starting HolidayPlanner pipeline...")

    # Initialize metrics tracker
    metrics = MetricsTracker()

    # Sample user input (can be replaced by real input)
    user_data = {"destination": "Tokyo", "budget": 1200}

    # Run the planner (agents execute here)
    plan = run_holiday_planner(user_data)

    # Save metrics
    metrics_file = metrics.save_metrics()
    logger.info(f"Metrics saved to {metrics_file}")

    # Generate flow diagram
    diagram_path = os.path.join("data", "graphs", "holiday_planner_flow.png")
    generate_flow_diagram(
        filename=diagram_path,
        include_metrics=True,          # optional, shows node success/failure
        metrics_data=plan.get("node_metrics", {})  # optional
    )
    logger.info(f"Flow diagram saved at {diagram_path}")

    logger.info("Pipeline execution completed successfully.")
    print("✅ Pipeline completed. Check 'data/' and 'logs/' folders for output.")
