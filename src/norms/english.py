"""The four English norm predictors, attached to uni_lemmas. Raw values, the
regression side standardises them."""
import pandas as pd

from src.common.config import raw_dir

DIR = raw_dir("norms")


def _lookup(lemmas, replacements, norms, columns):
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