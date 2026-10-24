#!/usr/bin/env python3
"""Delete all seed rows from mandi.db.

Use this when you have loaded live data and want to remove the demo fallback.

Usage:
    python scripts/reset_seed.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend.db import delete_seed_rows, count_prices, init_db


def main() -> None:
    init_db()
    before = count_prices()
    n = delete_seed_rows()
    after = count_prices()
    print(f"Deleted {n} seed rows ({before} → {after} total rows remain).")


if __name__ == "__main__":
    main()
