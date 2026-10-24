#!/usr/bin/env bash
# Create a venv, install deps, seed SQLite if empty, optionally fetch live
# Agmarknet data, then start the app on port 8000.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

export PYTHONPATH="$ROOT"

python scripts/seed_demo_data.py

python - <<'PY'
import os
from backend.db import count_prices, get_meta, init_db
from backend.fetch_prices import fetch_live, load_seed

init_db()
if count_prices() == 0:
    print("Database empty — loading SAMPLE demo prices…")
    n = load_seed()
    print(f"  inserted {n} seed rows")
else:
    print(f"Database already has {count_prices()} price rows")
    if not get_meta("source"):
        load_seed()

key = os.getenv("DATA_GOV_API_KEY", "").strip()
if key:
    print("DATA_GOV_API_KEY is set — attempting live Agmarknet fetch…")
    try:
        n = fetch_live()
        print(f"  live fetch inserted {n} new rows")
    except Exception as exc:
        print(f"  live fetch failed ({exc}). Keeping existing / sample data.")
        if count_prices() == 0:
            load_seed()
else:
    print("No DATA_GOV_API_KEY — using SAMPLE demo data.")
    if count_prices() == 0:
        load_seed()
PY

echo
echo "Starting Mandi Saathi at http://127.0.0.1:8000"
exec uvicorn backend.main:app --host 127.0.0.1 --port 8000
