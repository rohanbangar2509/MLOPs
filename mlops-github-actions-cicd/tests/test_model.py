"""Tests for the Iris model training pipeline."""

import joblib
import numpy as np

from src.train import MINIMUM_ACCURACY, MODEL_PATH, train_model


def test_model_trains_and_meets_accuracy_threshold():
    model, accuracy = train_model()

    assert accuracy >= MINIMUM_ACCURACY
    assert hasattr(model, "predict")


def test_model_predicts_three_iris_classes():
    model, _ = train_model()
    predictions = model.predict(
        np.array(
            [
                [5.1, 3.5, 1.4, 0.2],
                [6.0, 2.9, 4.5, 1.5],
                [6.5, 3.0, 5.5, 1.8],
            ]
        )
    )

    assert set(predictions).issubset({0, 1, 2})
    assert len(predictions) == 3


def test_saved_artifact_can_be_loaded(tmp_path, monkeypatch):
    model, _ = train_model()
    artifact_path = tmp_path / "iris_model.joblib"
    joblib.dump(model, artifact_path)

    loaded_model = joblib.load(artifact_path)
    prediction = loaded_model.predict([[5.1, 3.5, 1.4, 0.2]])

    assert len(prediction) == 1
    assert MODEL_PATH.name == "iris_model.joblib"
