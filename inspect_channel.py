import pandas as pd
import matplotlib.pyplot as plt

file_path = "data/ESA-Mission1/channels/channel_1/channel_1"

data = pd.read_pickle(file_path)

print("===== CHANNEL 1 ANALYSIS =====")

print("\nShape:")
print(data.shape)

print("\nFirst 5 values:")
print(data.head())

print("\n===== STATISTICS =====")
print("Minimum:", data["channel_1"].min())
print("Maximum:", data["channel_1"].max())
print("Mean:", data["channel_1"].mean())
print("Standard deviation:", data["channel_1"].std())

print("\nUnique values:", data["channel_1"].nunique())
print("Missing values:", data["channel_1"].isna().sum())

print("\nTime range:")
print("Start:", data.index.min())
print("End:", data.index.max())


# =========================
# GRAPH
# =========================

# Take first 10,000 measurements
sample = data.iloc[:10000]

plt.figure(figsize=(12, 5))

plt.plot(sample.index, sample["channel_1"])

plt.xlabel("Time")
plt.ylabel("Telemetry Value")
plt.title("ESA Mission 1 - Channel 1 Telemetry")

plt.grid(True)
plt.tight_layout()

plt.show()


print("\n===== EXTREME VALUES =====")

min_index = data["channel_1"].idxmin()
max_index = data["channel_1"].idxmax()

print("Minimum value:", data["channel_1"].min())
print("Minimum occurs at:", min_index)

print("Maximum value:", data["channel_1"].max())
print("Maximum occurs at:", max_index)