-- CareFlow Clinical Pathway Process Mining
-- BigQuery Event Log Schema

CREATE TABLE IF NOT EXISTS `careflow_dataset.hospital_event_logs`
(
    Case_ID STRING NOT NULL,
    Activity_Name STRING NOT NULL,
    Timestamp TIMESTAMP NOT NULL
);

-- Processed event log table

CREATE TABLE IF NOT EXISTS `careflow_dataset.cleaned_hospital_event_logs`
(
    Case_ID STRING NOT NULL,
    Activity_Name STRING NOT NULL,
    Timestamp TIMESTAMP NOT NULL
);