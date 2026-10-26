"""Generate global and local SHAP/LIME explanations."""
from __future__ import annotations

import json
import warnings
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from lime.lime_tabular import LimeTabularExplainer

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
ARTIFACTS.mkdir(exist_ok=True)


def positive_class_shap_values(explainer, X_sample: pd.DataFrame):
    """Normalize SHAP output across common SHAP versions for binary classifiers."""
    values = explainer.shap_values(X_sample)
    if isinstance(values, list):
        # Binary classification: SHAP often returns one array per class.
        return values[1] if len(values) > 1 else values[0]

    values = np.asarray(values)
    # Newer SHAP versions may return (rows, features, classes).
    if values.ndim == 3:
        return values[:, :, 1] if values.shape[2] > 1 else values[:, :, 0]
    return values


def main() -> None:
    model_path = ARTIFACTS / "model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            "Model not found. Run `python src/train_model.py` first."
        )

    bundle = joblib.load(model_path)
    model = bundle["model"]
    feature_names = bundle["feature_names"]
    target_names = bundle["target_names"]
    X_train = bundle["X_train"]
    X_test = bundle["X_test"]
    y_test = bundle["y_test"]

    # Keep a small, fixed sample for quick, repeatable explanation generation.
    X_explain = X_test.iloc[: min(80, len(X_test))].copy()
    row = X_test.iloc[[0]].copy()
    predicted_class = int(model.predict(row)[0])
    probabilities = model.predict_proba(row)[0]
    predicted_label = target_names[predicted_class]

    # SHAP: explain the Random Forest classifier within the fitted pipeline.
    classifier = model.named_steps["classifier"]
    imputer = model.named_steps["imputer"]
    X_train_transformed = pd.DataFrame(
        imputer.transform(X_train), columns=feature_names, index=X_train.index
    )
    X_explain_transformed = pd.DataFrame(
        imputer.transform(X_explain), columns=feature_names, index=X_explain.index
    )
    row_transformed = pd.DataFrame(
        imputer.transform(row), columns=feature_names, index=row.index
    )

    explainer = shap.TreeExplainer(classifier)
    shap_values = positive_class_shap_values(explainer, X_explain_transformed)
    row_values = positive_class_shap_values(explainer, row_transformed)

    plt.figure()
    shap.summary_plot(
        shap_values, X_explain_transformed, show=False, max_display=15
    )
    plt.tight_layout()
    plt.savefig(ARTIFACTS / "shap_summary.png", dpi=160, bbox_inches="tight")
    plt.close("all")

    # A simple local bar chart works across SHAP versions and clearly shows direction.
    local_values = np.asarray(row_values)[0]
    local_df = pd.DataFrame({
        "feature": feature_names,
        "shap_value": local_values,
        "abs_shap_value": np.abs(local_values),
    }).sort_values("abs_shap_value", ascending=False).head(12).sort_values("shap_value")
    plt.figure(figsize=(9, 6))
    plt.barh(local_df["feature"], local_df["shap_value"])
    plt.axvline(0, linewidth=1)
    plt.xlabel("SHAP value (class 1 output)")
    plt.title("Local SHAP explanation — selected test row")
    plt.tight_layout()
    plt.savefig(ARTIFACTS / "shap_local.png", dpi=160, bbox_inches="tight")
    plt.close("all")

    # LIME explains the full pipeline via predict_proba, using original feature values.
    lime_explainer = LimeTabularExplainer(
        training_data=np.asarray(X_train, dtype=float),
        feature_names=feature_names,
        class_names=target_names,
        mode="classification",
        discretize_continuous=True,
        random_state=42,
    )
    lime_exp = lime_explainer.explain_instance(
        data_row=np.asarray(row.iloc[0], dtype=float),
        predict_fn=model.predict_proba,
        num_features=10,
        num_samples=3000,
        labels=[predicted_class],
    )
    lime_exp.save_to_file(str(ARTIFACTS / "lime_local.html"))

    try:
        fig = lime_exp.as_pyplot_figure(label=predicted_class)
        fig.tight_layout()
        fig.savefig(ARTIFACTS / "lime_local.png", dpi=160, bbox_inches="tight")
        plt.close(fig)
    except Exception as exc:
        warnings.warn(f"LIME PNG could not be generated; HTML is available. Details: {exc}")

    explanation = lime_exp.as_list(label=predicted_class)
    summary_lines = [
        "SHAP/LIME Explainability Summary",
        "================================",
        f"Selected test row index: {row.index[0]}",
        f"Actual class: {target_names[int(y_test.iloc[0])]}",
        f"Predicted class: {predicted_label}",
        "Class probabilities:",
    ]
    summary_lines.extend(
        f"  {target_names[i]}: {probabilities[i]:.4f}"
        for i in range(len(probabilities))
    )
    summary_lines.append("")
    summary_lines.append("Top local LIME conditions and weights:")
    summary_lines.extend(f"  {condition}: {weight:+.4f}" for condition, weight in explanation)
    summary_lines += [
        "",
        "Interpretation notes:",
        "- SHAP global summary ranks features by their contribution magnitude across the sample.",
        "- Positive/negative local SHAP values indicate direction relative to class 1 output.",
        "- LIME weights describe a local surrogate model and are not guaranteed to match SHAP.",
        "- This is an educational benchmark, not a medical diagnostic tool.",
    ]
    (ARTIFACTS / "explanation_summary.txt").write_text(
        "\n".join(summary_lines), encoding="utf-8"
    )

    print("Explainability generation complete.")
    print(f"Predicted class: {predicted_label}")
    print(f"Class probabilities: {np.round(probabilities, 4).tolist()}")
    print(f"Saved plots and explanations to: {ARTIFACTS}")


if __name__ == "__main__":
    main()
