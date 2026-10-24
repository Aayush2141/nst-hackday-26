"""Unit tests for distance, net price, trend signals, geocoding, outliers, and LLM number checks."""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.explain import numbers_are_subset, template_explanation
from backend.geo import haversine_km, _load_state_centroids
from backend.netprice import rank_from_rows, _days_old
from backend.outliers import filter_outliers
from backend.trend import compute_trend, percent_change_over_days, signal_from_change


# ─── Haversine Tests ────────────────────────────────────────────────────

def test_haversine_zero():
    assert haversine_km(18.52, 73.85, 18.52, 73.85) == 0


def test_haversine_pune_mumbai_sane():
    # Pune to Mumbai is roughly 120 km as the crow flies.
    km = haversine_km(18.5204, 73.8567, 19.0760, 72.8777)
    assert 100 < km < 160


def test_haversine_symmetric():
    a = haversine_km(21.14, 79.08, 18.52, 73.85)
    b = haversine_km(18.52, 73.85, 21.14, 79.08)
    assert abs(a - b) < 1e-9


def test_haversine_delhi_kolkata():
    # Delhi to Kolkata is roughly 1300 km
    km = haversine_km(28.70, 77.10, 22.57, 88.36)
    assert 1200 < km < 1500


# ─── Net Price Tests ─────────────────────────────────────────────────────

def test_net_price_math_and_order():
    # Two mandis 10 km and 100 km from origin. Same modal => nearer wins.
    origin_lat, origin_lon = 18.52, 73.85
    coords = {
        "Near": {"lat": 18.52, "lon": 73.94},  # ~9.5 km east
        "Far": {"lat": 19.4, "lon": 73.85},    # ~98 km north
    }

    def lookup(district):
        return coords[district]

    rows = [
        {"market": "Far APMC", "district": "Far", "modal_price": 2000, "arrival_date": "2026-10-24"},
        {"market": "Near APMC", "district": "Near", "modal_price": 2000, "arrival_date": "2026-10-24"},
    ]
    ranked = rank_from_rows(rows, origin_lat, origin_lon, rate=2.5, radius_km=300, coords_lookup=lookup)
    assert len(ranked) == 2
    near = next(r for r in ranked if r["market"] == "Near APMC")
    expected_transport = round(near["distance_km"] * 2.5, 2)
    assert near["transport_cost"] == expected_transport
    assert near["net_price"] == round(2000 - expected_transport, 2)
    assert ranked[0]["market"] == "Near APMC"
    assert ranked[0]["net_price"] > ranked[1]["net_price"]


def test_net_price_radius_filter():
    origin_lat, origin_lon = 18.52, 73.85
    coords = {"Near": {"lat": 18.52, "lon": 73.94}, "Far": {"lat": 21.14, "lon": 79.08}}

    def lookup(district):
        return coords[district]

    rows = [
        {"market": "Near APMC", "district": "Near", "modal_price": 1000},
        {"market": "Far APMC", "district": "Far", "modal_price": 9000},
    ]
    ranked = rank_from_rows(rows, origin_lat, origin_lon, rate=2.5, radius_km=50, coords_lookup=lookup)
    assert [r["market"] for r in ranked] == ["Near APMC"]


def test_days_old_today():
    today = date.today().isoformat()
    assert _days_old(today) == 0


def test_days_old_three_days():
    three_ago = (date.today() - timedelta(days=3)).isoformat()
    assert _days_old(three_ago) == 3


# ─── All-India Filtering Tests ───────────────────────────────────────────

def test_all_india_filtering_by_radius():
    """Markets in Punjab should be filtered out when user is in Tamil Nadu (>1000km)."""
    # Chennai approx location
    origin_lat, origin_lon = 13.08, 80.27
    coords = {
        "Amritsar": {"lat": 31.63, "lon": 74.87},  # ~2200 km from Chennai
        "Coimbatore": {"lat": 11.02, "lon": 76.97},  # ~490 km from Chennai
    }

    def lookup(district):
        return coords[district]

    rows = [
        {"market": "Amritsar Mandi", "district": "Amritsar", "modal_price": 2500},
        {"market": "Coimbatore Mandi", "district": "Coimbatore", "modal_price": 1800},
    ]
    # With 500 km radius: only Coimbatore should appear
    ranked = rank_from_rows(rows, origin_lat, origin_lon, rate=2.5, radius_km=500, coords_lookup=lookup)
    names = [r["market"] for r in ranked]
    assert "Amritsar Mandi" not in names
    assert "Coimbatore Mandi" in names


def test_all_india_filtering_large_radius():
    """With 1500 km radius from central India, most markets should be reachable."""
    # Bhopal approx
    origin_lat, origin_lon = 23.26, 77.41
    coords = {
        "Amritsar": {"lat": 31.63, "lon": 74.87},
        "Chennai": {"lat": 13.08, "lon": 80.27},
        "Kolkata": {"lat": 22.57, "lon": 88.36},
    }

    def lookup(district):
        return coords[district]

    rows = [
        {"market": "Amritsar Mandi", "district": "Amritsar", "modal_price": 2500},
        {"market": "Chennai Market", "district": "Chennai", "modal_price": 1800},
        {"market": "Kolkata Market", "district": "Kolkata", "modal_price": 2000},
    ]
    ranked = rank_from_rows(rows, origin_lat, origin_lon, rate=2.5, radius_km=1500, coords_lookup=lookup)
    assert len(ranked) == 3


# ─── Outlier Filter Tests ────────────────────────────────────────────────

def test_outlier_removes_zero():
    rows = [
        {"modal_price": 0, "arrival_date": "2026-10-01"},
        {"modal_price": 1500, "arrival_date": "2026-10-01"},
        {"modal_price": 1600, "arrival_date": "2026-10-01"},
    ]
    kept = filter_outliers(rows)
    prices = [r["modal_price"] for r in kept]
    assert 0 not in prices


def test_outlier_removes_5x_median():
    rows = [
        {"modal_price": 1500, "arrival_date": "2026-10-01"},
        {"modal_price": 1600, "arrival_date": "2026-10-01"},
        {"modal_price": 1550, "arrival_date": "2026-10-01"},
        {"modal_price": 50000, "arrival_date": "2026-10-01"},  # >5x median ~= 1550
    ]
    kept = filter_outliers(rows)
    prices = [r["modal_price"] for r in kept]
    assert 50000 not in prices
    assert len(kept) == 3


def test_outlier_keeps_reasonable_prices():
    rows = [
        {"modal_price": 1400, "arrival_date": "2026-10-01"},
        {"modal_price": 1500, "arrival_date": "2026-10-01"},
        {"modal_price": 1600, "arrival_date": "2026-10-01"},
        {"modal_price": 1700, "arrival_date": "2026-10-01"},
    ]
    kept = filter_outliers(rows)
    assert len(kept) == 4


# ─── Geocode Cache Fallback Order ────────────────────────────────────────

def test_state_centroids_loaded():
    """State centroids CSV should load and cover all major states."""
    centroids = _load_state_centroids()
    required = ["maharashtra", "punjab", "tamil nadu", "west bengal", "uttar pradesh"]
    for state in required:
        assert state in centroids, f"Missing state centroid: {state}"


def test_state_centroids_valid_coords():
    """All centroid lat/lon should be within India's rough bounding box."""
    centroids = _load_state_centroids()
    for state, data in centroids.items():
        lat, lon = data["lat"], data["lon"]
        assert 6 < lat < 38, f"{state}: lat {lat} out of range"
        assert 68 < lon < 98, f"{state}: lon {lon} out of range"


# ─── Stale Detection Tests ────────────────────────────────────────────────

def test_stale_detection_fresh():
    from backend.netprice import _days_old, STALE_DAYS
    today = date.today().isoformat()
    assert _days_old(today) <= STALE_DAYS  # today is not stale


def test_stale_detection_old():
    from backend.netprice import _days_old, STALE_DAYS
    old = (date.today() - timedelta(days=10)).isoformat()
    assert _days_old(old) > STALE_DAYS  # 10 days old is stale


# ─── Trend Tests ─────────────────────────────────────────────────────────

def test_trend_rising():
    values = [100, 102, 104, 106, 108, 110, 112, 120]
    pct = percent_change_over_days(values, days=7)
    assert pct is not None and pct >= 3
    assert signal_from_change(pct) == "rising"


def test_trend_falling():
    values = [120, 118, 116, 114, 112, 110, 108, 100]
    pct = percent_change_over_days(values, days=7)
    assert pct is not None and pct <= -3
    assert signal_from_change(pct) == "falling"


def test_trend_flat():
    values = [100, 101, 100, 102, 101, 100, 101, 102]
    pct = percent_change_over_days(values, days=7)
    assert signal_from_change(pct) == "flat"


def test_compute_trend_includes_ma_and_guidance_label():
    series = [{"arrival_date": f"2026-10-{i:02d}", "modal_price": 100 + i} for i in range(1, 11)]
    out = compute_trend(series, days=30)
    assert out["signal"] in {"rising", "falling", "flat"}
    assert len(out["points"]) == 10
    assert out["points"][-1]["ma7"] is not None
    assert out["hint"]["label"] == "guidance_not_prediction"


# ─── LLM Number Validation Tests ─────────────────────────────────────────

def test_explain_rejects_invented_number():
    prompt = "best_net_price_rs_per_quintal=1500 difference_vs_runner_up_rs=40"
    bad = "Sell at 1500, you might get 999 extra next week."
    good = "The best net price is 1500, which is 40 more than the runner-up."
    assert numbers_are_subset(good, prompt) is True
    assert numbers_are_subset(bad, prompt) is False


def test_template_uses_only_given_numbers():
    payload = {
        "crop": "Onion",
        "best": {
            "market": "Nashik APMC",
            "net_price": 1710.5,
            "modal_price": 1800,
            "transport_cost": 89.5,
            "distance_km": 35.8,
        },
        "runner_up": {"market": "Pune APMC", "net_price": 1680},
        "difference_rs": 30.5,
        "signal": "rising",
    }
    from backend.explain import extract_numbers
    for language in ("en", "hi", "mr", "pa", "gu", "ta", "te"):
        text = template_explanation(payload, language)
        allowed = {
            "1710.5", "1800", "89.5", "35.8", "30.5",
            "7",  # "7-day trend" in templates
            "1680",  # runner_up net price
        }
        for num in extract_numbers(text):
            assert num in allowed, f"lang={language}: unexpected number {num} in: {text}"


def test_explain_falls_back_when_ollama_is_down(monkeypatch):
    from backend.explain import explain

    monkeypatch.setenv("OLLAMA_HOST", "http://127.0.0.1:1")
    monkeypatch.setenv("OLLAMA_TIMEOUT", "0.2")
    payload = {
        "crop": "Onion",
        "best": {
            "market": "Nashik APMC",
            "net_price": 1710.5,
            "modal_price": 1800,
            "transport_cost": 89.5,
            "distance_km": 35.8,
        },
        "runner_up": {"market": "Pune APMC", "net_price": 1680},
        "difference_rs": 30.5,
        "signal": "rising",
    }
    out = explain(payload, lang="en")
    assert out["source"] == "template"
    assert "1710.5" in out["text"]
    assert "Nashik APMC" in out["text"]


def test_explain_multi_language_templates():
    """All language templates should produce non-empty output."""
    from backend.explain import template_explanation
    payload = {
        "crop": "Wheat",
        "best": {
            "market": "Ludhiana Mandi",
            "net_price": 2400.0,
            "modal_price": 2550.0,
            "transport_cost": 150.0,
            "distance_km": 60.0,
        },
        "runner_up": {"market": "Amritsar Mandi", "net_price": 2350.0},
        "difference_rs": 50.0,
        "signal": "flat",
    }
    for lang in ("en", "hi", "mr", "pa", "gu", "ta", "te"):
        text = template_explanation(payload, lang)
        assert len(text) > 20, f"Template for lang={lang} too short: {text!r}"
        assert "2400" in text or "2400.0" in text, f"Missing net_price in lang={lang}"
