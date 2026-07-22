"""
GitHub Momentum Dashboard
Cada gráfico responde una pregunta distinta sobre el ecosistema.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
    page_title="GitHub Momentum",
    page_icon="🔥",
    layout="wide",
)

load_css_bundle(
    "styles.css",
    "github_momentum.css"
)

# ==========================
# QUERY
# ==========================

query = """
SELECT
    rank,
    technology,
    repo_count,
    total_stars,
    avg_stars,
    total_forks,
    avg_forks,
    active_repo_count,
    recent_1y_count,
    stars_score,
    forks_score,
    repo_score,
    recent_score,
    active_score,
    momentum_score
FROM gold.github_skill_momentum
ORDER BY rank;
"""

with st.spinner("Cargando GitHub Momentum..."):
    df = pd.read_sql(query, engine)

if df.empty:
    st.info("No hay datos disponibles.")
    st.stop()


# ==========================
# HEADER Y EXPLICACIÓN
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
    """<div class="github-momentum-page">
        <div class="github-momentum-hero">
            <span class="github-momentum-badge">
                🔥 DATOS DE GITHUB
            </span>
            <h1>¿Qué tecnologías tienen mayor actividad en GitHub?</h1>
            <p>
            Explorá qué tecnologías presentan mayor actividad en GitHub
            a partir del análisis de repositorios, estrellas, forks y
            mantenimiento reciente.
            </p>
        </div>
    </div>""",
    unsafe_allow_html=True,
)


st.markdown(
    """<div class="github-momentum-panel">
        <div class="github-momentum-section-title">
            📄 ¿Qué es un repositorio en GitHub?
        </div>
        <div class="github-momentum-section-subtitle">
            Un repositorio es el espacio donde se almacena el código de un proyecto en GitHub. Analizando miles de repositorios públicos podemos medir la actividad, adopción y popularidad de distintas tecnologías.
        </div>
    </div>""",
    unsafe_allow_html=True
)



st.markdown(
    """<div class="github-momentum-panel">
        <div class="github-momentum-section-title">
            📊 ¿Cómo se calcula el Momentum Score?
        </div>
        <div class="github-momentum-section-subtitle"
             style="line-height:1.8;">
            El <b>Momentum Score</b> resume el estado de cada tecnología
            mediante una combinación ponderada de cinco indicadores del
            ecosistema GitHub.
            <br><br>
            ⭐ Popularidad (Stars) — 30%<br>
            🍴 Comunidad (Forks) — 25%<br>
            📦 Cantidad de repositorios — 20%<br>
            🚀 Repositorios creados durante el último año — 15%<br>
            🔄 Repositorios con actividad reciente — 10%
            <br><br>
            Todas las variables se normalizan utilizando una escala
            logarítmica para reducir el impacto de proyectos
            excepcionalmente grandes y facilitar una comparación
            equilibrada entre tecnologías.
        </div>
    </div>""",
    unsafe_allow_html=True,
)



# ==========================
# KPIs
# ==========================

metrics = [
    ("💻", "Tecnologías", len(df)),
    ("🏆", "Líder", df.iloc[0]["technology"]),
    ("⭐", "Stars totales", f'{df["total_stars"].sum()/1_000_000:.1f}M'),
    ("🚀", "Repos nuevos (1 año)", f'{df["recent_1y_count"].sum():,.0f}')
]

cols = st.columns(4)

for col, (icon, title, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""<div class="github-momentum-metric-card">
                <div class="github-momentum-metric-icon">
                    {icon}
                </div>
                <div class="github-momentum-metric-body">
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
        """<div class="github-momentum-panel">
            <div>
                <div class="github-momentum-section-title">
                    📊 Visualizando el Momentum
                </div>
                <div class="github-momentum-section-subtitle">
                    Cada gráfico responde una pregunta distinta.
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
# GRÁFICO 1: MOMENTUM RANKING
# PREGUNTA: ¿Quién lidera el ranking?
# ==========================

st.write("")

st.markdown(
    """<div class="github-momentum-panel github-momentum-chart-panel">
        <div class="github-momentum-section-title">
            🏆 Tecnologías con mayor Momentum
        </div>
        <div class="github-momentum-section-subtitle">
            Tecnologías ordenadas según su Momentum Score.
        </div>
    </div>""",
    unsafe_allow_html=True
)

fig_rank = px.bar(
    df_top,
    x="momentum_score",
    y="technology",
    orientation="h",
    text="momentum_score",
)

fig_rank.update_traces(

    marker_color="#C4B5FD",

    texttemplate="%{text:.1f}",

    textposition="outside",

    hovertemplate=
    "<b>%{y}</b><br>"
    "Momentum: %{x:.1f}<br>"
    "Repositorios: %{customdata[0]:,.0f}<br>"
    "Stars: %{customdata[1]:,.0f}<extra></extra>",

    customdata=df_top[
        [
            "repo_count",
            "total_stars"
        ]
    ]
)

fig_rank.update_layout(

    template="plotly_dark",

    height=550,

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    font=dict(
        family="Space Grotesk, sans-serif",
        color="#F5F7FB"
    ),

    xaxis=dict(

        title="Momentum Score",

        showgrid=True,

        gridcolor="rgba(255,255,255,.08)",

        range=[0,105]

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
# BREAKDOWN DEL MOMENTUM SCORE
# ==========================

st.write("")

st.markdown(
    """<div class="github-momentum-panel github-momentum-chart-panel">
        <div class="github-momentum-section-title">
            🔍 ¿Cómo se compone el Momentum Score?
        </div>
        <div class="github-momentum-section-subtitle">
            Seleccioná una tecnología para analizar el aporte de cada
            componente al puntaje final.
        </div>
    </div>""",
    unsafe_allow_html=True
)

selected_tech = st.selectbox(
    "Analizar tecnología",
    options=df_top["technology"],
    index=0
)

tech_data = df.loc[
    df["technology"] == selected_tech
].iloc[0]


# ==========================
# KPIs
# ==========================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Momentum Score",
        f"{tech_data['momentum_score']:.1f}",
        f"Rank #{int(tech_data['rank'])}"
    )

with k2:
    st.metric(
        "Repositorios",
        f"{tech_data['repo_count']:,.0f}",
        f"{tech_data['recent_1y_count']:,.0f} nuevos"
    )

with k3:
    st.metric(
        "Stars",
        f"{tech_data['total_stars']:,.0f}",
        f"{tech_data['avg_stars']:,.0f} promedio"
    )

with k4:
    st.metric(
        "Repos activos",
        f"{tech_data['active_repo_count']:,.0f}",
        "Últimos 6 meses"
    )


# ==========================
# RADAR
# ==========================

radar_df = pd.DataFrame({

    "Componente": [

        "Stars",
        "Forks",
        "Repositories",
        "Recent",
        "Active"

    ],

    "Score": [

        tech_data["stars_score"],
        tech_data["forks_score"],
        tech_data["repo_score"],
        tech_data["recent_score"],
        tech_data["active_score"]

    ]

})

fig_radar = px.line_polar(

    radar_df,

    r="Score",

    theta="Componente",

    line_close=True,

    markers=True,

    range_r=[0,100],

    color_discrete_sequence=["#C4B5FD"]

)

fig_radar.update_traces(

    line=dict(

        color="#C4B5FD",

        width=3

    ),

    marker=dict(

        size=8,

        color="#C4B5FD"

    ),

    fill="toself",

    fillcolor="rgba(196,181,253,0.18)",

    hovertemplate=

    "<b>%{theta}</b><br>" +

    "Score: %{r:.1f}<extra></extra>"

)

fig_radar.update_layout(

    template="plotly_dark",

    height=470,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    margin=dict(

        l=35,

        r=35,

        t=35,

        b=35

    ),

    font=dict(

        family="Space Grotesk, sans-serif",

        color="#F5F7FB"

    ),

    polar=dict(

        bgcolor="rgba(0,0,0,0)",

        radialaxis=dict(

            visible=True,

            range=[0,100],

            tick0=0,

            dtick=20,

            gridcolor="rgba(255,255,255,.08)",

            linecolor="rgba(255,255,255,.08)"

        ),

        angularaxis=dict(

            gridcolor="rgba(255,255,255,.08)",

            linecolor="rgba(255,255,255,.08)"

        )

    ),

    showlegend=False

)

st.plotly_chart(
    fig_radar,
    use_container_width=True
)

# ==========================
# TABLA DETALLADA
# ==========================

st.write("")

st.markdown(
    """<div class="github-momentum-panel github-momentum-table-panel">
        <div class="github-momentum-section-title">
            📋 Dataset completo
        </div>
        <div class="github-momentum-section-subtitle">
            Todas las métricas disponibles para análisis.
        </div>
    </div>""",
    unsafe_allow_html=True
)

display = df.copy()

# Renombrar columnas
display = display.rename(columns={
    "rank": "Rank",
    "technology": "Technology",
    "repo_count": "Repos",
    "total_stars": "Stars",
    "avg_stars": "Stars avg",
    "total_forks": "Forks",
    "avg_forks": "Forks avg",
    "active_repo_count": "Active",
    "recent_1y_count": "New (1Y)",
    "stars_score": "Stars score",
    "forks_score": "Forks score",
    "repo_score": "Repos score",
    "recent_score": "Recent score",
    "active_score": "Active score",
    "momentum_score": "Momentum"
})

# Formatear números
display["Stars"] = display["Stars"].apply(lambda x: f"{x:,.0f}")
display["Repos"] = display["Repos"].apply(lambda x: f"{x:,.0f}")
display["Forks"] = display["Forks"].apply(lambda x: f"{x:,.0f}")
display["Stars avg"] = display["Stars avg"].apply(lambda x: f"{x:,.0f}")
display["Forks avg"] = display["Forks avg"].apply(lambda x: f"{x:,.0f}")

st.dataframe(
    display,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(format="%d"),
        "Momentum": st.column_config.NumberColumn(format="%.1f"),
        "Stars score": st.column_config.NumberColumn(format="%.1f"),
        "Forks score": st.column_config.NumberColumn(format="%.1f"),
        "Repos score": st.column_config.NumberColumn(format="%.1f"),
        "Recent score": st.column_config.NumberColumn(format="%.1f"),
        "Active score": st.column_config.NumberColumn(format="%.1f"),
    }
)