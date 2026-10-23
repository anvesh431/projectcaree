
import pandas as pd
import os

print("========== PATIENT WAITING TIME ANALYSIS ==========")

# Load normalized hospital event logs
df = pd.read_csv(
    "data/processed/normalized_event_logs.csv"
)

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

# Remove invalid records
df = df.dropna(
    subset=["Case_ID", "Activity_Name", "Timestamp"]
)

# Sort events patient-wise
df = df.sort_values(
    by=["Case_ID", "Timestamp"]
).copy()

# Find previous activity and timestamp
df["Previous_Activity"] = (
    df.groupby("Case_ID")["Activity_Name"].shift(1)
)

df["Previous_Timestamp"] = (
    df.groupby("Case_ID")["Timestamp"].shift(1)
)

# Calculate elapsed time between consecutive activities
df["Waiting_Time_Minutes"] = (
    df["Timestamp"] - df["Previous_Timestamp"]
).dt.total_seconds() / 60

# Exclude first event of each patient
waiting_df = df.dropna(
    subset=["Previous_Activity", "Waiting_Time_Minutes"]
).copy()

# Calculate average time before each activity
waiting_summary = (
    waiting_df.groupby("Activity_Name")
    .agg(
        Average_Waiting_Time=("Waiting_Time_Minutes", "mean"),
        Maximum_Waiting_Time=("Waiting_Time_Minutes", "max"),
        Total_Transitions=("Waiting_Time_Minutes", "count")
    )
    .reset_index()
)

waiting_summary = waiting_summary.sort_values(
    by="Average_Waiting_Time",
    ascending=False
)

waiting_summary[
    ["Average_Waiting_Time", "Maximum_Waiting_Time"]
] = waiting_summary[
    ["Average_Waiting_Time", "Maximum_Waiting_Time"]
].round(2)

# Create output directory
os.makedirs("data/reports", exist_ok=True)

# Save detailed patient waiting times
waiting_df.to_csv(
    "data/reports/patient_waiting_details.csv",
    index=False
)

# Save activity-wise waiting summary
waiting_summary.to_csv(
    "data/reports/patient_waiting_summary.csv",
    index=False
)

print("\nActivity-wise waiting time:")
print(waiting_summary.to_string(index=False))

print("\nReports generated successfully!")
print("1. data/reports/patient_waiting_details.csv")
print("2. data/reports/patient_waiting_summary.csv")
