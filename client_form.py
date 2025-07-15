# client_form.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

client_log_path = "logs/client_attempts.csv"
os.makedirs("logs", exist_ok=True)

st.set_page_config(page_title="Client Input", layout="centered")
st.title("👥 Client Access Interaction")

with st.form("client_attempt_form"):
    bank = st.selectbox("Bank", ["Bank A", "Bank B", "Bank C"])
    incident_type = st.selectbox("Incident Type", ["Phishing", "Malware", "DDoS", "Data Breach", "Ransomware"])
    city = st.text_input("City")
    amount = st.number_input("Amount (MUR)", min_value=0)

    submitted = st.form_submit_button("Submit Attempt")

    if submitted:
        detected = "unauthorized" if amount > 400000 else "normal"
        new_attempt = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ClientID": "ManualEntry",
            "Bank": bank,
            "City": city,
            "Amount": amount,
            "Incident_Type": incident_type,
            "Detected_As": detected
        }

        if os.path.exists(client_log_path):
            df = pd.read_csv(client_log_path)
            df = pd.concat([df, pd.DataFrame([new_attempt])], ignore_index=True)
        else:
            df = pd.DataFrame([new_attempt])

        df.to_csv(client_log_path, index=False)
        st.success(f"Client attempt recorded and classified as '{detected}'.")
