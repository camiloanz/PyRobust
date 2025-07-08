from rs_class.rs_random import RandomFailureRobustness
from rs_class.rs_targeted import TargetedFailureRobustness
from rs_class.rs_epidemic import EpidemicFailureRobustness


def start_robustness_surface(graph, failing_type, metrics, failing_percentage_array, num_scenarios=None, 
         failing_nodes=False, failing_edges=False, edge_ratio=None, metric_weights=None, 
         graph_weights="distance", graph_capacity="capacity", A_dic=None, multiple_plots=False, 
         reduced_single_plot=False, add_line_plot=False, save_as_csv=False):
    
    """
    Starts the robustness surface simulation for a given graph and failure model.

    This function delegates to a specific robustness simulation class depending on the selected failure type:
    - Random node/edge failures
    - Targeted attacks based on metrics
    - Epidemic-style spreading failures

    @param graph: Input graph to be analyzed. Will be converted to igraph internally.
    @param failing_type: Either "random", "epidemic", or a tuple ("targeted", metric_name, mode).
    @param metrics: List of metric names or (metric_name, mode) tuples to compute.
    @param failing_percentage_array: List of failure percentages to simulate.
    @param num_scenarios: Number of random failure scenarios
    @param failing_nodes: Whether to simulate node failures.
    @param failing_edges: Whether to simulate edge failures.
    @param edge_ratio: Edge-to-node failure ratio (required if both nodes and edges fail).
    @param metric_weights: List of weights to combine metrics (used in reduced_single_plot).
    @param graph_weights: Name of the edge attribute storing weights/distances (default: "distance").
    @param graph_capacity: Name of the edge attribute representing capacity (default: "capacity").
    @param A_dic: Optional dictionary with additional inputs (e.g. for plotting or annotation).
    @param multiple_plots: If True, generates a separate plot for each metric.
    @param reduced_single_plot: If True, generates a combined plot using weighted metrics.
    @param add_line_plot: If True, adds a line plot summarizing the trend over failure steps.
    @param save_as_csv: If True, saves all results to CSV files in the output folder.

    @raises ValueError: If an unsupported `failing_type` is passed.
    """
    
    fail_type_mapping = {
        "random": RandomFailureRobustness,
        ("targeted", failing_type[1], failing_type[2]): TargetedFailureRobustness,
        "epidemic": EpidemicFailureRobustness
    }
    if failing_type in fail_type_mapping:
        fail_type_mapping[failing_type](
            graph=graph, 
            failing_type=failing_type, 
            metrics=metrics, 
            failing_percentage_array=failing_percentage_array,
            num_scenarios=num_scenarios, 
            failing_nodes=failing_nodes, 
            failing_edges=failing_edges, 
            edge_ratio=edge_ratio,
            metric_weights=metric_weights, 
            graph_weights=graph_weights, 
            graph_capacity=graph_capacity,
            A_dic=A_dic,
            multiple_plots=multiple_plots, 
            reduced_single_plot=reduced_single_plot, 
            add_line_plot=add_line_plot,
            save_as_csv=save_as_csv
        )
    else:
        raise ValueError(f"Unknown failing_type: {failing_type}. Supported: {list(fail_type_mapping.keys())}")
    
