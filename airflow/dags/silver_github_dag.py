from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform.silver.github_repositories import build_silver_github
from src.transform.silver.github_topics import build_github_topics


default_args = {
    "owner": "Alejo",
    "retries": 1,
}


with DAG(
    dag_id="silver_github",
    default_args=default_args,
    description="Transforma GitHub Bronze hacia Silver",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["silver", "github"],
) as dag:


    repositories_task = PythonOperator(
        task_id="build_github_repositories",
        python_callable=build_silver_github,
    )


    topics_task = PythonOperator(
        task_id="build_github_topics",
        python_callable=build_github_topics,
    )


    repositories_task >> topics_task