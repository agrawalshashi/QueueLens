# QueueLens 🔎

### Predicting Long-Resolution Risk in NYC 311 Service Requests

QueueLens is an end-to-end Data Science portfolio project that investigates whether a New York City 311 service request takes more than seven days to resolve.

It combines exploratory data analysis, feature engineering, machine learning, model evaluation, a Flask API, and an interactive web dashboard.

> **Disclaimer:** QueueLens is a research prototype, not an official NYC service tool. Predictions are estimates, not guarantees, and should not be used as the sole basis for service decisions.

## 🎯 Project Objective

Explore whether historical service-request attributes can help estimate the likelihood of a request having a resolution duration greater than seven days.

## ✨ Features

* Data cleaning and exploratory data analysis
* Resolution-time calculation and feature engineering
* Chronological train-test split
* Majority-class baseline comparison
* Random Forest classification pipeline
* Evaluation using precision, recall, F1-score, and PR-AUC
* Classification-threshold analysis and feature importance
* Flask API for health checks, category options, and predictions
* Responsive dashboard built with HTML, CSS, and JavaScript

## 🛠️ Tech Stack

| Category         | Technologies                  |
| ---------------- | ----------------------------- |
| Language         | Python                        |
| Data Analysis    | Pandas, NumPy                 |
| Machine Learning | Scikit-learn                  |
| Visualization    | Matplotlib                    |
| Backend          | Flask                         |
| Frontend         | HTML, CSS, JavaScript         |
| Development      | Jupyter Notebook, Git, GitHub |

## 📂 Project Structure

```text
QueueLens/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   └── model_utils.py
├── notebooks/
│   └── QueueLens_Research.ipynb
├── models/
│   └── README.md
├── data/
│   └── README.md
├── reports/
│   └── figures/
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── tests/
    └── test_api.py
```

## 📊 Dataset

This project uses the NYC Open Data dataset:

**311 Service Requests from 2020 to Present**

Dataset: [Explore NYC Open Data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)

The initial sample selected recent records within each month of 2025. This approach is not random and may introduce selection bias.

For reproducibility, record the retrieval date, API query, sample size, and data-cleaning steps in the research notebook.

The dataset's metadata and terms should be checked before redistributing records.

## 🧠 Machine Learning Approach

### Target Variable

The target is defined as:

`long_resolution = 1` when resolution duration is greater than seven days; otherwise, `0`.

Resolution duration is calculated from the request creation and closure timestamps.

Because the target requires a closure timestamp, the training dataset represents requests that have already been closed. Predictions should therefore be interpreted as estimates based on historical associations, not as verified forecasts of how long a currently open request will remain unresolved.

### Features

The model uses historical request attributes, including:

* Agency
* Complaint type
* Borough
* Request creation hour
* Request creation day
* Request creation month

Categorical variables are encoded using `OneHotEncoder`, and a Random Forest classifier estimates the probability of the positive class.

### Evaluation Strategy

A chronological train-test split is used to evaluate the model on a later portion of the sampled data.

The model is compared with a majority-class baseline using:

* Accuracy
* Precision
* Recall
* F1-score
* Precision-Recall AUC (PR-AUC)

Precision, recall, and PR-AUC are especially useful when evaluating imbalanced classification problems.

## 📈 Model Results

Add the final results from the notebook after rerunning the evaluation.

| Metric    |  Baseline | Random Forest |
| --------- | --------: | ------------: |
| Accuracy  | To verify |     To verify |
| Precision | To verify |     To verify |
| Recall    | To verify |     To verify |
| F1-score  | To verify |     To verify |
| PR-AUC    | To verify |     To verify |

Include the test-period dates, classification threshold, and relevant error analysis alongside the final metrics.

Do not compare results from different dataset samples or evaluation splits as if they were directly equivalent.

## 🖥️ Interactive Dashboard

The Flask application provides a web interface for entering request attributes and viewing an estimated long-resolution risk.

The dashboard communicates model output as a probability and a threshold-based label. It does not guarantee when a service request will be resolved.

Add a screenshot of the actual running application here when available.

## 🚀 Getting Started

###
