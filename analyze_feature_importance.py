import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

print("Loading balanced training data...")
train = pd.read_csv("data/balanced_features_train.csv")

# Separate features and target
exclude_cols = ["datetime", "event_id", "label"]
feature_cols = [col for col in train.columns if col not in exclude_cols]

X_train = train[feature_cols]
y_train = train["label"]

print("Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

print("Training Random Forest to extract feature importances...")
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train_scaled, y_train)

# Extract and sort importances
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]

print("\n===== TOP 15 FEATURES =====")
for i in range(15):
    print(f"{i+1}. {feature_cols[indices[i]]:<25} ({importances[indices[i]]:.4f})")

# Plotting
plt.figure(figsize=(12, 8))
plt.title("Top 15 Feature Importances (Random Forest)")
plt.bar(range(15), importances[indices][:15], align="center")
plt.xticks(range(15), [feature_cols[i] for i in indices[:15]], rotation=45, ha='right')
plt.xlim([-1, 15])
plt.tight_layout()
plt.savefig("feature_importances.png")
print("\nPlot saved as 'feature_importances.png'")