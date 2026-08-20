import pandas as pd
import matplotlib.pyplot as plt

channels = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]

# -----------------------------
# Load all 6 channels
# -----------------------------

dataframes = []

for channel in channels:

    path = f"data/ESA-Mission1/channels/{channel}/{channel}"

    df = pd.read_pickle(path)

    dataframes.append(df)


data = pd.concat(dataframes, axis=1)

data.index = pd.to_datetime(data.index)


# -----------------------------
# Anomaly ID 1 time range
# -----------------------------

start = pd.Timestamp("2004-12-02 03:07:17.646")
end = pd.Timestamp("2004-12-08 23:35:55.146")


# Take 1 day before and after
before = start - pd.Timedelta(days=1)
after = end + pd.Timedelta(days=1)

plot_data = data.loc[before:after]


print("Selected rows:", len(plot_data))


# -----------------------------
# Plot
# -----------------------------

fig, axes = plt.subplots(
    6,
    1,
    figsize=(14, 14),
    sharex=True
)

for i, channel in enumerate(channels):

    axes[i].plot(
        plot_data.index,
        plot_data[channel]
    )

    axes[i].set_ylabel(channel)
    axes[i].grid(True)

    # Mark anomaly
    axes[i].axvspan(
        start,
        end,
        alpha=0.3
    )


axes[-1].set_xlabel("Time")

fig.suptitle(
    "Anomaly ID 1 - Multivariate Telemetry",
    fontsize=16
)

plt.tight_layout()

plt.show()