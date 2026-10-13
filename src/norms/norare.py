"""Native-language norms from NoRaRe. Raw values, each on its own
study's scale."""
import io
import zipfile
import pandas as pd

from src.common.config import raw_dir

PATH = raw_dir("norare") / "norare-cldf-v1.1.zip"
CLDF = "concepticon-norare-cldf-9fb8c96/cldf/"

# Montefinese also split valence and arousal by gender, these are the means over everyone
VARIABLES = {
    "ita": {
        "concreteness": "Montefinese-2014-AffectiveRatings-ITALIAN_CONCRETENESS_MEAN",
        "valence": "Montefinese-2014-AffectiveRatings-ITALIAN_VALENCE_ALL_MEAN",
        "arousal": "Montefinese-2014-AffectiveRatings-ITALIAN_AROUSAL_ALL_MEAN",
    },
    "fra": {
        "concreteness": "Bonin-2018-Concreteness-FRENCH_CONCRETENESS_MEAN",
        "valence": "Bonin-2018-Concreteness-FRENCH_VALENCE_MEAN",
        "arousal": "Bonin-2018-Concreteness-FRENCH_AROUSAL_MEAN",
    },
    "spa": {
        "concreteness": "Guasch-2016-AffectiveRatings-SPANISH_CONCRETENESS_MEAN",
        "valence": "Guasch-2016-AffectiveRatings-SPANISH_VALENCE_MEAN",
        "arousal": "Guasch-2016-AffectiveRatings-SPANISH_AROUSAL_MEAN",
    },
    "nld": {
        "concreteness": "Verheyen-2020-1000-CONCRETENESS_MEAN",
        "valence": "Verheyen-2020-1000-VALENCE_MEAN",
        "arousal": "Verheyen-2020-1000-AROUSAL_MEAN",
    },
    # not a transfer, a second English study as the baseline for how well two norm sets agree
    "eng": {
        "concreteness": "Scott-2019-Ratings-ENGLISH_CONCRETENESS_MEAN",
        "valence": "Scott-2019-Ratings-ENGLISH_VALENCE_MEAN",
        "arousal": "Scott-2019-Ratings-ENGLISH_AROUSAL_MEAN",
    },
}

NORMS = ["concreteness", "valence", "arousal"]


def _words(language):
    """One row per word form in the study, with its three norms."""
    with zipfile.ZipFile(PATH) as archive:
        glosses = pd.read_csv(archive.open(CLDF + "glosses.csv"))
        # the values table is zipped a second time inside the archive
        with zipfile.ZipFile(io.BytesIO(archive.read(CLDF + "norare.csv.zip"))) as inner:
            # values mix numbers and text across datasets, ours are converted below
            values = pd.read_csv(inner.open("norare.csv"), dtype=str)

    names = {variable: norm for norm, variable in VARIABLES[language].items()}
    values = values[values["Variable_ID"].isin(names)].copy()
    values["norm"] = values["Variable_ID"].map(names)
    values["Value"] = pd.to_numeric(values["Value"])

    df = values.merge(glosses[["ID", "Form"]], left_on="Unit_ID", right_on="ID")

    # a form linked to two concepts appears twice with the same value
    return df.pivot_table(index="Form", columns="norm", values="Value", aggfunc="mean")


def load(items, language):
    """Native norms per uni_lemma, averaged over the words of its items. Lemmas
    without any match are left out."""
    words = items[["uni_lemma", "item_definition"]].copy()

    # "ir(se)", "konijn(tje)" and "poisson (animal)" lose the brackets, "gros/grand" splits in two
    words["word"] = words["item_definition"].str.replace(r"\(.*?\)", "", regex=True).str.split("/")
    words = words.explode("word")
    words["word"] = words["word"].str.strip()
    words = words.drop_duplicates(["uni_lemma", "word"])

    df = words.merge(_words(language), left_on="word", right_index=True)
    return df.groupby("uni_lemma")[NORMS].mean().reset_index()
