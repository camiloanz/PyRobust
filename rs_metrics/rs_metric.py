from . import (
    availability,
    average_path_length,
    average_path_length_in_hops,
    betweenness_centrality,
    closeness_centrality,
    connectivity,
    diameter,
    eccentricity,
    edge_betweenness,
    eigenvector_centrality,
    harmonic_centrality,
    maxflow,
    nodal_degree,
    rLCC,
    strength
)

# Mapping of metric names to their respective function
metric_func = {
    "availability": availability.calculate_availability,
    "average_path_length": average_path_length.calculate_avg_path_length,
    "average_path_length_in_hops": average_path_length_in_hops.calculate_avg_path_length_hops,
    "betweenness_centrality": betweenness_centrality.calculate_betweenness,
    "closeness_centrality": closeness_centrality.calculate_closeness,
    "connectivity": connectivity.calculate_connectivity,
    "diameter": diameter.calculate_diameter,
    "eccentricity": eccentricity.calculate_eccentricity,
    "edge_betweenness": edge_betweenness.calculate_edge_betweenness,
    "eigenvector_centrality": eigenvector_centrality.calculate_eigenvector,
    "harmonic_centrality": harmonic_centrality.calculate_harmonic,
    "maxflow": maxflow.calculate_maxflow,
    "nodal_degree": nodal_degree.calculate_nodal_degree,
    "rLCC": rLCC.calculate_rLCC,
    "strength": strength.calculate_strength
}


def compute_metric(graph, metric, mode="rs_value", **kwargs):
    """
    @brief Dispatches the appropriate robustness metric function based on name and mode.

    This function dynamically selects a metric computation function from a predefined
    registry and calls it with the given arguments.

    @param graph The input igraph.Graph instance.
    @param metric Either:
        - A string (e.g. "strength", "rLCC")
        - Or a tuple ("metric_name", aggregation_type) e.g. ("strength", "mean")
    @param mode Either "rs_value" for numerical result or "targeted" for node/edge ranking.
    @param kwargs Additional arguments passed to the metric function (e.g., weight, capacity).

    @return
        - If mode == "rs_value": A float representing the computed metric.
        - If mode == "targeted": A tuple of (ranking, failing_nodes, failing_edges).
    """

    if isinstance(metric, tuple):
        name, agg_type = metric
        if mode == "targeted":
            return metric_func[name](graph, mode, type=None, **kwargs)
        else:
            return metric_func[name](graph, mode, agg_type, **kwargs)
    else:
        return metric_func[metric](graph, mode, **kwargs)
   