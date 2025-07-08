from .random_component_ratio import ratio_weighted_random

def generate_random_node_and_edge_fail_scenarios(node_idx, edge_idx, num_scenarios, fail_percent, ratio, R):
    """
    @brief Generate random node and edge failure scenarios based on a link-per-node failure ratio.

    This function creates failure scenarios where both nodes and edges fail progressively.
    In each failure step, a fixed number of components (nodes and/or edges) are removed
    according to a defined link-per-node ratio. For example, a ratio of 2 means that
    for every failed node, two edges should also fail.

    @param node_idx List of node indices in the graph.
    @param edge_idx List of edge indices in the graph.
    @param num_scenarios Number of failure scenarios to generate.
    @param fail_percent List of cumulative failure percentages (e.g., [10, 20, 30]).
                        Percentages refer to the total number of components (nodes + edges).
    @param ratio The edge-to-node failure ratio (e.g., 2.0 means 2 edges fail per node).
    @param R An instance of random.Random for reproducibility.

    @return A list of scenarios. Each scenario is a list of cumulative failure steps,
            and each step is a list of ("node", node_id) or ("edge", edge_id) tuples.
    """

    FAIL_SCENE_ALL = []  # Stores all generated scenarios
    all_nodes = list(node_idx)
    all_edges = list(edge_idx)

    N_vs = len(all_nodes)
    N_es = len(all_edges)
    N = N_vs + N_es  # Total components

    # Calculate incremental failure steps (as percentages)
    step_sizes = [fail_percent[0]] + [j - i for i, j in zip(fail_percent[:-1], fail_percent[1:])]

    # Convert step percentages into number of total components to fail per step
    batch_sizes = [max(1, int(N * (step / 100))) for step in step_sizes]

    for i in range(num_scenarios):
        failure_scenario = [[]]  # Start with no failed components
        remaining_nodes = all_nodes.copy()
        remaining_edges = all_edges.copy()

        for batch_size in batch_sizes:
            batch = []

            # Randomly choose components (nodes/edges) to fail, honoring the link-per-node ratio
            for _ in range(batch_size):
                if remaining_nodes and remaining_edges:
                    # Decide whether to fail a node or an edge, using the link-per-node ratio
                    if ratio_weighted_random(ratio) == "node":
                        node = R.choice(remaining_nodes)
                        batch.append(("node", node))
                        remaining_nodes.remove(node)
                    else:
                        edge = R.choice(remaining_edges)
                        batch.append(("edge", edge))
                        remaining_edges.remove(edge)

                elif remaining_edges:
                    edge = R.choice(remaining_edges)
                    batch.append(("edge", edge))
                    remaining_edges.remove(edge)

                elif remaining_nodes:
                    node = R.choice(remaining_nodes)
                    batch.append(("node", node))
                    remaining_nodes.remove(node)

            # Append cumulative list of failures for this step
            failure_scenario.append(failure_scenario[-1] + batch)

        FAIL_SCENE_ALL.append(failure_scenario)

    return FAIL_SCENE_ALL
       