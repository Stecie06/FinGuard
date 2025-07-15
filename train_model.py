import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
import joblib

# Create models directory
os.makedirs("models", exist_ok=True)

# Load the dataset
df = pd.read_csv("data/cybersecurity_cases_india_combined.csv")

# Encode categorical variables
incident_encoder = LabelEncoder()
city_encoder = LabelEncoder()
severity_encoder = LabelEncoder()

incident_encoder.fit(df['Incident_Type'])
city_encoder.fit(df['City'])
severity_encoder.fit(df['Severity'])

# Transform columns
df['Incident_Type'] = incident_encoder.transform(df['Incident_Type'])
df['City'] = city_encoder.transform(df['City'])
df['Severity'] = severity_encoder.transform(df['Severity'])

# Define features and target
X = df[['Year', 'Day', 'Amount_Lost_MUR', 'Incident_Type', 'City']]
y = df['Severity']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create pipeline
pipeline = Pipeline([
    ('smote', SMOTE(random_state=42)),
    ('rf', RandomForestClassifier(random_state=42))
])

# Parameter tuning
param_dist = {
    'rf__n_estimators': [100, 300, 500],
    'rf__max_depth': [None, 10, 20, 30],
    'rf__min_samples_split': [2, 5, 10],
    'rf__min_samples_leaf': [1, 2, 4],
    'rf__max_features': ['sqrt', 'log2']
}

random_search = RandomizedSearchCV(
    pipeline,
    param_distributions=param_dist,
    n_iter=20,
    scoring='accuracy',
    cv=5,
    verbose=2,
    random_state=42,
    n_jobs=-1
)

# Train model
random_search.fit(X_train, y_train)

# Evaluate
print("\nTest Set Report:")
y_pred = random_search.predict(X_test)
print(classification_report(y_test, y_pred, zero_division=0))

# Save model and encoders
joblib.dump(random_search.best_estimator_, "models/model_severity.pkl")
joblib.dump(severity_encoder, "models/label_encoder_severity.pkl")
joblib.dump(incident_encoder, "models/label_encoder_incident.pkl")
joblib.dump(city_encoder, "models/label_encoder_city.pkl")

print("\n✅ Model and encoders saved successfully.")
