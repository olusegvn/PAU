"""
Generates a synthetic transaction dataset of 2000 rows for fraud detection analysis.

Schema:
    transaction_amount    continuous, transaction value in Naira (NGN)
    customer_age          discrete, 18 to 75
    account_balance       continuous, balance prior to the transaction
    num_transactions_30d  discrete, transaction count in the prior 30 days
    transaction_hour      discrete, 0 to 23
    distance_from_home_km continuous, distance from registered home address
    merchant_category     categorical: grocery, electronics, entertainment, travel, utilities
    is_fraud              binary target, 1 = fraudulent, 0 = legitimate, approx 1% fraud rate

Fraudulent rows are drawn from shifted distributions (larger amounts, night hours,
greater distance from home, high-value merchant categories) so that the signal is
learnable but overlaps with legitimate behaviour, as in real transaction data.
A fixed seed ensures the dataset is reproducible.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

N_TOTAL = 2000
N_FRAUD = 20  # 1.0% fraud rate
N_LEGIT = N_TOTAL - N_FRAUD

CATEGORIES = ["grocery", "electronics", "entertainment", "travel", "utilities"]

# Hourly weights: legitimate activity peaks in daytime and evening;
# fraud concentrates in late night and early morning hours.
legit_hour_w = np.array(
    [0.5, 0.4, 0.3, 0.3, 0.4, 0.6, 1.5, 2.0, 3.0, 3.0, 3.0, 3.2,
     3.5, 3.2, 3.0, 3.0, 3.2, 3.5, 4.0, 4.2, 4.0, 3.0, 1.5, 0.8]
)
fraud_hour_w = np.array(
    [4.0, 4.0, 4.5, 4.0, 3.5, 3.0, 0.6, 0.5, 0.5, 0.6, 0.8, 0.8,
     0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 1.2, 1.5, 1.5, 2.0, 3.5, 4.0]
)


def make_rows(n, fraud):
    if fraud:
        # Fraud skews to large amounts, wealthier target accounts, bursts of
        # recent activity, night hours, long distances, and resellable goods.
        amount = rng.lognormal(11.3, 0.8, n)
        age = rng.normal(45, 15, n)
        balance = rng.lognormal(12.6, 1.0, n)
        n30 = rng.poisson(25, n)
        hour_w = fraud_hour_w
        distance = rng.lognormal(4.3, 0.9, n)
        cat_p = [0.08, 0.45, 0.15, 0.25, 0.07]
    else:
        amount = rng.lognormal(9.2, 1.0, n)
        age = rng.normal(36, 12, n)
        balance = rng.lognormal(12.0, 1.1, n)
        n30 = rng.negative_binomial(5, 0.3, n)
        hour_w = legit_hour_w
        distance = rng.lognormal(1.5, 1.2, n)
        cat_p = [0.35, 0.15, 0.18, 0.12, 0.20]

    # Balance is the pre-transaction balance, so it must cover the amount.
    low = balance < amount
    balance[low] = amount[low] * rng.uniform(1.05, 3.0, low.sum())

    return pd.DataFrame(
        {
            "transaction_amount": np.round(amount, 2),
            "customer_age": np.clip(np.round(age), 18, 75).astype(int),
            "account_balance": np.round(balance, 2),
            "num_transactions_30d": n30.astype(int),
            "transaction_hour": rng.choice(24, size=n, p=hour_w / hour_w.sum()),
            "distance_from_home_km": np.round(distance, 2),
            "merchant_category": rng.choice(CATEGORIES, size=n, p=cat_p),
            "is_fraud": np.full(n, int(fraud)),
        }
    )


df = pd.concat([make_rows(N_LEGIT, False), make_rows(N_FRAUD, True)])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("transaction_dataset.csv", index=False)

print(df.shape)
print(df["is_fraud"].value_counts())
print(df.describe().round(2))
