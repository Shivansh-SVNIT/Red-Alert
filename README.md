# 🛰️ Red-Alert

## Satellite Telemetry Anomaly Detection & Digital Twin

> **🏆 SVNIT & SAC-ISRO Space Innovation Hackathon 2026**
> **Team:** Red Alert
> **Theme 3:** Smart Satellite Health Monitoring

**Red-Alert** is an end-to-end machine learning and real-time monitoring system for detecting failures and abnormal behavior in multivariate satellite telemetry.

The system combines **time-series feature engineering, event-aware data balancing, Random Forest anomaly classification, FastAPI inference, and a Next.js digital-twin dashboard** to simulate a real satellite ground-control monitoring environment.

### 🎯 Why Red-Alert?

Satellite telemetry is not a normal classification problem.

Real spacecraft data introduces three major challenges:

* ⏱️ **Temporal dependency:** Future telemetry must never influence past training data.
* ⚖️ **Extreme imbalance:** Failure periods can be tiny compared with the full telemetry stream.
* 🛰️ **Steady-state failures:** A failed subsystem may settle into a new stable state that looks "normal" to a short-memory model.

**Red-Alert was designed specifically to address these problems.**

---

# 🚀 Key Results

| Metric                  |      Result |
| ----------------------- | ----------: |
| Future test samples     | **328,556** |
| Future failure events   |      **23** |
| Precision               |  **99.56%** |
| Recall                  |   **67.6%** |
| PR-AUC                  |  **0.9966** |
| Failure events detected | **23 / 23** |
| Event detection rate    |    **100%** |
| Engineered features     |      **39** |

> **Important:** The 100% figure refers to **event-level detection**, not sample-level recall.
> The system successfully triggered an alarm during all 23 unseen future failure events, while sample-level anomaly recall was 67.6%.

---

# 🧠 Core Engineering Innovations

## 1. Zero Temporal Leakage

### The Problem

A random train/test split is dangerous for time-series telemetry.

Imagine training on data from:

```text
January → February → March → April
```

and randomly placing some April samples into the training set while testing on March.

The model has effectively seen the future.

That produces unrealistic evaluation results.

### Our Solution

Red-Alert performs a **strict chronological event split**.

```text
Historical Events                         Future Events
      │                                         │
      ▼                                         ▼
┌─────────────────────────────┐      ┌─────────────────────┐
│      Training Dataset       │      │    Test Dataset     │
│                             │      │                     │
│       90 Events             │      │      23 Events      │
│                             │      │                     │
│      Past telemetry         │ ───► │   Future telemetry  │
└─────────────────────────────┘      └─────────────────────┘
```

The model learns only from historical failure events and is evaluated on completely unseen future events.

**Total valid anomaly events:** 113
**Training events:** 90
**Future test events:** 23

This makes the evaluation much closer to the real deployment scenario:

> **Train on yesterday's spacecraft behavior → detect tomorrow's failures.**

---

# ⚖️ 2. Event-Aware Undersampling

Satellite anomaly datasets can be extremely imbalanced.

Our raw telemetry contains approximately:

```text
Normal     █████████████████████████████████████████████  ~99%
Anomaly    █                                               ~1%
```

However, simply undersampling anomalies randomly can cause another problem: the model may see too many samples from a few large failure events and memorize those specific patterns.

### Our Solution

We perform **event-aware undersampling**.

Instead of treating every anomaly sample equally:

```text
Anomaly Dataset
      │
      ├── Event 1
      ├── Event 2
      ├── Event 3
      ├── ...
      └── Event 90
              │
              ▼
      Balanced sampling
              │
              ▼
      Training dataset
```

Samples are selected across the historical failure events so that the model learns **general failure characteristics**, rather than memorizing one unusually long anomaly.

---

# 🧠 3. Dual-Memory Time-Series Features

One of the biggest challenges in satellite anomaly detection is the **steady-state failure problem**.

Consider a sensor:

```text
Normal
  │
  │
  │        Failure
  │          ↓
  │        ╱─────── Faulty steady state
  │      ╱
  │─────╯
  │
  └──────────────────────────► Time
```

A short-memory model may see the sensor becoming stable again and conclude:

> "The sensor is stable, so everything is normal."

But physically, the sensor has stabilized at a **faulty operating condition**.

### Our Solution

Red-Alert gives the model two different memories.

### ⚡ Short-Term Memory

**5-step window**

Captures:

* Sudden spikes
* Sudden drops
* Local trends
* Rapid changes
* First-order differences (`diff`)

### 🕐 Long-Term Memory

**60-step window**

Captures:

* Historical baseline
* Long-term variation
* Sustained changes
* Changes in sensor behavior
* Faulty steady-state conditions

Together:

```text
                    Current Sensor
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       Short-Term Memory       Long-Term Memory
          5 steps                  60 steps
              │                       │
              ▼                       ▼
       Sudden Changes          Historical Context
              │                       │
              └───────────┬───────────┘
                          ▼
                   ML Feature Vector
                          │
                          ▼
                  Random Forest Model
                          │
                          ▼
                Normal / Anomaly
```

This produces **39 engineered features per timestamp**.

---

# 📊 What Did the Model Actually Learn?

Feature importance analysis provided an interesting physical insight.

The **six most important features** were all based on:

```text
rolling_std_60
```

In other words, long-term variability was more informative than simply looking at the raw sensor value.

### Why is this important?

A healthy subsystem may have a relatively consistent noise pattern.

When hardware begins failing:

```text
Healthy
Small, consistent variation
       ↓
       📈
       📉
       📈


Faulty
Higher / different variability
       ↓
    📈     📉
  📉    📈     📉
       📈
```

The absolute sensor value may eventually look stable.

But its **noise and variability profile can remain different**.

This means the model discovered a potentially useful physical signature:

> **Failure is not always about where the sensor value is. It can also be about how the sensor behaves over time.**

---

# 🤖 Machine Learning Pipeline

```text
             ESA Telemetry
                    │
                    ▼
          Data Cleaning & Parsing
                    │
                    ▼
       Chronological Event Splitting
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
     Historical Data      Future Data
          │                   │
          ▼                   │
   Event-Aware Sampling       │
          │                   │
          ▼                   │
   Feature Engineering        │
          │                   │
          ├──────────────┐    │
          │              │    │
          ▼              ▼    │
     5-Step Window   60-Step Window
          │              │    │
          └──────┬───────┘    │
                 ▼            │
           39 Features        │
                 │            │
                 ▼            │
          Random Forest       │
                 │            │
                 └──────┐     │
                        ▼     ▼
                    Evaluation
                        │
                        ▼
                 Event-Level Check
                        │
                        ▼
                  23 / 23 Detected
```

---

# 📈 Evaluation

The final model was evaluated on a **strictly future, unseen dataset** containing:

* **328,556 telemetry samples**
* **23 isolated failure events**

## Sample-Level Performance

| Metric    |      Score |
| --------- | ---------: |
| Precision | **0.9956** |
| Recall    |  **0.676** |
| PR-AUC    | **0.9966** |

The high precision means that when the system raises an anomaly alarm, it is very likely to correspond to an actual anomaly.

---

## 🚨 Event-Level Performance

For spacecraft monitoring, sample-level recall is not the only metric that matters.

Suppose a failure lasts for 1,000 telemetry points and the model detects only 100 of them.

Sample recall may not be perfect.

But if those 100 detections occur **inside the actual failure window**, the ground-control team still receives the critical warning.

Therefore, Red-Alert also evaluates predictions at the **event level**.

### Result

```text
Future Failure Events

Event 01  ✅
Event 02  ✅
Event 03  ✅
   ...
Event 22  ✅
Event 23  ✅

Detected: 23 / 23
Catch Rate: 100%
```

> **100% event-level detection on 23 unseen future failure events.**

---

# 🛰️ Digital Twin & Real-Time Monitoring

The trained model is exported and served through a lightweight FastAPI microservice.

The frontend consumes telemetry frames from the API and visualizes the spacecraft state through a **Next.js control-room dashboard**.

```text
┌──────────────────────────┐
│     Satellite Telemetry  │
│          Stream          │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       FastAPI API        │
│                          │
│  /next-frame             │
│                          │
│  Model Inference         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Next.js Dashboard    │
│                          │
│  Telemetry               │
│  Anomaly Status           │
│  Charts                   │
│  Alerts                   │
│  Digital Twin             │
└──────────────────────────┘
```

This separates the system into two independent services:

### Backend

**FastAPI + Python**

Responsible for:

* Loading ML models
* Processing telemetry
* Generating predictions
* Streaming the next telemetry frame
* Exposing API endpoints

### Frontend

**Next.js + React**

Responsible for:

* Real-time visualization
* Satellite health indicators
* Telemetry charts
* Anomaly alerts
* Digital-twin interface

---

# 🛠️ Technology Stack

### Machine Learning

* Python
* Pandas
* Scikit-Learn
* Joblib

### Backend

* FastAPI
* Uvicorn

### Frontend

* Next.js
* React
* Tailwind CSS
* Recharts
* Lucide React

### Architecture

```text
        ┌───────────────────────┐
        │    Python ML Layer    │
        │                       │
        │ Pandas + Scikit-Learn │
        └───────────┬───────────┘
                    │
                    ▼
             Exported Models
                    │
                    ▼
        ┌───────────────────────┐
        │      FastAPI API      │
        │       Port 8000       │
        └───────────┬───────────┘
                    │
                  HTTP
                    │
                    ▼
        ┌───────────────────────┐
        │     Next.js UI        │
        │       Port 3000       │
        └───────────────────────┘
```

---

# 📦 Dataset

### ESA Satellite Anomaly Dataset

**Source:** European Space Agency (ESA) Open Telemetry Data

The original telemetry dataset is extremely large.

For repository size and reproducibility considerations:

* Large raw CSV files are excluded through `.gitignore`
* A smaller `features_test.csv` sample is included
* Exported ML models are included for live inference
* The dashboard can therefore be demonstrated without downloading the complete raw dataset

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Red-Alert
```

---

# ⚡ Run the Live Prototype

## Step 1: Start the Ground Station API

The FastAPI backend loads the exported models and provides real-time predictions.

```bash
python app.py
```

The API will run on:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

## Step 2: Start the Digital Twin Dashboard

Open another terminal:

```bash
cd red-alert-dashboard
npm install
npm run dev
```

The dashboard will be available at:

```text
http://localhost:3000
```

---

# 🧪 Model Training Pipeline

Training is optional if you only want to run the prototype.

The complete ML pipeline consists of five stages.

### 1. `feature_engineering.py`

Creates time-series features including:

* Rolling mean
* Rolling standard deviation
* Differential features
* Short-term windows
* Long-term windows

---

### 2. `balance_training_data.py`

Performs event-aware undersampling while preserving the chronological boundaries of the training data.

---

### 3. `train_baseline.py`

Trains the Random Forest anomaly classifier using the engineered training dataset.

---

### 4. `evaluate_events.py`

Converts timestamp-level predictions back into failure events and evaluates whether each unseen failure event was detected.

---

### 5. `export_model.py`

Exports the trained model and preprocessing components into the `models/` directory for deployment.

---

# 📁 Repository Structure

```text
📦 Red-Alert
│
├── 📂 data/
│   └── features_test.csv
│
├── 📂 models/
│   └── *.pkl
│
├── 📂 red-alert-dashboard/
│   ├── 📂 app/
│   │   └── 📜 page.tsx
│   ├── 📂 components/
│   └── 📜 package.json
│
├── 📜 feature_engineering.py
├── 📜 balance_training_data.py
├── 📜 train_baseline.py
├── 📜 evaluate_events.py
├── 📜 export_model.py
├── 📜 app.py
├── 📜 requirements.txt
├── 📜 .gitignore
└── 📜 README.md
```

---

# 🎥 Hackathon Deliverables

### 📄 Executive Summary

[View Executive Summary](https://drive.google.com/file/d/1Jcat07HEHMyLIvVYmnwFT9wOcbuO5vvb/view?usp=sharing)

### 📑 Technical Report

[View Technical Report](https://drive.google.com/file/d/1oDsflzK38ow0JPMBfNP28ahlqSjQlgD6/view?usp=sharing)

### 🎬 Working Prototype Demo

[Watch Prototype Demo](https://drive.google.com/file/d/1aJlWDPMhaiVBeDdsoxNYgT4q2-x4aauZ/view?usp=sharing)

---

# 💡 Why This Approach Matters

Traditional anomaly detection often asks:

> **"Is this telemetry point unusual?"**

Red-Alert asks a more useful question:

> **"Does the current behavior indicate that a spacecraft subsystem is moving away from its historical healthy behavior?"**

That difference is important.

The system combines:

**Current behavior**
+
**Short-term changes**
+
**Long-term historical context**
+
**Event-level reasoning**

to produce a more realistic satellite health-monitoring pipeline.

---

# 🏁 Final Takeaway

Red-Alert demonstrates an end-to-end approach to spacecraft anomaly detection:

```text
Raw Telemetry
      ↓
Temporal-Safe Dataset
      ↓
Event-Aware Balancing
      ↓
Dual-Memory Features
      ↓
Random Forest
      ↓
Future-Unseen Evaluation
      ↓
23 / 23 Failure Events Detected
      ↓
FastAPI Inference
      ↓
Next.js Digital Twin
```

### 🛰️ From telemetry data to a simulated satellite control room.

**Built for the SVNIT & SAC-ISRO Space Innovation Hackathon 2026.**

---

## 👥 Team

**Team Red Alert**

**Theme:** Smart Satellite Health Monitoring
**Institution:** SVNIT
**Hackathon:** SVNIT & SAC-ISRO Space Innovation Hackathon 2026
