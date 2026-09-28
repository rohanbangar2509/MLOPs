# MLOps: Create Feature Engineering Pipeline

## Objective

Create a reusable **data-cleaning and feature-engineering pipeline** using an approximately 1,800-row e-commerce orders dataset with deliberate data-quality problems.

## Dataset

**Dataset:** E-commerce Orders & Sales  
**Rows:** 1,805 (1,800 base orders + 5 deliberate duplicate records)  
**Columns:** 19

Raw columns:

`order_id`, `order_date`, `customer_id`, `customer_age`, `customer_gender`, `city`, `state`, `category`, `product`, `quantity`, `unit_price`, `discount_pct`, `payment_method`, `shipping_type`, `delivery_days`, `customer_rating`, `returned`, `order_status`, `total_amount`

## Intentional Impurity

The dataset contains:

- missing customer ages
- missing discounts
- missing ratings
- missing delivery days
- invalid numeric values such as `unknown` and `N/A`
- invalid dates
- whitespace and capitalization inconsistencies
- inconsistent category values
- 5 exact duplicate records
- outliers/impossible values such as quantity 100, price 999999, age 125 and delivery 60 days

This gives the assignment reasonable impurity for genuine cleaning practice.

## Cleaning

`OrdersDataCleaner`:

1. Removes exact duplicates.
2. Strips text whitespace.
3. Normalizes categorical values.
4. Converts invalid numeric values to `NaN`.
5. Parses invalid dates as `NaT`.
6. Applies domain validation to impossible values.

## Feature Engineering

The pipeline creates:

### Monetary
- `gross_amount`
- `discount_amount`
- `calculated_net_amount`

### Date
- `order_year`
- `order_month`
- `order_quarter`
- `order_day_of_week`
- `is_weekend`

### Customer
- `age_group`

### Delivery
- `delivery_delay_days`
- `delivery_delay_flag`

### Discount
- `high_discount_flag`

### Other
- `quantity_per_1000_value`
- `days_since_order`

## Preprocessing

Numeric features:

```text
Median imputation
        ↓
RobustScaler
```

Categorical features:

```text
Most-frequent imputation
        ↓
OneHotEncoder(handle_unknown="ignore")
```

## Pipeline

```text
Raw Orders
    ↓
OrdersDataCleaner
    ↓
OrderFeatureEngineer
    ↓
ColumnTransformer
    ├── Numeric → Impute → RobustScaler
    └── Categorical → Impute → OneHotEncoder
    ↓
ML-ready feature matrix
```

## Data Leakage Prevention

The train/test split occurs before fitting the preprocessing pipeline.

Training:

```python
pipeline.fit_transform(X_train, y_train)
```

Testing:

```python
pipeline.transform(X_test)
```

Therefore imputation, scaling and encoding statistics are learned only from training data.

## Project Structure

```text
mlops-orders-feature-engineering-pipeline/
├── data/
│   ├── raw/
│   │   └── ecommerce_orders_impure.csv
│   └── processed/
├── src/
│   ├── pipeline_components.py
│   ├── feature_pipeline.py
│   ├── transform_new_data.py
│   └── generate_dataset.py
├── artifacts/
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows Setup

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python src\feature_pipeline.py
```

Then test reuse:

```powershell
python src\transform_new_data.py
```

## Expected Result

The supplied dataset should report approximately:

```text
Raw rows: 1805
Raw columns: 19
Duplicate rows: 5
Training rows: 1444
Testing rows: 361
```

The final feature count depends on the categories present in the training split, but with this deterministic dataset it is reproducible.

The pipeline saves:

```text
artifacts/orders_feature_engineering_pipeline.joblib
data/processed/X_train_transformed.csv
data/processed/X_test_transformed.csv
```

These generated files are ignored by Git.

## MLOps Relevance

This assignment demonstrates:

- reproducible data cleaning
- feature engineering
- missing-value handling
- invalid-value handling
- outlier-aware preprocessing
- categorical encoding
- train/test separation
- prevention of preprocessing leakage
- reusable preprocessing artifacts

It can later connect with your other assignments:

```text
DVC
  ↓
Versioned Dataset
  ↓
Feature Engineering
  ↓
MLflow
  ↓
Model Training
  ↓
Model Registry
```

## Future Extensions

- DVC-version the order dataset
- Track experiments with MLflow
- Train return/churn/sales models
- Add data validation
- Add CI/CD
- Dockerize the pipeline
- Add data drift monitoring
- Add a feature store
