import pandas as pd
import warnings
warnings.filterwarnings('ignore') # To suppress pandas fragmentation warnings

def engineer_features(df):
    print("Calculating features...")
    
    # Sort just to be absolutely sure time is sequential
    df = df.sort_values(by=["event_id", "datetime"])
    
    channels = ["channel_41", "channel_42", "channel_43", "channel_44", "channel_45", "channel_46"]
    
    # Create an empty list to store processed event dataframes
    processed_events = []
    
    # Process EACH event separately to avoid data leakage between events
    for event_id, event_data in df.groupby("event_id"):
        # Calculate diffs
        for ch in channels:
            event_data[f"{ch}_diff"] = event_data[ch].diff()
            
            # Short-term memory (5 steps)
            event_data[f"{ch}_rolling_mean_5"] = event_data[ch].rolling(window=5, min_periods=1).mean()
            event_data[f"{ch}_rolling_std_5"] = event_data[ch].rolling(window=5, min_periods=1).std().fillna(0)
            
            # Long-term memory (60 steps)
            event_data[f"{ch}_rolling_mean_60"] = event_data[ch].rolling(window=60, min_periods=1).mean()
            event_data[f"{ch}_rolling_std_60"] = event_data[ch].rolling(window=60, min_periods=1).std().fillna(0)
            
        processed_events.append(event_data)
        
    # Combine everything back
    final_df = pd.concat(processed_events)
    
    # Diff will create NaNs in the very first row of each event, fill them with 0
    final_df = final_df.fillna(0)
    
    return final_df

print("Loading multievent_train.csv...")
train_raw = pd.read_csv("data/multievent_train.csv", parse_dates=["datetime"])
train_features = engineer_features(train_raw)

print("Loading multievent_test.csv...")
test_raw = pd.read_csv("data/multievent_test.csv", parse_dates=["datetime"])
test_features = engineer_features(test_raw)

# Save the feature engineered raw files
print("Saving feature-engineered datasets...")
train_features.to_csv("data/features_train.csv", index=False)
test_features.to_csv("data/features_test.csv", index=False)

print("Feature engineering complete!")
print(f"Train features shape: {train_features.shape}")
print(f"Test features shape: {test_features.shape}")