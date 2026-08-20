import pandas as pd

# Load prepared dataset
data = pd.read_csv(
    "data/mission1_training_window.csv",
    index_col="datetime"
)

# Features
features = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]
data.index = pd.to_datetime(data.index)
X = data[features]
y = data["label"]

print("===== ML DATASET =====")

print("\nX shape:")
print(X.shape)

print("\ny shape:")
print(y.shape)

print("\nFeatures:")
print(X.head())

print("\nLabels:")
print(y.head())

print("\nLabel distribution:")
print(y.value_counts())


# ==========================================
# TIME-BASED TRAIN / TEST SPLIT
# ==========================================

split_time = pd.Timestamp("2004-12-08")


X_train = X[X.index < split_time]
X_test = X[X.index >= split_time]

y_train = y[y.index < split_time]
y_test = y[y.index >= split_time]


print("\n===== TRAIN / TEST SPLIT =====")

print("\nTraining data:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTesting data:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)


print("\nTraining labels:")
print(y_train.value_counts())

print("\nTesting labels:")
print(y_test.value_counts())