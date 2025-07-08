from rs_metrics import rs_metric

def fail_edges(graph, fail_scenarios, metrics, metric_matrices, graph_weight, graph_capacity, A_dic):
    """
    @brief Apply edge failure scenarios and compute robustness metrics at each step.

    For each scenario and failure percentage, this function removes the specified edges
    from a copy of the input graph and computes the specified robustness metrics.

    @param graph The original igraph.Graph object to be copied and modified.
    @param fail_scenarios A list of failure scenarios (each a list of cumulative edge name lists).
    @param metrics A list of metric names or (metric, mode) tuples to compute.
    @param metric_matrices A dict mapping metric names to 2D result arrays (scenario x step).
    @param graph_weight Name of the edge weight attribute (used in metric computation).
    @param graph_capacity Name of the edge capacity attribute (used in flow-based metrics).
    @param A_dic Optional additional parameter dictionary, passed to the metric functions.

    @return None (results are written into metric_matrices in-place).
    """

    for i, scenario in enumerate(fail_scenarios):
        # Create a copy of the graph for this scenario
        active_graph = graph.copy()

        # Compute metrics at 0% failure (baseline)
        for metric in metrics:
            metric_matrices[metric][i, 0] = rs_metric.compute_metric(
                active_graph,
                metric,
                mode="rs_value",
                weight=graph_weight,
                capacity=graph_capacity,
                A_dic=A_dic,
                num_nodes=graph.vcount()
            )

        # Iterate over failure steps (skip initial empty state)
        for j, cumulative_failed_edges in enumerate(scenario[1:], start=1):

            try:
                # Edges are referred to by their "name" attribute
                existing_edges = list(active_graph.es['name'])
                valid_edges_to_delete = [
                    edge for edge in cumulative_failed_edges if edge in existing_edges
                ]

                # Convert names to igraph edge indices and delete them
                if valid_edges_to_delete:
                    ids_to_delete = [
                        active_graph.es.find(name=edge).index
                        for edge in valid_edges_to_delete
                    ]
                    active_graph.delete_edges(ids_to_delete)

            except Exception as e:
                print(f"Error deleting edges in scenario {i}, percentage step {j}: {e}")
                print(active_graph.es.attributes())  # Optional: helps with debugging

            # Compute metrics after current failure step
            for metric in metrics:
                metric_matrices[metric][i, j] = rs_metric.compute_metric(
                    active_graph,
                    metric,
                    mode="rs_value",
                    weight=graph_weight,
                    capacity=graph_capacity,
                    A_dic=A_dic,
                    num_nodes=graph.vcount()
                )