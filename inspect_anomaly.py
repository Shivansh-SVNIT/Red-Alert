import pandas as pd

labels = pd.read_csv("data/ESA-Mission1/labels.csv")
anomaly_types = pd.read_csv("data/ESA-Mission1/anomaly_types.csv")

# Get the first Channel 41 anomaly
channel_41 = labels[
    labels["Channel"] == "channel_41"
]

first_anomaly_id = channel_41.iloc[0]["ID"]

print("Anomaly ID:", first_anomaly_id)

# Find its description
anomaly_info = anomaly_types[
    anomaly_types["ID"] == first_anomaly_id
]

print("\n===== ANOMALY INFORMATION =====")
print(anomaly_info.to_string(index=False))