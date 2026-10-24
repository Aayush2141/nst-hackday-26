"""Net price = mandi modal price minus estimated transport.

net_price = modal_price - (distance_km * rate_per_quintal_per_km)

Default rate is 2.5 Rs per quintal per km (user-adjustable).
Only markets whose latest price is within the last 7 days are considered.
Results are ranked by net_price, highest first.

Outlier filtering: drops rows where modal_price is 0, null, or >5x the median
for that crop/day.
"""

from __future__ import annotations

from datetime import date

from backend.db import latest_prices_for_crop, list_states, newest_price_date
from backend.geo import haversine_km, resolve_district
from backend.outliers import filter_outliers

DEFAULT_RATE = 2.5
DEFAULT_RADIUS_KM = 300.0
STALE_DAYS = 3  # Show stale badge if price is older than this


def _days_old(arrival_date: str) -> int:
    """Days between arrival_date and today (non-negative)."""
    try:
        d = date.fromisoformat(arrival_date)
        return max(0, (date.today() - d).days)
    except (ValueError, TypeError):
        return 999


def rank_mandis(
    crop: str,
    lat: float,
    lon: float,
    rate: float = DEFAULT_RATE,
    radius_km: float = DEFAULT_RADIUS_KM,
) -> dict:
    """Return origin, ranked mandis, and the best row (or None).

    When no mandis are found within radius_km, returns nearest_state with data
    so the UI can show a helpful message.
    """
    origin = {"lat": lat, "lon": lon, "snapped": False}

    raw_rows = latest_prices_for_crop(crop, within_days=7)
    rows = filter_outliers(raw_rows)

    ranked: list[dict] = []
    for row in rows:
        try:
            loc = resolve_district(row["state"], row["district"], allow_remote=False)
        except RuntimeError:
            continue
        distance_km = round(haversine_km(lat, lon, loc["lat"], loc["lon"]), 2)
        if distance_km > radius_km:
            continue
        transport_cost = round(distance_km * rate, 2)
        net = round(float(row["modal_price"]) - transport_cost, 2)
        age = _days_old(row["arrival_date"])
        ranked.append(
            {
                "market": row["market"],
                "district": row["district"],
                "state": row["state"],
                "modal_price": round(float(row["modal_price"]), 2),
                "min_price": round(float(row["min_price"]), 2),
                "max_price": round(float(row["max_price"]), 2),
                "distance_km": distance_km,
                "transport_cost": transport_cost,
                "net_price": net,
                "price_date": row["arrival_date"],
                "arrival_date": row["arrival_date"],
                "crop": crop,
                "days_old": age,
                "stale": age > STALE_DAYS,
                "lat": loc["lat"],
                "lon": loc["lon"],
                "approximate_location": loc.get("approximate", False),
            }
        )

    ranked.sort(key=lambda r: r["net_price"], reverse=True)
    for i, item in enumerate(ranked, start=1):
        item["rank"] = i

    best = ranked[0] if ranked else None
    runner_up = ranked[1] if len(ranked) > 1 else None
    difference = None
    if best and runner_up:
        difference = round(best["net_price"] - runner_up["net_price"], 2)

    # Find nearest state with data if no results
    nearest_state_with_data = None
    if not ranked and raw_rows:
        min_dist = float("inf")
        nearest_state = None
        for r in raw_rows:
            try:
                loc = resolve_district(r["state"], r["district"], allow_remote=False)
                d = haversine_km(lat, lon, loc["lat"], loc["lon"])
                if d < min_dist:
                    min_dist = d
                    nearest_state = r["state"]
            except Exception:
                continue
        nearest_state_with_data = nearest_state

    return {
        "origin": origin,
        "crop": crop,
        "rate": rate,
        "radius_km": radius_km,
        "ranked": ranked,
        "best": best,
        "runner_up": runner_up,
        "difference_rs": difference,
        "nearest_state_with_data": nearest_state_with_data,
        "total_markets_checked": len(raw_rows),
    }


def rank_from_rows(
    rows: list[dict],
    origin_lat: float,
    origin_lon: float,
    rate: float,
    radius_km: float,
    coords_lookup,
) -> list[dict]:
    """Pure helper used by tests: rank pre-built rows without touching SQLite."""
    ranked = []
    for row in rows:
        loc = coords_lookup(row["district"])
        distance_km = round(haversine_km(origin_lat, origin_lon, loc["lat"], loc["lon"]), 2)
        if distance_km > radius_km:
            continue
        transport_cost = round(distance_km * rate, 2)
        net = round(float(row["modal_price"]) - transport_cost, 2)
        ranked.append(
            {
                "market": row["market"],
                "district": row["district"],
                "modal_price": float(row["modal_price"]),
                "distance_km": distance_km,
                "transport_cost": transport_cost,
                "net_price": net,
                "price_date": row.get("arrival_date"),
            }
        )
    ranked.sort(key=lambda r: r["net_price"], reverse=True)
    return ranked
