import math
import numpy as np

def calculate_closeness(graph, mode, type=None, **kwargs):
    """
    @brief Computes closeness centrality-based metrics.

    This function evaluates node closeness centrality either as an aggregated robustness metric
    or as a vulnerability ranking for targeted node failure.

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: "rs_value" or "targeted".
    @param type (Optional, for rs_value) Aggregation type: "mean", "max", or "min".
    @param kwargs Optional keyword arguments (not used but accepted for compatibility).

    @return
        - If mode == "rs_value": A float (aggregated closeness value).
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False),
          where ranking is a list of node indices sorted by descending closeness.
    """

    # Compute node closeness centrality (unweighted)
    closeness = graph.closeness()

    # Handle NaNs (e.g., disconnected/isolated nodes)
    closeness = [0 if math.isnan(c) else c for c in closeness]

    if mode == "rs_value":
        if type == "max":
            return np.max(closeness)
        elif type == "mean":
            return np.mean(closeness)
        elif type == "min":
            return np.min(closeness)
        else:
            raise ValueError("Unknown type. Use 'mean', 'max', or 'min'.")

    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False

        # Rank nodes by closeness (higher closeness = more central = more critical)
        ranking = sorted(
            range(len(closeness)),
            key=lambda x: closeness[x],
            reverse=True
        )

        return ranking, failing_nodes, failing_edges