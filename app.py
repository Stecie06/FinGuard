import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os
import csv

# Load AI model and label encoder
model = joblib.load("models/model_severity.pkl")
label_encoder = joblib.load("models/label_encoder_severity.pkl")

# Bank registry (you can expand this list)
banks = ["Bank of Africa", "Equity Bank", "EcoBank", "Standard Bank", "Access Bank"]

incident_types = ['Phishing', 'Data Breach', 'Malware', 'DDoS', 'Ransomware']
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Ahmedabad']
incident_map = {name: i for i, name in enumerate(incident_types)}
city_map = {name: i for i, name in enumerate(cities)}

# Streamlit UI
st.title("🔐 Central Bank Threat Intelligence & Incident Reporting System")

st.markdown("### 🏦 Report a Cyber Incident")

with st.form("incident_form"):
    bank_name = st.selectbox("Affected Institution", banks)
    year = st.number_input("Year", 2020, 2030, 2023)
    day = st.number_input("Day of the Month", 1, 31, 15)
    amount = st.number_input("Estimated Amount Lost (MUR)", 0)
    incident_type = st.selectbox("Type of Incident", incident_types)
    city = st.selectbox("City of Occurrence", cities)
    submitted = st.form_submit_button("Predict & Report Incident")

if submitted:
    encoded_input = [[
        year,
        day,
        amount,
        incident_map[incident_type],
        city_map[city]
    ]]
    pred = model.predict(encoded_input)
    severity = label_encoder.inverse_transform(pred)[0]

    st.warning(f"🔎 Predicted Severity: **{severity}**")

    full_log = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bank_name, year, day, amount, incident_type, city, severity]
    full_log_file = "central_reports.csv"
    if not os.path.exists(full_log_file):
        with open(full_log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Bank", "Year", "Day", "Amount_Lost_INR", "Incident_Type", "City", "Predicted_Severity"])
    with open(full_log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(full_log)

    # Broadcast alert if needed
    if severity in ['Medium', 'High', 'Critical']:
        broadcast_log = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bank_name, incident_type, severity]
        broadcast_file = "broadcast_alerts.csv"
        if not os.path.exists(broadcast_file):
            with open(broadcast_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Institution", "Incident_Type", "Severity"])
        with open(broadcast_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(broadcast_log)

        st.success("✅ Attack reported to Central Bank and broadcasted to other banks.")
    else:
        st.info("🟢 No major threat. Logged quietly for records.")

# Optional report views
st.markdown("---")
st.markdown("### 📄 Central Reports & Broadcast Log")

if st.button("📊 View Central Bank Report"):
    if os.path.exists("central_reports.csv"):
        df = pd.read_csv("central_reports.csv")
        st.dataframe(df)
    else:
        st.info("No reports yet.")

if st.button("📡 View Broadcast Alerts"):
    if os.path.exists("broadcast_alerts.csv"):
        df = pd.read_csv("broadcast_alerts.csv")
        st.dataframe(df)
    else:
        st.info("No alerts broadcasted yet.")