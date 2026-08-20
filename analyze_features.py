import pandas as pd

# Load feature dataset
data = pd.read_csv(
    "data/mission1_features.csv",
    index_col="datetime"
)

data.index = pd.to_datetime(data.index)

normal = data[data["label"] == 0]
anomaly = data[data["label"] == 1]


channels = [
    "channel_41",
    "channel_42",
    "channel_43",
    "channel_44",
    "channel_45",
    "channel_46"
]


print("===== ALL CHANNEL FEATURE ANALYSIS =====")


results = []


for channel in channels:

    features = [
        channel,
        channel + "_diff",
        channel + "_rolling_mean",
        channel + "_rolling_std"
    ]

    for feature in features:

        normal_mean = normal[feature].mean()
        anomaly_mean = anomaly[feature].mean()

        difference = abs(
            anomaly_mean - normal_mean
        )

        results.append({
            "Feature": feature,
            "Normal Mean": normal_mean,
            "Anomaly Mean": anomaly_mean,
            "Absolute Difference": difference
        })


result = pd.DataFrame(results)


print("\n===== MOST DIFFERENT FEATURES =====")

print(
    result.sort_values(
        "Absolute Difference",
        ascending=False
    ).to_string(index=False)
)