-- ============================================================
-- Sample seed data so the app/queries are runnable without
-- a live API key. Replace/extend with real Cricbuzz data.
-- ============================================================

INSERT INTO teams (team_name, country) VALUES
('India', 'India'), ('Australia', 'Australia'), ('England', 'England'),
('New Zealand', 'New Zealand'), ('South Africa', 'South Africa'), ('Pakistan', 'Pakistan');

INSERT INTO venues (venue_name, city, country, capacity) VALUES
('Melbourne Cricket Ground', 'Melbourne', 'Australia', 100024),
('Eden Gardens', 'Kolkata', 'India', 68000),
('Lords', 'London', 'England', 30000),
('Wankhede Stadium', 'Mumbai', 'India', 33000),
('Narendra Modi Stadium', 'Ahmedabad', 'India', 132000);

INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style, date_of_birth) VALUES
('Virat Kohli', 'India', 'Batsman', 'Right-hand bat', NULL, '1988-11-05'),
('Rohit Sharma', 'India', 'Batsman', 'Right-hand bat', NULL, '1987-04-30'),
('Jasprit Bumrah', 'India', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-12-06'),
('Ravindra Jadeja', 'India', 'All-rounder', 'Left-hand bat', 'Left-arm orthodox', '1988-12-06'),
('Pat Cummins', 'Australia', 'Bowler', 'Right-hand bat', 'Right-arm fast', '1993-05-08'),
('Steve Smith', 'Australia', 'Batsman', 'Right-hand bat', 'Right-arm leg break', '1989-06-02'),
('Joe Root', 'England', 'Batsman', 'Right-hand bat', 'Right-arm off break', '1990-12-30'),
('Ben Stokes', 'England', 'All-rounder', 'Left-hand bat', 'Right-arm fast-medium', '1991-06-04'),
('Kane Williamson', 'New Zealand', 'Batsman', 'Right-hand bat', NULL, '1990-08-08'),
('Babar Azam', 'Pakistan', 'Batsman', 'Right-hand bat', NULL, '1994-10-15');

INSERT INTO series (series_name, host_country, match_type, start_date, total_matches) VALUES
('Border-Gavaskar Trophy 2024', 'Australia', 'Test', '2024-12-06', 5),
('India tour of England 2024', 'England', 'ODI', '2024-01-15', 3);

-- Note: matches / batting / bowling / fielding sample rows would be
-- generated in bulk by notebooks/data_fetching.ipynb once the live
-- API is connected. A few illustrative rows are inserted below.

INSERT INTO matches (series_id, match_desc, team1_id, team2_id, venue_id, match_format, match_date, toss_winner_id, toss_decision, winner_id, victory_margin, victory_type) VALUES
(1, '1st Test', 1, 2, 1, 'Test', '2024-12-06', 2, 'bat', 2, 9, 'wickets'),
(2, '2nd ODI', 1, 3, 4, 'ODI', '2024-01-19', 1, 'bowl', 1, 3, 'wickets');

INSERT INTO batting_performance (match_id, player_id, team_id, innings_no, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, is_out) VALUES
(1, 1, 1, 1, 4, 56, 45, 4, 1, 124.44, 1),
(1, 2, 1, 1, 1, 28, 23, 3, 0, 121.74, 1),
(2, 1, 1, 1, 4, 74, 60, 6, 2, 123.33, 0);

INSERT INTO bowling_performance (match_id, player_id, team_id, innings_no, overs_bowled, runs_conceded, wickets_taken, economy_rate) VALUES
(1, 5, 2, 2, 18.0, 62, 4, 3.44),
(1, 3, 1, 2, 20.0, 55, 2, 2.75);

INSERT INTO fielding_performance (match_id, player_id, catches, stumpings, run_outs) VALUES
(1, 4, 2, 0, 0),
(2, 3, 1, 0, 1);
