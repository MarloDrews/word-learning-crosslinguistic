"""Item selection. One row per item, the word list a language contributes to
the curve fits."""
import pandas as pd

from src.aoa.forms import FORMS, WORD_LIST_FORM
from src.common.config import LANGUAGES, raw_dir

PATH = raw_dir("wordbank") / "items.parquet"

COLUMNS = ["item_id", "form", "item_kind", "category", "item_definition",
           "uni_lemma", "lexical_category"]


def load(language):
    df = pd.read_parquet(
        PATH,
        columns=COLUMNS + ["language"],
        filters=[("language", "==", LANGUAGES[language])],
    ).drop(columns="language")

    df = df[df["item_kind"] == "word"]
    df = df[df["form"].isin(FORMS[language])]

    # definitions carry trailing spaces in some languages
    df["item_definition"] = df["item_definition"].str.strip().str.lower()

    # a WS item without a uni_lemma inherits it from the WG item of the same definition
    # No English item lacks one but 5002 rows across the table do
    lemmas = df[["item_definition", "uni_lemma"]].dropna().drop_duplicates()
    df = df.drop(columns="uni_lemma").merge(lemmas, on="item_definition", how="left")
    df = df.dropna(subset="uni_lemma")

    # Braginsky keep definitions that appear on the WG form, not those on both
    word_list_form = WORD_LIST_FORM[language]
    if word_list_form is not None:
        on_word_list = df.loc[df["form"] == word_list_form, "item_definition"]
        df = df[df["item_definition"].isin(on_word_list)]

    # from Braginsky, drops the whole lemma not just the starred item
    # no effect in our ten languages, the three English ones are WS only.
    starred = (df["category"] == "body_parts") & df["item_definition"].str.contains(r"\*")
    df = df[~df["uni_lemma"].isin(df.loc[starred, "uni_lemma"])]

    # placeholder items like "child's own name", the leading space is Braginsky's
    df = df[~df["uni_lemma"].str.contains(" name")]

    return df.drop(columns="item_kind").reset_index(drop=True)