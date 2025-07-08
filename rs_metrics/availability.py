
from rs_metrics.availability_evaluation.availability_evaluation import *
import numpy as np
import networkx as nx

def calculate_availability(graph, mode, A_dic, num_nodes, **kwargs):
    """
    @brief Compute the availability of a graph based on node availability values.

    This function converts an igraph.Graph into a NetworkX graph, sets up node availability values,
    and calculates overall network availability using a parallelized C++ backend.

    @param graph The igraph.Graph object representing the current state of the network.
    @param mode The evaluation mode. Only "rs_value" is currently supported.
    @param A_dic Dictionary of node availability values
    @param num_nodes Total number of nodes (used for normalization).
    @param kwargs Optional keyword arguments (currently unused, but kept for compatibility).

    @return A float between 0 and 1 representing average node availability,
            or 0 if no availability could be computed.
    """

    if mode == "rs_value":
        # Convert igraph to NetworkX for compatibility with the availability evaluator
        A = {}
        g_nx = nx.Graph()
        g_nx.add_nodes_from(graph.vs["name"])
        g_nx.add_edges_from([
            (graph.vs[e.source]["name"], graph.vs[e.target]["name"]) for e in graph.es
        ])

        


        # Filter availability dictionary to match current graph nodes
        A_dic_filtered = {v["name"]: A_dic.get(v["name"], 0.0) for v in graph.vs}
        

        # Call the multithreaded availability evaluator (likely in C++ backend)
        results = calculate_availability_multithreading_cpp(g_nx, A_dic_filtered)

        if results == []:
            return 0

        # Extract availability values from result
        availabilities = np.array([a for _, _, a in results])

        # Normalize by number of nodes
        return np.sum(availabilities) / num_nodes
        