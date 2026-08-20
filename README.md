# Predictors of early word learning across languages

Replication and typological extension of Braginsky, Yurovsky, Marchman & Frank (2019).

Final project for Data Science for Linguists, Summer 2026,
University of Tübingen, supervised by Dr. Johannes Dellert.

Marlo Drews, Joshua Bartl

## Research question

Are the predictors of early word learning consistent across typologically diverse
languages, and how robust is the finding to (a) statistical noise in the
coefficient estimates and (b) the transfer of English psycholinguistic norms?

The project has three parts:

1. **Replication.** Rebuild the pipeline for five of Braginsky et al.'s languages
   and validate it against their published predictor values.
2. **Extension.** Add five languages not in the original sample, three of them
   Uralic, so that the sample is no longer predominantly Indo-European.
3. **Norm transfer.** Test whether English-based concreteness, valence and arousal
   ratings can be applied to other languages, using native-language norms where
   available. Babiness has no non-English norms at all, so the assumption cannot
   be tested for it and it stays transferred throughout.

Languages: English (American), Spanish (Mexican), French (Quebecois), Italian,
Croatian, German, Dutch, Hungarian, Finnish, Estonian.

## Data sources

All raw data are archived unmodified in `data/raw/`. Versions and retrieval dates
are recorded in `data/MANIFEST.csv`.

| Source | Provides | Access |
|---|---|---|
| Wordbank (CDI) | age of acquisition | Redivis, dataset version 2.0 |
| CHILDES | corpus-based predictors | childes.talkbank.org |
| English norms | concreteness, valence, arousal, babiness | supplementary material of the source publications |
| NoRaRe | native-language norms | norare.clld.org |

The raw data are not part of this repository. The derived per-word tables under
`data/processed/` are, so the analysis can be re-run without downloading anything.

Citation requirements: TalkBank rules require citing at least one corpus reference
per corpus used and acknowledging NICHD HD082736. Corpus references are listed in
`docs/corpora.md`.

## Setup



## Reproducing the analysis