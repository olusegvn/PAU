"""
DAT610 CA1, Part B: Five-level validation of the CTGAN synthetic dataset.

The synthetic dataset is assessed against the real dataset with the
five-level distributional alignment framework.

Every computed value is written to validation_results.json so the report
quotes the exact numbers produced by this script.
"""

import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

SEED = 42
np.random.seed(SEED)

real_df = pd.read_csv("transaction_dataset.csv")
synth_df = pd.read_csv("synthetic_transaction_dataset.csv")

CONTINUOUS = ["transaction_amount", "account_balance", "distance_from_home_km"]
DISCRETE = ["customer_age", "num_transactions_30d", "transaction_hour"]
NUMERIC = CONTINUOUS + DISCRETE
CATEGORICAL = ["merchant_category", "is_fraud"]

results = {}

"""
Level 1: summary statistics. Means within 10% of the real value pass the
screening; a gap above 20% would block further validation on that feature.
"""
level1 = {}
for col in NUMERIC:
    real_mean = real_df[col].mean()
    synth_mean = synth_df[col].mean()
    diff_pct = abs(synth_mean - real_mean) / abs(real_mean) * 100
    level1[col] = {
        "real_mean": round(float(real_mean), 2),
        "synth_mean": round(float(synth_mean), 2),
        "mean_diff_pct": round(float(diff_pct), 1),
        "pass_10pct": bool(diff_pct <= 10),
    }
results["level1_summary_stats"] = level1
print("Level 1: mean comparison")
print(pd.DataFrame(level1).T.to_string())

# The fraud rate is part of the Level 1 sanity check because a mismatch
# here means any downstream model trains on the wrong class balance.
real_fraud_rate = real_df["is_fraud"].mean()
synth_fraud_rate = synth_df["is_fraud"].mean()
results["fraud_rate"] = {
    "real": round(float(real_fraud_rate), 4),
    "synthetic": round(float(synth_fraud_rate), 4),
}
print(f"fraud rate real={real_fraud_rate} synthetic={synth_fraud_rate}")

"""
Level 2: visual distributions. 
"""
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, col in zip(axes.ravel(), NUMERIC):
    sns.kdeplot(real_df[col], ax=ax, label="Real", fill=True, alpha=0.3)
    sns.kdeplot(synth_df[col], ax=ax, label="Synthetic", fill=True, alpha=0.3)
    ax.set_title(col)
    ax.legend()
fig.suptitle("Level 2: real vs synthetic distributions (KDE)")
fig.tight_layout()
fig.savefig("figures/fig1_kde_numeric.png", dpi=150)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for ax, col in zip(axes, CATEGORICAL):
    props = pd.DataFrame({
        "Real": real_df[col].value_counts(normalize=True),
        "Synthetic": synth_df[col].value_counts(normalize=True),
    })
    props.plot.bar(ax=ax)
    ax.set_title(col)
    ax.set_ylabel("proportion")
    ax.tick_params(axis="x", rotation=30)
fig.suptitle("Level 2: categorical proportions")
fig.tight_layout()
fig.savefig("figures/fig2_categorical_bars.png", dpi=150)
plt.close(fig)

# Correlation must be preserved between columns, not only within columns;
# losing the correlation between the fraud flag and its driver features
# would erase the fraud signal even if every marginal looked correct.
real_corr = real_df[NUMERIC + ["is_fraud"]].corr()
synth_corr = synth_df[NUMERIC + ["is_fraud"]].corr()
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
sns.heatmap(real_corr, ax=axes[0], vmin=-1, vmax=1, cmap="coolwarm", annot=True, fmt=".2f", annot_kws={"size": 7})
axes[0].set_title("Real correlations")
sns.heatmap(synth_corr, ax=axes[1], vmin=-1, vmax=1, cmap="coolwarm", annot=True, fmt=".2f", annot_kws={"size": 7})
axes[1].set_title("Synthetic correlations")
fig.tight_layout()
fig.savefig("figures/fig3_correlation_heatmaps.png", dpi=150)
plt.close(fig)

corr_gap = (real_corr - synth_corr).abs()
np.fill_diagonal(corr_gap.values, 0)
corr_max_abs_gap = float(corr_gap.max().max())
gap_pairs = (
    corr_gap.where(np.triu(np.ones(corr_gap.shape, dtype=bool), k=1))
    .stack()
    .sort_values(ascending=False)
    .head(3)
)
results["level2_correlation_max_abs_gap"] = round(corr_max_abs_gap, 3)
results["level2_worst_correlation_pairs"] = {
    " vs ".join(idx): {
        "real": round(float(real_corr.loc[idx[0], idx[1]]), 3),
        "synthetic": round(float(synth_corr.loc[idx[0], idx[1]]), 3),
    }
    for idx in gap_pairs.index
}
print("Level 2: figures saved, max absolute correlation gap = %.3f" % corr_max_abs_gap)
print(json.dumps(results["level2_worst_correlation_pairs"], indent=2))

# Level 3a: Kolmogorov-Smirnov test on continuous columns. H0 is that the
# two samples come from the same distribution; p > 0.05 fails to reject H0.
level3a = {}
for col in CONTINUOUS:
    ks_stat, p_value = stats.ks_2samp(real_df[col].dropna(), synth_df[col].dropna())
    level3a[col] = {
        "ks_stat": round(float(ks_stat), 4),
        "p_value": float(p_value),
        "aligned": bool(p_value > 0.05),
    }
results["level3a_ks"] = level3a
print("Level 3a: KS test")
print(pd.DataFrame(level3a).T.to_string())

# Level 3b: Chi-squared test on categorical columns. Expected counts are the
# real proportions scaled to the synthetic sample size.
level3b = {}
for col in CATEGORICAL:
    cats = sorted(real_df[col].unique())
    obs = synth_df[col].value_counts().reindex(cats).fillna(0).to_numpy()
    exp = real_df[col].value_counts(normalize=True).reindex(cats).fillna(0).to_numpy() * len(synth_df)
    chi2, p_value = stats.chisquare(f_obs=obs, f_exp=exp)
    level3b[col] = {
        "chi2": round(float(chi2), 2),
        "p_value": float(p_value),
        "aligned": bool(p_value > 0.05),
    }
results["level3b_chi2"] = level3b
print("Level 3b: Chi-squared test")
print(pd.DataFrame(level3b).T.to_string())

# Level 3c: Wasserstein distance normalised by the real standard deviation,
# so the drift magnitude is comparable across features.
level3c = {}
for col in NUMERIC:
    wd = stats.wasserstein_distance(real_df[col], synth_df[col])
    wd_norm = wd / real_df[col].std()
    rating = "excellent" if wd_norm < 0.05 else ("acceptable" if wd_norm <= 0.15 else "poor")
    level3c[col] = {"wasserstein_norm": round(float(wd_norm), 4), "rating": rating}
results["level3c_wasserstein"] = level3c
print("Level 3c: normalised Wasserstein distance")
print(pd.DataFrame(level3c).T.to_string())

# Level 4: ML utility, TSTR vs TRTR. A shared 20% real test set is held out
# before any training. TRTR trains on the remaining real data; TSTR trains
# on the synthetic data only. Both are evaluated on the same real test set.
def encode(df, columns):
    X = pd.get_dummies(df.drop(columns=["is_fraud"]), columns=["merchant_category"])
    return X.reindex(columns=columns, fill_value=0)

feature_columns = pd.get_dummies(
    real_df.drop(columns=["is_fraud"]), columns=["merchant_category"]
).columns

real_train, real_test = train_test_split(
    real_df, test_size=0.2, stratify=real_df["is_fraud"], random_state=SEED
)
X_test, y_test = encode(real_test, feature_columns), real_test["is_fraud"]

trtr_model = RandomForestClassifier(n_estimators=200, random_state=SEED)
trtr_model.fit(encode(real_train, feature_columns), real_train["is_fraud"])
trtr_scores = trtr_model.predict_proba(X_test)[:, 1]
trtr_auc = roc_auc_score(y_test, trtr_scores)
trtr_ap = average_precision_score(y_test, trtr_scores)

tstr_model = RandomForestClassifier(n_estimators=200, random_state=SEED)
tstr_model.fit(encode(synth_df, feature_columns), synth_df["is_fraud"])
tstr_scores = tstr_model.predict_proba(X_test)[:, 1]
tstr_auc = roc_auc_score(y_test, tstr_scores)
tstr_ap = average_precision_score(y_test, tstr_scores)

auc_gap = abs(tstr_auc - trtr_auc)
verdict = (
    "fully equivalent" if auc_gap < 0.02
    else ("acceptable with monitoring" if auc_gap <= 0.05 else "investigate before deployment")
)
# Average precision is reported alongside AUC because the shared test set
# holds only a handful of positive cases; ranking-based AUC can saturate at
# 1.0 in that regime while precision-based metrics still expose differences.
results["level4_tstr"] = {
    "trtr_auc": round(float(trtr_auc), 4),
    "tstr_auc": round(float(tstr_auc), 4),
    "auc_gap": round(float(auc_gap), 4),
    "trtr_avg_precision": round(float(trtr_ap), 4),
    "tstr_avg_precision": round(float(tstr_ap), 4),
    "verdict": verdict,
    "test_set_size": len(real_test),
    "test_set_fraud_cases": int(y_test.sum()),
}
print("Level 4: TRTR AUC=%.4f TSTR AUC=%.4f gap=%.4f (%s)" % (trtr_auc, tstr_auc, auc_gap, verdict))
print("Level 4: TRTR AP=%.4f TSTR AP=%.4f" % (trtr_ap, tstr_ap))

# Level 5: privacy, Distance to Nearest Neighbour Ratio. Records are one-hot
# encoded and standardised on the real data so no feature dominates the
# distance. DNNR at or below 1.0 signals memorisation of real records.

def encode_full(df, columns):
    X = pd.get_dummies(df, columns=["merchant_category"])
    return X.reindex(columns=columns, fill_value=0).astype(float)

full_columns = pd.get_dummies(real_df, columns=["merchant_category"]).columns
scaler = StandardScaler().fit(encode_full(real_df, full_columns))
R = scaler.transform(encode_full(real_df, full_columns))
S = scaler.transform(encode_full(synth_df, full_columns))

nn_real = NearestNeighbors(n_neighbors=2).fit(R)
d_sr = nn_real.kneighbors(S, n_neighbors=1)[0][:, 0]
d_rr = nn_real.kneighbors(R, n_neighbors=2)[0][:, 1]
dnnr = float(np.median(d_sr) / np.median(d_rr))
interpretation = (
    "privacy preserved" if dnnr > 1.5
    else ("borderline" if dnnr > 1.0 else "memorisation risk")
)
results["level5_dnnr"] = {
    "median_d_sr": round(float(np.median(d_sr)), 4),
    "median_d_rr": round(float(np.median(d_rr)), 4),
    "dnnr": round(dnnr, 3),
    "interpretation": interpretation,
}
print("Level 5: DNNR = %.3f (%s)" % (dnnr, interpretation))

with open("validation_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("results written to validation_results.json")
