from . import rs
import numpy as np
from rs_fail_scenario.targeted_failure import generate_targeted_fail_scenario
from rs_fail_component.fail_nodes import fail_nodes
from rs_fail_component.fail_edges import fail_edges
from rs_plotting.generate_outputs import plot_and_save


class TargetedFailureRobustness(rs.RobustnessSurface):
    """
    @brief Subclass for evaluating robustness under targeted failure scenarios.

    This class implements targeted attacks based on node or edge importance
    (e.g., degree, centrality). The specific strategy is passed as a tuple
    in the @c failing_type parameter: ("targeted", targeted_metric, mode).

    @note Supports both node-based and edge-based targeted failures.
    """

    def __init__(self, graph, failing_type, metrics, failing_percentage_array, num_scenarios=None,
                 failing_nodes=False, failing_edges=False, edge_ratio=None, metric_weights=None,
                 graph_weights="distance", graph_capacity="capacity", A_dic=None,
                 multiple_plots=False, reduced_single_plot=False, add_line_plot=False, save_as_csv=False):
        """
        @brief Constructor for TargetedFailureRobustness.

        @param graph The input graph to analyze.
        @param failing_type A tuple ("targeted", metric_name, mode) defining the targeting strategy.
        @param metrics A list of metric names or (metric_name, mode) tuples to evaluate robustness.
        @param failing_percentage_array A list of failure percentages for each evaluation step.
        @param num_scenarios Not used in targeted failures; kept for compatibility.
        @param failing_nodes May be overridden internally, depending on the targeted strategy.
        @param failing_edges May be overridden internally, depending on the targeted strategy.
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

        # Generate targeted failure scenarios based on the selected metric and mode
        self.fail_scenarios, self.failing_nodes, self.failing_edges = generate_targeted_fail_scenario(
            self.igraph_graph,
            self.targeted_mode,
            self.targeted_metric,
            self.fail_percent,
            self.graph_weights,
            self.graph_capacity
        )

        # Apply failures depending on type
        if self.failing_nodes:
            self.metric_matrices = {
                metric: np.zeros((len(self.fail_scenarios), len(self.fail_percent) + 1))
                for metric in self.metrics
            }
            fail_nodes(self.igraph_graph, self.fail_scenarios, self.metrics,
                       self.metric_matrices, self.graph_weights,
                       self.graph_capacity, self.A_dic)

        elif self.failing_edges:
            self.metric_matrices = {
                metric: np.zeros((len(self.fail_scenarios), len(self.fail_percent) + 1))
                for metric in self.metrics
            }
            fail_edges(self.igraph_graph, self.fail_scenarios, self.metrics,
                       self.metric_matrices, self.graph_weights,
                       self.graph_capacity, self.A_dic)

        else:
            raise ValueError("Neither 'failing_nodes' nor 'failing_edges' is set to True. At least one must be enabled for the robustness analysis.")

        # Generate outputs (including targeted mode/metric info)
        plot_and_save(self.metric_matrices, self.metrics, self.metric_weights, self.fail_percent,
                      self.failing_type, self.failing_nodes, self.failing_edges,
                      multiple_plots, self.line_plot, reduced_single_plot, save_as_csv,
                      targeted_mode=self.targeted_mode, targeted_metric=self.targeted_metric)