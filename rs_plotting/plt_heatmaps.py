import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_heatmaps(matrix, fail_percent, metric, failing_type, fail_str):
    """
    @brief Plot a heatmap for visualizing metric degradation under failure scenarios.

    This function creates a heatmap where each row corresponds to a failure percentage
    and each column represents a scenario. The color intensity reflects the metric value,
    showing how robustness changes with increasing failure severity.

    @param matrix 2D NumPy array of shape [num_levels x num_scenarios], preprocessed
                  (e.g., sorted and vertically reversed) metric values.
    @param fail_percent List of failure percentages (excluding 0%), e.g., [10, 20, 30, ...].
    @param metric String name of the metric being visualized (e.g., "connectivity").
    @param failing_type Type of failure mechanism (e.g., "random", "epidemic").
    @param fail_str A description of the failed components ("node", "edge", "node and edge").
    """

    # Create heatmap figure
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        matrix,
        annot=False,            # Set to True to show exact values
        fmt=".2f",
        cmap="viridis_r",       # Reversed viridis colormap
        linewidths=0.5
    )

    # Create y-axis labels in reverse order (from 0% at bottom to highest on top)
    y_axis_labels = ['0%'] + [f'{p}%' for p in fail_percent]
    y_axis_labels = y_axis_labels[::-1]

    plt.yticks(
        ticks=np.arange(len(y_axis_labels)) + 0.5,  # Align ticks to heatmap cells
        labels=y_axis_labels,
        rotation=0
    )

    # Hide x-ticks (optional)
    plt.xticks([])

    # Label axes
    plt.xlabel("Failure Scenarios", fontsize=14)
    plt.ylabel("Percentage of Failures", fontsize=14)

    # Optional: Uncomment to include a title
    # plt.title(f"{metric} under {failing_type} {fail_str} failures", fontsize=16)