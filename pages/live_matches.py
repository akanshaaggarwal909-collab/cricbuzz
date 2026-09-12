"""
pages/live_matches.py
Displays live match data from the Cricbuzz API.
"""
import streamlit as st
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.api_client import get_live_matches, get_match_scorecard, CricbuzzAPIError

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="⚡", layout="wide")
st.title("⚡ Live Matches")

if st.button("🔄 Refresh"):
    st.rerun()

try:
    data = get_live_matches()

    # NOTE: Actual JSON shape depends on the Cricbuzz API plan/endpoint used.
    # The parsing below assumes a typeMatches -> seriesMatches -> matches structure,
    # adjust field paths to match your live response.
    type_matches = data.get("typeMatches", [])

    if not type_matches:
        st.warning("No live matches right now. Showing sample layout below.")

    for type_match in type_matches:
        st.subheader(type_match.get("matchType", "Matches"))
        for series in type_match.get("seriesMatches", []):
            series_info = series.get("seriesAdWrapper", {})
            for match in series_info.get("matches", []):
                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{info.get('matchDesc', 'Match')}** — "
                                f"{info.get('team1', {}).get('teamName', '')} vs "
                                f"{info.get('team2', {}).get('teamName', '')}")
                    st.caption(info.get("venueInfo", {}).get("ground", ""))
                with col2:
                    if st.button("View Scorecard", key=info.get("matchId")):
                        card = get_match_scorecard(info.get("matchId"))
                        st.json(card)
                st.divider()

except CricbuzzAPIError as e:
    st.error(f"Could not fetch live matches: {e}")
    st.info("Showing a sample layout so the page remains usable offline:")
    sample = pd.DataFrame([
        {"Match": "IND vs AUS, 3rd ODI", "Team1": "IND 210/3", "Team2": "AUS 207 & 250", "Status": "IND won"},
    ])
    st.dataframe(sample, use_container_width=True)
