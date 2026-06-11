import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

class TransactionGenerator:
    def __init__(self, num_users=50, num_days=30):
        self.num_users = num_users
        self.num_days = num_days
        self.user_profiles = {}
        
        # Standard merchant categories and their baseline weights
        self.categories = ['groceries', 'gas', 'dining', 'online_retail', 'travel', 'luxury']
        self.cat_probs = [0.35, 0.20, 0.25, 0.15, 0.04, 0.01]

    def generate_user_profiles(self):
        """Creates unique spending personalities for our customer base."""
        np.random.seed(28)  
        random.seed(28)
        
        for uid in range(1000, 1000 + self.num_users):
            self.user_profiles[uid] = {
                'home_lat': float(np.random.uniform(12.90, 13.10)),  # Bounded near Chennai
                'home_long': float(np.random.uniform(80.15, 80.28)),
                'mean_spend': float(np.random.uniform(500, 3000)),   # Average purchase amount
                'std_spend': float(np.random.uniform(100, 500)),     # Spending volatility
            }
        return self.user_profiles

    def generate_clean_transactions(self):
        """Simulates authentic customer transaction logs with human circadian rhythms."""
        if not self.user_profiles:
            self.generate_user_profiles()
            
        start_date = datetime(2026, 1, 1)
        transactions = []
        tx_id = 100000
        
        for uid, profile in self.user_profiles.items():
            num_tx = np.random.randint(20, 60)
            
            for _ in range(num_tx):
                # 1. Simulate Day Placement
                random_days = np.random.uniform(0, self.num_days)
                base_date = start_date + timedelta(days=random_days)
                
                # Circadian Time-of-Day Math
                # Mixes two Gaussian distributions to create peaks at 1:00 PM (13h) and 8:00 PM (20h)
                if np.random.rand() < 0.40:
                    hour = np.random.normal(13.0, 1.5)  # Lunch hour rush
                else:
                    hour = np.random.normal(20.0, 2.0)  # Evening dinner/shopping rush
                
                # Constrain hours strictly between 0 and 23.99
                hour = max(0.0, min(23.99, hour))
                
                # Reconstruct the exact final timestamp
                tx_time = datetime(base_date.year, base_date.month, base_date.day) + timedelta(hours=hour)
                
                # 2. Simulate Amount & Geography
                amount = max(10.0, np.random.normal(profile['mean_spend'], profile['std_spend']))
                category = np.random.choice(self.categories, p=self.cat_probs)
                
                lat_offset = np.random.uniform(-0.03, 0.03)
                long_offset = np.random.uniform(-0.03, 0.03)
                
                transactions.append({
                    'transaction_id': tx_id,
                    'user_id': uid,
                    'timestamp': tx_time,
                    'amount': round(amount, 2),
                    'category': category,
                    'merchant_lat': round(profile['home_lat'] + lat_offset, 4),
                    'merchant_long': round(profile['home_long'] + long_offset, 4),
                    'is_fraud': 0
                })
                tx_id += 1
                
        df = pd.DataFrame(transactions)
        return df.sort_values(by='timestamp').reset_index(drop=True)