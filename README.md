# PyRobust

An open-source Python tool for evaluating network robustness using **robustness surface analysis**.

PyRobust enables simulation of progressive node and edge failures to analyze how complex networks degrade under stress. The tool supports **random**, **targeted**, and **epidemic** failure models and generates robustness surfaces that visualize how a network's structural properties change under failure scenarios.

The main codebase is written entirely in Python.  
PyRobust uses `igraph` as a high-performance backend for graph operations, while remaining fully compatible with **NetworkX** for input and integration. 

Users can add or modify metrics and failure models, as well as export results as CSV files or visual plots.

---

## Installation

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd PyRobust
pip install -r requirements.txt
```
---

### Optional: Availability Metric

To use the additional `availability_evaluation` metric:

1. Navigate to the following directory:

    ```bash
    cd rs_metrics/availability_evaluation
    ```

2. Follow the setup instructions provided in its `README.md`.

---

## Generating a Robustness Surface

To run an analysis, use the function `start_robustness_surface` from the file `robustness_surface.py`.

Example usage configurations are provided in the file `rs_example.py`. The included example uses the `Nobel Germany 17` topology stored in: `topologies/nobel_germany.xml`

The general workflow is:

1. Load a network graph
2. Define failure settings and metrics
3. Call `start_robustness_surface(...)`
4. Analyze or visualize the generated output

---

## Documentation

- **Parameter definitions**: [parameters.md](./parameters.md)
- **Supported metrics**: [metrics.md](./metrics.md)

---

## Extending Metrics

To add metrics:

1. Implement the logic in the `rs_metrics/` directory.
2. Register the metric in `rs_metric.py`.

---
