import pandas as pd
import os

# Input and output paths
input_file = "data/processed/cleaned_hospital_event_logs.csv"
output_file = "data/processed/normalized_event_logs.csv"

# Load cleaned dataset
df = pd.read_csv(input_file)

print("========== EVENT LOG NORMALIZATION ==========")
print("Input records:", len(df))

# Convert timestamp to datetime
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

# Remove unnecessary spaces
df["Case_ID"] = df["Case_ID"].astype(str).str.strip()
df["Activity_Name"] = df["Activity_Name"].astype(str).str.strip()

# Remove invalid records
df = df.dropna(
    subset=["Case_ID", "Activity_Name", "Timestamp"]
)

# Remove duplicate events
df = df.drop_duplicates()

# Sort every patient's events chronologically
df = df.sort_values(
    by=["Case_ID", "Timestamp"]
)

# Add event sequence number for each patient
df["Event_Order"] = (
    df.groupby("Case_ID").cumcount() + 1
)

# Create output directory if required
os.makedirs(
    "data/processed",
    exist_ok=True
)

# Save normalized event log
df.to_csv(
    output_file,
    index=False
)

print("\nNormalization completed successfully!")
print("Total normalized records:", len(df))
print("Total patient cases:", df["Case_ID"].nunique())
print("Saved at:", output_file)

print("\nSample normalized events:")
print(df.head(15))