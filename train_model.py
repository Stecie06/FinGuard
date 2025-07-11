import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1. Load the dataset
df = pd.read_csv('data/cybersecurity_cases_india_combined.csv')

# 2. Encode text fields into numbers
le_type = LabelEncoder()
le_city = LabelEncoder()
le_severity = LabelEncoder()

df['Incident_Type'] = le_type.fit_transform(df['Incident_Type'])
df['City'] = le_city.fit_transform(df['City'])
df['Severity'] = le_severity.fit_transform(df['Severity'])

# 3. Save label encoder (to decode predictions later)
joblib.dump(le_severity, 'models/label_encoder_severity.pkl')

# 4. Select features and label
X = df[['Year', 'Day', 'Amount_Lost_INR', 'Incident_Type', 'City']]
y = df['Severity']

# 5. Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 7. Save the model
joblib.dump(model, 'models/model_severity.pkl')
print("✅ Model trained and saved.")

# 8. Evaluate model
y_pred = model.predict(X_test)
print("\n📊 Severity Prediction Report:\n")
print(classification_report(y_test, y_pred))
