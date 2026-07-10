# Adversarial Anomaly Detection Engine for Real-Time Financial Fraud Mitigation

An enterprise-grade, unsupervised risk simulation and anomaly detection pipeline designed to isolate sophisticated, multi-dimensional financial fraud. By combining a realistic, non-uniform human behavior simulator with an adversarial threat generation layer, this system evaluates the resiliency of space-partitioning machine learning models against camouflaged, in-distribution financial crime.

---

##  System Architecture

The repository is modularly structured into three distinct pipeline layers:
1. **Data Synthesis (`src/generator.py`):** Models human circadian rhythms using a Bimodal Gaussian Mixture Model to prevent simple uniform distributions from trivializing temporal dependencies.
2. **Adversarial Injection (`src/inject_fraud.py`):** Embeds adaptive spending spikes, stateful card-testing loops, and peak-hour geospatial velocity camouflage.
3. **Detection & Explainability Pipeline (`src/detectors.py`, `src/explainability.py`):** Engineers multi-dimensional spatial-temporal features and applies an unsupervised Isolation Forest to flag latent outliers without historical ground-truth training labels.

---

##  Pipeline Performance Metrics

The architecture achieves high operational efficiency on highly imbalanced data profiles, establishing an optimal balance between maximum threat containment and minimal customer friction:

| Performance Metric | Evaluation Result | Target Operational Context |
| :--- | :--- | :--- |
| **Total Transactions Evaluated** | 5,916 | Raw Synthetic Ledger |
| **Ground-Truth Fraud Anomalies** | 159 | Multi-Tiered Injected Attack Nodes |
| **Overall Model Accuracy** | **97.26%** | System Balance Metric |
| **Recall (Detection Rate)** | **73.58%** | 117/159 Camouflaged Threats Isolated |
| **Precision Score** | **49.37%** | Industry-Standard Fraud Alert Sweet Spot |
| **False Positive Disruption Rate**| **2.08%** | Only 120 / 5,757 Legitimate Transactions Flagged |

###  Validation Confusion Matrix

| | Predicted Clean | Predicted Fraud |
| :--- | :---: | :---: |
| **Actual Clean** | 5,637 (True Negatives) | 120 (False Positives) |
| **Actual Fraud** | 42 (False Negatives) | 117 (Successfully Caught) |

* **Total Clean Transactions:** 5,757
* **Total Fraudulent Transactions:** 159

##  Mathematical & Adversarial Engineering Deep Dive

### 1. Circumventing Threshold Overfitting (Adaptive Spikes)
Instead of injecting easily detectable static outlier amounts, spending spikes are regularized stochastically using continuous uniform rational scaling factors relative to individual historical customer standard deviations:

$$\alpha \sim \mathcal{U}(3.5, 8.5)$$
$$\text{Spike Amount} = \mu_{\text{user}} + \alpha \cdot \sigma_{\text{user}}$$

This forces the Isolation Forest to map generalized continuous probability densities rather than memorizing deterministic cutting boundaries.

### 2. In-Distribution Camouflage via Joint Space-Time Geodesics
Sophisticated attackers blend into high-traffic daytime clusters. The threat engine injects impossible travel velocities while completely preserving the authentic bimodal temporal timeline of the user. Distance vectors are calculated using the spherical **Haversine Equation**:

$$d = 2R \arcsin\left(\sqrt{\sin^2\left(\frac{\Delta\phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)}\right)$$

By altering locations across an international and domestic **Geographic Anchor Matrix** (New York, Mumbai, Bengaluru, Trichy) with scattering offsets ($\pm 0.05^{\circ}$), the model cannot over-rely on raw coordinates and must isolate fraud based purely on the joint rate-of-change vector ($\Delta \text{Distance} / \Delta \text{Time}$).

### 3. State-Tracking for Sequential Card Testing
The engine simulates multi-step probing behavior by hijacking consecutive rows in the time-series matrix. It introduces an initial micro-probe ($\sim \mathcal{U}(1.05, 9.75)$) under `online_retail` to bypass volumetric rules, rapidly followed by a localized luxury balance drain 15 minutes later, validating the pipeline's stateful feature tracking capabilities.

---

##  Execution Guide

### Prerequisites
Ensure your Python runtime environment has the required core scientific dependencies compiled:
```bash
pip install pandas numpy scikit-learn
