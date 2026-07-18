"""
GitHub Topics Dashboard
Exploración del ecosistema GitHub a través de tópicos.
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
    page_title="GitHub Topics",
    page_icon="🏷️",
    layout="wide",
)

load_css_bundle(
    "styles.css",
    "github_topics.css"
)

# ==========================
# QUERY (sin trend_score)
# ==========================

query = """
    SELECT
        rank,
        topic,
        repo_count,
        total_stars,
        avg_stars,
        total_forks,
        avg_forks,
        languages,
        recent_repo_count,
        active_repo_count
    FROM gold.github_topic_trends
    ORDER BY rank;
"""

with st.spinner("Cargando GitHub Topics..."):
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
    """<div class="github-topics-page">
        <div class="github-topics-hero">
            <span class="github-topics-badge">
                🏷️ GITHUB TOPICS
            </span>
            <h1>Explorá el ecosistema <span class="highlight">GitHub</span></h1>
            <p>
            Los <b>Topics</b> son etiquetas que los desarrolladores asignan
            a sus repositorios para describir tecnologías, frameworks,
            lenguajes o áreas de conocimiento.
            <br><br>
            Analizarlos permite identificar tendencias, comunidades activas
            y áreas con mayor crecimiento dentro del ecosistema open source.
            </p>
        </div>
    </div>""",
    unsafe_allow_html=True,
)


# ==========================
# EXPLICACIÓN
# ==========================

st.markdown(
    """<div class="github-topics-panel">
        <div class="github-topics-section-title">
            📐 ¿Qué estamos midiendo?
        </div>
        <div class="github-topics-section-subtitle"
             style="line-height:1.8;">
            Cada Topic se analiza desde múltiples dimensiones:
            <br><br>
            📦 <b>Tamaño del ecosistema</b> — Cantidad de repositorios<br>
            ⭐ <b>Popularidad</b> — Total de estrellas acumuladas<br>
            🍴 <b>Comunidad</b> — Total de forks<br>
            🔄 <b>Mantenimiento</b> — Repositorios actualizados recientemente<br>
            🚀 <b>Adopción reciente</b> — Repositorios creados en el último año<br>
            🌐 <b>Diversidad</b> — Lenguajes utilizados en el ecosistema
        </div>
    </div>""",
    unsafe_allow_html=True,
)


# ==========================
# KPIs
# ==========================

metrics = [
    ("🏷️", "Topics", len(df)),
    ("📦", "Repositorios", f'{df["repo_count"].sum():,}'),
    ("⭐", "Stars totales", f'{df["total_stars"].sum()/1_000_000:.1f}M'),
    ("🍴", "Forks totales", f'{df["total_forks"].sum()/1_000_000:.1f}M')
]

cols = st.columns(4)

for col, (icon, title, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""<div class="github-topics-metric-card">
                <div class="github-topics-metric-icon">
                    {icon}
                </div>
                <div class="github-topics-metric-body">
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
        """<div class="github-topics-panel">
            <div>
                <div class="github-topics-section-title">
                    📊 Explorando Topics
                </div>
                <div class="github-topics-section-subtitle">
                    Visualizá las comunidades y tendencias en GitHub.
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
# GRÁFICO 1: TOPICS MÁS POPULARES (Horizontal Bar)
# PREGUNTA: ¿Cuáles son los Topics con más estrellas?
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-chart-panel">
        <div class="github-topics-section-title">
            ⭐ Topics más populares
        </div>
        <div class="github-topics-section-subtitle">
            Los Topics con mayor cantidad de estrellas acumuladas.
        </div>
    </div>""",
    unsafe_allow_html=True
)

fig_popular = px.bar(
    df_top,
    x="total_stars",
    y="topic",
    orientation="h",
    text="total_stars",
    color="repo_count",
    color_continuous_scale="Viridis",
    labels={
        "total_stars": "Total de estrellas",
        "topic": "",
        "repo_count": "Repositorios"
    }
)

fig_popular.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside",
    marker=dict(
        line=dict(width=0)
    ),
    hovertemplate="<b>%{y}</b><br>" +
                  "Stars: %{x:,.0f}<br>" +
                  "Repos: %{marker.color:,.0f}<extra></extra>"
)

fig_popular.update_layout(
    template="plotly_dark",
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(
        family="Space Grotesk, sans-serif",
        color="#F5F7FB"
    ),
    xaxis=dict(
        title="Estrellas",
        showgrid=True,
        gridcolor="rgba(255,255,255,.08)",
        showline=True,
        linecolor="rgba(255,255,255,.1)"
    ),
    yaxis=dict(
        title=None,
        autorange="reversed"
    ),
    coloraxis_colorbar=dict(
        title="Repos",
        tickformat=",.0f"
    )
)

st.plotly_chart(fig_popular, use_container_width=True)


# ==========================
# GRÁFICO 2: BUBBLE CHART
# PREGUNTA: ¿Cómo se relaciona popularidad vs ecosistema?
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-chart-panel">
        <div class="github-topics-section-title">
            🌐 Popularidad vs Ecosistema
        </div>
        <div class="github-topics-section-subtitle">
            <b>Eje X:</b> Repositorios  |  
            <b>Eje Y:</b> Estrellas totales  |  
            <b>Tamaño:</b> Forks  |  
            <b>Color:</b> Repos activos
        </div>
    </div>""",
    unsafe_allow_html=True
)

fig_bubble = px.scatter(
    df_top,
    x="repo_count",
    y="total_stars",
    size="total_forks",
    color="active_repo_count",
    hover_name="topic",
    text="topic",
    size_max=50,
    color_continuous_scale="Viridis",
    labels={
        "repo_count": "Repositorios totales",
        "total_stars": "Estrellas totales",
        "total_forks": "Forks totales",
        "active_repo_count": "Repos activos"
    },
    log_x=True,
    log_y=True
)

fig_bubble.update_traces(
    textposition="top center",
    marker=dict(
        line=dict(width=1, color="rgba(255,255,255,0.2)")
    ),
    hovertemplate="<b>%{hovertext}</b><br>" +
                  "Repos: %{x:,.0f}<br>" +
                  "Stars: %{y:,.0f}<br>" +
                  "Forks: %{marker.size:,.0f}<br>" +
                  "Activos: %{marker.color:,.0f}<extra></extra>"
)

fig_bubble.update_layout(
    template="plotly_dark",
    height=550,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(
        family="Space Grotesk, sans-serif",
        color="#F5F7FB"
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,.06)",
        showline=True,
        linecolor="rgba(255,255,255,.1)"
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,.06)",
        showline=True,
        linecolor="rgba(255,255,255,.1)"
    ),
    coloraxis_colorbar=dict(
        title="Repos activos",
        tickformat=",.0f"
    )
)

st.plotly_chart(fig_bubble, use_container_width=True)


# ==========================
# GRÁFICO 3: TREEMAP
# PREGUNTA: ¿Cómo se distribuye la popularidad en el ecosistema?
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-chart-panel">
        <div class="github-topics-section-title">
            🗺️ Distribución de popularidad
        </div>
        <div class="github-topics-section-subtitle">
            <b>Tamaño:</b> Estrellas  |  
            <b>Color:</b> Cantidad de repositorios
        </div>
    </div>""",
    unsafe_allow_html=True
)

fig_treemap = px.treemap(
    df_top,
    path=["topic"],
    values="total_stars",
    color="repo_count",
    color_continuous_scale="Viridis",
    hover_data={
        "total_stars": ":,.0f",
        "repo_count": ":,.0f",
        "languages": True,
        "active_repo_count": ":,.0f"
    },
    labels={
        "topic": "Topic",
        "total_stars": "Estrellas",
        "repo_count": "Repositorios",
        "languages": "Lenguajes",
        "active_repo_count": "Repos activos"
    }
)

fig_treemap.update_traces(
    textinfo="label+value",
    textposition="middle center",
    hovertemplate="<b>%{label}</b><br>" +
                  "Stars: %{value:,.0f}<br>" +
                  "Repos: %{color:,.0f}<br>" +
                  "Lenguajes: %{customdata[0]}<br>" +
                  "Activos: %{customdata[1]:,.0f}<extra></extra>"
)

fig_treemap.update_layout(
    template="plotly_dark",
    height=550,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=10, b=10),
    font=dict(
        family="Space Grotesk, sans-serif",
        color="#F5F7FB"
    ),
    coloraxis_colorbar=dict(
        title="Repositorios",
        tickformat=",.0f"
    )
)

st.plotly_chart(fig_treemap, use_container_width=True)


# ==========================
# GRÁFICO 4: EXPLORAR TOPIC (Perfil + Buscador unificados)
# PREGUNTA: ¿Cómo es la comunidad de un Topic específico?
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-chart-panel">
        <div class="github-topics-section-title">
            🔍 Explorar un Topic
        </div>
        <div class="github-topics-section-subtitle">
            Seleccioná un Topic para ver su ecosistema en detalle.
        </div>
    </div>""",
    unsafe_allow_html=True
)

# Selector único con todos los topics ordenados alfabéticamente
all_topics = sorted(df["topic"].tolist())
selected_topic = st.selectbox(
    "Seleccionar o buscar un Topic",
    options=all_topics,
    index=0
)

if selected_topic:
    topic_data = df[df["topic"] == selected_topic].iloc[0]
    global_rank = int(topic_data["rank"])
    
    # KPIs del Topic
    k1, k2, k3, k4, k5 = st.columns(5)
    
    with k1:
        st.metric(
            "Ranking global",
            f"#{global_rank}",
            f"de {len(df)} topics"
        )
    
    with k2:
        st.metric(
            "Repositorios",
            f"{topic_data['repo_count']:,.0f}",
            f"{topic_data['languages']}"
        )
    
    with k3:
        st.metric(
            "Estrellas",
            f"{topic_data['total_stars']:,.0f}",
            f"{topic_data['avg_stars']:,.0f} promedio"
        )
    
    with k4:
        st.metric(
            "Forks",
            f"{topic_data['total_forks']:,.0f}",
            f"{topic_data['avg_forks']:,.0f} promedio"
        )
    
    with k5:
        st.metric(
            "Repos activos",
            f"{topic_data['active_repo_count']:,.0f}",
            f"{topic_data['recent_repo_count']:,.0f} nuevos (1 año)"
        )


# ==========================
# GRÁFICO 5: TOPICS DE ALTO CRECIMIENTO
# PREGUNTA: ¿Qué Topics están creciendo más rápido?
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-chart-panel">
        <div class="github-topics-section-title">
            📈 Topics de alto crecimiento
        </div>
        <div class="github-topics-section-subtitle">
            Topics con mayor proporción de repositorios creados recientemente
            (mínimo 200 repositorios totales).
        </div>
    </div>""",
    unsafe_allow_html=True
)

# Calcular crecimiento como % de repos recientes
df["recent_percentage"] = (df["recent_repo_count"] / df["repo_count"] * 100).round(1)

# Filtro más estricto: mínimo 200 repos para evitar ruido
growth_df = df[
    (df["recent_percentage"] > 15) &
    (df["repo_count"] >= 200)
].head(15).sort_values("recent_percentage", ascending=True)

if not growth_df.empty:
    fig_growth = px.bar(
        growth_df,
        x="recent_percentage",
        y="topic",
        orientation="h",
        text="recent_percentage",
        color="recent_repo_count",
        color_continuous_scale="Viridis",
        labels={
            "recent_percentage": "% repos recientes",
            "topic": "",
            "recent_repo_count": "Cantidad de repos nuevos"
        }
    )
    
    fig_growth.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker=dict(
            line=dict(width=0)
        ),
        hovertemplate="<b>%{y}</b><br>" +
                      "Repos recientes: %{x:.1f}%<br>" +
                      "Nuevos repos: %{marker.color:,.0f}<extra></extra>"
    )
    
    fig_growth.update_layout(
        template="plotly_dark",
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            family="Space Grotesk, sans-serif",
            color="#F5F7FB"
        ),
        xaxis=dict(
            title="% de repositorios recientes",
            showgrid=True,
            gridcolor="rgba(255,255,255,.08)",
            showline=True,
            linecolor="rgba(255,255,255,.1)"
        ),
        yaxis=dict(
            title=None,
            autorange="reversed"
        ),
        coloraxis_colorbar=dict(
            title="Repos nuevos",
            tickformat=",.0f"
        )
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
else:
    st.info("No se encontraron Topics con crecimiento significativo (mínimo 200 repositorios).")


# ==========================
# TABLA DETALLADA (sin Trend Score)
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-table-panel">
        <div class="github-topics-section-title">
            📋 Dataset completo
        </div>
        <div class="github-topics-section-subtitle">
            Todas las métricas disponibles para análisis.
        </div>
    </div>""",
    unsafe_allow_html=True
)

display = df.copy()

# Renombrar columnas
display = display.rename(columns={
    "rank": "Rank",
    "topic": "Topic",
    "repo_count": "Repos",
    "total_stars": "Stars",
    "avg_stars": "Stars avg",
    "total_forks": "Forks",
    "avg_forks": "Forks avg",
    "languages": "Lenguajes",
    "recent_repo_count": "Repos nuevos",
    "active_repo_count": "Repos activos"
})

# Formatear números grandes
display["Repos"] = display["Repos"].apply(lambda x: f"{x:,.0f}")
display["Stars"] = display["Stars"].apply(lambda x: f"{x:,.0f}")
display["Forks"] = display["Forks"].apply(lambda x: f"{x:,.0f}")

st.dataframe(
    display,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(format="%d"),
        "Stars avg": st.column_config.NumberColumn(format="%.0f"),
        "Forks avg": st.column_config.NumberColumn(format="%.0f"),
    }
)