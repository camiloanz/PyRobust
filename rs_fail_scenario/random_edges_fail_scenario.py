def generate_random_edge_fail_scenarios(edge_idx, num_scenarios, fail_percent, R):
    """
    @brief Generate random link (edge) failure scenarios for robustness testing.

    This function creates multiple edge failure scenarios where, in each step,
    a percentage of the remaining edges are randomly selected and removed.

    @param edge_idx List of edge indices from the input graph.
    @param num_scenarios Number of failure scenarios to generate.
    @param fail_percent List of failure percentages (e.g., [10, 20, 30]) to define each step.
    @param R An instance of random.Random with a fixed seed, used for reproducibility.

    @return A list of scenarios, each being a list of cumulative failure steps.
            Each scenario[i][j] gives the list of failed edges after step j.
    """
    
    FAIL_SCENE_ALL = []  # Stores all generated failure scenarios
    all_edges = list(edge_idx)  # Convert edge indices to list for manipulation
    N_es = len(all_edges)  # Total number of edges in the graph

    # Compute incremental failure percentages (step sizes)
    step_sizes = [fail_percent[0]] + [j - i for i, j in zip(fail_percent[:-1], fail_percent[1:])]

    # Convert percentage steps to actual edge counts (minimum of 1 per step)
    batch_sizes = [max(1, int(N_es * (step / 100))) for step in step_sizes]

    # Generate multiple random failure scenarios
    for i in range(num_scenarios):
        failure_scenario = [[]]  # Initial empty failure state
        remaining_edges = all_edges.copy()  # Track which edges can still fail

        # Simulate progressive failure across percentage steps
        for batch_size in batch_sizes:
            batch = []

            # Randomly select 'batch_size' edges to fail at this step
            for _ in range(batch_size):
                if remaining_edges:
                    edge = R.choice(remaining_edges)
                    batch.append(edge)
                    remaining_edges.remove(edge)

            # Append cumulative failure list up to this step
            failure_scenario.append(failure_scenario[-1] + batch)

        # Store the complete scenario
        FAIL_SCENE_ALL.append(failure_scenario)

    return FAIL_SCENE_ALL