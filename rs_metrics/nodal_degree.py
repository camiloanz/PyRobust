import numpy as np
import random

def calculate_nodal_degree(graph, mode, type=None, **kwargs):
    """
    @brief Computes node degree-based metrics.

    This function evaluates nodal degree centrality (i.e., number of incident edges).
    It supports both:
    - Aggregated scoring ("rs_value"), and
    - Targeted node ranking for attack simulations ("targeted").

    @param graph The igraph.Graph object to analyze.
    @param mode Operation mode: "rs_value" or "targeted".
    @param type (Optional, for rs_value) Aggregation method: "mean", "max", or "min".
    @param kwargs Optional keyword arguments (unused).

    @return
        - If mode == "rs_value": A float summarizing degree values across the graph.
        - If mode == "targeted": Tuple (ranking, failing_nodes=True, failing_edges=False),
          where ranking is a list of node indices sorted by descending degree.
    """

    degrees = graph.degree()

    if mode == "rs_value":
        if type == "max":
            return np.max(degrees)
        elif type == "mean":
            return np.mean(degrees)
        elif type == "min":
            return np.min(degrees)
        else:
            raise ValueError("Invalid type. Use 'mean', 'max', or 'min'.")

    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False

        # Random tie-breaker to avoid deterministic bias on equal degrees
        ranking = sorted(
            range(len(degrees)),
            key=lambda x: (degrees[x], random.random()),
            reverse=True
        )

        return ranking, failing_nodes, failing_edges

    else:
        raise NotImplementedError("Unsupported mode. Use 'rs_value' or 'targeted'.")