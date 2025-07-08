from rs_metrics import rs_metric

def fail_nodes_and_edges(graph, fail_scenarios, metrics, metric_matrices, graph_weight, graph_capacity, A_dic):
    """
    @brief Apply node and edge failure scenarios and compute robustness metrics at each step.

    This function handles combined node and edge failures. For each scenario and percentage step,
    it removes the specified nodes and edges (based on their "name" attribute) from a copy of the input graph,
    and computes the specified metrics.

    @param graph The original igraph.Graph object to be copied and modified.
    @param fail_scenarios A list of failure scenarios. Each scenario is a list of steps,
                          and each step is a list of ("node" or "edge", name) tuples.
    @param metrics A list of metric names or (metric, mode) tuples to compute.
    @param metric_matrices A dict mapping metric names to 2D result arrays (scenario x step).
    @param graph_weight Name of the edge weight attribute (used in metric computation).
    @param graph_capacity Name of the edge capacity attribute (used in flow-based metrics).
    @param A_dic Optional dictionary of additional arguments passed to metric functions.

    @return None (results are written into metric_matrices in-place).
    """

    for i, scenario in enumerate(fail_scenarios):
        # Create a fresh copy of the graph for this scenario
        active_graph = graph.copy()

        # Compute baseline (0% failure) metric values
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

        # Iterate through failure percentage steps (skip initial state)
        for j, cumulative_failures in enumerate(scenario[1:], start=1):
            try:
                existing_nodes = list(active_graph.vs['name'])
                existing_edges = list(active_graph.es['name'])

                valid_nodes_to_delete = []
                valid_edges_to_delete = []

                # Separate valid edge and node deletions
                for fail in cumulative_failures:
                    typ, name = fail
                    if typ == "edge" and name in existing_edges:
                        valid_edges_to_delete.append(name)
                    elif typ == "node" and name in existing_nodes:
                        valid_nodes_to_delete.append(name)

                # Delete edges first to avoid referencing broken topology
                if valid_edges_to_delete:
                    edge_ids = [
                        active_graph.es.find(name=edge_name).index
                        for edge_name in valid_edges_to_delete
                    ]
                    active_graph.delete_edges(edge_ids)

                # Delete nodes next
                if valid_nodes_to_delete:
                    node_ids = [
                        active_graph.vs.find(name=node_name).index
                        for node_name in valid_nodes_to_delete
                    ]
                    active_graph.delete_vertices(node_ids)

            except Exception as e:
                print(f"Error deleting nodes/edges in scenario {i}, step {j}: {e}")

            # Compute metrics after this failure step
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