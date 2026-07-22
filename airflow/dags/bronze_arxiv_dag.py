from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform.bronze.b_arxiv import load_bronze_arxiv

default_args = {
    "owner": "Alejo",
    "retries": 1,
}

with DAG(
    dag_id="bronze_arxiv",
    default_args=default_args,
    description="Carga de papers de arXiv a Bronze",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["bronze", "arxiv"],
) as dag:

    load_bronze = PythonOperator(
        task_id="load_arxiv_bronze",
        python_callable=load_bronze_arxiv,
    )

    load_bronze