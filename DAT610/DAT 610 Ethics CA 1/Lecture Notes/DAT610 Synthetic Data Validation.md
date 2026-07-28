<!-- Slide number: 1 -->
MSc Data Science  ·  Ethics & Privacy
Synthetic Data
in ML Pipelines
Documentation  ·  Disclosure  ·  Distributional Alignment Validation
Practical lecture with hands-on lab

### Notes:
Opening: ask students what they think 'distributional alignment' means before defining it. Then work through the statement together before moving to the case study. The lecture is structured as three interlocking skills: generate, validate, disclose. All three must be present for the work to be professionally defensible.

<!-- Slide number: 2 -->
Three Professional Obligations

"A data scientist must document and disclose when generative AI synthetic data is included in model training, and must provide validation evidence of its distributional alignment with real-world data before production deployment."

DOCUMENT
Record generator, source data, counts, date, and purpose before any training begins.

1

DISCLOSE
Notify data leads, owners, and regulators before the model reaches production.

2

VALIDATE
Confirm alignment using KS tests, Wasserstein distance, and TSTR benchmarks.

3

### Notes:
Ask students: which of the three is hardest to enforce in practice? Almost always the answer is DISCLOSE — it requires organisational culture, not just technical skill. A team that validates perfectly but never tells stakeholders has met two obligations and failed the third. Emphasise: skipping any one invalidates the others.

<!-- Slide number: 3 -->
What We Cover Today
| Section | Topic | Time |
| --- | --- | --- |
| Case Study | FintechPay Fraud Detection — context and the data challenge | 15 min |
| Part 1 | Generating synthetic data with CTGAN via the SDV library | 30 min |
| Part 2 | Validating distributional alignment — five-level framework | 60 min |
| Part 3 | Producing the Synthetic Data Card and formal disclosure | 20 min |
| Part 4 | Ethics, professional standards, and regulatory obligations | 20 min |

### Notes:
A natural split point for a two-session delivery is between Part 1 and Part 2. The first session covers the business motivation and synthesis pipeline (~1 hour); the second covers the full validation framework and ethics (~2 hours). The hands-on lab runs during the second session.

<!-- Slide number: 4 -->
Case Study Setup
FintechPay
Fraud Detection

### Notes:

<!-- Slide number: 5 -->
FintechPay: A Realistic Data Problem
Nigerian digital payments company · 2 million transactions daily · Real-time fraud classification required

Problem 1
Problem 2
Severe Class Imbalance
Privacy Restrictions
Raw transaction records

contain customer Personal Identifiable Information (PII).

Nigeria's NDPA 2023 and internal policy restrict PII use in development and staging environments.
~100 fraud cases
out of 10,000 records
Too few examples for a model to learn reliable fraud patterns.

### Notes:
The decision that triggers the professional obligation: use CTGAN to generate synthetic transaction records, augmenting fraud cases while removing PII exposure. This is a legitimate and common practice — but the moment it is chosen, all three obligations become active. The rest of the lecture teaches students how to meet them.

<!-- Slide number: 6 -->
The Transaction Dataset
| Feature | Type | What It Captures |
| --- | --- | --- |
| transaction\_amount | Continuous | Transaction value in Naira (NGN) |
| customer\_age | Discrete | Customer age in years (18–75) |
| account\_balance | Continuous | Balance prior to the transaction |
| num\_transactions\_30d | Discrete | Transaction count in the prior 30 days |
| transaction\_hour | Discrete | Hour the transaction occurred (0–23) |
| distance\_from\_home\_km | Continuous | Distance from customer's registered home address |
| merchant\_category | Categorical | grocery · electronics · entertainment · travel · utilities |
| is\_fraud | Binary | Target: 1 = fraudulent, 0 = legitimate (~1% fraud rate) |

### Notes:
Discussion prompt before showing any code: which features do you expect to look different between fraud and legitimate transactions? Key answers: transaction_hour (fraud clusters at 0–3, 22–23), distance_from_home_km (fraud has exponential mean 80km vs 15km for legitimate), transaction_amount (fraud is higher). This motivates the validation framework — if synthesis loses these signatures, the model fails silently.

<!-- Slide number: 7 -->
Part 1
Generating Synthetic Data
with Generative AI

### Notes:

<!-- Slide number: 8 -->
Three Approaches to Tabular Synthesis
Each must preserve: column distributions · inter-column correlations · data types · class balance

CTGAN
TVAE
Gaussian
Copula
Conditional Tabular GAN
Tabular VAE
Statistical Copula
GAN with mode-specific normalisation. Handles multi-modal continuous columns and imbalanced classes. Industry standard via SDV.
Variational autoencoder approach. Faster training than CTGAN. Best suited to simpler, unimodal distributions.
Models each column's marginal independently, then reconstructs correlations via a copula. Fully interpretable; works on small datasets.

Our choice for FintechPay

Faster · simpler datasets

Small data · interpretable

### Notes:
Ask: why can image-generation approaches (diffusion models, image GANs) not simply be adapted for tabular data? Key answer: tabular data has no spatial structure; columns have different types; distributions vary enormously per column; and inter-column relationships must be preserved exactly, not approximately.

<!-- Slide number: 9 -->
CTGAN: The Four-Step Pipeline

Install SDV

pip install sdv pandas numpy matplotlib seaborn scipy scikit-learn
1

Detect metadata

metadata = SingleTableMetadata()
metadata.detect_from_dataframe(real_df)
# Always verify: print(metadata.to_dict())

2

Train synthesiser

synthesizer = CTGANSynthesizer(metadata, epochs=300)
synthesizer.fit(real_df)

3

Sample records

synthetic_df = synthesizer.sample(
    num_rows=len(real_df))
4

### Notes:
Run Step 3 live or show training output. Key teaching point: always inspect the auto-detected metadata using metadata.to_dict() before training. If the synthesiser misclassifies a column type (e.g., treats transaction_hour as continuous rather than discrete), it will generate nonsense values for that feature. One minute of metadata review prevents hours of debugging.

<!-- Slide number: 10 -->
Documentation Checkpoint — Record It Now
Record this at the moment synthesis runs — before validation begins.

Date Generated
2024-04-15
Generator Model
CTGAN via SDV v1.x
Training Data Source
FintechPay transactions — Q1 2024
Real Records
10,000
Synthetic Records
10,000  (50% of combined set)
Purpose
Fraud detection class augmentation
Data Sensitivity
Financial — no raw PII in output
Generated By
[Data Scientist Name  ·  Role  ·  Date]
Validation Status
PENDING — see Validation Report

### Notes:
The Validation Status field says PENDING. This is intentional and correct. The record is not complete — and the model should not be submitted for deployment review — until all five validation levels pass and the status is updated. The Synthetic Data Card is a living document until it is signed off by the validation reviewer.

<!-- Slide number: 11 -->
Part 2
Validating Distributional
Alignment — Five Levels

### Notes:

<!-- Slide number: 12 -->
The Validation Framework

Summary Statistics
Side-by-side means, std, and percentiles

1

Visual Distributions
KDE plots, bar charts, and heatmaps

2

Statistical Tests
KS test, Chi-squared, Wasserstein

3

ML Utility — TSTR
Train Synthetic, Test Real vs baseline

4

Privacy — DNNR
Distance to Nearest Neighbour ratio

5

### Notes:
Motivate the progression: Level 1 is a 30-second sanity check. Level 2 catches shape differences that statistics miss (Anscombe's Quartet is the classic demonstration — use it). Level 3 gives auditable, quantitative proof. Level 4 tests whether the data actually works for the modelling task. Level 5 confirms it doesn't expose real individuals. Every level adds something the previous levels cannot.

<!-- Slide number: 13 -->
Level 1 + 2: Initial Checks

Level 1 — Summary Statistics
Level 2 — Visual Distributions
pandas describe() side by side
Flag any mean difference above 10%
Above 20%: do not proceed
A screening step — not a conclusion
KDE plots: curves should overlap closely
Bar charts: categorical proportions must match
Correlation heatmaps: patterns between columns must be preserved, not just individual columns
Statistics can look fine while distributions differ in shape — which is why this is only Level 1.

### Notes:
The correlation heatmap comparison is the step most commonly skipped in practice. Emphasise: a synthesiser can reproduce every column's marginal distribution perfectly but destroy the relationships between columns. If the synthesis loses the correlation between distance_from_home and is_fraud, the fraud signal is gone — even if each column individually passes Level 1 and Level 2.

<!-- Slide number: 14 -->
Level 3a: Kolmogorov-Smirnov Test
For continuous variables — tests whether two samples share the same distribution.

| p-value | Result |
| --- | --- |
| p > 0.05 | ✓ Aligned — fail to reject H₀ |
| p ≤ 0.05 | ✗ Not aligned — reject H₀ |
H₀ :  Real and synthetic samples come from the same distribution
Hₐ :  They come from different distributions
Python

from scipy import stats

ks_stat, p_value = stats.ks_2samp(
    real_df[col].dropna(),
    synthetic_df[col].dropna()
)
aligned = (p_value > 0.05)   # True = pass

### Notes:
Demonstrate geometrically: draw two CDFs on the board. The KS statistic is the maximum vertical distance between them. A small gap means the CDFs nearly coincide — distributions are similar. Ask: if transaction_hour has p = 0.003, what does that mean in plain language? (Answer: the chance of seeing a gap this large if real and synthetic had the same distribution is 0.3% — so we have strong evidence they differ.)

<!-- Slide number: 15 -->
Level 3b + 3c: Chi-Squared and Wasserstein

3b — Chi-Squared Test
3c — Wasserstein Distance
For categorical columns.
Drift magnitude — not just pass/fail.

| Normalised Score | Rating |
| --- | --- |
| < 0.05 | Excellent |
| 0.05 – 0.15 | Acceptable |
| > 0.15 | Poor — review |
stats.chisquare(
  f_obs = real_counts,
  f_exp = synth_expected
)
Apply to: merchant_category and is_fraud.
Normalise by σ(real) for cross-feature comparability.
Mismatch in is_fraud = model trains
on the wrong fraud rate.
A feature can pass KS but still score 0.12 Wasserstein — track it.

### Notes:
The earth-mover analogy: if distribution A is a pile of dirt and you reshape it to match distribution B, the Wasserstein distance is the minimum work required. Unlike KS, it tells you not just that distributions differ but by how much. A feature can pass KS (p > 0.05) but have a Wasserstein of 0.12 — borderline and worth tracking in the Synthetic Data Card even if it doesn't block deployment.

<!-- Slide number: 16 -->
Level 4: ML Utility Test — TSTR vs TRTR
Does a model trained only on synthetic data perform comparably when tested on real data?

TRTR
TSTR
Train on Real
Test on Real
→
Train on Synthetic
Test on Real
Gold standard baseline
Simulates production
| |TSTR AUC − TRTR AUC| | Verdict |
| --- | --- |
| < 0.02 | Fully equivalent |
| 0.02 – 0.05 | Acceptable with monitoring |
| > 0.05 | Investigate before deployment |

### Notes:
The shared held-out test set is critical: 20% of real data reserved before any training. Both TRTR and TSTR use the same 2,000-record real test set. If TRTR AUC = 0.861 and TSTR AUC = 0.847, the gap is 0.014 — acceptable. Ask: if TSTR AUC is dramatically worse, what does that tell us? (Answer: the synthetic data is missing distributional features the model needs, even if it passed all the statistical tests at Levels 1–3.)

<!-- Slide number: 17 -->
Level 5: Privacy Check — DNNR
Memorisation bypasses statistical tests — DNNR measures proximity to real data.

d_SR  =  nearest synthetic-to-real distance
d_RR  =  nearest real-to-real distance (excluding itself)
DNNR  =  median(d_SR) / median(d_RR)
| DNNR Score | Interpretation |
| --- | --- |
| DNNR > 1.5 | Privacy preserved — synthetic records are well-separated from real ones |
| 1.0 < DNNR ≤ 1.5 | Borderline — synthetic records are moderately close to real records |
| DNNR ≤ 1.0 | Memorisation risk — investigate before any deployment |

### Notes:
Ask: if DNNR = 1.0 exactly, what does that mean geometrically? Answer: synthetic records are as close to real records as real records are to each other — the synthetic dataset is indistinguishable from the real data in feature space. This is the worst possible privacy outcome from a synthesis run. The DNNR check matters even when CTGAN is the method, because on small training datasets the generator can collapse into memorisation.

<!-- Slide number: 18 -->
Validation Summary — What Goes in the Report
| Lvl | Test | Pass Criterion | Library |
| --- | --- | --- | --- |
| 1 | Descriptive statistics | All means within 10% of real | pandas |
| 2 | KDE + correlation heatmaps | Visual alignment confirmed | seaborn / matplotlib |
| 3a | KS test — continuous cols | p > 0.05 for every continuous column | scipy.stats.ks\_2samp |
| 3b | Chi-squared — categorical | p > 0.05 for every categorical column | scipy.stats.chisquare |
| 3c | Wasserstein distance | Normalised score < 0.15 per feature | wasserstein\_distance |
| 4 | TSTR vs TRTR AUC gap | Gap < 0.05 on shared real test set | sklearn |
| 5 | Privacy DNNR ratio | DNNR > 1.5 | sklearn NearestNeighbors |

### Notes:
This table is the skeleton of the Synthetic Data Card's Validation Evidence section. Each row must appear with the actual computed values — not just pass/fail marks. Ask: why do we need both KS test and Wasserstein? (KS is binary; Wasserstein gives magnitude — a feature can technically pass KS but have a Wasserstein of 0.12, which should be monitored and explained in the card even if it doesn't block deployment.)

<!-- Slide number: 19 -->
The Synthetic Data Card
Three mandatory sections — one document attached to every deployment artefact.

GENERATION

1
Generator model  ·  Training source  ·  Record counts  ·  Date  ·  Purpose  ·  Creator
VALIDATION EVIDENCE

2
KS Test (continuous)  ·  Chi-squared (categorical)  ·  Wasserstein score  ·  TSTR AUC gap  ·  Privacy DNNR  ·  Validated by
DISCLOSURE

3
Stakeholders notified  ·  Documentation link  ·  Approval sign-off  ·  Date approved

### Notes:
Walk through each section: GENERATION is filled in at synthesis time. VALIDATION EVIDENCE is completed as each test runs. DISCLOSURE is the last section completed — after internal sign-off. Ask students: where should this card be stored? Answer: model registry, data catalogue, MLflow run, version control, and any regulatory submission package.

<!-- Slide number: 20 -->
Part 4
Ethics &
Professional Practice

### Notes:

<!-- Slide number: 21 -->
Without Disclosure and Validation
Each represents a documented category of harm from production ML deployments.

A — Bias Amplification
CTGAN encodes biases. Undisclosed — no reviewer can trace or correct the amplification.

B — Silent Model Failure
Wrong scale erases the fraud signal. Production failure with no traceable cause.

C — Regulatory Breach
EU AI Act Art. 10: undisclosed synthetic data in high-risk AI. Fines up to 3% of turnover.

D — Governance Failure
No documentation in a post-incident audit is classified as a control failure.

### Notes:
Scenarios A and B are technical failures; Scenarios C and D are professional and legal failures. Ask: which scenario affects the most people? Scenario A (bias amplification) can affect every customer the model evaluates, often silently for years. Ask: who bears professional responsibility in Scenario D? Everyone who touched the pipeline without raising the documentation gap.

<!-- Slide number: 22 -->
The Professional Obligation
| Organisation | Standard | Obligation Triggered |
| --- | --- | --- |
| ACM Code of Ethics (2018) | §1.2 · §2.5 | Avoid harm through negligence; perform work only in areas of competence |
| IEEE Code of Ethics | §I.1 | Honesty in claims; disclose factors that may endanger others |
| Nigeria NDPA (2023) | Art. 24 · 38 | Data subject rights and technical safeguards for PII processing |
| EU AI Act (2024) | Art. 10 · 13 | Data governance and transparency requirements for high-risk AI |
| ISO/IEC 42001 (2023) | §8.4 | Data quality management throughout the AI system lifecycle |

### Notes:
Nigeria's NDPA is particularly relevant for Lagos-based students and organisations. The Act was passed in 2023 and has enforcement teeth — penalties up to 2% of annual gross revenue or 10 million naira, whichever is higher. Ask: which of these instruments creates liability for an individual data scientist, rather than the organisation? This prompts useful discussion about the difference between professional accountability and organisational liability.

<!-- Slide number: 23 -->
"A data scientist who deploys a model trained on synthetic data without validation is making a claim about the world — based on evidence they cannot substantiate.

This is scientific dishonesty, regardless of intent."
The standard does not require perfection. It requires evidence.

### Notes:
Pause after showing this slide. Give students a moment before speaking. The crucial nuance is in the second paragraph: documented synthetic data with known limitations is professionally defensible. Undisclosed, unvalidated synthetic data is not — even if it happens to produce good results. Intent is irrelevant once harm materialises. A data scientist who did not know they were doing wrong is not absolved by ignorance.

<!-- Slide number: 24 -->
Lab Exercise: Find the Failures
Dataset: corrupted_synthetic — two features deliberately misaligned with real_df.

Run ks_test_report(). Which two features fail? Record the KS statistic and p-value for each.

1

KDE plots for both failing features. In one sentence each: what went wrong with the distribution?

2

TSTR test with corrupted_synthetic as training data. By how much does fraud AUC degrade vs TRTR?

3

Write a one-paragraph failure report: which features failed, drift magnitude, model impact, and your deployment recommendation.

4

### Notes:
The two deliberate bugs: (1) transaction_amount lognormal mean shifted from 4.5 to 5.5 — overestimates transaction values; (2) distance_from_home_km exponential scale changed from 15 to 50 — completely erases the fraud distance signature. The distance bug is the critical one. Students who find it in Task 1 and then see its model impact in Task 3 have the core lesson: statistical failures at Level 3 have concrete operational consequences. Students who only catch it in Task 3 have learned why all five levels are necessary, not just Level 4.

<!-- Slide number: 25 -->
Key Takeaways

Generate
Validate
Disclose
Use CTGAN via SDV for tabular synthesis
All five levels are required
Notify all stakeholders before deployment
Inspect auto-detected metadata before training
Column correlations matter as much as marginal distributions
Documentation is evidence, not overhead
Complete the Synthetic Data Card at synthesis — not after
TSTR confirms functional equivalence
Undisclosed synthetic data is a professional and regulatory failure

### Notes:
Return to the opening statement. Ask a student to explain what 'distributional alignment' means technically and why it matters professionally — connecting the KS test, the Wasserstein score, and the TSTR test to the obligation in the statement. If they can do that without notes, the lecture has succeeded.