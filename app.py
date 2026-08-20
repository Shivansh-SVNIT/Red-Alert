from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import uvicorn
import numpy as np
import os

app = FastAPI(title="Red-Alert ISRO Telemetry API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading Engine & Telemetry Stream...")
clf = joblib.load("models/rf_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")

test_data = pd.read_csv("data/features_test.csv")
stream_data = test_data[test_data["event_id"] == "id_154"].reset_index(drop=True)
current_idx = 0

@app.get("/")
def root():
    return {"status": "ISRO Telemetry Stream Active"}

@app.get("/next-frame")
def get_next_frame():
    global current_idx
    if current_idx >= len(stream_data):
        current_idx = 0  # Loop back
        
    row = stream_data.iloc[current_idx]
    
    # ML Prediction & Probability
    X_live = pd.DataFrame([row[feature_cols]], columns=feature_cols)
    X_scaled = scaler.transform(X_live)
    prediction = int(clf.predict(X_scaled)[0])
    
    # Calculate anomaly probability if model supports it
    if hasattr(clf, "predict_proba"):
        risk_score = round(float(clf.predict_proba(X_scaled)[0][1]) * 100, 1)
    else:
        risk_score = 98.4 if prediction == 1 else 3.2
    
    current_idx += 1
    
    # Extract multiple channels if available, else derive nominal subsystem values
    ch41_val = round(float(row.get("channel_41", 0.80)), 4)
    temp_val = round(24.5 + (ch41_val - 0.80) * 120 + np.random.uniform(-0.3, 0.3), 2)
    bus_volt = round(28.2 + (ch41_val - 0.80) * 8 + np.random.uniform(-0.05, 0.05), 2)
    gyro_drift = round(0.012 + (0.08 if prediction == 1 else 0.0) + np.random.uniform(-0.002, 0.002), 4)

    return {
        "time": str(row["datetime"]).split(" ")[1][:8],
        "ch41": ch41_val,
        "temperature": temp_val,
        "busVoltage": bus_volt,
        "gyroDrift": gyro_drift,
        "riskScore": risk_score,
        "isAnomaly": bool(prediction == 1),
        "frameIndex": current_idx
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)