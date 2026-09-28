import pandas as pd
from pathlib import Path
def check_data(input_path):
    p=Path(input_path)
    if not p.exists(): raise FileNotFoundError(f"Raw dataset not found: {p}")
    df=pd.read_csv(p)
    if df.empty: raise ValueError("Raw dataset is empty.")
    r={"rows":len(df),"columns":len(df.columns),"duplicate_rows":int(df.duplicated().sum()),"missing_cells":int(df.isna().sum().sum())}
    print(r); return r
if __name__=="__main__": check_data("data/raw/ecommerce_orders.csv")
