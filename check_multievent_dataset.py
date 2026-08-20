import pandas as pd

train = pd.read_csv(
    "data/multievent_train.csv",
    parse_dates=["datetime"]
)

test = pd.read_csv(
    "data/multievent_test.csv",
    parse_dates=["datetime"]
)

print("===== TRAIN DATA =====")

print("Shape:", train.shape)

print("\nLabels:")
print(train["label"].value_counts())

print("\nPercentages:")
print(
    train["label"]
    .value_counts(normalize=True)
    .mul(100)
)


print("\n===== TEST DATA =====")

print("Shape:", test.shape)

print("\nLabels:")
print(test["label"].value_counts())

print("\nPercentages:")
print(
    test["label"]
    .value_counts(normalize=True)
    .mul(100)
)


print("\n===== EVENTS =====")

print(
    "Train:",
    train["event_id"].nunique()
)

print(
    "Test:",
    test["event_id"].nunique()
)


print("\n===== TRAIN SAMPLES PER EVENT =====")

print(
    train.groupby(
        ["event_id", "label"]
    ).size().head(20)
)