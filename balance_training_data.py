import pandas as pd

print("Loading training data...")
# Read the feature-engineered training dataset (NOT the old raw one)
train = pd.read_csv("data/features_train.csv", parse_dates=["datetime"])

# 1. Separate normal and anomaly data
normal_df = train[train["label"] == 0]
anomaly_df = train[train["label"] == 1]

target_normal_count = len(normal_df)
print(f"Total Normal samples: {target_normal_count}")

# 2. Event-aware sampling for anomalies
unique_events = anomaly_df["event_id"].unique()
# Calculate how many samples to take from each event
samples_per_event = target_normal_count // len(unique_events)
print(f"Sampling ~{samples_per_event} anomaly samples per event (Total events: {len(unique_events)})...")

# Function to sample safely (in case an event has fewer samples than requested)
def sample_event(group, n):
    return group.sample(n=min(len(group), n), random_state=42)

# Apply the sampling across grouped events
balanced_anomalies = anomaly_df.groupby("event_id", group_keys=False).apply(
    sample_event, n=samples_per_event
)

# 3. Combine and shuffle
balanced_train = pd.concat([normal_df, balanced_anomalies]).sample(frac=1, random_state=42).reset_index(drop=True)

print("\n===== BALANCED TRAIN DATA =====")
print("Shape:", balanced_train.shape)
print("\nLabels:")
print(balanced_train["label"].value_counts())

print("\nSaving to data/balanced_features_train.csv...")
# Save function shifted to the end, where it belongs!
balanced_train.to_csv("data/balanced_features_train.csv", index=False)
print("Done!")