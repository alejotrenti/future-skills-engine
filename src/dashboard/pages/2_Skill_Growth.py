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


df = pd.read_sql(query, engine)


with st.spinner("Cargando Skill Growth..."):
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
    <div class="skill-growth-page">
        <div class="skill-growth-hero">
            <span class="skill-growth-badge">
                🚀 CRECIMIENTO Y DECRECIMIENTO DE HABILIDADES TECH
            </span>
            <h1>Evolución de habilidades</h1>
            <p>Explorá las tecnologías que están ganando relevancia
            y descubrí cuáles son las habilidades con mayor crecimiento
            dentro de la comunidad.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """<div class="skill-growth-panel">
        <div class="skill-growth-section-title">
        ¿Cómo se calcula?
        </div>
        <div class="skill-growth-section-subtitle" style="line-height:1.8;">
            El <b>Growth Score</b> compara cuántos desarrolladores
            <b>ya utilizan</b> una tecnología (<i>HaveWorked</i>)
            con cuántos <b>quieren aprenderla</b> (<i>WantToWork</i>).
            Un ajuste logarítmico evita favorecer únicamente a las
            tecnologías más populares.
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# METRICS

metrics = [
    (
        "🚀",
        "Skills analizadas",
        len(df)
    ),

    (
        "🔥",
        "Mayor potencial",
        df.sort_values(
            "growth_score",
            ascending=False
        ).iloc[0]["skill"]
    ),

    (
        "📊",
        "Score promedio",
        f'{df["growth_score"].mean():.2f}'
    )
]


metric_cols = st.columns(3)


for col, (icon,title,value) in zip(metric_cols,metrics):

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



# CONTROL + HEADER

left,right = st.columns([4,1], gap="medium")


with left:

    st.markdown(
        """
        <div class="skill-growth-panel">
            <div>
                <div class="skill-growth-section-title">
                    Tecnologías con mayor impulso
                </div>
                <div class="skill-growth-section-subtitle">
                    Seleccioná cuántas habilidades querés comparar.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with right:

    top_n = st.select_slider(
        "Seleccioná:",
        options=[5,10,15,20,30,40,50],
        value=20
    )


growth_df = (
    df
    .sort_values(
        "growth_score",
        ascending=False
    )
    .head(top_n)
)


# CHART


fig = px.bar(
    growth_df,
    x="growth_score",
    y="skill",
    orientation="h",
    text="growth_score",
    color="category",
)


fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside",
    marker_line_color="rgba(255,255,255,0.10)",
    marker_line_width=1,
)


fig.update_layout(

    height=560,

    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",

    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),

    xaxis_title="Crecimiento (%)",

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



st.markdown(
    """
    <div class="skill-growth-panel skill-growth-chart-panel">
        <div class="skill-growth-section-title">
            Ranking de crecimiento
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



st.plotly_chart(
    fig,
    use_container_width=True
)



st.write("")



# TABLE


st.markdown(
    """
    <div class="skill-growth-panel skill-growth-table-panel">
        <div class="skill-growth-section-title">
            Detalle de evolución
        </div>
        <div class="skill-growth-section-subtitle">
            Comparación del crecimiento relativo de cada habilidad.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



display_df = df.rename(
    columns={
        "rank":"Ranking",
        "skill":"Habilidad",
        "category":"Categoría",
        "have_worked":"Usuarios actuales",
        "want_to_work":"Interesados",
        "growth_score":"Future Demand Score"
    }
)


st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True
)