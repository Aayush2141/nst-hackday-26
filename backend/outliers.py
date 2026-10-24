"""Drop impossible mandi prices before ranking.

A row is dropped when modal_price is missing, zero, or more than
`factor` times the median modal price for that crop and day.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import median
from typing import Optional


def filter_outliers(
    rows: list[dict],
    price_key: str = "modal_price",
    date_key: str = "arrival_date",
    factor: float = 5.0,
) -> list[dict]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        price = _as_price(row.get(price_key))
        if price is None or price <= 0:
            continue
        grouped[str(row.get(date_key) or "_")].append(price)

    medians = {day: median(vals) for day, vals in grouped.items() if vals}
    kept: list[dict] = []
    for row in rows:
        price = _as_price(row.get(price_key))
        if price is None or price <= 0:
            continue
        day = str(row.get(date_key) or "_")
        med = medians.get(day)
        if med is None or med <= 0:
            continue
        if price > factor * med:
            continue
        kept.append(row)
    return kept


def _as_price(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
