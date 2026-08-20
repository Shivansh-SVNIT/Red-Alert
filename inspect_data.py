import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/ESA-Mission1")

print("===== ESA MISSION 1 =====")

print("\nFiles:")
for item in DATA_DIR.iterdir():
    print(" -", item.name)

print("\n===== CHANNELS =====")
channels = pd.read_csv(DATA_DIR / "channels.csv")
print(channels.head())
print("Shape:", channels.shape)
print("Columns:", list(channels.columns))

print("\n===== LABELS =====")
labels = pd.read_csv(DATA_DIR / "labels.csv")
print(labels.head())
print("Shape:", labels.shape)
print("Columns:", list(labels.columns))

print("\n===== ANOMALY TYPES =====")
anomaly_types = pd.read_csv(DATA_DIR / "anomaly_types.csv")
print(anomaly_types.head())
print("Shape:", anomaly_types.shape)
print("Columns:", list(anomaly_types.columns))

print("\n===== TELECOMMANDS =====")
telecommands = pd.read_csv(DATA_DIR / "telecommands.csv")
print(telecommands.head())
print("Shape:", telecommands.shape)
print("Columns:", list(telecommands.columns))