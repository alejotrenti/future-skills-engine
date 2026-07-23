"""
Future Skills Engine
Predicción de tendencias tecnológicas basada en Stack Overflow, GitHub y arXiv
"""

import pandas as pd
import streamlit as st
from sqlalchemy import text

from db import engine

try:
    from theme import load_css_bundle
except Exception:
    def load_css_bundle(*css_files: str) -> None:
        from pathlib import Path
        css_chunks = []
        for css_file in css_files:
            css_path = Path(__file__).resolve().parents[1] / ".streamlit" / css_file
            if css_path.exists():
                css_chunks.append(css_path.read_text(encoding="utf-8"))
        if css_chunks:
            st.markdown(f"<style>{''.join(css_chunks)}</style>", unsafe_allow_html=True)



st.set_page_config(
    page_title="Future Skills Engine",
    page_icon="🔮",
    layout="wide",
)

load_css_bundle(
    "styles.css",
    "future_skill_engine.css"
)

# ==========================
# QUERY - ESTRUCTURA REAL
# ==========================

query = """
SELECT
    technology,
    category,
    trend_type,
    future_score,
    rank,
    research_score,
    github_score,
    stackoverflow_score,
    source_count,
    coverage_score,
    coverage_factor,
    sources_used,
    score_explanation,
    computed_at
FROM gold.future_skills
ORDER BY rank;
"""


with st.spinner("Cargando Future Skills Engine..."):
    df = pd.read_sql(text(query), engine)

if df.empty:
    st.info("No hay datos disponibles.")
    st.stop()

# ==========================
# UTILITY FUNCTIONS
# ==========================

def get_trend_display(trend_type: str) -> dict:
    """Retorna el display name e ícono para el tipo de tendencia"""
    trend_map = {
        "established_leader": {
            "icon": "🏛",
            "label": "Established Leader",
            "description": "Tecnología dominante con adopción masiva y ecosistema maduro",
            "color": "#4CAF50"
        },
        "rising_star": {
            "icon": "🚀",
            "label": "Rising Star",
            "description": "Tecnología en rápido crecimiento con alto potencial futuro",
            "color": "#FF9800"
        },
        "industry_standard": {
            "icon": "⚡",
            "label": "Industry Standard",
            "description": "Estándar de la industria con adopción generalizada",
            "color": "#2196F3"
        },
        "research_driven": {
            "icon": "🔬",
            "label": "Research Driven",
            "description": "Tecnología impulsada por investigación académica",
            "color": "#9C27B0"
        },
        "emerging": {
            "icon": "🌱",
            "label": "Emerging",
            "description": "Tecnología emergente con potencial de crecimiento",
            "color": "#FF5722"
        },
        "niche": {
            "icon": "🎯",
            "label": "Niche",
            "description": "Tecnología especializada con adopción enfocada",
            "color": "#607D8B"
        }
    }
    return trend_map.get(trend_type, {
        "icon": "📊",
        "label": trend_type.replace("_", " ").title(),
        "description": "Tecnología en evolución",
        "color": "#9E9E9E"
    })

def get_confidence_level(coverage_score: float) -> dict:
    """Retorna el nivel de confianza basado en el coverage score"""
    if coverage_score >= 80:
        return {
            "level": "High",
            "icon": "🟢",
            "description": "Alta confianza - datos completos de múltiples fuentes"
        }
    elif coverage_score >= 50:
        return {
            "level": "Medium",
            "icon": "🟡",
            "description": "Confianza media - datos parciales de algunas fuentes"
        }
    else:
        return {
            "level": "Low",
            "icon": "🔴",
            "description": "Baja confianza - datos limitados, considerar más investigación"
        }

def get_metric_display_name(metric: str) -> str:
    """Retorna el nombre display para cada métrica"""
    names = {
        "research_score": "🔬 arXiv Research Impact",
        "github_score": "🚀 Open Source Momentum",
        "stackoverflow_score": "💻 Developer Adoption"
    }
    return names.get(metric, metric.replace("_", " ").title())

def get_metric_icon(metric: str) -> str:
    """Retorna el ícono para cada métrica"""
    icons = {
        "research_score": "📚",
        "github_score": "💻",
        "stackoverflow_score": "📊"
    }
    return icons.get(metric, "📌")

# ==========================
# FUNCIONES DE FORMATEO 🆕
# ==========================

def format_score(value, decimals=1):
    """Formatea un score, manejando NaN de manera profesional"""
    if pd.isna(value):
        return "—"
    return f"{value:.{decimals}f}"

def format_category(category):
    """Limpia categorías mostrando nombres amigables"""
    if pd.isna(category) or category == "uncategorized" or category == "":
        return "Other"
    return category.title()

def format_confidence_display(coverage_score, source_count, total_sources=3):
    """Retorna un display más intuitivo de confianza"""
    if pd.isna(coverage_score):
        return {
            "label": "No Data",
            "icon": "⚪",
            "description": "Sin datos suficientes para evaluación"
        }
    
    # Mostrar fuentes disponibles
    sources_text = f"{source_count}/{total_sources} fuentes"
    
    if coverage_score >= 80:
        return {
            "label": f"High ({sources_text})",
            "icon": "🟢",
            "description": "Alta confianza - datos completos de múltiples fuentes"
        }
    elif coverage_score >= 50:
        return {
            "label": f"Medium ({sources_text})",
            "icon": "🟡",
            "description": "Confianza media - datos parciales de algunas fuentes"
        }
    else:
        return {
            "label": f"Low ({sources_text})",
            "icon": "🔴",
            "description": "Baja confianza - datos limitados, considerar más investigación"
        }

def get_source_badge(source):
    """Retorna el badge con nombre completo de la fuente"""
    source_map = {
        "SO": "Stack Overflow",
        "GitHub": "GitHub",
        "arXiv": "arXiv",
        "so": "Stack Overflow",
        "github": "GitHub",
        "arxiv": "arXiv"
    }
    return source_map.get(source.strip(), source.strip())


# ==========================
# HERO (SIMPLE Y LIMPIO)
# ==========================

st.markdown(
    """<a href="/" target="_self"
       style="
            position: fixed;
            top: 20px;
            left: 20px;
            width: 46px;
            height: 46px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:50%;
            background:rgba(24,24,32,.75);
            border:1px solid rgba(255,255,255,.08);
            backdrop-filter:blur(12px);
            text-decoration:none;
            z-index:9999;
       ">
        <svg xmlns="http://www.w3.org/2000/svg"
             width="22"
             height="22"
             fill="none"
             viewBox="0 0 24 24"
             stroke="white"
             stroke-width="2"
             stroke-linecap="round"
             stroke-linejoin="round">
            <path d="M19 12H5"/>
            <path d="m12 19-7-7 7-7"/>
        </svg>
    </a>""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""<div class="fse-hero">
        <div class="fse-hero-content">
            <h1>Future Skills Engine</h1>
            <p class="fse-hero-subtitle">
                Predicción de tendencias tecnológicas basada en
                <span class="fse-hero-source">Stack Overflow</span> •
                <span class="fse-hero-source">GitHub</span> •
                <span class="fse-hero-source">arXiv</span>
            </p>
            <div class="fse-hero-meta">
                <span class="fse-hero-meta-item">
                    <span class="fse-hero-meta-number">{len(df)}</span> tecnologías analizadas
                </span>
                <span class="fse-hero-meta-item">
                    <span class="fse-hero-meta-number">{df['computed_at'].iloc[0].strftime('%Y-%m-%d %H:%M')}</span> última actualización
                </span>
            </div>
        </div>
    </div>""",
    unsafe_allow_html=True
)

# ==========================
# KPIs (4)
# ==========================

top_tech = df.iloc[0]["technology"]
top_score = df.iloc[0]["future_score"]
avg_score = df["future_score"].mean()
max_coverage = df.loc[df["coverage_score"].idxmax()]["technology"]
coverage_pct = df["coverage_score"].max()

# Tecnología con mayor cobertura de fuentes
max_sources = df.loc[df["source_count"].idxmax()]["technology"]
source_count = df["source_count"].max()

metrics = [
    (
        "🏆",
        "Top Future Score",
        f"{top_tech}",
        f"Score: {top_score:.1f}"
    ),
    (
        "📈",
        "Average Future Score",
        f"{avg_score:.1f}",
        "Promedio del ecosistema"
    ),
    (
        "🎯",
        "Highest Coverage",
        f"{max_coverage}",
        f"{coverage_pct:.1f}% de cobertura"
    ),
    (
        "🔬",
        "Most Sources",
        f"{max_sources}",
        f"{source_count} fuentes analizadas"
    )
]

cols = st.columns(4)

for col, (icon, title, value, subtitle) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""<div class="fse-metric-card">
                <div class="fse-metric-icon">{icon}</div>
                <div class="fse-metric-body">
                    <p class="fse-metric-label">{title}</p>
                    <p class="fse-metric-value">{value}</p>
                    <p class="fse-metric-subtitle">{subtitle}</p>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

st.write("")

# ==========================
# RANKING + DISTRIBUCIÓN (2 columnas)
# ==========================

left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown(
        """<div class="fse-section-header">
            <h2>🏆 Ranking de Future Score</h2>
            <p class="fse-section-subtitle">
                Tecnologías ordenadas por su puntuación de futuro
            </p>
        </div>""",
        unsafe_allow_html=True
    )
    
    # Selector de top N
    top_n = st.select_slider(
        "Mostrar top",
        options=[10, 15, 20, 30, 50],
        value=20
    )
    
    df_top = df.head(top_n)
    
    # Ranking visual mejorado
    for idx, row in df_top.iterrows():
        score = row["future_score"]
        tech = row["technology"]
        rank = row["rank"]
        category = format_category(row["category"])
        sources = row["source_count"]
        
        # Determinar color según score
        if score >= 90:
            bar_color = "var(--fse-gradient-start)"
        elif score >= 75:
            bar_color = "var(--fse-gradient-mid)"
        else:
            bar_color = "var(--fse-gradient-end)"
        
        # 🆕 Mostrar cobertura de fuentes en lugar de solo número
        coverage_display = f"{sources}/3"
        
        st.markdown(
            f"""<div class="fse-rank-item">
                <span class="fse-rank-number">#{rank}</span>
                <span class="fse-rank-name">{tech}</span>
                <span class="fse-rank-category">{category}</span>
                <div class="fse-rank-bar-container">
                    <div class="fse-rank-bar" style="width: {score}%; background: {bar_color};"></div>
                </div>
                <span class="fse-rank-score">{score:.1f}</span>
                <span class="fse-rank-sources">📚{coverage_display}</span>
            </div>""",
            unsafe_allow_html=True
        )

with right_col:
    st.markdown(
        """<div class="fse-section-header">
            <h2>📊 Distribución</h2>
            <p class="fse-section-subtitle">
                Concentración de scores en el ecosistema
            </p>
        </div>""",
        unsafe_allow_html=True
    )
    
    # Distribución de Future Scores
    bins = [0, 20, 40, 60, 80, 100]
    labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
    df['score_bin'] = pd.cut(df['future_score'], bins=bins, labels=labels, right=False)
    distribution = df['score_bin'].value_counts().sort_index()
    
    for label in labels:
        count = distribution.get(label, 0)
        pct = (count / len(df)) * 100
        bar_width = max(10, pct * 2)
        
        st.markdown(
            f"""<div class="fse-dist-item">
                <span class="fse-dist-label">{label}</span>
                <div class="fse-dist-bar-container">
                    <div class="fse-dist-bar" style="width: {bar_width}%;"></div>
                </div>
                <span class="fse-dist-count">{count}</span>
            </div>""",
            unsafe_allow_html=True
        )
    
    # Categorías más representadas
    top_categories = df['category'].value_counts().head(3)
    categories_text = ", ".join([f"{cat} ({count})" for cat, count in top_categories.items()])
    
    st.markdown(
        f"""<div class="fse-dist-note">
            <strong>Categorías principales:</strong> {categories_text}
        </div>""",
        unsafe_allow_html=True
    )

st.write("")

# ==========================
# DETALLE DE TECNOLOGÍA - VERSIÓN MEJORADA 🆕
# ==========================

st.markdown(
    """<div class="fse-section-header">
        <h2>🔍 Análisis detallado</h2>
        <p class="fse-section-subtitle">
            Seleccioná una tecnología para ver su análisis completo
        </p>
    </div>""",
    unsafe_allow_html=True
)

# Selector de tecnología
tech_options = df["technology"].tolist()
selected_tech = st.selectbox(
    "Seleccionar tecnología",
    options=tech_options,
    index=0
)

tech_data = df.loc[df["technology"] == selected_tech].iloc[0]

# Obtener trend_type y confidence
trend_info = get_trend_display(tech_data.get("trend_type", "emerging"))

# 🆕 Usar la nueva función de confianza
confidence_display = format_confidence_display(
    tech_data["coverage_score"],
    tech_data["source_count"]
)

# 🆕 Formatear categoría
category_display = format_category(tech_data["category"])

# Layout de 4 columnas para el detalle
detail_cols = st.columns([1.5, 1, 0.8, 1])

with detail_cols[0]:
    st.markdown(
        f"""<div class="fse-detail-card">
            <div class="fse-detail-header">
                <h3>{tech_data['technology']}</h3>
                <span class="fse-detail-badge" style="background: {trend_info['color']}20; color: {trend_info['color']}; border: 1px solid {trend_info['color']}40;">
                    {trend_info['icon']} {trend_info['label']}
                </span>
            </div>
            <div style="margin-bottom: 0.5rem;">
                <span class="fse-detail-category">📂 {category_display}</span>
                <span class="fse-detail-sources-count">📚 {tech_data['source_count']} fuentes</span>
            </div>
            <div style="margin-bottom: 0.75rem;">
                <span style="font-size: 0.75rem; color: var(--fse-text-muted);">
                    {trend_info['description']}
                </span>
            </div>
            <div class="fse-detail-metrics">
                <div class="fse-detail-metric">
                    <span class="fse-detail-metric-label">{get_metric_display_name('research_score')}</span>
                    <span class="fse-detail-metric-value">{format_score(tech_data['research_score'])}</span>
                    {'<div class="fse-mini-bar"><div class="fse-mini-bar-fill" style="width: ' + format_score(tech_data['research_score'], 0) + '%; background: var(--fse-research-color);"></div></div>' if not pd.isna(tech_data['research_score']) else '<div style="font-size: 0.65rem; color: var(--fse-text-muted);">No data</div>'}
                </div>
                <div class="fse-detail-metric">
                    <span class="fse-detail-metric-label">{get_metric_display_name('github_score')}</span>
                    <span class="fse-detail-metric-value">{format_score(tech_data['github_score'])}</span>
                    {'<div class="fse-mini-bar"><div class="fse-mini-bar-fill" style="width: ' + format_score(tech_data['github_score'], 0) + '%; background: var(--fse-github-color);"></div></div>' if not pd.isna(tech_data['github_score']) else '<div style="font-size: 0.65rem; color: var(--fse-text-muted);">No data</div>'}
                </div>
                <div class="fse-detail-metric">
                    <span class="fse-detail-metric-label">{get_metric_display_name('stackoverflow_score')}</span>
                    <span class="fse-detail-metric-value">{format_score(tech_data['stackoverflow_score'])}</span>
                    {'<div class="fse-mini-bar"><div class="fse-mini-bar-fill" style="width: ' + format_score(tech_data['stackoverflow_score'], 0) + '%; background: var(--fse-stackoverflow-color);"></div></div>' if not pd.isna(tech_data['stackoverflow_score']) else '<div style="font-size: 0.65rem; color: var(--fse-text-muted);">No data</div>'}
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

with detail_cols[1]:
    st.markdown(
        f"""<div class="fse-detail-card">
            <div class="fse-detail-header">
                <h4>📊 Métricas clave</h4>
            </div>
            <div class="fse-detail-stats">
                <div class="fse-detail-stat">
                    <span class="fse-detail-stat-label">🏆 Future Score</span>
                    <span class="fse-detail-stat-value" style="font-size: 1.5rem; color: var(--fse-gradient-start);">
                        {format_score(tech_data['future_score'])}
                    </span>
                </div>
                <div class="fse-detail-stat">
                    <span class="fse-detail-stat-label">📈 Ranking</span>
                    <span class="fse-detail-stat-value">#{int(tech_data['rank'])}</span>
                </div>
                <div class="fse-detail-stat">
                    <span class="fse-detail-stat-label">📊 Confianza</span>
                    <span class="fse-detail-stat-value" style="font-size: 1.1rem;">
                        {confidence_display['icon']} {confidence_display['label']}
                    </span>
                </div>
                <div class="fse-detail-stat">
                    <span class="fse-detail-stat-label">📚 Fuentes</span>
                    <span class="fse-detail-stat-value">{tech_data['source_count']}/3</span>
                </div>
            </div>
            <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <span class="fse-detail-stat-label" style="font-size: 0.65rem; text-transform: uppercase; color: var(--fse-text-muted);">Versión del modelo</span>
                <div style="color: var(--fse-text-secondary); font-size: 0.8rem;">v1.0</div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

with detail_cols[2]:
    st.markdown(
        f"""<div class="fse-detail-card">
            <div class="fse-detail-header">
                <h4>🎯 Fuentes utilizadas</h4>
            </div>
            <div style="padding: 0.5rem 0;">
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    {''.join([f'<div class="fse-source-item">📚 {get_source_badge(source)}</div>' for source in tech_data['sources_used'].split(',') if source.strip()]) if tech_data['sources_used'] else '<div style="color: var(--fse-text-muted); font-size: 0.85rem;">No hay fuentes disponibles</div>'}
                </div>
            </div>
            <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <div style="font-size: 0.65rem; color: var(--fse-text-muted); text-transform: uppercase; margin-bottom: 0.25rem;">
                    Cobertura
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <div style="flex: 1; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; overflow: hidden;">
                        <div style="width: {tech_data['coverage_score'] if not pd.isna(tech_data['coverage_score']) else 0}%; height: 100%; background: { 'var(--fse-gradient-start)' if tech_data['coverage_score'] >= 80 else 'var(--fse-gradient-mid)' if tech_data['coverage_score'] >= 50 else 'var(--fse-gradient-end)' }; border-radius: 2px;"></div>
                    </div>
                    <span style="font-size: 0.8rem; min-width: 40px;">{format_score(tech_data['coverage_score'], 0)}%</span>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

with detail_cols[3]:
    # 🆕 Interpretación mejorada dependiendo de los datos
    explanation = tech_data['score_explanation'] if pd.notna(tech_data['score_explanation']) else None
    
    if explanation is None:
        # Generar interpretación automática
        has_research = not pd.isna(tech_data['research_score']) and tech_data['research_score'] > 30
        has_github = not pd.isna(tech_data['github_score']) and tech_data['github_score'] > 30
        has_so = not pd.isna(tech_data['stackoverflow_score']) and tech_data['stackoverflow_score'] > 30
        
        if has_research and has_github and has_so:
            explanation = f"{tech_data['technology']} muestra adopción balanceada en investigación, open source y comunidad de desarrolladores."
        elif has_research and has_so:
            explanation = f"{tech_data['technology']} tiene fuerte presencia en investigación y adopción por desarrolladores, aunque con actividad open source limitada."
        elif has_github and has_so:
            explanation = f"{tech_data['technology']} tiene alta adopción en la comunidad open source y entre desarrolladores, aunque con menor impacto académico."
        elif has_research and has_github:
            explanation = f"{tech_data['technology']} está impulsada principalmente por investigación y actividad open source."
        elif has_so:
            explanation = f"{tech_data['technology']} tiene alta adopción entre desarrolladores, aunque sin señales relevantes en investigación académica ni actividad open source reciente."
        else:
            explanation = f"Análisis basado en la combinación de tres fuentes de datos: investigación académica, actividad open source y adopción por desarrolladores."
    
    st.markdown(
        f"""<div class="fse-detail-card">
            <div class="fse-detail-header">
                <h4>💡 Interpretación</h4>
            </div>
            <div class="fse-insight-text">
                <p>{explanation}</p>
            </div>
            <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.05);">
                <span class="fse-detail-stat-label" style="font-size: 0.65rem; text-transform: uppercase; color: var(--fse-text-muted);">Composición del Score</span>
                <div style="display: flex; gap: 0.5rem; margin-top: 0.25rem; flex-wrap: wrap;">
                    <span class="fse-detail-tag">arXiv: {format_score(tech_data['research_score'])}%</span>
                    <span class="fse-detail-tag">GitHub: {format_score(tech_data['github_score'])}%</span>
                    <span class="fse-detail-tag">SO: {format_score(tech_data['stackoverflow_score'])}%</span>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )
    
st.write("")

# ==========================
# COMPARACIÓN ENTRE TECNOLOGÍAS
# ==========================

st.markdown(
    """<div class="fse-section-header">
        <h2>⚖️ Comparación de tecnologías</h2>
        <p class="fse-section-subtitle">
            Seleccioná dos tecnologías para comparar su performance
        </p>
    </div>""",
    unsafe_allow_html=True
)

# Selectores de comparación
comp_cols = st.columns(2)

with comp_cols[0]:
    tech1 = st.selectbox(
        "Tecnología 1",
        options=tech_options,
        index=0,
        key="comp1"
    )

with comp_cols[1]:
    tech2 = st.selectbox(
        "Tecnología 2",
        options=tech_options,
        index=1 if len(tech_options) > 1 else 0,
        key="comp2"
    )

if tech1 != tech2:
    data1 = df.loc[df["technology"] == tech1].iloc[0]
    data2 = df.loc[df["technology"] == tech2].iloc[0]
    
    # Comparación visual
    st.markdown(
        f"""<div class="fse-comparison-container">
            <div class="fse-comparison-item">
                <div class="fse-comparison-header">
                    <span class="fse-comparison-name">{data1['technology']}</span>
                    <span class="fse-comparison-score">{data1['future_score']:.1f}</span>
                </div>
                <div class="fse-comparison-bars">
                    <div class="fse-comp-bar">
                        <span class="fse-comp-label">Research</span>
                        <div class="fse-comp-bar-container">
                            <div class="fse-comp-bar-fill" style="width: {data1['research_score']}%; background: var(--fse-research-color);"></div>
                        </div>
                        <span class="fse-comp-value">{data1['research_score']:.1f}</span>
                    </div>
                    <div class="fse-comp-bar">
                        <span class="fse-comp-label">GitHub</span>
                        <div class="fse-comp-bar-container">
                            <div class="fse-comp-bar-fill" style="width: {data1['github_score']}%; background: var(--fse-github-color);"></div>
                        </div>
                        <span class="fse-comp-value">{data1['github_score']:.1f}</span>
                    </div>
                    <div class="fse-comp-bar">
                        <span class="fse-comp-label">Stack Overflow</span>
                        <div class="fse-comp-bar-container">
                            <div class="fse-comp-bar-fill" style="width: {data1['stackoverflow_score']}%; background: var(--fse-stackoverflow-color);"></div>
                        </div>
                        <span class="fse-comp-value">{data1['stackoverflow_score']:.1f}</span>
                    </div>
                </div>
                <div style="margin-top: 0.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="fse-comp-tag">Rank #{int(data1['rank'])}</span>
                    <span class="fse-comp-tag">{data1['source_count']} fuentes</span>
                </div>
            </div>
            <div class="fse-comparison-vs">VS</div>
            <div class="fse-comparison-item">
                <div class="fse-comparison-header">
                    <span class="fse-comparison-name">{data2['technology']}</span>
                    <span class="fse-comparison-score">{data2['future_score']:.1f}</span>
                </div>
                <div class="fse-comparison-bars">
                    <div class="fse-comp-bar">
                        <span class="fse-comp-label">Research</span>
                        <div class="fse-comp-bar-container">
                            <div class="fse-comp-bar-fill" style="width: {data2['research_score']}%; background: var(--fse-research-color);"></div>
                        </div>
                        <span class="fse-comp-value">{data2['research_score']:.1f}</span>
                    </div>
                    <div class="fse-comp-bar">
                        <span class="fse-comp-label">GitHub</span>
                        <div class="fse-comp-bar-container">
                            <div class="fse-comp-bar-fill" style="width: {data2['github_score']}%; background: var(--fse-github-color);"></div>
                        </div>
                        <span class="fse-comp-value">{data2['github_score']:.1f}</span>
                    </div>
                    <div class="fse-comp-bar">
                        <span class="fse-comp-label">Stack Overflow</span>
                        <div class="fse-comp-bar-container">
                            <div class="fse-comp-bar-fill" style="width: {data2['stackoverflow_score']}%; background: var(--fse-stackoverflow-color);"></div>
                        </div>
                        <span class="fse-comp-value">{data2['stackoverflow_score']:.1f}</span>
                    </div>
                </div>
                <div style="margin-top: 0.5rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="fse-comp-tag">Rank #{int(data2['rank'])}</span>
                    <span class="fse-comp-tag">{data2['source_count']} fuentes</span>
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

st.write("")

# ==========================
# INSIGHTS AUTOMÁTICOS - VERSIÓN MEJORADA 🆕
# ==========================

st.markdown(
    """<div class="fse-section-header">
        <h2>💡 Insights automáticos</h2>
        <p class="fse-section-subtitle">
            Análisis generados a partir de los datos
        </p>
    </div>""",
    unsafe_allow_html=True
)

# 🆕 Generar insights con manejo de NaN
top_tech = df.iloc[0]["technology"]
top_score = df.iloc[0]["future_score"]

# Filtrar NaN para cada métrica
research_df = df.dropna(subset=["research_score"])
github_df = df.dropna(subset=["github_score"])
so_df = df.dropna(subset=["stackoverflow_score"])

top_research = research_df.loc[research_df["research_score"].idxmax()]["technology"] if not research_df.empty else "N/A"
top_github = github_df.loc[github_df["github_score"].idxmax()]["technology"] if not github_df.empty else "N/A"
top_so = so_df.loc[so_df["stackoverflow_score"].idxmax()]["technology"] if not so_df.empty else "N/A"

# Insights de tendencias
trend_counts = df['trend_type'].value_counts() if 'trend_type' in df.columns else pd.Series()
trend_insights = []
if not trend_counts.empty:
    top_trend = trend_counts.index[0]
    trend_info = get_trend_display(top_trend)
    trend_insights.append(
        f"El tipo de tendencia más común es **{trend_info['icon']} {trend_info['label']}** con {trend_counts[top_trend]} tecnologías, lo que indica un ecosistema con {trend_info['description'].lower()}."
    )

insights = [
    {
        "type": "success",
        "text": f"**{top_tech}** lidera el ranking con un Future Score de {top_score:.1f}, destacándose en todas las dimensiones del análisis."
    }
]

if not research_df.empty:
    insights.append({
        "type": "success",
        "text": f"En investigación académica, **{top_research}** obtiene la mejor puntuación con {research_df['research_score'].max():.1f} puntos."
    })

if not github_df.empty:
    insights.append({
        "type": "success",
        "text": f"En el ecosistema open source, **{top_github}** domina con {github_df['github_score'].max():.1f} puntos en GitHub."
    })

if not so_df.empty:
    insights.append({
        "type": "success",
        "text": f"En adopción por desarrolladores, **{top_so}** lidera con {so_df['stackoverflow_score'].max():.1f} puntos en Stack Overflow."
    })

# Agregar insights de tendencias si existen
for insight_text in trend_insights:
    insights.append({
        "type": "info",
        "text": insight_text
    })

# Tecnologías con baja cobertura
low_coverage_df = df[df['coverage_score'] < 50]
if not low_coverage_df.empty:
    insights.append({
        "type": "warning",
        "text": f"{len(low_coverage_df)} tecnologías tienen una cobertura inferior al 50%, lo que indica que podrían estar subrepresentadas en las fuentes. ({', '.join(low_coverage_df['technology'].head(3).tolist())}{'...' if len(low_coverage_df) > 3 else ''})"
    })

for insight in insights:
    st.markdown(
        f"""<div class="fse-insight-card fse-insight-{insight['type']}">
            <span class="fse-insight-icon">
                {'✅' if insight['type'] == 'success' else 'ℹ️' if insight['type'] == 'info' else '⚠️'}
            </span>
            <span class="fse-insight-text">{insight['text']}</span>
        </div>""",
        unsafe_allow_html=True
    )

st.write("")

# ==========================
# EXPLICACIÓN DEL ALGORITMO (PLEGABLE) - VERSIÓN CORREGIDA 🆕
# ==========================

with st.expander("🤖 ¿Cómo se calcula el Future Score?", expanded=False):
    st.markdown(
        """<div class="fse-algorithm">
            <div class="fse-algorithm-intro">
                <p>El <strong>Future Score</strong> es un índice compuesto que estima el potencial futuro de una tecnología combinando evidencia de tres dimensiones complementarias:</p>
            </div>
            <div class="fse-algorithm-grid">
                <div class="fse-detail-card">
                    <div class="fse-algorithm-icon">📚</div>
                    <div class="fse-algorithm-content">
                        <h4>Research Score</h4>
                        <p>Volumen y crecimiento de publicaciones en arXiv. Mide la actividad científica y el interés académico.</p>
                        <div class="fse-algorithm-weight">Peso: 35%</div>
                        <div class="fse-algorithm-source">Fuente: arXiv</div>
                    </div>
                </div>
                <div class="fse-detail-card">
                    <div class="fse-algorithm-icon">💻</div>
                    <div class="fse-algorithm-content">
                        <h4>Adoption Score</h4>
                        <p>Demanda y popularidad en Stack Overflow. Refleja la adopción real por parte de la comunidad de desarrolladores.</p>
                        <div class="fse-algorithm-weight">Peso: 30%</div>
                        <div class="fse-algorithm-source">Fuente: Stack Overflow</div>
                    </div>
                </div>
                <div class="fse-detail-card">
                    <div class="fse-algorithm-icon">🌐</div>
                    <div class="fse-algorithm-content">
                        <h4>Ecosystem Score</h4>
                        <p>Actividad y salud del ecosistema en GitHub. Mide la contribución open source y el mantenimiento del proyecto.</p>
                        <div class="fse-algorithm-weight">Peso: 35%</div>
                        <div class="fse-algorithm-source">Fuente: GitHub</div>
                    </div>
                </div>
            </div>
            <div class="fse-detail-card">
                <div class="fse-formula-box">
                    <span class="fse-formula-label">Future Score =</span>
                    <span class="fse-formula-text">0.35 × Research + 0.30 × Adoption + 0.35 × Ecosystem</span>
                </div>
                <div class="fse-formula-note">
                    <span class="fse-formula-badge">Actualizado diariamente</span>
                    <span class="fse-formula-badge">Basado en datos reales</span>
                    <span class="fse-formula-badge">Cobertura ajustada por fuentes</span>
                </div>
            </div>
            <div style="margin-top: 1rem; padding: 0.75rem 1rem; background: rgba(255,255,255,0.03); border-radius: 8px; border-left: 3px solid var(--fse-gradient-start);">
                <p style="font-size: 0.8rem; color: var(--fse-text-secondary); margin: 0;">
                    <strong>ℹ️ Nota metodológica:</strong> Los pesos se ajustan dinámicamente cuando una tecnología no cuenta con información en alguna de las fuentes disponibles, redistribuyendo el peso entre las dimensiones existentes para mantener la comparabilidad del índice.
                </p>
            </div>
        </div>""",
        unsafe_allow_html=True
    )