import pandas as pd

labels = pd.read_csv("data/ESA-Mission1/labels.csv")
channels = pd.read_csv("data/ESA-Mission1/channels.csv")

# Channels involved in anomaly id_1
event_channels = labels[
    labels["ID"] == "id_1"
]["Channel"].unique()

# Get metadata of those channels
info = channels[
    channels["Channel"].isin(event_channels)
].copy()

print("===== CHANNEL METADATA FOR ANOMALY ID_1 =====")

print(info.to_string(index=False))

print("\n===== SUBSYSTEM COUNT =====")

print(info["Subsystem"].value_counts())

print("\n===== GROUP COUNT =====")

print(info["Group"].value_counts())