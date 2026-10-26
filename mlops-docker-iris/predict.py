"""Predict an Iris species using the saved KNN model."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

MODEL_PATH = Path("/app/model.json")

def predict(features, artifact):
    distances = []
    for row in artifact["training_data"]:
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(features, row["features"])))
        distances.append((distance, row["label"]))
    distances.sort(key=lambda item: item[0])
    closest = distances[:artifact["k"]]
    votes = Counter(label for _, label in closest)
    best_count = max(votes.values())
    tied = {label for label, count in votes.items() if count == best_count}
    winner = next(label for _, label in closest if label in tied)
    return winner, votes[winner] / artifact["k"], closest

def main():
    parser = argparse.ArgumentParser(description="Predict an Iris species from four measurements (cm).")
    parser.add_argument("sepal_length", type=float)
    parser.add_argument("sepal_width", type=float)
    parser.add_argument("petal_length", type=float)
    parser.add_argument("petal_width", type=float)
    args = parser.parse_args()
    features = [args.sepal_length, args.sepal_width, args.petal_length, args.petal_width]
    if any(not math.isfinite(x) or x <= 0 or x > 10 for x in features):
        parser.error("Measurements must be finite, greater than 0, and no more than 10 cm.")

    artifact = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    species, vote_share, closest = predict(features, artifact)
    print("\n=== Iris Flower Prediction ===")
    for name, value in zip(artifact["feature_names"], features):
        print(f"{name}: {value} cm")
    print(f"Algorithm: {artifact['algorithm']} (k={artifact['k']})")
    print(f"Predicted species: {species}")
    print(f"Nearest-neighbour vote share: {vote_share:.0%}")
    print("\nNearest training examples:")
    for distance, label in closest:
        print(f"  class={label}, distance={distance:.3f}")
    print("\nNote: this demo uses 15 illustrative training samples, not the full Iris dataset.")

if __name__ == "__main__":
    main()
