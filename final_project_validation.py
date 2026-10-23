
import os
from datetime import datetime
import pandas as pd

print("========== CAREFLOW FINAL PROJECT VALIDATION ==========")

# Required project datasets
required_files = {
    "Raw Event Logs": "data/raw/hospital_event_logs.csv",
    "Normalized Event Logs": "data/processed/normalized_event_logs.csv",
    "Bottleneck Analysis": "data/processed/bottleneck_analysis.csv",
    "Dashboard Summary": "data/dashboard/dashboard_summary.csv",
    "Activity Frequency": "data/dashboard/activity_frequency.csv",
    "Patient Journey": "data/dashboard/patient_journey.csv",
    "Hospital Performance": "data/reports/hospital_performance.csv",
    "Waiting Time Summary": "data/reports/patient_waiting_summary.csv",
    "Patient Risk Analysis": "data/reports/patient_risk_analysis.csv",
    "Hospital Efficiency": "data/reports/hospital_efficiency.csv",
    "Journey Comparison": "data/reports/patient_journey_comparison.csv"
}

validation_results = []

# Validate each CSV
for name, path in required_files.items():
    if not os.path.exists(path):
        validation_results.append({
            "Dataset": name,
            "File_Path": path,
            "Status": "Missing",
            "Rows": 0,
            "Columns": 0
        })
        continue

    try:
        df = pd.read_csv(path)

        status = "Valid" if not df.empty else "Empty"

        validation_results.append({
            "Dataset": name,
            "File_Path": path,
            "Status": status,
            "Rows": len(df),
            "Columns": len(df.columns)
        })

    except Exception as error:
        validation_results.append({
            "Dataset": name,
            "File_Path": path,
            "Status": f"Error: {error}",
            "Rows": 0,
            "Columns": 0
        })

# Create validation report
validation_df = pd.DataFrame(validation_results)

total_files = len(validation_df)
valid_files = (
    validation_df["Status"] == "Valid"
).sum()
missing_files = (
    validation_df["Status"] == "Missing"
).sum()

# Check event log data
event_file = "data/processed/normalized_event_logs.csv"

total_patients = "N/A"
total_events = "N/A"
total_activities = "N/A"

if os.path.exists(event_file):
    try:
        events = pd.read_csv(event_file)

        if {"Case_ID", "Activity_Name"}.issubset(events.columns):
            total_patients = events["Case_ID"].nunique()
            total_events = len(events)
            total_activities = events["Activity_Name"].nunique()
    except Exception as error:
        print("Event log summary error:", error)

# Save reports
os.makedirs("data/reports", exist_ok=True)

validation_df.to_csv(
    "data/reports/final_validation_report.csv",
    index=False
)

# Generate project summary
summary_lines = [
    "CAREFLOW - CLINICAL PATHWAY PROCESS MINING",
    "FINAL PROJECT SUMMARY",
    "=" * 50,
    f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "",
    "PROJECT OVERVIEW",
    "CareFlow analyzes simulated hospital event logs",
    "to understand patient journeys and process delays.",
    "",
    "PROJECT METRICS",
    f"Total Patients: {total_patients}",
    f"Total Events: {total_events}",
    f"Unique Activities: {total_activities}",
    "",
    "DATA VALIDATION",
    f"Total Required Files: {total_files}",
    f"Valid Files: {valid_files}",
    f"Missing Files: {missing_files}",
    f"Other Issues: {total_files - valid_files - missing_files}",
    "",
    "PROJECT COMPONENTS",
    "- Hospital Event Log Processing",
    "- Patient Journey Analysis",
    "- Bottleneck Analysis",
    "- Waiting Time Analysis",
    "- Hospital Efficiency Analysis",
    "- Patient Journey Comparison",
    "- Interactive Streamlit Dashboard",
    "",
    "VALIDATION RESULT",
    (
        "All required CSV files are present and non-empty."
        if valid_files == total_files
        else "Some required CSV files need attention."
    ),
    "",
    "NOTE",
    "This report checks CSV file presence and readability.",
    "It does not verify every calculation or dashboard feature."
]

summary_path = "data/reports/final_project_summary.txt"

with open(summary_path, "w", encoding="utf-8") as file:
    file.write("\n".join(summary_lines))

# Display results
print("\nDATASET VALIDATION RESULTS")
print(validation_df.to_string(index=False))

print("\nFINAL PROJECT SUMMARY")
print("\n".join(summary_lines))

print("\nReports generated successfully!")
print("1. data/reports/final_validation_report.csv")
print("2. data/reports/final_project_summary.txt")
