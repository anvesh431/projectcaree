
import os
import pandas as pd
import matplotlib.pyplot as plt

print("========== PATIENT JOURNEY VISUALIZATION ==========")

# Load files generated in Commit #18
comparison_file = "data/reports/patient_journey_comparison.csv"
top_file = "data/reports/top_10_longest_journeys.csv"

if not os.path.exists(comparison_file):
    raise FileNotFoundError(
        "Run: python python/patient_journey_comparison.py"
    )

if not os.path.exists(top_file):
    raise FileNotFoundError(
        "Top 10 journey report not found."
    )

df = pd.read_csv(comparison_file)
top_10 = pd.read_csv(top_file)

required_columns = [
    "Case_ID",
    "Journey_Time_Minutes",
    "Journey_Performance"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

if df.empty or top_10.empty:
    raise ValueError("Journey data is empty.")

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

# CHART 1: Top 10 longest journeys
top_10 = top_10.sort_values(
    "Journey_Time_Minutes",
    ascending=True
)

plt.figure(figsize=(11, 6))

bars = plt.barh(
    top_10["Case_ID"].astype(str),
    top_10["Journey_Time_Minutes"],
    color="#2563EB"
)

plt.title(
    "CareFlow - Top 10 Longest Patient Journeys",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Journey Duration (Minutes)")
plt.ylabel("Patient Case ID")
plt.grid(axis="x", alpha=0.2)
plt.bar_label(bars, fmt="%.1f", padding=4)
plt.tight_layout()

plt.savefig(
    "screenshots/top_10_patient_journeys.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

# CHART 2: Journey duration comparison
counts = df["Journey_Performance"].value_counts()

plt.figure(figsize=(9, 6))

colors = [
    "#1E3A8A" if "Above" in label
    else "#60A5FA" if "Below" in label
    else "#94A3B8"
    for label in counts.index
]

bars = plt.bar(
    counts.index,
    counts.values,
    color=colors,
    width=0.55
)

plt.title(
    "CareFlow - Patient Journey Duration Comparison",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Journey Duration Category")
plt.ylabel("Number of Patients")
plt.xticks(rotation=10)
plt.grid(axis="y", alpha=0.2)
plt.bar_label(bars, fmt="%.0f", padding=4)
plt.tight_layout()

plt.savefig(
    "screenshots/patient_journey_comparison.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nCharts generated successfully!")
print("1. screenshots/top_10_patient_journeys.png")
print("2. screenshots/patient_journey_comparison.png")
