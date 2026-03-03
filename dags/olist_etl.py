import sys
import os

sys.path.append("/opt/airflow/src")

import pendulum
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from deployment.extract import extract_to_raw_db
from deployment.transform import transform_and_load

local_tz = pendulum.timezone("Asia/Jakarta")

with DAG(
    dag_id="olist_star_schema_etl",
    start_date=datetime(2024, 1, 1, tzinfo=local_tz),
    schedule=None,  # manual trigger
    catchup=False,
    tags=["olist", "etl"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_raw_data",
        python_callable=extract_to_raw_db,
    )

    transform_task = PythonOperator(
        task_id="transform_validate_and_load",
        python_callable=transform_and_load,
    )

    extract_task >> transform_task