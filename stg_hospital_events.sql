-- CareFlow Hospital Event Log Transformation
-- Standardizes raw hospital events for process mining

SELECT
    Case_ID,
    TRIM(Activity_Name) AS Activity_Name,
    TIMESTAMP(Timestamp) AS Timestamp

FROM
    `careflow_dataset.hospital_event_logs`

WHERE
    Case_ID IS NOT NULL
    AND Activity_Name IS NOT NULL
    AND Timestamp IS NOT NULL