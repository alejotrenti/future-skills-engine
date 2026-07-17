from sqlalchemy import create_engine
import os
import pandas as pd
import streamlit as st

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

@st.cache_data

def get_home_metrics():
    query = """
    SELECT
        (SELECT COUNT(*) FROM silver.respondents) AS respondents,
        (SELECT COUNT(DISTINCT skill) FROM silver.skills) AS skills,
        (SELECT COUNT(DISTINCT category) FROM silver.skills) AS categories,
        (SELECT COUNT(DISTINCT country) FROM silver.respondents) AS countries;
    """

    return pd.read_sql(query, engine).iloc[0]