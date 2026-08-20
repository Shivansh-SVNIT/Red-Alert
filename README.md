# 🛰️ Red-Alert

### Satellite Telemetry Anomaly Detection & Digital Twin

**🏆 SVNIT & SAC-ISRO Space Innovation Hackathon 2026**
**Team:** Red Alert | **Theme 3:** Smart Satellite Health Monitoring

Red-Alert is an end-to-end **machine learning + real-time monitoring system** for detecting anomalies and subsystem failures in satellite telemetry.

It combines **time-series feature engineering, event-aware sampling, Random Forest, FastAPI, and a Next.js digital-twin dashboard**.

---

## 🚀 Key Results

| Metric                |      Result |
| --------------------- | ----------: |
| Future Test Samples   | **328,556** |
| Future Failure Events |      **23** |
| Precision             |  **99.56%** |
| Recall                |   **67.6%** |
| PR-AUC                |  **0.9966** |
| Events Detected       | **23 / 23** |
| Event Detection Rate  |    **100%** |

> **100% event-level detection** means the system detected all 23 unseen future failure events.

---

## 🧠 Key Innovations

### 1. Zero Temporal Leakage

Instead of random splitting, anomaly events were split **chronologically**.

* **90 historical events → Training**
* **23 future events → Testing**

This ensures the model is evaluated on genuinely unseen future behavior.

### 2. Event-Aware Undersampling

Satellite anomalies are highly imbalanced. The pipeline balances training data across failure events so the model learns **general failure patterns instead of memorizing large events**.

### 3. Dual-Memory Features

The model uses two time windows:

* ⚡ **5-step window:** sudden changes, spikes, drops, derivatives
* 🕐 **60-step window:** long-term behavior and faulty steady states

**39 engineered features** are generated per timestamp.

### 4. Physical Insight

The top features were dominated by **60-step rolling standard deviation (`rolling_std_60`)**.

This suggests that changes in a subsystem's **long-term variability/noise profile** can be stronger failure indicators than its raw value.

---

## 🏗️ Architecture

```text
ESA Telemetry
      ↓
Feature Engineering
      ↓
Event-Aware Balancing
      ↓
Random Forest Model
      ↓
FastAPI Backend
      ↓
Next.js Digital Twin
      ↓
Real-Time Anomaly Alerts
```

---

## 🛠️ Tech Stack

**ML:** Python, Pandas, Scikit-Learn, Joblib
**Backend:** FastAPI, Uvicorn
**Frontend:** Next.js, React, Tailwind CSS, Recharts

---

## 📁 Project Structure

```text
📦 Red-Alert
├── 📂 data/
├── 📂 models/
├── 📂 red-alert-dashboard/
├── feature_engineering.py
├── balance_training_data.py
├── train_baseline.py
├── evaluate_events.py
├── export_model.py
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚡ Run the Prototype

### Backend

```bash
python app.py
```

API:

```text
http://localhost:8000
```

### Dashboard

```bash
cd red-alert-dashboard
npm install
npm run dev
```

Dashboard:

```text
http://localhost:3000
```

API Docs:

```text
http://localhost:8000/docs
```

---

## 📦 Dataset

**Source:** European Space Agency (ESA) Open Telemetry Data

Large raw telemetry files are excluded through `.gitignore`. A sample `features_test.csv` is included for the live dashboard demo.

---

## 📄 Hackathon Deliverables

* 📑 [Executive Summary](https://drive.google.com/file/d/1Jcat07HEHMyLIvVYmnwFT9wOcbuO5vvb/view?usp=sharing)
* 📘 [Technical Report](https://drive.google.com/file/d/1oDsflzK38ow0JPMBfNP28ahlqSjQlgD6/view?usp=sharing)
* 🎬 [Prototype Demo](https://drive.google.com/file/d/1aJlWDPMhaiVBeDdsoxNYgT4q2-x4aauZ/view?usp=sharing)

---

### 🛰️ Red-Alert

**From satellite telemetry to real-time spacecraft health monitoring.**

**Team Red Alert | SVNIT × SAC-ISRO | 2026**
