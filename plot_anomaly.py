import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load Channel 41 telemetry
# -----------------------------

file_path = "data/ESA-Mission1/channels/channel_41/channel_41"

data = pd.read_pickle(file_path)

# Make sure datetime is in proper format
data.index = pd.to_datetime(data.index)


# -----------------------------
# Load labels
# -----------------------------

labels = pd.read_csv("data/ESA-Mission1/labels.csv")

channel_41_labels = labels[
    labels["Channel"] == "channel_41"
].copy()

# Convert label times to datetime
channel_41_labels["StartTime"] = pd.to_datetime(
    channel_41_labels["StartTime"],
    utc=True
).dt.tz_localize(None)

channel_41_labels["EndTime"] = pd.to_datetime(
    channel_41_labels["EndTime"],
    utc=True
).dt.tz_localize(None)


# -----------------------------
# Take first anomaly
# -----------------------------

anomaly = channel_41_labels.iloc[0]

start = anomaly["StartTime"]
end = anomaly["EndTime"]

print("===== SELECTED ANOMALY =====")
print("ID:", anomaly["ID"])
print("Start:", start)
print("End:", end)


# -----------------------------
# Select data around anomaly
# -----------------------------

before = start - pd.Timedelta(days=1)
after = end + pd.Timedelta(days=1)

plot_data = data.loc[before:after]

print("\nTelemetry points selected:", len(plot_data))


# -----------------------------
# Plot
# -----------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    plot_data.index,
    plot_data["channel_41"],
    linewidth=1
)

# Mark anomaly region
plt.axvspan(
    start,
    end,
    alpha=0.3,
    label="Labelled anomaly"
)

plt.xlabel("Time")
plt.ylabel("Channel 41 Value")
plt.title("Channel 41: Normal vs Labelled Anomaly")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()