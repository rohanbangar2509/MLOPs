from pathlib import Path
import sys
import pendulum
from airflow.sdk import dag, task
PROJECT_ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT_ROOT))
from scripts.check_data import check_data
from scripts.pipeline_components import clean_orders
from scripts.feature_engineering import build_features
from scripts.validate_data import validate_data
from scripts.generate_report import generate_report

@dag(dag_id="ecommerce_orders_etl_pipeline",schedule="@daily",start_date=pendulum.datetime(2026,1,1,tz="UTC"),catchup=False,tags=["mlops","etl","feature-engineering"],description="Automated e-commerce ETL workflow")
def ecommerce_orders_etl_pipeline():
    @task
    def check_raw_data(): return check_data(PROJECT_ROOT/"data/raw/ecommerce_orders.csv")
    @task
    def clean(): return clean_orders(PROJECT_ROOT/"data/raw/ecommerce_orders.csv",PROJECT_ROOT/"data/processed/orders_cleaned.csv")
    @task
    def feature_engineering(): return build_features(PROJECT_ROOT/"data/processed/orders_cleaned.csv",PROJECT_ROOT/"data/processed/orders_features.csv")
    @task
    def validate(): return validate_data(PROJECT_ROOT/"data/processed/orders_features.csv",PROJECT_ROOT/"reports/validation_report.json")
    @task
    def report(): return generate_report(PROJECT_ROOT/"data/processed/orders_features.csv",PROJECT_ROOT/"reports/pipeline_summary.json")
    a=check_raw_data(); b=clean(); c=feature_engineering(); d=validate(); e=report()
    a >> b >> c >> d >> e
ecommerce_orders_etl_pipeline()
