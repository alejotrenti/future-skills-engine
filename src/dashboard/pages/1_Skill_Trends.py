import pandas as pd
import plotly.express as px
import streamlit as st

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
    page_title="Tendencias de habilidades",
    page_icon="📈",
    layout="wide",
)

load_css_bundle("styles.css", "skill_trends.css")

query = """
SELECT
    rank,
    skill,
    category,
    users_count
FROM gold.skill_trends
ORDER BY rank;
"""

df = pd.read_sql(query, engine)

with st.spinner("Cargando Skill Trends..."):
    df = pd.read_sql(query, engine)

if df.empty:
    st.info("No hay datos disponibles para mostrar.")
    st.stop()

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
    """
    <div class="skill-trends-page">
        <div class="skill-trends-hero">
            <span class="skill-trends-badge">🚀 con RESPUESTAS DE STACK OVERFLOW</span>
            <h1>Tendencias de habilidadess</h1>
            <p>Explorá las tecnologías más utilizadas por la comunidad y detectá las habilidades con mayor impulso en el ecosistema tech.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """<div class="skill-trends-panel" style="margin-bottom:1.5rem;">
        <div class="skill-trends-section-title">
            📊 ¿Cómo se obtuvo este ranking?
        </div>
        <div class="skill-trends-section-subtitle" style="line-height:1.8;">
            El ranking se construyó a partir de la <b>Stack Overflow Developer Survey</b>.
            Tras procesar y normalizar el archivo CSV, se filtraron únicamente las tecnologías
            marcadas como <b>HaveWorked</b>, es decir, aquellas con las que los desarrolladores
            ya tienen experiencia. Luego se contabilizaron los usuarios únicos por habilidad,
            se agruparon por categoría y se ordenaron para generar el ranking.
            <br><br>
            Esta misma información también sirve como base para la sección
            <b>Skill Growth</b>, donde se combina con las respuestas
            <b>WantToWork</b> para identificar las tecnologías con mayor potencial de crecimiento.
        </div>
    </div>""",
    unsafe_allow_html=True,
)

metrics = [
    ("🧩", "Habilidades", len(df)),
    ("📚", "Categorías", df["category"].nunique()),
    ("🔥", "Más utilizada", df.iloc[0]["skill"]),
]

metric_cols = st.columns(3)
for col, (icon, title, value) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="skill-trends-metric-card">
                <div class="skill-trends-metric-icon">{icon}</div>
                <div class="skill-trends-metric-body">
                    <p>{title}</p>
                    <h2>{value}</h2>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")


left, right = st.columns([4, 1], gap="medium")

with left:
    
    st.markdown(
        """
        <div class="skill-trends-panel">
            <div>
                <div class="skill-trends-section-title">Ranking de tecnologías</div>
                <div class="skill-trends-section-subtitle">Seleccioná cuántas habilidades querés comparar en el análisis.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    top_n = st.select_slider(
        "Seleccioná:",
        options=[5, 10, 15, 20, 30, 40, 50],
        value=20,
    )

top_df = df.head(top_n)

palette = ["#6C7CFF", "#7DD3FC", "#34D399", "#F59E0B", "#F472B6", "#8B5CF6"]
fig = px.bar(
    top_df,
    x="users_count",
    y="skill",
    orientation="h",
    text="users_count",
    color="category",
    color_discrete_sequence=palette,
)

fig.update_traces(
    textposition="outside",
    texttemplate="%{text:,}",
    marker_line_color="rgba(255,255,255,0.10)",
    marker_line_width=1,
)

fig.update_layout(
    height=560,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="Cantidad de desarrolladores",
    yaxis_title=None,
    legend_title="Categoría",
    font=dict(family="Space Grotesk, sans-serif", color="#F5F7FB"),
    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", zeroline=False),
    yaxis=dict(showgrid=False, autorange="reversed"),
)

st.markdown(
    """
    <div class="skill-trends-panel skill-trends-chart-panel">
        <div class="skill-trends-section-title">Ranking actual de habilidades</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.plotly_chart(fig, use_container_width=True)

st.write("")

st.markdown(
    """
    <div class="skill-trends-panel skill-trends-table-panel">
        <div class="skill-trends-section-title">Ranking completo</div>
        <div class="skill-trends-section-subtitle">Detalle de todas las habilidades analizadas y su categoría.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
display_df = df.rename(
    columns={
        "rank":"Ranking",
        "skill":"Habilidad",
        "category":"Categoría",
        "users_count":"Desarrolladores"
    }
)

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True
)