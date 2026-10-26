"""Train and validate a small Iris classification model."""

from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

MODEL_PATH = Path("artifacts/iris_model.joblib")
RANDOM_STATE = 42
MINIMUM_ACCURACY = 0.90


def train_model():
    """Train the classifier and return the fitted model and test accuracy."""
    iris = load_iris()
    features_train, features_test, labels_train, labels_test = train_test_split(
        iris.data,
        iris.target,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=iris.target,
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=RANDOM_STATE,
    )
    model.fit(features_train, labels_train)
    predictions = model.predict(features_test)
    accuracy = accuracy_score(labels_test, predictions)

    return model, accuracy


def main():
    """Train, validate, and save the model artifact."""
    model, accuracy = train_model()
    print(f"Test accuracy: {accuracy:.3f}")

    if accuracy < MINIMUM_ACCURACY:
        raise SystemExit(
            f"Model validation failed: accuracy {accuracy:.3f} "
            f"is below {MINIMUM_ACCURACY:.2f}"
        )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
