import numpy as np

def calculate_maxflow(graph, mode, type=None, capacity="capacity", **kwargs):
    """
    @brief Computes the average maximum flow between all node pairs.

    For each distinct pair of nodes, this function computes the maximum flow value
    using the specified edge capacity attribute. It then aggregates the results
    using the specified method (mean, min, or max).

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: only "rs_value" is currently supported.
    @param type Aggregation method for flow values: "mean", "max", or "min".
    @param capacity Name of the edge attribute representing flow capacity.
    @param kwargs Optional keyword arguments (ignored).

    @return A float representing the aggregated maximum flow metric.
    """

    if mode != "rs_value":
        raise NotImplementedError("Only 'rs_value' mode is supported for maximum flow.")

    if graph.vcount() < 2:
        return 0  # Not enough nodes to compute flow

    nodes = range(len(graph.vs))
    max_flows = []

    for source in nodes:
        for target in nodes:
            if source != target:
                try:
                    flow = graph.maxflow_value(source, target, capacity=capacity)
                    max_flows.append(flow)
                except Exception:
                    max_flows.append(0)  # fallback if no path exists

    if not max_flows:
        return 0

    if type == "max":
        return np.max(max_flows)
    elif type == "mean":
        return np.mean(max_flows)
    elif type == "min":
        return np.min(max_flows)
    else:
        raise ValueError("Invalid type. Use 'mean', 'max', or 'min'.")
        