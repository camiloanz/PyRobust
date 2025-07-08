def calculate_connectivity(graph, mode, num_nodes, **kwargs):
    """
    @brief Computes the proportion of node pairs that are connected.

    This function evaluates how well-connected the graph is by comparing the number
    of node pairs that lie within the same connected component to the number of all
    possible node pairs in a fully connected graph.

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: only "rs_value" is supported.
    @param num_nodes Total number of nodes in the original (unfailed) graph.
    @param kwargs Optional keyword arguments (ignored).

    @return A float between 0 and 1 indicating the fraction of connected node pairs.
    """

    if mode == "rs_value":
        # Get connected components (clusters)
        clusters = graph.clusters()

        # Total number of node pairs in a fully connected graph: n choose 2
        total_pairs = num_nodes * (num_nodes - 1) / 2

        # Sum of connected node pairs within each cluster
        connected_pairs = sum((size * (size - 1)) / 2 for size in clusters.sizes())

        return (connected_pairs / total_pairs) if total_pairs > 0 else 0

    else:
        raise NotImplementedError("Only 'rs_value' mode is supported for connectivity.")