import pandas as pd
import pm4py
import os

print("========== CAREFLOW PROCESS MAP ==========")

# Input dataset
input_file = "data/processed/normalized_event_logs.csv"

# Output folder
output_folder = "screenshots"
os.makedirs(output_folder, exist_ok=True)

# Load dataset
df = pd.read_csv(input_file)

print("Total events:", len(df))
print("Total patients:", df["Case_ID"].nunique())

# Convert timestamp
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"]
)

# Convert columns into PM4Py format
event_log = df.rename(
    columns={
        "Case_ID": "case:concept:name",
        "Activity_Name": "concept:name",
        "Timestamp": "time:timestamp"
    }
)

event_log = pm4py.format_dataframe(
    event_log,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

print("Discovering Directly-Follows Graph...")

# Discover process
dfg, start_activities, end_activities = (
    pm4py.discover_dfg(event_log)
)

# Save process map
output_file = "screenshots/careflow_process_map.png"

pm4py.save_vis_dfg(
    dfg,
    start_activities,
    end_activities,
    output_file
)

print("\nProcess map generated successfully!")
print("Saved at:", output_file)