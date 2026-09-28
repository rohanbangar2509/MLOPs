# MLOps — REST API Using FastAPI

## Objective

Build a production-style REST API using **FastAPI** to expose a trained machine-learning model.

The API accepts student academic information and returns a prediction of whether the student is likely to pass.

## Architecture

```text
Client
  |
  | HTTP POST /predict
  v
FastAPI
  |
  v
Pydantic Validation
  |
  v
Random Forest Model
  |
  v
JSON Prediction
```

## Project Structure

```text
mlops-fastapi-rest-api/

├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── model.py
│   └── schemas.py
├── data/
│   └── student_performance.csv
├── models/
│   ├── student_performance_model.joblib
│   └── metrics.json
├── scripts/
│   └── train_model.py
├── tests/
│   └── test_api.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Dataset

The project uses a synthetic student-performance dataset with 1,200 records.

### Features

- `study_hours`
- `attendance_pct`
- `previous_score`
- `assignments_completed`
- `sleep_hours`

### Target

- `passed` — `1` for Pass and `0` for Fail

The model is a `RandomForestClassifier`.

## Installation

From PowerShell, create and activate a dedicated virtual environment:

```powershell
cd "D:\TY Sem-I\MLOPs Assignements\mlops-fastapi-rest-api"

python -m venv .venv

.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Train the Model

The trained model is included in the project, but the training script is also provided for reproducibility.

Run:

```powershell
python scripts/train_model.py
```

This creates:

```text
models/student_performance_model.joblib
models/metrics.json
```

## Start the API

From the project root:

```powershell
fastapi dev app/main.py
```

Alternatively:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Interactive Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

### Alternative ReDoc Documentation

```text
http://127.0.0.1:8000/redoc
```

FastAPI automatically generates OpenAPI documentation and provides interactive API testing through Swagger UI.

## API Endpoints

### 1. Root

```http
GET /
```

Example response:

```json
{
  "message": "Student Performance Prediction API",
  "docs": "/docs",
  "health": "/health"
}
```

### 2. Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 3. Model Information

```http
GET /model-info
```

Returns information about the model, prediction task, target, and features.

### 4. Prediction

```http
POST /predict
```

Request body:

```json
{
  "study_hours": 7,
  "attendance_pct": 90,
  "previous_score": 78,
  "assignments_completed": 9,
  "sleep_hours": 7
}
```

Example response:

```json
{
  "passed": 1,
  "prediction": "Pass",
  "probability": 0.96,
  "model": "RandomForestClassifier"
}
```

The exact probability depends on the trained model.

## Input Validation

The API uses Pydantic models to validate incoming request data.

Validation constraints:

```text
study_hours: 0–24
attendance_pct: 0–100
previous_score: 0–100
assignments_completed: 0–20
sleep_hours: 0–24
```

Invalid requests receive an HTTP `422 Unprocessable Entity` response.

## Testing

The project includes automated API tests.

Run:

```powershell
python -m pytest
```

Using `python -m pytest` ensures that pytest runs with the active Python virtual environment.

The tests verify:

- Root endpoint
- Health endpoint
- Model information endpoint
- Successful prediction
- Invalid input handling

Expected result:

```text
5 passed
```

## Example cURL Request

On Windows PowerShell:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{"study_hours":7,"attendance_pct":90,"previous_score":78,"assignments_completed":9,"sleep_hours":7}'
```

## MLOps Concepts Demonstrated

This project demonstrates:

- REST API development
- ML model serving
- FastAPI
- Pydantic request validation
- OpenAPI documentation
- Model serialization with Joblib
- Health checks
- API testing
- Separation of API and model logic
- Reproducible model training

## Git Integration

This assignment belongs inside the existing parent Git repository:

```text
D:\TY Sem-I\MLOPs Assignements
```

**Do not run `git init` inside this assignment.**

From PowerShell:

```powershell
cd "D:\TY Sem-I\MLOPs Assignements"

git status

git add mlops-fastapi-rest-api

git status

git commit -m "Added FastAPI REST API assignment"

git push
```

Before committing, verify that generated caches and virtual environments are ignored by `.gitignore`.

## Verification

The implementation has been verified with:

- FastAPI application import
- Successful model loading
- Automated API tests
- Swagger/OpenAPI documentation
- REST prediction endpoint

The automated test suite currently reports:

```text
5 passed
```

## Learning Outcome

The main objective is to understand how a machine-learning model can be exposed as a REST service.

The completed workflow is:

```text
Dataset
   ↓
Model Training
   ↓
Saved ML Model
   ↓
FastAPI Application
   ↓
Pydantic Validation
   ↓
Prediction Endpoint
   ↓
JSON Response
```
