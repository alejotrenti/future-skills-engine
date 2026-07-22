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
# QUERY
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
    """<div class="github-topics-page">
        <div class="github-topics-hero">
            <span class="github-topics-badge">
                🏷️ DATOS DE GITHUB
            </span>
            <h1>¿Qué comunidades están activas en GitHub?</h1>
            <p>
            Los <b>Topics</b> son etiquetas que los desarrolladores asignan
            a sus repositorios para describir tecnologías, frameworks,
            lenguajes o áreas de conocimiento. Este ranking identifica 
            las comunidades más activas y populares dentro del ecosistema open source.
            </p>
        </div>
    </div>""",
    unsafe_allow_html=True,
)


# ==========================
# ¿QUÉ ES UN TOPIC?
# ==========================

st.markdown(
    """<div class="github-topics-panel">
        <div class="github-topics-section-title">
            📄 ¿Qué es un Topic en GitHub?
        </div>
        <div class="github-topics-section-subtitle">
            Un Topic es una etiqueta que los desarrolladores asignan a sus repositorios 
            para categorizarlos y hacerlos más descubribles. Los Topics permiten 
            agrupar repositorios por tecnología, lenguaje, framework o área de interés.
            <br><br>
            Por ejemplo, un repositorio sobre machine learning puede tener topics como 
            <b>"machine-learning"</b>, <b>"pytorch"</b> y <b>"python"</b>.
            </div>
    </div>""",
    unsafe_allow_html=True
)


# ==========================
# ¿CÓMO SE OBTUVO ESTE RANKING?
# ==========================

st.markdown(
    """<div class="github-topics-panel">
        <div class="github-topics-section-title">
            📊 ¿Cómo se construyó este análisis?
        </div>
        <div class="github-topics-section-subtitle">
            Cada Topic se analiza desde múltiples dimensiones para entender 
            su ecosistema y relevancia dentro de GitHub.
            <br><br>
            • 📦 <b>Tamaño del ecosistema</b> — Cantidad de repositorios<br>
            • ⭐ <b>Popularidad</b> — Total de estrellas acumuladas<br>
            • 🍴 <b>Comunidad</b> — Total de forks<br>
            • 🔄 <b>Mantenimiento</b> — Repositorios actualizados recientemente<br>
            • 🚀 <b>Adopción reciente</b> — Repositorios creados en el último año<br>
            • 🌐 <b>Diversidad</b> — Lenguajes utilizados en el ecosistema
            <br><br>
            Este dashboard responde a la pregunta: <br>
            <b style="color: #F5F7FB;">¿Qué comunidades están activas en GitHub?</b>
        </div>
    </div>""",
    unsafe_allow_html=True,
)


# ==========================
# KPIs
# ==========================

total_topics = len(df)
max_stars_topic = df.loc[df["total_stars"].idxmax(), "topic"]
total_repos = df["repo_count"].sum()
total_stars_m = df["total_stars"].sum() / 1_000_000
total_forks_m = df["total_forks"].sum() / 1_000_000

metrics = [
    ("🏷️", "Topics analizados", total_topics),
    ("⭐", "Topic con más estrellas", max_stars_topic),
    ("📦", "Repositorios totales", f'{total_repos:,.0f}'),
    ("🌟", "Estrellas totales", f'{total_stars_m:.1f}M')
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


df_top = df.head(top_n).sort_values(
    "total_stars",
    ascending=False
)


# ==========================
# GRÁFICO 1: TOPICS MÁS POPULARES
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

# Gradiente de colores naranja
def get_orange_color(stars):
    max_stars = df_top["total_stars"].max()
    if stars >= max_stars * 0.7:
        return "#EA580C"  # Naranja fuerte
    elif stars >= max_stars * 0.4:
        return "#F97316"  # Naranja medio
    elif stars >= max_stars * 0.2:
        return "#FB923C"  # Naranja claro
    else:
        return "#FDBA74"  # Naranja muy claro

colors = [get_orange_color(stars) for stars in df_top["total_stars"]]

fig_popular = px.bar(
    df_top,
    x="total_stars",
    y="topic",
    orientation="h",
    text="total_stars",
)

fig_popular.update_traces(
    marker_color=colors,
    texttemplate="%{text:,.0f}",
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>" +
                  "Rank: %{customdata[0]}<br>" +
                  "Stars: %{x:,.0f}<br>" +
                  "Repos: %{customdata[1]:,.0f}<br>" +
                  "Forks: %{customdata[2]:,.0f}<br>" +
                  "Lenguajes: %{customdata[3]}<extra></extra>",
    customdata=df_top[
        [
            "rank",
            "repo_count",
            "total_forks",
            "languages"
        ]
    ]
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
    )
)

st.plotly_chart(fig_popular, use_container_width=True)


# ==========================
# GRÁFICO 2: BUBBLE CHART
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
    color_continuous_scale="Oranges",
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
                  "Rank: %{customdata[0]}<br>" +
                  "Repos: %{x:,.0f}<br>" +
                  "Stars: %{y:,.0f}<br>" +
                  "Forks: %{marker.size:,.0f}<br>" +
                  "Activos: %{marker.color:,.0f}<extra></extra>",
    customdata=df_top[["rank"]]
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
# GRÁFICO 4: TOPICS DE ALTO CRECIMIENTO
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
    colors_growth = [get_orange_color(repos) for repos in growth_df["recent_repo_count"]]
    
    fig_growth = px.bar(
        growth_df,
        x="recent_percentage",
        y="topic",
        orientation="h",
        text="recent_percentage",
    )
    
    fig_growth.update_traces(
        marker_color=colors_growth,
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>" +
                      "Repos recientes: %{x:.1f}%<br>" +
                      "Nuevos repos: %{customdata[0]:,.0f}<br>" +
                      "Rank: %{customdata[1]}<extra></extra>",
        customdata=growth_df[
            [
                "recent_repo_count",
                "rank"
            ]
        ]
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
        )
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
else:
    st.info("No se encontraron Topics con crecimiento significativo (mínimo 200 repositorios).")


# ==========================
# EXPLORAR UN TOPIC
# ==========================

st.write("")

st.markdown(
    """<div class="github-topics-panel github-topics-chart-panel">
        <div class="github-topics-section-title">
            🔍 Detalle del Topic
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

# Construir interpretación
rank = int(topic_data["rank"])

if rank == 1:
    liderazgo = "lidera el ranking"
elif rank <= 3:
    liderazgo = f"ocupa el puesto #{rank} del ranking"
else:
    liderazgo = f"se encuentra en la posición #{rank} del ranking"

if topic_data["total_stars"] > 100000:
    popularidad = "con una popularidad excepcional"
elif topic_data["total_stars"] > 50000:
    popularidad = "con una alta popularidad"
elif topic_data["total_stars"] > 10000:
    popularidad = "con popularidad significativa"
else:
    popularidad = "con popularidad moderada"

st.markdown(
    f"""<div style="padding:12px 0;color:#94A3B8;line-height:1.8;">
        <b style="color:#F5F7FB;">{selected_topic}</b> {liderazgo} {popularidad} dentro del ecosistema GitHub. 
        Su comunidad cuenta con {topic_data['repo_count']:,.0f} repositorios distribuidos en 
        {topic_data['languages']} lenguajes diferentes, lo que demuestra su diversidad y adopción.
        <br><br>
        <b style="color:#F5F7FB;">Ranking global:</b> #{rank}<br>
        <b style="color:#F5F7FB;">Repositorios:</b> {topic_data['repo_count']:,.0f}<br>
        <b style="color:#F5F7FB;">Estrellas totales:</b> {topic_data['total_stars']:,.0f} ({topic_data['avg_stars']:,.0f} promedio)<br>
        <b style="color:#F5F7FB;">Forks totales:</b> {topic_data['total_forks']:,.0f} ({topic_data['avg_forks']:,.0f} promedio)<br>
        <b style="color:#F5F7FB;">Lenguajes:</b> {topic_data['languages']}<br>
        <b style="color:#F5F7FB;">Repos activos:</b> {topic_data['active_repo_count']:,.0f}<br>
        <b style="color:#F5F7FB;">Repos nuevos (1 año):</b> {topic_data['recent_repo_count']:,.0f}
    </div>""",
    unsafe_allow_html=True
)

# ==========================
# TABLA DETALLADA
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
    "languages": "Languages",
    "recent_repo_count": "New repos",
    "active_repo_count": "Active repos"
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