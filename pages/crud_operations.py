"""
pages/crud_operations.py
Full Create, Read, Update, Delete operations on player records
through a form-based UI, with basic validation and error handling.
"""
import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_connection import run_query, execute

st.set_page_config(page_title="CRUD Operations | Cricbuzz LiveStats", page_icon="⚙️", layout="wide")
st.title("⚙️ CRUD Operations — Player Records")

tab_create, tab_read, tab_update, tab_delete = st.tabs(["➕ Create", "📖 Read", "✏️ Update", "🗑 Delete"])

ROLES = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]

# ---------------- CREATE ----------------
with tab_create:
    st.subheader("Add New Player")
    with st.form("create_player_form", clear_on_submit=True):
        full_name = st.text_input("Full Name *")
        country = st.text_input("Country *")
        role = st.selectbox("Playing Role *", ROLES)
        batting_style = st.text_input("Batting Style")
        bowling_style = st.text_input("Bowling Style")
        dob = st.date_input("Date of Birth", value=None)
        submitted = st.form_submit_button("Add Player")

        if submitted:
            if not full_name.strip() or not country.strip():
                st.error("Full Name and Country are required fields.")
            else:
                try:
                    execute(
                        """INSERT INTO players
                           (full_name, country, playing_role, batting_style, bowling_style, date_of_birth)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (full_name.strip(), country.strip(), role,
                         batting_style.strip() or None, bowling_style.strip() or None,
                         str(dob) if dob else None)
                    )
                    st.success(f"Player '{full_name}' added successfully.")
                except Exception as e:
                    st.error(f"Failed to add player: {e}")

# ---------------- READ ----------------
with tab_read:
    st.subheader("All Players")
    search = st.text_input("Search by name or country")
    try:
        if search:
            df = run_query(
                "SELECT * FROM players WHERE full_name LIKE ? OR country LIKE ?",
                (f"%{search}%", f"%{search}%")
            )
        else:
            df = run_query("SELECT * FROM players ORDER BY player_id DESC")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to fetch players: {e}")

# ---------------- UPDATE ----------------
with tab_update:
    st.subheader("Update Player")
    try:
        players_df = run_query("SELECT player_id, full_name FROM players ORDER BY full_name")
        if players_df.empty:
            st.info("No players found. Add one in the Create tab first.")
        else:
            options = dict(zip(players_df["full_name"], players_df["player_id"]))
            selected_name = st.selectbox("Select player to update", options.keys())
            pid = options[selected_name]
            current = run_query("SELECT * FROM players WHERE player_id = ?", (pid,)).iloc[0]

            with st.form("update_player_form"):
                new_name = st.text_input("Full Name", value=current["full_name"])
                new_country = st.text_input("Country", value=current["country"])
                new_role = st.selectbox("Playing Role", ROLES,
                                         index=ROLES.index(current["playing_role"]) if current["playing_role"] in ROLES else 0)
                new_batting = st.text_input("Batting Style", value=current["batting_style"] or "")
                new_bowling = st.text_input("Bowling Style", value=current["bowling_style"] or "")
                update_submitted = st.form_submit_button("Update Player")

                if update_submitted:
                    if not new_name.strip() or not new_country.strip():
                        st.error("Full Name and Country cannot be empty.")
                    else:
                        try:
                            execute(
                                """UPDATE players SET full_name=?, country=?, playing_role=?,
                                   batting_style=?, bowling_style=? WHERE player_id=?""",
                                (new_name.strip(), new_country.strip(), new_role,
                                 new_batting.strip() or None, new_bowling.strip() or None, pid)
                            )
                            st.success("Player updated successfully.")
                        except Exception as e:
                            st.error(f"Update failed: {e}")
    except Exception as e:
        st.error(f"Failed to load players: {e}")

# ---------------- DELETE ----------------
with tab_delete:
    st.subheader("Delete Player")
    try:
        players_df = run_query("SELECT player_id, full_name FROM players ORDER BY full_name")
        if players_df.empty:
            st.info("No players found.")
        else:
            options = dict(zip(players_df["full_name"], players_df["player_id"]))
            selected_name = st.selectbox("Select player to delete", options.keys(), key="delete_select")
            pid = options[selected_name]

            st.warning(f"This will permanently delete **{selected_name}** and cannot be undone.")
            confirm = st.checkbox("I understand this action is permanent.")
            if st.button("Delete Player", type="primary", disabled=not confirm):
                try:
                    execute("DELETE FROM players WHERE player_id = ?", (pid,))
                    st.success(f"Player '{selected_name}' deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Delete failed: {e}")
    except Exception as e:
        st.error(f"Failed to load players: {e}")
