import pandas as pd, json
from pathlib import Path
REQUIRED=["gross_amount","discount_amount","calculated_net_amount","order_year","order_month","order_quarter","is_weekend","age_group","delivery_delay_flag","high_discount_flag","days_since_order"]
def validate_data(input_path,report_path):
    df=pd.read_csv(input_path)
    missing=[c for c in REQUIRED if c not in df.columns]
    numeric_required=[c for c in REQUIRED if c not in ["age_group"]]
    nulls=int(df[numeric_required].isna().sum().sum()) if not missing else -1
    passed=len(df)>0 and not missing and nulls==0
    r={"status":"PASS" if passed else "FAIL","rows":len(df),"columns":len(df.columns),"missing_required_columns":missing,"null_cells_in_required_features":nulls}
    Path(report_path).parent.mkdir(parents=True,exist_ok=True)
    Path(report_path).write_text(json.dumps(r,indent=2),encoding="utf-8")
    print(json.dumps(r,indent=2))
    if not passed: raise ValueError(r)
    return r
if __name__=="__main__": validate_data("data/processed/orders_features.csv","reports/validation_report.json")
