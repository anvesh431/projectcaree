
import os
import pandas as pd
import matplotlib.pyplot as plt

print("========== ACTIVITY PERFORMANCE VISUALIZATION ==========")

# Load waiting time summary from Commit #12
file_path = "data/reports/patient_waiting_summary.csv"

if not os.path.exists(file_path):
    print("ERROR: Waiting time summary not found.")
    print("First run: python python/patient_waiting_time.py")
    raise SystemExit(1)

df = pd.read_csv(file_path)

required_columns = [
    "Activity_Name",
    "Average_Waiting_Time",
    "Maximum_Waiting_Time"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

if df.empty:
    raise ValueError("Waiting time summary is empty.")

# Create charts directory
os.makedirs("screenshots", exist_ok=True)

# Chart 1: Average Waiting Time
avg_df = df.sort_values(
    "Average_Waiting_Time",
    ascending=True
)

plt.figure(figsize=(11, 6))

bars = plt.barh(
    avg_df["Activity_Name"],
    avg_df["Average_Waiting_Time"],
    color="#2563EB"
)

plt.title(
    "CareFlow - Average Time Between Activities",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Average Time (Minutes)")
plt.ylabel("Hospital Activity")
plt.grid(axis="x", alpha=0.2)
plt.bar_label(bars, fmt="%.1f", padding=4)
plt.tight_layout()

plt.savefig(
    "screenshots/average_waiting_time.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

# Chart 2: Maximum Waiting Time
max_df = df.sort_values(
    "Maximum_Waiting_Time",
    ascending=True
)

plt.figure(figsize=(11, 6))

bars = plt.barh(
    max_df["Activity_Name"],
    max_df["Maximum_Waiting_Time"],
    color="#0F766E"
)

plt.title(
    "CareFlow - Maximum Time Between Activities",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Maximum Time (Minutes)")
plt.ylabel("Hospital Activity")
plt.grid(axis="x", alpha=0.2)
plt.bar_label(bars, fmt="%.1f", padding=4)
plt.tight_layout()

plt.savefig(
    "screenshots/maximum_waiting_time.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nCharts generated successfully!")
print("1. screenshots/average_waiting_time.png")
print("2. screenshots/maximum_waiting_time.png")
