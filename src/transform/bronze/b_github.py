from src.extract.github import extract_github
from src.utils.database import engine


def load_bronze_github():

    df = extract_github()

    print(f"Extrayendo {len(df)} registros...")

    df.to_sql(
        name="github_raw",
        con=engine,
        schema="bronze",
        if_exists="replace",
        index=False,
        chunksize=1000,
    )

    print("✔ Bronze GitHub cargado correctamente")


if __name__ == "__main__":
    load_bronze_github()