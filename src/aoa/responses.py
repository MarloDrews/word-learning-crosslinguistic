"""Response aggregation. One row per lemma and age, the input to the curve
fits."""
import pandas as pd

from src.common.config import LANGUAGES, INTERIM

PATH = INTERIM / "wordbank" / "item_responses"

COLUMNS = ["data_id", "form", "item_id", "produces"]


def load(language, admins, items):
    responses = pd.read_parquet(
        PATH,
        columns=COLUMNS + ["language"],
        filters=[("language", "==", LANGUAGES[language])],
    ).drop(columns="language")

    responses = responses[responses["data_id"].isin(admins["data_id"])]

    # item_id restarts at 1 on every form, so item_1 is a different word on WG than on WS
    # Joining without form silently mislabels every WG response
    responses = responses.merge(
        items[["form", "item_id", "uni_lemma"]], on=["form", "item_id"]
    )

    # a blank answer counts as not produced, as in Braginsky. 16 percent of the English rows
    responses["produces"] = responses["produces"].fillna(False)

    responses = responses.merge(admins[["data_id", "age"]], on="data_id")

    per_child = responses.groupby(["uni_lemma", "age", "data_id"])["produces"].any()

    counts = per_child.groupby(["uni_lemma", "age"]).agg(
        n_children="size", n_produces="sum"
    )

    return counts.reset_index()