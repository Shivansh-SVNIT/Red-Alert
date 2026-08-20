```markdown
# 🛰️ Red-Alert: Satellite Telemetry Anomaly Detection & Digital Twin

**🏆 SVNIT & SAC-ISRO Space Innovation Hackathon 2026 Submission**  
**Team:** Red Alert | **Theme:** 3 - Smart Satellite Health Monitoring  

**Red-Alert** is a production-grade machine learning pipeline and real-time monitoring dashboard designed to detect subsystem failures in multivariate satellite telemetry data. 

Unlike standard anomaly detection tasks, satellite telemetry presents unique time-series challenges: extreme class imbalance, the risk of temporal data leakage, and "steady-state" anomalies that trick models into accepting faulty hardware states as normal. This project engineers a robust pipeline to solve these physical data challenges, achieving a **100% event-level detection rate** on strictly future, unseen data, and visualizes it through a live microservice architecture.

---

## 🛠️ Tech Stack
* **Machine Learning & Data Engineering:** Python, Pandas, Scikit-Learn, Joblib
* **Backend API (Microservice):** FastAPI, Uvicorn
* **Frontend Dashboard:** Next.js (React), Tailwind CSS, Recharts, Lucide-React

---

## 🧠 Key Engineering Challenges Solved

### 1. Zero Temporal Leakage (Chronological Splitting)
Randomly splitting time-series data causes future data to leak into the training set, leading to falsely high accuracies. 
* **Solution:** Isolated 113 valid anomaly events and split them strictly chronologically. The model is trained entirely on past historical events (90 events) and evaluated purely on unseen future events (23 events).

### 2. Severe Class Imbalance (~99% Anomaly Skew)
Anomalies in satellites can last for weeks, dwarfing the normal baseline data and causing models to trivially predict 'Anomaly' for everything.
* **Solution:** Implemented **Event-Aware Undersampling**. The pipeline dynamically caps and samples anomaly data evenly across all 90 training events, forcing the model to learn the generalized signature of a failure rather than memorizing one massive event. 

### 3. The "Steady-State" Trap (Physical Feature Engineering)
When a satellite component fails, the sensor reading often spikes and then settles into a new, faulty "steady state." Short-term ML models forget the baseline and accept the new faulty state as normal.
* **Solution:** Engineered dual-memory time-series features.
  * **Short-term memory (5-step window):** Captures sudden spikes/drops and derivatives (`diff`).
  * **Long-term memory (60-step window):** Provides a 1-hour historical context to prevent the model from normalizing sustained faulty states.
  * *Total Features:* 39 engineered features per timestamp.

---

## 📊 Feature Interpretation: How the Model Thinks
By extracting the Random Forest's feature importances, the pipeline revealed a critical physical insight about satellite hardware failures:
* The top 6 most important features were all **Long-Term Standard Deviations (`rolling_std_60`)**.
* **Insight:** When a satellite subsystem fails, its *noise profile and vibration/variability* change fundamentally. The model learned that tracking the variance of a sensor over an hour is a much stronger indicator of failure than just looking at the raw numerical mean.

---

## 📦 Dataset: ESA Satellite Anomaly Data
* **Source:** European Space Agency (ESA) Open Telemetry Data
* **Note on Reproducibility:** Due to the massive size of the raw spacecraft telemetry dataset, the heavy raw `.csv` files inside `data/` are excluded via `.gitignore`. However, a sample `features_test.csv` is included to power the live dashboard demo.

---

## 🚀 Final Evaluation Results

Tested on a highly imbalanced, strictly future dataset of 328,556 telemetry samples across 23 isolated failure events.

* **Sample-Level Performance:**
  * **Precision:** 0.9956
  * **Recall (Anomaly):** 67.6% (Significantly boosted by long-term memory windows)
  * **PR-AUC:** 0.9966

* **Event-Level Performance (Real-World Metric):**
  In a real satellite control room, the goal is to trigger an alarm during the failure window. 
  * **Score:** **23 out of 23 Events Detected**
  * **Catch Rate:** 100%

---

## ⚙️ Pipeline Architecture & How to Run

### Phase 1: Live Inference & Dashboard (Running the Prototype)

**1. Start the Ground Station API (Backend)**
Spins up a FastAPI server that loads the exported ML models and exposes a `/next-frame` endpoint to stream real-time predictions.
```bash
python app.py

```

*API Documentation available at `http://localhost:8000/docs*`

**2. Launch the Control Room Dashboard (Frontend)**
Open a new terminal, navigate to the dashboard directory, and start the Next.js application.

```bash
cd red-alert-dashboard
npm install
npm run dev

```

*Dashboard available at `http://localhost:3000*`

### Phase 2: Data Engineering & Model Training (Optional/Reproducibility)

1. **`feature_engineering.py`**: Calculates rolling means, standard deviations, and differentials for both short and long windows.
2. **`balance_training_data.py`**: Applies the undersampling strategy to achieve a balanced Normal/Anomaly ratio without breaking temporal bounds.
3. **`train_baseline.py`**: Trains the Random Forest classifier on historical data.
4. **`evaluate_events.py`**: Groups continuous predictions back into original events to verify subsystem failure detection.
5. **`export_model.py`**: Packages the trained models into the `/models` directory for live inference.

---

## 📁 Repository Structure

```text
📦 Red-Alert
 ┣ 📂 data/                    # Sample telemetry datasets for live stream
 ┣ 📂 models/                  # Exported .pkl ML models (Included for API)
 ┣ 📂 red-alert-dashboard/     # Next.js Digital Twin Frontend
 ┃ ┣ 📂 app/
 ┃ ┃ ┗ 📜 page.tsx             # Main Control Room Dashboard Code
 ┣ 📜 feature_engineering.py   # Sliding window calculations
 ┣ 📜 balance_training_data.py # Undersampling logic
 ┣ 📜 train_baseline.py        # Model training
 ┣ 📜 evaluate_events.py       # Event-level evaluation logic
 ┣ 📜 export_model.py          # Model packaging
 ┣ 📜 app.py                   # FastAPI Live Telemetry Server
 ┣ 📜 requirements.txt         # Python dependencies
 ┗ 📜 README.md                # Project documentation

```
