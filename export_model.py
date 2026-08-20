import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# 1. This line automatically creates the 'models' folder if it doesn't exist!
os.makedirs("models", exist_ok=True)

print("Loading balanced training data...")
train = pd.read_csv("data/balanced_features_train.csv")

exclude_cols = ["datetime", "event_id", "label"]
feature_cols = [col for col in train.columns if col not in exclude_cols]

X_train, y_train = train[feature_cols], train["label"]

print("Scaling and Training the Final Random Forest Engine...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train_scaled, y_train)

print("Exporting model and scaler to /models directory...")
# Save the model and scaler
joblib.dump(clf, "models/rf_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

# Save the feature column names so our API/Inference knows the exact order
joblib.dump(feature_cols, "models/feature_cols.pkl")

print("✅ EXPORT COMPLETE! Model is ready for live inference.")