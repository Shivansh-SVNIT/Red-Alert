import pandas as pd
import joblib
import time
import sys

# Load the saved model assets
print("Loading Red-Alert Engine...")
clf = joblib.load("models/rf_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")

# Load the test features (simulating incoming data stream)
test_data = pd.read_csv("data/features_test.csv")

# Let's monitor a specific event that contains a failure
EVENT_TO_MONITOR = "id_154"
stream_data = test_data[test_data["event_id"] == EVENT_TO_MONITOR].reset_index(drop=True)

print(f"\n📡 ESTABLISHING CONNECTION TO SATELLITE TELEMETRY...")
print(f"▶️ STARTING LIVE STREAM FOR EVENT: {EVENT_TO_MONITOR}\n")
time.sleep(2)

print(f"{'TIMESTAMP':<25} | {'CH_41_VAL':<10} | {'PREDICTION STATUS'}")
print("-" * 65)

# Simulate live stream row by row
for index, row in stream_data.iterrows():
    # Extract the features in the exact order the model expects
    X_live = row[feature_cols].values.reshape(1, -1)
    X_live_scaled = scaler.transform(X_live)
    
    # Predict
    prediction = clf.predict(X_live_scaled)[0]
    
    timestamp = str(row["datetime"])
    ch41_val = round(row["channel_41"], 4)
    
    # Terminal UI formatting
    if prediction == 1:
        # RED alert for anomaly
        status = "\033[91m🚨 RED ALERT: ANOMALY DETECTED!\033[0m"
    else:
        # GREEN for normal
        status = "\033[92m✅ SYSTEM NORMAL\033[0m"
        
    print(f"{timestamp:<25} | {ch41_val:<10} | {status}")
    
    # Sleep to simulate the delay of incoming live data
    time.sleep(0.05)