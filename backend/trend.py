"""Price trend: moving average, percent change, and a simple signal.

Signal rules (computed in code, never by the LLM):
  rising  — 7-day percent change >= +3%
  falling — 7-day percent change <= -3%
  flat    — otherwise

The sell-now / wait hint is labelled as guidance, not a prediction.
"""

from __future__ import annotations

from typing import Optional


def moving_average(values: list[float], window: int = 7) -> list[Optional[float]]:
    """Simple moving average. Early days use a shorter window so the chart is full."""
    out: list[Optional[float]] = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        chunk = values[start : i + 1]
        out.append(round(sum(chunk) / len(chunk), 2))
    return out


def percent_change_over_days(values: list[float], days: int = 7) -> Optional[float]:
    """(last - value `days` ago) / value_days_ago * 100. None if not enough data."""
    if len(values) < 2:
        return None
    old_index = max(0, len(values) - 1 - days)
    old = values[old_index]
    new = values[-1]
    if old == 0:
        return None
    return round((new - old) / old * 100.0, 2)


def signal_from_change(pct: Optional[float], threshold: float = 3.0) -> str:
    if pct is None:
        return "flat"
    if pct >= threshold:
        return "rising"
    if pct <= -threshold:
        return "falling"
    return "flat"


def sell_hint(signal: str, values: list[float], lang: str = "en") -> dict:
    """Compare the latest price to the recent high/low. Guidance only."""
    if not values:
        code = "watch"
    elif len(values) < 2:
        code = "not_enough_history"
    else:
        window = values[-7:] if len(values) >= 7 else values
        last = values[-1]
        recent_high = max(window)
        recent_low = min(window)
        near_high = last >= recent_high * 0.98
        near_low = last <= recent_low * 1.02
        if signal == "rising" and near_high:
            code = "sell_now"
        elif signal == "falling" and near_low:
            code = "wait"
        elif signal == "falling":
            code = "wait"
        elif signal == "rising":
            code = "sell_now"
        else:
            code = "watch"

    texts = {
        "en": {
            "not_enough_history": "Guidance: Not enough history yet, trends and moving averages will accumulate over daily fetches. Today's reported price shown.",
            "sell_now": "Guidance (not a prediction): the 7-day trend is rising, so selling now locks in the current net price.",
            "wait": "Guidance (not a prediction): the 7-day trend is falling; waiting a few days may or may not help — watch the next arrivals.",
            "watch": "Guidance (not a prediction): the 7-day trend is flat, so there is no strong timing signal from this data.",
        },
        "hi": {
            "not_enough_history": "मार्गदर्शन: अभी पर्याप्त इतिहास नहीं है; दैनिक डेटा आने पर रुझान दिखाई देंगे। आज का भाव दिखाया गया है।",
            "sell_now": "मार्गदर्शन (भविष्यवाणी नहीं): 7 दिन की प्रवृत्ति बढ़ रही है, इसलिए अभी बेचने से मौजूदा नेट भाव मिल सकता है।",
            "wait": "मार्गदर्शन (भविष्यवाणी नहीं): 7 दिन की प्रवृत्ति गिर रही है; कुछ दिन रुकना फायदा दे भी सकता है और नहीं भी — अगली आवक देखें।",
            "watch": "मार्गदर्शन (भविष्यवाणी नहीं): 7 दिन की प्रवृत्ति स्थिर है, इसलिए इस आँकड़े से मजबूत समय का संकेत नहीं मिलता।",
        },
    }
    lang_key = "hi" if lang.startswith("hi") else "en"
    return {
        "code": code,
        "label": "guidance_not_prediction",
        "text": texts[lang_key][code],
        "text_en": texts["en"][code],
        "text_hi": texts["hi"][code],
    }


def compute_trend(series: list[dict], days: int = 30, lang: str = "en") -> dict:
    """`series` is a list of {arrival_date, modal_price} oldest-first."""
    values = [float(p["modal_price"]) for p in series]
    dates = [p["arrival_date"] for p in series]
    ma = moving_average(values, window=7)
    pct = percent_change_over_days(values, days=7)
    signal = signal_from_change(pct)
    hint = sell_hint(signal, values, lang=lang)
    points = [
        {
            "date": d,
            "modal_price": v,
            "ma7": m,
            "min_price": float(p.get("min_price", v) or v),
            "max_price": float(p.get("max_price", v) or v),
        }
        for d, v, m, p in zip(dates, values, ma, series)
    ]
    return {
        "days_requested": days,
        "points": points,
        "series": points,
        "percent_change_7d": pct,
        "pct_change": pct,
        "signal": signal,
        "hint": hint,
    }

