from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform.bronze.b_stackoverflow import load_bronze_stackoverflow

default_args = {
    "owner": "Alejo",
    "retries": 1,
}


with DAG(
    dag_id="bronze_stackoverflow",
    default_args=default_args,
    description="Carga del dataset StackOverflow a Bronze",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["bronze", "stackoverflow"],
) as dag:

    load_bronze = PythonOperator(
        task_id="load_stackoverflow_bronze",
        python_callable=load_bronze_stackoverflow,
    )

    load_bronze