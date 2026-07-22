from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from src.utils.database import engine


def build_silver_papers():

    print("🔄 Construyendo silver.papers...")

    query = """
        SELECT *
        FROM bronze.arxiv_raw
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        raise Exception("❌ bronze.arxiv_raw está vacío")

    print(f"📦 Registros bronze: {len(df)}")

    # Renombrar columnas
    df = df.rename(
        columns={
            "id": "paper_id"
        }
    )

    # Seleccionar columnas
    columns = [
        "paper_id",
        "technology",
        "title",
        "summary",
        "authors",
        "categories",
        "primary_category",
        "published",
        "updated",
        "pdf_url"
    ]

    df = df[[col for col in columns if col in df.columns]]

    # Eliminar duplicados
    df = df.drop_duplicates(
        subset=["paper_id", "technology"]
    )

    # Limpieza de texto
    text_columns = [
        "technology",
        "title",
        "summary",
        "primary_category",
        "pdf_url"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # Fechas
    date_columns = [
        "published",
        "updated"
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
            TRUNCATE TABLE silver.papers;
            """
        )

    df.to_sql(
        "papers",
        engine,
        schema="silver",
        if_exists="append",
        index=False
    )

    print(
        "✅ silver.papers cargada correctamente"
    )