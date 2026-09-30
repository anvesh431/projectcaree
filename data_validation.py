import pandas as pd
import os

from pandas import DataFrame

# Load raw dataset
input_file = "data/raw/hospital_event_logs.csv"

df: DataFrame = pd.read_csv(input_file)

print("========== DATASET INFORMATION ==========")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("\nColumns:")
print(df.columns.tolist())


# 1. Missing value check
print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


# 2. Duplicate check
print("\n========== DUPLICATE RECORDS ==========")
duplicates = df.duplicated().sum()
print("Duplicate records:", duplicates)


# 3. Timestamp conversion
df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    errors="coerce"
)

invalid_timestamps = df["Timestamp"].isnull().sum()

print("\n========== TIMESTAMP VALIDATION ==========")
print("Invalid timestamps:", invalid_timestamps)


# 4. Case ID validation
invalid_case_ids = df["Case_ID"].isnull().sum()

print("\n========== CASE ID VALIDATION ==========")
print("Missing Case IDs:", invalid_case_ids)


# 5. Activity validation
valid_activities = [
    "Registration",
    "Triage",
    "Doctor Consultation",
    "X-Ray",
    "Lab Test",
    "Doctor Review",
    "Pharmacy",
    "Discharge"
]

invalid_activities = df[
    ~df["Activity_Name"].isin(valid_activities)
]

print("\n========== ACTIVITY VALIDATION ==========")
print("Invalid activities:", len(invalid_activities))


# 6. Remove invalid records
df = df.dropna(
    subset=["Case_ID", "Activity_Name", "Timestamp"]
)

df = df[
    df["Activity_Name"].isin(valid_activities)
]


# 7. Remove duplicate records
df = df.drop_duplicates()


# 8. Sort event log
df = df.sort_values(
    by=["Case_ID", "Timestamp"]
)


# 9. Save processed dataset
output_folder = "data/processed"

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = (
    "data/processed/"
    "cleaned_hospital_event_logs.csv"
)

df.to_csv(
    output_file,
    index=False
)


print("\n========== VALIDATION COMPLETE ==========")
print("Clean records:", len(df))
print("Processed dataset saved at:")
print(output_file)