import random

def ratio_weighted_random(ratio):
    """
    @brief Decide randomly whether to fail a node or an edge, based on edge-to-node ratio.

    Given an edge-to-node failure ratio (e.g., 2.0 = 2 edges per 1 node),
    this function uses weighted probability to determine whether the next
    failure should be a node or an edge.

    @param ratio The edge-to-node failure ratio (e.g., 2.0 = fail 2 edges per 1 node).
    @return "node" or "edge", depending on the random draw and ratio.
    """

    # Total parts = edge weight + node weight (node is always weight 1)
    total_parts = ratio + 1

    # Probability that the next failure should be a node
    node_threshold = 1 / total_parts

    # Generate a random float between 0.00 and 0.99
    rand_value = random.uniform(0.00, 0.99)

    # Compare the random value to the node threshold
    return "node" if rand_value < node_threshold else "edge"