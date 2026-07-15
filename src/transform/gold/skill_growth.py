from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[2])
)

from utils.database import engine


def build_skill_growth():

    query = """
        SELECT
            response_id,
            skill,
            category,
            relation
        FROM silver.skills
    """

    df = pd.read_sql(query, engine)

    have_worked = (
        df[df["relation"] == "HaveWorked"]
        .groupby(["skill", "category"])["response_id"]
        .nunique()
        .reset_index(name="have_worked")
    )

    want_to_work = (
        df[df["relation"] == "WantToWork"]
        .groupby(["skill", "category"])["response_id"]
        .nunique()
        .reset_index(name="want_to_work")
    )

    growth = have_worked.merge(
        want_to_work,
        on=["skill", "category"],
        how="outer"
    )

    growth = growth.fillna(0)

    growth["growth_score"] = (
        growth["want_to_work"]
        /
        (growth["have_worked"] + 1)
    ) * np.log1p(growth["have_worked"])

    growth = growth.sort_values(
        "growth_score",
        ascending=False
    ).reset_index(drop=True)

    growth["rank"] = growth.index + 1

    growth.to_sql(
        "skill_growth",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )


def main():
    build_skill_growth()


if __name__ == "__main__":
    main()