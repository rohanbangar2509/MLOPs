"""The prepared deterministic learning dataset is included in data/raw.
This file documents that the dataset is synthetic and intentionally impure.
Run feature_pipeline.py to use it."""
from pathlib import Path
def main():
    p=Path("data/raw/ecommerce_orders_impure.csv")
    print(f"Prepared dataset: {p}")
    print("Regeneration is intentionally omitted here; the exact dataset used for the assignment is versioned with the project.")
if __name__=="__main__": main()
