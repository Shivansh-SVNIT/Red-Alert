import pandas as pd

labels = pd.read_csv(
    "data/ESA-Mission1/labels.csv"
)

# Count how many different anomaly events
# involve each channel

channel_event_count = (
    labels
    .drop_duplicates(["ID", "Channel"])
    .groupby("Channel")["ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("===== CHANNEL FREQUENCY ACROSS EVENTS =====")

print(channel_event_count.to_string())


print("\n===== TOP 20 CHANNELS =====")

print(
    channel_event_count.head(20)
)