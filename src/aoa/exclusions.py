"""Exclusion criteria from the proposal. Applied per language, after the fits."""
import pandas as pd

from src.common.config import LANGUAGES, LEXICAL_CATEGORIES, raw_dir

MIN_WORDS_PER_CATEGORY = 30
MAX_EXTRAPOLATED = 0.4


def age_range(language):
    # the range each form is normed for, 8 to 30 months in English
    # Not the observed range, that one is set by a single child at 173 months
    admins = pd.read_parquet(
        raw_dir("wordbank") / "administrations.parquet",
        columns=["language", "form", "age", "in_age_range"],
        filters=[("language", "==", LANGUAGES[language]),
                 ("in_age_range", "==", True)],
    )
    ages = admins.loc[admins["form"].isin(("WG", "WS")), "age"]
    return ages.min(), ages.max()


def categories(items):
    # a lemma whose items disagree becomes other and is dropped with it
    per_lemma = items.groupby("uni_lemma")["lexical_category"].agg(
        lambda values: values.iloc[0] if values.nunique() == 1 else "other"
    )
    return per_lemma.rename("lexical_category")


def apply(fits, items, language):
    low, high = age_range(language)

    df = fits.merge(categories(items), on="uni_lemma")
    df = df[df["lexical_category"].isin(LEXICAL_CATEGORIES)]

    df["extrapolated"] = ~df["aoa"].between(low, high)
    df = df[df["aoa"].notna()]

    return df[["uni_lemma", "lexical_category", "aoa", "extrapolated"]].reset_index(drop=True)


def check(df, language):
    """Language-level criteria. Prints what is wrong."""
    counts = df["lexical_category"].value_counts()
    for category in LEXICAL_CATEGORIES:
        n = counts.get(category, 0)
        if n < MIN_WORDS_PER_CATEGORY:
            print(f"{language}: {category} has {n} words")

    share = df["extrapolated"].mean()
    if share > MAX_EXTRAPOLATED:
        print(f"{language}: {share:.0%} of aoa values are extrapolated")