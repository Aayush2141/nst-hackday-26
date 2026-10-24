#!/usr/bin/env python3
"""Generate ~30 days of SAMPLE mandi prices across 8 states for the demo fallback.

This is NOT live Agmarknet data. Each market has a bias, and each crop
follows a random walk plus a small seasonal drift. min <= modal <= max.

Usage (from repo root):
    python scripts/seed_demo_data.py
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "seed_prices.csv"

# 8 states, representative markets across India
MARKETS = [
    # (state, district, market_name, district_bias_pct)
    # Maharashtra
    ("Maharashtra", "Pune", "Pune APMC", 0.04),
    ("Maharashtra", "Nashik", "Nashik APMC", 0.07),
    ("Maharashtra", "Nagpur", "Nagpur APMC", -0.02),
    ("Maharashtra", "Solapur", "Solapur APMC", -0.015),
    ("Maharashtra", "Kolhapur", "Kolhapur APMC", 0.005),
    # Punjab
    ("Punjab", "Amritsar", "Amritsar Grain Market", 0.06),
    ("Punjab", "Ludhiana", "Ludhiana Mandi", 0.04),
    ("Punjab", "Jalandhar", "Jalandhar Mandi", 0.03),
    # Uttar Pradesh
    ("Uttar Pradesh", "Agra", "Agra Mandi", -0.03),
    ("Uttar Pradesh", "Lucknow", "Lucknow Mandi", 0.02),
    ("Uttar Pradesh", "Varanasi", "Varanasi Mandi", -0.01),
    ("Uttar Pradesh", "Kanpur", "Kanpur Mandi", 0.01),
    # West Bengal
    ("West Bengal", "Kolkata", "Kolkata Coochbehar Mkt", 0.05),
    ("West Bengal", "Hooghly", "Hooghly Mandi", 0.03),
    ("West Bengal", "Murshidabad", "Murshidabad Mandi", -0.02),
    # Tamil Nadu
    ("Tamil Nadu", "Chennai", "Koyambedu Market", 0.06),
    ("Tamil Nadu", "Coimbatore", "Coimbatore Mandi", 0.04),
    ("Tamil Nadu", "Madurai", "Madurai Mandi", 0.02),
    # Madhya Pradesh
    ("Madhya Pradesh", "Indore", "Indore Krishi Mandi", 0.03),
    ("Madhya Pradesh", "Bhopal", "Bhopal Karond Mandi", 0.02),
    ("Madhya Pradesh", "Ujjain", "Ujjain Mandi", -0.01),
    # Rajasthan
    ("Rajasthan", "Jaipur", "Jaipur Muhana Mandi", 0.03),
    ("Rajasthan", "Jodhpur", "Jodhpur Mandi", -0.02),
    # Gujarat
    ("Gujarat", "Ahmedabad", "Ahmedabad Mandi", 0.04),
    ("Gujarat", "Surat", "Surat Veg Market", 0.05),
    ("Gujarat", "Rajkot", "Rajkot Mandi", 0.02),
]

# Typical modal prices in Rs per quintal (illustrative, not live quotes)
CROPS = {
    "Onion": 1800,
    "Tomato": 1400,
    "Wheat": 2550,
    "Potato": 1250,
    "Soybean": 4300,
}

DAYS = 30


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def generate(today: date | None = None) -> list[dict]:
    today = today or date.today()
    rng = random.Random(42)  # reproducible demo file
    rows: list[dict] = []

    for crop, base in CROPS.items():
        for state, district, market, bias_pct in MARKETS:
            # Skip crops that don't make geographic sense (rough heuristic)
            if crop == "Soybean" and state in ("Tamil Nadu", "West Bengal"):
                continue
            if crop == "Wheat" and state == "Tamil Nadu":
                continue

            modal = float(base * (1.0 + bias_pct))
            for day_offset in range(DAYS - 1, -1, -1):
                d = today - timedelta(days=day_offset)
                # Daily random walk plus a tiny upward seasonal drift (~2% / month)
                shock = rng.uniform(-0.025, 0.025)
                modal = clamp(
                    modal * (1.0 + shock) + (base * 0.0007),
                    base * 0.55,
                    base * 1.55,
                )
                spread = rng.uniform(0.04, 0.09)
                min_p = round(modal * (1.0 - spread), 2)
                max_p = round(modal * (1.0 + spread), 2)
                modal_r = round(modal, 2)
                if min_p > modal_r:
                    min_p = modal_r
                if max_p < modal_r:
                    max_p = modal_r
                rows.append(
                    {
                        "state": state,
                        "district": district,
                        "market": market,
                        "commodity": crop,
                        "variety": "FAQ",
                        "arrival_date": d.isoformat(),
                        "min_price": min_p,
                        "max_price": max_p,
                        "modal_price": modal_r,
                    }
                )
    return rows


def main() -> None:
    rows = generate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "state", "district", "market", "commodity", "variety",
                "arrival_date", "min_price", "max_price", "modal_price",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} sample rows to {OUT}")
    # Report coverage
    states = {r["state"] for r in rows}
    crops = {r["commodity"] for r in rows}
    print(f"  States: {len(states)}: {', '.join(sorted(states))}")
    print(f"  Crops: {len(crops)}: {', '.join(sorted(crops))}")


if __name__ == "__main__":
    main()
