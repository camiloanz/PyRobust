
def calculate_diameter(graph, mode, weights, **kwargs):
    """
    @brief Computes the graph diameter (longest shortest path between any pair of nodes).

    The diameter is calculated using igraph's built-in function. It can handle disconnected graphs
    by setting `unconn=True`, which returns the longest shortest path among reachable pairs.

    @param graph The igraph.Graph to analyze.
    @param mode Operation mode: only "rs_value" is supported.
    @param weights Edge weights to use for path calculation, or None for unweighted.
    @param kwargs Optional keyword arguments (unused, kept for compatibility).

    @return A float representing the diameter, or 0 if the graph has no edges.
    """

    if mode == "rs_value":
        return graph.diameter(unconn=True, weights=weights) if graph.ecount() > 0 else 0
    else:
        raise NotImplementedError("Only 'rs_value' mode is supported for diameter.")