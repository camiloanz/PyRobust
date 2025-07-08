def calculate_rLCC(graph, mode, num_nodes, **kwargs):
    """
    @brief Computes the relative size of the Largest Connected Component (rLCC).

    rLCC is defined as the size of the largest connected component divided by the 
    total number of original nodes. It is a common robustness indicator under node/edge failures.

    @param graph The igraph.Graph to analyze.
    @param mode Operation mode. Only "rs_value" is currently supported.
    @param num_nodes The number of nodes in the original (unperturbed) graph.
    @param kwargs Additional keyword arguments (ignored here).

    @return A float value representing the rLCC (between 0 and 1).
    """

    if mode != "rs_value":
        raise NotImplementedError("rLCC supports only 'rs_value' mode.")


    largest_component_size = max(graph.connected_components().sizes(), default=0)
    return largest_component_size / num_nodes