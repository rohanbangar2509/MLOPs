from pathlib import Path

import mlflow
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"
MLFLOW_DB_URI = f"sqlite:///{MLFLOW_DB_PATH.as_posix()}"

mlflow.set_tracking_uri(MLFLOW_DB_URI)


def main():
    client = mlflow.MlflowClient()

    experiment = client.get_experiment_by_name("Student Marks Prediction")

    if experiment is None:
        raise RuntimeError(
            "Experiment not found. Run src/train.py first."
        )

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.rmse ASC"],
        max_results=1,
    )

    if not runs:
        raise RuntimeError("No MLflow runs found.")

    best_run = runs[0]
    run_id = best_run.info.run_id
    model_uri = f"runs:/{run_id}/model"

    model = mlflow.sklearn.load_model(model_uri)

    sample = pd.DataFrame(
        [
            {
                "attendance": 93,
                "study_hours": 8,
                "assignment_score": 92,
            }
        ]
    )

    prediction = model.predict(sample)[0]

    print(f"Best run ID: {run_id}")
    print(f"Model URI: {model_uri}")
    print(f"Predicted marks: {prediction:.2f}")


if __name__ == "__main__":
    main()
