import pandas as pd
from sqlalchemy import create_engine, text
import great_expectations as gx

RAW_DB = "postgresql://airflow:airflow@postgres:5432/olist_raw"
PROCESSED_DB = "postgresql://airflow:airflow@postgres:5432/olist_processed"

def run_gx_validation(df):

    context = gx.get_context()

    data_source = context.data_sources.add_pandas(name="datasource")
    data_asset = data_source.add_dataframe_asset(name="dataframe")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("batch_definition")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})
    validator = context.get_validator(batch=batch)

    # validator = gx.from_pandas(df)

    validator.expect_column_values_to_not_be_null("order_id")
    validator.expect_column_values_to_not_be_null("customer_id")
    validator.expect_column_values_to_be_between("total_items", min_value=1)
    validator.expect_column_values_to_be_between("total_order_value", min_value=0)
    validator.expect_column_values_to_be_in_set("is_canceled", [0, 1])

    results = validator.validate()

    if not results["success"]:
        raise ValueError("GX validation failed. Pipeline stopped.")

    print("GX validation passed.")

def add_is_canceled(df):
    df["is_canceled"] = 0
    df.loc[df["order_status"] == "canceled", "is_canceled"] = 1
    return df

def transform_and_load():

    raw_engine = create_engine(RAW_DB)
    processed_engine = create_engine(PROCESSED_DB)

    # -----------------------------
    # 1. READ RAW TABLES
    # -----------------------------
    orders = pd.read_sql("SELECT * FROM orders", raw_engine)
    order_items = pd.read_sql("SELECT * FROM order_items", raw_engine)
    payments = pd.read_sql("SELECT * FROM order_payments", raw_engine)
    customers = pd.read_sql("SELECT * FROM customers", raw_engine)

    # -----------------------------
    # 2. AGGREGATION (YOUR LOGIC)
    # -----------------------------
    order_agg = order_items.groupby("order_id").agg(
        total_items=("order_item_id", "count"),
        total_order_value=("price", "sum"),
        total_freight=("freight_value", "sum"),
        avg_item_price=("price", "mean")
    ).reset_index()

    payments_agg = payments.groupby("order_id").agg(
        payment_type=("payment_type", lambda x: x.mode()[0]),
        total_payment_value=("payment_value", "sum"),
        max_installments=("payment_installments", "max")
    ).reset_index()

    df_agg = orders.merge(order_agg, on="order_id")
    df_agg = df_agg.merge(payments_agg, on="order_id")
    df_agg = df_agg.merge(customers, on="customer_id")

    df_agg = add_is_canceled(df_agg)

    run_gx_validation(df_agg)

    # Convert timestamps
    timestamp_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in timestamp_cols:
        df_agg[col] = pd.to_datetime(df_agg[col])

    # -----------------------------
    # 3. TRUNCATE TABLES
    # -----------------------------
    with processed_engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE fact_orders RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_customer RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_order_status RESTART IDENTITY CASCADE;"))
        conn.execute(text("TRUNCATE TABLE dim_payment_type RESTART IDENTITY CASCADE;"))

    # -----------------------------
    # 4. LOAD DIMENSIONS
    # -----------------------------
    dim_customer = df_agg[[
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state"
    ]].drop_duplicates()

    dim_customer.to_sql(
        "dim_customer",
        processed_engine,
        if_exists="append",
        index=False
    )

    dim_status = df_agg[["order_status"]].drop_duplicates()
    dim_status.to_sql(
        "dim_order_status",
        processed_engine,
        if_exists="append",
        index=False
    )

    dim_payment = df_agg[["payment_type"]].drop_duplicates()
    dim_payment.to_sql(
        "dim_payment_type",
        processed_engine,
        if_exists="append",
        index=False
    )

    # -----------------------------
    # 5. MAP SURROGATE KEYS
    # -----------------------------
    dim_customer_db = pd.read_sql("SELECT * FROM dim_customer", processed_engine)
    dim_status_db = pd.read_sql("SELECT * FROM dim_order_status", processed_engine)
    dim_payment_db = pd.read_sql("SELECT * FROM dim_payment_type", processed_engine)

    df_agg = df_agg.merge(dim_customer_db, on="customer_id")
    df_agg = df_agg.merge(dim_status_db, on="order_status")
    df_agg = df_agg.merge(dim_payment_db, on="payment_type")

    # -----------------------------
    # 6. PREPARE FACT TABLE
    # -----------------------------
    fact_df = df_agg[[
        "order_id",
        "customer_key",
        "order_status_key",
        "payment_type_key",
        "order_purchase_timestamp",
        "total_items",
        "total_order_value",
        "total_freight",
        "avg_item_price",
        "total_payment_value",
        "max_installments",
        "is_canceled"
    ]]

    fact_df.to_sql(
        "fact_orders",
        processed_engine,
        if_exists="append",
        index=False
    )

    print("Transformation and load completed successfully.")