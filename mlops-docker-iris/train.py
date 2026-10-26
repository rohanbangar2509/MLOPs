"""Train a small educational Iris KNN model using only Python's standard library."""
import json
from pathlib import Path

MODEL_PATH = Path("/app/model.json")

# 15 illustrative Iris measurements in cm: [sepal length, sepal width, petal length, petal width]
TRAINING_DATA = [
    ([5.1, 3.5, 1.4, 0.2], "setosa"),
    ([4.9, 3.0, 1.4, 0.2], "setosa"),
    ([4.7, 3.2, 1.3, 0.2], "setosa"),
    ([5.0, 3.6, 1.4, 0.2], "setosa"),
    ([5.4, 3.9, 1.7, 0.4], "setosa"),
    ([5.0, 2.0, 3.5, 1.0], "versicolor"),
    ([5.9, 3.0, 4.2, 1.5], "versicolor"),
    ([6.0, 2.9, 4.5, 1.5], "versicolor"),
    ([6.1, 2.8, 4.0, 1.3], "versicolor"),
    ([5.6, 2.9, 3.6, 1.3], "versicolor"),
    ([6.3, 3.3, 6.0, 2.5], "virginica"),
    ([5.8, 2.7, 5.1, 1.9], "virginica"),
    ([7.1, 3.0, 5.9, 2.1], "virginica"),
    ([6.5, 3.0, 5.8, 2.2], "virginica"),
    ([6.7, 3.3, 5.7, 2.1], "virginica"),
]

def main():
    artifact = {
        "algorithm": "K-Nearest Neighbours (KNN)",
        "k": 3,
        "feature_names": [
            "sepal length (cm)", "sepal width (cm)",
            "petal length (cm)", "petal width (cm)"
        ],
        "training_data": [
            {"features": x, "label": label} for x, label in TRAINING_DATA
        ],
        "classes": ["setosa", "versicolor", "virginica"],
        "note": "Educational model trained on 15 illustrative samples, not the full Iris dataset."
    }
    MODEL_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print("=== Iris KNN training ===")
    print(f"Algorithm: {artifact['algorithm']}")
    print(f"Training samples: {len(TRAINING_DATA)}")
    print(f"Classes: {', '.join(artifact['classes'])}")
    print(f"Saved model artifact to {MODEL_PATH}")
    print("Training complete; no third-party packages required.")

if __name__ == "__main__":
    main()
