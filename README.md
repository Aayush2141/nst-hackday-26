# Mandi Saathi

A modern, trustworthy mandi price and selling assistant for Indian farmers with **All-India coverage**. Pick a crop and your location (via GPS, state/district dropdowns, or map-click); the app ranks nearby mandis, subtracts estimated transport cost, computes moving average price trends, and explains the best recommendation in 7 Indian languages.

**Code computes every single number** (distance, transport, net price, moving average, trend signals). The local open-source LLM (Ollama) **only explains the numbers it is given**. A strict number-validation check rejects any LLM response containing figures not found in the prompt, falling back cleanly to multi-lingual verified templates (English, Hindi, Marathi, Punjabi, Gujarati, Tamil, Telugu).

---

## Key Features

1. **All-India Coverage**:
   - Covers all 28 Indian States and 8 Union Territories.
   - Dynamic crop list with bilingual labels for popular commodities.
   - Live Agmarknet ingestion via data.gov.in API with full pagination, backoff retries, and column normalisation.
   - Offline sample fallback covering 8 states, 26 markets, and 5 staple crops.

2. **Geocoding & Location Hierarchy**:
   - Fast permanent lookup in SQLite `geo_cache`.
   - On-demand geocoding using the free Open-Meteo Geocoding API (rate-limited, polite, cached).
   - Accurate state centroid fallback (`data/state_centroids.csv`) for every state/UT, clearly flagged as *"≈ Approx. location"* in the UI.
   - Background batch runner: `python -m backend.geocode_missing`.

3. **Smart Net Price & Trend Logic**:
   - `net_price = modal_price − (distance_km × rate_per_quintal_per_km)`.
   - Outlier filter ignores prices that are 0, null, or >5x the median for that crop/day.
   - 7-day and 30-day moving average price charts with min–max price bands.
   - Price trend signals (`rising`, `falling`, `flat`) clearly labeled as *guidance, not a guarantee*.
   - Gain badge highlighting additional earnings versus the nearest mandi.

4. **Modern Agricultural UI**:
   - Clean, accessible design with deep green primary, warm amber accents, and WCAG AA contrast.
   - Dark mode toggle with `localStorage` persistence and `prefers-color-scheme` support.
   - Multi-language switcher supporting English, हिन्दी, मराठी, ਪੰਜਾਬੀ, ગુજરાતી, தமிழ், and తెలుగు.
   - Interactive Leaflet map with colored rank markers and direct route lines.
   - Sortable ranked table with rank medals and one-click CSV download.
   - Speech synthesis (read-aloud in native languages) and voice speech-to-text crop input.
   - Collapsible *"How this was calculated"* breakdown displaying the formula with live numbers.

---

## Architecture & Data Flow

```text
Farmer (browser)
    → Single-page web app (index.html, style.css, app.js)
        → FastAPI backend (/api/health, /api/meta, /api/best, /api/trend, /api/explain, /api/geocode)
            → SQLite database (data/mandi.db: prices, geo_cache, meta)
            → Geo Resolver (geo_cache → Open-Meteo → state_centroids.csv)
            → Core Math (haversine km, net price, moving averages)  ← NUMBERS
            → Ollama / Template Generator (verified subset check)    ← WORDS ONLY
```

---

## Quickstart

### Prerequisites
- Python 3.10+
- (Optional) [Ollama](https://ollama.com) running locally (`ollama run gemma3:4b`)
- (Optional) `DATA_GOV_API_KEY` for live Agmarknet prices

### Running the App

```bash
git clone <repo-url>
cd NST_HACKDAY
chmod +x run.sh
./run.sh
```

Then visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

`run.sh` automatically creates the virtualenv, installs dependencies, verifies the seed data, initializes SQLite, checks for live Agmarknet credentials, and starts the FastAPI server.

### Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Seed all-India demo dataset
python scripts/seed_demo_data.py
python -m backend.fetch_prices --seed

# Populate coordinates cache
python -m backend.geocode_missing

# Start web server
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Running Tests

```bash
source .venv/bin/activate
pytest -v tests/
```

---

## Data Management CLI

`backend.fetch_prices` provides a full-featured CLI to import prices:

```bash
# Fetch all-India prices from data.gov.in (requires DATA_GOV_API_KEY in .env)
python -m backend.fetch_prices --all

# Fetch specific states
python -m backend.fetch_prices --states "Maharashtra,Punjab,Tamil Nadu,West Bengal"

# Fetch specific commodities
python -m backend.fetch_prices --commodities "Onion,Tomato,Potato,Wheat"

# Load a local CSV file
python -m backend.fetch_prices --csv path/to/agmarknet_dump.csv

# Re-load the sample seed dataset
python -m backend.fetch_prices --seed

# Delete all sample seed rows once live data is loaded
python scripts/reset_seed.py
```

---

## Environment Variables

Copy `.env.example` to `.env`:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DATA_GOV_API_KEY` | *(empty)* | Free API key from [data.gov.in](https://data.gov.in). If omitted, the app uses sample seed data. |
| `DATA_GOV_RESOURCE_ID` | `9ef84268-d588-465a-a308-a365eb75a8c0` | Agmarknet daily price resource ID on data.gov.in. |
| `OLLAMA_HOST` | `http://localhost:11434` | Endpoint for local Ollama instance. |
| `OLLAMA_MODEL` | `gemma3:4b` | Model name to use for generating natural-language explanations. |
| `OLLAMA_TIMEOUT` | `45` | Maximum seconds to wait for Ollama before falling back to verified templates. |

---

## API Endpoints

- `GET /api/health`: Health status, price row counts (live vs seed), market and state counts, and Ollama connectivity.
- `GET /api/meta`: Metadata including available crops, states, districts, coordinates, and data freshness flags.
- `GET /api/best`: Ranks mandis for a given crop, latitude, longitude, transport rate, and search radius.
- `GET /api/trend`: 7-day and 30-day price series, moving averages, and trend direction.
- `POST /api/explain`: Generates farmer-facing explanations in the requested language (verified numbers only).
- `GET /api/geocode`: Resolves coordinates for any Indian district/state via cache or Open-Meteo.
- `POST /api/transcribe`: Transcribes spoken crop audio files using `faster-whisper` (optional).

---

## Limitations & Known Constraints

1. **Straight-line Distance**: Distances are computed using the Haversine formula (great-circle distance). Actual road travel distances will typically be 15–30% higher depending on highway topology.
2. **Approximate Locations**: When specific district coordinates have not yet been resolved by Open-Meteo, the system falls back to the official state centroid coordinates, flagged as *"≈ Approx. location"* in the UI.
3. **Flat Transport Rate**: The model uses a user-adjustable flat rate (default ₹2.5 / quintal / km). Actual commercial freight rates vary by truck capacity, terrain, return loads, and road tolls.
4. **Data Reporting Delays**: Agmarknet data relies on APMC mandi secretaries uploading arrival data. Reporting delays can range from a few hours to several days. The UI automatically displays a *"Stale"* badge for records older than 3 days and a banner warning if data exceeds 7 days.
5. **Real vs. Sample Data**: When `DATA_GOV_API_KEY` is not set or Agmarknet is unreachable, the system serves realistic multi-state sample data generated by `scripts/seed_demo_data.py`. The sample banner clearly marks these as demo prices.

---

## Licenses & Credits

| Component | License | Notes |
| --- | --- | --- |
| Mandi Saathi Code | MIT | See `LICENSE` |
| Agmarknet Data | [Government Open Data License — India (GODL)](https://data.gov.in/government-open-data-license-india) | Published by Ministry of Agriculture on data.gov.in |
| Open-Meteo Geocoding API | [CC BY 4.0](https://open-meteo.com/en/terms) | Open-source geocoding API, no key required |
| OpenStreetMap Map Data | [ODbL](https://www.openstreetmap.org/copyright) | Map tiles and geographical context |
| Leaflet.js | BSD-2-Clause | Mobile-friendly interactive maps |
| Chart.js | MIT | Responsive canvas-based charting |
| FastAPI & Uvicorn | MIT / BSD | High-performance Python async backend |
| Gemma 3 / Ollama | [Gemma Terms of Use](https://ai.google.dev/gemma/terms) / MIT | Local AI explanation engine |
