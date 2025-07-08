def calculate_avg_path_length(graph, mode, **kwargs):
    """
    @brief Calculates the average weighted shortest path length.

    This function supports two modes:
    - "rs_value": Computes the overall average shortest path length using the edge weights.
    - "targeted": Computes per-node average weighted shortest paths and ranks nodes
                  by their average (lower = more central/vulnerable).

    @param graph The igraph.Graph object to analyze. Must have 'graph_weights' as attribute.
    @param mode Operation mode: "rs_value" or "targeted".
    @param kwargs Optional keyword arguments (unused, but accepted for compatibility).

    @return
        - If mode == "rs_value": A float, average weighted path length or 0 if the graph is empty.
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False),
          where ranking is a list of node indices sorted by average path length (ascending).
    """

    if mode == "rs_value":
        return graph.average_path_length(weights=graph.graph_weights) if graph.ecount() > 0 else 0

    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False

        # Compute all-pairs shortest paths using Dijkstra (weighted)
        shortest_paths = graph.shortest_paths_dijkstra(weights=graph.graph_weights)

        # Compute average shortest path per node
        avg_shortest_paths = {
            node: sum(paths) / (len(paths) - 1) if len(paths) > 1 else float("inf")
            for node, paths in enumerate(shortest_paths)
        }

        # Rank nodes by lowest average path length (most central = lowest)
        ranking = sorted(
            range(len(avg_shortest_paths)),
            key=lambda x: avg_shortest_paths[x],
            reverse=False
        )

        return ranking, failing_nodes, failing_edges