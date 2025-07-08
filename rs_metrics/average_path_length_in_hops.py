import numpy as np

def calculate_avg_path_length_hops(graph, mode, **kwargs):
    """
    @brief Calculates the average shortest path length in hops (unweighted).

    This function operates in two modes:
    - "rs_values": Computes the overall average shortest path length of the entire graph.
    - "targeted": Computes per-node average shortest path lengths and ranks nodes based on centrality
                  (lower values indicate higher centrality / vulnerability).

    @param graph The igraph.Graph to analyze.
    @param mode Operation mode: "rs_values" or "targeted".
    @param kwargs Additional arguments (not used here, kept for interface consistency).

    @return
        - If mode == "rs_values": A float (average path length or 0 if graph is disconnected).
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False)
          where ranking is a list of node indices sorted by average path length (ascending).
    """

    if mode == "rs_values":
        return graph.average_path_length() if graph.ecount() > 0 else 0

    elif mode == "targeted":
        # Targeted attack: rank nodes by average shortest path (unweighted)
        failing_nodes = True
        failing_edges = False

        # Compute all-pairs shortest paths (hop-based)
        shortest_paths = np.array(graph.shortest_paths(), dtype=float)
        n = shortest_paths.shape[0]
        avg_paths = {}

        for node_id in range(n):
            paths = shortest_paths[node_id]
            reachable = (np.isfinite(paths)) & (paths != 0)
            if reachable.any():
                avg = paths[reachable].mean()
            else:
                avg = float("inf")
            avg_paths[node_id] = avg

        # Sort node indices by average shortest path (ascending)
        ranking = sorted(
            range(len(avg_paths)),
            key=lambda x: avg_paths[x],
            reverse=False
        )

        return ranking, failing_nodes, failing_edges