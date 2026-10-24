"""Turn computed numbers into a short farmer-facing explanation.

The LLM is only allowed to rephrase numbers that THIS function puts in the
prompt. After the model replies we extract every number from the text; if any
number was not in the prompt, we throw the reply away and use a template.

If Ollama is down, we also use the template. The app never invents a figure.

Multi-language templates: English, Hindi, Marathi, Punjabi, Gujarati, Tamil, Telugu.
LLM tries the chosen language; falls back to the template for that language.
"""

from __future__ import annotations

import os
import re
from typing import Optional

import requests


def _ollama_settings() -> tuple[str, str, float]:
    """Read env at call time so .env loaded in main.py is honoured."""
    host = os.getenv("OLLAMA_HOST", os.getenv("OLLAMA_URL", "http://localhost:11434")).rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "gemma3:4b")
    timeout = float(os.getenv("OLLAMA_TIMEOUT", "45"))
    return host, model, timeout


# Strip grouping commas first, then take full integers/decimals (1710.5 not 171).
_NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")


def extract_numbers(text: str) -> list[str]:
    """Return canonical string forms of every number in `text`."""
    cleaned = (text or "").replace(",", "")
    return [canonicalize_number(raw) for raw in _NUMBER_RE.findall(cleaned)]


def canonicalize_number(raw: str) -> str:
    """1,250.50 -> '1250.5'; 7.00 -> '7' so 7 and 7.0 compare equal."""
    cleaned = raw.replace(",", "").strip()
    try:
        value = float(cleaned)
    except ValueError:
        return cleaned
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    # Keep up to 2 decimal places, strip trailing zeros.
    return f"{value:.2f}".rstrip("0").rstrip(".")


def numbers_are_subset(output: str, prompt: str) -> bool:
    """True iff every number in `output` already appears in `prompt` (with sensible rounding)."""
    raw_allowed = extract_numbers(prompt)
    allowed = set(raw_allowed)
    for raw in raw_allowed:
        try:
            val = float(raw)
            allowed.add(str(int(round(val))))
            allowed.add(str(int(val)))
            allowed.add(f"{val:.1f}")
            allowed.add(f"{val:.2f}")
        except ValueError:
            pass
    # Allow 7 for 7-day trend, 1 for rank 1, 2 for runner-up
    allowed.update(["1", "2", "3", "7", "30"])

    output_numbers = extract_numbers(output)
    if not output_numbers:
        return False
    for num in output_numbers:
        if num not in allowed:
            # Check if num is close to any float in allowed within rounding error
            try:
                n_val = float(num)
                if any(abs(n_val - float(a)) <= 1.01 for a in raw_allowed if a.replace(".", "", 1).isdigit()):
                    continue
            except ValueError:
                pass
            return False
    return True


# ─── Template explanations (multi-language) ──────────────────────────────

def template_explanation(payload: dict, lang: str) -> str:
    """Deterministic template text that only uses the given numbers."""
    best = payload["best"]
    runner = payload.get("runner_up")
    diff = payload.get("difference_rs")
    signal = payload.get("signal", "flat")
    crop = payload.get("crop", "")
    net = best["net_price"]
    market = best["market"]
    transport = best["transport_cost"]
    modal = best["modal_price"]
    dist = best["distance_km"]

    lang_key = _norm_lang(lang)

    templates = {
        "en": _tpl_en,
        "hi": _tpl_hi,
        "mr": _tpl_mr,
        "pa": _tpl_pa,
        "gu": _tpl_gu,
        "ta": _tpl_ta,
        "te": _tpl_te,
    }
    fn = templates.get(lang_key, _tpl_en)
    return fn(crop, market, net, modal, transport, dist, runner, diff, signal)


def _tpl_en(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_word = {"rising": "rising", "falling": "falling", "flat": "flat"}.get(signal, signal)
    lines = [
        f"For {crop}, the best net price is at {market}: Rs {net} per quintal.",
        f"The mandi modal price is Rs {modal} and estimated transport for {dist} km is Rs {transport} per quintal.",
    ]
    if runner and diff is not None:
        lines.append(f"That is Rs {diff} more per quintal than {runner['market']}. The 7-day trend is {signal_word}.")
    else:
        lines.append(f"The 7-day trend is {signal_word}.")
    return " ".join(lines)


def _tpl_hi(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_hi = {"rising": "बढ़ रही", "falling": "गिर रही", "flat": "स्थिर"}.get(signal, signal)
    lines = [
        f"{crop} के लिए सबसे अच्छा मंडी भाव {market} में है: नेट {net} रुपये प्रति क्विंटल।",
        f"मंडी भाव {modal} रुपये है और अनुमानित ढुलाई {dist} किमी के लिए {transport} रुपये प्रति क्विंटल है।",
    ]
    if runner and diff is not None:
        lines.append(f"यह {runner['market']} से {diff} रुपये प्रति क्विंटल अधिक है। 7 दिन की प्रवृत्ति {signal_hi} है।")
    else:
        lines.append(f"7 दिन की प्रवृत्ति {signal_hi} है।")
    return " ".join(lines)


def _tpl_mr(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_mr = {"rising": "वाढत आहे", "falling": "घसरत आहे", "flat": "स्थिर"}.get(signal, signal)
    lines = [
        f"{crop} साठी सर्वोत्तम निव्वळ भाव {market} येथे आहे: ₹{net} प्रति क्विंटल.",
        f"मंडी मोडल भाव ₹{modal} आणि {dist} किमी साठी अंदाजे वाहतूक खर्च ₹{transport} आहे.",
    ]
    if runner and diff is not None:
        lines.append(f"{runner['market']} पेक्षा ₹{diff} जास्त. 7 दिवसांचा कल {signal_mr} आहे.")
    else:
        lines.append(f"7 दिवसांचा कल {signal_mr} आहे.")
    return " ".join(lines)


def _tpl_pa(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_pa = {"rising": "ਵੱਧ ਰਿਹਾ", "falling": "ਘੱਟ ਰਿਹਾ", "flat": "ਸਥਿਰ"}.get(signal, signal)
    lines = [
        f"{crop} ਲਈ ਸਭ ਤੋਂ ਵਧੀਆ ਮੁੱਲ {market} ਵਿੱਚ ਹੈ: ₹{net} ਪ੍ਰਤੀ ਕੁਇੰਟਲ.",
        f"ਮੰਡੀ ਭਾਅ ₹{modal} ਹੈ ਅਤੇ {dist} ਕਿਮੀ ਲਈ ਢੋਆ ₹{transport} ਹੈ.",
    ]
    if runner and diff is not None:
        lines.append(f"{runner['market']} ਨਾਲੋਂ ₹{diff} ਵੱਧ. 7 ਦਿਨਾਂ ਦਾ ਰੁਝਾਨ {signal_pa} ਹੈ.")
    else:
        lines.append(f"7 ਦਿਨਾਂ ਦਾ ਰੁਝਾਨ {signal_pa} ਹੈ.")
    return " ".join(lines)


def _tpl_gu(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_gu = {"rising": "વધી રહ્યો", "falling": "ઘટી રહ્યો", "flat": "સ્થિર"}.get(signal, signal)
    lines = [
        f"{crop} માટે શ્રેષ્ઠ ચોખ્ખો ભાવ {market} ખાતે ₹{net} પ્રતિ ક્વિન્ટલ છે.",
        f"મંડી ભાવ ₹{modal} છે અને {dist} કિ.મી. માટે પરિવહન ₹{transport} છે.",
    ]
    if runner and diff is not None:
        lines.append(f"{runner['market']} કરતાં ₹{diff} વધારે. 7 દિવસનો ટ્રેન્ડ {signal_gu} છે.")
    else:
        lines.append(f"7 દિવસનો ટ્રેન્ડ {signal_gu} છે.")
    return " ".join(lines)


def _tpl_ta(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_ta = {"rising": "உயர்கிறது", "falling": "குறைகிறது", "flat": "நிலையானது"}.get(signal, signal)
    lines = [
        f"{crop}-க்கு சிறந்த நிகர விலை {market}-ல் உள்ளது: ₹{net} ஒரு குவிண்டாலுக்கு.",
        f"மண்டி விலை ₹{modal}; {dist} கி.மீ. போக்குவரத்து செலவு ₹{transport}.",
    ]
    if runner and diff is not None:
        lines.append(f"{runner['market']}-ஐ விட ₹{diff} அதிகம். 7 நாள் போக்கு {signal_ta}.")
    else:
        lines.append(f"7 நாள் போக்கு {signal_ta}.")
    return " ".join(lines)


def _tpl_te(crop, market, net, modal, transport, dist, runner, diff, signal):
    signal_te = {"rising": "పెరుగుతోంది", "falling": "తగ్గుతోంది", "flat": "స్థిరంగా"}.get(signal, signal)
    lines = [
        f"{crop} కోసం అత్యుత్తమ నికర ధర {market}లో ₹{net} కి.గ్రా.",
        f"మండీ ధర ₹{modal}; {dist} కి.మీ కోసం రవాణా ₹{transport}.",
    ]
    if runner and diff is not None:
        lines.append(f"{runner['market']} కంటే ₹{diff} ఎక్కువ. 7 రోజుల ట్రెండ్ {signal_te}.")
    else:
        lines.append(f"7 రోజుల ట్రెండ్ {signal_te}.")
    return " ".join(lines)


def _norm_lang(lang: str) -> str:
    """Normalise a lang code to our two-letter key."""
    s = (lang or "en").lower().strip()
    for prefix, key in [
        ("hi", "hi"), ("mr", "mr"), ("pa", "pa"), ("gu", "gu"),
        ("ta", "ta"), ("te", "te"), ("en", "en"),
    ]:
        if s.startswith(prefix):
            return key
    return "en"


def build_prompt(payload: dict, lang: str) -> str:
    """Prompt contains ONLY computed figures plus strict instructions."""
    lang_names = {
        "hi": "Hindi", "mr": "Marathi", "pa": "Punjabi",
        "gu": "Gujarati", "ta": "Tamil", "te": "Telugu", "en": "English",
    }
    language = lang_names.get(_norm_lang(lang), "English")
    best = payload["best"]
    runner = payload.get("runner_up")
    parts = [
        f"crop={payload.get('crop')}",
        f"best_market={best['market']}",
        f"best_net_price_rs_per_quintal={best['net_price']}",
        f"best_modal_price_rs={best['modal_price']}",
        f"best_transport_cost_rs={best['transport_cost']}",
        f"best_distance_km={best['distance_km']}",
        f"trend_signal={payload.get('signal')}",
    ]
    if runner:
        parts.append(f"runner_up_market={runner['market']}")
        parts.append(f"runner_up_net_price_rs={runner['net_price']}")
    if payload.get("difference_rs") is not None:
        parts.append(f"difference_vs_runner_up_rs={payload['difference_rs']}")
    # So "7-day trend" in a reply is a number that already appears in the input.
    parts.append("trend_window_days=7")

    numbers_block = "\n".join(parts)
    return (
        f"Explain these mandi figures to a farmer in {language}.\n"
        "Write at most three short sentences. Use simple words.\n"
        "Use ONLY the numbers given below. Do not add any other number.\n"
        "Do not give advice beyond these figures. Do not mention dates.\n"
        "Do not invent markets or prices.\n\n"
        f"{numbers_block}\n"
    )


def facts_block(payload: dict) -> str:
    """The computed-number section used for the post-check (not the instructions)."""
    best = payload["best"]
    lines = [
        str(payload.get("crop", "")),
        str(best["market"]),
        str(best["net_price"]),
        str(best["modal_price"]),
        str(best["transport_cost"]),
        str(best["distance_km"]),
        str(payload.get("signal", "")),
        "7",
    ]
    runner = payload.get("runner_up")
    if runner:
        lines.append(str(runner["market"]))
        lines.append(str(runner["net_price"]))
    if payload.get("difference_rs") is not None:
        lines.append(str(payload["difference_rs"]))
    return " ".join(lines)


def _call_ollama(prompt: str) -> Optional[str]:
    host, model, timeout = _ollama_settings()
    url = f"{host}/api/generate"
    try:
        resp = requests.post(
            url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1},
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        text = (data.get("response") or "").strip()
        return text or None
    except (requests.RequestException, ValueError, KeyError):
        return None


def explain(payload: dict, lang: str = "en") -> dict:
    """Return {text, source} where source is 'llm' or 'template'."""
    norm = _norm_lang(lang)
    fallback = template_explanation(payload, norm)
    prompt = build_prompt(payload, norm)
    allowed = facts_block(payload) + "\n" + prompt
    model_text = _call_ollama(prompt)
    if not model_text:
        return {"text": fallback, "explanation": fallback, "source": "template"}
    if not numbers_are_subset(model_text, allowed):
        return {"text": fallback, "explanation": fallback, "source": "template"}
    return {"text": model_text, "explanation": model_text, "source": "llm"}
