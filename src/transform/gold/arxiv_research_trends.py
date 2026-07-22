"""
Construye el índice de Research Trends de arXiv.

Versión 1.0

Score combina:
- Papers únicos: 50%
- Actividad último año: 30%
- Actividad últimos 90 días: 10%
- Diversidad de categorías: 10%
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sqlalchemy import text


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.database import engine



def build_arxiv_research_trends():

    """
    Construye el ranking de tecnologías con mayor presencia
    dentro del ecosistema de investigación arXiv.
    """


    query = """
        SELECT
            paper_id,
            technology,
            primary_category,
            published
        FROM silver.papers
        WHERE technology IS NOT NULL
        AND technology <> 'Unknown'
    """


    df = pd.read_sql(query, engine)


    if df.empty:
        print("❌ No se encontraron papers en silver.papers")
        return


    print(f"📚 Procesando {len(df)} relaciones paper-tecnología...")


    # ==========================
    # LIMPIEZA
    # ==========================

    df["published"] = pd.to_datetime(df["published"])

    df["technology"] = (
        df["technology"]
        .str.strip()
    )


    # ==========================
    # MÉTRICAS POR TECNOLOGÍA
    # ==========================

    trends = (
        df.groupby("technology")
        .agg(
            unique_papers=("paper_id", "nunique"),
            research_mentions=("paper_id", "count"),
            category_count=("primary_category", "nunique")
        )
        .reset_index()
    )


    # ==========================
    # ACTIVIDAD TEMPORAL
    # ==========================

    now = pd.Timestamp.now()

    cutoff_year = now - pd.DateOffset(years=1)

    cutoff_90d = now - pd.DateOffset(days=90)



    yearly_activity = (
        df[df["published"] >= cutoff_year]
        .groupby("technology")
        .size()
        .reset_index(name="papers_last_year")
    )


    trends = trends.merge(
        yearly_activity,
        on="technology",
        how="left"
    )


    trends["papers_last_year"] = (
        trends["papers_last_year"]
        .fillna(0)
    )



    recent_activity = (
        df[df["published"] >= cutoff_90d]
        .groupby("technology")
        .size()
        .reset_index(name="papers_last_90_days")
    )


    trends = trends.merge(
        recent_activity,
        on="technology",
        how="left"
    )


    trends["papers_last_90_days"] = (
        trends["papers_last_90_days"]
        .fillna(0)
    )


    # ==========================
    # NORMALIZACIÓN
    # ==========================

    def log_normalize(column):

        values = np.log1p(trends[column])

        min_val = values.min()
        max_val = values.max()

        if max_val == min_val:
            return 100

        return (
            (values - min_val)
            /
            (max_val - min_val)
        ) * 100



    def linear_normalize(column):

        min_val = trends[column].min()
        max_val = trends[column].max()

        if max_val == min_val:
            return 100

        return (
            (trends[column] - min_val)
            /
            (max_val - min_val)
        ) * 100



    trends["unique_papers_score"] = (
        log_normalize("unique_papers")
    )


    trends["yearly_score"] = (
        linear_normalize("papers_last_year")
    )


    trends["recent_score"] = (
        linear_normalize("papers_last_90_days")
    )


    trends["diversity_score"] = (
        linear_normalize("category_count")
    )



    # ==========================
    # RESEARCH SCORE - V1.1
    # ==========================

    trends["research_score"] = (

        trends["yearly_score"] * 0.40      # ↑ 30% → 40%
        
        +
        
        trends["recent_score"] * 0.30      # ↑ 10% → 30%
        
        +
        
        trends["unique_papers_score"] * 0.20  # ↓ 50% → 20%
        
        +
        
        trends["diversity_score"] * 0.10   # se mantiene

    )


    # ==========================
    # RANKING
    # ==========================

    trends = (
        trends
        .sort_values(
            "research_score",
            ascending=False
        )
        .reset_index(drop=True)
    )


    trends["rank"] = (
        trends.index + 1
    )


    # ==========================
    # COLUMNAS FINALES
    # ==========================

    final = trends[
        [
            "technology",
            "unique_papers",
            "research_mentions",
            "papers_last_year",
            "papers_last_90_days",
            "category_count",
            "unique_papers_score",
            "yearly_score",
            "recent_score",
            "diversity_score",
            "research_score",
            "rank",
        ]
    ].copy()



    # ==========================
    # METADATA
    # ==========================

    final["computed_at"] = pd.Timestamp.now()

    final["version"] = "1.1.0"


    # ==========================
    # GUARDAR GOLD
    # ==========================

    print(
        f"📝 Guardando {len(final)} tecnologías..."
    )


    with engine.begin() as conn:

        conn.execute(
            text(
                "TRUNCATE TABLE gold.research_trends"
            )
        )



    final.to_sql(
        "research_trends",
        engine,
        schema="gold",
        if_exists="append",
        index=False
    )


    print(
        f"✅ Insertadas {len(final)} tecnologías en gold.research_trends"
    )



    # ==========================
    # TOP 10
    # ==========================

    print("\n🏆 TOP 10 ARXIV RESEARCH TRENDS")
    print("-" * 80)


    for _, row in final.head(10).iterrows():

        print(
            f"{row['rank']:2d}. "
            f"{row['technology']:35s} "
            f"Score: {row['research_score']:6.1f} "
            f"Papers: {row['unique_papers']:4d}"
        )


    return final



if __name__ == "__main__":

    build_arxiv_research_trends()