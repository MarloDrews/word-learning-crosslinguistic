"""Administration-level filtering. One row per child, the basis for the curve
fits, the instrument characteristics and the split-half noise ceiling."""
import pandas as pd

from src.aoa.forms import FORMS
from src.common.config import LANGUAGES, raw_dir

PATH = raw_dir("wordbank") / "administrations.parquet"

COLUMNS = ["data_id", "child_id", "dataset_name", "form", "age", "in_age_range"]

# Braginsky drop this dataset. Wordbank's dataset_name carries only the surname
EXCLUDE_DATASETS = ["Fernald"]


def load(language, exclude_datasets=EXCLUDE_DATASETS):
    df = pd.read_parquet(
        PATH,
        columns=COLUMNS + ["language"],
        filters=[("language", "==", LANGUAGES[language])],
    ).drop(columns="language")

    df = df[df["form"].isin(FORMS[language])]
    df = df[~df["dataset_name"].isin(exclude_datasets)]

    # Forms first, otherwise a child's earliest administration could be on a
    # form we drop and the child vanishes with it. Braginsky deduplicate only
    # what their data marks as longitudinal, that flag is not in this table.
    # Ties by data_id, they leave them to database order.
    df = df.sort_values(["age", "data_id"]).drop_duplicates("child_id")

    return df.reset_index(drop=True)


# age has no missing values here, in_age_range is kept unfiltered because Braginsky set no age bounds