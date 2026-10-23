
import pandas as pd
import os

print("========== HOSPITAL PERFORMANCE ==========")

# Load normalized event logs
events = pd.read_csv(
    "data/processed/normalized_event_logs.csv"
)

events["Timestamp"] = pd.to_datetime(
    events["Timestamp"],
    errors="coerce"
)

events = events.dropna(
    subset=["Case_ID", "Activity_Name", "Timestamp"]
)

events = events.sort_values(
    ["Case_ID", "Timestamp"]
)

# Total patients and events
total_patients = events["Case_ID"].nunique()
total_events = len(events)

# Count activities per patient
patient_activity = (
    events.groupby("Case_ID")
    .agg(
        Total_Activities=("Activity_Name", "count"),
        Start_Time=("Timestamp", "min"),
        End_Time=("Timestamp", "max")
    )
    .reset_index()
)

# Calculate patient journey duration
patient_activity["Journey_Time_Minutes"] = (
    patient_activity["End_Time"]
    - patient_activity["Start_Time"]
).dt.total_seconds() / 60

# Average activities per patient
average_activities = (
    patient_activity["Total_Activities"].mean()
)

# Average patient journey time
average_journey = (
    patient_activity["Journey_Time_Minutes"].mean()
)

# Save report
os.makedirs("data/reports", exist_ok=True)

patient_activity.to_csv(
    "data/reports/hospital_performance.csv",
    index=False
)

print("Total Patients:", total_patients)
print("Total Events:", total_events)
print(
    "Average Activities per Patient:",
    round(average_activities, 2)
)
print(
    "Average Journey Time:",
    round(average_journey, 2),
    "minutes"
)

print("Hospital performance report generated!")
