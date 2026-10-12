# Deviations from the proposal

The proposal was submitted on 27 August 2026 as an initial plan. This file
records where the implementation departs from it and why.

## Minimum words per category

The proposal excludes a language when fewer than 30 words remain in a lexical category.
We drop only that category for that language and keep the others.
The regressions run per category, so a language with too few function words still has usable nouns and predicates.
Excluding whole languages would leave two of the five replication languages, because many function words do not reach 50% by 30 months.

## Longitudinal administrations

The proposal excludes longitudinal administrations so that no child is counted twice.
We keep each child's earliest administration instead, as Braginsky's loading code does.
This reaches the same goal without losing data. Dropping every child with several administrations would cost a fifth of the English children.
Wordbank marks all Dutch, Hungarian and Estonian datasets as longitudinal, so excluding by that flag would remove these languages entirely.