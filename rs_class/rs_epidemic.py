from . import rs
import numpy as np
from rs_fail_scenario.epidemic_node_failures import generate_epidemic_node_fail_scenarios
from rs_fail_component.fail_nodes import fail_nodes
from rs_plotting.generate_outputs import plot_and_save


class EpidemicFailureRobustness(rs.RobustnessSurface):
    """
    @brief Subclass for evaluating robustness under epidemic-like node failure scenarios.

    This class implements epidemic spreading failures, where nodes fail progressively
    based on some diffusion-like process. Only node failures are supported in this model.

    @note This class is used when @c failing_type is set to "epidemic".
    """

    def __init__(self, graph, failing_type, metrics, failing_percentage_array, num_scenarios=None,
                 failing_nodes=False, failing_edges=False, edge_ratio=None, metric_weights=None,
                 graph_weights="distance", graph_capacity="capacity", A_dic=None,
                 multiple_plots=False, reduced_single_plot=False, add_line_plot=False, save_as_csv=False):
        """
        @brief Constructor for EpidemicFailureRobustness.

        @param graph The input graph to analyze.
        @param failing_type Must be "epidemic" for this subclass to be used.
        @param metrics A list of metric names or (metric_name, mode) tuples to evaluate robustness.
        @param failing_percentage_array A list of failure percentages for each evaluation step.
        @param num_scenarios Number of epidemic failure scenarios to simulate.
        @param failing_nodes Should be True; epidemic failures apply to nodes.
        @param failing_edges Ignored in this class; only node failures are used.
        @param edge_ratio Not used here.
        @param metric_weights Optional list of weights for combining metrics.
        @param graph_weights Name of the edge attribute representing weights (e.g., "distance").
        @param graph_capacity Name of the edge attribute representing capacity.
        @param A_dic Optional dictionary, passed to metric functions if needed.
        @param multiple_plots If True, generate a separate surface plot for each metric.
        @param reduced_single_plot If True, combine metrics into a single surface plot using weights.
        @param add_line_plot If True, add a line plot summarizing the average trend.
        @param save_as_csv If True, save the robustness results as CSV files.
        """

        # Initialize the base class
        super().__init__(graph, failing_type, metrics, failing_percentage_array, num_scenarios,
                         failing_nodes, failing_edges, edge_ratio, metric_weights,
                         graph_weights, graph_capacity, A_dic, multiple_plots,
                         reduced_single_plot, add_line_plot, save_as_csv)

        # Generate epidemic-style node failure scenarios
        self.fail_scenarios = generate_epidemic_node_fail_scenarios(
            self.igraph_graph,
            self.num_scenarios,
            self.fail_percent,
            self.R
        )

        # Prepare metric result matrices
        self.metric_matrices = {
            metric: np.zeros((len(self.fail_scenarios), len(self.fail_percent) + 1))
            for metric in self.metrics
        }

        # Simulate node failures
        fail_nodes(self.igraph_graph, self.fail_scenarios, self.metrics,
                   self.metric_matrices, self.graph_weights,
                   self.graph_capacity, self.A_dic)

        # Generate visual and CSV outputs
        plot_and_save(self.metric_matrices, self.metrics, self.metric_weights, self.fail_percent,
                      self.failing_type, self.failing_nodes, self.failing_edges,
                      self.multiple_plots, self.line_plot, self.reduced_single_plot,
                      self.save_as_csv, self.num_scenarios)