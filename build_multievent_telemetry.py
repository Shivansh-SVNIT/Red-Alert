import pandas as pd

# ==========================================
# SETTINGS
# ==========================================

channels = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]

# Har anomaly se pehle 1 hour normal data
NORMAL_BEFORE = pd.Timedelta(hours=1)


# ==========================================
# LOAD TRAIN / TEST EVENTS
# ==========================================

train_events = pd.read_csv(
    "data/train_events.csv",
    index_col="ID"
)

test_events = pd.read_csv(
    "data/test_events.csv",
    index_col="ID"
)


# ==========================================
# CONVERT EVENT TIMES
# format="mixed" is important
# ==========================================

train_events["StartTime"] = pd.to_datetime(
    train_events["StartTime"],
    format="mixed",
    utc=True
)

train_events["EndTime"] = pd.to_datetime(
    train_events["EndTime"],
    format="mixed",
    utc=True
)

test_events["StartTime"] = pd.to_datetime(
    test_events["StartTime"],
    format="mixed",
    utc=True
)

test_events["EndTime"] = pd.to_datetime(
    test_events["EndTime"],
    format="mixed",
    utc=True
)


# ==========================================
# LOAD ALL 6 CHANNELS
# ==========================================

dataframes = []

for channel in channels:

    print("Loading", channel)

    path = (
        f"data/ESA-Mission1/channels/"
        f"{channel}/{channel}"
    )

    df = pd.read_pickle(path)

    # Make index timezone-aware
    df.index = pd.to_datetime(
        df.index,
        utc=True
    )

    dataframes.append(df)


# Combine all channels
telemetry = pd.concat(
    dataframes,
    axis=1
)

telemetry = telemetry.sort_index()


print("\n===== TELEMETRY LOADED =====")
print("Shape:", telemetry.shape)

print("\nChannels:")
print(telemetry.columns.tolist())


# ==========================================
# BUILD DATASET FUNCTION
# ==========================================

def build_dataset(events):

    pieces = []

    for event_id, event in events.iterrows():

        start = event["StartTime"]
        end = event["EndTime"]

        # 1 hour before anomaly
        normal_start = start - NORMAL_BEFORE

        print(
            f"\nProcessing {event_id}"
        )

        print(
            f"Normal : {normal_start} -> {start}"
        )

        print(
            f"Anomaly: {start} -> {end}"
        )


        # ==================================
        # NORMAL DATA
        # ==================================

        normal = telemetry.loc[
            normal_start:start
        ].copy()

        normal["label"] = 0
        normal["event_id"] = event_id


        # ==================================
        # ANOMALY DATA
        # ==================================

        anomaly = telemetry.loc[
            start:end
        ].copy()

        anomaly["label"] = 1
        anomaly["event_id"] = event_id


        # ==================================
        # COMBINE
        # ==================================

        pieces.append(normal)
        pieces.append(anomaly)


    # Combine all events
    return pd.concat(
        pieces
    )


# ==========================================
# BUILD TRAIN DATA
# ==========================================

print(
    "\n\n===== BUILDING TRAIN DATA ====="
)

train_data = build_dataset(
    train_events
)


# ==========================================
# BUILD TEST DATA
# ==========================================

print(
    "\n\n===== BUILDING TEST DATA ====="
)

test_data = build_dataset(
    test_events
)


# ==========================================
# SAVE DATASETS
# ==========================================

train_data.to_csv(
    "data/multievent_train.csv"
)

test_data.to_csv(
    "data/multievent_test.csv"
)


# ==========================================
# FINAL SUMMARY
# ==========================================

print(
    "\n\n===== FINAL DATASETS ====="
)

print(
    "Train shape:",
    train_data.shape
)

print(
    "Test shape:",
    test_data.shape
)


print(
    "\n===== TRAIN LABELS ====="
)

print(
    train_data["label"].value_counts()
)


print(
    "\n===== TEST LABELS ====="
)

print(
    test_data["label"].value_counts()
)


print(
    "\n===== EVENTS ====="
)

print(
    "Train events:",
    train_data["event_id"].nunique()
)

print(
    "Test events:",
    test_data["event_id"].nunique()
)


print(
    "\n===== DATASET TIME RANGE ====="
)

print(
    "Train start:",
    train_data.index.min()
)

print(
    "Train end:",
    train_data.index.max()
)

print(
    "Test start:",
    test_data.index.min()
)

print(
    "Test end:",
    test_data.index.max()
)


print(
    "\nDatasets saved successfully!"
)