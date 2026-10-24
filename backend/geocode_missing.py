"""Geocode districts missing from geo_cache.

Run in the background so user requests never wait on hundreds of lookups:

    python -m backend.geocode_missing
"""

from __future__ import annotations

import argparse
import sys
import time

from backend import db
from backend.geo import resolve_district


def geocode_missing(limit: int = 500, sleep_s: float = 0.3) -> int:
    db.init_db()
    missing = db.geo_missing_districts()
    done = 0
    for place in missing[:limit]:
        try:
            resolve_district(
                place["state"],
                place["district"],
                allow_remote=True,
                remote_budget=[1],
            )
        except RuntimeError as exc:
            print(f"  skip {place['district']}, {place['state']}: {exc}")
        done += 1
        time.sleep(sleep_s)
        if done % 25 == 0:
            print(f"geocoded {done}/{min(limit, len(missing))}", flush=True)
    print(f"geocode_missing finished: {done} districts")
    return done


def main() -> int:
    parser = argparse.ArgumentParser(description="Geocode districts missing from geo_cache")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--sleep", type=float, default=0.3)
    args = parser.parse_args()
    try:
        geocode_missing(limit=args.limit, sleep_s=args.sleep)
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"geocode_missing failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
