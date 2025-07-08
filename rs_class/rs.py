import random
from graph_utils.convert_to_igraph import convert_to_igraph

class RobustnessSurface:
    def __init__(self, graph, failing_type, metrics, failing_percentage_array, num_scenarios=None,
                  failing_nodes = False, failing_edges = False, edge_ratio=None, metric_weights=None, 
                  graph_weights="weights", graph_capacity="capacity", A_dic=None, multiple_plots=False, 
                  reduced_single_plot=False, add_line_plot=False, save_as_csv=False):
        """
        Initializes the RobustnessSurface class with the given parameters.

        @param graph: The input graph to be analyzed. It will be converted to an igraph.Graph.
        @param failing_type: Defines the failure strategy: either a string ("random", "epidemic") or a tuple ("targeted", metric_name, mode).
        @param metrics: List of metric names or (metric_name, mode) tuples used in robustness evaluation.
        @param failing_percentage_array: List of percentages representing how much of the graph fails in each step.
        @param num_scenarios: Number of random failure scenarios to simulate.
        @param failing_nodes: Whether to simulate node failures.
        @param failing_edges: Whether to simulate edge failures.
        @param edge_ratio: Edge-to-node failure ratio. Required if both node and edge failure are simulated.
        @param metric_weights: Optional list of weights used for combining metrics (only used if reduced_single_plot=True).
        @param graph_weights: Name of edge attribute that stores weights (e.g. "distance", "weight").
        @param graph_capacity: Name of edge attribute representing capacity (used in flow-based metrics).
        @param A_dic Optional dictionary, passed to metric functions if needed.
        @param multiple_plots: If True, generates one surface plot per metric.
        @param reduced_single_plot: If True, combines multiple metrics into a single surface using weights.
        @param add_line_plot: If True, adds a line plot summarizing the average robustness trend.
        @param save_as_csv: If True, results are saved as CSV files in the output directory.

        @note See the full parameter documentation in docs/start_robustness_surface.md
        """

        self.igraph_graph = convert_to_igraph(graph)
        self.R = random.Random(129) 
        self.active_graph = self.igraph_graph.copy()

        self.graph_weights = graph_weights
        self.graph_capacity = graph_capacity
        self.A_dic = A_dic
        self.failing_nodes = failing_nodes
        self.failing_edges = failing_edges
        if isinstance(failing_type, tuple):
            self.failing_type = failing_type[0]
            self.targeted_metric = failing_type[1]
            self.targeted_mode = failing_type[2]
        else:
            self.failing_type = failing_type
        self.ratio = edge_ratio
        self.metrics = metrics
        self.metric_weights = metric_weights
        self.num_scenarios = num_scenarios
        self.fail_percent = failing_percentage_array
        self.multiple_plots = multiple_plots
        self.reduced_single_plot = reduced_single_plot
        self.line_plot = add_line_plot
        self.save_as_csv = save_as_csv
    