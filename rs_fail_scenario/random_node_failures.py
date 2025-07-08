
def generate_random_node_fail_scenarios(node_idx, num_scenarios, fail_percent, R):
    """
    @brief Generate random nodal failure scenarios for robustness testing.

    This function creates multiple node failure scenarios where, in each step,
    a percentage of the remaining nodes are randomly selected and marked as failed.

    @param node_idx List of node indices from the input graph.
    @param num_scenarios Number of failure scenarios to generate.
    @param fail_percent List of failure percentages (e.g., [10, 20, 30]) to define each step.
    @param R An instance of random.Random with a fixed seed, used for reproducibility.

    @return A list of scenarios, each being a list of cumulative failure steps.
            Each scenario[i][j] gives the list of failed nodes after step j.
    """
    
    FAIL_SCENE_ALL = []  # This will store all generated failure scenarios
    all_nodes = list(node_idx)  # Convert node indices to list for manipulation
    N_vs = len(all_nodes)  # Total number of nodes in the graph

    # Compute how many nodes should fail at each step (batch sizes)
    # Step sizes represent incremental failure percentages between each level
    step_sizes = [fail_percent[0]] + [j - i for i, j in zip(fail_percent[:-1], fail_percent[1:])]
    
    # Convert each percentage step into an absolute number of nodes (minimum 1)
    batch_sizes = [max(1, int(N_vs * (step / 100))) for step in step_sizes]

    # Generate multiple random failure scenarios
    for i in range(num_scenarios):
        failure_scenario = [[]]  # Start with no failed nodes
        remaining_nodes = all_nodes.copy()  # Nodes that can still fail in this scenario

        # Simulate progressive failure across defined percentages
        for batch_size in batch_sizes:
            batch = []

            # Randomly select 'batch_size' nodes to fail at this step
            for _ in range(batch_size):
                if remaining_nodes:
                    node = R.choice(remaining_nodes)
                    batch.append(node)
                    remaining_nodes.remove(node)

            # Add this batch to the cumulative failure list
            failure_scenario.append(failure_scenario[-1] + batch)

        # Store the complete scenario (list of steps with cumulative node failures)
        FAIL_SCENE_ALL.append(failure_scenario)

    return FAIL_SCENE_ALL