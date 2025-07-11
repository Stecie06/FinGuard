import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import csv
import os

# Load model and label encoder
model = joblib.load('models/model_severity.pkl')
le_severity = joblib.load('models/label_encoder_severity.pkl')

st.title("🏦 Real-Time Threat Detection for Financial Institutions")

st.markdown("""
Enter incident details. If the AI predicts a significant threat,  
🛡️ **the system will automatically log it without requiring bank action.**
""")

# Input form
year = st.number_input("📅 Year", 2000, 2030, 2023)
day = st.number_input("📆 Day of Month", 1, 31, 15)
amount = st.number_input("💸 Amount Lost (MUR)", 0)
incident_type = st.selectbox("🚨 Incident Type", ['Phishing', 'Data Breach', 'Malware', 'DDoS', 'Ransomware'])
city = st.selectbox("🏙️ City", ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Ahmedabad'])

# Encode
incident_map = {'Phishing': 0, 'Data Breach': 1, 'Malware': 2, 'DDoS': 3, 'Ransomware': 4}
city_map = {'Mumbai': 0, 'Delhi': 1, 'Bangalore': 2, 'Kolkata': 3, 'Ahmedabad': 4}
features = [[year, day, amount, incident_map[incident_type], city_map[city]]]

# Predict and auto-report
if st.button("🧠 Predict & Auto-Report"):
    prediction = model.predict(features)
    severity = le_severity.inverse_transform(prediction)[0]

    st.warning(f"🔥 Predicted Severity: **{severity}**")

    # Automatically log if attack detected
    if severity in ['Medium', 'High', 'Critical']:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [now, year, day, amount, incident_type, city, severity]
        file_exists = os.path.exists("report.csv")

        with open("report.csv", "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Year', 'Day', 'Amount_Lost_INR', 'Incident_Type', 'City', 'Predicted_Severity'])
            writer.writerow(row)

        st.success("✅ Incident automatically reported.")
    else:
        st.info("🟢 No significant threat detected. No report logged.")

# Show report
if st.button("📄 View Logged Reports"):
    if os.path.exists("report.csv"):
        df = pd.read_csv("report.csv")
        st.dataframe(df)
    else:
        st.info("No incidents reported yet.")
