import pandas as pd
import os

labels = pd.read_csv(
    "data/ESA-Mission1/labels.csv"
)

# Get unique events
event_ids = labels["ID"].unique()

print("===== EVENT COVERAGE =====")

for event_id in event_ids:

    event_data = labels[
        labels["ID"] == event_id
    ]

    channels = event_data["Channel"].unique()

    available = 0
    missing = 0

    for channel in channels:

        path = f"data/ESA-Mission1/channels/{channel}/{channel}"

        if os.path.exists(path):
            available += 1
        else:
            missing += 1

    print(
        f"{event_id}: "
        f"{len(channels)} labelled channels | "
        f"{available} available | "
        f"{missing} missing"
    )
    