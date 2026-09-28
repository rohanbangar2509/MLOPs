from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Student Performance Prediction API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_model_info():
    response = client.get("/model-info")
    assert response.status_code == 200
    assert response.json()["target"] == "passed"

def test_prediction():
    payload = {
        "study_hours": 7,
        "attendance_pct": 90,
        "previous_score": 78,
        "assignments_completed": 9,
        "sleep_hours": 7,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["passed"] in [0, 1]
    assert 0 <= body["probability"] <= 1
    assert body["prediction"] in ["Pass", "Fail"]

def test_validation():
    payload = {
        "study_hours": 30,
        "attendance_pct": 90,
        "previous_score": 78,
        "assignments_completed": 9,
        "sleep_hours": 7,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
