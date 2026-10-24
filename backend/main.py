"""FastAPI app: JSON APIs plus the static frontend.

Run from the repo root:
    uvicorn backend.main:app --reload --port 8000
"""

from __future__ import annotations

import os
import tempfile
from contextlib import asynccontextmanager
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

# Load .env before importing modules that read OLLAMA_* / DATA_GOV_*.
load_dotenv()

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend import db, explain as explain_mod, geo, netprice, trend as trend_mod
from backend.fetch_prices import SEED_CSV, load_seed
from backend.transcribe import WhisperUnavailable, transcribe_file

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.init_db()
    # Seed geo_cache from state centroids so every district has a fallback immediately
    _seed_geo_cache_from_centroids()
    # So `uvicorn` alone still has something to show if run.sh was skipped.
    if db.count_prices() == 0 and SEED_CSV.exists():
        load_seed()
    yield


def _seed_geo_cache_from_centroids() -> None:
    """Pre-populate geo_cache with state centroids and known district coordinates."""
    import csv
    centroids_path = ROOT / "data" / "state_centroids.csv"
    if centroids_path.exists():
        with centroids_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                state = row["state"].strip()
                cached = db.geo_cache_get(state, state)
                if cached is None:
                    db.geo_cache_put(state, state, float(row["lat"]), float(row["lon"]), "state_centroid")

    try:
        from scripts.fix_geocode import HARDCODED
        for (state, district), (lat, lon) in HARDCODED.items():
            cached = db.geo_cache_get(state, district)
            if cached is None or cached.get("lat") is None:
                db.geo_cache_put(state, district, lat, lon, "curated")
    except Exception:
        pass


app = FastAPI(title="Mandi Saathi", version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _ollama_reachable() -> bool:
    import requests
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    try:
        r = requests.get(f"{host}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


@app.get("/api/health")
def api_health():
    """Health check: db status, row count, data source, Ollama reachability."""
    try:
        count = db.count_prices()
        db_ok = True
        db_error = None
    except Exception as exc:
        count = 0
        db_ok = False
        db_error = str(exc)
    return {
        "db_ok": db_ok,
        "db_error": db_error,
        "price_rows": count,
        "live_rows": db.count_live_prices() if db_ok else 0,
        "markets": db.count_markets() if db_ok else 0,
        "states": db.count_states() if db_ok else 0,
        "data_source": db.get_meta("source", "unknown") if db_ok else "unknown",
        "last_updated": db.get_meta("last_updated") if db_ok else None,
        "ollama_reachable": _ollama_reachable(),
        "ollama_model": os.getenv("OLLAMA_MODEL", "gemma3:4b"),
    }


@app.get("/api/meta")
def api_meta():
    source = db.get_meta("source", "seed")
    last_updated = db.get_meta("last_updated")
    banner = db.get_meta("banner", "sample")
    has_live = db.has_live_data()

    # Check if data is stale (>7 days old)
    newest = db.newest_price_date()
    stale = False
    if newest:
        try:
            newest_d = date.fromisoformat(newest)
            stale = (date.today() - newest_d).days > 7
        except (ValueError, TypeError):
            pass

    markets_count = db.count_markets()
    states_count = db.count_states()

    # Get districts that have geocoordinates (from geo_cache)
    geo_districts = geo.load_coords()

    return {
        "source": source,
        "banner": banner,
        "has_live_data": has_live,
        "last_updated": last_updated,
        "newest_price_date": newest,
        "stale": stale,
        "crops": db.list_crops(),
        "states": db.list_states(),
        "districts": db.list_districts(),
        "coord_districts": geo_districts,
        "markets_count": markets_count,
        "states_count": states_count,
        "default_rate": netprice.DEFAULT_RATE,
        "default_radius_km": netprice.DEFAULT_RADIUS_KM,
        "ollama_model": os.getenv("OLLAMA_MODEL", "gemma3:4b"),
    }


@app.get("/api/mandis")
def api_mandis(
    crop: str | None = None,
    state: str | None = None,
):
    return {"mandis": db.list_mandis(crop=crop, state=state)}


@app.get("/api/best")
def api_best(
    crop: str = Query(..., min_length=1),
    lat: float = Query(...),
    lon: float = Query(...),
    rate: float = Query(netprice.DEFAULT_RATE, gt=0),
    radius: float = Query(netprice.DEFAULT_RADIUS_KM, gt=0),
):
    result = netprice.rank_mandis(crop, lat, lon, rate=rate, radius_km=radius)
    if result["best"]:
        series = db.price_series(crop, result["best"]["market"], days=30)
        trend = trend_mod.compute_trend(series, days=30)
        result["trend"] = trend
        payload = {
            "crop": crop,
            "best": result["best"],
            "runner_up": result.get("runner_up"),
            "difference_rs": result.get("difference_rs"),
            "signal": trend["signal"],
        }
        result["explanation"] = explain_mod.template_explanation(payload, lang="en")
        result["source"] = "template"
        hint_obj = trend.get("hint")
        result["hint"] = hint_obj.get("text") if isinstance(hint_obj, dict) else str(hint_obj or "")
    else:
        result["trend"] = None
        result["explanation"] = None
        result["hint"] = None
    return result


@app.get("/api/trend")
def api_trend(
    crop: str = Query(...),
    market: str = Query(...),
    days: int = Query(30),
    lang: str = Query("en"),
):
    if days not in (7, 30):
        raise HTTPException(status_code=400, detail="days must be 7 or 30")
    series = db.price_series(crop, market, days=days)
    if not series:
        return {
            "crop": crop,
            "market": market,
            "days_requested": days,
            "points": [],
            "series": [],
            "percent_change_7d": None,
            "pct_change": None,
            "signal": "flat",
            "hint": trend_mod.sell_hint("flat", [], lang=lang),
        }
    return {"crop": crop, "market": market, **trend_mod.compute_trend(series, days=days, lang=lang)}


class ExplainIn(BaseModel):
    crop: str
    lat: float
    lon: float
    rate: float = Field(default=netprice.DEFAULT_RATE, gt=0)
    radius: float = Field(default=netprice.DEFAULT_RADIUS_KM, gt=0)
    lang: str = "en"


@app.post("/api/explain")
def api_explain(body: ExplainIn):
    result = netprice.rank_mandis(
        body.crop, body.lat, body.lon, rate=body.rate, radius_km=body.radius
    )
    if not result["best"]:
        nearest = result.get("nearest_state_with_data")
        detail = "No mandis in range for that crop."
        if nearest:
            detail += f" Try expanding radius or looking near {nearest}."
        raise HTTPException(status_code=404, detail=detail)
    series = db.price_series(body.crop, result["best"]["market"], days=30)
    computed_trend = trend_mod.compute_trend(series, days=30, lang=body.lang)
    payload = {
        "crop": body.crop,
        "best": result["best"],
        "runner_up": result["runner_up"],
        "difference_rs": result["difference_rs"],
        "signal": computed_trend["signal"],
    }
    explained = explain_mod.explain(payload, lang=body.lang)
    hint_obj = computed_trend.get("hint")
    hint_str = hint_obj.get("text") if isinstance(hint_obj, dict) else str(hint_obj or "")
    return {
        **explained,
        "explanation": explained.get("text") or explained.get("explanation"),
        "best": result["best"],
        "runner_up": result["runner_up"],
        "difference_rs": result["difference_rs"],
        "signal": computed_trend["signal"],
        "hint": hint_str,
    }


@app.get("/api/geocode")
def api_geocode(
    state: str = Query(...),
    district: str = Query(...),
):
    """Resolve coordinates for a state+district (cached or via Open-Meteo)."""
    try:
        result = geo.resolve_district(state, district, allow_remote=True, remote_budget=[1])
        return result
    except RuntimeError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/transcribe")
async def api_transcribe(
    audio: UploadFile = File(...),
    lang: str | None = None,
):
    suffix = Path(audio.filename or "clip.webm").suffix or ".webm"
    try:
        data = await audio.read()
        if not data:
            raise HTTPException(status_code=400, detail="Empty audio upload")
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(data)
            tmp_path = Path(tmp.name)
        try:
            text = transcribe_file(tmp_path, language=lang)
        finally:
            tmp_path.unlink(missing_ok=True)
    except WhisperUnavailable as exc:
        raise HTTPException(status_code=503, detail=exc.message) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {exc}") from exc
    return {"text": text}


@app.get("/")
def index():
    return FileResponse(FRONTEND / "index.html")


# Static JS/CSS after API routes so /api/* is never swallowed.
app.mount("/static", StaticFiles(directory=str(FRONTEND)), name="static")
