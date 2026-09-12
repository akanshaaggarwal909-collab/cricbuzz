"""
pages/sql_queries.py
SQL query interface exposing the 25 analytics queries plus a free-form
custom query box.
"""
import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.db_connection import run_query

st.set_page_config(page_title="SQL Analytics | Cricbuzz LiveStats", page_icon="🧮", layout="wide")
st.title("🧮 SQL Queries & Analytics")

QUESTIONS = {
    "Q1 - Indian players": "SELECT full_name, playing_role, batting_style, bowling_style FROM players WHERE country = 'India';",
    "Q2 - Matches in last 30 days": "SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2, v.venue_name, v.city, m.match_date FROM matches m JOIN teams t1 ON m.team1_id=t1.team_id JOIN teams t2 ON m.team2_id=t2.team_id JOIN venues v ON m.venue_id=v.venue_id WHERE m.match_date >= DATE('now','-30 day') ORDER BY m.match_date DESC;",
    "Q3 - Top 10 ODI run scorers": "SELECT p.full_name, SUM(b.runs_scored) AS total_runs, ROUND(AVG(b.runs_scored),2) AS batting_average, SUM(CASE WHEN b.runs_scored>=100 THEN 1 ELSE 0 END) AS centuries FROM batting_performance b JOIN players p ON b.player_id=p.player_id JOIN matches m ON b.match_id=m.match_id WHERE m.match_format='ODI' GROUP BY p.player_id ORDER BY total_runs DESC LIMIT 10;",
    "Q4 - Venues capacity > 50,000": "SELECT venue_name, city, country, capacity FROM venues WHERE capacity > 50000 ORDER BY capacity DESC;",
    "Q5 - Total wins per team": "SELECT t.team_name, COUNT(*) AS total_wins FROM matches m JOIN teams t ON m.winner_id=t.team_id GROUP BY t.team_name ORDER BY total_wins DESC;",
    "Q6 - Player count by role": "SELECT playing_role, COUNT(*) AS player_count FROM players GROUP BY playing_role;",
    "Q7 - Highest score per format": "SELECT m.match_format, MAX(b.runs_scored) AS highest_score FROM batting_performance b JOIN matches m ON b.match_id=m.match_id GROUP BY m.match_format;",
    "Q8 - Series started in 2024": "SELECT series_name, host_country, match_type, start_date, total_matches FROM series WHERE strftime('%Y', start_date) = '2024';",
    "Q9 - All-rounders >1000 runs & >50 wkts": "SELECT p.full_name, SUM(b.runs_scored) AS total_runs, SUM(bo.wickets_taken) AS total_wickets, m.match_format FROM players p JOIN batting_performance b ON p.player_id=b.player_id JOIN bowling_performance bo ON p.player_id=bo.player_id AND b.match_id=bo.match_id JOIN matches m ON b.match_id=m.match_id WHERE p.playing_role='All-rounder' GROUP BY p.player_id, m.match_format HAVING SUM(b.runs_scored)>1000 AND SUM(bo.wickets_taken)>50;",
    "Q10 - Last 20 completed matches": "SELECT m.match_desc, t1.team_name AS team1, t2.team_name AS team2, tw.team_name AS winner, m.victory_margin, m.victory_type, v.venue_name FROM matches m JOIN teams t1 ON m.team1_id=t1.team_id JOIN teams t2 ON m.team2_id=t2.team_id JOIN teams tw ON m.winner_id=tw.team_id JOIN venues v ON m.venue_id=v.venue_id ORDER BY m.match_date DESC LIMIT 20;",
    "Q11 - Cross-format performance": "SELECT p.full_name, SUM(CASE WHEN m.match_format='Test' THEN b.runs_scored ELSE 0 END) AS test_runs, SUM(CASE WHEN m.match_format='ODI' THEN b.runs_scored ELSE 0 END) AS odi_runs, SUM(CASE WHEN m.match_format='T20I' THEN b.runs_scored ELSE 0 END) AS t20i_runs, ROUND(AVG(b.runs_scored),2) AS overall_batting_avg FROM players p JOIN batting_performance b ON p.player_id=b.player_id JOIN matches m ON b.match_id=m.match_id GROUP BY p.player_id HAVING COUNT(DISTINCT m.match_format) >= 2;",
    "Q12 - Home vs away wins": "SELECT t.team_name, SUM(CASE WHEN v.country=t.country AND m.winner_id=t.team_id THEN 1 ELSE 0 END) AS home_wins, SUM(CASE WHEN v.country!=t.country AND m.winner_id=t.team_id THEN 1 ELSE 0 END) AS away_wins FROM matches m JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id) JOIN venues v ON m.venue_id=v.venue_id GROUP BY t.team_id;",
    "Q13 - Partnerships >= 100 runs": "SELECT p1.full_name AS batter1, p2.full_name AS batter2, (b1.runs_scored+b2.runs_scored) AS partnership_runs, b1.innings_no FROM batting_performance b1 JOIN batting_performance b2 ON b1.match_id=b2.match_id AND b1.innings_no=b2.innings_no AND b2.batting_position=b1.batting_position+1 JOIN players p1 ON b1.player_id=p1.player_id JOIN players p2 ON b2.player_id=p2.player_id WHERE (b1.runs_scored+b2.runs_scored) >= 100;",
    "Q14 - Bowling economy by venue": "SELECT p.full_name, v.venue_name, ROUND(AVG(bo.economy_rate),2) AS avg_economy, SUM(bo.wickets_taken) AS total_wickets, COUNT(DISTINCT bo.match_id) AS matches_played FROM bowling_performance bo JOIN players p ON bo.player_id=p.player_id JOIN matches m ON bo.match_id=m.match_id JOIN venues v ON m.venue_id=v.venue_id WHERE bo.overs_bowled >= 4 GROUP BY p.player_id, v.venue_id HAVING COUNT(DISTINCT bo.match_id) >= 3;",
    "Q15 - Performance in close matches": "SELECT p.full_name, ROUND(AVG(b.runs_scored),2) AS avg_runs_close_matches, COUNT(DISTINCT m.match_id) AS close_matches_played, SUM(CASE WHEN m.winner_id=b.team_id THEN 1 ELSE 0 END) AS close_matches_won FROM batting_performance b JOIN players p ON b.player_id=p.player_id JOIN matches m ON b.match_id=m.match_id WHERE (m.victory_type='runs' AND m.victory_margin<50) OR (m.victory_type='wickets' AND m.victory_margin<5) GROUP BY p.player_id;",
    "Q16 - Yearly batting trend since 2020": "SELECT p.full_name, strftime('%Y', m.match_date) AS year, ROUND(AVG(b.runs_scored),2) AS avg_runs, ROUND(AVG(b.strike_rate),2) AS avg_strike_rate FROM batting_performance b JOIN players p ON b.player_id=p.player_id JOIN matches m ON b.match_id=m.match_id WHERE m.match_date >= '2020-01-01' GROUP BY p.player_id, year HAVING COUNT(DISTINCT b.match_id) >= 5;",
    "Q17 - Toss impact on outcome": "SELECT m.toss_decision, COUNT(*) AS total_matches, SUM(CASE WHEN m.toss_winner_id=m.winner_id THEN 1 ELSE 0 END) AS toss_winner_also_match_winner, ROUND(100.0*SUM(CASE WHEN m.toss_winner_id=m.winner_id THEN 1 ELSE 0 END)/COUNT(*),2) AS win_pct FROM matches m GROUP BY m.toss_decision;",
    "Q18 - Most economical bowlers": "SELECT p.full_name, ROUND(SUM(bo.runs_conceded)*1.0/SUM(bo.overs_bowled),2) AS economy_rate, SUM(bo.wickets_taken) AS total_wickets FROM bowling_performance bo JOIN players p ON bo.player_id=p.player_id JOIN matches m ON bo.match_id=m.match_id WHERE m.match_format IN ('ODI','T20I') GROUP BY p.player_id HAVING COUNT(DISTINCT bo.match_id)>=10 AND AVG(bo.overs_bowled)>=2 ORDER BY economy_rate ASC;",
    "Q19 - Most consistent batsmen": "SELECT p.full_name, ROUND(AVG(b.runs_scored),2) AS avg_runs, ROUND(SQRT(AVG(b.runs_scored*b.runs_scored)-AVG(b.runs_scored)*AVG(b.runs_scored)),2) AS stddev_runs FROM batting_performance b JOIN players p ON b.player_id=p.player_id JOIN matches m ON b.match_id=m.match_id WHERE b.balls_faced>=10 AND m.match_date>='2022-01-01' GROUP BY p.player_id ORDER BY stddev_runs ASC;",
    "Q20 - Matches & avg per format": "SELECT p.full_name, SUM(CASE WHEN m.match_format='Test' THEN 1 ELSE 0 END) AS test_matches, SUM(CASE WHEN m.match_format='ODI' THEN 1 ELSE 0 END) AS odi_matches, SUM(CASE WHEN m.match_format='T20I' THEN 1 ELSE 0 END) AS t20_matches, ROUND(AVG(CASE WHEN m.match_format='Test' THEN b.runs_scored END),2) AS test_avg, ROUND(AVG(CASE WHEN m.match_format='ODI' THEN b.runs_scored END),2) AS odi_avg, ROUND(AVG(CASE WHEN m.match_format='T20I' THEN b.runs_scored END),2) AS t20_avg FROM batting_performance b JOIN players p ON b.player_id=p.player_id JOIN matches m ON b.match_id=m.match_id GROUP BY p.player_id HAVING COUNT(DISTINCT b.match_id)>=20;",
    "Q21 - Weighted performance ranking": "SELECT p.full_name, m.match_format, ROUND((COALESCE(SUM(b.runs_scored),0)*0.01)+(COALESCE(AVG(b.runs_scored),0)*0.5)+(COALESCE(AVG(b.strike_rate),0)*0.3)+(COALESCE(SUM(bo.wickets_taken),0)*2)+((50-COALESCE(AVG(bo.runs_conceded*1.0/NULLIF(bo.wickets_taken,0)),50))*0.5)+((6-COALESCE(AVG(bo.economy_rate),6))*2)+(COALESCE(SUM(f.catches),0)*3)+(COALESCE(SUM(f.stumpings),0)*5),2) AS total_points FROM players p LEFT JOIN batting_performance b ON p.player_id=b.player_id LEFT JOIN bowling_performance bo ON p.player_id=bo.player_id AND b.match_id=bo.match_id LEFT JOIN fielding_performance f ON p.player_id=f.player_id AND b.match_id=f.match_id LEFT JOIN matches m ON b.match_id=m.match_id GROUP BY p.player_id, m.match_format ORDER BY m.match_format, total_points DESC;",
    "Q22 - Head-to-head analysis": "SELECT t1.team_name AS team_a, t2.team_name AS team_b, COUNT(*) AS total_matches, SUM(CASE WHEN m.winner_id=m.team1_id THEN 1 ELSE 0 END) AS team_a_wins, SUM(CASE WHEN m.winner_id=m.team2_id THEN 1 ELSE 0 END) AS team_b_wins, ROUND(AVG(CASE WHEN m.winner_id=m.team1_id THEN m.victory_margin END),2) AS avg_margin_team_a_win, ROUND(AVG(CASE WHEN m.winner_id=m.team2_id THEN m.victory_margin END),2) AS avg_margin_team_b_win FROM matches m JOIN teams t1 ON m.team1_id=t1.team_id JOIN teams t2 ON m.team2_id=t2.team_id WHERE m.match_date >= DATE('now','-3 years') GROUP BY t1.team_id, t2.team_id HAVING COUNT(*) >= 5;",
    "Q23 - Recent form categorization": "WITH recent_innings AS (SELECT b.player_id, b.runs_scored, b.strike_rate, ROW_NUMBER() OVER (PARTITION BY b.player_id ORDER BY m.match_date DESC) AS rn FROM batting_performance b JOIN matches m ON b.match_id=m.match_id) SELECT p.full_name, ROUND(AVG(CASE WHEN rn<=5 THEN runs_scored END),2) AS avg_last_5, ROUND(AVG(CASE WHEN rn<=10 THEN runs_scored END),2) AS avg_last_10, SUM(CASE WHEN rn<=10 AND runs_scored>=50 THEN 1 ELSE 0 END) AS scores_above_50, CASE WHEN AVG(CASE WHEN rn<=5 THEN runs_scored END)>=50 THEN 'Excellent Form' WHEN AVG(CASE WHEN rn<=5 THEN runs_scored END)>=35 THEN 'Good Form' WHEN AVG(CASE WHEN rn<=5 THEN runs_scored END)>=20 THEN 'Average Form' ELSE 'Poor Form' END AS form_category FROM recent_innings ri JOIN players p ON ri.player_id=p.player_id WHERE rn<=10 GROUP BY p.player_id;",
    "Q24 - Best batting partnerships": "SELECT p1.full_name AS batter1, p2.full_name AS batter2, ROUND(AVG(b1.runs_scored+b2.runs_scored),2) AS avg_partnership_runs, SUM(CASE WHEN (b1.runs_scored+b2.runs_scored)>50 THEN 1 ELSE 0 END) AS partnerships_over_50, MAX(b1.runs_scored+b2.runs_scored) AS highest_partnership, ROUND(100.0*SUM(CASE WHEN (b1.runs_scored+b2.runs_scored)>50 THEN 1 ELSE 0 END)/COUNT(*),2) AS success_rate FROM batting_performance b1 JOIN batting_performance b2 ON b1.match_id=b2.match_id AND b1.innings_no=b2.innings_no AND b2.batting_position=b1.batting_position+1 JOIN players p1 ON b1.player_id=p1.player_id JOIN players p2 ON b2.player_id=p2.player_id GROUP BY p1.player_id, p2.player_id HAVING COUNT(*)>=5 ORDER BY avg_partnership_runs DESC;",
    "Q25 - Quarterly trend & trajectory": "WITH quarterly AS (SELECT b.player_id, strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INTEGER)-1)/3+1) AS quarter, AVG(b.runs_scored) AS avg_runs, AVG(b.strike_rate) AS avg_sr, COUNT(*) AS matches_in_quarter FROM batting_performance b JOIN matches m ON b.match_id=m.match_id GROUP BY b.player_id, quarter HAVING COUNT(*)>=3), trend AS (SELECT *, LAG(avg_runs) OVER (PARTITION BY player_id ORDER BY quarter) AS prev_avg_runs FROM quarterly) SELECT p.full_name, t.quarter, t.avg_runs, t.avg_sr, CASE WHEN t.prev_avg_runs IS NULL THEN 'Baseline' WHEN t.avg_runs > t.prev_avg_runs THEN 'Improving' WHEN t.avg_runs < t.prev_avg_runs THEN 'Declining' ELSE 'Stable' END AS quarter_trend FROM trend t JOIN players p ON t.player_id=p.player_id WHERE t.player_id IN (SELECT player_id FROM quarterly GROUP BY player_id HAVING COUNT(*)>=6) ORDER BY p.full_name, t.quarter;",
}

st.sidebar.markdown("### Query difficulty")
difficulty = st.sidebar.radio("Filter", ["All", "Beginner (1-8)", "Intermediate (9-16)", "Advanced (17-25)"])

def filter_questions():
    keys = list(QUESTIONS.keys())
    if difficulty == "Beginner (1-8)":
        return keys[0:8]
    if difficulty == "Intermediate (9-16)":
        return keys[8:16]
    if difficulty == "Advanced (17-25)":
        return keys[16:25]
    return keys

choice = st.selectbox("Choose a predefined analytics question", filter_questions())
sql_text = st.text_area("SQL Query", value=QUESTIONS[choice], height=150)

col1, col2 = st.columns([1, 5])
with col1:
    run_clicked = st.button("▶ Run Query", type="primary")

if run_clicked:
    try:
        df = run_query(sql_text)
        st.success(f"{len(df)} rows returned")
        st.dataframe(df, use_container_width=True)
        if len(df) > 0 and df.select_dtypes(include="number").shape[1] > 0:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, 0])
    except Exception as e:
        st.error(f"Query failed: {e}")

st.divider()
st.markdown("#### ✍️ Or write your own custom query")
custom_sql = st.text_area("Custom SQL", placeholder="SELECT * FROM players LIMIT 10;", height=100)
if st.button("Run Custom Query"):
    try:
        df = run_query(custom_sql)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Query failed: {e}")
