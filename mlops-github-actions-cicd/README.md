# MLOps CI/CD with GitHub Actions — Iris Classifier

A beginner-friendly MLOps assignment demonstrating automated linting, tests, model training,
model validation, and model artifact upload with GitHub Actions.

## Pipeline behavior

On every push to `main` and every pull request targeting `main`, GitHub Actions:
1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs pinned dependencies.
4. Runs Ruff lint checks.
5. Runs pytest unit tests.
6. Trains the Iris classifier and validates its accuracy.
7. Uploads `artifacts/iris_model.joblib` as a downloadable workflow artifact.

This is CI plus model packaging (continuous delivery of an artifact), not deployment to a live server.

## Project structure

```text
mlops-github-actions-cicd/
├── .github/
│   └── workflows/
│       └── ml-ci-cd.yml
├── artifacts/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   └── train.py
├── tests/
│   └── test_model.py
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Run locally on Windows PowerShell

From this project directory:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest -v
python -m src.train
```

If PowerShell blocks activation, use this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The trained model is written to `artifacts/iris_model.joblib`. The generated model is ignored by Git; GitHub Actions uploads it as a workflow artifact.

## Push to GitHub

Create an empty GitHub repository named `mlops-github-actions-cicd` (do not add a README or license if you already have these files locally), then run:

```powershell
git init
git add .
git commit -m "Add Iris model CI/CD pipeline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/mlops-github-actions-cicd.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

If Git says `remote origin already exists`, run `git remote -v` and update it with:
`git remote set-url origin https://github.com/YOUR-USERNAME/mlops-github-actions-cicd.git`

If your remote repository already contains commits, fetch and integrate them before pushing; do not force-push blindly.

## Verify GitHub Actions

1. Open your repository on GitHub.
2. Select **Actions**.
3. Open **MLOps CI/CD - Iris Classifier**.
4. Open the latest run and confirm all steps are green.
5. At the bottom of the successful run, download the `iris-model` artifact.
6. Make a small code change, commit, and push again to demonstrate that the workflow runs automatically.

## Assignment explanation

- **Continuous Integration (CI):** every push/pull request automatically checks code quality and runs tests.
- **Model validation:** the workflow trains the model and fails if test accuracy is below the defined threshold.
- **Continuous Delivery (CD):** after successful validation, the model file is packaged and uploaded as an artifact.
- **GitHub Actions:** hosted automation executes the workflow without requiring a local runner.
- **Artifact:** a downloadable output retained with the workflow run for a limited period according to GitHub's artifact retention settings.

## Notes

- The Iris dataset is loaded from scikit-learn, so no dataset download or API key is needed.
- Do not commit `.venv/`, caches, or generated model binaries.
- For production use, add model versioning, security scanning, deployment approval, monitoring, and a real deployment target.
