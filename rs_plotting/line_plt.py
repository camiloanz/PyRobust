import matplotlib.pyplot as plt
import numpy as np

def generate_additional_line_plot(metric, matrix, fail_percent, failing_type, fail_str):
    """
    @brief Generate a line plot with error bars for a robustness metric.

    This function visualizes how a given robustness metric evolves under increasing 
    failure rates. It plots the mean metric value over all scenarios and includes 
    error bars showing the standard deviation.

    @param metric The name of the metric to plot (used as y-axis label).
    @param matrix 2D NumPy array (num_scenarios x num_failure_steps) with computed values.
    @param fail_percent List of failure percentages (excluding 0%).
    @param failing_type A string describing the type of failure ("random", "targeted", etc.).
    @param fail_str Human-readable description of failed components ("node", "edge", etc.).
    """

    # Calculate statistics
    avg_matrix = np.mean(matrix, axis=0)
    yerr = np.std(matrix, axis=0)
    
    # Generate x-axis labels
    x_axis_labels = ['0%'] + [f'{p}%' for p in fail_percent]

    # Create a new figure
    plt.figure(figsize=(8, 6))
    plt.errorbar(
        x_axis_labels,
        avg_matrix,
        yerr=yerr,
        fmt="o-",
        markersize=8,
        capsize=6,
        label=failing_type
    )

    # Labels and title
    plt.xlabel("Percentage of Failures")
    plt.ylabel(metric)
    # Optional: Uncomment to include a title
    #plt.title(f"{metric} under {failing_type} failures ({fail_str})"