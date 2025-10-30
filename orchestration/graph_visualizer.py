# orchestration/graph_visualizer.py
import os
import matplotlib.pyplot as plt
import networkx as nx

def generate_flow_diagram(filename: str, include_metrics: bool = False, metrics_data: dict = None):
    """
    Generate a simple directed graph visualization of the HolidayPlanner pipeline.
    Optionally includes node-level execution metrics.
    """
    # Define node connections
    edges = [
        ("user_input", "destination_agent"),
        ("destination_agent", "weather_agent"),
        ("weather_agent", "itinerary_agent"),
        ("itinerary_agent", "budget_agent"),
        ("budget_agent", "result_aggregator")
    ]

    # Create graph
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Node color based on metrics (if available)
    node_colors = []
    if include_metrics and metrics_data:
        for node in G.nodes():
            status = metrics_data.get(node, "")
            if "✅" in status:
                node_colors.append("lightgreen")
            elif "❌" in status:
                node_colors.append("lightcoral")
            else:
                node_colors.append("lightgray")
    else:
        node_colors = ["skyblue"] * len(G.nodes)

    # Layout and draw
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 5))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=9,
        font_weight="bold",
        arrows=True,
        edgecolors="black"
    )

    # Add optional text overlay for metrics summary
    if include_metrics and metrics_data:
        success = sum("✅" in v for v in metrics_data.values())
        failed = sum("❌" in v for v in metrics_data.values())
        plt.title(f"HolidayPlanner Flow\n✅ Success: {success} | ❌ Failed: {failed}", fontsize=10)

    # Save diagram
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
