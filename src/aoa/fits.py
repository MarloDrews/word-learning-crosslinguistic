"""Logistic curve per lemma. Age of acquisition is where the curve crosses
50 percent."""
import numpy as np
import pandas as pd
import statsmodels.api as sm


def fit_lemma(group):
    x = sm.add_constant(group["age"].to_numpy(dtype=float), has_constant="add")
    y = np.column_stack([group["n_produces"], group["n_children"] - group["n_produces"]])

    try:
        model = sm.GLM(y, x, family=sm.families.Binomial()).fit()
    except Exception:
        return pd.Series({"intercept": np.nan, "slope": np.nan, "aoa": np.nan})

    intercept, slope = model.params

    # a lemma every child produces at every age has no slope to find, the fit runs off to infinity instead of failing
    if not model.converged or slope <= 0:
        return pd.Series({"intercept": np.nan, "slope": np.nan, "aoa": np.nan})

    return pd.Series({
        "intercept": intercept,
        "slope": slope,
        "aoa": -intercept / slope,
    })


def fit(counts):
    # Braginsky use a robust GLM, we use a plain one
    # Weighting by the number of children already dampens the thin ages a robust fit would downweight
    fits = counts.groupby("uni_lemma").apply(fit_lemma, include_groups=False)

    ages = counts.groupby("uni_lemma").size().rename("n_ages")

    return fits.join(ages).reset_index()