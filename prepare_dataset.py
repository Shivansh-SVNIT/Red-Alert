import pandas as pd

# ==========================================
# 1. Channels we want to study
# ==========================================

channels = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]


# ==========================================
# 2. Load telemetry
# ==========================================

dataframes = []

for channel in channels:

    print("Loading", channel)

    path = f"data/ESA-Mission1/channels/{channel}/{channel}"

    df = pd.read_pickle(path)

    dataframes.append(df)


data = pd.concat(dataframes, axis=1)

data.index = pd.to_datetime(data.index)


# ==========================================
# 3. Select a small time window
# ==========================================

start_time = pd.Timestamp("2004-12-01")
end_time = pd.Timestamp("2004-12-10")

data = data.loc[start_time:end_time].copy()


print("\nTelemetry shape:")
print(data.shape)


# ==========================================
# 4. Load anomaly labels
# ==========================================

labels = pd.read_csv(
    "data/ESA-Mission1/labels.csv"
)

labels["StartTime"] = pd.to_datetime(
    labels["StartTime"],
    utc=True
).dt.tz_localize(None)

labels["EndTime"] = pd.to_datetime(
    labels["EndTime"],
    utc=True
).dt.tz_localize(None)


# ==========================================
# 5. Start with everything NORMAL
# ==========================================

data["label"] = 0


# ==========================================
# 6. Mark labelled anomaly periods
# ==========================================

for _, row in labels.iterrows():

    channel = row["Channel"]

    # Only our six channels
    if channel not in channels:
        continue

    anomaly_start = row["StartTime"]
    anomaly_end = row["EndTime"]

    mask = (
        (data.index >= anomaly_start) &
        (data.index <= anomaly_end)
    )

    data.loc[mask, "label"] = 1


# ==========================================
# 7. Check labels
# ==========================================

print("\n===== FINAL DATASET =====")

print(data.head())

print("\nShape:")
print(data.shape)

print("\nLabel counts:")
print(data["label"].value_counts())

print("\nLabel percentages:")
print(data["label"].value_counts(normalize=True) * 100)


# ==========================================
# 8. Save dataset
# ==========================================

data.to_csv(
    "data/mission1_training_window.csv"
)

print("\nDataset saved!")