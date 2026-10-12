# Deviations from the proposal

The proposal was submitted on 27 August 2026 as an initial plan. This file
records where the implementation departs from it and why.

## Minimum words per category

The proposal excludes a language when fewer than 30 words remain in a lexical category.
We drop only that category for that language and keep the others.
The regressions run per category, so a language with too few function words still has usable nouns and predicates.
Excluding whole languages would leave two of the five replication languages, because many function words do not reach 50% by 30 months.