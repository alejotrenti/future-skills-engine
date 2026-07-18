"""
Construye el índice de momentum de GitHub para tecnologías.
Versión 1.1 - Simplificada pero robusta.
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from utils.database import engine


def build_github_skill_momentum():
    """
    Construye el índice de momentum de GitHub.
    
    Score combina:
    - Estrellas (log-normalizado): 30%
    - Forks (log-normalizado): 25%  
    - Cantidad de repos (log-normalizado): 20%
    - Actividad último año: 15%
    - Repos activos (últimos 6 meses): 10%
    """
    
    query = """
        SELECT
            language,
            stars,
            forks,
            created_at,
            pushed_at
        FROM silver.github_repositories
        WHERE language IS NOT NULL
        AND language <> 'Unknown'
    """
    
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("❌ No se encontraron repositorios en silver.github_repositories")
        return
    
    print(f"📊 Procesando {len(df)} repositorios...")
    
    # ============ LIMPIEZA ============
    df["stars"] = pd.to_numeric(df["stars"], errors="coerce").fillna(0)
    df["forks"] = pd.to_numeric(df["forks"], errors="coerce").fillna(0)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["pushed_at"] = pd.to_datetime(df["pushed_at"])
    
    # ============ MÉTRICAS POR TECNOLOGÍA ============
    momentum = (
        df.groupby("language")
        .agg(
            repo_count=("language", "count"),
            total_stars=("stars", "sum"),
            total_forks=("forks", "sum"),
            avg_stars=("stars", "mean"),
            avg_forks=("forks", "mean"),
        )
        .reset_index()
    )
    
    # ============ ACTIVIDAD RECIENTE ============
    now = pd.Timestamp.now()
    cutoff_1y = now - pd.DateOffset(years=1)
    cutoff_6m = now - pd.DateOffset(months=6)
    
    # Repos creados en el último año
    recent_created = (
        df[df["created_at"] >= cutoff_1y]
        .groupby("language")
        .size()
        .reset_index(name="recent_1y_count")
    )
    momentum = momentum.merge(recent_created, on="language", how="left")
    momentum["recent_1y_count"] = momentum["recent_1y_count"].fillna(0)
    
    # Repos activos (actualizados en últimos 6 meses)
    active = (
        df[df["pushed_at"] >= cutoff_6m]
        .groupby("language")
        .size()
        .reset_index(name="active_repo_count")
    )
    momentum = momentum.merge(active, on="language", how="left")
    momentum["active_repo_count"] = momentum["active_repo_count"].fillna(0)
    
    # ============ LOG NORMALIZATION ============
    def log_normalize(column):
        """Normaliza usando log1p para distribuciones con cola larga."""
        values = np.log1p(momentum[column])
        min_val = values.min()
        max_val = values.max()
        
        if max_val == min_val:
            return 100
        
        return ((values - min_val) / (max_val - min_val)) * 100
    
    momentum["stars_score"] = log_normalize("total_stars")
    momentum["forks_score"] = log_normalize("total_forks")
    momentum["repo_score"] = log_normalize("repo_count")
    
    # ============ NORMALIZACIÓN LINEAL PARA ACTIVIDAD ============
    def linear_normalize(column):
        """Normalización lineal simple."""
        if momentum[column].max() == momentum[column].min():
            return 100
        return ((momentum[column] - momentum[column].min()) / 
                (momentum[column].max() - momentum[column].min()) * 100)
    
    momentum["recent_score"] = linear_normalize("recent_1y_count")
    momentum["active_score"] = linear_normalize("active_repo_count")
    
    # ============ COMPOSITE SCORE ============
    momentum["momentum_score"] = (
        momentum["stars_score"] * 0.30 +
        momentum["forks_score"] * 0.25 +
        momentum["repo_score"] * 0.20 +
        momentum["recent_score"] * 0.15 +
        momentum["active_score"] * 0.10
    )
    
    # ============ RANKING ============
    momentum = momentum.sort_values("momentum_score", ascending=False)
    momentum["rank"] = range(1, len(momentum) + 1)
    
    # ============ SELECCIONAR COLUMNAS FINALES ============
    final = momentum[[
        "language",
        "repo_count",
        "total_stars",
        "total_forks",
        "avg_stars",
        "avg_forks",
        "recent_1y_count",
        "active_repo_count",
        "stars_score",
        "forks_score",
        "repo_score",
        "recent_score",
        "active_score",
        "momentum_score",
        "rank",
    ]].copy()
    
    final = final.rename(columns={"language": "technology"})
    
    # ============ METADATOS ============
    final["computed_at"] = pd.Timestamp.now()
    final["version"] = "1.1.0"
    
    # ============ GUARDAR EN GOLD ============
    print(f"📝 Guardando {len(final)} tecnologías...")
    
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE gold.github_skill_momentum"))
    
    final.to_sql(
        "github_skill_momentum",
        engine,
        schema="gold",
        if_exists="append",
        index=False
    )
    
    print(f"✅ Insertadas {len(final)} tecnologías en gold.github_skill_momentum")
    
    # ============ MOSTRAR TOP 10 ============
    print("\n🏆 TOP 10 GITHUB MOMENTUM:")
    print("-" * 80)
    
    top10 = final.head(10)
    for _, row in top10.iterrows():
        stars_m = row["total_stars"] / 1_000_000
        print(f"{row['rank']:2d}. {row['technology']:20s} "
              f"Score: {row['momentum_score']:6.1f} "
              f"Repos: {row['repo_count']:5d} "
              f"Stars: {stars_m:5.1f}M")
    
    return final


if __name__ == "__main__":
    build_github_skill_momentum()