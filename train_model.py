# 💡 PART 1: TRAIN THE AI MODEL
# File: train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("data/threat_dataset_bank_only.csv")

# Encode categorical features
incident_encoder = LabelEncoder()
city_encoder = LabelEncoder()
severity_encoder = LabelEncoder()

df['Incident_Type'] = incident_encoder.fit_transform(df['Incident_Type'])
df['City'] = city_encoder.fit_transform(df['City'])
df['Severity'] = severity_encoder.fit_transform(df['Severity'])

# Features and target
X = df[['Year', 'Day', 'Amount_Lost_INR', 'Incident_Type', 'City']]
y = df['Severity']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model and encoders
joblib.dump(model, "models/model_severity.pkl")
joblib.dump(severity_encoder, "models/label_encoder_severity.pkl")

print("✅ Model trained and saved.")
