"""
DAT610 CA1, Part A: Synthetic data generation with CTGAN (via the SDV library).

This script covers the generation stage of the exercise:
    1. Load the real fraud-detection dataset (2,000 records).
    2. Detect and correct the single-table metadata, as the synthesiser
       misclassifying a column type would corrupt the generated values.
    3. Train a Conditional Tabular GAN (CTGAN) on the real data.
    4. Sample a synthetic dataset of equal size and save it to CSV.
    5. Print the documentation fields required for the Synthetic Data Card
       at the moment of synthesis, before any validation begins.

Design decisions:
    - epochs=300 follows the standard CTGAN configuration used in class.
    - batch_size=2000 (full batch). With only 2,000 records, the default
      batch of 500 yields four noisy adversarial updates per epoch; a
      full-batch regime gives the discriminator a stable view of the whole
      table at every step, which is appropriate for a table this small.
    - Seeds are fixed so the run is reproducible end to end.
"""

import datetime
import time

import numpy as np
import pandas as pd
import torch

from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer

SEED = 42
np.random.seed(SEED)
torch.manual_seed(SEED)

REAL_PATH = "transaction_dataset.csv"
SYNTH_PATH = "synthetic_transaction_dataset.csv"
METADATA_PATH = "metadata.json"

# Step 1: load the real dataset.
real_df = pd.read_csv(REAL_PATH)
print("real dataset shape:", real_df.shape)
print(real_df["is_fraud"].value_counts())

# Step 2: detect metadata, then verify and correct it before training.
# A misclassified column (for example is_fraud treated as a continuous
# number) would make the GAN regress a float target instead of learning
# the binary class, so the auto-detected types are never trusted blindly.
metadata = SingleTableMetadata()
metadata.detect_from_dataframe(real_df)
metadata.update_column("merchant_category", sdtype="categorical")
metadata.update_column("is_fraud", sdtype="categorical")
metadata.update_column("customer_age", sdtype="numerical", computer_representation="Int64")
metadata.update_column("num_transactions_30d", sdtype="numerical", computer_representation="Int64")
metadata.update_column("transaction_hour", sdtype="numerical", computer_representation="Int64")
print(metadata.to_dict())
metadata.save_to_json(METADATA_PATH, mode="overwrite")

# Step 3: train the CTGAN synthesiser.
synthesizer = CTGANSynthesizer(metadata, epochs=300, batch_size=2000, verbose=False)
t_start = time.time()
synthesizer.fit(real_df)
t_train = time.time() - t_start
print("training time: %.1f s" % t_train)

# Step 4: sample a synthetic dataset the same size as the real one.
synthetic_df = synthesizer.sample(num_rows=len(real_df))
synthetic_df.to_csv(SYNTH_PATH, index=False)
print("synthetic dataset shape:", synthetic_df.shape)
print(synthetic_df["is_fraud"].value_counts())

# Step 5: Synthetic Data Card, GENERATION section (validation status is
# PENDING until every level of the validation framework has been run).
print("--- Synthetic Data Card: GENERATION ---")
print("Date generated:      ", datetime.date.today().isoformat())
print("Generator model:      CTGAN via SDV")
print("Training data source: transaction_dataset.csv (real dataset)")
print("Real records:        ", len(real_df))
print("Synthetic records:   ", len(synthetic_df))
print("Purpose:              Fraud-detection model development without PII exposure")
print("Data sensitivity:     Financial, no raw PII in output")
print("Validation status:    PENDING, see validation report")
