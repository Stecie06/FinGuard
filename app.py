import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Bank Incident Monitoring", layout="wide")
st.title("📊 Cyber Threat Intelligence Dashboard")

# Load data
log_path = "logs/central_reports.csv"
alert_path = "logs/broadcast_alerts.csv"
client_log_path = "logs/client_attempts.csv"

if not os.path.exists(log_path):
    st.warning("No central log found. Run the AI monitoring first.")
    st.stop()

log_df = pd.read_csv(log_path)
alert_df = pd.read_csv(alert_path) if os.path.exists(alert_path) else pd.DataFrame()
client_df = pd.read_csv(client_log_path) if os.path.exists(client_log_path) else pd.DataFrame()

# Clean and prepare severity values for sidebar filter
severity_values = log_df["Predicted_Severity"].dropna().astype(str).unique().tolist()
severity_values = sorted(severity_values)

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_bank = st.sidebar.selectbox("Filter by Bank", ["All"] + sorted(log_df["Bank"].dropna().unique().tolist()))
selected_type = st.sidebar.selectbox("Filter by Incident Type", ["All"] + sorted(log_df["Incident_Type"].dropna().unique().tolist()))
selected_severity = st.sidebar.selectbox("Filter by Severity", ["All"] + severity_values)

# Filtering dataframe
filtered = log_df.copy()
if selected_bank != "All":
    filtered = filtered[filtered["Bank"] == selected_bank]
if selected_type != "All":
    filtered = filtered[filtered["Incident_Type"] == selected_type]
if selected_severity != "All":
    filtered = filtered[filtered["Predicted_Severity"].astype(str) == selected_severity]

# Central Reports
st.subheader("📄 Central Threat Reports")
st.dataframe(filtered.sort_values("Timestamp", ascending=False), use_container_width=True)

# Broadcast Alerts
st.subheader("🚨 Broadcast Alerts")
if alert_df.empty:
    st.info("No broadcast alerts generated yet.")
else:
    st.dataframe(alert_df.tail(10).sort_values("Timestamp", ascending=False), use_container_width=True)

# Client Attempt Logs
st.subheader("👥 Client Access Attempts")
if client_df.empty:
    st.info("No client access attempts recorded yet.")
else:
    st.dataframe(client_df.tail(15).sort_values("Timestamp", ascending=False), use_container_width=True)

# Live Alert Monitor
st.subheader("🔴 Live Alerts Monitor")
if not alert_df.empty:
    for i, row in alert_df.tail(5).iterrows():
        severity = row.get('Severity', 'Unknown')
        bank = row.get('Bank', 'Unknown Bank')
        timestamp = row.get('Timestamp', 'Unknown Time')
        incident = row.get('Incident_Type', 'Unknown Incident')
        
        color = "red" if severity == "Critical" else ("orange" if severity == "High" else "yellow")
        
        st.markdown(
            f"<div style='background-color:{color};padding:8px;border-radius:5px;margin:5px 0'>"
            f"<b>{timestamp} | {bank}</b>: {incident} - {severity}</div>",
            unsafe_allow_html=True
        )
else:
    st.success("✅ All clear. No critical incidents to broadcast.")
