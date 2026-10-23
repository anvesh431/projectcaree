
import os
import pandas as pd

print("========== PATIENT JOURNEY RISK ANALYSIS ==========")

# Load patient journey data
file_path = "data/dashboard/patient_journey.csv"

if not os.path.exists(file_path):
    print("ERROR: Patient journey data not found.")
    print("Run: python python/dashboard_data.py")
    raise SystemExit(1)

df = pd.read_csv(file_path)

# Check required columns
required_columns = ["Case_ID", "Journey_Time_Minutes"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

df["Journey_Time_Minutes"] = pd.to_numeric(
    df["Journey_Time_Minutes"],
    errors="coerce"
)

df = df.dropna(
    subset=["Case_ID", "Journey_Time_Minutes"]
).copy()

if df.empty:
    raise ValueError("No valid patient journey records found.")

# Calculate journey time statistics
average_time = df["Journey_Time_Minutes"].mean()
median_time = df["Journey_Time_Minutes"].median()

# Calculate percentile thresholds
p75 = df["Journey_Time_Minutes"].quantile(0.75)
p90 = df["Journey_Time_Minutes"].quantile(0.90)

# Categorize patients by relative journey duration
def assign_risk(duration):
    if duration >= p90:
        return "High"
    elif duration >= p75:
        return "Medium"
    else:
        return "Low"

df["Journey_Risk_Level"] = df[
    "Journey_Time_Minutes"
].apply(assign_risk)

# Sort longest journeys first
df = df.sort_values(
    "Journey_Time_Minutes",
    ascending=False
)

# Create summary
risk_summary = (
    df["Journey_Risk_Level"]
    .value_counts()
    .reindex(["Low", "Medium", "High"], fill_value=0)
    .rename_axis("Journey_Risk_Level")
    .reset_index(name="Patient_Count")
)

risk_summary["Percentage"] = (
    risk_summary["Patient_Count"] / len(df) * 100
).round(2)

# Save reports
os.makedirs("data/reports", exist_ok=True)

df.to_csv(
    "data/reports/patient_risk_analysis.csv",
    index=False
)

risk_summary.to_csv(
    "data/reports/patient_risk_summary.csv",
    index=False
)

print("\nTotal Patients:", len(df))
print("Average Journey Time:", round(average_time, 2))
print("Median Journey Time:", round(median_time, 2))
print("75th Percentile:", round(p75, 2))
print("90th Percentile:", round(p90, 2))

print("\nJourney Risk Summary:")
print(risk_summary.to_string(index=False))

print("\nReports generated successfully!")
print("1. data/reports/patient_risk_analysis.csv")
print("2. data/reports/patient_risk_summary.csv")
