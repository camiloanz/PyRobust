import numpy as np
import matplotlib.pyplot as plt
import os
from .plt_heatmaps import plot_heatmaps
from .save_data import save_path
from .line_plt import generate_additional_line_plot

def generate_reduced_plot(metric_matrices, metrics, metric_weights, fail_percent,
                          failing_type, fail_str, save_as_csv, csv_data, line_plot):
    """
    @brief Generates a reduced robustness surface plot by aggregating multiple metrics with weights.

    This function computes a weighted sum of different metric matrices to produce a single
    combined robustness surface (heatmap), and optionally saves it and its line plot as image files.

    @param metric_matrices Dictionary mapping metric names to 2D numpy arrays of shape [scenarios x fail_levels].
    @param metrics List of metric names used in the analysis.
    @param metric_weights List of weights corresponding to the metrics (same order as `metrics`).
    @param fail_percent List of failure percentages for the simulation steps.
    @param failing_type Type of failure used ("random", "epidemic", etc.).
    @param fail_str Human-readable string describing the failing components (e.g., "node", "node and edge").
    @param save_as_csv If True, save the reduced data to the `csv_data` dictionary.
    @param csv_data Dictionary to which CSV-exportable results are written.
    @param line_plot If True, also generate a line plot representing average trends with error bars.
    """

    # Initialize combined metric matrix (same shape as individual matrices)
    weighted_results = np.zeros_like(next(iter(metric_matrices.values())))

    # Aggregate weighted metrics
    for i, (metric, matrix) in enumerate(metric_matrices.items()):
        weighted_results += metric_weights[i] * matrix

    # Prepare the matrix for heatmap visualization
    transposed_matrix = np.array(weighted_results).transpose()
    sorted_matrix = np.array([np.sort(row) for row in transposed_matrix])
    reversed_matrix = sorted_matrix[::-1]

    # Use the last metric name (arbitrary) for labeling (you could use a fixed name like "combined")
    plot_heatmaps(reversed_matrix, fail_percent, metrics, failing_type, fail_str)

    # Construct filename depending on number of metrics
    if len(metrics) > 3:
        filename = f"rs_{failing_type}_{fail_str}_failure_for_{len(metrics)}_metrics.png"
    else:
        filename = f"rs_{failing_type}_{fail_str}_failure_{metrics}.png"

    # Save the heatmap to disk
    path = save_path(failing_type, fail_str)
    filename = filename.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(",", "")
    full_path = os.path.join(path, filename)
    os.makedirs(path, exist_ok=True)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')

    # Optionally export matrix to CSV
    if save_as_csv:
        csv_data[f"{metrics} (weighted by: {metric_weights})"] = weighted_results

    # Optionally generate and save line plot
    if line_plot:
        generate_additional_line_plot(metrics, weighted_results, fail_percent, failing_type, fail_str)

        if len(metrics) > 3:
            filename = f"rs_{failing_type}_{fail_str}_failure_for_{len(metrics)}_metrics_line_plot.png"
        else:
            filename = f"rs_{failing_type}_{fail_str}_failure_{metrics}_line_plot.png"
        
        filename = filename.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(",", "")
        full_path = os.path.join(path, filename)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')