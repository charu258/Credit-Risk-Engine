import os
import pandas as pd
from src.generator import TransactionGenerator
from src.inject_fraud import FraudInjector
from src.detectors import FraudDetectorPipeline

# Create data cache folder if it doesn't exist
os.makedirs("data", exist_ok=True)

print("Executing Risk Engine End-to-End Pipeline...\n")

# 1. Run Generation Engine
generator = TransactionGenerator(num_users=150, num_days=30)
profiles = generator.generate_user_profiles()
df_clean = generator.generate_clean_transactions()

# 2. Run Adversarial Threat Injection
injector = FraudInjector(profiles)
df_spikes = injector.inject_spending_spikes(df_clean, count=40)
df_velocity = injector.inject_geo_velocity_violations(df_spikes, count=40)
df_final = injector.inject_card_testing_attacks(df_velocity, count=40)

# 3. Run Defense & Detection Pipeline
pipeline = FraudDetectorPipeline(contamination=0.04)  # ~4% target balance
df_features = pipeline.engineer_features(df_final)
precision, recall, f1 = pipeline.train_and_evaluate(df_features)

