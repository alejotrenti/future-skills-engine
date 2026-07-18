"""
Construye el índice de tendencias de topics de GitHub.

Versión 1.0:
- Limpieza de topics irrelevantes
- Métricas de popularidad
- Señales recientes
- Trend score compuesto
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.database import engine


IGNORED_TOPICS = {

    # contenido genérico
    "awesome",
    "awesome-list",
    "tutorial",
    "example",
    "examples",
    "beginner",
    "resources",
    "list",
    "documentation",
    "docs",

    # conceptos demasiado genéricos
    "api",
    "apis",
    "web",
    "application",
    "app",
    "software",
    "project",
    "library",
    "framework",
    "development",
    "programming",
    "code",

    # infraestructura demasiado amplia
    "cli",
    "tool",
    "tools"
}


def build_github_topic_trends():

    query = """
        SELECT
            t.topic,
            t.technology AS language,
            r.stars,
            r.forks,
            r.created_at,
            r.pushed_at

        FROM silver.github_topics t

        INNER JOIN silver.github_repositories r

        ON t.repository_id = r.repository_id

        WHERE t.topic IS NOT NULL
    """


    df = pd.read_sql(query, engine)


    if df.empty:
        print("❌ No hay topics disponibles")
        return


    print(
        f"📊 Procesando {len(df)} relaciones topic-repo..."
    )


    # ==========================
    # LIMPIEZA
    # ==========================

    df["topic"] = (
        df["topic"]
        .str.lower()
        .str.strip()
    )


    df = df[
        ~df["topic"].isin(IGNORED_TOPICS)
    ]


    df["stars"] = pd.to_numeric(
        df["stars"],
        errors="coerce"
    ).fillna(0)


    df["forks"] = pd.to_numeric(
        df["forks"],
        errors="coerce"
    ).fillna(0)


    df["created_at"] = pd.to_datetime(
        df["created_at"]
    )


    df["pushed_at"] = pd.to_datetime(
        df["pushed_at"]
    )


    # ==========================
    # MÉTRICAS POR TOPIC
    # ==========================


    trends = (
        df.groupby("topic")
        .agg(
            repo_count=("topic", "count"),
            total_stars=("stars", "sum"),
            total_forks=("forks", "sum"),
            avg_stars=("stars", "mean"),
            avg_forks=("forks", "mean"),
        )
        .reset_index()
    )


    # ==========================
    # LENGUAJES ASOCIADOS
    # ==========================

    languages = (
        df.groupby("topic")["language"]
        .apply(
            lambda x:
            ", ".join(
                sorted(
                    set(
                        x.dropna()
                    )
                )
            )
        )
        .reset_index(
            name="languages"
        )
    )


    trends = trends.merge(
        languages,
        on="topic",
        how="left"
    )


    # ==========================
    # ACTIVIDAD RECIENTE
    # ==========================

    now = pd.Timestamp.now()

    cutoff_1y = (
        now - pd.DateOffset(years=1)
    )

    cutoff_6m = (
        now - pd.DateOffset(months=6)
    )


    recent_created = (
        df[df["created_at"] >= cutoff_1y]
        .groupby("topic")
        .size()
        .reset_index(
            name="recent_repo_count"
        )
    )


    trends = trends.merge(
        recent_created,
        on="topic",
        how="left"
    )


    trends["recent_repo_count"] = (
        trends["recent_repo_count"]
        .fillna(0)
    )


    active = (
        df[df["pushed_at"] >= cutoff_6m]
        .groupby("topic")
        .size()
        .reset_index(
            name="active_repo_count"
        )
    )


    trends = trends.merge(
        active,
        on="topic",
        how="left"
    )


    trends["active_repo_count"] = (
        trends["active_repo_count"]
        .fillna(0)
    )


    # ==========================
    # NORMALIZACIÓN
    # ==========================


    def log_normalize(column):

        values = np.log1p(
            trends[column]
        )

        min_val = values.min()
        max_val = values.max()


        if max_val == min_val:
            return 0


        return (
            (values - min_val)
            /
            (max_val - min_val)
            *
            100
        )


    def normalize(column):

        max_val = trends[column].max()
        min_val = trends[column].min()


        if max_val == min_val:
            return 0


        return (
            (trends[column] - min_val)
            /
            (max_val - min_val)
            *
            100
        )


    trends["stars_score"] = (
        log_normalize(
            "total_stars"
        )
    )

    trends["forks_score"] = (
        log_normalize(
            "total_forks"
        )
    )

    trends["repo_score"] = (
        log_normalize(
            "repo_count"
        )
    )

    trends["recent_score"] = (
        normalize(
            "recent_repo_count"
        )
    )

    trends["active_score"] = (
        normalize(
            "active_repo_count"
        )
    )


    # ==========================
    # TREND SCORE
    # ==========================

    trends["trend_score"] = (

        trends["stars_score"] * 0.25

        +
        trends["forks_score"] * 0.20

        +
        trends["repo_score"] * 0.25

        +
        trends["recent_score"] * 0.20

        +
        trends["active_score"] * 0.10

    )


    # ==========================
    # RANKING
    # ==========================

    trends = trends.sort_values(
        "trend_score",
        ascending=False
    )


    trends["rank"] = range(
        1,
        len(trends)+1
    )


    final = trends[[
        "topic",
        "repo_count",
        "total_stars",
        "total_forks",
        "avg_stars",
        "avg_forks",
        "languages",
        "recent_repo_count",
        "active_repo_count",
        "trend_score",
        "rank",
    ]]


    print(
        f"📝 Guardando {len(final)} topics..."
    )


    with engine.begin() as conn:
        conn.execute(
            text(
                """
                TRUNCATE TABLE gold.github_topic_trends
                """
            )
        )


    final.to_sql(
        "github_topic_trends",
        engine,
        schema="gold",
        if_exists="append",
        index=False
    )


    print(
        f"✅ Insertados {len(final)} topics"
    )


    print("\n🔥 TOP 20 TOPICS:")

    print(
        final.head(20)[
            [
                "rank",
                "topic",
                "trend_score",
                "repo_count"
            ]
        ]
    )


    return final



if __name__ == "__main__":
    build_github_topic_trends()