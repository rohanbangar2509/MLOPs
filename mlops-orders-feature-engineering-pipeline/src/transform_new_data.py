from pathlib import Path
import joblib, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
PIPELINE=ROOT/"artifacts/orders_feature_engineering_pipeline.joblib"
def main():
    pipe=joblib.load(PIPELINE)
    row=pd.DataFrame([{
        "order_id":"NEW00001","order_date":"2025-08-12","customer_id":"CUST0042","customer_age":29,
        "customer_gender":" male ","city":" pune ","state":"Maharashtra","category":"electronics ",
        "product":"Wireless Mouse","quantity":2,"unit_price":799,"discount_pct":10,"payment_method":"upi ",
        "shipping_type":" express ","delivery_days":4,"customer_rating":5,"returned":"No",
        "order_status":"Delivered","total_amount":1438.20
    }])
    out=pipe.transform(row); names=pipe.named_steps["preprocessor"].get_feature_names_out()
    print("New order transformed successfully.")
    print(f"Input shape: {row.shape}"); print(f"Output shape: {out.shape}")
    print("\nFirst 12 transformed features:")
    print(pd.DataFrame(out,columns=names).iloc[:,:12].to_string(index=False))
if __name__=="__main__": main()
