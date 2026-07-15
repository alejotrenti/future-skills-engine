import pandas as pd

from src.utils.database import engine


RESPONDENT_COLUMNS = {
    "ResponseId": "response_id",
    "Country": "country",
    "Age": "age",
    "EdLevel": "education",
    "Employment": "employment",
    "YearsCode": "years_code",
    "WorkExp": "work_exp",
    "DevType": "dev_type",
    "RemoteWork": "remote_work",
    "Industry": "industry",
    "ConvertedCompYearly": "salary_usd",
    "JobSat": "job_satisfaction",
}


def extract_bronze_stackoverflow():

    query = """
    SELECT
        "ResponseId",
        "Country",
        "Age",
        "EdLevel",
        "Employment",
        "YearsCode",
        "WorkExp",
        "DevType",
        "RemoteWork",
        "Industry",
        "ConvertedCompYearly",
        "JobSat"
    FROM bronze.stackoverflow_raw;
    """

    return pd.read_sql(query, engine)


def transform_respondents(df):

    respondents = (
        df
        .rename(columns=RESPONDENT_COLUMNS)
        .copy()
    )

    respondents.insert(
        1,
        "source",
        "stackoverflow"
    )

    return respondents


def load_silver_respondents(df):

    df.to_sql(
        name="respondents",
        con=engine,
        schema="silver",
        if_exists="replace",
        index=False,
        chunksize=1000,
    )


def main():

    bronze_df = extract_bronze_stackoverflow()

    print(f"Bronze registros: {len(bronze_df)}")

    silver_df = transform_respondents(bronze_df)

    print(silver_df.head())

    load_silver_respondents(silver_df)

    print(
        f"✔ silver.respondents cargado: {len(silver_df)} registros"
    )


if __name__ == "__main__":
    main()