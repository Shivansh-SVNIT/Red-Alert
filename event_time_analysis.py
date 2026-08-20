import pandas as pd

labels = pd.read_csv(
    "data/ESA-Mission1/labels.csv"
)

selected_channels = {
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
}

# Find events containing all six channels
event_channels = (
    labels
    .groupby("ID")["Channel"]
    .apply(set)
)

valid_events = [
    event_id
    for event_id, channels in event_channels.items()
    if selected_channels.issubset(channels)
]

# Keep only valid events
valid_labels = labels[
    labels["ID"].isin(valid_events)
].copy()

# Convert times
valid_labels["StartTime"] = pd.to_datetime(
    valid_labels["StartTime"],
    utc=True
)

valid_labels["EndTime"] = pd.to_datetime(
    valid_labels["EndTime"],
    utc=True
)

# One overall time range per event
event_times = (
    valid_labels
    .groupby("ID")
    .agg(
        StartTime=("StartTime", "min"),
        EndTime=("EndTime", "max")
    )
    .sort_values("StartTime")
)

print("===== 113 VALID EVENTS =====")

print(event_times.to_string())

print("\n===== EARLIEST EVENTS =====")
print(event_times.head(10))

print("\n===== LATEST EVENTS =====")
print(event_times.tail(10))