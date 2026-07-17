import streamlit as st
from pathlib import Path
from db import get_home_metrics

try:
    from theme import load_css
except Exception:
    def load_css(css_file: str = "app.css") -> None:
        """Fallback loader for app.css when the theme module cannot be imported."""
        base_dir = Path(__file__).resolve().parent
        css_path = base_dir / ".streamlit" / css_file

        if not css_path.exists():
            return

        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Future Skills Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar el estilo visual principal del dashboard
load_css("app.css")

metrics = get_home_metrics()

# ============ HERO SECTION ============
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🚀 Plataforma de inteligencia tecnológica
</div>
    <h1 class="hero-title">
        Future Skills <span class="hero-highlight">Engine</span>
    </h1>
    <p class="hero-subtitle">
        Detectá las tecnologías que están definiendo el futuro del desarrollo de software.
    </p>
    <div class="hero-cta">
        <button class="cta-primary">
            <a href="#explorar" style="text-decoration: none; color: #FFF;">Explorar dashboard →</a>
        </button>
        <button class="cta-secondary">
            <a href="#arquitectura" style="text-decoration: none; color: #FFF;">Ver arquitectura</a>
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ METRICS ROW ============
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">👥</div>
        <div class="metric-value">{metrics["respondents"]:,}</div>
        <div class="metric-label">Encuestados</div>
        <div class="metric-trend">Stack Overflow Survey 2025</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-icon">📦</div>
        <div class="metric-value">80.000</div>
        <div class="metric-label">Repositorios</div>
        <div class="metric-trend">CAMBIAR A DATOS REALES</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📈</div>
        <div class="metric-value">{metrics["categories"]}</div>
        <div class="metric-label">Categorías</div>
        <div class="metric-trend" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Lenguajes • Frameworks • Bases de datos...</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🌍</div>
        <div class="metric-value">{metrics["countries"]}</div>
        <div class="metric-label">Países representados</div>
        <div class="metric-trend">Global coverage</div>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# ============ FEATURES GRID ============
st.markdown("""
<div class="section-header centered">
    <span class="section-badge">EXPLORÁ</span>
    <h2 class="section-title">Análisis disponibles</h2>
</div>
""", unsafe_allow_html=True)

feat_col1, feat_col2, feat_col3 = st.columns(3)

with feat_col1:

    st.markdown(f"""
    <div class="feature-card" >
        <a href="/Skill_Trends" target="_self" style="text-decoration: none; color: inherit;" target="_blank">
            <div class="feature-icon">📊</div>
            <h3>Skill Trends</h3>
            <p>Evolución temporal de las tecnologías más populares.</p>
            <div class="feature-tag">Tendencias</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <a href="/Skill_Growth" target="_self" style="text-decoration: none; color: inherit;"  class="feature-card feature-card-link">
        <div class="feature-icon">📈</div>
        <h3>Habilidades en crecimiento</h3>
        <p>Crecimiento y caída según encuesta de desarrolladores</p>
        <div class="feature-tag">% Crecimiento</div>
    </a>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class="feature-card feature-card-disabled">
        <div class="feature-icon">🐙</div>
        <h3>GitHub Skills</h3>
        <p>Próximamente: descubrí las tecnologías con mayor actividad, crecimiento y adopción a partir de repositorios de GitHub.</p>
        <div class="feature-tag">Próximamente</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============ TWO COLUMN LAYOUT ============
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">CÓMO FUNCIONA</span>
        <h2 class="section-title">Arquitectura de datos</h2>
        <p class="section-desc">Pipeline ETL basado en el patrón Medallion</p>
    </div>
    """, unsafe_allow_html=True)

    # Flowchart visual con CSS
    st.markdown("""
    <div class="flowchart">
        <div class="flow-step data">
            <div class="flow-icon">📄</div>
            <div class="flow-label">CSV/API</div>
            <div class="flow-desc"> </div>
            <div class="flow-arrow">⬇</div>
        </div>
        <div class="flow-step bronze">
            <div class="flow-icon">🟤</div>
            <div class="flow-label">Bronze</div>
            <div class="flow-desc">Raw data</div>
            <div class="flow-arrow">⬇</div>
        </div>
        <div class="flow-step silver">
            <div class="flow-icon">⚪</div>
            <div class="flow-label">Silver</div>
            <div class="flow-desc">Cleaned</div>
            <div class="flow-arrow">⬇</div>
        </div>
        <div class="flow-step gold">
            <div class="flow-icon">🟡</div>
            <div class="flow-label">Gold</div>
            <div class="flow-desc">Curated</div>
            <div class="flow-arrow">⬇</div>
        </div>
        <div class="flow-step dashboard">
            <div class="flow-icon">📊</div>
            <div class="flow-label">Dashboard</div>
            <div class="flow-desc">Insights</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">OBJETIVO</span>
        <h2 class="section-title">Visión estratégica</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="vision-card">
        <div class="vision-item">
            <div class="vision-icon">🎯</div>
            <div>
                <h4>Análisis de demanda</h4>
                <p>Identificá las habilidades tecnológicas más buscadas en el mercado actual</p>
            </div>
        </div>
        <div class="vision-item">
            <div class="vision-icon">🔮</div>
            <div>
                <h4>Detección temprana</h4>
                <p>Descubrí tecnologías emergentes antes de que se conviertan en mainstream</p>
            </div>
        </div>
        <div class="vision-item">
            <div class="vision-icon">📈</div>
            <div>
                <h4>Decisiones basadas en datos</h4>
                <p>Tomá decisiones estratégicas con información verificada y actualizada</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# st.divider()

# # ============ QUICK START / CTA ============
# st.markdown("""
# <div class="cta-section">
#     <div class="cta-content">
#         <h2>¿Listo para explorar?</h2>
#         <p>Navegá por el menú lateral para acceder a todos los análisis</p>
#         <div style="margin-top: 20px;">
#             <a href="#explorar" class="cta-primary">Comenzar análisis →</a>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown("""
<div class="footer">
    <p>Future Skills Engine · Built with Streamlit · Datos actualizados desde Stack Overflow-Github-arXiv</p>
</div>
""", unsafe_allow_html=True)