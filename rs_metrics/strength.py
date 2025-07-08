import numpy as np

def calculate_strength(graph, mode, type=None, weight="distance", **kwargss):
    """
    Calculate the strength of all nodes

    Definition:
    For a node v, the strength is defined as:
    Strength(v) = ∑(v, u)∈E w(v, u)
    - E: Set of edges in the graph.
    - w(v, u): Weight of the edge between nodes v and u.
    """
    strength = graph.strength(weights=weight)

    if mode == "rs_value":

        if type == "max":
            return np.max(strength)
        elif type == "mean":
            return np.mean(strength)
        elif type == "min":
            return np.min(strength)
    
    elif mode == "targeted":
        failing_nodes = True
        failing_edges = False
        ranking = sorted(range(len(strength)),
                         key=lambda x: strength[x],
                         reverse = True)
        return ranking, failing_nodes, failing_edges