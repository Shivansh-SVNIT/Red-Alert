import pandas as pd

file_path = "data/ESA-Mission1/channels/channel_41/channel_41"

data = pd.read_pickle(file_path)

print("===== CHANNEL 41 =====")

print("\nShape:")
print(data.shape)

print("\nFirst 5:")
print(data.head())

print("\nLast 5:")
print(data.tail())

print("\n===== STATISTICS =====")

print("Minimum:", data["channel_41"].min())
print("Maximum:", data["channel_41"].max())
print("Mean:", data["channel_41"].mean())
print("Standard deviation:", data["channel_41"].std())

print("\nUnique values:", data["channel_41"].nunique())
print("Missing values:", data["channel_41"].isna().sum())

print("\nTime range:")
print("Start:", data.index.min())
print("End:", data.index.max())