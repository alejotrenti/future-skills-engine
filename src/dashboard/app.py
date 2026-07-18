"""
Future Skills Engine - Home
Plataforma de inteligencia tecnológica con múltiples fuentes de datos.
"""

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

# ============ MÉTRICAS ============
metrics = get_home_metrics()

# Métricas reales de GitHub (hardcodeadas temporalmente)
# En producción vendrían de una query a la DB
GITHUB_METRICS = {
    "repos": 80000,
    "stars": 43000000,
    "technologies": 230
}


# ============ HERO SECTION ============
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🚀 PLATAFORMA DE INTELIGENCIA TECNOLÓGICA</div>
    <h1 class="hero-title">
        Future Skills <span class="hero-highlight">Engine</span>
    </h1>
    <p class="hero-subtitle">
        Análisis tecnológico multi-fuente basado en Stack Overflow Survey, 
        GitHub API y próximamente arXiv para detectar tendencias, 
        crecimiento y adopción de tecnologías.
    </p>
    <div class="hero-cta">
        <button class="cta-primary">
            <a href="#fuentes" style="text-decoration: none; color: #FFF;">Explorar fuentes →</a>
        </button>
        <button class="cta-secondary">
            <a href="#arquitectura" style="text-decoration: none; color: #FFF;">Ver arquitectura</a>
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

# ============ CHIPS DE FUENTES ============
st.markdown("""
<div style="display: flex; justify-content: center; gap: 16px; margin: -10px 0 30px 0; flex-wrap: wrap;">
    <span style="
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 100px;
        padding: 6px 18px;
        font-size: 13px;
        font-weight: 500;
        color: #F5F7FB;
        letter-spacing: 0.3px;
    ">📄 Stack Overflow</span>
    <span style="
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 100px;
        padding: 6px 18px;
        font-size: 13px;
        font-weight: 500;
        color: #F5F7FB;
        letter-spacing: 0.3px;
    ">🐙 GitHub</span>
    <span style="
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 100px;
        padding: 6px 18px;
        font-size: 13px;
        font-weight: 400;
        color: rgba(255,255,255,0.3);
        letter-spacing: 0.3px;
    ">📚 arXiv <span style="font-size: 10px; opacity: 0.5;">(Próximamente)</span></span>
</div>
""", unsafe_allow_html=True)


# ============ METRICS ROW ============
st.markdown("""
<div style="margin-bottom: 8px; text-align: center; opacity: 0.6; font-size: 13px; letter-spacing: 0.5px;">
    DATOS AGREGADOS
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">👥</div>
        <div class="metric-value">{metrics["respondents"]:,}</div>
        <div class="metric-label">Desarrolladores</div>
        <div class="metric-trend">Stack Overflow 2025</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with col2:
    st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">🐙</div>
        <div class="metric-value">{GITHUB_METRICS['repos']:,}</div>
        <div class="metric-label">Repositorios</div>
        <div class="metric-trend">GitHub API</div>
    </div>
    """,
    unsafe_allow_html=True)

with col3:
    st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">⭐</div>
        <div class="metric-value">{GITHUB_METRICS['stars']/1_000_000:.1f}M</div>
        <div class="metric-label">Estrellas analizadas</div>
        <div class="metric-trend">GitHub API</div>
    </div>
    """,
    unsafe_allow_html=True)

with col4:
    st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">💻</div>
        <div class="metric-value">{metrics["categories"]}</div>
        <div class="metric-label">Tecnologías</div>
        <div class="metric-trend">Multi-fuente</div>
    </div>
    """,
    unsafe_allow_html=True)

with col5:
    st.markdown(
    f"""
    <div class="metric-card">
        <div class="metric-icon">🌍</div>
        <div class="metric-value">{metrics["countries"]}</div>
        <div class="metric-label">Países representados</div>
        <div class="metric-trend">Cobertura global</div>
    </div>
    """,
    unsafe_allow_html=True)


st.divider()


# ============ FEATURES GRID ============
st.markdown("""
<div class="section-header centered">
    <span class="section-badge">EXPLORÁ</span>
    <h2 class="section-title">Análisis disponibles</h2>
</div>
""", unsafe_allow_html=True)

# ============ STACK OVERFLOW SECTION ============
st.markdown("""
<div style="margin-top: 20px; margin-bottom: 16px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 24px;">📄</span>
        <h3 style="margin: 0; color: #F5F7FB; font-weight: 600;">Stack Overflow Survey</h3>
        <span style="
            background: rgba(255,255,255,0.06);
            border-radius: 100px;
            padding: 2px 14px;
            font-size: 12px;
            color: rgba(255,255,255,0.4);
        ">Encuesta anual de desarrolladores</span>
    </div>
</div>
""", unsafe_allow_html=True)

so_col1, so_col2 = st.columns(2)

with so_col1:
    st.markdown("""
    <a href="/Skill_Trends" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Skill Trends</h3>
            <p>Evolución temporal de las tecnologías más populares.</p>
            <div class="feature-tag">Tendencias</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with so_col2:
    st.markdown("""
    <a href="/Skill_Growth" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Skill Growth</h3>
            <p>Crecimiento y caída según encuesta de desarrolladores.</p>
            <div class="feature-tag">% Crecimiento</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# ============ GITHUB SECTION ============
st.markdown("""
<div style="margin-top: 48px; margin-bottom: 16px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 24px;">🐙</span>
        <h3 style="margin: 0; color: #F5F7FB; font-weight: 600;">GitHub API</h3>
        <span style="
            background: rgba(255,255,255,0.06);
            border-radius: 100px;
            padding: 2px 14px;
            font-size: 12px;
            color: rgba(255,255,255,0.4);
        ">Ecosistema open source</span>
    </div>
</div>
""", unsafe_allow_html=True)

gh_col1, gh_col2 = st.columns(2)

with gh_col1:
    st.markdown("""
    <a href="/github_momentum" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3>GitHub Momentum</h3>
            <p>Tecnologías con mayor actividad, popularidad y crecimiento en GitHub.</p>
            <div class="feature-tag">Momentum</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with gh_col2:
    st.markdown("""
    <a href="/github_topics" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="feature-icon">🏷️</div>
            <h3>GitHub Topics</h3>
            <p>Comunidades y temas emergentes a través de tópicos de repositorios.</p>
            <div class="feature-tag">Tópicos</div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# ============ ARXIV SECTION (Próximamente) ============
st.markdown("""
<div style="margin-top: 48px; margin-bottom: 16px; opacity: 0.4;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 24px;">📚</span>
        <h3 style="margin: 0; color: #F5F7FB; font-weight: 600;">arXiv</h3>
        <span style="
            background: rgba(255,255,255,0.04);
            border-radius: 100px;
            padding: 2px 14px;
            font-size: 12px;
            color: rgba(255,255,255,0.3);
        ">Próximamente</span>
    </div>
</div>
""", unsafe_allow_html=True)

arxiv_col1, arxiv_col2 = st.columns(2)

with arxiv_col1:
    st.markdown("""
    <div class="feature-card feature-card-disabled">
        <div class="feature-icon">🔬</div>
        <h3>Research Trends</h3>
        <p>Tendencias de investigación a partir de papers académicos.</p>
        <div class="feature-tag">Próximamente</div>
    </div>
    """, unsafe_allow_html=True)

with arxiv_col2:
    st.markdown("""
    <div class="feature-card feature-card-disabled">
        <div class="feature-icon">🧠</div>
        <h3>Emerging Topics</h3>
        <p>Identificación temprana de tecnologías emergentes en investigación.</p>
        <div class="feature-tag">Próximamente</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============ ARQUITECTURA ============
st.markdown("""
<div class="section-header centered" id="arquitectura">
    <span class="section-badge">ARQUITECTURA</span>
    <h2 class="section-title">Pipeline ETL</h2>
    <p class="section-desc" style="max-width: 600px; margin: 0 auto;">
        Patrón Medallion para procesamiento de datos multi-fuente.
    </p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    # Flowchart visual con CSS
    st.markdown("""
    <div class="flowchart">
        <div class="flow-step data">
            <div class="flow-icon">📄</div>
            <div class="flow-label">CSV/API</div>
            <div class="flow-desc">Stack Overflow · GitHub</div>
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
    <div class="vision-card">
        <div class="vision-item">
            <div class="vision-icon">📄</div>
            <div>
                <h4>Stack Overflow</h4>
                <p>Adopción por desarrolladores y tendencias de aprendizaje</p>
            </div>
        </div>
        <div class="vision-item">
            <div class="vision-icon">🐙</div>
            <div>
                <h4>GitHub</h4>
                <p>Actividad real, ecosistemas y comunidades open source</p>
            </div>
        </div>
        <div class="vision-item" style="opacity: 0.4;">
            <div class="vision-icon">📚</div>
            <div>
                <h4>arXiv</h4>
                <p>Investigación académica y tecnologías emergentes</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============ FOOTER ============
st.markdown("""
<div class="footer">
    <p>Future Skills Engine · Built with Streamlit · Datos actualizados desde Stack Overflow + GitHub + arXiv (próximamente)</p>
</div>
""", unsafe_allow_html=True)