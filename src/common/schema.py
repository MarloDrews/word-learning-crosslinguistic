"""Schema of the handover file. One file per language, written by the AoA side
and read by the regression side. Changes here break the other half."""
import numpy as np
import pandas as pd

from src.common.config import INTERFACE, LEXICAL_CATEGORIES

COLUMNS = {
    "language": "string",
    "uni_lemma": "string",
    "lexical_category": "string",
    "aoa": "float64",
    "concreteness": "float64",
    "valence": "float64",
    "arousal": "float64",
    "babiness": "float64",
}

KEY = ["language", "uni_lemma"]
NORMS = ["concreteness", "valence", "arousal", "babiness"]


def path(language):
    return INTERFACE / f"aoa_norms_{language}.csv"


def read(language):
    df = pd.read_csv(path(language))
    validate(df)
    return df


def write(df, language):
    validate(df)
    INTERFACE.mkdir(parents=True, exist_ok=True)
    df[list(COLUMNS)].to_csv(path(language), index=False)


def validate(df):
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")

    extra = set(df.columns) - set(COLUMNS)
    if extra:
        raise ValueError(f"unexpected columns: {sorted(extra)}")

    dup = df.duplicated(subset=KEY).sum()
    if dup:
        raise ValueError(f"{dup} duplicate rows on {KEY}")

    for col in KEY + ["lexical_category"]:
        if df[col].isna().any():
            raise ValueError(f"{col} must not contain NaN")

    unknown = set(df["lexical_category"]) - set(LEXICAL_CATEGORIES)
    if unknown:
        raise ValueError(f"unknown lexical_category: {sorted(unknown)}")

    if df["language"].nunique() != 1:
        raise ValueError("one language per file")

    # no range check on aoa: -intercept/slope is unbounded, extrapolated values
    # outside the observed age range are expected
    if not np.isfinite(df["aoa"].dropna()).all():
        raise ValueError("aoa contains inf")

    return True