# Supported Metrics in PyRobust

This document lists all metrics currently supported by PyRobust and their configurations.

Some metrics return scalar values and can be used directly (e.g., `"connectivity"`), while others return node- or edge-level values and require an evaluation **mode** such as `"mean"`, `"max"`, or `"min"` to summarize them.

---

## Format

Metrics can be specified as:

- A **string**, for metrics that return a single value.
- A **tuple** `(metric_name, mode)`, where `mode` defines how to reduce node- or edge-level values.

### Common types:
- `"mean"` — average value
- `"max"` — maximum value
- `"min"` — minimum value

---

## Metrics Overview

| Metric Name                  | Requires Mode  | Use as Targeted Metric  | Short Description |
|------------------------------|----------------|----------------------|-------------|
| `availability`               | No             | No                   | Metric from optional availability module |
| `average_path_length`        | No             | Yes                  | Average shortest path length (weighted) |
| `average_path_length_in_hops`| No             | Yes                  | Average path length in number of hops (ignores edge weights) |
| `betweenness_centrality`     | Yes            | Yes                  | Betweenness centrality of nodes |
| `closeness_centrality`       | Yes            | Yes                  | Closeness centrality of nodes |
| `connectivity`               | No             | No                   | Percentage of connected node pairs |
| `diameter`                   | No             | No                   | Longest shortest path in the graph |
| `eccentricity`               | Yes            | Yes                  | Eccentricity |
| `edge_betweenness`           | Yes            | Yes                  | Betweenness centrality of edges |
| `eigenvector_centrality`     | Yes            | Yes                  | Eigenvector centrality of nodes |
| `harmonic_centrality`        | Yes            | Yes                  | Harmonic mean of shortest path lengths per node |
| `maxflow`                    | Yes            | No                   | Maximum flow between node pairs |
| `nodal_degree`               | Yes            | Yes                  | Degree centrality of nodes |
| `rLCC`                       | No             | No                   | Relative size of the largest connected component |
| `strength`                   | Yes            | Yes                  | Strength of nodes |

---

## Notes

- If a metric requires a mode, it must be passed as a tuple: `("metric_name", "mode")`
- Modes are ignored for metrics that return a single scalar (e.g., `"connectivity"`)
- Metrics that depend on edge attributes may require `graph_weights` or `graph_capacity`

---

## Adding Custom Metrics

You can add your own metric by implementing it in the `rs_metrics/` directory and registering it in `rs_metric.py`.  
Custom metric functions must be compatible with the interface used by `compute_metric(...)`.  
The function should have the following signature:

```python
def calculate_my_metric(graph, mode, type=None, **kwargs):
```

The function can support two modes:

- **`mode="rs_value"`** *(default mode for robustness output — required)*  
  Return a single scalar value representing the network's robustness.  
  If applicable, use the type argument to reduce node/edge-level values: 
  - `"mean"`
  - `"max"`
  - `"min"`

- **`mode="targeted"`**  
  Return a ranking list from highest node/edge to target to least

```

To register the metric in `rs_metric.py`, add it to the `metric_func` dictionary:

```python
from rs_metrics import my_metric

metric_func["my_metric"] = my_metric.calculate_my_metric
```
