import numpy as np
import pandas as pd
from datetime import timedelta

class FraudInjector:
    def __init__(self, user_profiles):
        self.user_profiles = user_profiles

    def inject_spending_spikes(self, df, count=15):
        """Forces random transactions to smash past behavioral boundaries using stochastic multipliers."""
        df_copy = df.copy()
        sampled_indices = df_copy.sample(n=count, random_state=77).index
        
        for idx in sampled_indices:
            uid = df_copy.loc[idx, 'user_id']
            profile = self.user_profiles[uid]
            
            # Continuous random multiplier to destroy fixed threshold signatures
            random_multiplier = np.random.uniform(3.5, 8.5)
            spike_amount = profile['mean_spend'] + (random_multiplier * profile['std_spend'])
            
            df_copy.loc[idx, 'amount'] = round(spike_amount, 2)
            df_copy.loc[idx, 'is_fraud'] = 1
            
        return df_copy

    def inject_geo_velocity_violations(self, df, count=15):
        """
        UPGRADE: Simulates advanced adversarial blending fraud.
        Dynamically distributes fraud locations across both international hubs
        and realistic domestic economic centers (like Bengaluru and Trichy) 
        to prevent the ML model from over-indexing on a single global coordinate.
        """
        df_copy = df.copy()
        sampled_indices = df_copy.sample(n=count, random_state=88).index
        
        # A list of realistic target cities with their actual coordinate center points
        target_destinations = [
            {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060},    # International Jump
            {'name': 'Bengaluru', 'lat': 12.9716, 'lon': 77.5946},   # Domestic Tech Hub (~300km away)
            {'name': 'Trichy', 'lat': 10.7905, 'lon': 78.7047},      # Regional Center (~330km away)
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777}        # Commercial Capital (~1000km away)
        ]
        
        # Ensure reproducibility when picking cities inside the loop
        np.random.seed(88)
        
        for idx in sampled_indices:
            if idx == 0: continue
            
            # Dynamically select one of our target destinations
            destination = np.random.choice(target_destinations)
            
            # Apply a tiny random scattering offset so all fraud isn't hitting the exact same pinpoint
            lat_scatter = np.random.uniform(-0.05, 0.05)
            lon_scatter = np.random.uniform(-0.05, 0.05)
            
            # Overwrite the clean local coordinates with our dynamic fraud target
            df_copy.loc[idx, 'merchant_lat'] = round(destination['lat'] + lat_scatter, 4)
            df_copy.loc[idx, 'merchant_long'] = round(destination['lon'] + lon_scatter, 4)
            
            # Compress the timeline to force an impossible physical travel speed
            prev_time = df_copy.loc[idx - 1, 'timestamp']
            
            # Forcing a 4-minute gap between Chennai and ANY of these cities creates an absolute velocity failure
            df_copy.loc[idx, 'timestamp'] = prev_time + timedelta(minutes=4)
            df_copy.loc[idx, 'is_fraud'] = 1  
            
        return df_copy

    def inject_card_testing_attacks(self, df, count=15):
        """
        IMPROVEMENT 2: Simulates sequential low-value probing (card testing).
        A microscopic digital charge followed rapidly by an account drain.
        """
        df_copy = df.copy()
        # Ensure we avoid picking the final rows of the matrix to prevent sequence blowouts
        sampled_indices = df_copy.sample(n=count, random_state=99).index
        
        for idx in sampled_indices:
            if idx >= len(df_copy) - 1: continue
            
            uid = df_copy.loc[idx, 'user_id']
            profile = self.user_profiles[uid]
            
            # --- Transaction A: The Micro-Probe ---
            # Force a tiny value completely beneath normal user limits
            df_copy.loc[idx, 'amount'] = round(np.random.uniform(1.05, 9.75), 2)
            df_copy.loc[idx, 'category'] = 'online_retail'
            df_copy.loc[idx, 'is_fraud'] = 1
            
            # --- Transaction B: The Downstream Account Drain (Happening 15 mins later) ---
            next_idx = idx + 1
            df_copy.loc[next_idx, 'user_id'] = uid  # Target the same user identity
            df_copy.loc[next_idx, 'category'] = 'luxury'
            
            # Force a massive randomized spending spike
            drain_multiplier = np.random.uniform(6.0, 10.0)
            drain_amount = profile['mean_spend'] + (drain_multiplier * profile['std_spend'])
            
            df_copy.loc[next_idx, 'amount'] = round(drain_amount, 2)
            df_copy.loc[next_idx, 'timestamp'] = df_copy.loc[idx, 'timestamp'] + timedelta(minutes=15)
            df_copy.loc[next_idx, 'is_fraud'] = 1
            
        return df_copy