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

event_channels = (
    labels
    .groupby("ID")["Channel"]
    .apply(set)
)

valid_events = []

for event_id, channels in event_channels.items():

    if selected_channels.issubset(channels):
        valid_events.append(event_id)


print("===== VALID EVENTS =====")

print("Total valid events:", len(valid_events))

print("\nEvents:")

print(valid_events)