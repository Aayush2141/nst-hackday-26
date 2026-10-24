"""District coordinates: geo_cache SQLite table → Open-Meteo geocoding → state centroid fallback.

Lookup order for any district:
  1. geo_cache table (SQLite, fast, permanent)
  2. Open-Meteo geocoding API (free, no key, rate-limited)
  3. State centroid from data/state_centroids.csv (always available, flagged "approximate")

Distances are computed with the haversine formula (great-circle km).
"""

from __future__ import annotations

import csv
import math
import time
from functools import lru_cache
from pathlib import Path
from typing import Optional

import requests

ROOT = Path(__file__).resolve().parent.parent
STATE_CENTROIDS_CSV = ROOT / "data" / "state_centroids.csv"
MANDI_COORDS_CSV = ROOT / "data" / "mandi_coords.csv"

EARTH_RADIUS_KM = 6371.0
_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Rate-limit: one external geocoding call per second at most
_LAST_GEOCODE_CALL: float = 0.0
_MIN_GEOCODE_INTERVAL = 1.1  # seconds between calls


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return great-circle distance in kilometres between two WGS84 points."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


@lru_cache(maxsize=1)
def _load_mandi_coords() -> dict[str, tuple[float, float]]:
    coords: dict[str, tuple[float, float]] = {}
    if not MANDI_COORDS_CSV.exists():
        return coords
    with MANDI_COORDS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            k = f"{row['state'].strip().lower()}|{row['district'].strip().lower()}"
            coords[k] = (float(row["lat"]), float(row["lon"]))
    return coords


@lru_cache(maxsize=1)
def _load_state_centroids() -> dict[str, dict]:
    """Load all-India state centroids. Cached after the first read."""
    centroids: dict[str, dict] = {}
    if not STATE_CENTROIDS_CSV.exists():
        return centroids
    with STATE_CENTROIDS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            state = row["state"].strip()
            centroids[state.lower()] = {
                "state": state,
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "source": "state_centroid",
                "approximate": True,
            }
    return centroids


def _state_centroid(state: str) -> Optional[dict]:
    """Return the state centroid dict or None."""
    centroids = _load_state_centroids()
    return centroids.get(state.strip().lower())


def _rate_limit_geocode() -> None:
    global _LAST_GEOCODE_CALL
    elapsed = time.time() - _LAST_GEOCODE_CALL
    if elapsed < _MIN_GEOCODE_INTERVAL:
        time.sleep(_MIN_GEOCODE_INTERVAL - elapsed)
    _LAST_GEOCODE_CALL = time.time()


def _fetch_geocode(district: str, state: str) -> Optional[tuple[float, float]]:
    """Call Open-Meteo geocoding API. Returns (lat, lon) or None."""
    _rate_limit_geocode()
    query = f"{district}, {state}, India"
    try:
        resp = requests.get(
            _GEOCODE_URL,
            params={"name": query, "count": 5, "language": "en", "format": "json"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results") or []
        if not results:
            return None
        # Prefer results in the correct country (India) and matching state
        state_lower = state.lower()
        for r in results:
            country = (r.get("country") or "").lower()
            admin1 = (r.get("admin1") or "").lower()
            if "india" in country or country == "in":
                if state_lower in admin1 or admin1 in state_lower:
                    return float(r["latitude"]), float(r["longitude"])
        # If no state match, accept any India result
        for r in results:
            country = (r.get("country") or "").lower()
            if "india" in country or country == "in":
                return float(r["latitude"]), float(r["longitude"])
        return None
    except (requests.RequestException, KeyError, ValueError):
        return None


def resolve_district(
    state: str,
    district: str,
    allow_remote: bool = True,
    remote_budget: Optional[list[int]] = None,
) -> dict:
    """Resolve (state, district) → {lat, lon, source, approximate}.

    Lookup order:
      1. geo_cache SQLite table
      2. Open-Meteo geocoding (if allow_remote and budget > 0)
      3. State centroid (always succeeds, approximate=True)

    `remote_budget` is a mutable [count] list; each remote call decrements it.
    Pass [1] to allow at most one live call in this invocation.
    """
    from backend import db  # avoid circular at module load
    from backend.names import DISTRICT_ALIASES

    alias_name = DISTRICT_ALIASES.get(district.lower().strip())

    # 1. Check local mandi coordinates table first
    local_coords = _load_mandi_coords()
    key = f"{state.strip().lower()}|{district.strip().lower()}"
    alias_key = f"{state.strip().lower()}|{alias_name.strip().lower()}" if alias_name else None
    if key in local_coords or (alias_key and alias_key in local_coords):
        lat, lon = local_coords[key] if key in local_coords else local_coords[alias_key]
        return {
            "state": state,
            "district": district,
            "lat": lat,
            "lon": lon,
            "source": "mandi_coords",
            "approximate": False,
        }

    # 2. Check cache (original name or alias)
    cached = db.geo_cache_get(state, district)
    if cached is None and alias_name:
        cached = db.geo_cache_get(state, alias_name)

    if cached is not None and cached["lat"] is not None:
        return {
            "state": state,
            "district": district,
            "lat": cached["lat"],
            "lon": cached["lon"],
            "source": cached["source"],
            "approximate": cached["source"] in ("state_centroid", "geocode_failed"),
        }

    # 2. Remote geocoding
    if allow_remote and (remote_budget is None or (remote_budget and remote_budget[0] > 0)):
        if remote_budget is not None:
            remote_budget[0] -= 1
        coords = _fetch_geocode(district, state)
        if not coords and alias_name:
            coords = _fetch_geocode(alias_name, state)

        if coords:
            lat, lon = coords
            db.geo_cache_put(state, district, lat, lon, "open_meteo")
            if alias_name:
                db.geo_cache_put(state, alias_name, lat, lon, "open_meteo")
            return {
                "state": state,
                "district": district,
                "lat": lat,
                "lon": lon,
                "source": "open_meteo",
                "approximate": False,
            }
        else:
            # Cache the failure so we don't retry every request
            db.geo_cache_put(state, district, None, None, "geocode_failed")

    # 3. State centroid fallback
    centroid = _state_centroid(state)
    if centroid:
        return {**centroid, "state": state, "district": district, "approximate": True}

    raise RuntimeError(f"No coordinates for {district}, {state} — add to state_centroids.csv")


def coords_for_district(
    district: str, state: Optional[str] = None, allow_remote: bool = False
) -> Optional[dict]:
    """Look up coordinates for a district; returns None if not found and remote disabled."""
    if not state:
        return None
    try:
        return resolve_district(state, district, allow_remote=allow_remote)
    except RuntimeError:
        return None


def nearest_district_from_db(lat: float, lon: float) -> Optional[dict]:
    """Find the closest district in geo_cache with valid coordinates."""
    from backend import db
    conn = db.get_conn()
    try:
        rows = conn.execute(
            "SELECT state, district, lat, lon, source FROM geo_cache WHERE lat IS NOT NULL"
        ).fetchall()
    finally:
        conn.close()
    if not rows:
        return None
    best = None
    best_km = float("inf")
    for row in rows:
        km = haversine_km(lat, lon, row["lat"], row["lon"])
        if km < best_km:
            best_km = km
            best = {
                "state": row["state"],
                "district": row["district"],
                "lat": row["lat"],
                "lon": row["lon"],
                "distance_km": round(km, 2),
                "source": row["source"],
            }
    return best


def resolve_origin(lat: float, lon: float) -> dict:
    """Return the user's effective origin; always succeeds."""
    return {
        "lat": lat,
        "lon": lon,
        "snapped": False,
    }


# Keep legacy compat
def load_coords() -> list[dict]:
    """Return districts from geo_cache that have coordinates (for the meta endpoint)."""
    from backend import db
    conn = db.get_conn()
    try:
        rows = conn.execute(
            "SELECT DISTINCT state, district, lat, lon FROM geo_cache WHERE lat IS NOT NULL ORDER BY state, district"
        ).fetchall()
        return [{"district": r["district"], "state": r["state"], "lat": r["lat"], "lon": r["lon"]} for r in rows]
    finally:
        conn.close()
