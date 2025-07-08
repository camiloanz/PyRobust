from rs_metrics import rs_metric

def generate_targeted_fail_scenario(graph, mode, metric, fail_percentage, graph_weight, graph_capacity):
    """
    @brief Generate a targeted failure scenario based on metric rankings.

    This function simulates a sequence of node or edge failures by ranking components
    using a vulnerability metric (e.g., degree, betweenness). Failures occur in a
    stepwise fashion according to the given failure percentages. In "dynamic" mode,
    the graph is updated and re-ranked after each failure step.

    @param graph The input igraph.Graph to simulate failures on (will be copied internally).
    @param mode Failure mode: either "static" (rank once) or "dynamic" (re-rank after each step).
    @param metric The name of the vulnerability metric to use (e.g., "degree").
    @param fail_percentage List of percentages specifying cumulative failure levels.
    @param graph_weight Name of the edge weight attribute (e.g., "distance").
    @param graph_capacity Name of the edge capacity attribute (used for flow-based metrics).

    @return Tuple:
        - A list containing one scenario: each element is the cumulative set of failed component IDs (or names for dynamic).
        - A boolean indicating whether nodes are being failed.
        - A boolean indicating whether edges are being failed.
    """

    FAIL_SCENE_ALL = []                 # List of all scenarios (only one is generated here)
    failure_scenario = [[]]            # Start with no failures
    active_graph = graph.copy()        # Work on a copy to avoid modifying original

    # Compute initial metric-based vulnerability ranking
    vulnerability_rankings, fail_nodes, fail_edges = rs_metric.compute_metric(
        graph=active_graph,
        metric=metric,
        mode="targeted",
        weight=graph_weight,
        capacity=graph_capacity
    )

    # Calculate batch sizes from percentage steps
    step_sizes = [fail_percentage[0]] + [j - i for i, j in zip(fail_percentage[:-1], fail_percentage[1:])]
    batch_sizes = [max(1, int(len(vulnerability_rankings) * (step / 100))) for step in step_sizes]

    for batch_size in batch_sizes:
        batch = []

        if mode == "dynamic":
            # Recompute after each failure batch
            for _ in range(batch_size):
                if vulnerability_rankings:
                    idx = vulnerability_rankings.pop(0)  # Most vulnerable component

                    # Remove from graph and track by name (because indices change!)
                    if fail_nodes:
                        name_tag = active_graph.vs[idx]["name"]
                        active_graph.delete_vertices(idx)
                    elif fail_edges:
                        name_tag = active_graph.es[idx]["name"]
                        active_graph.delete_edges(idx)

                    batch.append(name_tag)

            # Append cumulative failures
            failure_scenario.append(failure_scenario[-1] + batch)

            # Recompute vulnerability rankings after graph update
            vulnerability_rankings, fail_nodes, fail_edges = rs_metric.compute_metric(
                graph=active_graph,
                metric=metric,
                mode="targeted",
                weight=graph_weight,
                capacity=graph_capacity
            )

        else:  # Static ranking
            for _ in range(batch_size):
                if vulnerability_rankings:
                    idx = vulnerability_rankings.pop(0)
                    batch.append(idx)

            # Append cumulative failures
            failure_scenario.append(failure_scenario[-1] + batch)

    FAIL_SCENE_ALL.append(failure_scenario)

    return FAIL_SCENE_ALL, fail_nodes, fail_edges