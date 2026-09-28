from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "student_performance_model.joblib"

FEATURES = [
    "study_hours",
    "attendance_pct",
    "previous_score",
    "assignments_completed",
    "sleep_hours",
]

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH}. Run: python scripts/train_model.py"
    )

model = joblib.load(MODEL_PATH)

def predict(values: dict):
    import pandas as pd
    X = pd.DataFrame([values], columns=FEATURES)
    predicted = int(model.predict(X)[0])
    probability = float(model.predict_proba(X)[0][1])
    return predicted, probability
