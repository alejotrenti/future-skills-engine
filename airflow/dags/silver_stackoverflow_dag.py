from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.transform.silver.respondents import main as build_respondents
from src.transform.silver.skills import main as build_skills


default_args = {
    "owner": "Alejo",
    "retries": 1,
}


with DAG(
    dag_id="silver_stackoverflow",
    default_args=default_args,
    description="Transforma StackOverflow Bronze hacia Silver",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
    tags=["silver", "stackoverflow"],
) as dag:


    respondents_task = PythonOperator(
        task_id="build_respondents",
        python_callable=build_respondents,
    )


    skills_task = PythonOperator(
        task_id="build_skills",
        python_callable=build_skills,
    )


    respondents_task >> skills_task