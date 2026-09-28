import pandas as pd, json
from pathlib import Path
def generate_report(input_path,report_path):
    df=pd.read_csv(input_path); r={"rows":len(df),"columns":len(df.columns),"numeric_columns":len(df.select_dtypes(include="number").columns),"categorical_columns":len(df.select_dtypes(exclude="number").columns),"feature_columns":list(df.columns)}
    Path(report_path).parent.mkdir(parents=True,exist_ok=True); Path(report_path).write_text(json.dumps(r,indent=2),encoding="utf-8"); print(json.dumps(r,indent=2)); return r
if __name__=="__main__": generate_report("data/processed/orders_features.csv","reports/pipeline_summary.json")
