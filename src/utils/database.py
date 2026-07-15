import os
from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://airflow:airflow@localhost:5432/airflow"
)


engine = create_engine(DATABASE_URL)