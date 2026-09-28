from pathlib import Path
import joblib, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from pipeline_components import OrdersDataCleaner, OrderFeatureEngineer

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/raw/ecommerce_orders_impure.csv"
ARTIFACT=ROOT/"artifacts/orders_feature_engineering_pipeline.joblib"
TRAIN=ROOT/"data/processed/X_train_transformed.csv"
TEST=ROOT/"data/processed/X_test_transformed.csv"

def build_pipeline():
    numeric=["customer_age","quantity","unit_price","discount_pct","delivery_days","customer_rating","total_amount",
             "gross_amount","discount_amount","calculated_net_amount","order_year","order_month","order_quarter",
             "order_day_of_week","is_weekend","delivery_delay_days","delivery_delay_flag","high_discount_flag",
             "quantity_per_1000_value","days_since_order"]
    categorical=["customer_gender","city","state","category","product","payment_method","shipping_type","order_status","returned","age_group"]
    num=Pipeline([("imputer",SimpleImputer(strategy="median")),("scaler",RobustScaler())])
    cat=Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore",sparse_output=False))])
    pre=ColumnTransformer([("numeric",num,numeric),("categorical",cat,categorical)])
    return Pipeline([("cleaner",OrdersDataCleaner()),("feature_engineering",OrderFeatureEngineer()),("preprocessor",pre)])

def main():
    df=pd.read_csv(DATA)
    print("="*72); print("RAW E-COMMERCE DATA QUALITY"); print("="*72)
    print(f"Raw rows: {len(df)}"); print(f"Raw columns: {len(df.columns)}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Missing cells before cleaning: {df.isna().sum().sum()}")
    # This assignment focuses on preprocessing, not model training.
    # Therefore there is no prediction target. We still split the raw
    # records before fitting preprocessing to avoid leakage.
    X=df.copy()
    Xtr,Xte=train_test_split(X,test_size=.20,random_state=42)
    pipe=build_pipeline()
    Xt=pipe.fit_transform(Xtr); Xv=pipe.transform(Xte)
    names=pipe.named_steps["preprocessor"].get_feature_names_out()
    TRAIN.parent.mkdir(parents=True,exist_ok=True); ARTIFACT.parent.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(Xt,columns=names).to_csv(TRAIN,index=False)
    pd.DataFrame(Xv,columns=names).to_csv(TEST,index=False)
    joblib.dump(pipe,ARTIFACT)
    print("\n"+"="*72); print("PIPELINE RESULT"); print("="*72)
    print(f"Training rows: {len(Xtr)}"); print(f"Testing rows: {len(Xte)}")
    print(f"Output feature count: {Xt.shape[1]}")
    print(f"Training feature matrix: {Xt.shape}"); print(f"Testing feature matrix: {Xv.shape}")
    print(f"Saved pipeline: {ARTIFACT}")
if __name__=="__main__": main()
