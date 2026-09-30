import pandas as pd
import pm4py
import os

# Input file
input_file = "data/processed/normalized_event_logs.csv"

# Output folder
output_folder = "screenshots"

os.makedirs(output_folder, exist_ok=True)

print("========== CAREFLOW PROCESS DISCOVERY ==========")

# Load normalized hospital event log
df = pd.read_csv(input_file)

print("Total events:", len(df))
print("Total patient cases:", df["Case_ID"].nunique())

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Convert columns to PM4Py standard format
event_log = df.rename(
    columns={
        "Case_ID": "case:concept:name",
        "Activity_Name": "concept:name",
        "Timestamp": "time:timestamp"
    }
)

# Format dataframe for PM4Py
event_log = pm4py.format_dataframe(
    event_log,
    case_id="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp"
)

print("\nDiscovering process model...")

# Discover Directly-Follows Graph
dfg, start_activities, end_activities = (
    pm4py.discover_dfg(event_log)
)

print("\n========== PROCESS DISCOVERY RESULTS ==========")

print("\nStart Activities:")
print(start_activities)

print("\nEnd Activities:")
print(end_activities)

print("\nDirectly-Follows Relationships:")

for connection, frequency in dfg.items():

    source = connection[0]
    target = connection[1]

    print(
        source,
        "->",
        target,
        ":",
        frequency
    )

print("\nProcess discovery completed successfully!")