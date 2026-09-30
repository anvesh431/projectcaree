# CareFlow – Clinical Pathway Process Mining

## Project Overview

CareFlow is a healthcare process analytics project designed to
analyze hospital patient journeys using Process Mining.

Traditional dashboards mainly show average waiting times.
CareFlow analyzes the actual sequence of hospital events to
identify process bottlenecks, pathway deviations, and operational
inefficiencies.

---

## Project Objectives

- Generate realistic hospital EHR event logs
- Validate and clean hospital event data
- Normalize data for process mining
- Discover actual patient pathways using PM4Py
- Generate a Directly-Follows Graph (DFG)
- Calculate transition waiting times
- Identify hospital bottlenecks
- Perform clinical pathway conformance checking
- Build an interactive analytics dashboard

---

## Technology Stack

- Python
- Pandas
- PM4Py
- Graphviz
- Plotly
- Streamlit
- Google BigQuery Schema
- dbt Models
- Git & GitHub

---

## Event Log Structure

The process-mining dataset contains:

| Column | Description |
|---|---|
| Case_ID | Unique patient journey ID |
| Activity_Name | Hospital activity |
| Timestamp | Time when activity occurred |
| Event_Order | Sequence of patient events |

---

## Clinical Activities

The simulated hospital pathway contains:

1. Registration
2. Triage
3. Doctor Consultation
4. X-Ray
5. Lab Test
6. Doctor Review
7. Pharmacy
8. Discharge

---

## Project Workflow

Raw EHR Event Logs

↓

Data Validation & Cleaning

↓

Event Log Normalization

↓

BigQuery / dbt Transformation

↓

PM4Py Process Discovery

↓

Process Map Generation

↓

Bottleneck Analysis

↓

Conformance Checking

↓

Interactive Dashboard

---

## Current Dataset Results

- Total Patients: 100
- Total Events: 849
- Total Activities: 8
- Average Journey Time: 191.1 minutes
- Average Transition Time: 24.59 minutes
- Biggest Bottleneck: Pharmacy → Discharge
- Bottleneck Average Time: 26.9 minutes

---

## Process Mining

PM4Py is used to discover the actual hospital process from
timestamped patient event logs.

The project generates a Directly-Follows Graph showing the
relationships between hospital activities.

---

## Bottleneck Analysis

For each transition, the system calculates:

- Transition frequency
- Average transition time
- Minimum transition time
- Maximum transition time

This helps identify slow stages in the hospital workflow.

---

## Conformance Checking

The actual patient pathway is compared with the expected pathway:

Registration
→ Triage
→ Doctor Consultation
→ X-Ray
→ Lab Test
→ Doctor Review
→ Pharmacy
→ Discharge

Patient journeys containing additional, missing, or reordered
activities are identified as deviations.

---

## Dashboard

The interactive CareFlow dashboard displays:

- Total Patients
- Total Events
- Average Journey Time
- Average Transition Time
- Major Process Bottleneck
- Activity Frequency
- Transition Frequency
- Bottleneck Analysis
- Patient Journey Distribution
- Clinical Process Map
- Conformance Results

---

## Run the Project

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run app.py

---

## Project Structure

CareFlow-Clinical-Process-Mining/

- data/
  - raw/
  - processed/
  - dashboard/
- python/
- pm4py/
- dbt/
- sql/
- screenshots/
- app.py
- README.md
- requirements.txt

---

## Conclusion

CareFlow demonstrates how process mining can be used to analyze
hospital operations beyond traditional KPI dashboards.

The system reconstructs patient journeys from event logs,
identifies bottlenecks, detects pathway deviations, and presents
the results through an interactive analytics dashboard.
