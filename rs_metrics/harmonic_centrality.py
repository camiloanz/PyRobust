import numpy as np

def calculate_harmonic(graph, mode, type=None, **kwargs):
    """
    @brief Computes harmonic centrality-based metrics.

    Harmonic centrality is defined as the sum of the reciprocal shortest-path distances
    from a given node to all others. It is well-defined even in disconnected graphs.
    This function supports both aggregated robustness scores and targeted ranking.

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: "rs_value" or "targeted".
    @param type (Optional, for rs_value) Aggregation method: "mean", "max", or "min".
    @param kwargs Optional keyword arguments (ignored).

    @return
        - If mode == "rs_value": A float representing the aggregated harmonic centrality.
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False),
          where ranking is a list of node indices sorted by descending harmonic centrality.
    """

    harmonic_centrality = graph.harmonic_centrality()

    if mode == "rs_value":
        if type == "max":
            return np.max(harmonic_centrality)
        elif type == "mean":
            return np.mean(harmonic_centrality)
        elif type == "min":
            return np.min(harmonic_centrality)
        else:
            raise ValueError("Invalid type. Use 'mean', 'max', or 'min'.")

    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False

        ranking = sorted(
            range(len(harmonic_centrality)),
            key=lambda x: harmonic_centrality[x],
            reverse=True
        )

        return ranking, failing_nodes, failing_edges

    else:
        raise NotImplementedError("Unsupported mode. Use 'rs_value' or 'targeted'.")