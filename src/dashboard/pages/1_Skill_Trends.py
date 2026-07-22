"""
Skill Trends Dashboard
¿Qué tecnologías dominan el ecosistema de desarrollo?
"""

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
    page_title="Skill Trends",
    page_icon="📊",
    layout="wide",
)

load_css_bundle("styles.css", "skill_trends.css")

# ==========================
# QUERY
# ==========================

query = """
SELECT
    rank,
    skill,
    category,
    users_count
FROM gold.skill_trends
ORDER BY rank;
"""

with st.spinner("Cargando Skill Trends..."):
    df = pd.read_sql(query, engine)

if df.empty:
    st.info("No hay datos disponibles para mostrar.")
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
    """
    <div class="skill-trends-page">
        <div class="skill-trends-hero">
            <span class="skill-trends-badge">
                📊 DATOS DE STACK OVERFLOW
            </span>
            <h1>¿Qué tecnologías dominan el ecosistema?</h1>
            <p>Explorá las tecnologías más utilizadas por la comunidad 
            y detectá las habilidades con mayor adopción en el ecosistema tech.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# ¿QUÉ ES STACK OVERFLOW?
# ==========================

st.markdown(
    """<div class="skill-trends-panel">
        <div class="skill-trends-section-title">
            📄 ¿Qué es Stack Overflow?
        </div>
        <div class="skill-trends-section-subtitle">
            Stack Overflow es la comunidad más grande de desarrolladores del mundo, 
            donde se comparten conocimientos y se resuelven dudas sobre programación. 
            Cada año, realizan una encuesta global que captura las herramientas, 
            tecnologías y tendencias que están moldeando el futuro del desarrollo de software.
        </div>
    </div>""",
    unsafe_allow_html=True
)

# ==========================
# ¿CÓMO SE OBTUVO ESTE RANKING?
# ==========================

st.markdown(
    """<div class="skill-trends-panel">
        <div class="skill-trends-section-title">
            📊 ¿Cómo se obtuvo este ranking?
        </div>
        <div class="skill-trends-section-subtitle" style="line-height:1.8;">
            El ranking se construyó a partir de la <b style="color: #F5F7FB;">Stack Overflow Developer Survey</b>.
            Tras procesar y normalizar el archivo CSV, se filtraron únicamente las tecnologías
            marcadas como <b style="color: #F5F7FB;">Have Worked</b>, es decir, aquellas con las que los desarrolladores
            ya tienen experiencia. Luego se contabilizaron los usuarios únicos por habilidad,
            se agruparon por categoría y se ordenaron para generar el ranking.
            <br><br>
            Esta misma información también sirve como base para la sección
            <b style="color: #F5F7FB;">Skill Growth</b>, donde se combina con las respuestas
            <b style="color: #F5F7FB;">Want to Work</b> para identificar las tecnologías con mayor potencial de crecimiento.
        </div>
    </div>""",
    unsafe_allow_html=True
)

# ==========================
# KPIs
# ==========================

total_skills = len(df)
total_categories = df["category"].nunique()
top_skill = df.iloc[0]["skill"]
# Usar el máximo de usuarios (no la suma total, que es engañosa)
max_users = df["users_count"].max()

metrics = [
    ("🔬", "Habilidades analizadas", total_skills),
    ("📂", "Categorías", total_categories),
    ("🏆", "Tecnología líder", top_skill),
    ("👨‍💻", "Máx. desarrolladores", f'{max_users:,.0f}')
]

cols = st.columns(4)

for col, (icon, title, value) in zip(cols, metrics):
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

# ==========================
# CONTROLES
# ==========================

left, mid, right = st.columns([3, 2, 1])

with left:
    st.markdown(
        """
        <div class="skill-trends-panel">
            <div>
                <div class="skill-trends-section-title">📊 Ranking de tecnologías</div>
                <div class="skill-trends-section-subtitle">Tecnologías más utilizadas por la comunidad de desarrolladores.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with mid:
    # Filtro por categoría
    categories = ["Todas"] + sorted(df["category"].unique().tolist())
    selected_category = st.selectbox(
        "Filtrar por categoría",
        options=categories,
        index=0
    )

with right:
    top_n = st.select_slider(
        "Mostrar top",
        options=[10, 15, 20, 30, 40, 50],
        value=20,
    )

# Aplicar filtro de categoría
if selected_category != "Todas":
    filtered_df = df[df["category"] == selected_category]
else:
    filtered_df = df

top_df = filtered_df.head(top_n)

# ==========================
# GRÁFICO 1: RANKING
# ==========================

st.write("")

st.markdown(
    """
    <div class="skill-trends-panel skill-trends-chart-panel">
        <div class="skill-trends-section-title">🏆 Ranking de habilidades</div>
        <div class="skill-trends-section-subtitle">Tecnologías ordenadas por cantidad de desarrolladores que las utilizan.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

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
    hovertemplate=
    "<b>%{y}</b><br>"
    "Desarrolladores: %{x:,.0f}<br>"
    "Rank: %{customdata[0]}<br>"
    "Categoría: %{customdata[1]}<extra></extra>",
    customdata=top_df[
        [
            "rank",
            "category"
        ]
    ]
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

st.plotly_chart(fig, use_container_width=True)

# ==========================
# DISTRIBUCIÓN POR CATEGORÍA
# ==========================

st.write("")

st.markdown(
    """
    <div class="skill-trends-panel skill-trends-chart-panel">
        <div class="skill-trends-section-title">📂 Distribución por categoría</div>
        <div class="skill-trends-section-subtitle">Cantidad de desarrolladores agrupados por categoría de tecnología.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Agrupar por categoría
category_distribution = df.groupby("category")["users_count"].sum().reset_index()
category_distribution = category_distribution.sort_values("users_count", ascending=False)

# Paleta de colores azules
colors_pie = ["#6C7CFF", "#7DD3FC", "#34D399", "#F59E0B", "#F472B6", "#8B5CF6"]

fig_pie = px.pie(
    category_distribution,
    values="users_count",
    names="category",
    color_discrete_sequence=colors_pie,
    hole=0.4,
)

fig_pie.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>" +
                  "Desarrolladores: %{value:,.0f}<br>" +
                  "Porcentaje: %{percent}<extra></extra>",
    marker=dict(line=dict(color="rgba(0,0,0,0)", width=0)),
    pull=[0.03 if i == 0 else 0 for i in range(len(category_distribution))]
)

fig_pie.update_layout(
    template="plotly_dark",
    height=420,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(
        family="Space Grotesk, sans-serif",
        color="#F5F7FB"
    ),
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    )
)

st.plotly_chart(fig_pie, use_container_width=True)

st.write("")


# ==========================
# INSIGHT PRINCIPAL
# ==========================

st.markdown(
    """<div class="skill-trends-panel" style="margin-top: 0.5rem;">
        <div class="skill-trends-section-title">
            💡 Insight principal
        </div>
    </div>""",
    unsafe_allow_html=True
)

top_skill_data = df.iloc[0]
rank = int(top_skill_data["rank"])

st.markdown(
    f"""
    <div class="insight-card">
        <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
            <div class="insight-card-icon">🏆</div>
            <div class="insight-card-content">
                <div class="insight-card-title">{top_skill_data['skill']}</div>
                <div class="insight-card-metrics">
                    <div>
                        <div class="insight-card-metric-label">Ranking</div>
                        <div class="insight-card-metric-value">#{rank}</div>
                    </div>
                    <div>
                        <div class="insight-card-metric-label">Desarrolladores</div>
                        <div class="insight-card-metric-value">{top_skill_data['users_count']:,.0f}</div>
                    </div>
                    <div>
                        <div class="insight-card-metric-label">Categoría</div>
                        <div class="insight-card-metric-value">{top_skill_data['category']}</div>
                    </div>
                </div>
                <div class="insight-card-text">
                    <strong>{top_skill_data['skill']}</strong> es la tecnología más utilizada por los desarrolladores encuestados, 
                    con <span class="highlight">{top_skill_data['users_count']:,.0f}</span> profesionales que reportan tener experiencia con ella. 
                    Su adopción masiva y su presencia en la categoría <span class="highlight">{top_skill_data['category']}</span> 
                    la consolidan como una de las herramientas fundamentales en el ecosistema de desarrollo actual.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================
# RANKING TABLE
# ==========================

st.write("")

st.markdown(
    """
    <div class="skill-trends-panel skill-trends-table-panel">
        <div class="skill-trends-section-title">📋 Ranking completo</div>
        <div class="skill-trends-section-subtitle">Detalle de todas las habilidades analizadas y su categoría.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

display_df = df.rename(
    columns={
        "rank": "Rank",
        "skill": "Skill",
        "category": "Category",
        "users_count": "Developers"
    }
)

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(format="%d"),
        "Developers": st.column_config.NumberColumn(format="%d"),
    }
)
