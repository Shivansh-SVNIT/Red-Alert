import pandas as pd

labels = pd.read_csv("data/ESA-Mission1/labels.csv")

# Find all channels involved in anomaly id_1
event = labels[labels["ID"] == "id_1"]

print("===== ANOMALY ID_1 =====")
print(event.to_string(index=False))

print("\n===== CHANNELS INVOLVED =====")
print(event["Channel"].unique())

print("\nNumber of channels:", event["Channel"].nunique())