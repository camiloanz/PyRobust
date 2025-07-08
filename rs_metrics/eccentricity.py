import numpy as np

import numpy as np

def calculate_eccentricity(graph, mode, type=None, **kwargs):
    """
    @brief Computes node eccentricity-based metrics.

    Eccentricity is the greatest shortest path distance from a node to any other node.
    This function supports two modes:
    - "rs_value": Returns an aggregate value across all nodes (mean, max, or min).
    - "targeted": Returns a ranking of nodes with highest eccentricity first.

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: "rs_value" or "targeted".
    @param type (Optional, for rs_value) Aggregation method: "mean", "max", or "min".
    @param kwargs Optional keyword arguments (not used here).

    @return
        - If mode == "rs_value": A float representing the aggregate eccentricity.
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False),
          where ranking is a list of node indices sorted by descending eccentricity.
    """

    eccentricities = graph.eccentricity()

    if mode == "rs_value":
        if type == "max":
            return np.max(eccentricities)
        elif type == "mean":
            return np.mean(eccentricities)
        elif type == "min":
            return np.min(eccentricities)
        else:
            raise ValueError("Invalid type. Use 'mean', 'max', or 'min'.")

    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False

        # Sort nodes by eccentricity (higher = more peripheral)
        ranking = sorted(
            range(len(eccentricities)),
            key=lambda x: eccentricities[x],
            reverse=True
        )

        return ranking, failing_nodes, failing_edges

    else:
        raise NotImplementedError("Unsupported mode. Use 'rs_value' or 'targeted'.")