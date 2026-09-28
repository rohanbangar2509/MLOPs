from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from scripts.pipeline_components import clean_orders
if __name__=="__main__": print(clean_orders(ROOT/"data/raw/ecommerce_orders.csv",ROOT/"data/processed/orders_cleaned.csv"))
