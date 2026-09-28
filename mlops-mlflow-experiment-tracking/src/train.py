from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "students_mlflow.csv"

# MLflow 3.x: use SQLite instead of the legacy filesystem backend
MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"
MLFLOW_DB_URI = f"sqlite:///{MLFLOW_DB_PATH.as_posix()}"

mlflow.set_tracking_uri(MLFLOW_DB_URI)

EXPERIMENT_NAME = "Student Marks Prediction"

mlflow.set_experiment(EXPERIMENT_NAME)


# ============================================================
# DATA LOADING
# ============================================================

def load_data():
    """Load the student dataset and separate features and target."""

    df = pd.read_csv(DATA_PATH)

    features = [
        "attendance",
        "study_hours",
        "assignment_score",
    ]

    target = "marks"

    X = df[features]
    y = df[target]

    return X, y


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_model(model, X_test, y_test):
    """Calculate regression evaluation metrics."""

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    return mae, rmse, r2


# ============================================================
# MLflow EXPERIMENT
# ============================================================

def run_experiment(run_name, model, model_params):
    """Train, evaluate and log one ML experiment to MLflow."""

    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    with mlflow.start_run(run_name=run_name):

        # ----------------------------------------------------
        # Log parameters
        # ----------------------------------------------------

        mlflow.log_params(model_params)

        mlflow.log_param(
            "test_size",
            0.2
        )

        mlflow.log_param(
            "random_state",
            42
        )

        mlflow.log_param(
            "dataset",
            DATA_PATH.name
        )

        # ----------------------------------------------------
        # Train model
        # ----------------------------------------------------

        model.fit(
            X_train,
            y_train
        )

        # ----------------------------------------------------
        # Evaluate model
        # ----------------------------------------------------

        mae, rmse, r2 = evaluate_model(
            model,
            X_test,
            y_test
        )

        # ----------------------------------------------------
        # Log metrics
        # ----------------------------------------------------

        mlflow.log_metric(
            "mae",
            mae
        )

        mlflow.log_metric(
            "rmse",
            rmse
        )

        mlflow.log_metric(
            "r2_score",
            r2
        )

        # ----------------------------------------------------
        # Log dataset
        # ----------------------------------------------------

        mlflow.log_artifact(
            DATA_PATH,
            artifact_path="dataset"
        )

        # ----------------------------------------------------
        # Log trained model
        # ----------------------------------------------------
        #
        # MLflow 3.x uses skops serialization for sklearn
        # models in this environment.
        #
        # DecisionTreeRegressor and RandomForestRegressor
        # internally use sklearn.tree._tree.Tree.
        #
        # The models are created and trained locally in this
        # trusted assignment, so we explicitly allow this
        # specific type.
        # ----------------------------------------------------

        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            skops_trusted_types=[
                "sklearn.tree._tree.Tree"
            ],
        )

        # ----------------------------------------------------
        # Add useful MLflow tags
        # ----------------------------------------------------

        mlflow.set_tag(
            "project",
            "MLOps MLflow Experiment Tracking"
        )

        mlflow.set_tag(
            "task",
            "Student Marks Regression"
        )

        mlflow.set_tag(
            "model_type",
            type(model).__name__
        )

        # ----------------------------------------------------
        # Console output
        # ----------------------------------------------------

        print()
        print(f"Run: {run_name}")
        print(f"Model: {type(model).__name__}")
        print(f"MAE: {mae:.4f}")
        print(f"RMSE: {rmse:.4f}")
        print(f"R2 Score: {r2:.4f}")
        print(f"Model URI: {model_info.model_uri}")

        return {
            "run_name": run_name,
            "model": type(model).__name__,
            "mae": mae,
            "rmse": rmse,
            "r2_score": r2,
        }


# ============================================================
# MAIN
# ============================================================

def main():

    experiments = [

        # ----------------------------------------------------
        # Experiment 1: Linear Regression
        # ----------------------------------------------------

        (
            "Linear Regression",

            Pipeline(
                [
                    (
                        "scaler",
                        StandardScaler()
                    ),

                    (
                        "model",
                        LinearRegression()
                    ),
                ]
            ),

            {
                "algorithm": "LinearRegression",
            },
        ),

        # ----------------------------------------------------
        # Experiment 2: Decision Tree
        # ----------------------------------------------------

        (
            "Decision Tree Depth 3",

            DecisionTreeRegressor(
                max_depth=3,
                random_state=42,
            ),

            {
                "algorithm": "DecisionTreeRegressor",
                "max_depth": 3,
            },
        ),

        # ----------------------------------------------------
        # Experiment 3: Random Forest
        # ----------------------------------------------------

        (
            "Random Forest 100 Trees",

            RandomForestRegressor(
                n_estimators=100,
                max_depth=5,
                random_state=42,
            ),

            {
                "algorithm": "RandomForestRegressor",
                "n_estimators": 100,
                "max_depth": 5,
            },
        ),
    ]

    results = []

    for run_name, model, params in experiments:

        results.append(
            run_experiment(
                run_name,
                model,
                params
            )
        )

    # --------------------------------------------------------
    # Experiment summary
    # --------------------------------------------------------

    results_df = pd.DataFrame(results)

    print()
    print("=" * 70)
    print("EXPERIMENT SUMMARY")
    print("=" * 70)

    print(
        results_df.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()