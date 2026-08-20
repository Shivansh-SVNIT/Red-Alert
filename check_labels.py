import pandas as pd

labels = pd.read_csv("data/ESA-Mission1/labels.csv")

channel_41_labels = labels[
    labels["Channel"] == "channel_41"
].copy()

print("===== CHANNEL 41 ANOMALY LABELS =====")

print("\nNumber of labelled intervals:")
print(len(channel_41_labels))

print("\nFirst 20 labels:")
print(channel_41_labels.head(20).to_string(index=False))