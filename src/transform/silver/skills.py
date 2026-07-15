import pandas as pd

from src.utils.database import engine


SKILL_CONFIG = {

    "LanguageHaveWorkedWith": {
        "category": "Language",
        "relation": "HaveWorked"
    },

    "LanguageWantToWorkWith": {
        "category": "Language",
        "relation": "WantToWork"
    },

    "DatabaseHaveWorkedWith": {
        "category": "Database",
        "relation": "HaveWorked"
    },

    "DatabaseWantToWorkWith": {
        "category": "Database",
        "relation": "WantToWork"
    },

    "PlatformHaveWorkedWith": {
        "category": "Platform",
        "relation": "HaveWorked"
    },

    "PlatformWantToWorkWith": {
        "category": "Platform",
        "relation": "WantToWork"
    },

    "WebframeHaveWorkedWith": {
        "category": "Framework",
        "relation": "HaveWorked"
    },

    "WebframeWantToWorkWith": {
        "category": "Framework",
        "relation": "WantToWork"
    },

    "AIModelsHaveWorkedWith": {
        "category": "AI Model",
        "relation": "HaveWorked"
    },

    "AIModelsWantToWorkWith": {
        "category": "AI Model",
        "relation": "WantToWork"
    }
}

def extract_bronze_stackoverflow():

    columns = [
        "ResponseId",
        *SKILL_CONFIG.keys()
    ]

    query = f"""
    SELECT
        {','.join(f'"{col}"' for col in columns)}
    FROM bronze.stackoverflow_raw;
    """

    return pd.read_sql(query, engine)



def normalize_skills(df):

    skills = []

    for column, config in SKILL_CONFIG.items():

        temp = df[
            [
                "ResponseId",
                column
            ]
        ].copy()

        temp = temp.dropna()

        temp[column] = temp[column].str.split(";")

        temp = temp.explode(column)

        temp["source"] = "stackoverflow"

        temp["category"] = config["category"]

        temp["relation"] = config["relation"]

        temp = temp.rename(
            columns={
                "ResponseId": "response_id",
                column: "skill"
            }
        )

        skills.append(temp)


    final_df = pd.concat(
        skills,
        ignore_index=True
    )


    print("Antes de limpiar:", len(final_df))

    final_df["skill"] = final_df["skill"].str.strip()

    print(
        "Duplicados encontrados:",
        final_df.duplicated().sum()
    )

    final_df = final_df.drop_duplicates()

    print("Después de limpiar:", len(final_df))


    return final_df[
        [
            "source",
            "response_id",
            "skill",
            "category",
            "relation"
        ]
    ]

def load_silver_skills(df):

    df.to_sql(
        name="skills",
        con=engine,
        schema="silver",
        if_exists="replace",
        index=False,
        chunksize=1000,
    )



def main():

    bronze_df = extract_bronze_stackoverflow()

    print(
        f"Bronze registros: {len(bronze_df)}"
    )

    skills_df = normalize_skills(bronze_df)

    print(skills_df.head())

    load_silver_skills(skills_df)

    print(
        f"✔ silver.skills cargado: {len(skills_df)} registros"
    )


if __name__ == "__main__":
    main()