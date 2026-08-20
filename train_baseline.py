import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_curve, auc

print("Loading datasets...")
# 1. Load the BALANCED feature-engineered train data
train = pd.read_csv("data/balanced_features_train.csv")

# 2. Load the UNBALANCED (original distribution) feature-engineered test data
test = pd.read_csv("data/features_test.csv")

# 3. Separate features and target
# Drop non-ML columns
exclude_cols = ["datetime", "event_id", "label"]
feature_cols = [col for col in train.columns if col not in exclude_cols]

X_train = train[feature_cols]
y_train = train["label"]

X_test = test[feature_cols]
y_test = test["label"]

print(f"Training on {X_train.shape[0]} samples, Testing on {X_test.shape[0]} samples...")

# 4. Scale the features
print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train the Model
print("Training Random Forest Classifier (this might take a few seconds)...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train_scaled, y_train)

# 6. Evaluate on realistic future data
print("\nEvaluating on UNTOUCHED future test events...")
y_pred = clf.predict(X_test_scaled)
y_prob = clf.predict_proba(X_test_scaled)[:, 1]

print("\n===== CONFUSION MATRIX =====")
print("              Predicted Normal  Predicted Anomaly")
print(f"Actual Normal  {confusion_matrix(y_test, y_pred)[0][0]:<17} {confusion_matrix(y_test, y_pred)[0][1]}")
print(f"Actual Anomaly {confusion_matrix(y_test, y_pred)[1][0]:<17} {confusion_matrix(y_test, y_pred)[1][1]}")

print("\n===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, y_pred, digits=4))

# Calculate PR-AUC (crucial for highly imbalanced test sets)
precision, recall, _ = precision_recall_curve(y_test, y_prob)
pr_auc = auc(recall, precision)
print(f"PR-AUC Score: {pr_auc:.4f}")