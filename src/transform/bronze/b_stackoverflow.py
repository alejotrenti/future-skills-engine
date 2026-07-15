from src.extract.stackoverflow import extract_stackoverflow
from src.utils.database import engine


def load_bronze_stackoverflow():

    df = extract_stackoverflow()

    print(f"Extrayendo {len(df)} registros...")

    df.to_sql(
        name="stackoverflow_raw",
        con=engine,
        schema="bronze",
        if_exists="replace",
        index=False,
        chunksize=1000,
    )

    print("✔ Bronze cargado correctamente")


if __name__ == "__main__":
    load_bronze_stackoverflow()