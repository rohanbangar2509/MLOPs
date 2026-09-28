# Track ML Experiments Using MLflow

## Overview

This project demonstrates **ML experiment tracking using MLflow**.

A small synthetic student dataset is used to train multiple regression models for predicting examination marks. MLflow records the important information associated with each experiment, including:

- Model parameters
- Evaluation metrics
- Dataset artifact
- Trained model
- Run metadata
- Tags

The project is designed for learning MLOps concepts on Windows and is intentionally small enough to run on a normal laptop.

## MLOps Objective

During machine learning development, many model configurations may be tested.

Without experiment tracking, it becomes difficult to remember:

- Which model was trained
- Which hyperparameters were used
- Which dataset was used
- Which metrics were obtained
- Where the trained model was stored

MLflow Tracking provides a structured way to record this information for every run.

According to the MLflow documentation, an experiment groups related runs, while each run records metadata such as parameters, metrics, and artifacts. MLflow can also log trained models. 

## Project Workflow

```text
Student Dataset
      |
      v
Train Multiple Models
      |
      +-------------------+
      |                   |
      v                   v
Linear Regression   Decision Tree
      |                   |
      +---------+---------+
                |
                v
        Random Forest
                |
                v
          MLflow Tracking
                |
        +-------+-------+
        |       |       |
        v       v       v
     Params  Metrics  Models
                |
                v
          MLflow UI
```

## Models

The project compares three simple regression approaches:

1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor

The goal is to demonstrate experiment tracking, not to build a production-quality marks prediction system.

## Dataset

The dataset contains 15 synthetic student records.

### Features

| Feature | Description |
|---|---|
| `student_id` | Student identifier |
| `attendance` | Attendance percentage |
| `study_hours` | Average study hours |
| `assignment_score` | Assignment score |
| `marks` | Examination marks / target |

The dataset is synthetic and is intended only for learning.

## Project Structure

```text
mlops-mlflow-experiment-tracking/
│
├── data/
│   └── raw/
│       └── students_mlflow.csv
│
├── src/
│   ├── train.py
│   └── load_model.py
│
├── mlflow.db                # Generated locally; ignored by Git
├── mlartifacts/             # Generated locally; ignored by Git
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows Setup

Open PowerShell from the project directory.

### 1. Create virtual environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for the current user, use:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Verify MLflow:

```powershell
mlflow --version
```

## Run the Experiments

From the project root:

```powershell
python src\train.py
```

The script performs three MLflow runs.

Each run logs:

### Parameters

Examples:

```text
algorithm
max_depth
n_estimators
test_size
random_state
dataset
```

### Metrics

```text
MAE
RMSE
R2 Score
```

### Artifacts

```text
Dataset
Trained model
Model metadata
```

MLflow's scikit-learn integration supports automatic logging, but this project intentionally uses explicit `log_params`, `log_metric`, and `log_model` calls so that the core tracking API is visible and easy to understand.

## Launch MLflow UI

After running the training script:

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Open the following in your browser:

```text
http://127.0.0.1:5000
```

You should see the:

```text
Student Marks Prediction
```

experiment.

Inside it, you should see multiple runs.

## What to Inspect in the MLflow UI

For each run, inspect:

### Parameters

Compare:

```text
algorithm
max_depth
n_estimators
test_size
random_state
```

### Metrics

Compare:

```text
mae
rmse
r2_score
```

### Artifacts

Open:

```text
dataset/
model/
```

The trained model is stored as an MLflow model artifact.

## Load a Tracked Model

The project includes:

```text
src/load_model.py
```

Run:

```powershell
python src\load_model.py
```

The script searches the MLflow experiment for the run with the lowest recorded RMSE, loads that run's model, and performs a sample prediction.

## Important MLflow Concepts

### Experiment

An experiment groups related machine learning runs.

Example:

```text
Student Marks Prediction
```

### Run

A run represents one execution of a training experiment.

For example:

```text
Run 1 → Linear Regression
Run 2 → Decision Tree
Run 3 → Random Forest
```

### Parameter

A parameter is an input or configuration value.

Example:

```text
max_depth = 5
n_estimators = 100
```

### Metric

A metric measures model performance.

Example:

```text
RMSE = ...
R2 = ...
```

### Artifact

An artifact is a file generated or used by the run.

Examples:

```text
trained model
dataset
plots
configuration files
```

## Why Experiment Tracking Matters

Suppose five models are trained manually.

Without tracking:

```text
Model 1 → What parameters?
Model 2 → Which dataset?
Model 3 → Which model performed better?
Model 4 → Where is the model file?
Model 5 → What changed?
```

With MLflow:

```text
Experiment
   |
   +-- Run 1
   |    +-- Parameters
   |    +-- Metrics
   |    +-- Artifacts
   |
   +-- Run 2
   |    +-- Parameters
   |    +-- Metrics
   |    +-- Artifacts
   |
   +-- Run 3
        +-- Parameters
        +-- Metrics
        +-- Artifacts
```

This makes experiments easier to reproduce and compare.

## Manual Logging vs Autologging

This project uses manual logging because it is useful for learning the fundamentals:

```python
mlflow.log_param(...)
mlflow.log_metric(...)
mlflow.sklearn.log_model(...)
```

MLflow also provides scikit-learn autologging:

```python
mlflow.sklearn.autolog()
```

Autologging can automatically capture parameters, metrics, models, and related information for supported scikit-learn workflows.

## Reproducibility

The project records:

- Dataset used
- Model type
- Hyperparameters
- Random seed
- Evaluation metrics
- Trained model

For a larger production project, experiment tracking would normally be combined with:

- Git
- DVC
- CI/CD
- Model registry
- Containerization
- Monitoring

## Relationship With the Previous DVC Assignment

This assignment complements the previous:

**Dataset Versioning Using DVC**

DVC answers:

> Which version of the dataset was used?

MLflow answers:

> Which experiment, parameters, metrics, and model were produced?

Together:

```text
Git
 |
 +-- Code Version
 |
 +-- DVC Metadata
 |      |
 |      +-- Dataset Version
 |
 +-- MLflow
        |
        +-- Experiment
        +-- Parameters
        +-- Metrics
        +-- Model
```

This is an important foundation of an MLOps workflow.

## Limitations

The student dataset is intentionally tiny and synthetic.

Therefore:

- Metrics are not statistically meaningful for real-world deployment.
- The dataset is not representative of real student populations.
- The model should not be used for real academic decisions.
- The project exists to demonstrate MLflow experiment tracking.

## Learning Outcomes

After completing this assignment, you should understand:

- What MLflow is
- What an MLflow experiment is
- What an MLflow run is
- How to log parameters
- How to log metrics
- How to log artifacts
- How to log a scikit-learn model
- How to view experiments in MLflow UI
- How to load a tracked model
- How MLflow complements DVC and Git

## Useful Commands

Start training:

```powershell
python src\train.py
```

Start MLflow UI:

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Load a tracked model:

```powershell
python src\load_model.py
```

Check installed version:

```powershell
mlflow --version
```

## Conclusion

This project demonstrates the fundamental MLflow Tracking workflow by running multiple machine learning experiments and recording their parameters, metrics, dataset artifact, and trained models.

It provides a simple foundation for more advanced MLOps workflows involving DVC, model registries, CI/CD, deployment, and monitoring.
