import pandas as pd
import numpy as np
from pathlib import Path

RULES={"customer_age":(18,100),"quantity":(1,50),"unit_price":(.01,100000),"discount_pct":(0,80),"delivery_days":(0,30),"customer_rating":(1,5)}
def clean_orders(input_path, output_path):
    df=pd.read_csv(input_path); before=len(df); df=df.drop_duplicates().copy()
    for c in ["city","state","category","product","payment_method","shipping_type","customer_gender","order_status"]:
        df[c]=df[c].astype("string").str.strip().str.replace(r"\s+"," ",regex=True)
    for c,(lo,hi) in RULES.items():
        df[c]=pd.to_numeric(df[c],errors="coerce"); df.loc[~df[c].between(lo,hi),c]=np.nan
    df["order_date"]=pd.to_datetime(df["order_date"],errors="coerce")
    Path(output_path).parent.mkdir(parents=True,exist_ok=True); df.to_csv(output_path,index=False)
    return {"input_rows":before,"output_rows":len(df),"duplicates_removed":before-len(df),"missing_cells":int(df.isna().sum().sum())}
