import numpy as np
import os
import matplotlib.pyplot as plt
from .plt_heatmaps import plot_heatmaps
from .line_plt import generate_additional_line_plot
from .save_data import save_path

def generate_multiple_plots(metric_matrices, fail_percent, failing_type, fail_str, csv_data, save_as_csv, line_plot):
    """
    @brief Generate surface and optional line plots for each metric.

    This function creates visualizations (heatmaps and optionally line plots) 
    for all metrics in the metric_matrices dictionary. It also stores images 
    and optionally prepares data for CSV export.

    @param metric_matrices Dictionary of metric names -> 2D NumPy arrays [scenarios x failure steps].
    @param fail_percent List of failure percentages (excluding 0%).
    @param failing_type String specifying the failure type ("random", "targeted", etc.).
    @param fail_str String describing the failed components ("node", "edge", "node and edge", etc.).
    @param csv_data Dictionary that will be populated with metric data for CSV saving.
    @param save_as_csv Boolean flag: if True, CSV export is prepared.
    @param line_plot Boolean flag: if True, line plots will also be generated and saved.
    """

    for metric, matrix in metric_matrices.items():
        # Prepare matrix for heatmap: transpose and sort each row (across scenarios)
        transposed_matrix = np.array(matrix).transpose()
        sorted_matrix = np.array([np.sort(row) for row in transposed_matrix])
        reversed_matrix = sorted_matrix[::-1]  # Reverse y-axis for better visual structure

        # Plot heatmap
        plot_heatmaps(reversed_matrix, fail_percent, metric, failing_type, fail_str)

        # Save heatmap figure
        path = save_path(failing_type, fail_str)
        filename = f"rs_{failing_type}_{fail_str}_failure_{metric}.png"
        filename = filename.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(",", "")
        full_path = os.path.join(path, filename)
        os.makedirs(path, exist_ok=True)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        plt.close()

        # Store matrix for CSV if requested
        if save_as_csv:
            csv_data[metric] = matrix

        # Optionally generate and save line plot
        if line_plot:
            generate_additional_line_plot(metric, matrix, fail_percent, failing_type, fail_str)
            line_filename = f"rs_{failing_type}_{fail_str}_failure_{metric}_line_plot.png".replace(" ", "_")
            full_line_path = os.path.join(path, line_filename)
            plt.savefig(full_line_path, dpi=300, bbox_inches='tight')
            plt.close()
            