"""
app.py
Main entry point for the Cricbuzz LiveStats Streamlit application.
Run with: streamlit run app.py
"""
import streamlit as st
from config import APP_TITLE

st.set_page_config(page_title=APP_TITLE, page_icon="🏏", layout="wide")

st.title("🏏 Cricbuzz LiveStats")
st.subheader("Real-Time Cricket Insights & SQL-Based Analytics")

st.markdown(
    """
    Welcome! Use the sidebar to navigate between pages:

    - **Home** — project overview & setup instructions
    - **Live Matches** — live scores from the Cricbuzz API
    - **Top Player Stats** — top batting/bowling stats
    - **SQL Queries & Analytics** — 25 analytical SQL queries
    - **CRUD Operations** — add / edit / delete player & match records

    > This is the landing page. Streamlit auto-detects pages placed in the
    > `pages/` folder and lists them in the sidebar.
    """
)

st.info("First time running the app? Go to **Home** for setup instructions, "
        "or run `python utils/db_connection.py` equivalent setup to initialize the database.")
