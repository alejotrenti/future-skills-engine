"""
Construye el índice de Research Growth de arXiv.

Versión 1.0

Mide la aceleración de cada tecnología en el ecosistema de investigación.
El score combina:
- Growth rate (último año vs año anterior): 35%
- Actividad reciente (últimos 90 días): 30%
- Volumen anual: 25%
- Consistencia (meses activos): 10%
"""

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sqlalchemy import text


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.database import engine


def build_arxiv_research_growth():
    """
    Construye el ranking de tecnologías con mayor aceleración
    en el ecosistema de investigación arXiv.
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
    df["technology"] = df["technology"].str.strip()
    
    # ==========================
    # VENTANAS TEMPORALES
    # ==========================
    
    now = pd.Timestamp.now()
    
    # Ventanas de 12 meses
    cutoff_current_year = now - pd.DateOffset(years=1)
    cutoff_previous_year = now - pd.DateOffset(years=2)
    cutoff_90d = now - pd.DateOffset(days=90)
    
    print(f"\n📅 Ventanas temporales:")
    print(f"   Último año: {cutoff_current_year.strftime('%Y-%m-%d')} → {now.strftime('%Y-%m-%d')}")
    print(f"   Año anterior: {cutoff_previous_year.strftime('%Y-%m-%d')} → {cutoff_current_year.strftime('%Y-%m-%d')}")
    print(f"   Últimos 90 días: {cutoff_90d.strftime('%Y-%m-%d')} → {now.strftime('%Y-%m-%d')}")
    
    # ==========================
    # MÉTRICAS POR TECNOLOGÍA
    # ==========================
    
    # 1. Total histórico (contexto)
    total_papers = (
        df.groupby("technology")
        .size()
        .reset_index(name="total_papers")
    )
    
    # 2. Papers en últimos 12 meses
    current_year = (
        df[df["published"] >= cutoff_current_year]
        .groupby("technology")
        .size()
        .reset_index(name="papers_last_year")
    )
    
    # 3. Papers en año anterior (12 meses previos)
    previous_year = (
        df[
            (df["published"] >= cutoff_previous_year) & 
            (df["published"] < cutoff_current_year)
        ]
        .groupby("technology")
        .size()
        .reset_index(name="papers_previous_year")
    )
    
    # 4. Papers en últimos 90 días
    recent_activity = (
        df[df["published"] >= cutoff_90d]
        .groupby("technology")
        .size()
        .reset_index(name="papers_last_90_days")
    )
    
    # 5. Meses activos (consistencia)
    df["year_month"] = df["published"].dt.to_period("M")
    
    active_months = (
        df.groupby("technology")["year_month"]
        .nunique()
        .reset_index(name="active_months")
    )
    
    # ==========================
    # COMBINAR MÉTRICAS
    # ==========================
    
    growth = total_papers.merge(
        current_year, on="technology", how="left"
    ).merge(
        previous_year, on="technology", how="left"
    ).merge(
        recent_activity, on="technology", how="left"
    ).merge(
        active_months, on="technology", how="left"
    )
    
    # Rellenar NaN con 0
    growth[["papers_last_year", "papers_previous_year", 
            "papers_last_90_days", "active_months"]] = (
        growth[["papers_last_year", "papers_previous_year", 
                "papers_last_90_days", "active_months"]]
        .fillna(0)
    )
    
    # ==========================
    # CALCULAR GROWTH RATE
    # ==========================
    
    # Evitar división por cero
    # Si no había papers antes, el crecimiento es "infinito"
    # Pero cap en 10x para evitar outliers
    growth["growth_rate"] = np.where(
        growth["papers_previous_year"] == 0,
        growth["papers_last_year"],  # Valor base para tecnologías nuevas
        0.0
    )
    
    # Para tecnologías con papers previos, calcular tasa
    mask_has_previous = growth["papers_previous_year"] > 0
    growth.loc[mask_has_previous, "growth_rate"] = (
        (growth.loc[mask_has_previous, "papers_last_year"] - 
         growth.loc[mask_has_previous, "papers_previous_year"]) /
        growth.loc[mask_has_previous, "papers_previous_year"]
    )
    
    # Para tecnologías nuevas: asignar 10x (1000%) si tienen papers recientes
    # Si tienen 0 papers en último año, growth_rate = 0
    growth["growth_rate"] = np.where(
        (growth["papers_previous_year"] == 0) & (growth["papers_last_year"] > 0),
        10.0,  # 1000% de crecimiento (capped)
        growth["growth_rate"]
    )
    
    # Limitar growth rate extremo para evitar outliers
    growth["growth_rate"] = growth["growth_rate"].clip(-1.0, 10.0)
    
    # ==========================
    # CALCULAR MULTIPLICADOR
    # ==========================
    
    growth["growth_multiplier"] = np.where(
        growth["papers_previous_year"] == 0,
        growth["papers_last_year"],
        growth["papers_last_year"] / growth["papers_previous_year"]
    )
    
    # Cap multiplicador para no mostrar números absurdos
    growth["growth_multiplier"] = growth["growth_multiplier"].clip(0, 100)
    
    # ==========================
    # NORMALIZACIÓN
    # ==========================
    
    def log_normalize(column):
        """Normalización logarítmica para distribuciones con cola larga"""
        values = np.log1p(growth[column])
        min_val = values.min()
        max_val = values.max()
        if max_val == min_val:
            return 100
        return ((values - min_val) / (max_val - min_val)) * 100
    
    def linear_normalize(column):
        """Normalización lineal estándar"""
        min_val = growth[column].min()
        max_val = growth[column].max()
        if max_val == min_val:
            return 100
        return ((growth[column] - min_val) / (max_val - min_val)) * 100
    
    # 1. Growth rate score (log-normalize porque puede tener valores extremos)
    growth["growth_rate_score"] = log_normalize("growth_rate")
    
    # 2. Actividad reciente (linear normalize)
    growth["recent_score"] = linear_normalize("papers_last_90_days")
    
    # 3. Volumen anual (log-normalize)
    growth["volume_score"] = log_normalize("papers_last_year")
    
    # 4. Consistencia (linear normalize)
    growth["consistency_score"] = linear_normalize("active_months")
    
    # ==========================
    # GROWTH SCORE - V1.0
    # ==========================
    
    growth["growth_score"] = (
        growth["growth_rate_score"] * 0.35 +    # Aceleración (↓ 5%)
        growth["recent_score"] * 0.30 +         # Señal reciente (↑ 5%)
        growth["volume_score"] * 0.25 +         # Volumen (↑ 5%)
        growth["consistency_score"] * 0.10      # Consistencia (↓ 5%)
    )
    
    # ==========================
    # RANKING
    # ==========================
    
    growth = growth.sort_values("growth_score", ascending=False).reset_index(drop=True)
    growth["rank"] = growth.index + 1
    
    # ==========================
    # COLUMNAS FINALES
    # ==========================
    
    final = growth[
        [
            "technology",
            "total_papers",
            "papers_last_year",
            "papers_previous_year",
            "growth_rate",
            "growth_multiplier",
            "papers_last_90_days",
            "active_months",
            "growth_rate_score",
            "recent_score",
            "volume_score",
            "consistency_score",
            "growth_score",
            "rank",
        ]
    ].copy()
    
    # ==========================
    # METADATA
    # ==========================
    
    final["computed_at"] = pd.Timestamp.now()
    final["version"] = "1.0.0"
    
    # ==========================
    # GUARDAR GOLD
    # ==========================
    
    print(f"\n📝 Guardando {len(final)} tecnologías en gold.research_growth...")
    
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE gold.research_growth"))
    
    final.to_sql(
        "research_growth",
        engine,
        schema="gold",
        if_exists="append",
        index=False
    )
    
    print(f"✅ Insertadas {len(final)} tecnologías en gold.research_growth")
    
    # ==========================
    # TOP 10
    # ==========================
    
    print("\n📈 TOP 10 ARXIV RESEARCH GROWTH")
    print("-" * 90)
    
    for _, row in final.head(10).iterrows():
        growth_pct = row["growth_rate"] * 100
        multiplier = row["growth_multiplier"]
        print(
            f"{row['rank']:2d}. "
            f"{row['technology']:35s} "
            f"Score: {row['growth_score']:6.1f}  "
            f"{growth_pct:+.0f}%  "
            f"({multiplier:.1f}x)  "
            f"Papers: {int(row['papers_previous_year']):3d} → {int(row['papers_last_year']):3d}"
        )
    
    return final


if __name__ == "__main__":
    build_arxiv_research_growth()