
from robustness_surface import start_robustness_surface
from graph_utils.graph_xml2nx import load_networkx_graph_from_xml

"""
This script demonstrates how to run three types of failure simulations:
1. Random failure
2. Targeted failure
3. Epidemic failure

The example topology used is "Germany_17", loaded from an XML file and  processed using NetworkX.
Each call to `start_robustness_surface` uses different example parameter configurations.
"""

# Load the Germany_17 network topology into a NetworkX graph from XML
G = load_networkx_graph_from_xml("topologies/nobel_germany.xml")

# --- Example 1: Random failure ---
start_robustness_surface(
    graph=G,
    # List of output metrics
    metrics=[("nodal_degree", "max")],
    # Enable node and/or edge failures
    failing_nodes=True,
    failing_edges=True,
    # Type of failure: "random", "targeted", or "epidemic"
    failing_type="random",
    # Ratio of edge failures to node failures (e.g., 3 means 3 edges per failed node)
    edge_ratio=3,
    # Generate a separate robustness surface for each metric
    multiple_plots=True,
    # If True, combine all metrics into one plot (requires `metric_weights`)
    reduced_single_plot=False,
    # If True, also generate an line plot across all metrics
    add_line_plot=True,
    # Save the output to CSV (stored in `rs_output/random_failures/...`)
    save_as_csv=True,
    # Number of failure scenarios to generate
    num_scenarios=15,
    # List of failure percentages to simulate
    failing_percentage_array=[i * 5 for i in range(1, 15)]
)

# --- Example 2: Targeted failure ---
start_robustness_surface(
    graph=G,
    # List of output metrics
    metrics=["connectivity"],
    # Type of failure: "random", "targeted", or "epidemic"
    # Format targeted: ("targeted", metric_name, mode) where mode is "static" or "dynamic"
    failing_type=("targeted", "betweenness_centrality", "static"),
    # Generate a separate robustness surface for each metric
    multiple_plots=True,
    # If True, combine all metrics into one plot (requires `metric_weights`)
    reduced_single_plot=False,
    # If True, also generate an line plot across all metrics
    add_line_plot=True,
    # Save the output to CSV (stored in `rs_output/targeted_failures/...`)
    save_as_csv=True,
    # List of failure percentages to simulate
    failing_percentage_array=[i * 5 for i in range(1, 15)]
)

# --- Example 3: Epidemic failure ---
start_robustness_surface(
    graph=G,
    # List of output metrics
    metrics=[("closeness_centrality", "mean"), ("eigenvector_centrality", "mean")],
    # Corresponding weights for each metric (must sum to 1.0)
    metric_weights=[0.5, 0.5],
    # Enable node and/or edge failures
    failing_nodes=True,
    failing_edges=False,
    # Type of failure: "random", "targeted", or "epidemic"
    failing_type="epidemic",
    # Generate a separate robustness surface for each metric
    multiple_plots=False,
    # If True, combine all metrics into one plot (requires `metric_weights`)
    reduced_single_plot=True,
    # If True, also generate an line plot across all metrics
    add_line_plot=False,
    # Save the output to CSV (stored in `rs_output/epidemic_failures/...`)
    save_as_csv=True,
    # Number of failure scenarios to generate
    num_scenarios=15,
    # List of failure percentages to simulate
    failing_percentage_array=[i * 5 for i in range(1, 15)]
)
