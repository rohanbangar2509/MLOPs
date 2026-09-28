from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "student_performance.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "student_performance_model.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

FEATURES = [
    "study_hours",
    "attendance_pct",
    "previous_score",
    "assignments_completed",
    "sleep_hours",
]

def train():
    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y = df["passed"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metrics = {
        "model": "RandomForestClassifier",
        "n_estimators": 200,
        "accuracy": round(float(accuracy), 4),
        "features": FEATURES,
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(json.dumps(metrics, indent=2))
    print("\nClassification report:")
    print(classification_report(y_test, predictions))

if __name__ == "__main__":
    train()
