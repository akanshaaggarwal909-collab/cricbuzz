"""
utils/api_client.py
Thin wrapper around the Cricbuzz Cricket API (RapidAPI) with
retry handling and clean error messages.
"""
import time
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CRICBUZZ_BASE_URL, CRICBUZZ_HEADERS, REQUEST_TIMEOUT


class CricbuzzAPIError(Exception):
    pass


def _get(endpoint: str, params: dict = None, retries: int = 3, backoff: float = 1.5):
    """GET request with simple retry/backoff. Raises CricbuzzAPIError on failure."""
    url = f"{CRICBUZZ_BASE_URL}{endpoint}"
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=CRICBUZZ_HEADERS, params=params, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < retries:
                time.sleep(backoff * attempt)
            continue

    raise CricbuzzAPIError(f"Failed to reach {endpoint} after {retries} attempts: {last_error}")


def get_live_matches():
    """Fetch currently live matches."""
    return _get("/matches/v1/live")


def get_recent_matches():
    """Fetch recently completed matches."""
    return _get("/matches/v1/recent")


def get_upcoming_matches():
    """Fetch upcoming/scheduled matches."""
    return _get("/matches/v1/upcoming")


def get_match_scorecard(match_id: str):
    """Fetch full scorecard for a given match id."""
    return _get(f"/mcenter/v1/{match_id}/scard")


def get_top_stats(stats_type: str = "mostRuns"):
    """
    Fetch top player stats.
    stats_type examples: mostRuns, mostWickets, highestScore, bestBowling
    """
    return _get(f"/stats/v1/topstats/0", params={"statsType": stats_type})


def get_player_info(player_id: str):
    """Fetch detailed profile info for a player."""
    return _get(f"/stats/v1/player/{player_id}")
