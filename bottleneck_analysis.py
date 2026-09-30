import pandas as pd
import os

print("========== CAREFLOW BOTTLENECK ANALYSIS ==========")

# Input file
input_file = "data/processed/normalized_event_logs.csv"

# Output file
output_file = "data/processed/bottleneck_analysis.csv"

# Load normalized event log
df = pd.read_csv(input_file)

# Convert timestamp
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

# Sort patient events
df = df.sort_values(
    by=["Case_ID", "Timestamp"]
)

# Get next activity for each patient
df["Next_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(-1)
)

# Get next timestamp
df["Next_Timestamp"] = (
    df.groupby("Case_ID")["Timestamp"].shift(-1)
)

# Calculate transition time in minutes
df["Transition_Time_Minutes"] = (
    (
        df["Next_Timestamp"] - df["Timestamp"]
    ).dt.total_seconds() / 60
)

# Remove last activity of each patient
transitions = df.dropna(
    subset=[
        "Next_Activity",
        "Transition_Time_Minutes"
    ]
)

# Create transition name
transitions["Transition"] = (
    transitions["Activity_Name"]
    + " -> "
    + transitions["Next_Activity"]
)

# Calculate statistics for each transition
bottleneck_summary = (
    transitions
    .groupby("Transition")
    .agg(
        Frequency=("Transition", "count"),
        Average_Time_Minutes=(
            "Transition_Time_Minutes",
            "mean"
        ),
        Minimum_Time_Minutes=(
            "Transition_Time_Minutes",
            "min"
        ),
        Maximum_Time_Minutes=(
            "Transition_Time_Minutes",
            "max"
        )
    )
    .reset_index()
)

# Round values
bottleneck_summary[
    "Average_Time_Minutes"
] = bottleneck_summary[
    "Average_Time_Minutes"
].round(2)

bottleneck_summary[
    "Minimum_Time_Minutes"
] = bottleneck_summary[
    "Minimum_Time_Minutes"
].round(2)

bottleneck_summary[
    "Maximum_Time_Minutes"
] = bottleneck_summary[
    "Maximum_Time_Minutes"
].round(2)

# Sort by highest average transition time
bottleneck_summary = bottleneck_summary.sort_values(
    by="Average_Time_Minutes",
    ascending=False
)

# Save results
os.makedirs(
    "data/processed",
    exist_ok=True
)

bottleneck_summary.to_csv(
    output_file,
    index=False
)

print("\n========== BOTTLENECK RESULTS ==========")

print(
    bottleneck_summary.to_string(index=False)
)

# Display biggest bottleneck
if not bottleneck_summary.empty:

    biggest_bottleneck = bottleneck_summary.iloc[0]

    print("\n========== BIGGEST BOTTLENECK ==========")

    print(
        "Transition:",
        biggest_bottleneck["Transition"]
    )

    print(
        "Average waiting time:",
        biggest_bottleneck["Average_Time_Minutes"],
        "minutes"
    )

print("\nAnalysis completed successfully!")
print("Results saved at:", output_file)