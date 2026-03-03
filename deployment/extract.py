import os
import pandas as pd
from sqlalchemy import create_engine

RAW_PATH = "/opt/airflow/data/raw"

DB_URL = "postgresql://airflow:airflow@postgres:5432/olist_raw"

RAW_TABLES = {
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv"
}

def extract_to_raw_db():

    engine = create_engine(DB_URL)

    for table_name, file_name in RAW_TABLES.items():

        file_path = os.path.join(RAW_PATH, file_name)

        print(f"Loading {table_name}...")

        df = pd.read_csv(file_path, encoding="latin1")

        df.to_sql(
            table_name,
            engine,
            if_exists="replace",  # safe for dev
            index=False
        )

        print(f"{table_name} loaded successfully.")