"""
Skill Growth Dashboard
¿Qué habilidades están creciendo más rápido en la comunidad de desarrolladores?
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
    page_title="Skill Growth",
    page_icon="📈",
    layout="wide",
)

load_css_bundle("styles.css", "skill_growth.css")

# ==========================
# QUERY
# ==========================

query = """
SELECT
    rank,
    skill,
    category,
    have_worked,
    want_to_work,
    growth_score
FROM gold.skill_growth
ORDER BY rank;
"""

with st.spinner("Cargando Skill Growth..."):
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
    <div class="skill-growth-page">
        <div class="skill-growth-hero">
            <span class="skill-growth-badge">
                📈 DATOS DE STACK OVERFLOW
            </span>
            <h1>¿Qué habilidades están creciendo más rápido?</h1>
            <p>Explorá las tecnologías que están ganando relevancia
            y descubrí cuáles son las habilidades con mayor crecimiento
            dentro de la comunidad de desarrolladores.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================
# ¿QUÉ ES STACK OVERFLOW?
# ==========================

st.markdown(
    """<div class="skill-growth-panel">
        <div class="skill-growth-section-title">
            📄 ¿Qué es Stack Overflow?
        </div>
        <div class="skill-growth-section-subtitle">
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
    """<div class="skill-growth-panel">
        <div class="skill-growth-section-title">
            📊 ¿Cómo se obtuvo este ranking?
        </div>
        <div class="skill-growth-section-subtitle" style="line-height:1.8;">
            El <b>Growth Score</b> se calcula comparando la cantidad de desarrolladores
            que <b>ya utilizan</b> una tecnología (<i>Have Worked</i>) con aquellos que
            <b>desean aprenderla</b> (<i>Want to Work</i>).
            <br><br>
            Este indicador estima el <b>potencial de crecimiento</b> de cada habilidad.
            Además, se aplica un ajuste logarítmico para evitar que las tecnologías más
            populares dominen el ranking únicamente por su tamaño.
        </div>
    </div>""",
    unsafe_allow_html=True,
)
# ==========================
# KPIs
# ==========================

total_skills = len(df)
top_skill = df.sort_values("growth_score", ascending=False).iloc[0]["skill"]
avg_growth_score = df["growth_score"].mean()
total_worked = df["have_worked"].sum()

metrics = [
    ("📚", "Skills analizadas", total_skills),
    ("🏆", "Líder en crecimiento", top_skill),
    ("📊", "Growth Score promedio", f"{avg_growth_score:.2f}"),
    ("👨‍💻", "Desarrolladores encuestados", f"{total_worked:,.0f}")
]

cols = st.columns(4)

for col, (icon, title, value) in zip(cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="skill-growth-metric-card">
                <div class="skill-growth-metric-icon">
                    {icon}
                </div>
                <div class="skill-growth-metric-body">
                    <p>{title}</p>
                    <h2>{value}</h2>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

# ==========================
# CONTROLES
# ==========================

left, right = st.columns([4, 1], gap="medium")

with left:
    st.markdown(
        """
        <div class="skill-growth-panel">
            <div>
                <div class="skill-growth-section-title">
                    📊 Ranking de crecimiento
                </div>
                <div class="skill-growth-section-subtitle">
                    Tecnologías con mayor impulso en la comunidad.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:
    top_n = st.select_slider(
        "Mostrar top",
        options=[10, 15, 20, 30, 40, 50],
        value=20
    )

growth_df = df.sort_values("growth_score", ascending=False).head(top_n)

# ==========================
# GRÁFICO 1: RANKING
# ==========================

st.write("")

st.markdown(
    """
    <div class="skill-growth-panel skill-growth-chart-panel">
        <div class="skill-growth-section-title">
            🏆 Ranking de crecimiento
        </div>
        <div class="skill-growth-section-subtitle">
            Habilidades ordenadas por su Growth Score.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Gradiente de colores verde-azul
def get_growth_color(score):
    max_score = growth_df["growth_score"].max()
    if score >= max_score * 0.7:
        return "#34D399"  # Verde fuerte
    elif score >= max_score * 0.4:
        return "#6EE7B7"  # Verde medio
    elif score >= max_score * 0.2:
        return "#6C7CFF"  # Azul
    else:
        return "#93C5FD"  # Azul claro

colors = [get_growth_color(score) for score in growth_df["growth_score"]]

fig = px.bar(
    growth_df,
    x="growth_score",
    y="skill",
    orientation="h",
    text="growth_score",
)

fig.update_traces(
    marker_color=colors,
    texttemplate="%{text:.2f}",
    textposition="outside",
    hovertemplate=
    "<b>%{y}</b><br>"
    "Growth Score: %{x:.2f}<br>"
    "Rank: %{customdata[0]}<br>"
    "Usuarios actuales: %{customdata[1]:,.0f}<br>"
    "Interesados: %{customdata[2]:,.0f}<br>"
    "Categoría: %{customdata[3]}<extra></extra>",
    customdata=growth_df[
        [
            "rank",
            "have_worked",
            "want_to_work",
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
    xaxis_title="Growth Score",
    yaxis_title=None,
    font=dict(
        family="Space Grotesk, sans-serif",
        color="#F5F7FB"
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        autorange="reversed"
    )
)

st.plotly_chart(fig, use_container_width=True)


# ==========================
# INSIGHT PRINCIPAL
# ==========================

st.markdown(
    """<div class="skill-growth-panel" style="margin-top: 0.5rem;">
        <div class="skill-growth-section-title">
            🏆 Skill destacada
        </div>
    </div>""",
    unsafe_allow_html=True
)

# Construir interpretación para la tecnología líder
top_skill_data = df.sort_values("growth_score", ascending=False).iloc[0]
rank = int(top_skill_data["rank"])

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.08), rgba(108, 124, 255, 0.05));
        border: 1px solid rgba(52, 211, 153, 0.15);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin: 0.5rem 0 1rem 0;
    ">
        <div style="display: flex; align-items: flex-start; gap: 1.5rem;">
            <div style="flex: 0 0 auto;">
                <div style="
                    font-size: 2.5rem;
                    width: 4rem;
                    height: 4rem;
                    display: grid;
                    place-items: center;
                    background: rgba(52, 211, 153, 0.12);
                    border-radius: 14px;
                ">
                    🏆
                </div>
            </div>
            <div style="flex: 1;">
                <div style="
                    font-size: 1.4rem;
                    font-weight: 700;
                    color: #F5F7FB;
                    margin-bottom: 0.3rem;
                ">
                    {top_skill_data['skill']}
                </div>
                <div style="
                    display: flex;
                    gap: 1.5rem;
                    flex-wrap: wrap;
                    margin-bottom: 0.5rem;
                ">
                    <div>
                        <span style="color: rgba(245,247,251,0.5); font-size: 0.8rem;">Growth Score</span>
                        <div style="color: #6EE7B7; font-size: 1.1rem; font-weight: 600;">{top_skill_data['growth_score']:.2f}</div>
                    </div>
                    <div>
                        <span style="color: rgba(245,247,251,0.5); font-size: 0.8rem;">Ranking</span>
                        <div style="color: #F5F7FB; font-size: 1.1rem; font-weight: 600;">#{rank}</div>
                    </div>
                    <div>
                        <span style="color: rgba(245,247,251,0.5); font-size: 0.8rem;">Usuarios actuales</span>
                        <div style="color: #F5F7FB; font-size: 1.1rem; font-weight: 600;">{top_skill_data['have_worked']:,.0f}</div>
                    </div>
                    <div>
                        <span style="color: rgba(245,247,251,0.5); font-size: 0.8rem;">Interesados</span>
                        <div style="color: #F5F7FB; font-size: 1.1rem; font-weight: 600;">{top_skill_data['want_to_work']:,.0f}</div>
                    </div>
                </div>
                <div style="color: rgba(245,247,251,0.7); font-size: 0.95rem; line-height: 1.6;">
                    Presenta un <b style="color: #6EE7B7;">Growth Score de {top_skill_data['growth_score']:.2f}</b>, 
                    con {top_skill_data['have_worked']:,.0f} desarrolladores que ya la utilizan 
                    y más de {top_skill_data['want_to_work']:,.0f} interesados en aprenderla, 
                    lo que la posiciona como una de las tecnologías con mayor potencial de 
                    crecimiento según la encuesta de Stack Overflow.
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
    <div class="skill-growth-panel skill-growth-table-panel">
        <div class="skill-growth-section-title">
            📋 Ranking completo
        </div>
        <div class="skill-growth-section-subtitle">
            Detalle de todas las habilidades analizadas.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

display_df = df.rename(
    columns={
        "rank": "Rank",
        "skill": "Skill",
        "category": "Category",
        "have_worked": "Current users",
        "want_to_work": "Interested",
        "growth_score": "Growth Score"
    }
)

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Rank": st.column_config.NumberColumn(format="%d"),
        "Growth Score": st.column_config.NumberColumn(format="%.2f"),
    }
)
