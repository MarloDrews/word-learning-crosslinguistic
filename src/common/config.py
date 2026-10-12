"""Paths and project constants."""
from pathlib import Path

# common -> src -> project root
ROOT = Path(__file__).resolve().parents[2]

DATA = ROOT / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
INTERFACE = PROCESSED / "interface"
MANIFEST = DATA / "MANIFEST.csv"

RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"
TABLES = RESULTS / "tables"
REPORTS = RESULTS / "reports"
MODELS = RESULTS / "models"

SNAPSHOTS = {
    "wordbank": "2026-08-31",
    "norms": "2026-08-31",
    "braginsky": "2026-08-31",
    "norare": "2026-10-12",
}

# Wordbank spelling on the right, we filter on that and use the codes elsewhere
LANGUAGES = {
    "eng": "English (American)",
    "spa": "Spanish (Mexican)",
    "fra": "French (Quebecois)",
    "ita": "Italian",
    "hrv": "Croatian",
    "deu": "German",
    "nld": "Dutch",
    "hun": "Hungarian",
    "fin": "Finnish",
    "est": "Estonian",
}

REPLICATION = ["eng", "spa", "fra", "ita", "hrv"]
EXTENSION = ["deu", "nld", "hun", "fin", "est"]
NORM_CHECK = ["ita", "fra", "spa", "nld"]

# dropping 'other', 'unknown' and unlabelled items
LEXICAL_CATEGORIES = ["nouns", "predicates", "function_words"]


def raw_dir(source):
    return RAW / source / SNAPSHOTS[source]