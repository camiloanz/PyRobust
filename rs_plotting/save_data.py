import pandas as pd
import os

def save_csv(csv_data, fail_percent, failing_type, metrics, fail_component, num_scenarios=None, targeted_mode=None):
    data = []
    print(csv_data)
    fail_percentages = [0] + fail_percent
    if failing_type == "random" or failing_type == "epidemic":
        for i in range(num_scenarios):
            for j, percentage in enumerate(fail_percentages):
                row = {
                    "Scenario": i,
                    "Failing Percentage": percentage
                }
                for metric, matrix in csv_data.items():
                    row[metric] = matrix[i, j]
                data.append(row)
        
            
    elif failing_type == "targeted":
        
        for j, percentage in enumerate(fail_percentages):
            row = {
                "Failing Percentage": percentage
            }
            for metric, matrix in csv_data.items():
                matrix = matrix[0]
                row[metric] = matrix[j]
            data.append(row)

    
    dataframe = pd.DataFrame(data)

    path = save_path(failing_type, fail_component, targeted_mode)
    os.makedirs(path, exist_ok=True)

    if len(metrics) > 3:
        file_name = f"rs_{failing_type}_{fail_component}_failure_for_{len(metrics)}_metrics.csv"
    else:
        file_name_raw = f"rs_{failing_type}_{fail_component}_failure_{metrics}.csv"
        file_name = file_name_raw.replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace(" ", "_")
        file_path = os.path.join(path, file_name)
    dataframe.to_csv(file_path, index=False)

    

import os

def save_path(failing_type, failing_component, targeted_mode=None):
    """
    @brief Constructs the directory path to save robustness surface outputs based on failure type.

    @param failing_type Type of failure: "random", "targeted", or "epidemic".
    @param failing_component Component that fails: "node", "edge", or "node_and_edge".
    @param targeted_mode Optional mode for targeted failure scenarios (e.g., "static" or "dynamic").

    @return A string representing the full output directory path.
    """
    output_dir = "rs_output"

    if failing_type == "random":
        main_dir = "random_failures"
        component_map = {
            "node": "node_failures",
            "edge": "edge_failures",
            "node_and_edge": "nodal_and_edge_failures",
            "node and edge": "nodal_and_edge_failures"
        }
        sub_dir = component_map.get(failing_component, "unknown_component")

    elif failing_type == "targeted":
        main_dir = "targeted_failures"
        sub_dir = targeted_mode if targeted_mode else "unspecified_mode"

    elif failing_type == "epidemic":
        main_dir = "epidemic_failures"
        sub_dir = ""

    else:
        main_dir = "unknown_failures"
        sub_dir = ""

    return os.path.join(output_dir, main_dir, sub_dir)