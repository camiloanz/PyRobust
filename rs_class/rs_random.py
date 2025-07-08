from . import rs
import numpy as np
from rs_fail_scenario.random_node_failures import generate_random_node_fail_scenarios
from rs_fail_scenario.random_edges_fail_scenario import generate_random_edge_fail_scenarios
from rs_fail_scenario.random_node_and_edges_fail_scenario import generate_random_node_and_edge_fail_scenarios
from rs_fail_component.fail_nodes import fail_nodes
from rs_fail_component.fail_edges import fail_edges
from rs_fail_component.fail_nodes_and_edges import fail_nodes_and_edges
from rs_plotting.generate_outputs import plot_and_save

class RandomFailureRobustness(rs.RobustnessSurface):
    """
    @brief Specialized subclass for analyzing robustness under random failure scenarios.

    This class handles robustness evaluation for randomly failing nodes, edges,
    or a combination of both. It extends the base RobustnessSurface class
    and applies appropriate scenario generation and failure handling.

    @note This class is used when @c failing_type is set to "random".
    """

    def __init__(self, graph, failing_type, metrics, failing_percentage_array=[i * 5 for i in range(1, 15)], num_scenarios=15,
                 failing_nodes=False, failing_edges=False, edge_ratio=None, metric_weights=None,
                 graph_weights="distance", graph_capacity="capacity", A_dic=None,
                 multiple_plots=False, reduced_single_plot=False, add_line_plot=False, save_as_csv=False):
        """
        @brief Constructor for the RandomFailureRobustness class.

        @param graph The input graph to analyze.
        @param failing_type Must be "random" for this subclass to be used.
        @param metrics A list of metric names or (metric_name, mode) tuples to evaluate robustness.
        @param failing_percentage_array A list of failure percentages for each evaluation step.
        @param num_scenarios Number of random failure scenarios to simulate.
        @param failing_nodes If True, simulate random node failures.
        @param failing_edges If True, simulate random edge failures.
        @param edge_ratio Ratio of edge to node failures (required if both types are simulated).
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
        super().__init__(graph, failing_type, metrics, failing_percentage_array, num_scenarios, failing_nodes, failing_edges, edge_ratio, metric_weights, graph_weights, 
                         graph_capacity, A_dic, multiple_plots, reduced_single_plot, add_line_plot, save_as_csv)

        # Node + edge failures
        if self.failing_nodes and self.failing_edges:
            self.fail_scenarios = generate_random_node_and_edge_fail_scenarios(
                self.igraph_graph.vs.indices,
                self.igraph_graph.es.indices,
                self.num_scenarios,
                self.fail_percent,
                self.ratio,
                self.R
            )
            self.metric_matrices = {
                metric: np.zeros((len(self.fail_scenarios), len(self.fail_percent) + 1)) for metric in self.metrics
            }
            fail_nodes_and_edges(
                self.igraph_graph,
                self.fail_scenarios,
                self.metrics,
                self.metric_matrices,
                self.graph_weights,
                self.graph_capacity,
                self.A_dic
            )

        # Only node failures
        elif self.failing_nodes:
            self.fail_scenarios = generate_random_node_fail_scenarios(
                self.igraph_graph.vs.indices,
                self.num_scenarios,
                self.fail_percent,
                self.R
            )
            self.metric_matrices = {
                metric: np.zeros((len(self.fail_scenarios), len(self.fail_percent) + 1)) for metric in self.metrics
            }
            fail_nodes(
                self.igraph_graph,
                self.fail_scenarios,
                self.metrics,
                self.metric_matrices,
                self.graph_weights,
                self.graph_capacity,
                self.A_dic
            )

        # Only edge failures
        elif self.failing_edges:
            self.fail_scenarios = generate_random_edge_fail_scenarios(
                self.igraph_graph.es.indices,
                self.num_scenarios,
                self.fail_percent,
                self.R
            )
            self.metric_matrices = {
                metric: np.zeros((len(self.fail_scenarios), len(self.fail_percent) + 1)) for metric in self.metrics
            }
            fail_edges(
                self.igraph_graph,
                self.fail_scenarios,
                self.metrics,
                self.metric_matrices,
                self.graph_weights,
                self.graph_capacity,
                self.A_dic
            )

        # Neither node nor edge failures were selected
        else:
            raise ValueError("Neither 'failing_nodes' nor 'failing_edges' is set to True. At least one must be enabled.")

        # Generate visual and CSV outputs
        plot_and_save(
            self.metric_matrices,
            self.metrics,
            self.metric_weights,
            self.fail_percent,
            self.failing_type,
            self.failing_nodes,
            self.failing_edges,
            self.multiple_plots,
            self.line_plot,
            self.reduced_single_plot,
            self.save_as_csv,
            self.num_scenarios
        )