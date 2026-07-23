"""
Build Gold layer: Future Skills Engine

Construye la tabla gold.future_skills combinando:
- Stack Overflow (skill_trends + skill_growth)
- GitHub (github_skill_momentum)
- Research (research_trends + research_growth)

Arquitectura aprobada:
- Stack Overflow: 35% (Adopción actual + potencial de crecimiento)
- GitHub: 35% (Actividad en ecosistema open source)
- Research: 30% (Volumen de investigación + aceleración)

No participa: gold.github_topic_trends (representa comunidades, no tecnologías)
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import text

from src.utils.database import engine
from src.config.technology_mapping import (
    normalize_technology,
    get_category,
    get_trend_type
)


# ==========================
# CONFIGURACIÓN
# ==========================

VERSION = "1.0"
SCHEMA = "gold"
TABLE_NAME = "future_skills"


# ==========================
# FUNCIONES AUXILIARES
# ==========================

def normalize_score(series):
    """
    Normalización por percentiles (0-100).
    Más robusta frente a valores extremos.
    """
    return series.rank(pct=True) * 100


def calculate_future_score(row: pd.Series) -> float:
    """
    Calcula el Future Score con pesos dinámicos.
    
    Pesos base:
    - Stack Overflow: 35%
    - GitHub: 35%
    - Research: 30%
    
    Si una fuente no tiene datos, su peso se redistribuye
    entre las fuentes que sí tienen datos.
    """
    # Verificar qué fuentes tienen datos
    has_so = not pd.isna(row.get("stackoverflow_score", np.nan))
    has_gh = not pd.isna(row.get("github_score", np.nan))
    has_research = not pd.isna(row.get("research_score", np.nan))
    
    # Si no tiene ninguna fuente, retornar NaN
    if not any([has_so, has_gh, has_research]):
        return np.nan
    
    # Pesos base
    weights = {
        "so":0.30,
        "gh":0.35,
        "research":0.35
    }   
    
    # Calcular pesos ajustados
    total_weight = 0
    adjusted_weights = {}
    
    if has_so:
        adjusted_weights["so"] = weights["so"]
        total_weight += weights["so"]
    
    if has_gh:
        adjusted_weights["gh"] = weights["gh"]
        total_weight += weights["gh"]
    
    if has_research:
        adjusted_weights["research"] = weights["research"]
        total_weight += weights["research"]
    
    # Normalizar pesos para que sumen 1
    for key in adjusted_weights:
        adjusted_weights[key] = adjusted_weights[key] / total_weight
    
    # Calcular score ponderado
    score = 0
    if has_so:
        score += row["stackoverflow_score"] * adjusted_weights["so"]
    if has_gh:
        score += row["github_score"] * adjusted_weights["gh"]
    if has_research:
        score += row["research_score"] * adjusted_weights["research"]
    
    return score


def get_sources_used(row: pd.Series) -> str:
    """Retorna las fuentes disponibles como string legible."""
    sources = []
    if not pd.isna(row.get("stackoverflow_score", np.nan)):
        sources.append("SO")
    if not pd.isna(row.get("github_score", np.nan)):
        sources.append("GitHub")
    if not pd.isna(row.get("research_score", np.nan)):
        sources.append("Research")
    return ", ".join(sources) if sources else ""


def get_score_explanation(row: pd.Series) -> str:

    so = row.get("stackoverflow_score", np.nan)
    gh = row.get("github_score", np.nan)
    research = row.get("research_score", np.nan)


    available = [
        x for x in [so, gh, research]
        if not pd.isna(x)
    ]


    if not available:
        return "Limited data available"


    # Caso 1: equilibrio fuerte
    if (
        not pd.isna(so)
        and not pd.isna(gh)
        and not pd.isna(research)
        and so > 70
        and gh > 70
        and research > 70
    ):
        return (
            "Excelente equilibrio entre adopción, "
            "ecosistema open source e investigación."
        )


    # Caso 2: investigación domina
    if (
        not pd.isna(research)
        and research > gh if not pd.isna(gh) else True
        and research > so if not pd.isna(so) else True
    ):
        return (
            "Alta actividad científica y creciente interés "
            "en investigación."
        )


    # Caso 3: GitHub domina
    if (
        not pd.isna(gh)
        and gh > so if not pd.isna(so) else True
    ):
        return (
            "Ecosistema open source fuerte "
            "con alta actividad de desarrollo."
        )


    # Caso 4: Stack Overflow domina
    if (
        not pd.isna(so)
    ):
        return (
            "Alta adopción entre desarrolladores "
            "y uso activo en la comunidad."
        )


    return "Tendencia emergente basada en datos disponibles."


# ==========================
# FUNCIÓN PRINCIPAL
# ==========================

def build_future_skills() -> None:
    """
    Construye la tabla gold.future_skills.
    """
    
    print("=== Future Skills Engine ===")
    print(f"Versión: {VERSION}")
    print(f"Timestamp: {datetime.now()}\n")
    
    # ==========================
    # 1. Cargar datos de cada fuente
    # ==========================
    
    print("1. Cargando datos...")
    
    # Stack Overflow - Trends
    so_trends = pd.read_sql(
        text("""
            SELECT
                skill,
                category,
                users_count
            FROM gold.skill_trends
        """),
        engine
    )
    print(f"   SO Trends: {len(so_trends)} registros")
    
    # Stack Overflow - Growth
    so_growth = pd.read_sql(
        text("""
            SELECT
                skill,
                growth_score
            FROM gold.skill_growth
        """),
        engine
    )
    print(f"   SO Growth: {len(so_growth)} registros")
    
    # GitHub - Momentum
    gh_momentum = pd.read_sql(
        text("""
            SELECT
                technology,
                momentum_score
            FROM gold.github_skill_momentum
        """),
        engine
    )
    print(f"   GitHub Momentum: {len(gh_momentum)} registros")
    
    # Research - Trends
    research_trends = pd.read_sql(
        text("""
            SELECT
                technology,
                research_score
            FROM gold.research_trends
        """),
        engine
    )
    print(f"   Research Trends: {len(research_trends)} registros")
    
    # Research - Growth
    research_growth = pd.read_sql(
        text("""
            SELECT
                technology,
                growth_score
            FROM gold.research_growth
        """),
        engine
    )
    print(f"   Research Growth: {len(research_growth)} registros\n")
    
    # ==========================
    # 2. Normalizar nombres de tecnologías
    # ==========================
    
    print("2. Normalizando nombres...")
    
    # Stack Overflow
    so_trends["technology"] = so_trends["skill"].apply(normalize_technology)
    so_growth["technology"] = so_growth["skill"].apply(normalize_technology)
    
    # GitHub
    gh_momentum["technology"] = gh_momentum["technology"].apply(normalize_technology)
    
    # Research
    research_trends["technology"] = research_trends["technology"].apply(normalize_technology)
    research_growth["technology"] = research_growth["technology"].apply(normalize_technology)
    
    print("   Normalización completada\n")
    
    # ==========================
    # 3. Agrupar por tecnología (eliminar duplicados)
    # ==========================
    
    print("3. Agrupando por tecnología...")
    
    # Stack Overflow Trends
    so_trends = (
        so_trends
        .groupby("technology", as_index=False)
        .agg({
            "users_count": "sum",
            "category": "first"
        })
    )
    
    # Stack Overflow Growth
    so_growth = (
        so_growth
        .groupby("technology", as_index=False)
        .agg({
            "growth_score": "max"
        })
    )
    
    # GitHub Momentum
    gh_momentum = (
        gh_momentum
        .groupby("technology", as_index=False)
        .agg({
            "momentum_score": "max"
        })
    )
    
    # Research Trends
    research_trends = (
        research_trends
        .groupby("technology", as_index=False)
        .agg({
            "research_score": "max"
        })
    )
    
    # Research Growth
    research_growth = (
        research_growth
        .groupby("technology", as_index=False)
        .agg({
            "growth_score": "max"
        })
    )
    
    print(f"   SO Trends: {len(so_trends)} tecnologías")
    print(f"   SO Growth: {len(so_growth)} tecnologías")
    print(f"   GitHub Momentum: {len(gh_momentum)} tecnologías")
    print(f"   Research Trends: {len(research_trends)} tecnologías")
    print(f"   Research Growth: {len(research_growth)} tecnologías\n")
    
    # ==========================
    # 4. Unificar todas las fuentes
    # ==========================
    
    print("4. Unificando fuentes...")
    
    # Comenzar con Stack Overflow Trends
    future = so_trends.copy()
    
    # Agregar Stack Overflow Growth
    future = future.merge(
        so_growth[["technology", "growth_score"]],
        on="technology",
        how="outer"
    )
    
    # Agregar GitHub Momentum
    future = future.merge(
        gh_momentum[["technology", "momentum_score"]],
        on="technology",
        how="outer"
    )
    
    # Agregar Research Trends
    future = future.merge(
        research_trends[["technology", "research_score"]],
        on="technology",
        how="outer"
    )
    
    # Agregar Research Growth (renombrar para evitar conflicto)
    research_growth_renamed = research_growth.rename(
        columns={"growth_score": "research_growth_score"}
    )
    future = future.merge(
        research_growth_renamed[["technology", "research_growth_score"]],
        on="technology",
        how="outer"
    )
    
    print(f"   Total tecnologías únicas: {len(future)}\n")
    
    # ==========================
    # 5. Normalizar métricas a escala 0-100
    # ==========================
    
    print("5. Normalizando métricas...")
    
    # Columnas a normalizar
    metrics_to_normalize = [
        "users_count",
        "growth_score",
        "momentum_score",
        "research_score",
        "research_growth_score"
    ]
    
    # Aplicar normalización a cada columna
    for metric in metrics_to_normalize:
        future[f"{metric}_norm"] = normalize_score(future[metric])
    
    print("   Normalización completada\n")
    
    # ==========================
    # 6. Calcular scores intermedios
    # ==========================
    
    print("6. Calculando scores intermedios...")
    
    # Stack Overflow Score (60% Trends + 40% Growth)
    future["stackoverflow_score"] = (
        future["users_count_norm"] * 0.30 +
        future["growth_score_norm"] * 0.70
    )
    
    # GitHub Score (100% Momentum)
    future["github_score"] = future["momentum_score_norm"]
    
    # Research Score (50% Trends + 50% Growth)
    future["research_score"] = (
        future["research_score_norm"] * 0.30 +
        future["research_growth_score_norm"] * 0.70
    )
    
    print("   Scores calculados\n")
    
    # ==========================
    # Calcular tipo de tendencia
    # ==========================

    print("   Clasificando tendencias...")

    future["trend_type"] = future.apply(
        lambda row: get_trend_type(
            row["technology"],
            {
                "stackoverflow_score": row["stackoverflow_score"],
                "github_score": row["github_score"],
                "research_score": row["research_score"]
            }
        ),
        axis=1
    )

    print("   Trend types asignados\n")
    
    # ==========================
    # 7. Calcular Future Score (dinámico)
    # ==========================
    
    print("7. Calculando Future Score...")
    
    future["raw_future_score"] = future.apply(calculate_future_score, axis=1)

    
    print(f"   Future Score raw calculado\n")
    
    # ==========================
    # 8. Asignar categorías consistentes
    # ==========================
    
    print("8. Asignando categorías...")
    
    future["category"] = future["technology"].apply(get_category)
    
    print("   Categorías asignadas\n")
    
    # ==========================
    # 9. Calcular cobertura (metadata)
    # ==========================

    print("9. Calculando cobertura...")

    # Contar fuentes disponibles
    future["source_count"] = (
        future["stackoverflow_score"].notna().astype(int) +
        future["github_score"].notna().astype(int) +
        future["research_score"].notna().astype(int)
    )

    # Cobertura explicativa
    coverage_map = {
        3: 100,
        2: 75,
        1: 50
    }

    future["coverage_score"] = future["source_count"].map(
        coverage_map
    )

    # Factor de confianza
    coverage_factor_map = {
        3: 1.00,
        2: 0.85,
        1: 0.65
    }

    future["coverage_factor"] = future["source_count"].map(
        coverage_factor_map
    )


    # Fuentes utilizadas
    future["sources_used"] = future.apply(
        get_sources_used,
        axis=1
    )

    # Explicación
    future["score_explanation"] = future.apply(
        get_score_explanation,
        axis=1
    )
    
    
    future["future_score"] = (
        future["raw_future_score"] *
        future["coverage_factor"]
    )
    
    
    print(f"   Distribución de fuentes:")
    for count in sorted(future["source_count"].unique()):
        if not pd.isna(count):
            n = (future["source_count"] == count).sum()
            coverage = coverage_map.get(int(count), 0)
            print(f"      {int(count)} fuente(s): {n} tecnologías (coverage: {coverage}%)")
    print()
    
    # ==========================
    # 10. Generar ranking
    # ==========================
    
    print("10. Generando ranking...")
    
    # Ordenar por Future Score
    future = future.sort_values(
        ["future_score", "source_count"],
        ascending=[False, False]
    ).reset_index(drop=True)

    # Generar ranking
    future["rank"] = future.index + 1
        
    print(f"   Ranking generado (ordenado por future_score)\n")
    
    # ==========================
    # 11. Agregar metadata
    # ==========================
    
    print("11. Agregando metadata...")
    
    future["computed_at"] = datetime.now()
    future["version"] = VERSION
    
    print("   Metadata agregada\n")
    
    # ==========================
    # 12. Seleccionar columnas finales
    # ==========================
    
    final_columns = [
        "rank",
        "technology",
        "category",
        "trend_type",
        "future_score",
        "stackoverflow_score",
        "github_score",
        "research_score",
        "source_count",
        "coverage_score",
        "coverage_factor",
        "sources_used",
        "score_explanation",
        "computed_at",
        "version"
    ]
        
    future_final = future[final_columns]
    
    print(f"   Columnas finales ({len(final_columns)}):")
    for col in final_columns:
        print(f"      - {col}")
    print()
    
    # ==========================
    # 13. Guardar en base de datos
    # ==========================
    
    print(f"13. Guardando en {SCHEMA}.{TABLE_NAME}...")
    
    future_final.to_sql(
        TABLE_NAME,
        engine,
        schema=SCHEMA,
        if_exists="replace",
        index=False
    )
    
    print(f"   ✅ Tabla {SCHEMA}.{TABLE_NAME} creada exitosamente")
    print(f"   Total de registros: {len(future_final)}")
    
    # Mostrar top 10
    print("\n   Top 10 tecnologías:")
    print(f"   {'Rank':<6} {'Technology':<20} {'Category':<12} {'Future':<10} {'Ranking':<10} {'Coverage':<10} {'Sources'}")
    print("   " + "-" * 95)
    for _, row in future_final.head(10).iterrows():
        print(f"   {row['rank']:<6} {row['technology']:<20} {row['category']:<12} "
              f"{row['future_score']:<10.1f}"
              f"{row['coverage_score']:<10} {row['sources_used']}")
    
    print(f"\n✅ Future Skills Engine completado a las {datetime.now().strftime('%H:%M:%S')}")


# ==========================
# MAIN (para ejecución directa)
# ==========================

if __name__ == "__main__":
    build_future_skills()