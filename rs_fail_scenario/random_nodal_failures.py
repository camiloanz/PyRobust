
def generate_random_node_fail_scenarios(node_idx, num_scenarios, fail_percent, R):
    """Generate random nodal failure scenarios for robustness testing."""
    
    FAIL_SCENE_ALL = []
    all_nodes = list(node_idx)
    N_vs = len(all_nodes)
    
    # Calculate the incremental differences (step sizes) from the fail_percent list
    step_sizes = [fail_percent[0]] + [j - i for i, j in zip(fail_percent[:-1], fail_percent[1:])]
    # Convert each incremental percentage into the actual number of nodes that fail at each step
    batch_sizes = [max(1, int(N_vs * (step / 100))) for step in step_sizes]

    for i in range(num_scenarios):  # Create # failure scenarios
        failure_scenario = [[]]  
        remaining_nodes = all_nodes.copy()
        #print(f"Starting scenario {i}, remaining nodes: {remaining_nodes}")

        for batch_size in batch_sizes: 
            batch = []
            for _ in range(batch_size):
                if remaining_nodes:
                    node = R.choice(remaining_nodes)  # Randomly pick a node
                    batch.append(node)
                    remaining_nodes.remove(node)  
            # Add the current failed nodes to the scenario
            failure_scenario.append(failure_scenario[-1] + batch)
            #print(f"Step {j}, batch selected: {batch}")

        FAIL_SCENE_ALL.append(failure_scenario)
    return FAIL_SCENE_ALL
    #print(f"Generated failure scenario {i}: {failure_scenario}")
    #print(failure_scenario)

    #for i, failure_scenario in enumerate(self.FAIL_SCENE_ALL):
            #print(f"Final failure scenario {i}: {failure_scenario}")
    