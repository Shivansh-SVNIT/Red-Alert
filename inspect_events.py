import pandas as pd

labels = pd.read_csv(
    "data/ESA-Mission1/labels.csv"
)

anomaly_types = pd.read_csv(
    "data/ESA-Mission1/anomaly_types.csv"
)

print("===== ANOMALY EVENTS =====")

print("Total unique anomaly IDs:")
print(labels["ID"].nunique())

print("\nFirst 20 anomaly IDs:")
print(labels["ID"].unique()[:20])

print("\n===== ANOMALY TYPE COUNT =====")

print(
    anomaly_types["Category"].value_counts()
)

print("\n===== EVENTS PER CATEGORY =====")

event_category = anomaly_types[
    ["ID", "Category", "Dimensionality", "Locality", "Length"]
]

print(
    event_category.head(20).to_string(index=False)
)