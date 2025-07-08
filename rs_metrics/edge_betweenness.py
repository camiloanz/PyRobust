import numpy as np

def calculate_edge_betweenness(graph, mode, type=None, **kwargs):
    """
    @brief Computes edge betweenness centrality-based metrics.

    Edge betweenness measures how often an edge lies on the shortest paths between pairs of nodes.
    This function supports both scalar metric extraction and targeted failure ranking.

    @param graph The igraph.Graph to analyze.
    @param mode Operation mode: "rs_value" (scalar) or "targeted" (ranking).
    @param type (Optional, for rs_value) Aggregation method: "mean", "max", or "min".
    @param kwargs Additional keyword arguments (not used here).

    @return
        - If mode == "rs_value": A float (aggregated edge betweenness value).
        - If mode == "targeted": Tuple (ranking, failing_nodes=False, failing_edges=True),
          where ranking is a list of edge indices sorted by descending betweenness.
    """

    if mode == "rs_value":
        if graph.ecount() > 0:
            edge_betweenness = graph.edge_betweenness()

            if type == "max":
                return np.max(edge_betweenness)
            elif type == "mean":
                return np.mean(edge_betweenness)
            elif type == "min":
                return np.min(edge_betweenness)
            else:
                raise ValueError("Invalid type. Use 'mean', 'max', or 'min'.")
        else:
            return 0

    elif mode == "targeted":
        failing_nodes = False
        failing_edges = True

        edge_betweenness = graph.edge_betweenness()

        ranking = sorted(
            range(len(edge_betweenness)),
            key=lambda x: edge_betweenness[x],
            reverse=True
        )

        return ranking, failing_nodes, failing_edges

    else:
        raise NotImplementedError("Unsupported mode. Use 'rs_value' or 'targeted'.")
