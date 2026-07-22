"""
Research Growth Dashboard
¿Qué tecnologías están creciendo más rápido en la investigación científica?
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
            css_path = (
                Path(__file__).resolve().parents[1]
                / ".streamlit"
                / css_file
            )

            if css_path.exists():
                css_chunks.append(
                    css_path.read_text(
                        encoding="utf-8"
                    )
                )

        if css_chunks:
            st.markdown(
                f"<style>{''.join(css_chunks)}</style>",
                unsafe_allow_html=True
            )


st.set_page_config(
    page_title="Research Growth",
    page_icon="📈",
    layout="wide",
)

load_css_bundle(
    "styles.css",
    "arxiv_research_growth.css"
)

# ==========================
# QUERY - SOLO GOLD
# ==========================

query = """
SELECT
    technology,
    total_papers,
    papers_last_year,
    papers_previous_year,
    growth_rate,
    growth_multiplier,
    papers_last_90_days,
    active_months,
    growth_rate_score,
    recent_score,
    volume_score,
    consistency_score,
    growth_score,
    rank
FROM gold.research_growth
ORDER BY rank;
"""

with st.spinner("Cargando Research Growth..."):
    df = pd.read_sql(text(query), engine)

if df.empty:
    st.info("No hay datos disponibles.")
    st.stop()

# ==========================
# HEADER
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
    """<div class="arxiv-growth-page">
        <div class="arxiv-growth-hero">
            <span class="arxiv-growth-badge">
                📈 DATOS DE ARXIV
            </span>
            <h1>¿Qué tecnologías están creciendo más rápido en la investigación científica?</h1>
            <p>
            Basado en miles de publicaciones indexadas en arXiv,
            este ranking identifica las tecnologías cuya actividad 
            científica está creciendo más rápidamente.
            </p>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# ==========================
# ¿QUÉ ES UN PAPER? Y ¿CÓMO SE OBTUVO?
# ==========================

st.markdown(
    """<div class="arxiv-growth-panel">
        <div class="arxiv-growth-section-title">
            📄 ¿Qué es un paper?
        </div>
        <div class="arxiv-growth-section-subtitle">
            Un paper es un artículo científico que presenta resultados de investigación originales. 
            En el contexto de este dashboard, analizamos publicaciones indexadas en arXiv —el repositorio 
            de preprints más importante del mundo— para identificar las tecnologías que están ganando 
            mayor tracción dentro de la comunidad científica.
        </div>
    </div>""",
    unsafe_allow_html=True
)

st.markdown(
    """<div class="arxiv-growth-panel">
        <div class="arxiv-growth-section-title">
            📊 ¿Cómo se obtuvo este ranking?
        </div>
        <div class="arxiv-growth-section-subtitle">
            El ranking se construyó a partir de publicaciones indexadas en arXiv. 
            Cada tecnología fue analizada considerando su tasa de crecimiento anual, 
            la consistencia en el tiempo y la actividad reciente. El Growth Score 
            combina estos factores para identificar qué tecnologías están ganando 
            mayor tracción en la comunidad científica.
        </div>
    </div>""",
    unsafe_allow_html=True
)

# ==========================
# KPIs
# ==========================

total_technologies = len(df)
top_technology = df.iloc[0]["technology"]
max_growth_score = df["growth_score"].max()
total_papers_last_year = df["papers_last_year"].sum()

metrics = [
    ("📚", "Papers último año", f'{total_papers_last_year:,.0f}'),
    ("🏆", "Líder en crecimiento", top_technology),
    ("🚀", "Growth Score máximo", f"{max_growth_score:.1f}"),
    ("🔬", "Tecnologías analizadas", total_technologies)
]

cols = st.columns(4)

for col, (icon, title, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""<div class="arxiv-growth-metric-card">
                <div class="arxiv-growth-metric-icon">
                    {icon}
                </div>
                <div class="arxiv-growth-metric-body">
                    <p>{title}</p>
                    <h2>{value}</h2>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

st.write("")

# ==========================
# CONTROLES
# ==========================

left, right = st.columns([4, 1])

with left:
    st.markdown(
        """<div class="arxiv-growth-panel">
            <div>
                <div class="arxiv-growth-section-title">
                    📊 Ranking por aceleración científica
                </div>
                <div class="arxiv-growth-section-subtitle">
                    El Growth Score combina tasa de crecimiento, 
                    consistencia y actividad reciente.
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True
    )

with right:
    top_n = st.select_slider(
        "Mostrar top",
        options=[10, 15, 20, 30, 50],
        value=20
    )

df_top = df.head(top_n)

# ==========================
# GRÁFICO 1: RANKING
# ==========================

st.write("")

st.markdown(
    """<div class="arxiv-growth-panel arxiv-growth-chart-panel">
        <div class="arxiv-growth-section-title">
            🏆 Top tecnologías en crecimiento
        </div>
        <div class="arxiv-growth-section-subtitle">
            Tecnologías ordenadas por su Growth Score.
        </div>
    </div>""",
    unsafe_allow_html=True
)

# Gradiente de colores rosa
def get_score_color(score):
    if score >= 70:
        return "#EC4899"  # Rosa fuerte
    elif score >= 50:
        return "#F472B6"  # Rosa medio
    elif score >= 30:
        return "#F9A8D4"  # Rosa claro
    else:
        return "#FBCFE8"  # Rosa muy claro

colors = [get_score_color(score) for score in df_top["growth_score"]]

fig_rank = px.bar(
    df_top,
    x="growth_score",
    y="technology",
    orientation="h",
    text="growth_score",
)

fig_rank.update_traces(
    marker_color=colors,
    texttemplate="%{text:.1f}",
    textposition="outside",
    hovertemplate=
    "<b>%{y}</b><br>"
    "Growth Score: %{x:.1f}<br>"
    "Rank: %{customdata[4]}<br>"
    "Growth Rate: %{customdata[0]:.1f}x<br>"
    "Growth Multiplier: %{customdata[1]:.1f}x<br>"
    "Papers (1Y): %{customdata[2]:,.0f}<br>"
    "Papers (Prev): %{customdata[3]:,.0f}<extra></extra>",
    customdata=df_top[
        [
            "growth_rate",
            "growth_multiplier",
            "papers_last_year",
            "papers_previous_year",
            "rank"
        ]
    ]
)

fig_rank.update_layout(
    template="plotly_dark",
    height=550,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family="Space Grotesk, sans-serif", color="#F5F7FB"),
    xaxis=dict(
        title="Growth Score",
        showgrid=True,
        gridcolor="rgba(255,255,255,.08)",
        range=[0, 105]
    ),
    yaxis=dict(
        title=None,
        autorange="reversed"
    )
)

st.plotly_chart(
    fig_rank,
    use_container_width=True
)

# ==========================
# RANKING TABLE
# ==========================

st.write("")

st.markdown(
    """<div class="arxiv-growth-panel arxiv-growth-table-panel">
        <div class="arxiv-growth-section-title">
            📋 Ranking completo
        </div>
        <div class="arxiv-growth-section-subtitle">
            Detalle de todas las tecnologías analizadas.
        </div>
    </div>""",
    unsafe_allow_html=True
)

display = df.copy()

display = display.rename(columns={
    "rank": "Rank",
    "technology": "Technology",
    "growth_rate": "Growth Rate",
    "growth_multiplier": "Multiplier",
    "papers_last_year": "Papers (1Y)",
    "papers_previous_year": "Papers (Prev)",
    "papers_last_90_days": "Papers (90D)",
    "active_months": "Active Months",
    "growth_score": "Growth Score"
})

# Formatear números
display["Growth Score"] = display["Growth Score"].apply(lambda x: f"{x:.1f}")
display["Growth Rate"] = display["Growth Rate"].apply(lambda x: f"{x:.1f}x")
display["Multiplier"] = display["Multiplier"].apply(lambda x: f"{x:.1f}x")
display["Papers (1Y)"] = display["Papers (1Y)"].apply(lambda x: f"{x:,.0f}")
display["Papers (Prev)"] = display["Papers (Prev)"].apply(lambda x: f"{x:,.0f}")
display["Papers (90D)"] = display["Papers (90D)"].apply(lambda x: f"{x:,.0f}")

display = display[[
    "Rank",
    "Technology",
    "Growth Score",
    "Growth Rate",
    "Multiplier",
    "Papers (1Y)",
    "Papers (Prev)",
    "Papers (90D)",
    "Active Months"
]]

st.dataframe(
    display,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(format="%d"),
        "Technology": st.column_config.TextColumn("Technology"),
        "Growth Score": st.column_config.NumberColumn(
            "Growth Score",
            format="%.1f"
        ),
        "Growth Rate": st.column_config.TextColumn("Growth Rate"),
        "Multiplier": st.column_config.TextColumn("Multiplier"),
    }
)

# ==========================
# TECHNOLOGY DETAIL
# ==========================

st.write("")

st.markdown(
    """<div class="arxiv-growth-panel arxiv-growth-chart-panel">
        <div class="arxiv-growth-section-title">
            🔬 Detalle de la tecnología
        </div>
        <div class="arxiv-growth-section-subtitle">
            Seleccioná una tecnología para ver su análisis detallado.
        </div>
    </div>""",
    unsafe_allow_html=True
)

selected_tech = st.selectbox(
    "Seleccionar tecnología",
    options=df["technology"],
    index=0
)

tech_data = df.loc[
    df["technology"] == selected_tech
].iloc[0]

# ==========================
# DETAIL KPIs
# ==========================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Growth Score",
        f"{tech_data['growth_score']:.1f}",
        f"Rank #{int(tech_data['rank'])}"
    )

with k2:
    growth_pct = ((tech_data['papers_last_year'] - tech_data['papers_previous_year']) 
                  / tech_data['papers_previous_year'] * 100) if tech_data['papers_previous_year'] > 0 else float('inf')
    st.metric(
        "Growth Rate",
        f"{tech_data['growth_rate']:.1f}x",
        f"{growth_pct:.1f}% de incremento anual"
    )

with k3:
    st.metric(
        "Papers (1Y)",
        f"{tech_data['papers_last_year']:,.0f}",
        f"{tech_data['papers_previous_year']:,.0f} año anterior"
    )

with k4:
    st.metric(
        "Papers últimos 90 días",
        f"{tech_data['papers_last_90_days']:,.0f}",
        f"{tech_data['active_months']} meses activos"
    )

# ==========================
# RESUMEN Y DESGLOSE DEL SCORE
# ==========================


with st.expander("📊 Ver desglose del Growth Score", expanded=False):
    # Construir interpretación
    rank = int(tech_data['rank'])
    growth_pct = ((tech_data['papers_last_year'] - tech_data['papers_previous_year']) 
                  / tech_data['papers_previous_year'] * 100) if tech_data['papers_previous_year'] > 0 else float('inf')
    
    # Construir una interpretación narrativa
    if rank == 1:
        liderazgo = "lidera el ranking"
    elif rank <= 3:
        liderazgo = f"ocupa el puesto #{rank} del ranking"
    else:
        liderazgo = f"se encuentra en la posición #{rank} del ranking"
    
    if tech_data['growth_rate'] > 3:
        crecimiento = "con un crecimiento explosivo"
    elif tech_data['growth_rate'] > 1.5:
        crecimiento = "con un crecimiento acelerado"
    else:
        crecimiento = "con un crecimiento constante"
    
    st.markdown(
        f"""<div style="padding:12px 0;color:#94A3B8;line-height:1.8;">
            <b style="color:#F5F7FB;">{selected_tech}</b> {liderazgo} {crecimiento} de publicaciones durante el último año. 
            Su actividad reciente y la consistencia de publicaciones a lo largo del tiempo indican que continúa 
            ganando relevancia dentro de la comunidad científica.
            <br><br>
            <b style="color:#F5F7FB;">Growth Score:</b> {tech_data['growth_score']:.1f}<br>
            <b style="color:#F5F7FB;">Growth Rate:</b> {tech_data['growth_rate']:.1f}x ({growth_pct:.1f}% de incremento anual)<br>
            <b style="color:#F5F7FB;">Multiplicador:</b> {tech_data['growth_multiplier']:.1f}x (aceleración vs período anterior)<br>
            <b style="color:#F5F7FB;">Actividad reciente:</b> {tech_data['papers_last_90_days']:,.0f} papers en últimos 90 días
        </div>""",
        unsafe_allow_html=True
    )