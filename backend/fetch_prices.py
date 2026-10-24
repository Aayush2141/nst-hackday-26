"""Load Agmarknet prices from data.gov.in, a CSV file, or the demo seed.

Field names from data.gov.in vary (spaces vs underscores, Title Case, etc.).
We normalise them before insert. Pagination and retries with backoff are handled.

CLI:
  python -m backend.fetch_prices --all
  python -m backend.fetch_prices --states "Maharashtra,Punjab,Uttar Pradesh,Madhya Pradesh,Gujarat,Karnataka,Tamil Nadu,West Bengal,Rajasthan,Haryana,Andhra Pradesh,Telangana,Bihar,Kerala,Odisha"
  python -m backend.fetch_prices --csv path/to/file.csv
  python -m backend.fetch_prices --seed
"""

from __future__ import annotations

import argparse
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import pandas as pd
import requests
from dotenv import load_dotenv

from backend.db import (
    count_live_prices,
    count_markets,
    count_prices,
    count_states,
    delete_seed_rows,
    init_db,
    newest_price_date,
    oldest_price_date,
    sample_prices,
    set_meta,
    upsert_prices,
)
from backend.names import canonical_state, title_place

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("fetch_prices")

ROOT = Path(__file__).resolve().parent.parent
SEED_CSV = ROOT / "data" / "seed_prices.csv"

# Verified active Agmarknet daily prices resource ID on data.gov.in
DEFAULT_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
API_BASE = "https://api.data.gov.in/resource/{resource_id}"

ALL_INDIA_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Andaman and Nicobar Islands", "Chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu", "Delhi",
    "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
]

FIELD_ALIASES = {
    "state": {"state", "state_name", "state name"},
    "district": {"district", "district_name", "district name"},
    "market": {"market", "mandi", "market_name", "mandiname", "market name"},
    "commodity": {"commodity", "commodity_name", "crop", "commodity name"},
    "variety": {"variety", "variety_name", "variety name"},
    "grade": {"grade", "grade_name", "quality"},
    "arrival_date": {
        "arrival_date",
        "arrivaldate",
        "date",
        "reported_date",
        "price_date",
        "arrival date",
    },
    "min_price": {"min_price", "minprice", "minimum", "min", "min_pric", "minimum price", "min price"},
    "max_price": {"max_price", "maxprice", "maximum", "max", "max_pric", "maximum price", "max price"},
    "modal_price": {"modal_price", "modalprice", "modal", "mode_price", "modal_pric", "modal price"},
}

REQUIRED = (
    "state",
    "district",
    "market",
    "commodity",
    "arrival_date",
    "min_price",
    "max_price",
    "modal_price",
)


def _norm_col(name: str) -> str:
    text = str(name).strip().lower()
    text = text.replace("_x0020_", "_").replace("x0020", "_")
    return (
        text.replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace(".", "")
        .replace("__", "_")
    )


def _canonical_columns(columns: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    normalised = {_norm_col(c): c for c in columns}
    raw_lower = {c.strip().lower(): c for c in columns}
    for canon, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            norm_alias = _norm_col(alias)
            if norm_alias in normalised:
                mapping[canon] = normalised[norm_alias]
                break
            if alias in raw_lower:
                mapping[canon] = raw_lower[alias]
                break
    return mapping


def parse_record(rec: dict[str, Any]) -> Optional[dict[str, Any]]:
    arrival_raw = str(rec.get("arrival_date") or "").strip()
    if not arrival_raw:
        return None

    arrival_iso = None
    # Parse format %d/%m/%Y (e.g. 24/10/2026) and store ISO YYYY-MM-DD
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            arrival_iso = datetime.strptime(arrival_raw, fmt).date().isoformat()
            break
        except ValueError:
            pass
    if not arrival_iso:
        return None

    # Keep numeric prices; skip rows with null or zero modal_price
    try:
        modal_val = rec.get("modal_price")
        if modal_val is None or str(modal_val).strip() == "":
            return None
        modal = float(modal_val)
        if modal <= 0:
            return None
    except (ValueError, TypeError):
        return None

    try:
        min_p = float(rec.get("min_price", modal) or modal)
    except (ValueError, TypeError):
        min_p = modal

    try:
        max_p = float(rec.get("max_price", modal) or modal)
    except (ValueError, TypeError):
        max_p = modal

    lo, hi = (min_p, max_p) if min_p <= max_p else (max_p, min_p)
    if lo <= 0:
        lo = modal
    if hi <= 0:
        hi = modal
    modal = min(max(modal, lo), hi)

    state = str(rec.get("state") or "").strip()
    district = str(rec.get("district") or "").strip()
    market = str(rec.get("market") or "").strip()
    commodity = str(rec.get("commodity") or "").strip()
    variety = str(rec.get("variety") or "FAQ").strip() or "FAQ"
    grade = str(rec.get("grade") or "FAQ").strip() or "FAQ"

    if not state or not district or not market or not commodity:
        return None

    return {
        "state": canonical_state(state),
        "district": title_place(district),
        "market": title_place(market),
        "commodity": commodity,
        "variety": variety,
        "grade": grade,
        "arrival_date": arrival_iso,
        "min_price": round(lo, 2),
        "max_price": round(hi, 2),
        "modal_price": round(float(modal), 2),
    }


def dataframe_to_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    mapping = _canonical_columns(list(df.columns))
    missing = [k for k in REQUIRED if k not in mapping]
    if missing:
        raise ValueError(
            f"CSV/API columns missing {missing}. Got: {list(df.columns)}"
        )
    rows = []
    for _, rec in df.iterrows():
        raw_dict = {k: rec[mapping[k]] for k in REQUIRED}
        if "variety" in mapping:
            raw_dict["variety"] = rec[mapping["variety"]]
        if "grade" in mapping:
            raw_dict["grade"] = rec[mapping["grade"]]
        parsed = parse_record(raw_dict)
        if parsed is not None:
            rows.append(parsed)
    return rows


def load_csv(path: Path, is_seed: bool = False) -> int:
    """Read a downloaded Agmarknet CSV (or our seed file) into SQLite."""
    init_db()
    df = pd.read_csv(path)
    rows = dataframe_to_rows(df)
    return upsert_prices(rows, is_seed=is_seed)


def load_seed() -> int:
    """Load data/seed_prices.csv and mark the database as sample data."""
    if not SEED_CSV.exists():
        raise FileNotFoundError(
            f"{SEED_CSV} missing. Run: python scripts/seed_demo_data.py"
        )
    added = load_csv(SEED_CSV, is_seed=True)
    set_meta("source", "seed")
    set_meta("last_updated", datetime.now().date().isoformat())
    set_meta("banner", "sample")
    return added


def _fetch_state_prices(
    session: requests.Session,
    url: str,
    api_key: str,
    state: str,
    limit: int = 100,
    max_pages: int = 50,
) -> int:
    """Fetch all pages for one state using filters[state.keyword]=<State>, limit=100.
    
    Connect timeout 20s, read timeout 180s, up to 6 retries with exponential backoff & jitter.
    Commits after every page and prints 'state, page N, rows so far'.
    """
    offset = 0
    state_total_inserted = 0

    for page_idx in range(1, max_pages + 1):
        params = {
            "api-key": api_key,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[state.keyword]": state,
        }

        attempts = 6
        payload: Optional[dict[str, Any]] = None
        for attempt in range(1, attempts + 1):
            try:
                resp = session.get(url, params=params, timeout=(20, 180))
                if resp.status_code == 429:
                    # Rate limit backoff
                    delay = (2.0 ** attempt) + random.uniform(0.5, 2.5)
                    time.sleep(delay)
                    continue
                resp.raise_for_status()
                payload = resp.json()
                break
            except Exception as exc:
                delay = (1.5 ** attempt) + random.uniform(0.5, 2.0)
                if attempt == attempts:
                    logger.warning(f"[{state}] Page {page_idx} (offset {offset}) failed after {attempts} retries: {exc}. Skipping page.")
                else:
                    time.sleep(delay)

        if payload is None:
            # Skip this page and try next offset
            offset += limit
            continue

        records = payload.get("records") or []
        total_api = payload.get("total") or 0

        if not records:
            break

        parsed_rows: list[dict[str, Any]] = []
        for rec in records:
            p = parse_record(rec)
            if p is not None:
                parsed_rows.append(p)

        page_inserted = 0
        if parsed_rows:
            page_inserted = upsert_prices(parsed_rows, is_seed=False)
            state_total_inserted += page_inserted

        print(f"{state}, page {page_idx}, rows so far: {state_total_inserted}")

        offset += limit
        if total_api > 0 and offset >= total_api:
            break
        if len(records) < limit:
            break

        # Polite interval between requests
        time.sleep(0.4)

    return state_total_inserted


def fetch_live_all_states(
    states: list[str],
    api_key: Optional[str] = None,
    resource_id: Optional[str] = None,
) -> int:
    api_key = api_key or os.getenv("DATA_GOV_API_KEY", "").strip()
    resource_id = resource_id or os.getenv("DATA_GOV_RESOURCE_ID", "").strip() or DEFAULT_RESOURCE_ID

    if not api_key:
        raise RuntimeError("DATA_GOV_API_KEY is not set in environment or .env")

    init_db()
    url = API_BASE.format(resource_id=resource_id)

    session = requests.Session()
    session.headers.update({
        "User-Agent": "MandiSaathi/2.0 (Agmarknet Live Ingestion; AgriTech India)",
        "Accept": "application/json",
    })

    grand_total = 0
    for state in states:
        logger.info(f"--- Fetching prices for {state} ---")
        try:
            n = _fetch_state_prices(session, url, api_key, state, limit=100)
            grand_total += n
            logger.info(f"Finished {state}: {n} rows committed")
        except Exception as exc:
            logger.error(f"Error fetching state {state}: {exc}")

    if grand_total > 0:
        set_meta("source", "live")
        set_meta("banner", "live")
        set_meta("last_updated", datetime.now().date().isoformat())

    return grand_total


def main() -> None:
    parser = argparse.ArgumentParser(description="Load mandi prices into SQLite")
    parser.add_argument("--csv", type=str, help="Path to a downloaded CSV")
    parser.add_argument("--seed", action="store_true", help="Load data/seed_prices.csv")
    parser.add_argument("--live", action="store_true", help="Fetch from data.gov.in")
    parser.add_argument("--all", action="store_true", help="Fetch all-India data (28 states + UTs)")
    parser.add_argument("--states", type=str, help='Comma-separated states e.g. "Maharashtra,Punjab"')
    parser.add_argument("--commodities", type=str, help='Comma-separated crops')
    args = parser.parse_args()

    init_db()

    if args.csv:
        n = load_csv(Path(args.csv))
        if Path(args.csv).resolve() == SEED_CSV.resolve():
            set_meta("source", "seed")
            set_meta("banner", "sample")
        else:
            set_meta("source", "live")
            set_meta("banner", "live")
        set_meta("last_updated", datetime.now().date().isoformat())
        print(f"Loaded {n} rows from CSV ({count_prices()} total).")
        return

    if args.seed:
        n = load_seed()
        print(f"Seeded {n} new rows ({count_prices()} total).")
        return

    # Live fetch per state
    target_states: list[str] = []
    if args.states:
        target_states = [s.strip() for s in args.states.split(",") if s.strip()]
    elif args.all or args.live:
        target_states = ALL_INDIA_STATES

    if target_states:
        print(f"Starting state-by-state Agmarknet fetch for {len(target_states)} states...")
        total = fetch_live_all_states(target_states)
        print(f"Live fetch complete! Total rows inserted/updated: {total}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
