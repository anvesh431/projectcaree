
import os
import pandas as pd
import matplotlib.pyplot as plt

print("========== PATIENT JOURNEY RISK VISUALIZATION ==========")

# Load reports generated in Commit #14
risk_file = "data/reports/patient_risk_analysis.csv"
summary_file = "data/reports/patient_risk_summary.csv"

if not os.path.exists(risk_file) or not os.path.exists(summary_file):
    print("ERROR: Risk analysis reports not found.")
    print("Run: python python/patient_risk_analysis.py")
    raise SystemExit(1)

df = pd.read_csv(risk_file)
summary = pd.read_csv(summary_file)

if df.empty or summary.empty:
    raise ValueError("Risk analysis reports are empty.")

required_columns = [
    "Journey_Risk_Level",
    "Journey_Time_Minutes"
]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing column: {column}")

# Consistent category ordering and colors
levels = ["Low", "Medium", "High"]
colors = {
    "Low": "#60A5FA",
    "Medium": "#2563EB",
    "High": "#1E3A8A"
}

# Create output directory
os.makedirs("screenshots", exist_ok=True)

# Chart 1: Risk Distribution
counts = (
    df["Journey_Risk_Level"]
    .value_counts()
    .reindex(levels, fill_value=0)
)

counts = counts[counts > 0]

plt.figure(figsize=(8, 7))

plt.pie(
    counts.values,
    labels=counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=[colors[level] for level in counts.index],
    wedgeprops={"edgecolor": "white", "linewidth": 2}
)

plt.title(
    "CareFlow - Patient Journey Duration Categories",
    fontsize=15,
    fontweight="bold"
)

plt.tight_layout()

plt.savefig(
    "screenshots/patient_risk_distribution.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

# Chart 2: Average Journey Time by Risk Level
average_df = (
    df.groupby("Journey_Risk_Level")["Journey_Time_Minutes"]
    .mean()
    .reindex(levels)
    .dropna()
)

plt.figure(figsize=(9, 6))

bars = plt.bar(
    average_df.index,
    average_df.values,
    color=[colors[level] for level in average_df.index],
    width=0.55
)

plt.title(
    "CareFlow - Average Journey Time by Category",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Journey Duration Category")
plt.ylabel("Average Journey Time (Minutes)")
plt.grid(axis="y", alpha=0.2)
plt.bar_label(bars, fmt="%.1f", padding=4)

plt.tight_layout()

plt.savefig(
    "screenshots/patient_risk_average_time.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()

print("\nCharts generated successfully!")
print("1. screenshots/patient_risk_distribution.png")
print("2. screenshots/patient_risk_average_time.png")
