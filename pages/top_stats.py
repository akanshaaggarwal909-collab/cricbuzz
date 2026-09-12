"""
pages/top_stats.py
Shows top batting/bowling stats fetched via the Cricbuzz API.
"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import get_top_stats, CricbuzzAPIError

st.set_page_config(page_title="Top Player Stats | Cricbuzz LiveStats", page_icon="📊", layout="wide")
st.title("📊 Top Player Stats")

stat_type = st.selectbox(
    "Choose a stat category",
    ["mostRuns", "mostWickets", "highestScore", "bestBowling"]
)

try:
    data = get_top_stats(stat_type)
    rows = data.get("headers", []), data.get("values", [])
    if rows[1]:
        df = pd.DataFrame([v.get("values", []) for v in rows[1]], columns=rows[0])
        st.dataframe(df, use_container_width=True)
        if "Runs" in df.columns or "Wkts" in df.columns:
            numeric_col = "Runs" if "Runs" in df.columns else "Wkts"
            st.bar_chart(df.set_index(df.columns[1])[numeric_col].astype(float).head(10))
    else:
        st.warning("No data returned for this category.")
except CricbuzzAPIError as e:
    st.error(f"Could not fetch stats: {e}")
