"""
Research Trends Dashboard
¿Qué tecnologías están impulsando la investigación científica?
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
    page_title="Research Trends",
    page_icon="🔬",
    layout="wide",
)

load_css_bundle(
    "styles.css",
    "arxiv_research_trends.css"
)

# ==========================
# QUERY - SOLO GOLD
# ==========================

query = """
SELECT
    technology,
    unique_papers,
    papers_last_year,
    papers_last_90_days,
    category_count,
    research_score,
    rank
FROM gold.research_trends
ORDER BY rank;
"""

with st.spinner("Cargando Research Trends..."):
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
    """<div class="arxiv-research-page">
        <div class="arxiv-research-hero">
            <span class="arxiv-research-badge">
                🔬 DATOS DE ARXIV
            </span>
            <h1>¿Qué tecnologías dominan la investigación científica?</h1>
            <p>
            Basado en miles de publicaciones indexadas en arXiv, 
            este ranking identifica las tecnologías con mayor presencia 
            en la investigación científica reciente.
            </p>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# ==========================
# ¿CÓMO SE OBTUVO ESTE RANKING?
# ==========================

st.markdown(
    """<div class="arxiv-research-panel">
        <div class="arxiv-research-section-title">
            📄 ¿Qué es un paper?
        </div>
        <div class="arxiv-research-section-subtitle">
            Un paper es un artículo científico que presenta resultados de investigación originales. 
            En el contexto de este dashboard, analizamos publicaciones indexadas en arXiv —el repositorio 
            de preprints más importante del mundo— para identificar las tecnologías que están ganando 
            mayor tracción dentro de la comunidad científica.
        </div>
    </div>""",
    unsafe_allow_html=True
)

st.markdown(
    """<div class="arxiv-research-panel">
        <div class="arxiv-research-section-title">
            📊 ¿Cómo se obtuvo este ranking?
        </div>
        <div class="arxiv-research-section-subtitle">
            El ranking se construyó a partir de publicaciones indexadas en arXiv. Cada paper fue analizado para identificar las tecnologías mencionadas 
            y eliminar duplicados. <br>Finalmente se calculó un Research Score 
            considerando el volumen de publicaciones, la actividad reciente 
            y la diversidad de áreas de investigación.
            <br><br>
            Este dashboard responde a la pregunta: <br>
            <b style="color: #F5F7FB;">¿Qué tecnologías dominan la investigación científica actual?</b>
        </div>
    </div>""",
    unsafe_allow_html=True
)

# ==========================
# KPIs
# ==========================

total_technologies = len(df)
top_technology = df.iloc[0]["technology"]
total_papers = df["unique_papers"].sum()
total_papers_last_year = df["papers_last_year"].sum()
max_research_score = df["research_score"].max()
avg_research_score = df["research_score"].mean()

metrics = [
    ("📚", "Papers analizados", f'{total_papers:,.0f}'),
    ("🆕", "Papers último año", f'{total_papers_last_year:,.0f}'),
    ("🏆", "Tecnología líder", top_technology),
    ("🚀", "Score máximo", f'{max_research_score:.1f}')
]

cols = st.columns(4)

for col, (icon, title, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""<div class="arxiv-research-metric-card">
                <div class="arxiv-research-metric-icon">
                    {icon}
                </div>
                <div class="arxiv-research-metric-body">
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
        """<div class="arxiv-research-panel">
            <div>
                <div class="arxiv-research-section-title">
                    📊 Ranking por impacto científico
                </div>
                <div class="arxiv-research-section-subtitle">
                    El Research Score es un índice compuesto (0-100) que estima la relevancia científica de cada tecnología. Se calcula combinando el volumen histórico de publicaciones, la actividad reciente y la diversidad de áreas de investigación donde aparece cada tecnología. Un score más alto indica mayor presencia e impacto dentro de la literatura científica reciente.
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
    """<div class="arxiv-research-panel arxiv-research-chart-panel">
        <div class="arxiv-research-section-title">
            🏆 Top tecnologías en investigación
        </div>
        <div class="arxiv-research-section-subtitle">
            Tecnologías ordenadas por su Research Score.
        </div>
    </div>""",
    unsafe_allow_html=True
)

# Gradiente de colores rojo (igual que el rosa en Growth)
def get_score_color(score):
    if score >= 70:
        return "#EF4444"  # Rojo fuerte
    elif score >= 50:
        return "#F87171"  # Rojo medio
    elif score >= 30:
        return "#FCA5A5"  # Rojo claro
    else:
        return "#FECACA"  # Rojo muy claro

colors = [get_score_color(score) for score in df_top["research_score"]]

fig_rank = px.bar(
    df_top,
    x="research_score",
    y="technology",
    orientation="h",
    text="research_score",
)

fig_rank.update_traces(
    marker_color=colors,
    texttemplate="%{text:.1f}",
    textposition="outside",
    hovertemplate=
    "<b>%{y}</b><br>"
    "Research Score: %{x:.1f}<br>"
    "Rank: %{customdata[3]}<br>"
    "Papers: %{customdata[0]:,.0f}<br>"
    "Papers (1Y): %{customdata[1]:,.0f}<br>"
    "Áreas: %{customdata[2]}<extra></extra>",
    customdata=df_top[
        [
            "unique_papers",
            "papers_last_year",
            "category_count",
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
        title="Research Score",
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
    """<div class="arxiv-research-panel arxiv-research-table-panel">
        <div class="arxiv-research-section-title">
            📋 Ranking completo
        </div>
        <div class="arxiv-research-section-subtitle">
            Detalle de todas las tecnologías analizadas.
        </div>
    </div>""",
    unsafe_allow_html=True
)

display = df.copy()

display = display.rename(columns={
    "rank": "Rank",
    "technology": "Technology",
    "unique_papers": "Papers",
    "papers_last_year": "Papers (1Y)",
    "papers_last_90_days": "Papers (90D)",
    "category_count": "Areas",
    "research_score": "Score"
})

# Formatear números
display["Score"] = display["Score"].apply(lambda x: f"{x:.1f}")
display["Papers"] = display["Papers"].apply(lambda x: f"{x:,.0f}")
display["Papers (1Y)"] = display["Papers (1Y)"].apply(lambda x: f"{x:,.0f}")
display["Papers (90D)"] = display["Papers (90D)"].apply(lambda x: f"{x:,.0f}")

display = display[[
    "Rank",
    "Technology",
    "Score",
    "Papers",
    "Papers (1Y)",
    "Papers (90D)",
    "Areas"
]]

st.dataframe(
    display,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(format="%d"),
        "Technology": st.column_config.TextColumn("Technology"),
        "Score": st.column_config.NumberColumn(
            "Score",
            format="%.1f"
        ),
    }
)

# ==========================
# TECHNOLOGY DETAIL
# ==========================

st.write("")

st.markdown(
    """<div class="arxiv-research-panel arxiv-research-chart-panel">
        <div class="arxiv-research-section-title">
            🔬 Detalle de la tecnología
        </div>
        <div class="arxiv-research-section-subtitle">
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
        "Research Score",
        f"{tech_data['research_score']:.1f}",
        f"Rank #{int(tech_data['rank'])}"
    )

with k2:
    st.metric(
        "Papers totales",
        f"{tech_data['unique_papers']:,.0f}",
        f"{tech_data['papers_last_year']:,.0f} en último año"
    )

with k3:
    st.metric(
        "Papers últimos 90 días",
        f"{tech_data['papers_last_90_days']:,.0f}"
    )

with k4:
    st.metric(
        "Áreas de investigación",
        f"{tech_data['category_count']:,.0f}"
    )

# ==========================
# RESUMEN Y DESGLOSE DEL SCORE
# ==========================

with st.expander("📊 Ver desglose del Research Score", expanded=False):
    # Construir interpretación
    rank = int(tech_data['rank'])
    
    # Construir una interpretación narrativa
    if rank == 1:
        liderazgo = "lidera el ranking"
    elif rank <= 3:
        liderazgo = f"ocupa el puesto #{rank} del ranking"
    else:
        liderazgo = f"se encuentra en la posición #{rank} del ranking"
    
    if tech_data['research_score'] > 70:
        impacto = "con un impacto científico muy alto"
    elif tech_data['research_score'] > 50:
        impacto = "con un impacto científico significativo"
    else:
        impacto = "con un impacto científico moderado"
    
    st.markdown(
        f"""<div style="padding:12px 0;color:#94A3B8;line-height:1.8;">
            <b style="color:#F5F7FB;">{selected_tech}</b> {liderazgo} {impacto} en la literatura científica. 
            Su presencia en {tech_data['category_count']} áreas de investigación y su volumen de publicaciones 
            la posicionan como una tecnología relevante dentro de la comunidad académica.
            <br><br>
            <b style="color:#F5F7FB;">Research Score:</b> {tech_data['research_score']:.1f}<br>
            <b style="color:#F5F7FB;">Volumen de papers:</b> {tech_data['unique_papers']:,.0f} publicaciones únicas<br>
            <b style="color:#F5F7FB;">Actividad reciente:</b> {tech_data['papers_last_year']:,.0f} papers en el último año<br>
            <b style="color:#F5F7FB;">Actualidad inmediata:</b> {tech_data['papers_last_90_days']:,.0f} papers en últimos 90 días<br>
            <b style="color:#F5F7FB;">Diversidad:</b> presencia en {tech_data['category_count']} áreas de investigación
        </div>""",
        unsafe_allow_html=True
    )