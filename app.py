from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import uvicorn

app = FastAPI(title="Red-Alert ISRO Telemetry API")

# 1. Enable CORS so Next.js (port 3000) can fetch data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Load ML Assets & Test Data
print("Loading Engine & Simulating Stream...")
clf = joblib.load("models/rf_model.pkl")
scaler = joblib.load("models/scaler.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")

# Load the test event we want to stream
test_data = pd.read_csv("data/features_test.csv")
stream_data = test_data[test_data["event_id"] == "id_154"].reset_index(drop=True)
current_idx = 0

# 3. New Streaming Endpoint
@app.get("/next-frame")
def get_next_frame():
    global current_idx
    if current_idx >= len(stream_data):
        current_idx = 0 # Loop back to start if we run out of data
        
    row = stream_data.iloc[current_idx]
    
    # Predict
    X_live = pd.DataFrame([row[feature_cols]], columns=feature_cols)
    X_scaled = scaler.transform(X_live)
    prediction = int(clf.predict(X_scaled)[0])
    
    current_idx += 1
    
    # Send back only what the dashboard needs to draw the UI
    return {
        "time": str(row["datetime"]).split(" ")[1][:8], # Extract just HH:MM:SS
        "ch41": round(float(row["channel_41"]), 4),
        "isAnomaly": bool(prediction == 1)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)