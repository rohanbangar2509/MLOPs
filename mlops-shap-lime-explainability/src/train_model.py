"""Train and evaluate a Random Forest classifier for the SHAP/LIME assignment."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def main() -> None:
    dataset = load_breast_cancer(as_frame=True)
    X = dataset.data
    y = dataset.target
    feature_names = list(X.columns)
    target_names = list(dataset.target_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("classifier", RandomForestClassifier(
                n_estimators=250, random_state=42, class_weight="balanced"
            )),
        ]
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]
    metrics = {
        "model": "RandomForestClassifier",
        "dataset": "Wisconsin Breast Cancer (scikit-learn built-in)",
        "test_rows": int(len(X_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1_score": float(f1_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "random_state": 42,
    }

    joblib.dump(
        {
            "model": model,
            "feature_names": feature_names,
            "target_names": target_names,
            "X_test": X_test,
            "y_test": y_test,
            "X_train": X_train,
        },
        ARTIFACTS / "model.joblib",
    )
    (ARTIFACTS / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    classifier = model.named_steps["classifier"]
    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": classifier.feature_importances_,
    }).sort_values("importance", ascending=False)
    importance.to_csv(ARTIFACTS / "feature_importance.csv", index=False)

    print("Training complete.")
    print(json.dumps(metrics, indent=2))
    print(f"\nSaved model and metrics to: {ARTIFACTS}")


if __name__ == "__main__":
    main()
