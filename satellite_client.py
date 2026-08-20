import pandas as pd
import requests
import time
import joblib

print("🛰️ Satellite Transmission Array Initialized...")

# Load test data and feature columns to match API expectation
test_data = pd.read_csv("data/features_test.csv")
feature_cols = joblib.load("models/feature_cols.pkl")

# We will transmit the same failure event we tested locally
EVENT_TO_MONITOR = "id_154"
stream_data = test_data[test_data["event_id"] == EVENT_TO_MONITOR].reset_index(drop=True)

# Your FastAPI Ground Station URL
API_URL = "http://127.0.0.1:8000/predict"

print(f"▶️ STARTING DATA TRANSMISSION TO GROUND STATION FOR EVENT: {EVENT_TO_MONITOR}\n")
time.sleep(2)

print(f"{'TIMESTAMP':<25} | {'CH_41':<8} | {'GROUND STATION RESPONSE'}")
print("-" * 75)

try:
    for index, row in stream_data.iterrows():
        # Package exactly what the API expects into a JSON dictionary
        payload = {
            "features": row[feature_cols].to_dict()
        }
        
        # Transmit POST request over the local network to FastAPI
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            timestamp = str(row["datetime"])
            ch41_val = round(row["channel_41"], 4)
            
            # Print the API's response
            status_color = "\033[91m" if result["anomaly_flag"] else "\033[92m"
            print(f"{timestamp:<25} | {ch41_val:<8} | {status_color}{result['status']}\033[0m")
        else:
            print(f"Error {response.status_code}: {response.text}")
            break
            
        time.sleep(0.05) # Network delay simulation
        
except KeyboardInterrupt:
    print("\n🛑 Transmission manually stopped.")