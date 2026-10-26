# MLOps Docker Assignment — Iris KNN

## Why this version?
The previous Scikit-learn build was slow because pip had to download large compiled packages. This version uses only Python's standard library, so there is no `pip install` step.

It demonstrates the required workflow: train a simple model, save an artifact, build a Docker image, and run predictions in a container.

**Important limitation:** This educational K-nearest-neighbours (KNN) model uses 15 illustrative Iris measurement samples embedded in `train.py`, not the complete 150-row Iris dataset. It demonstrates containerization, not benchmark model performance.

## Requirements
- Docker Desktop running with Linux container support
- Windows PowerShell
- Internet access only if Docker still needs to download `python:3.11-slim`

## Build
Open PowerShell in the extracted project folder (the folder containing `Dockerfile`) and run:

```powershell
docker build --progress=plain -t iris-classifier .
```

The build trains the model and saves `/app/model.json` inside the image. There is no third-party package download.

## Predict
```powershell
docker run --rm iris-classifier 5.1 3.5 1.4 0.2
```

Expected class for this sample: `setosa`.

Try another input:
```powershell
docker run --rm iris-classifier 6.0 2.9 4.5 1.5
```

## Verify
```powershell
docker images
docker ps
docker ps -a
```

`--rm` removes the container after it exits; the image remains.

## Files
- `train.py`: creates the small KNN model artifact.
- `predict.py`: predicts by majority vote among the three nearest examples.
- `requirements.txt`: documents that no third-party dependencies are needed.
- `Dockerfile`: builds the image and runs training during image build.
- `.dockerignore`: excludes unnecessary local files.
- `REPORT.md`: assignment write-up template.

## Troubleshooting
- If Docker is still downloading `python:3.11-slim`, the base image is the remaining network dependency. Wait for it, or check internet access and retry.
- If `iris-classifier` is not found, the image build did not finish successfully. Fix the build first.
- If Docker cannot connect to the daemon, open Docker Desktop and wait for its engine to start.
