# 🛰️ Red-Alert: Satellite Telemetry Anomaly Detection

**Red-Alert** is a production-grade machine learning pipeline designed to detect subsystem failures in multivariate satellite telemetry data (inspired by ESA/ISRO operations). 

Unlike standard anomaly detection tasks, satellite telemetry presents unique time-series challenges: extreme class imbalance, the risk of temporal data leakage, and "steady-state" anomalies that trick models into accepting faulty hardware states as normal. This project engineers a robust pipeline to solve these physical data challenges, achieving a **100% event-level detection rate** on strictly future, unseen data.

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

## 🛠️ Pipeline Architecture & How to Run

The repository is modularized into distinct pipeline stages. To replicate the results, run the scripts in the following order:

### 1. Feature Engineering
Processes the raw chronological multievent data, calculating rolling means, standard deviations, and differentials for both short (5-step) and long (60-step) windows.
```bash
python feature_engineering.py