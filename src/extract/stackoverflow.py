from pathlib import Path

import pandas as pd

from src.database import engine

DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "stackoverflow"
    / "survey_results_public.csv"
)


def extract_stackoverflow():

    df = pd.read_csv(DATA_PATH, low_memory=False)

    print(df.shape)

    df.to_sql(
        "stackoverflow_raw",
        engine,
        schema="bronze",
        if_exists="replace",
        index=False,
        chunksize=1000,
    )

    print("Datos cargados en bronze.stackoverflow_raw")


if __name__ == "__main__":
    extract_stackoverflow()