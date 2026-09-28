import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class OrdersDataCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self
    def transform(self, X):
        df=X.copy().drop_duplicates().reset_index(drop=True)
        for c in df.select_dtypes(include=["object"]).columns:
            df[c]=df[c].astype("string").str.strip()
        maps={
            "city":{x:x.title() for x in ["pune","mumbai","nashik","nagpur","bengaluru","hyderabad","delhi","jaipur","ahmedabad","chennai"]},
            "category":{x:x.title() for x in ["electronics","home","fashion","beauty","grocery"]},
            "payment_method":{"upi":"UPI","credit card":"Credit Card","debit card":"Debit Card","cash on delivery":"Cash on Delivery","net banking":"Net Banking"},
            "shipping_type":{"standard":"Standard","express":"Express","same day":"Same Day"},
            "customer_gender":{"male":"Male","female":"Female","other":"Other"},
        }
        for c,m in maps.items():
            low=df[c].str.lower(); df[c]=low.map(m).fillna(df[c])
        for c in ["customer_age","quantity","unit_price","discount_pct","delivery_days","customer_rating","total_amount"]:
            df[c]=pd.to_numeric(df[c],errors="coerce")
        df["order_date"]=pd.to_datetime(df["order_date"],errors="coerce")
        rules={
            "customer_age":(18,100),"quantity":(1,50),"unit_price":(.01,100000),
            "discount_pct":(0,80),"delivery_days":(0,30),"customer_rating":(1,5)
        }
        for c,(lo,hi) in rules.items():
            df.loc[(df[c]<lo)|(df[c]>hi),c]=np.nan
        return df

class OrderFeatureEngineer(BaseEstimator, TransformerMixin):
    SNAPSHOT_DATE=pd.Timestamp("2026-01-01")
    def fit(self,X,y=None): return self
    def transform(self,X):
        df=X.copy()
        df["gross_amount"]=df["quantity"]*df["unit_price"]
        df["discount_amount"]=df["gross_amount"]*df["discount_pct"]/100
        df["calculated_net_amount"]=df["gross_amount"]-df["discount_amount"]
        df["order_year"]=df["order_date"].dt.year
        df["order_month"]=df["order_date"].dt.month
        df["order_quarter"]=df["order_date"].dt.quarter
        df["order_day_of_week"]=df["order_date"].dt.dayofweek
        df["is_weekend"]=(df["order_day_of_week"]>=5).astype(int)
        df["age_group"]=pd.cut(df["customer_age"],[17,25,35,50,100],labels=["18-25","26-35","36-50","51+"],include_lowest=True)
        expected=df["shipping_type"].map({"Same Day":1,"Express":3,"Standard":7})
        df["delivery_delay_days"]=df["delivery_days"]-expected
        df["delivery_delay_flag"]=(df["delivery_delay_days"]>0).astype(int)
        df["high_discount_flag"]=(df["discount_pct"]>=20).astype(int)
        df["quantity_per_1000_value"]=df["quantity"]/(df["calculated_net_amount"]/1000).replace(0,np.nan)
        df["days_since_order"]=(self.SNAPSHOT_DATE-df["order_date"]).dt.days
        return df.drop(columns=["order_id","customer_id","order_date"],errors="ignore")
