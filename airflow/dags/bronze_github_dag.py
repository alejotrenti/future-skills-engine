from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform.bronze.b_github import load_bronze_github

default_args = {
    "owner": "Alejo",
    "retries": 1,
}

with DAG(
    dag_id="bronze_github",
    default_args=default_args,
    description="Carga de repositorios de GitHub a Bronze",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["bronze", "github"],
) as dag:

    load_bronze = PythonOperator(
        task_id="load_github_bronze",
        python_callable=load_bronze_github,
    )

    load_bronze