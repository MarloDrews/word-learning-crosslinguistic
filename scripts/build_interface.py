"""Run one language through the AoA pipeline and write the handover file."""
import sys

from src.aoa import administrations, exclusions, fits, items, responses
from src.common import schema
from src.norms import english


def build(language):
    admins = administrations.load(language)
    words = items.load(language)

    counts = responses.load(language, admins, words)
    curves = fits.fit(counts)

    df = exclusions.apply(curves, counts, words, language)
    df = exclusions.check(df, language)

    if df.empty:
        print(f"{language}: excluded, no file written")
        return

    df = df.drop(columns="extrapolated").merge(english.load(words), on="uni_lemma")
    df["language"] = language

    schema.write(df, language)
    print(f"{language}: {len(df)} lemmas")


if __name__ == "__main__":
    build(sys.argv[1])