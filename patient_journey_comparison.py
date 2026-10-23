
import os
import pandas as pd

print("========== PATIENT JOURNEY COMPARISON ==========")

# Load patient journey data
file_path = "data/dashboard/patient_journey.csv"

if not os.path.exists(file_path):
    print("ERROR: Patient journey file not found.")
    print("First run: python python/dashboard_data.py")
    raise SystemExit(1)

df = pd.read_csv(file_path)

required_columns = ["Case_ID", "Journey_Time_Minutes"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

# Clean journey times
df["Journey_Time_Minutes"] = pd.to_numeric(
    df["Journey_Time_Minutes"],
    errors="coerce"
)

df = df.dropna(
    subset=["Case_ID", "Journey_Time_Minutes"]
).copy()

if df.empty:
    raise ValueError("No valid patient journeys found.")

# Calculate overall average
average_time = df["Journey_Time_Minutes"].mean()

# Compare each patient with overall average
df["Average_Journey_Time"] = round(average_time, 2)

df["Difference_From_Average"] = (
    df["Journey_Time_Minutes"] - average_time
).round(2)

df["Journey_Performance"] = df[
    "Difference_From_Average"
].apply(
    lambda x: "Above Average Duration"
    if x > 0
    else "Below Average Duration"
    if x < 0
    else "Equal to Average"
)

# Sort longest journeys first
df = df.sort_values(
    "Journey_Time_Minutes",
    ascending=False
)

# Top 10 longest journeys
top_10 = df.head(10).copy()

# Create comparison summary
summary = (
    df.groupby("Journey_Performance")
    .agg(
        Total_Patients=("Case_ID", "count"),
        Average_Journey_Minutes=("Journey_Time_Minutes", "mean"),
        Minimum_Journey_Minutes=("Journey_Time_Minutes", "min"),
        Maximum_Journey_Minutes=("Journey_Time_Minutes", "max")
    )
    .reset_index()
)

time_columns = [
    "Average_Journey_Minutes",
    "Minimum_Journey_Minutes",
    "Maximum_Journey_Minutes"
]

summary[time_columns] = summary[time_columns].round(2)

# Save reports
os.makedirs("data/reports", exist_ok=True)

df.to_csv(
    "data/reports/patient_journey_comparison.csv",
    index=False
)

top_10.to_csv(
    "data/reports/top_10_longest_journeys.csv",
    index=False
)

summary.to_csv(
    "data/reports/journey_comparison_summary.csv",
    index=False
)

print("\nTotal Patients:", len(df))
print("Average Journey Time:", round(average_time, 2), "minutes")

print("\nJourney Comparison Summary:")
print(summary.to_string(index=False))

print("\nTop 10 Longest Patient Journeys:")
print(
    top_10[
        ["Case_ID", "Journey_Time_Minutes", "Difference_From_Average"]
    ].to_string(index=False)
)

print("\nReports generated successfully!")
print("1. data/reports/patient_journey_comparison.csv")
print("2. data/reports/top_10_longest_journeys.csv")
print("3. data/reports/journey_comparison_summary.csv")
