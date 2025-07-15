# 🔐 Secure Threat Intelligence Sharing and Incident Reporting System

A secure, AI-powered platform for real-time cyber incident detection, reporting, and intelligence sharing among financial institutions. Built for the Central Bank to automatically detect threats, classify severity, log attacks, and alert all connected institutions without manual reporting.

---

## 📁 Project Structure

```
ai_threat_detector/
├── data/                          # Training dataset
│   └── threat_dataset_bank_only.csv
├── logs/                          # All logs (auto-generated)
│   ├── central_reports.csv        # AI-reported confirmed threats
│   ├── broadcast_alerts.csv       # Alerts shared with other institutions
│   └── client_attempts.csv        # Raw client interaction logs
├── models/                        # Trained ML models and encoders
│   ├── model_severity.pkl
│   ├── label_encoder_*.pkl
├── train_model.py                # Model training script
├── client_simulator.py           # Simulates real/suspicious client interactions
├── ingest_and_predict.py         # AI classifies threats from new data
└── dashboard.py                  # Streamlit dashboard for live monitoring
```

---

## ⚙️ Features

### 🔍 AI Threat Prediction

* Trains on real banking incidents
* Detects severity: Low → Critical
* Continuously improves through online learning

### 🛡️ Autonomous Threat Response

* Logs attacks centrally
* Broadcasts alerts to all institutions
* Flags unauthorized client behavior

### 📊 Real-Time Monitoring

* Filters by bank, incident type, severity
* Live alerts & client activity
* Auto-refresh-ready dashboard (Streamlit)

---

## 🚀 How to Run

### 1. Train the Model

```bash
python train_model.py
```

### 2. Simulate Clients

```bash
python client_simulator.py
```

### 3. Run AI Threat Detection

```bash
python ingest_and_predict.py
```

### 4. Launch Dashboard

```bash
streamlit run dashboard.py
```

---

## 🔁 Optional Add-ons

* Online Learning: Supports `partial_fit()` using `SGDClassifier`
* REST API: Can be extended using FastAPI/Flask
* Auto Data Sync: Add CRON jobs to run prediction hourly

---

## 🤖 Built With

* Python
* Pandas, NumPy, Scikit-learn
* Streamlit
* Joblib

---

## 📌 Use Case

> Built for a Central Bank to monitor cybersecurity threats across multiple banks, prevent downtime, and initiate coordinated responses automatically.

---

## 👤 Author

**Stecie Niyonzima**
\[Software Engineer | AI for Cybersecurity Advocate]
