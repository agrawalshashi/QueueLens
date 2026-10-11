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

| Category             | Technologies                  |
| -------------------- | ----------------------------- |
| Programming Language | Python                        |
| Data Analysis        | Pandas, NumPy                 |
| Machine Learning     | Scikit-learn                  |
| Visualization        | Matplotlib                    |
| Backend              | Flask                         |
| Frontend             | HTML, CSS, JavaScript         |
| Development Tools    | Jupyter Notebook, Git, GitHub |

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

🔗 [Explore the dataset on NYC Open Data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9)

The initial sample selected recent records within each month of 2025. This approach is not random and may introduce selection bias.

For reproducibility, the research notebook should document:

* Data retrieval date
* API query and sampling strategy
* Number of records retrieved and retained
* Data-cleaning and preprocessing steps

Check the dataset's current metadata and terms before redistributing records.

## 🧠 Machine Learning Approach

### Target Variable

The target variable is defined as:

`long_resolution = 1` when resolution duration is greater than seven days; otherwise, `0`.

Resolution duration is calculated using the request creation and closure timestamps.

Because this target requires a closure timestamp, the training dataset represents requests that have already been closed. Consequently, the model's output should be interpreted as an estimate based on historical patterns, not a verified forecast of how long a currently open request will remain unresolved.

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

A chronological train-test split is used to evaluate performance on a later portion of the sampled data.

The Random Forest model is compared with a majority-class baseline using:

* Accuracy
* Precision
* Recall
* F1-score
* Precision-Recall AUC (PR-AUC)

Precision, recall, and PR-AUC are particularly useful for evaluating imbalanced classification problems.

## 📈 Model Evaluation

Final evaluation results should be generated from the research notebook.

| Metric    |  Baseline | Random Forest |
| --------- | --------: | ------------: |
| Accuracy  | To verify |     To verify |
| Precision | To verify |     To verify |
| Recall    | To verify |     To verify |
| F1-score  | To verify |     To verify |
| PR-AUC    | To verify |     To verify |

Before publishing final results, record the test-period dates, classification threshold, and relevant error analysis.

Do not treat accuracy alone as proof of model quality, particularly when the target classes are imbalanced.

## 🖥️ Interactive Dashboard

QueueLens includes a Flask application with an interactive dashboard.

The application allows users to enter request attributes and view an estimated long-resolution risk.

The dashboard communicates model output as a probability and a threshold-based classification label.

Add a screenshot of the actual running dashboard here once it is ready:

`![QueueLens Dashboard](reports/figures/dashboard.png)`

Make sure the screenshot exists at that path before publishing the README.

## 🚀 Getting Started

Follow these steps to run QueueLens locally on Windows.

### Prerequisites

* Python 3.13.9
* Git
* A trained model saved as `models/queuelens_model.joblib`

### 1. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username.

```powershell
git clone https://github.com/YOUR_USERNAME/QueueLens.git
cd QueueLens
```

If you already have the project on your computer, open PowerShell in your existing QueueLens folder instead.

### 2. Create a Virtual Environment

Create a Python virtual environment:

```powershell
python -m venv .venv313
```

If `.venv313` already exists, skip this command.

Activate the environment:

```powershell
.\.venv313\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run Python directly through the environment's executable:

```powershell
.\.venv313\Scripts\python.exe --version
```

### 3. Install Dependencies

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

The requirements file should pin scikit-learn to the version used to save the trained model:

```text
scikit-learn==1.9.1
```

Verify the installed version:

```powershell
python -c "import sklearn; print(sklearn.__version__)"
```

Expected output:

```text
1.9.1
```

### 4. Add the Trained Model

Ensure the trained model exists at:

```text
models/queuelens_model.joblib
```

If the model is not included in the repository, generate it using the research notebook or obtain it from a trusted source.

The model must be compatible with the installed scikit-learn version.

### 5. Start the Flask Application

Run:

```powershell
python app.py
```

Alternatively, without activating the virtual environment:

```powershell
.\.venv313\Scripts\python.exe app.py
```

When the application starts successfully, the terminal should display a local address similar to:

```text
http://127.0.0.1:5000
```

Keep the terminal open while using the application.

### 6. Open the Dashboard

Open your browser and visit:

**http://127.0.0.1:5000/**

You should see the QueueLens dashboard.

### 7. Test the API

Check the application and model status:

**GET `/api/health`**

```text
http://127.0.0.1:5000/api/health
```

Retrieve supported dropdown categories:

**GET `/api/options`**

```text
http://127.0.0.1:5000/api/options
```

Generate a prediction:

**POST `/api/predict`**

Example JSON request:

```json
{
  "agency": "EXAMPLE_AGENCY",
  "complaint_type": "EXAMPLE_COMPLAINT",
  "borough": "EXAMPLE_BOROUGH",
  "created_hour": 12,
  "created_day": 15,
  "created_month": 6
}
```

Replace the example category values with values returned by `/api/options`.

The actual request fields must match those accepted by the application and the features expected by the trained model.

The response includes an estimated probability, a threshold-based risk label, and a cautionary message.

The default classification threshold is `0.50`. It can be overridden using the `QUEUELENS_THRESHOLD` environment variable if the selected threshold is appropriately evaluated and documented.

## ⚠️ Limitations

* The initial dataset sample is not random and may not represent all NYC 311 service requests.
* A chronological holdout on a small, selected sample does not establish generalization to all future requests.
* The target is calculated from completed requests; currently open requests are not directly represented by the same observed-duration label.
* Predictions reflect historical associations, not causal explanations.
* Threshold selection affects false positives and false negatives.
* Historical category names, reporting practices, and data collection methods may change.
* Model predictions should not be treated as guaranteed resolution times.

## 🔮 Future Improvements

* Expand the dataset and improve sampling representativeness.
* Validate the model on a genuinely later time period.
* Evaluate probability calibration and classification thresholds.
* Investigate performance across agencies and boroughs.
* Compare additional machine learning models.
* Add model explainability using feature importance or SHAP.
* Automate data retrieval and data-quality checks.
* Deploy the application behind a production WSGI server after further validation and security review.

## 🙌 Acknowledgements

Dataset: NYC Open Data — 311 Service Requests.

Built as a Data Science portfolio project to explore practical machine learning, model evaluation, and deployment.

## 👩‍💻 Author

**Connect with me on LinkedIn and explore the project on GitHub.**
