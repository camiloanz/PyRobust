import numpy as np

def calculate_betweenness(graph, mode, type=None, **kwargs):
    """
    @brief Computes betweenness centrality-based metrics.

    This function calculates node betweenness centrality in two modes:
    - "rs_value": Returns a scalar value (max, mean, or min) over all nodes.
    - "targeted": Returns a ranking of nodes sorted by descending betweenness
                  to simulate targeted attacks.

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: "rs_value" or "targeted".
    @param type (Optional, for rs_value) Selects aggregation: "mean", "max", or "min".
    @param kwargs Optional keyword arguments (unused, reserved for interface compatibility).

    @return
        - If mode == "rs_value": A float value depending on the aggregation type.
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False),
          where ranking is a list of node indices sorted by descending betweenness.
    """

    if mode == "rs_value":
        if graph.ecount() > 0:
            betweenness = graph.betweenness()
            if type == "max":
                return np.max(betweenness)
            elif type == "mean":
                return np.mean(betweenness)
            elif type == "min":
                return np.min(betweenness)
        else:
            return 0

    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False

        # Calculate node betweenness centrality
        betweenness = graph.betweenness()

        # Sort nodes descending by betweenness (higher = more critical)
        ranking = sorted(
            range(len(betweenness)),
            key=lambda x: betweenness[x],
            reverse=True
        )

        return ranking, failing_nodes, failing_edges