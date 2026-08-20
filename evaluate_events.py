import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

print("Loading datasets...")
train = pd.read_csv("data/balanced_features_train.csv")
test = pd.read_csv("data/features_test.csv")

# Prepare features
exclude_cols = ["datetime", "event_id", "label"]
feature_cols = [col for col in train.columns if col not in exclude_cols]

X_train, y_train = train[feature_cols], train["label"]
X_test, y_test = test[feature_cols], test["label"]

print("Scaling and Training Random Forest (hang tight)...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train_scaled, y_train)

print("Predicting on test data...")
test["prediction"] = clf.predict(X_test_scaled)

print("\n===== EVENT-LEVEL EVALUATION =====")
# We only care about how well we detected the true anomaly part of each event
anomaly_test = test[test["label"] == 1]

detected_events = 0
total_events = anomaly_test["event_id"].nunique()

print(f"{'EVENT ID':<10} | {'SAMPLES':<7} | {'FLAGGED':<7} | {'% CAUGHT':<8} | {'STATUS'}")
print("-" * 60)

for event_id, group in anomaly_test.groupby("event_id"):
    total_samples = len(group)
    detected_samples = group["prediction"].sum()
    detection_rate = (detected_samples / total_samples) * 100
    
    # Assumption: If the model flags even 5% of the anomaly window, the alarm triggers in the control room
    is_detected = detection_rate > 5.0  
    if is_detected:
        detected_events += 1
        status = "✅ DETECTED"
    else:
        status = "❌ MISSED"
        
    print(f"{event_id:<10} | {total_samples:<7} | {detected_samples:<7} | {detection_rate:>5.1f}%   | {status}")

print("-" * 60)
print(f"Final Score: Successfully caught {detected_events} out of {total_events} anomaly events!")