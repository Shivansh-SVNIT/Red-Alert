import pandas as pd

# ==========================================
# SETTINGS
# ==========================================

channels = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]

labels_path = "data/ESA-Mission1/labels.csv"


# ==========================================
# LOAD LABELS
# ==========================================

labels = pd.read_csv(labels_path)

labels["StartTime"] = pd.to_datetime(
    labels["StartTime"],
    utc=True
)

labels["EndTime"] = pd.to_datetime(
    labels["EndTime"],
    utc=True
)


# ==========================================
# FIND EVENTS CONTAINING ALL 6 CHANNELS
# ==========================================

event_channels = (
    labels
    .groupby("ID")["Channel"]
    .apply(set)
)

valid_events = []

for event_id, event_channel_set in event_channels.items():

    if set(channels).issubset(event_channel_set):
        valid_events.append(event_id)


print("Valid events:", len(valid_events))


# ==========================================
# GET TIME RANGE OF EACH EVENT
# ==========================================

valid_labels = labels[
    labels["ID"].isin(valid_events)
].copy()

event_times = (
    valid_labels
    .groupby("ID")
    .agg(
        StartTime=("StartTime", "min"),
        EndTime=("EndTime", "max")
    )
    .sort_values("StartTime")
)


print("\nChronological events:")
print(event_times)


# ==========================================
# TRAIN / TEST EVENT SPLIT
# ==========================================

split_index = int(len(event_times) * 0.8)

train_events = event_times.iloc[:split_index]
test_events = event_times.iloc[split_index:]


print("\n===== EVENT SPLIT =====")

print("Training events:", len(train_events))
print("Testing events :", len(test_events))

print("\nLast training event:")
print(train_events.tail(1))

print("\nFirst testing event:")
print(test_events.head(1))


# ==========================================
# SAVE EVENT SPLIT
# ==========================================

train_events.to_csv(
    "data/train_events.csv"
)

test_events.to_csv(
    "data/test_events.csv"
)

print("\nEvent split saved!")