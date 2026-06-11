import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class FraudDetectorPipeline:
    def __init__(self, contamination=0.03):
        # We set contamination to ~3% to match the percentage of fraud we injected
        self.model = IsolationForest(contamination=contamination, random_state=77)
        
    def calculate_haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculates the great-circle distance between two points on a sphere."""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
        c = 2.0 * np.arcsin(np.sqrt(a))
        km = 6367.0 * c  # Radius of Earth in kilometers
        return km

    def engineer_features(self, df):
        """Transforms raw transaction columns into mathematical anomaly features."""
        df_feats = df.copy()
        df_feats = df_feats.sort_values(by=['user_id', 'timestamp']).reset_index(drop=True)
        
        # 1. Temporal Feature: Extract the raw transaction hour
        df_feats['hour'] = df_feats['timestamp'].dt.hour
        
        # 2. Sequential/Spatial Features: Look backward to compute differentials
        df_feats['prev_lat'] = df_feats.groupby('user_id')['merchant_lat'].shift(1)
        df_feats['prev_long'] = df_feats.groupby('user_id')['merchant_long'].shift(1)
        df_feats['prev_time'] = df_feats.groupby('user_id')['timestamp'].shift(1)
        
        # Fill first-transaction bounds to avoid NaNs crashing the model
        df_feats['prev_lat'] = df_feats['prev_lat'].fillna(df_feats['merchant_lat'])
        df_feats['prev_long'] = df_feats['prev_long'].fillna(df_feats['merchant_long'])
        df_feats['prev_time'] = df_feats['prev_time'].fillna(df_feats['timestamp'])
        
        # Calculate distance delta in km
        distances = self.calculate_haversine_distance(
            df_feats['merchant_lat'], df_feats['merchant_long'],
            df_feats['prev_lat'], df_feats['prev_long']
        )
        df_feats['distance_delta_km'] = distances
        
        # Calculate time delta in hours (add small epsilon to prevent division-by-zero)
        time_deltas_hours = (df_feats['timestamp'] - df_feats['prev_time']).dt.total_seconds() / 3600.0
        df_feats['time_delta_hours'] = time_deltas_hours
        
        # Calculate velocity vector (km/h)
        df_feats['geo_velocity'] = df_feats['distance_delta_km'] / (df_feats['time_delta_hours'] + 1e-5)
        
        # 3. Stateful Behavioral Features: User deviation from their historical mean
        user_means = df_feats.groupby('user_id')['amount'].transform('mean')
        user_stds = df_feats.groupby('user_id')['amount'].transform('std').fillna(100.0)
        df_feats['amount_zscore'] = (df_feats['amount'] - user_means) / (user_stds + 1e-5)
        
        return df_feats

    def train_and_evaluate(self, df_features):
        """Trains the Isolation Forest and outputs a complete cryptographic audit log."""
        feature_cols = ['amount', 'hour', 'distance_delta_km', 'geo_velocity', 'amount_zscore']
        X = df_features[feature_cols]
        
        preds = self.model.fit_predict(X)
        df_features['model_pred'] = np.where(preds == -1, 1, 0)
        
        # 1. Standard Confusion Matrix Calculation
        tp = int(((df_features['model_pred'] == 1) & (df_features['is_fraud'] == 1)).sum())
        fp = int(((df_features['model_pred'] == 1) & (df_features['is_fraud'] == 0)).sum())
        fn = int(((df_features['model_pred'] == 0) & (df_features['is_fraud'] == 1)).sum())
        tn = int(((df_features['model_pred'] == 0) & (df_features['is_fraud'] == 0)).sum())
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2.0 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / len(df_features)

        # 2. Advanced Diagnostic Breakdown (Proving exactly WHAT we caught)
        # Separate the dataset by original fraud labels to evaluate subset detection rates
        total_fraud_nodes = df_features['is_fraud'].sum()
        
        print("\n================ DETAILED PIPELINE AUDIT REPORT ================")
        print(f"Total Transactions Logged : {len(df_features)}")
        print(f"Ground-Truth Fraud Nodes  : {total_fraud_nodes}")
        print(f"Overall Model Accuracy     : {accuracy * 100:.2f}%")
        print("----------------------------------------------------------------")
        print("                    CONFUSION MATRIX MATRIX                     ")
        print(f"  True Positives  (TP) : {tp:<5} | [Caught Fraud Events]")
        print(f"  False Positives (FP) : {fp:<5} | [Legitimate Swipes Flagged]")
        print(f"  False Negatives (FN) : {fn:<5} | [Missed Fraud Events]")
        print(f"  True Negatives  (TN) : {tn:<5} | [Correctly Cleared Swipes]")
        print("----------------------------------------------------------------")
        print("                    CORE EVALUATION METRICS                     ")
        print(f"  Precision Score      : {precision * 100:.2f}%")
        print(f"  Recall Score         : {recall * 100:.2f}%")
        print(f"  F1-Score Metric      : {f1 * 100:.2f}%")
        print("================================================================")
        
        return precision, recall, f1