
def generate_epidemic_node_fail_scenarios(graph, num_scenarios, fail_percent, R):
    """
    @brief Generate epidemic-style node failure scenarios for robustness testing.

    This function simulates node failures that spread in an epidemic-like fashion.
    Starting from a random node, the failure propagates by repeatedly selecting
    the node with the highest number of failed neighbors (or ties randomly),
    mimicking local spread.

    @param graph The igraph.Graph on which to simulate the failures.
    @param num_scenarios Number of failure scenarios to generate.
    @param fail_percent List of cumulative failure percentages for each step.
    @param R An instance of random.Random for reproducible node selection.

    @return A list of scenarios. Each scenario is a list of failure steps,
            where each step contains the cumulative list of failed node indices.
    """

    FAIL_SCENE_ALL = []
    N_vs = len(graph.vs)

    # Precompute neighbors for all nodes
    neighbors = {v.index: graph.neighbors(v.index) for v in graph.vs}

    # Initialize failure score for each node (how many failed neighbors it has)
    neighbor_value = {v.index: 0 for v in graph.vs}

    # Determine failure batch sizes for each percentage step
    step_sizes = [fail_percent[0]] + [j - i for i, j in zip(fail_percent[:-1], fail_percent[1:])]
    batch_sizes = [max(1, int(N_vs * (step / 100))) for step in step_sizes]

    for _ in range(num_scenarios):
        failure_scenario = [[]]

        # Start with a random initial node
        node = R.choice(range(N_vs))

        for batch_size in batch_sizes:
            batch = []

            for _ in range(batch_size):
                # Mark node as failed
                neighbor_value[node] = -1  # Mark as removed
                batch.append(node)

                # Increase neighbor scores of neighbors
                for neighbor in neighbors[node]:
                    if neighbor_value[neighbor] != -1:      #skip removed nodes
                        neighbor_value[neighbor] += 1

                # Choose next node: one with max neighbor score (ties broken randomly)
                valid_nodes = [k for k, v in neighbor_value.items() if v != -1]
                if valid_nodes:
                    max_val = max(neighbor_value[n] for n in valid_nodes)
                    max_neighbors = [n for n in valid_nodes if neighbor_value[n] == max_val]
                    node = R.choice(max_neighbors)
                else:
                    break  # All nodes failed

            # Add cumulative batch to scenario
            failure_scenario.append(failure_scenario[-1] + batch)

        FAIL_SCENE_ALL.append(failure_scenario)

    return FAIL_SCENE_ALL