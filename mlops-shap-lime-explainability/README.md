# MLOps Assignment: SHAP/LIME for Explainability

This project trains a machine-learning classifier and explains its predictions using **SHAP** and **LIME**.

## What you will demonstrate
- Train and evaluate a reproducible scikit-learn model.
- Use SHAP to explain global feature importance and one individual prediction.
- Use LIME to explain one individual prediction.
- Save plots, metrics, and example explanations to `artifacts/`.
- Compare SHAP and LIME in a short assignment report.

> Dataset: scikit-learn's built-in Wisconsin Breast Cancer dataset. It downloads no external data and is used here as a standard educational benchmark. This is a learning demo, not a medical diagnostic tool.

## 1. Prerequisites
- Python 3.10 or 3.11 recommended
- pip
- (Optional) Git and GitHub

## 2. Create and activate a virtual environment (Windows PowerShell)

Open PowerShell in this project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.11` is not available, use `python -m venv .venv` with a supported Python version. If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Run the project

Run these commands from the project root, in this order:

```powershell
python src/train_model.py
python src/explain_model.py
```

The first script trains a Random Forest model and writes the model, metrics, and dataset metadata to `artifacts/`. The second generates SHAP and LIME explanations and saves plots and a text summary.

## 4. Expected output

After both commands, `artifacts/` should contain:
- `model.joblib` — trained model bundle (model + feature names + target labels)
- `metrics.json` — test accuracy, precision, recall, F1, and ROC-AUC
- `feature_importance.csv` — Random Forest feature importance
- `shap_summary.png` — global SHAP summary plot
- `shap_local.png` — SHAP explanation for one test row
- `lime_local.html` — interactive LIME explanation (open in a browser)
- `lime_local.png` — LIME explanation image, when supported by your environment
- `explanation_summary.txt` — short generated summary for the selected example

If a SHAP plot differs slightly between library versions, that is normal.

## 5. How to explain the results in your submission

1. **Model performance:** quote values from `artifacts/metrics.json`. Do not claim a score before running the code.
2. **SHAP global explanation:** inspect `shap_summary.png`. Features near the top have larger average absolute SHAP impact on the model output.
3. **SHAP local explanation:** inspect `shap_local.png`. It explains the model output for one selected test sample.
4. **LIME local explanation:** open `lime_local.html`. LIME fits a simple local surrogate around the selected sample; the weights indicate which features support or oppose the selected class locally.
5. **Comparison:** SHAP uses a game-theoretic feature attribution framework; LIME approximates the model locally with an interpretable surrogate. They can produce different rankings because their assumptions and sampling methods differ.

## 6. Troubleshooting

### Dependency installation fails
Use Python 3.11 in a fresh `.venv`, upgrade pip, then install requirements. Avoid installing into a global Python environment.

### SHAP fails while creating plots
Try:
```powershell
python -m pip install --upgrade shap matplotlib numpy
```
Then rerun `python src/explain_model.py`.

### LIME HTML is created but PNG is missing
This is acceptable: HTML is the primary LIME output and opens in a browser. PNG export depends on optional plotting support.

### Script cannot find `model.joblib`
Run `python src/train_model.py` before `python src/explain_model.py`.

## 7. Suggested submission checklist
- [ ] `README.md`
- [ ] `requirements.txt`
- [ ] Source code under `src/`
- [ ] Generated metrics and explanation plots under `artifacts/`
- [ ] Screenshots of terminal runs and the plots
- [ ] A 1–2 page report describing model, metrics, SHAP, LIME, and limitations

## 8. Git (optional)
From the project root:
```powershell
git init
git add README.md requirements.txt .gitignore src
git commit -m "Add SHAP and LIME explainability assignment"
```
You can choose whether to commit generated artifacts. For a clean source repository, keep the model bundle out of Git and commit selected report figures instead.
