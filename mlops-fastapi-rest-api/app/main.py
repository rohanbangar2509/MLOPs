from fastapi import FastAPI, HTTPException
from app.model import predict
from app.schemas import StudentInput, PredictionResponse

app = FastAPI(
    title="Student Performance Prediction API",
    description="REST API for serving a machine-learning model that predicts whether a student will pass.",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "Student Performance Prediction API",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}

@app.get("/model-info")
def model_info():
    return {
        "model": "RandomForestClassifier",
        "task": "Binary classification",
        "target": "passed",
        "features": [
            "study_hours",
            "attendance_pct",
            "previous_score",
            "assignments_completed",
            "sleep_hours",
        ],
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_student(student: StudentInput):
    try:
        values = student.model_dump()
        passed, probability = predict(values)
        return {
            "passed": passed,
            "prediction": "Pass" if passed else "Fail",
            "probability": round(probability, 4),
            "model": "RandomForestClassifier",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")
