import pandas as pd, numpy as np
from pathlib import Path
def build_features(input_path,output_path):
    df=pd.read_csv(input_path,parse_dates=["order_date"])
    for c in ["quantity","unit_price","discount_pct","delivery_days","customer_age"]:
        df[c]=df[c].fillna(df[c].median())
    df["order_date"]=df["order_date"].fillna(df["order_date"].median())
    df["gross_amount"]=df["quantity"]*df["unit_price"]
    df["discount_amount"]=df["gross_amount"]*df["discount_pct"]/100
    df["calculated_net_amount"]=df["gross_amount"]-df["discount_amount"]
    df["order_year"]=df.order_date.dt.year
    df["order_month"]=df.order_date.dt.month
    df["order_quarter"]=df.order_date.dt.quarter
    df["order_day_of_week"]=df.order_date.dt.dayofweek
    df["is_weekend"]=(df.order_day_of_week>=5).astype(int)
    df["age_group"]=pd.cut(df.customer_age,bins=[0,25,35,50,200],labels=["18-25","26-35","36-50","51+"]).astype("string").fillna("36-50")
    df["delivery_delay_days"]=df.delivery_days-3
    df["delivery_delay_flag"]=(df.delivery_delay_days>0).astype(int)
    df["high_discount_flag"]=(df.discount_pct>=20).astype(int)
    df["quantity_per_1000_value"]=df.quantity/(df.calculated_net_amount/1000).replace(0,np.nan)
    df["quantity_per_1000_value"]=df["quantity_per_1000_value"].replace([np.inf,-np.inf],np.nan).fillna(0)
    df["days_since_order"]=(df.order_date-df.order_date.min()).dt.days
    df=df.drop(columns=["order_id","customer_id","order_date"])
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(output_path,index=False)
    return {"rows":len(df),"columns":len(df.columns)}
if __name__=="__main__": build_features("data/processed/orders_cleaned.csv","data/processed/orders_features.csv")
