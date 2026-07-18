from pathlib import Path
import sys

import pandas as pd


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[3])
)


from src.utils.database import engine



def build_github_topics():

    print("🔄 Construyendo silver.github_topics...")


    query = """
        SELECT *
        FROM bronze.github_raw
    """


    df = pd.read_sql(
        query,
        engine
    )


    if df.empty:
        raise Exception(
            "❌ bronze.github_raw está vacío"
        )


    print(
        f"📦 Repositorios encontrados: {len(df)}"
    )


    # Nos quedamos solo con lo necesario
    df = df[
        [
            "id",
            "name",
            "full_name",
            "technology",
            "topics"
        ]
    ]


    # Eliminamos repos sin topics
    df = df.dropna(
        subset=["topics"]
    )


    rows = []


    for _, row in df.iterrows():

        topics = row["topics"]


        # PostgreSQL puede devolver array o string
        if isinstance(topics, str):

            topics = (
                topics
                .replace("{", "")
                .replace("}", "")
                .split(",")
            )


        for topic in topics:

            topic = topic.strip()


            if topic:

                rows.append(
                    {
                        "repository_id": row["id"],
                        "repo_name": row["name"],
                        "full_name": row["full_name"],
                        "technology": row["technology"],
                        "topic": topic.lower()
                    }
                )


    silver_df = pd.DataFrame(rows)


    if silver_df.empty:
        raise Exception(
            "❌ No se encontraron topics"
        )


    # Limpieza final

    silver_df = silver_df.drop_duplicates(
        subset=[
            "repository_id",
            "topic"
        ]
    )


    print(
        f"✨ Topics generados: {len(silver_df)}"
    )


    with engine.begin() as conn:

        conn.execute(
            """
            TRUNCATE TABLE silver.github_topics;
            """
        )


    silver_df.to_sql(
        "github_topics",
        engine,
        schema="silver",
        if_exists="append",
        index=False
    )


    print(
        "✅ silver.github_topics cargada correctamente"
    )