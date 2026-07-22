from src.extract.arxiv import extract_arxiv
from src.utils.database import engine


def load_bronze_arxiv():

    df = extract_arxiv()

    print(f"Extrayendo {len(df)} registros...")

    df.to_sql(
        name="arxiv_raw",
        con=engine,
        schema="bronze",
        if_exists="replace",
        index=False,
        chunksize=1000,
    )

    print("✔ Bronze arXiv cargado correctamente")


if __name__ == "__main__":
    load_bronze_arxiv()