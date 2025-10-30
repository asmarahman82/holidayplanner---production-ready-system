# orchestration/langgraph_flow.py
import logging, os
from agents.user_input_agent import UserInputAgent
from agents.destination_agent import DestinationAgent
from agents.weather_agent import WeatherAgent
from agents.itinerary_agent import ItineraryAgent
from agents.budget_agent import BudgetAgent
from agents.result_agent import ResultAggregator
from tools.mcp_client import MCPClient
from tools.metrics_tool import MetricsTracker

logger = logging.getLogger(__name__)

# ------------------------ Graph & Node Definitions ------------------------
class Node:
    def __init__(self, fn):
        self.fn = fn

class Graph:
    def __init__(self, name=""):
        self.name = name
        self.nodes = {}
        self.edges = []

    def add_node(self, name, node):
        self.nodes[name] = node

    def connect(self, src, dest):
        self.edges.append((src, dest))

    def get_node(self, name):
        return self.nodes[name]

# ------------------------ Flow Builder ------------------------
def build_holiday_planner_flow():
    """
    Constructs the HolidayPlanner workflow graph with all agents connected.
    """
    graph = Graph(name="HolidayPlannerFlow")
    graph.add_node("user_input", Node(UserInputAgent()))
    graph.add_node("destination_agent", Node(DestinationAgent()))
    graph.add_node("weather_agent", Node(WeatherAgent()))
    graph.add_node("itinerary_agent", Node(ItineraryAgent()))
    graph.add_node("budget_agent", Node(BudgetAgent()))
    graph.add_node("result_aggregator", Node(ResultAggregator()))

    graph.connect("user_input", "destination_agent")
    graph.connect("destination_agent", "weather_agent")
    graph.connect("weather_agent", "itinerary_agent")
    graph.connect("itinerary_agent", "budget_agent")
    graph.connect("budget_agent", "result_aggregator")

    return graph

# ------------------------ Flow Execution ------------------------
def run_holiday_planner(user_data: dict, visualize=True):
    """
    Executes the HolidayPlanner flow and optionally generates a flow diagram with metrics.
    """
    metrics = MetricsTracker()
    mcp = MCPClient()
    graph = build_holiday_planner_flow()
    node_metrics = {}

# Save metrics to file
    metrics_file = metrics.save_metrics()
    logger.info(f"Metrics saved to {metrics_file}")


    logger.info("Starting HolidayPlanner execution...")

    # Execute nodes sequentially
    for node_name, node_obj in graph.nodes.items():
        try:
            result = node_obj.fn(user_data)
            node_metrics[node_name] = "✅ Success"
            logger.info(f"Node '{node_name}' executed successfully.")
        except Exception as e:
            result = None
            node_metrics[node_name] = f"❌ Failed: {e}"
            logger.error(f"Node '{node_name}' failed: {e}")

        user_data[node_name] = result
        metrics.log_event(f"{node_name}_execution", {"result": result})

    final_plan = user_data.get("result_aggregator", {})

    # Import generate_flow_diagram only when needed to avoid circular imports
    if visualize:
        from orchestration.graph_visualizer import generate_flow_diagram
        diagram_path = os.path.join("data", "graphs", "holiday_planner_flow.png")
        generate_flow_diagram(
            filename=diagram_path,
            include_metrics=True,
            metrics_data=node_metrics
        )
        logger.info(f"Flow diagram saved at {diagram_path}")

    logger.info("HolidayPlanner execution completed.")
    return final_plan
