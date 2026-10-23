
import os
import pandas as pd

print("========== HOSPITAL EFFICIENCY ANALYSIS ==========")

# Load normalized hospital event logs
file_path = "data/processed/normalized_event_logs.csv"

if not os.path.exists(file_path):
    print("ERROR: Normalized event logs not found.")
    raise SystemExit(1)

df = pd.read_csv(file_path)

required_columns = ["Case_ID", "Activity_Name", "Timestamp"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

df = df.dropna(subset=required_columns).copy()

if df.empty:
    raise ValueError("No valid hospital events found.")

# Sort events patient-wise
df = df.sort_values(
    ["Case_ID", "Timestamp"]
)

# Calculate next activity and its timestamp
df["Next_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(-1)
)

df["Next_Timestamp"] = (
    df.groupby("Case_ID")["Timestamp"].shift(-1)
)

# Calculate time between activities
df["Transition_Time_Minutes"] = (
    df["Next_Timestamp"] - df["Timestamp"]
).dt.total_seconds() / 60

# Exclude last event of each patient
transitions = df.dropna(
    subset=["Next_Activity", "Transition_Time_Minutes"]
).copy()

# Calculate activity transition performance
efficiency = (
    transitions.groupby(["Activity_Name", "Next_Activity"])
    .agg(
        Total_Transitions=("Case_ID", "count"),
        Average_Time_Minutes=("Transition_Time_Minutes", "mean"),
        Minimum_Time_Minutes=("Transition_Time_Minutes", "min"),
        Maximum_Time_Minutes=("Transition_Time_Minutes", "max")
    )
    .reset_index()
)

# Round numeric values
time_columns = [
    "Average_Time_Minutes",
    "Minimum_Time_Minutes",
    "Maximum_Time_Minutes"
]

efficiency[time_columns] = efficiency[time_columns].round(2)

# Sort by longest average transition time
efficiency = efficiency.sort_values(
    "Average_Time_Minutes",
    ascending=False
)

# Calculate patient journey performance
journeys = (
    df.groupby("Case_ID")
    .agg(
        Start_Time=("Timestamp", "min"),
        End_Time=("Timestamp", "max"),
        Total_Activities=("Activity_Name", "count")
    )
    .reset_index()
)

journeys["Journey_Time_Minutes"] = (
    journeys["End_Time"] - journeys["Start_Time"]
).dt.total_seconds() / 60

# Generate summary
summary = pd.DataFrame({
    "Metric": [
        "Total Patients",
        "Total Events",
        "Unique Activities",
        "Average Journey Time (Minutes)",
        "Average Transition Time (Minutes)"
    ],
    "Value": [
        df["Case_ID"].nunique(),
        len(df),
        df["Activity_Name"].nunique(),
        round(journeys["Journey_Time_Minutes"].mean(), 2),
        round(transitions["Transition_Time_Minutes"].mean(), 2)
    ]
})

# Save reports
os.makedirs("data/reports", exist_ok=True)

efficiency.to_csv(
    "data/reports/hospital_efficiency.csv",
    index=False
)

summary.to_csv(
    "data/reports/hospital_efficiency_summary.csv",
    index=False
)

print("\nHospital Efficiency Summary:")
print(summary.to_string(index=False))

print("\nTop 5 Slowest Activity Transitions:")
print(efficiency.head(5).to_string(index=False))

print("\nReports generated successfully!")
print("1. data/reports/hospital_efficiency.csv")
print("2. data/reports/hospital_efficiency_summary.csv")
