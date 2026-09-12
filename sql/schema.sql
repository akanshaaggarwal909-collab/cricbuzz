-- ============================================================
-- Cricbuzz LiveStats - Database Schema
-- Works on SQLite / MySQL / PostgreSQL with minor type tweaks
-- ============================================================

-- 1. TEAMS
CREATE TABLE teams (
    team_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name    VARCHAR(100) NOT NULL UNIQUE,
    country      VARCHAR(100) NOT NULL
);

-- 2. VENUES
CREATE TABLE venues (
    venue_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name   VARCHAR(150) NOT NULL,
    city         VARCHAR(100),
    country      VARCHAR(100) NOT NULL,
    capacity     INTEGER
);

-- 3. PLAYERS
CREATE TABLE players (
    player_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     VARCHAR(150) NOT NULL,
    country       VARCHAR(100) NOT NULL,
    playing_role  VARCHAR(50)  NOT NULL,   -- Batsman, Bowler, All-rounder, Wicket-keeper
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    date_of_birth DATE
);

-- 4. SERIES
CREATE TABLE series (
    series_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name   VARCHAR(200) NOT NULL,
    host_country  VARCHAR(100),
    match_type    VARCHAR(20),             -- Test, ODI, T20I
    start_date    DATE,
    total_matches INTEGER
);

-- 5. MATCHES
CREATE TABLE matches (
    match_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id      INTEGER REFERENCES series(series_id),
    match_desc     VARCHAR(200),
    team1_id       INTEGER REFERENCES teams(team_id),
    team2_id       INTEGER REFERENCES teams(team_id),
    venue_id       INTEGER REFERENCES venues(venue_id),
    match_format   VARCHAR(20),            -- Test, ODI, T20I
    match_date     DATE,
    toss_winner_id INTEGER REFERENCES teams(team_id),
    toss_decision  VARCHAR(10),            -- bat / bowl
    winner_id      INTEGER REFERENCES teams(team_id),
    victory_margin INTEGER,
    victory_type   VARCHAR(10)             -- runs / wickets
);

-- 6. BATTING_PERFORMANCE (one row per player per innings)
CREATE TABLE batting_performance (
    batting_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id      INTEGER REFERENCES matches(match_id),
    player_id     INTEGER REFERENCES players(player_id),
    team_id       INTEGER REFERENCES teams(team_id),
    innings_no    INTEGER NOT NULL,
    batting_position INTEGER,
    runs_scored   INTEGER DEFAULT 0,
    balls_faced   INTEGER DEFAULT 0,
    fours         INTEGER DEFAULT 0,
    sixes         INTEGER DEFAULT 0,
    strike_rate   DECIMAL(6,2),
    is_out        BOOLEAN DEFAULT 1
);

-- 7. BOWLING_PERFORMANCE (one row per player per innings)
CREATE TABLE bowling_performance (
    bowling_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id      INTEGER REFERENCES matches(match_id),
    player_id     INTEGER REFERENCES players(player_id),
    team_id       INTEGER REFERENCES teams(team_id),
    innings_no    INTEGER NOT NULL,
    overs_bowled  DECIMAL(4,1) DEFAULT 0,
    runs_conceded INTEGER DEFAULT 0,
    wickets_taken INTEGER DEFAULT 0,
    economy_rate  DECIMAL(5,2)
);

-- 8. FIELDING_PERFORMANCE
CREATE TABLE fielding_performance (
    fielding_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id      INTEGER REFERENCES matches(match_id),
    player_id     INTEGER REFERENCES players(player_id),
    catches       INTEGER DEFAULT 0,
    stumpings     INTEGER DEFAULT 0,
    run_outs      INTEGER DEFAULT 0
);

-- ============================================================
-- INDEXES for frequently queried columns
-- ============================================================
CREATE INDEX idx_batting_player      ON batting_performance(player_id);
CREATE INDEX idx_batting_match       ON batting_performance(match_id);
CREATE INDEX idx_bowling_player      ON bowling_performance(player_id);
CREATE INDEX idx_bowling_match       ON bowling_performance(match_id);
CREATE INDEX idx_matches_date        ON matches(match_date);
CREATE INDEX idx_matches_format      ON matches(match_format);
CREATE INDEX idx_players_country     ON players(country);
CREATE INDEX idx_players_role        ON players(playing_role);
