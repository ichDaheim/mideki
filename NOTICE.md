# NOTICE

mideki
Licensed under the Apache License, Version 2.0 (see `LICENSE`).

This product contains code derived from
[misaki](https://github.com/hexgrad/misaki) by hexgrad (Apache License 2.0),
by way of the fork at [semidark/misaki](https://github.com/semidark/misaki),
which added the German G2P (text normalization, override lookup, `DEG2P`;
authored by Nico Thomaier). The pronunciation overrides in
`data/de_overrides.json` (`brand`, `en`, `de_foreign`, `aliases`) originate
from kikiri-tts (PR #28).

## Provenance per file

| File | Origin |
|---|---|
| `normalize.py` | semidark/misaki, modified (see below) |
| `overrides.py` | semidark/misaki, modified (see below) |
| `g2p.py` | semidark/misaki (`DEG2P`, renamed to `G2P`), modified (see below) |
| `espeak.py` | hexgrad/misaki (`EspeakG2P`), modified (see below) |
| `data/de_overrides.json` | kikiri-tts PR #28, modified (see below) |
| `segment.py`, `symbols.py`, `override_checks.py` | new |
| `data/phoneme_set_de.json`, `data/token_map_de.json` | new |

## Changes from upstream

### Text normalization (`normalize.py`)

- German compounds ending in "software"/"hardware" are split into two words
  before phonemization ("Steuerungssoftware" -> "Steuerungs software").
  espeak-ng's German dictionary garbles the entire compound for this suffix
  pair, not just the suffix. Splitting costs the compound's single-word
  stress. Not handled: "software"/"hardware" in the middle of a compound
  ("Bürosoftwarepaket").

### Overrides (`overrides.py`, `data/de_overrides.json`)

- New section `de_native` for native German words that espeak-ng garbles
  (e.g. "aneinander", which espeak-ng 1.52.0 phonemizes with a stray digit
  `1`). Section priority on lookup collisions:
  `brand > en > de_foreign > de_native`.
- Override lookup is public API.
- All override values are written in the canonical compressed symbol set.
  Overrides bypass espeak-ng and its postprocessing, so values with
  uncompressed diphthongs/affricates (`aɪ`, `tʃ`, …) or nasal tildes were
  rewritten to what `espeak.postprocess` would produce (e.g.
  `pytorch: "pˈItɔːɾʧ"`).
- Values avoid symbols that are (almost) absent from the kikiri-german training
  data (`ɹ`, `w`, `ʁ`, `ɒ`, `ʔ`, syllabic `n̩`/`l̩`, …) and use the closest
  trained substitute instead, so the acoustic model can actually pronounce
  them.
- `override_checks.py` enforces both rules above and rejects any symbol
  outside the canonical set:
  `mideki-check-overrides`.

### espeak-ng backend (`espeak.py`)

- Tie-compression table reduced to the sequences that occur in German
  espeak-ng output (`a^ɪ`→`I`, `a^ʊ`→`W`, `ɔ^ø`→`ʋ`, `t^s`→`ʦ`, `t^ʃ`→`ʧ`,
  `p^f`→`ꭧ`, `d^ʒ`→`ʤ`, `d^z`→`ʣ`, `s^s`→`S`). The English-only fallback
  and the nasal-vowel branch were removed.
- Untied `pf`/`tʃ`/`ts` are compressed as well, independent of position.
  espeak-ng only tie-marks them word-initially, but "Kopf" and "Pfote"
  contain the same affricate.
- Nasal vowels are denasalized (combining tilde U+0303 removed, e.g.
  "Chance" `ʃˈɑ̃sə` -> `ʃˈɑsə`). espeak-ng nasalizes French loanwords
  inconsistently and the training audio contains almost no nasal vowels, so
  a dedicated symbol would stay untrained.
- espeak-ng is pinned to 1.52.0 via `espeakng-loader==0.2.4` and
  `phonemizer-fork==3.3.2`; a system espeak-ng is never used. espeak-ng 1.50
  mispronounces German "ur" before a consonant ("Wurm", "kurz"), and other
  versions change stress and tie behaviour.

### G2P (`g2p.py`, `segment.py`)

- The class `DEG2P` is renamed to `G2P` (`from mideki import G2P`).
- `G2P` has an explicit `mode`. `'word'` (default) phonemizes every word in
  isolation; the downstream models (PL-BERT-de, ASR-de, kikiri-german) were
  trained on this output. `'sentence'` is the original upstream behaviour
  (espeak-ng sees whole spans between overrides) and is kept for comparison.

### Canonical symbol set (`symbols.py`, `data/`)

- `phoneme_set_de.json` defines the canonical phoneme and punctuation
  symbols; `token_map_de.json` assigns their model token IDs. The token map
  is append-only, and models pin it via `token_map_sha256()`. It contains
  the symbol `1`, an espeak-ng artifact ("aneinander", see above) that is
  kept for ID stability and never carries a real sound.
- Phoneme strings are split by longest match, so multi-code-point symbols
  such as `l̩` stay intact.
