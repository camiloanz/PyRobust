import os
import matplotlib.pyplot as plt
import numpy as np
from .save_data import save_path


def generate_multiple_targeted_plots(metric_matrices, fail_percent, targeted_mode, targeted_metric, save_as_csv, csv_data):
    """
    Generate line plots for each metric in targeted failure scenarios.
    """
    x_axis_labels = ['0%'] + [f'{p}%' for p in fail_percent]

    for metric, matrix in metric_matrices.items():
        plt.figure(figsize=(8, 6))
        plt.plot(x_axis_labels, matrix[0], marker="o", markersize=8)

        plt.xlabel("Percentage of Failures")
        plt.ylabel(metric)

        path = save_path("targeted", targeted_mode=targeted_mode, failing_component=None)
        filename = f"rs_targeted_{targeted_mode}_failure_{metric}_{targeted_metric}_based.png"
        filename = sanitize_filename(filename)
        full_path = os.path.join(path, filename)

        os.makedirs(path, exist_ok=True)
        plt.savefig(full_path, dpi=300, bbox_inches='tight')

        if save_as_csv:
            csv_data[metric] = matrix


def generate_reduced_targeted_plot(metric_matrices, metrics, metric_weights, targeted_mode, targeted_metric, fail_percent, save_as_csv, csv_data):
    """
    Generate a combined (weighted) plot for all metrics under targeted failure.
    """
    weighted_results = np.zeros_like(next(iter(metric_matrices.values())))

    for i, (metric, matrix) in enumerate(metric_matrices.items()):
        weighted_results += metric_weights[i] * matrix

    x_axis_labels = ['0%'] + [f'{p}%' for p in fail_percent]
    plt.figure(figsize=(8, 6))
    plt.plot(x_axis_labels, weighted_results[0], marker="o", markersize=8)

    plt.xlabel("Percentage of Failures")
    plt.ylabel("Weighted Robustness")

    path = save_path("targeted", targeted_mode=targeted_mode, failing_component=None)

    if len(metrics) > 3:
        filename = f"rs_targeted_{targeted_mode}_failure_for_{len(metrics)}_metrics_{targeted_metric}_based.png"
    else:
        filename = f"rs_targeted_{targeted_mode}_failure_{metrics}_{targeted_metric}_based.png"

    filename = sanitize_filename(filename)
    full_path = os.path.join(path, filename)

    os.makedirs(path, exist_ok=True)
    plt.savefig(full_path, dpi=300, bbox_inches='tight')

    if save_as_csv:
        csv_data[f"{metrics} (weighted by: {metric_weights})"] = weighted_results


def sanitize_filename(filename):
    """
    Removes or replaces problematic characters from a filename.
    """
    return filename.replace(" ", "_").replace("(", "").replace(")", "").replace("'", "").replace(",", "")