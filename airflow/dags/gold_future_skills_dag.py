from datetime import datetime
from pathlib import Path
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path("/opt/airflow")

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.transform.gold.skill_trends import main as build_skill_trends
from src.transform.gold.skill_growth import main as build_skill_growth


default_args = {
    "owner": "airflow",
}


with DAG(
    dag_id="gold_future_skills",
    default_args=default_args,
    description="Build Gold layer for Future Skills Engine",
    start_date=datetime(2026, 7, 1),
    schedule="@daily",
    catchup=False,
    tags=["gold", "future-skills"],
) as dag:

    build_skill_trends_task = PythonOperator(
        task_id="build_skill_trends",
        python_callable=build_skill_trends,
    )

    build_skill_growth_task = PythonOperator(
        task_id="build_skill_growth",
        python_callable=build_skill_growth,
    )

    # Orden de ejecución
    build_skill_trends_task >> build_skill_growth_task