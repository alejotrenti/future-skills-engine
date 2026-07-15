from pathlib import Path
import sys

import pandas as pd

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[2])
)

from utils.database import engine


def build_skill_trends():

    query = """
        SELECT
            response_id,
            skill,
            category
        FROM silver.skills
        WHERE relation = 'HaveWorked'
    """

    df = pd.read_sql(query, engine)


    trends = (
        df
        .groupby(["skill", "category"])
        ["response_id"]
        .nunique()
        .reset_index()
    )

    trends.rename(
        columns={
            "response_id": "users_count"
        },
        inplace=True
    )


    trends = trends.sort_values(
        "users_count",
        ascending=False
    )


    trends["rank"] = range(
        1,
        len(trends)+1
    )


    with engine.begin() as conn:
        conn.execute("TRUNCATE TABLE gold.skill_trends")

    trends.to_sql(
        "skill_trends",
        engine,
        schema="gold",
        if_exists="append",
        index=False
    )


def main():
    build_skill_trends()


if __name__ == "__main__":
    main()