from .multiple_plt import generate_multiple_plots
from .reduced_single_plt import generate_reduced_plot
from .targeted_plt import *
from .save_data import save_csv


def plot_and_save(metric_matrices, metrics, metric_weights, fail_percent, failing_type, 
    failing_nodes, failing_edges, multiple_plots, line_plot, 
    reduced_single_plot, save_as_csv, num_scenarios=None, targeted_mode=None, 
    targeted_metric=None):
    fail = []
    if failing_nodes:
        fail.append("node")
    if failing_edges:
        fail.append("edge")
    fail_component_str = " and ".join(fail)
    fail_component = "_and_".join(fail)

    csv_data = {}

    print(multiple_plots)
    if multiple_plots:
        if failing_type == "targeted":
            print(multiple_plots)
            generate_multiple_targeted_plots(metric_matrices, fail_percent, targeted_mode, targeted_metric, save_as_csv, csv_data)
        else:
            generate_multiple_plots(metric_matrices, fail_percent, failing_type, fail_component_str, csv_data, save_as_csv, line_plot)


    if reduced_single_plot:
        if failing_type == "targeted":
            print(reduced_single_plot)
            generate_reduced_targeted_plot(metric_matrices, metrics, metric_weights, targeted_mode, targeted_metric, fail_percent, save_as_csv, csv_data)
        else:
            generate_reduced_plot(metric_matrices, metrics, metric_weights, fail_percent, failing_type, fail_component_str, save_as_csv, csv_data, line_plot)
    

    if save_as_csv:
        
        save_csv(csv_data, fail_percent, failing_type, metrics, fail_component, num_scenarios, targeted_mode)
