import streamlit as st

st.set_page_config(
    page_title="Future Skills Engine",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Future Skills Engine")

st.markdown(
    """
## Bienvenido

Future Skills Engine es una plataforma de análisis de habilidades tecnológicas
construida sobre una arquitectura ETL siguiendo el patrón Medallion.

Actualmente el pipeline procesa datos de Stack Overflow Jobs para identificar
las habilidades más demandadas del mercado.

### Arquitectura

```

CSV
↓
Bronze
↓
Silver
↓
Gold
↓
Dashboard

```

Utilizá el menú lateral para navegar entre las distintas visualizaciones.
"""
)
