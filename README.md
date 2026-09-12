# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A Streamlit dashboard that combines live data from the Cricbuzz API with a SQL
database to deliver real-time match updates, player statistics, SQL-driven
analytics, and full CRUD data management.

## Features
- ⚡ **Live Matches** — real-time scores via the Cricbuzz API
- 📊 **Top Player Stats** — most runs, most wickets, highest scores, best bowling
- 🧮 **SQL Analytics** — 25 queries from beginner to advanced (joins, CTEs, window functions)
- 🛠 **CRUD** — add, view, update, delete player records through a form UI

## Tech Stack
Python · Streamlit · SQL (SQLite/MySQL/PostgreSQL) · REST API · pandas · requests

## Project Structure
```
cricbuzz_livestats/
├── app.py                     # Main entry point
├── config.py                  # API keys & DB settings (env-var driven)
├── requirements.txt
├── README.md
├── pages/
│   ├── home.py                # Overview & setup instructions
│   ├── live_matches.py        # Live scores from Cricbuzz API
│   ├── top_stats.py           # Top batting/bowling stats
│   ├── sql_queries.py         # 25 SQL analytics queries + custom query box
│   └── crud_operations.py     # CRUD on player records
├── utils/
│   ├── db_connection.py       # Database-agnostic connection handling
│   └── api_client.py          # Cricbuzz API wrapper with retry logic
├── sql/
│   ├── schema.sql             # CREATE TABLE statements, keys, indexes
│   ├── sample_data.sql        # Seed data for offline testing
│   └── queries.sql            # All 25 analytics queries, documented
└── notebooks/
    └── data_fetching.ipynb    # Scratchpad for testing API calls & DB writes
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API credentials
Get a free Cricbuzz API key from [RapidAPI](https://rapidapi.com/) and set:
```bash
export CRICBUZZ_API_KEY="your_rapidapi_key"
```

### 3. Configure the database
Defaults to SQLite (zero setup). To use MySQL/PostgreSQL instead:
```bash
export DB_TYPE="mysql"        # or "postgresql"
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="yourpassword"
export MYSQL_DATABASE="cricbuzz_livestats"
```

### 4. Initialize the database
```bash
python -c "from utils.db_connection import init_db; init_db()"
```
This runs `sql/schema.sql` (creates tables/indexes) and `sql/sample_data.sql`
(seeds sample rows) so the app and SQL queries are usable immediately.

### 5. Run the app
```bash
streamlit run app.py
```

## Database Schema (Summary)
| Table | Purpose |
|---|---|
| `teams` | International teams |
| `venues` | Grounds with city/country/capacity |
| `players` | Player master data |
| `series` | Tours/tournaments |
| `matches` | Individual matches, linked to series/teams/venues |
| `batting_performance` | Per-innings batting stats per player |
| `bowling_performance` | Per-innings bowling stats per player |
| `fielding_performance` | Catches/stumpings/run-outs per match |

See `sql/schema.sql` for full DDL with primary/foreign keys and indexes.

## SQL Analytics
`sql/queries.sql` contains all 25 required queries:
- **Beginner (1–8):** filtering, grouping, ordering
- **Intermediate (9–16):** joins, subqueries, aggregates
- **Advanced (17–25):** window functions, CTEs, statistical calculations
  (toss-advantage, consistency via std-dev, weighted ranking, head-to-head,
  form categorization, partnership analysis, quarterly trend/trajectory)

All 25 are also wired into the **SQL Queries & Analytics** page for one-click
execution against the live database.

## Notes on the Cricbuzz API
This project assumes access via RapidAPI's Cricbuzz Cricket API. Endpoint
paths and JSON field names can change between API plans — adjust the parsing
logic in `pages/live_matches.py` / `pages/top_stats.py` to match your
subscription's actual response shape.

## Deployment
The app can be deployed as-is to **Streamlit Community Cloud**, **Render**,
**Railway**, or containerized with **Docker** and deployed to Azure/AWS.
Remember to set the same environment variables (API key, DB config) in your
deployment platform's secrets manager.

## Coding Standards
- PEP 8 style
- Modular structure (API layer, DB layer, UI pages separated)
- Centralized error handling for API and DB exceptions
- Credentials via environment variables only — never hardcoded

## Timeline
Built to the 14-day project timeline: environment setup → database →
API integration → CRUD → SQL analytics → dashboard polish → documentation.
