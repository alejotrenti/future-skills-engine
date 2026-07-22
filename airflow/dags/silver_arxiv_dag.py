from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform.silver.build_papers import build_silver_papers


default_args = {
    "owner": "Alejo",
    "retries": 1,
}


with DAG(
    dag_id="silver_arxiv",
    default_args=default_args,
    description="Transforma arXiv Bronze hacia Silver",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["silver", "arxiv"],
) as dag:


    papers_task = PythonOperator(
        task_id="build_papers",
        python_callable=build_silver_papers,
    )