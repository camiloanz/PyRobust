# Parameter Guide: `start_robustness_surface`

This document explains all accepted parameters in detail.  
For inline documentation and API reference, see the class-level docstring in `robustness_surface.py`.

---

## `graph`
The input graph to be analyzed. It will be internally converted into an `igraph.Graph`.

---

## `metrics`
**Type:** `list[str]` or `list[tuple[str, str]]` 
A list of metric names or `(metric_name, mode)` tuples.

If a metric returns node- or edge-level values (e.g., centralities), a mode must be specified to summarize them:
- `"mean"` – mean value
- `"max"` – maximum value
- `"min"` – minimum value

See [metrics.md](./metrics.md) for a full list of supported metrics and their different configurations.

---

## `metric_weights`
**Type:** `list[float]`  
**Required if:** `reduced_single_plot=True`  
A list of weights assigned to each selected metric when generating a combined robustness surface.  

Weights reflect the relative importance or scale of each metric.  
They do **not** have to be normalized (i.e., they don't need to sum to 1.0), but they will be used proportionally.

---

## `failing_nodes`
**Type:** `bool`  
If `True`, node failures are simulated.

---

## `failing_edges`
**Type:** `bool`  
If `True`, edge failures are simulated.

---

## `failing_type`
**Type:** `str` or `tuple`  
Defines the failure strategy applied during simulation. Possible values:

- `"random"`  
  Simulates random failure of nodes and/or edges.

- `("targeted", metric_name, mode)`  
  Applies targeted failure based on a centrality or ranking metric.  
  The `mode` defines how often the ranking is updated:
  - `"static"` – ranking is computed once before the simulation
  - `"dynamic"` – ranking is re-evaluated after each failure step

  See [metrics.md](./metrics.md) for a list of available metrics and which are compatible with targeted failure strategies.

- `"epidemic"`  
  Simulates failure spreading from a randomly selected node to its neighbors.

---

## `edge_ratio`
**Type:** `float`  
Number of edge failures per failed node.  
Required only if both `failing_nodes=True` and `failing_edges=True`.

---

## `failing_percentage_array`
**Type:** `list[int]`  
A list of failure percentages to simulate.

Example:
```python
[i * 5 for i in range(1, 15)]  # [5, 10, ..., 70]
```

---

## `multiple_plots`
**Type:** `bool`  
If `True`, generates one robustness surface plot for each metric.

---

## `reduced_single_plot`
**Type:** `bool`  
If `True`, generates a single robustness surface by combining all metrics using the provided `metric_weights`.

---

## `add_line_plot`
**Type:** `bool`  
If `True`, generates an additional line plot that summarizes the robustness surface as an average trend over all failure scenarios.  
Each point shows the mean metric value at a given failure percentage, with error bars representing the standard deviation.  
This plot is added alongside the surface(s) generated via `multiple_plots` or `reduced_single_plot`.

---

## `save_as_csv`
**Type:** `bool`  
If `True`, exports all results as CSV files in the `rs_output/failing_type` directory.

---

## `num_scenarios`
**Type:** `int`  
Number of randomized failure scenarios to simulate

---

## `graph_weights`
**Type:** `str`  
Optional. Name of the edge attribute in the input graph that stores weights or distances.  
This is used by metrics that depend on edge length such as `average_path_length`.

Make sure this name matches the attribute used in your graph (e.g., `"weight"`, `"length"`, `"distance"`).

Default (if present): `"distance"`

---

## `graph_capacity`
**Type:** `str`  
Optional. Name of the edge attribute in the input graph that defines capacity values.  
Used by metrics such as `maxflow`.

Make sure this matches the attribute name used in your graph (e.g., `"capacity"`, `"bandwidth"`, `"capacity_mbps"`).

Default (if present): `"capacity"`
