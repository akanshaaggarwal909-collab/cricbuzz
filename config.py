"""
config.py
Central configuration for Cricbuzz LiveStats.
Loads secrets from environment variables — never hardcode credentials.
"""
import os

# ---- Cricbuzz API (via RapidAPI) ----
CRICBUZZ_API_KEY = os.getenv("CRICBUZZ_API_KEY", "")
CRICBUZZ_API_HOST = os.getenv("CRICBUZZ_API_HOST", "cricbuzz-cricket.p.rapidapi.com")
CRICBUZZ_BASE_URL = f"https://{CRICBUZZ_API_HOST}"

CRICBUZZ_HEADERS = {
    "X-RapidAPI-Key": CRICBUZZ_API_KEY,
    "X-RapidAPI-Host": CRICBUZZ_API_HOST,
}

# ---- Database ----
# db_type: "sqlite" | "mysql" | "postgresql"
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

DB_CONFIG = {
    "sqlite": {
        "path": os.getenv("SQLITE_PATH", "cricbuzz_livestats.db"),
    },
    "mysql": {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "cricbuzz_livestats"),
    },
    "postgresql": {
        "host": os.getenv("PG_HOST", "localhost"),
        "port": int(os.getenv("PG_PORT", 5432)),
        "user": os.getenv("PG_USER", "postgres"),
        "password": os.getenv("PG_PASSWORD", ""),
        "database": os.getenv("PG_DATABASE", "cricbuzz_livestats"),
    },
}

# App-level settings
APP_TITLE = "Cricbuzz LiveStats"
REQUEST_TIMEOUT = 10  # seconds
