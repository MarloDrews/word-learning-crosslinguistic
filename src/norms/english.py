"""The four English norm predictors, attached to uni_lemmas. Raw values, the
regression side standardises them."""
import pandas as pd

from src.common.config import raw_dir

DIR = raw_dir("norms")

# Wordbank 2.0 names pronouns by glossing codes, Braginsky's replacement tables predate that
# These are the English items under each code, with "he" moved out of 3SG.POSS where Wordbank files it
PRONOUNS = {
    "1SG": ["I", "me"],
    "1SG.POSS": ["my", "mine"],
    "1SG.REFL": ["myself"],
    "2SG": ["you"],
    "2SG.POSS": ["your"],
    "2SG.REFL": ["yourself"],
    "3SG": ["he", "she", "it", "him"],
    "3SG.POSS": ["his", "her", "hers"],
    "1PL": ["we", "us"],
    "1PL.POSS": ["our"],
    "3PL": ["they", "them"],
    "3PL.POSS": ["their"],
}


def _lookup(lemmas, replacements, norms, columns):

    pronouns = pd.DataFrame(
        [(code, word) for code, words in PRONOUNS.items() for word in words],
        columns=["uni_lemma", "replacement"],
    )
    replacements = pd.concat([replacements, pronouns])

    df = lemmas.merge(replacements, on="uni_lemma", how="left")

    word = df["replacement"].where(df["replacement"].notna() & (df["replacement"] != ""),
                                   df["uni_lemma"])

    # the CDI disambiguates senses in brackets, "chicken (animal)"
    df["word"] = word.str.replace(r" \(.*\)$", "", regex=True)

    df = df.merge(norms, on="word", how="left")

    # a lemma can map to several words, "one two three" to one, two and three
    return df.groupby("uni_lemma")[columns].mean()


def load(lemmas):
    lemmas = lemmas[["uni_lemma"]].drop_duplicates()

    valence = pd.read_csv(DIR / "valence.csv")[["Word", "V.Mean.Sum", "A.Mean.Sum"]]
    valence.columns = ["word", "valence", "arousal"]

    concreteness = pd.read_csv(DIR / "concreteness.csv")[["Word", "Conc.M"]]
    concreteness.columns = ["word", "concreteness"]

    # one row per rater, babyAVG is already averaged and repeated on each
    babiness = pd.read_csv(DIR / "english_babiness.csv")[["word", "babyAVG"]]
    babiness = babiness.drop_duplicates("word").rename(columns={"babyAVG": "babiness"})

    return pd.concat([
        _lookup(lemmas, pd.read_csv(DIR / "valence_replace.csv"), valence,
                ["valence", "arousal"]),
        _lookup(lemmas, pd.read_csv(DIR / "concreteness_replace.csv"), concreteness,
                ["concreteness"]),
        _lookup(lemmas, pd.read_csv(DIR / "babiness_replace.csv"), babiness,
                ["babiness"]),
    ], axis=1).reset_index()