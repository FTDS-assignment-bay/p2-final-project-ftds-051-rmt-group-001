import sys
import os

sys.path.append("/opt/airflow/deployment")

import pandas as pd
from sqlalchemy import create_engine

import pendulum
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator


from extract import extract_to_raw_db
from transform import transform_and_load

local_tz = pendulum.timezone("Asia/Jakarta")

RAW_DB = "postgresql://airflow:airflow@postgres:5432/olist_raw"

def check_data_availability():
    """
    Check if raw tables contain data.
    If no data exists, pipeline will be skipped.
    
    Return of the functions
    True → continue DAG
    False → skip downstream tasks
    """

    engine = create_engine(RAW_DB)

    query = """
    SELECT COUNT(*) as row_count
    FROM orders
    """

    result = pd.read_sql(query, engine)
    count = result.iloc[0]["row_count"]

    if count == 0:
        print("No data detected in raw tables. Skipping pipeline.")
        return False

    print(f"{count} rows detected in raw tables. Pipeline will run.")
    return True

with DAG(
    dag_id="olist_star_schema_etl",
    start_date=datetime(2024, 1, 1, tzinfo=local_tz),
    schedule="0 2 * * *",
    catchup=False,
    tags=["olist", "etl"],
) as dag:
    
    check_data = ShortCircuitOperator(
        task_id="check_data_availability",
        python_callable=check_data_availability
    )

    extract_task = PythonOperator(
        task_id="extract_raw_data",
        python_callable=extract_to_raw_db,
    )

    transform_task = PythonOperator(
        task_id="transform_validate_and_load",
        python_callable=transform_and_load,
    )

    check_data >> extract_task >> transform_task