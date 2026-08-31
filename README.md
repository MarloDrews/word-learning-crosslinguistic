# Predictors of early word learning across languages

Replication and typological extension of Braginsky, Yurovsky, Marchman & Frank (2019).

Final project for Data Science for Linguists, Summer 2026,
University of Tübingen, supervised by Dr. Johannes Dellert.

Marlo Drews, Joshua Bartl

## Research questions

- Can we replicate the findings of Braginsky et al. (2019) on early word acquisition?
- Do we get similar results when examining additional languages and language families?
- Is it valid to apply the English-based ratings to other languages?

One part per question:

1. **Replication.** Rebuild the pipeline for five of Braginsky et al.'s ten
   languages and validate it against their published predictor values.
2. **Extension.** Add five languages not in the original sample. Hungarian,
   Finnish and Estonian add Uralic as a second language family.
3. **Norm transfer.** Compare the English ratings against NoRaRe's
   native-language norms for Italian, French, Spanish and Dutch. Concreteness
   first, valence and arousal where available. Ratings are standardised, since
   the scales differ. There are no non-English babiness norms, so that predictor
   stays transferred and the assumption cannot be tested for it.

Languages: English (American), Spanish (Mexican), French (Quebecois), Italian,
Croatian, German, Dutch, Hungarian, Finnish, Estonian. Mandarin, Cantonese, Czech
and Portuguese are optional additions if time permits.

We use the nine predictors of the original study and fill missing values by
iterative regression within each language rather than dropping the rows. We
depart from the original in three ways: age interactions are dropped because
aggregating to the word level removes age as a within-word variable,
comprehension data are excluded because they would narrow the age range, and
mixed effects models are replaced by regression on per-word age of acquisition,
following Braginsky et al. (2016) and Goodman, Dale & Li (2008).

## Robustness checks

- **Noise ceiling.** Coefficients estimated on split halves of the children and
  correlated across bootstrap draws, giving an upper bound for the pairwise
  correlations where the original used a random baseline as a lower bound.
- **Relatedness split.** The 45 language pairs are not independent, so
  within-family and cross-family pairs are averaged separately, with a further
  split at branch level.
- **Corpus size.** Size per language against coefficient magnitude, reported
  with the number of children and corpora, since size alone is misleading.
- **Instrument characteristics.** Age range, item count, predictor variance and
  extrapolation share per language, compared against Wordbank's own age of
  acquisition estimates, which are clipped to the observed age range.

## Data

| Source | Provides | Version | Retrieved |
|---|---|---|---|
| Wordbank (CDI) | item responses by age, item metadata | 2.0, doi:10.57761/ytz9-sa21 | 2026-08-31 |
| CHILDES | child-directed speech for the input predictors | not yet retrieved | |
| English norms | concreteness, valence, arousal, babiness | not yet retrieved | |
| NoRaRe | native-language norms | not yet retrieved | |

Downloads are stored unchanged under `data/raw/`, one directory per source and
retrieval date, and are not committed. Unpacking and every other transformation
happens in code, writing to `data/interim/`.

Wordbank citation: Datapages (2026). *Wordbank* (Version 2.0) [Dataset]. Redivis.
TalkBank requires citing at least one reference per CHILDES corpus used and
acknowledging NICHD HD082736.

## Repository layout

    data/raw/         downloads, unchanged, not committed
    data/interim/     intermediate steps, rebuilt from raw, not committed
    data/processed/   analysis-ready tables, one row per word
    src/              importable modules, one per pipeline stage
    scripts/          command line entry points
    notebooks/        thin, prefixed a/ and b/ by owner
    results/          figures, tables, executed notebooks
    docs/             proposal, agreements, corpus references

Notebook outputs are stripped on commit, so notebooks here show code without
results. Executed versions go to `results/reports/`.

## Setup

Python 3.12.10. Other versions resolve to different package versions.

    python -m venv .venv
    .venv\Scripts\Activate.ps1     # Windows
    source .venv/bin/activate      # macOS, Linux
    pip install -r requirements.txt
    nbstripout --install --attributes .gitattributes

## Work split

Marlo: age of acquisition from the CDI data, norm predictors, part 3, noise ceiling
instrument characteristics, repository and reproducibility.

Joshua: CHILDES processing, input predictors, phoneme counts, regressions and
model diagnostics, corpus size diagnostics, pairwise comparison and relatedness
split.