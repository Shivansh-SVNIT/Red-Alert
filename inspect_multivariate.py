import pandas as pd

channels = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]

dataframes = []

for channel in channels:

    path = f"data/ESA-Mission1/channels/{channel}/{channel}"

    print(f"Loading {channel}...")

    df = pd.read_pickle(path)

    dataframes.append(df)


# Combine the channels by timestamp
data = pd.concat(dataframes, axis=1)

print("\n===== MULTIVARIATE DATA =====")

print("Shape:")
print(data.shape)

print("\nColumns:")
print(data.columns.tolist())

print("\nFirst 5 rows:")
print(data.head())

print("\nMissing values:")
print(data.isna().sum())

print("\nStatistics:")
print(data.describe())