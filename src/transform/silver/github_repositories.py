from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.utils.database import engine


def build_silver_github():

    print("🔄 Construyendo silver.github_repositories...")


    query = """
        SELECT *
        FROM bronze.github_raw
    """


    df = pd.read_sql(query, engine)


    if df.empty:
        raise Exception("❌ bronze.github_raw está vacío")


    print(f"📦 Registros bronze: {len(df)}")


    # Renombrar columnas
    df = df.rename(
        columns={
            "id": "repository_id",
            "name": "repo_name",
            "stargazers_count": "stars",
            "forks_count": "forks",
            "watchers_count": "watchers",
            "open_issues_count": "open_issues"
        }
    )


    columns = [
        "repository_id",
        "technology",
        "repo_name",
        "full_name",
        "owner",
        "description",
        "language",
        "stars",
        "forks",
        "watchers",
        "open_issues",
        "license",
        "topics",
        "created_at",
        "updated_at",
        "pushed_at"
    ]


    df = df[
        [col for col in columns if col in df.columns]
    ]


    # Eliminar repos repetidos
    df = df.drop_duplicates(
        subset=["full_name"]
    )


    # Limpieza texto
    text_columns = [
        "repo_name",
        "full_name",
        "owner",
        "language",
        "license"
    ]


    for col in text_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .fillna("Unknown")
                .astype(str)
            )


    # Métricas numéricas
    numeric_columns = [
        "stars",
        "forks",
        "watchers",
        "open_issues"
    ]


    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)


    # Fechas
    date_columns = [
        "created_at",
        "updated_at",
        "pushed_at"
    ]


    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )


    print(f"✨ Registros silver: {len(df)}")


    with engine.begin() as conn:

        conn.execute(
            """
            TRUNCATE TABLE silver.github_repositories;
            """
        )


    df.to_sql(
        "github_repositories",
        engine,
        schema="silver",
        if_exists="append",
        index=False
    )


    print(
        "✅ silver.github_repositories cargada correctamente"
    )