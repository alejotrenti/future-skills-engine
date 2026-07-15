from pathlib import Path
import pandas as pd


DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "raw"
    / "stackoverflow"
    / "survey_results_public.csv"
)


def extract_stackoverflow():

    df = pd.read_csv(
        DATA_PATH,
        low_memory=False
    )

    print(f"Dataset extraído: {df.shape[0]} filas, {df.shape[1]} columnas")

    return df


if __name__ == "__main__":
    extract_stackoverflow()