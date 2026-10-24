"""Normalize state / district / market / crop names so spelling variants match.

Code — not the LLM — owns these mappings.
"""

from __future__ import annotations

# Alternate English spellings → one canonical title-case name.
COMMODITY_ALIASES = {
    "onion": "Onion",
    "pyaz": "Onion",
    "pyaaz": "Onion",
    "tomato": "Tomato",
    "tamatar": "Tomato",
    "potato": "Potato",
    "aloo": "Potato",
    "alu": "Potato",
    "wheat": "Wheat",
    "gehu": "Wheat",
    "gehun": "Wheat",
    "rice": "Rice",
    "paddy": "Rice",
    "paddy(dhan)": "Rice",
    "paddy (dhan)": "Rice",
    "paddy(common)": "Rice",
    "paddy (common)": "Rice",
    "paddy common": "Rice",
    "paddy(dhan)(common)": "Rice",
    "paddy(dhan)(basmati)": "Rice",
    "paddy basmati": "Rice",
    "dhan": "Rice",
    "paddy dhan": "Rice",
    "soybean": "Soybean",
    "soyabean": "Soybean",
    "soya": "Soybean",
    "cotton": "Cotton",
    "kapas": "Cotton",
    "maize": "Maize",
    "makka": "Maize",
    "corn": "Maize",
    "mustard": "Mustard",
    "sarson": "Mustard",
    "groundnut": "Groundnut",
    "peanut": "Groundnut",
    "chilli": "Chilli",
    "chili": "Chilli",
    "mirch": "Chilli",
    "red chilli": "Chilli",
    "green chilli": "Green Chilli",
    "banana": "Banana",
    "kela": "Banana",
    "mango": "Mango",
    "apple": "Apple",
    "orange": "Orange",
    "mosambi": "Mosambi",
    "lemon": "Lemon",
    "garlic": "Garlic",
    "lahsun": "Garlic",
    "ginger": "Ginger",
    "adrak": "Ginger",
    "turmeric": "Turmeric",
    "haldi": "Turmeric",
    "coriander": "Coriander",
    "dhania": "Coriander",
    "cumin": "Cumin",
    "jeera": "Cumin",
    "gram": "Gram",
    "chana": "Gram",
    "bengal gram": "Gram",
    "moong": "Moong",
    "green gram": "Moong",
    "arhar": "Arhar",
    "tur": "Arhar",
    "toor": "Arhar",
    "urad": "Urad",
    "black gram": "Urad",
    "masur": "Masur",
    "lentil": "Masur",
    "sugarcane": "Sugarcane",
    "jowar": "Jowar",
    "sorghum": "Jowar",
    "bajra": "Bajra",
    "pearl millet": "Bajra",
    "ragi": "Ragi",
    "barley": "Barley",
    "jute": "Jute",
    "coconut": "Coconut",
    "arecanut": "Arecanut",
    "cashew": "Cashew",
    "rubber": "Rubber",
    "tea": "Tea",
    "coffee": "Coffee",
    "cabbage": "Cabbage",
    "cauliflower": "Cauliflower",
    "brinjal": "Brinjal",
    "eggplant": "Brinjal",
    "okra": "Bhindi",
    "bhindi": "Bhindi",
    "lady finger": "Bhindi",
    "peas": "Peas",
    "carrot": "Carrot",
}

# Hindi (and a few common spoken) labels for the UI crop chips / dropdown.
CROP_LABELS = {
    "Onion": {"hi": "प्याज", "en": "Onion"},
    "Tomato": {"hi": "टमाटर", "en": "Tomato"},
    "Potato": {"hi": "आलू", "en": "Potato"},
    "Wheat": {"hi": "गेहूं", "en": "Wheat"},
    "Rice": {"hi": "धान / चावल", "en": "Rice"},
    "Soybean": {"hi": "सोयाबीन", "en": "Soybean"},
    "Cotton": {"hi": "कपास", "en": "Cotton"},
    "Maize": {"hi": "मक्का", "en": "Maize"},
    "Mustard": {"hi": "सरसों", "en": "Mustard"},
    "Groundnut": {"hi": "मूंगफली", "en": "Groundnut"},
    "Chilli": {"hi": "मिर्च", "en": "Chilli"},
    "Green Chilli": {"hi": "हरी मिर्च", "en": "Green Chilli"},
    "Banana": {"hi": "केला", "en": "Banana"},
    "Mango": {"hi": "आम", "en": "Mango"},
    "Apple": {"hi": "सेब", "en": "Apple"},
    "Orange": {"hi": "संतरा", "en": "Orange"},
    "Lemon": {"hi": "नींबू", "en": "Lemon"},
    "Garlic": {"hi": "लहसुन", "en": "Garlic"},
    "Ginger": {"hi": "अदरक", "en": "Ginger"},
    "Turmeric": {"hi": "हल्दी", "en": "Turmeric"},
    "Coriander": {"hi": "धनिया", "en": "Coriander"},
    "Cumin": {"hi": "जीरा", "en": "Cumin"},
    "Gram": {"hi": "चना", "en": "Gram"},
    "Moong": {"hi": "मूंग", "en": "Moong"},
    "Arhar": {"hi": "अरहर / तूर", "en": "Arhar"},
    "Urad": {"hi": "उड़द", "en": "Urad"},
    "Masur": {"hi": "मसूर", "en": "Masur"},
    "Sugarcane": {"hi": "गन्ना", "en": "Sugarcane"},
    "Jowar": {"hi": "ज्वार", "en": "Jowar"},
    "Bajra": {"hi": "बाजरा", "en": "Bajra"},
    "Ragi": {"hi": "रागी", "en": "Ragi"},
    "Barley": {"hi": "जौ", "en": "Barley"},
    "Coconut": {"hi": "नारियल", "en": "Coconut"},
    "Brinjal": {"hi": "बैंगन", "en": "Brinjal"},
    "Bhindi": {"hi": "भिंडी", "en": "Bhindi"},
    "Cabbage": {"hi": "पत्ता गोभी", "en": "Cabbage"},
    "Cauliflower": {"hi": "फूल गोभी", "en": "Cauliflower"},
    "Peas": {"hi": "मटर", "en": "Peas"},
    "Carrot": {"hi": "गाजर", "en": "Carrot"},
    "Jute": {"hi": "जूट", "en": "Jute"},
    "Mosambi": {"hi": "मौसंबी", "en": "Mosambi"},
    "Arecanut": {"hi": "सुपारी", "en": "Arecanut"},
    "Cashew": {"hi": "काजू", "en": "Cashew"},
    "Tea": {"hi": "चाय", "en": "Tea"},
    "Coffee": {"hi": "कॉफी", "en": "Coffee"},
    "Rubber": {"hi": "रबर", "en": "Rubber"},
}

STATE_ALIASES = {
    "orissa": "Odisha",
    "odisha": "Odisha",
    "nct of delhi": "Delhi",
    "nct delhi": "Delhi",
    "delhi": "Delhi",
    "pondicherry": "Puducherry",
    "puducherry": "Puducherry",
    "uttaranchal": "Uttarakhand",
    "jammu & kashmir": "Jammu and Kashmir",
    "jammu and kashmir": "Jammu and Kashmir",
    "dadra and nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "andaman & nicobar": "Andaman and Nicobar Islands",
    "andaman and nicobar": "Andaman and Nicobar Islands",
    "chattisgarh": "Chhattisgarh",
    "keralam": "Kerala",
    "kerala": "Kerala",
    "telengana": "Telangana",
    "tamilnadu": "Tamil Nadu",
    "tamil nadu": "Tamil Nadu",
    "west bengal": "West Bengal",
}

# Renamed districts / spelling variants across India
DISTRICT_ALIASES = {
    "raigad": "Alibag",
    "raigarh": "Alibag",
    "ahilyanagar": "Ahmednagar",
    "ahmednagar": "Ahmednagar",
    "chhatrapati sambhajinagar": "Aurangabad",
    "chattrapati sambhajinagar": "Aurangabad",
    "aurangabad": "Aurangabad",
    "dharashiv": "Osmanabad",
    "osmanabad": "Osmanabad",
    "beed": "Bid",
    "bid": "Bid",
    "prayagraj": "Allahabad",
    "allahabad": "Allahabad",
    "ayodhya": "Faizabad",
    "faizabad": "Faizabad",
    "varanasi": "Banaras",
    "banaras": "Banaras",
    "kashi": "Banaras",
    "bengaluru urban": "Bangalore",
    "bengaluru rural": "Bangalore",
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "mysuru": "Mysore",
    "mysore": "Mysore",
    "gurugram": "Gurgaon",
    "gurgaon": "Gurgaon",
    "nuh": "Mewat",
    "mewat": "Mewat",
    "narmadapuram": "Hoshangabad",
    "hoshangabad": "Hoshangabad",
    "tirunelveli kattabo": "Tirunelveli",
    "tiruvannamalai sambuvarayar": "Tiruvannamalai",
    "banaskanth": "Banaskantha",
    "junagarh": "Junagadh",
    "kachchh": "Kutch",
    "bhatinda": "Bathinda",
    "ferozpur": "Firozpur",
    "tarntaran": "Tarn Taran",
    "chittor": "Chittoor",
    "ananthapuramu": "Anantapur",
    "vadodara(baroda)": "Vadodara",
    "east champaran/ motihari": "Motihari",
    "kaimur/bhabhua": "Bhabhua",
}

COMMODITY_GROUPS = [
    {"Soybean", "Soyabean", "Soya"},
    {"Rice", "Paddy", "Paddy(Common)", "Paddy (Common)", "Paddy(Dhan)(Common)", "Dhan", "Paddy Dhan"},
    {"Wheat", "Gehu", "Gehun"},
    {"Onion", "Pyaz", "Pyaaz"},
    {"Tomato", "Tamatar"},
    {"Potato", "Aloo", "Alu"},
    {"Maize", "Makka", "Corn"},
    {"Cotton", "Kapas"},
    {"Mustard", "Sarson"},
    {"Groundnut", "Peanut", "Mungfali"},
    {"Chilli", "Chili", "Mirch", "Green Chilli", "Red Chilli"},
    {"Gram", "Chana", "Bengal Gram"},
    {"Moong", "Green Gram"},
    {"Arhar", "Tur", "Toor"},
    {"Urad", "Black Gram"},
    {"Masur", "Lentil"},
    {"Garlic", "Lahsun"},
    {"Ginger", "Adrak"},
    {"Turmeric", "Haldi"},
    {"Banana", "Kela"},
    {"Apple", "Seb"},
    {"Mango", "Aam"},
    {"Cabbage", "Patta Gobhi"},
    {"Cauliflower", "Phool Gobhi"},
    {"Brinjal", "Baingan", "Eggplant"},
    {"Bhindi", "Okra", "Lady Finger"},
]


def get_commodity_variants(crop: str) -> list[str]:
    """Return all known naming variants for a given crop query."""
    c_lower = str(crop or "").strip().lower()
    variants = {crop.strip()} if crop else set()
    for group in COMMODITY_GROUPS:
        if any(item.lower() == c_lower for item in group):
            variants.update(group)
    return [v for v in variants if v]


def title_place(value: str) -> str:
    """Strip whitespace and title-case a place name (keeps '&')."""
    text = " ".join(str(value or "").split())
    if not text:
        return ""
    return " ".join(part.capitalize() if part != "&" else "&" for part in text.split(" "))


def canonical_state(value: str) -> str:
    titled = title_place(value)
    return STATE_ALIASES.get(titled.lower(), titled)


def canonical_commodity(value: str) -> str:
    raw = " ".join(str(value or "").split())
    if not raw:
        return ""
    key = (
        raw.lower()
        .replace("(", " ")
        .replace(")", " ")
        .replace("-", " ")
        .replace("/", " ")
    )
    key = " ".join(key.split())
    if key in COMMODITY_ALIASES:
        return COMMODITY_ALIASES[key]
    compact = key.replace(" ", "")
    for alias, canon in COMMODITY_ALIASES.items():
        if alias.replace(" ", "") == compact:
            return canon
    return title_place(raw)


def crop_label(commodity: str, lang: str = "en") -> str:
    labels = CROP_LABELS.get(commodity, {})
    if lang.startswith("hi") and labels.get("hi"):
        return f"{commodity} ({labels['hi']})"
    return commodity
