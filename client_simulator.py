# client_simulator.py
import pandas as pd
import random
from datetime import datetime
import os
import csv

CLIENT_LOG = "logs/client_attempts.csv"
os.makedirs("logs", exist_ok=True)

# Create log file if not exists
if not os.path.exists(CLIENT_LOG):
    with open(CLIENT_LOG, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "ClientID", "Bank", "City", "Amount", "Incident_Type", "Detected_As"])

banks = ["Bank A", "Bank B", "Bank C"]
cities = ["Mumbai", "Delhi", "Bangalore", "Ahmedabad"]
incidents = ["Phishing", "Data Breach", "Malware", "Ransomware"]

def generate_logs(n=50):
    rows = []
    for i in range(n):
        client_id = f"C{i+1}"
        bank = random.choice(banks)
        city = random.choice(cities)
        incident = random.choice(incidents)
        amount = random.randint(0, 600000)
        detected = "unauthorized" if amount > 400000 else "normal"

        rows.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            client_id, bank, city, amount, incident, detected
        ])

    with open(CLIENT_LOG, "a", newline="") as f:
        csv.writer(f).writerows(rows)

    print(f"✅ Simulated {n} client attempts.")

if __name__ == "__main__":
    generate_logs()
