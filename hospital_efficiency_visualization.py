
import os
import pandas as pd
import matplotlib.pyplot as plt

print("========== HOSPITAL EFFICIENCY VISUALIZATION ==========")

# Load hospital efficiency report
file_path = "data/reports/hospital_efficiency.csv"

if not os.path.exists(file_path):
    print("ERROR: Hospital efficiency report not found.")
    print("First run: python python/hospital_efficiency.py")
    raise SystemExit(1)

df = pd.read_csv(file_path)

required_columns = [
    "Activity_Name",
    "Next_Activity",
    "Average_Time_Minutes",
    "Total_Transitions"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

df["Average_Time_Minutes"] = pd.to_numeric(
    df["Average_Time_Minutes"],
    errors="coerce"
)

df = df.dropna(subset=["Average_Time_Minutes"])

if df.empty:
    raise ValueError("No valid efficiency data found.")

# Create transition labels
df["Transition"] = (
    df["Activity_Name"].astype(str)
    + " → "
    + df["Next_Activity"].astype(str)
)

# Select top 10 slowest transitions
top_10 = df.nlargest(
    10,
    "Average_Time_Minutes"
).sort_values("Average_Time_Minutes")

# Create output folder
os.makedirs("screenshots", exist_ok=True)

# Chart 1: Slowest hospital transitions
plt.figure(figsize=(12, 7))

bars = plt.barh(
    top_10["Transition"],
    top_10["Average_Time_Minutes"],
    color="#2563EB"
)

plt.title(
    "CareFlow - Top 10 Slowest Hospital Transitions",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Average Transition Time (Minutes)")
plt.ylabel("Hospital Activity Transition")

plt.grid(axis="x", alpha=0.2)
plt.bar_label(bars, fmt="%.1f", padding=4)
plt.tight_layout()

plt.savefig(
    "screenshots/hospital_efficiency_chart.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

# Chart 2: Transition frequency
frequency = df.nlargest(
    10,
    "Total_Transitions"
).sort_values("Total_Transitions")

plt.figure(figsize=(12, 7))

bars = plt.barh(
    frequency["Transition"],
    frequency["Total_Transitions"],
    color="#0F766E"
)

plt.title(
    "CareFlow - Most Frequent Hospital Transitions",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Transitions")
plt.ylabel("Hospital Activity Transition")

plt.grid(axis="x", alpha=0.2)
plt.bar_label(bars, fmt="%.0f", padding=4)
plt.tight_layout()

plt.savefig(
    "screenshots/hospital_transition_frequency.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nCharts generated successfully!")
print("1. screenshots/hospital_efficiency_chart.png")
print("2. screenshots/hospital_transition_frequency.png")
