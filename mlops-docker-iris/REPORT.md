# MLOps Practical Assignment

## Title
Containerize a Machine Learning Model Using Docker

## Aim
To package a simple Iris classification model and prediction program into a Docker image.

## Objectives
1. Implement a simple supervised learning algorithm.
2. Save the model artifact.
3. Build a Docker image.
4. Run inference inside a container.

## Software Requirements
- Windows PowerShell
- Docker Desktop with Linux container support
- Python 3.11 base image (downloaded by Docker if not cached)

## Theory
Docker packages application code and runtime requirements into an image. A container is a running instance of an image. This project uses K-nearest neighbours (KNN), which predicts a class by finding the nearest training examples and selecting the majority class.

To avoid downloading third-party machine-learning libraries, the implementation uses Python's standard library. The model is built from 15 illustrative Iris measurements embedded in the training script, not the full 150-sample Iris dataset.

## Procedure
1. Start Docker Desktop.
2. Open PowerShell in the project folder.
3. Run `docker build --progress=plain -t iris-classifier .`.
4. Confirm the build output says the model artifact was saved.
5. Run `docker run --rm iris-classifier 5.1 3.5 1.4 0.2`.
6. Record the predicted species.
7. Verify the image with `docker images`.

## Result
Complete after execution: The Docker image was built and the container predicted an Iris species from four measurements.

## Conclusion
This assignment demonstrates model artifact creation, Docker image building, and containerized inference without installing third-party Python packages.

## Evidence to attach
- Screenshot of `docker --version`
- Screenshot of successful `docker build`
- Screenshot of prediction output
- Screenshot of `docker images`
- Record the actual output observed; do not invent results.
