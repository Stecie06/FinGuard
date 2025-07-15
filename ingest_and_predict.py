import pandas as pd
import joblib
from datetime import datetime
import os
import csv

# Load model and encoders
try:
    model = joblib.load("models/model_severity.pkl")
    severity_encoder = joblib.load("models/label_encoder_severity.pkl")
    incident_encoder = joblib.load("models/label_encoder_incident.pkl")
    city_encoder = joblib.load("models/label_encoder_city.pkl")
except Exception as e:
    print(f"❌ Error loading model or encoders: {e}")
    exit()

# Prepare log paths
client_log = "logs/client_attempts.csv"
central_log = "logs/central_reports.csv"
broadcast_log = "logs/broadcast_alerts.csv"

# Ensure output logs exist
for path, headers in [
    (central_log, ["Timestamp", "Bank", "City", "Amount", "Incident_Type", "Predicted_Severity"]),
    (broadcast_log, ["Timestamp", "Bank", "Incident_Type", "Predicted_Severity"])
]:
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(headers)

# Load logs
try:
    client_df = pd.read_csv(client_log)
    central_df = pd.read_csv(central_log)
except Exception as e:
    print(f"❌ Error reading CSVs: {e}")
    exit()

# Filter only unauthorized and unprocessed rows
already_processed = set(
    central_df["Timestamp"] + central_df["Bank"] + central_df["Incident_Type"]
)
new_attempts = client_df[
    (client_df["Detected_As"] == "unauthorized") &
    ~((client_df["Timestamp"] + client_df["Bank"] + client_df["Incident_Type"]).isin(already_processed))
]

# Process new attempts
for _, row in new_attempts.iterrows():
    try:
        # Handle unknown cities
        city = row["City"]
        if city not in city_encoder.classes_:
            print(f"⚠️ Skipped row with unseen city: '{city}'")
            continue

        # Create prediction input with proper column names
        X = pd.DataFrame([[
            2023,
            datetime.now().day,
            row["Amount"],
            incident_encoder.transform([row["Incident_Type"]])[0],
            city_encoder.transform([city])[0]
        ]], columns=["Year", "Day", "Amount_Lost_MUR", "Incident_Type", "City"])

        # Run prediction
        pred = model.predict(X)
        severity = severity_encoder.inverse_transform(pred)[0]

        # Log to central reports
        with open(central_log, "a", newline="") as f:
            csv.writer(f).writerow([
                row["Timestamp"], row["Bank"], row["City"],
                row["Amount"], row["Incident_Type"], severity
            ])

        # Broadcast alert if needed
        if severity in ["High", "Critical"]:
            with open(broadcast_log, "a", newline="") as f:
                csv.writer(f).writerow([
                    row["Timestamp"], row["Bank"], row["Incident_Type"], severity
                ])
            print(f"🚨 ALERT: {row['Bank']} - {row['Incident_Type']} - {severity}")
        else:
            print(f"✔️ {row['Bank']} incident logged as {severity}")

    except Exception as e:
        print(f"❌ Error processing row: {e}")

print("✅ Ingestion complete.")
