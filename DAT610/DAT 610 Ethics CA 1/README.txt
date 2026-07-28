DAT610: Ethics and Privacy, Continuous Assessment 1
Validation of a CTGAN Synthetic Transaction Dataset
Prepared by Yinka, 11 July 2026

CONTENTS
    01_generate_synthetic_data.py       Trains CTGAN (via SDV) on the real dataset and samples
                                        the synthetic dataset. Prints the Synthetic Data Card
                                        generation fields at synthesis time.
    02_validate_synthetic_data.py       Runs the five-level validation framework and writes
                                        every computed value to validation_results.json and the
                                        diagnostic figures to figures/.
    transaction_dataset.csv             The real dataset: 2,000 records, 1.00% fraud rate.
    synthetic_transaction_dataset.csv   The CTGAN output: 2,000 records.
    metadata.json                       SDV single-table metadata used for training.
    validation_results.json             All validation metrics exactly as computed.
    figures/                            KDE plots, categorical bar charts, correlation heatmaps.

RUN ORDER
    python 01_generate_synthetic_data.py
    python 02_validate_synthetic_data.py

Both scripts are seeded (seed 42), so the pipeline is reproducible end to end.
Note that GAN training is only bit-reproducible on the same library versions and hardware.

DEPENDENCIES
    python 3.10, numpy 1.26, pandas 2.3, scipy 1.15, scikit-learn, matplotlib,
    seaborn, torch 1.13 (CPU), sdv 1.37

The accompanying report (DAT610 CA1 Validation Report.docx) explains the workflow,
diagnoses every figure, reports every metric, and gives the deployment recommendation.
