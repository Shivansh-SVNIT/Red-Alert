

```markdown
# 🛰️ Red-Alert: Satellite Telemetry Anomaly Detection

**Red-Alert** is a production-grade machine learning pipeline and real-time monitoring dashboard designed to detect subsystem failures in multivariate satellite telemetry data (inspired by ESA/ISRO operations). 

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

---

## 📦 Dataset: ESA Satellite Anomaly Data
* **Source:** European Space Agency (ESA)
* **Hosting:** Zenodo
* **Size:** ~3.5 GB (Raw Telemetry)
* **Note on Reproducibility:** Due to the massive 3.5 GB size of the raw spacecraft telemetry dataset, the `data/` directory is intentionally excluded from this repository via `.gitignore`. To run this pipeline from scratch, you must download the official ESA Satellite Anomaly Dataset from Zenodo, extract the multievent CSVs, and place them into the `/data` folder before executing the feature engineering script.

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

The repository is modularized into distinct pipeline stages. Clone the repository and run the scripts in the following order:

### Phase 1: Data Engineering & Model Training

**1. Feature Engineering**
Processes the raw chronological multievent data, calculating rolling means, standard deviations, and differentials for both short and long windows.
```bash
python feature_engineering.py

```

**2. Event-Aware Balancing**
Applies the undersampling strategy to the feature-engineered training data to achieve a balanced Normal/Anomaly ratio without breaking temporal bounds.

```bash
python balance_training_data.py

```

**3. Baseline Model Training & Evaluation**
Trains the Random Forest classifier on the balanced historical data and evaluates sample-level metrics on the untouched future test data.

```bash
python train_baseline.py

```

**4. Event-Level Evaluation**
Groups the continuous predictions back into their original events to verify if the alarm would have successfully triggered during each unique subsystem failure.

```bash
python evaluate_events.py

```

**5. Export Engine**
Packages the trained Random Forest model, the standard scaler, and feature metadata into `.pkl` files inside the `/models` directory for live inference.

```bash
python export_model.py

```

### Phase 2: Live Inference & Dashboard (Microservice)

**1. Start the Ground Station API (Backend)**
Spins up a FastAPI server that loads the exported ML models and exposes a `/next-frame` endpoint to stream real-time predictions.

```bash
python app.py

```

*API Documentation available at `http://localhost:8000/docs*`

**2. Launch the Control Room Dashboard (Frontend)**
Open a new terminal, navigate to the dashboard directory, and start the Next.js application. This fetches data from the FastAPI backend and visualizes the telemetry matrix-style in real-time.

```bash
cd red-alert-dashboard
npm install
npm run dev

```

*Dashboard available at `http://localhost:3000*`

---

## 📁 Repository Structure

```text
📦 Red-Alert
 ┣ 📂 data/                    # Raw & processed CSV datasets (Ignored in Git)
 ┣ 📂 models/                  # Exported .pkl ML models (Ignored in Git)
 ┣ 📂 red-alert-dashboard/     # Next.js Frontend UI
 ┃ ┣ 📂 src/app/
 ┃ ┃ ┗ 📜 page.tsx             # Main Control Room Dashboard Code
 ┣ 📜 feature_engineering.py   # Sliding window calculations
 ┣ 📜 balance_training_data.py # Undersampling logic
 ┣ 📜 train_baseline.py        # Model training
 ┣ 📜 evaluate_events.py       # 23/23 evaluation logic
 ┣ 📜 export_model.py          # Model packaging
 ┣ 📜 app.py                   # FastAPI Server
 ┣ 📜 README.md                # Project documentation
 ┗ 📜 .gitignore

```

```

```
