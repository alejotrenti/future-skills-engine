import pandas as pd
import streamlit as st
import plotly.express as px

from db import engine

st.set_page_config(
    page_title="Skill Trends",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Skill Trends")
st.caption("Most demanded technologies extracted from Stack Overflow.")

query = """
SELECT
    rank,
    skill,
    category,
    users_count
FROM gold.skill_trends
ORDER BY rank;
"""

df = pd.read_sql(query, engine)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Unique Skills",
    len(df)
)

col2.metric(
    "Categories",
    df["category"].nunique()
)

col3.metric(
    "Top Skill",
    df.iloc[0]["skill"]
)

top20 = df.head(20)

fig = px.bar(
    top20,
    x="users_count",
    y="skill",
    orientation="h",
    color="category",
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.metric(
    "Unique Skills",
    len(df)
)

st.dataframe(
    df,
    use_container_width=True,
)