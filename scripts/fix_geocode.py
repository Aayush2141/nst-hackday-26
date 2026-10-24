#!/usr/bin/env python3
"""Re-geocode all 'geocode_failed' districts using curated fallback coordinates.

Hardcoded WGS-84 coordinates sourced from Wikipedia / Census of India.
Run from repo root:
    .venv/bin/python3 scripts/fix_geocode.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from backend import db  # noqa: E402

# Curated fallback coordinates for districts that Open-Meteo couldn't resolve.
# Format: (state, district) → (lat, lon)
HARDCODED: dict[tuple[str, str], tuple[float, float]] = {
    # ── Andaman & Nicobar ──
    ("Andaman and Nicobar Islands", "North And Middle Andaman"): (12.5685, 92.8426),

    # ── Andhra Pradesh (new districts post-2022 reorganisation) ──
    ("Andhra Pradesh", "Alluri Sitharama Raju"): (18.4833, 82.8667),
    ("Andhra Pradesh", "Anakapally"): (17.6912, 83.0041),
    ("Andhra Pradesh", "Ananthapuramu"): (14.6819, 77.6006),   # = Anantapur
    ("Andhra Pradesh", "Annamayya"): (13.8200, 78.7000),
    ("Andhra Pradesh", "Chittor"): (13.2172, 79.0999),          # = Chittoor
    ("Andhra Pradesh", "Dr.b.r.a.konaseema"): (16.9167, 82.2333),
    ("Andhra Pradesh", "East Godavari"): (17.3273, 81.8282),
    ("Andhra Pradesh", "Ntr"): (16.5193, 80.6305),              # NTR = Krishna
    ("Andhra Pradesh", "Palnadu"): (16.2833, 79.6500),
    ("Andhra Pradesh", "Parvathipuram Manyam"): (18.7833, 83.4333),
    ("Andhra Pradesh", "Prakasam"): (15.3369, 79.5660),
    ("Andhra Pradesh", "Spsr Nellore"): (14.4426, 79.9865),
    ("Andhra Pradesh", "Vijayanagaram"): (18.1067, 83.3956),
    ("Andhra Pradesh", "Ysr Kadapa"): (14.4674, 78.8241),

    # ── Assam ──
    ("Assam", "Kamrup"): (26.1433, 91.7362),

    # ── Bihar ──
    ("Bihar", "East Champaran/ Motihari"): (26.6566, 84.9192),
    ("Bihar", "Kaimur/bhabhua"): (25.0426, 83.6005),
    ("Bihar", "Nalanda"): (25.0000, 85.5000),

    # ── Chhattisgarh (newly created districts) ──
    ("Chhattisgarh", "Balodabazar"): (21.6530, 82.1520),
    ("Chhattisgarh", "Kabirdham"): (22.0833, 81.2667),
    ("Chhattisgarh", "Khairagarh Chhuikhadan Gandai"): (21.4167, 80.9833),
    ("Chhattisgarh", "Koriya"): (23.2000, 82.6667),
    ("Chhattisgarh", "Manendragarh Chirmiri Bhartpur"): (23.2000, 82.2000),
    ("Chhattisgarh", "Sarangarh Bilaigarh"): (21.5833, 83.0833),

    # ── Goa ──
    ("Goa", "North Goa"): (15.5387, 73.9102),

    # ── Gujarat (renamed / alternate spellings) ──
    ("Gujarat", "Banaskanth"): (24.1700, 72.4200),   # = Banaskantha
    ("Gujarat", "Chhota Udaipur"): (22.3072, 74.0143),
    ("Gujarat", "Dahod"): (22.8350, 74.2541),
    ("Gujarat", "Gir Somnath"): (20.9056, 70.3844),
    ("Gujarat", "Junagarh"): (21.5222, 70.4579),     # = Junagadh
    ("Gujarat", "Kachchh"): (23.7337, 69.8597),      # = Kutch
    ("Gujarat", "Morbi"): (22.8173, 70.8379),
    ("Gujarat", "Narmada"): (21.8741, 73.7878),
    ("Gujarat", "Panchmahals"): (22.7685, 73.5993),  # Godhra area
    ("Gujarat", "Sabarkantha"): (23.5804, 72.9769),
    ("Gujarat", "Vadodara(baroda)"): (22.3072, 73.1812),

    # ── Haryana ──
    ("Haryana", "Gurgaon"): (28.4595, 77.0266),
    ("Haryana", "Jhajar"): (28.6050, 76.6500),

    # ── Punjab ──
    ("Punjab", "Bhatinda"): (30.2071, 74.9455),      # = Bathinda
    ("Punjab", "Ferozpur"): (30.9255, 74.6175),      # = Firozpur
    ("Punjab", "Tarntaran"): (31.4518, 74.9268),     # = Tarn Taran
}


def main() -> None:
    db.init_db()
    conn = db.get_conn()

    failed = conn.execute(
        "SELECT state, district FROM geo_cache WHERE lat IS NULL"
    ).fetchall()
    conn.close()

    fixed = 0
    still_failed = 0
    for row in failed:
        state, district = row["state"], row["district"]
        key = (state, district)
        if key in HARDCODED:
            lat, lon = HARDCODED[key]
            db.geo_cache_put(state, district, lat, lon, "open_meteo")
            print(f"  ✓ Fixed: {district}, {state}  ({lat:.4f}, {lon:.4f})")
            fixed += 1
        else:
            print(f"  ✗ No hardcoded entry for: {district}, {state}")
            still_failed += 1

    print(f"\nDone — fixed {fixed}, still missing {still_failed}")


if __name__ == "__main__":
    main()
