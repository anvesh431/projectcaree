import pandas as pd
import os

print("========== CAREFLOW DASHBOARD DATA ==========")

# File paths
event_file = "data/processed/normalized_event_logs.csv"
bottleneck_file = "data/processed/bottleneck_analysis.csv"

output_folder = "data/dashboard"
os.makedirs(output_folder, exist_ok=True)

# Load datasets
events = pd.read_csv(event_file)
bottlenecks = pd.read_csv(bottleneck_file)

# Convert timestamp
events["Timestamp"] = pd.to_datetime(
    events["Timestamp"],
    errors="coerce"
)

# Sort events
events = events.sort_values(
    by=["Case_ID", "Timestamp"]
)

# -----------------------------
# KPI 1: Total Patients
# -----------------------------

total_patients = events["Case_ID"].nunique()

# -----------------------------
# KPI 2: Total Events
# -----------------------------

total_events = len(events)

# -----------------------------
# KPI 3: Total Activities
# -----------------------------

total_activities = events["Activity_Name"].nunique()

# -----------------------------
# KPI 4: Average Patient Journey
# -----------------------------

patient_journey = (
    events.groupby("Case_ID")["Timestamp"]
    .agg(["min", "max"])
)

patient_journey["Journey_Time_Minutes"] = (
    (
        patient_journey["max"]
        - patient_journey["min"]
    ).dt.total_seconds() / 60
)

average_journey_time = (
    patient_journey["Journey_Time_Minutes"].mean()
)

# -----------------------------
# KPI 5: Average Transition Time
# -----------------------------

average_transition_time = (
    bottlenecks["Average_Time_Minutes"].mean()
)

# -----------------------------
# Biggest Bottleneck
# -----------------------------

biggest_bottleneck = (
    bottlenecks
    .sort_values(
        "Average_Time_Minutes",
        ascending=False
    )
    .iloc[0]
)

# Create KPI table
kpi_data = pd.DataFrame({
    "Metric": [
        "Total Patients",
        "Total Events",
        "Total Activities",
        "Average Journey Time (Minutes)",
        "Average Transition Time (Minutes)",
        "Biggest Bottleneck",
        "Bottleneck Average Time (Minutes)"
    ],

    "Value": [
        total_patients,
        total_events,
        total_activities,
        round(average_journey_time, 2),
        round(average_transition_time, 2),
        biggest_bottleneck["Transition"],
        biggest_bottleneck["Average_Time_Minutes"]
    ]
})

# Save KPI data
kpi_file = "data/dashboard/dashboard_kpis.csv"

kpi_data.to_csv(
    kpi_file,
    index=False
)

# Activity frequency for charts
activity_frequency = (
    events["Activity_Name"]
    .value_counts()
    .reset_index()
)

activity_frequency.columns = [
    "Activity_Name",
    "Frequency"
]

activity_file = (
    "data/dashboard/activity_frequency.csv"
)

activity_frequency.to_csv(
    activity_file,
    index=False
)

print("\n========== DASHBOARD KPIs ==========")
print(kpi_data.to_string(index=False))

print("\nDashboard data created successfully!")
print("KPI file:", kpi_file)
print("Activity file:", activity_file)