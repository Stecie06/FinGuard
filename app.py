import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import csv
import os

# Load trained model and label encoder
model = joblib.load('models/model_severity.pkl')
le_severity = joblib.load('models/label_encoder_severity.pkl')

st.title("🏦 Secure Banking Cyber Incident Reporter")

st.markdown("Use this tool to log incidents and predict the threat severity.")

# Input form
year = st.number_input("📅 Year", 2000, 2030, 2023)
day = st.number_input("📆 Day of Month", 1, 31, 15)
amount = st.number_input("💸 Amount Lost (MUR)", 0)
incident_type = st.selectbox("🚨 Incident Type", ['Phishing', 'Data Breach', 'Malware', 'DDoS', 'Ransomware'])
city = st.selectbox("🏙️ City", ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Ahmedabad'])

# Encode input
incident_map = {'Phishing': 0, 'Data Breach': 1, 'Malware': 2, 'DDoS': 3, 'Ransomware': 4}
city_map = {'Mumbai': 0, 'Delhi': 1, 'Bangalore': 2, 'Kolkata': 3, 'Ahmedabad': 4}
features = [[year, day, amount, incident_map[incident_type], city_map[city]]]

# Predict severity
if st.button("🧠 Predict Severity"):
    prediction = model.predict(features)
    severity = le_severity.inverse_transform(prediction)[0]

    st.warning(f"🔥 Predicted Severity: **{severity}**")

    # Log prediction
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [now, year, day, amount, incident_type, city, severity]
    exists = os.path.exists("report.csv")
    with open('report.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['Timestamp', 'Year', 'Day', 'Amount', 'Incident_Type', 'City', 'Predicted_Severity'])
        writer.writerow(row)

# View log
if st.button("📄 View Reports"):
    if os.path.exists("report.csv"):
        df = pd.read_csv("report.csv")
        st.dataframe(df)
    else:
        st.info("No reports yet.")
