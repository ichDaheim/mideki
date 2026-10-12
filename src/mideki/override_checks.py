"""Guard: override phonemes must look exactly like postprocessed espeak-ng output.

Override phonemes bypass `espeak.postprocess`, so hand-written entries can
drift out of sync with it. Two such drifts were found only after hour-long
corpus runs (uncompressed affricates, nasal vowels); later 23 entries with
uncompressed diphthongs turned up. This check makes each class a
seconds-long test. Run it whenever `data/de_overrides.json` changes:

    mideki-check-overrides
"""

from __future__ import annotations

import sys
from typing import List

from .espeak import COMBINING_TILDE
from .overrides import SECTIONS, load_raw_overrides
from .symbols import split_symbols, unknown_symbols

# Sequences espeak.postprocess would never leave uncompressed.
UNCOMPRESSED = {
    'pf': 'ꭧ',
    'tʃ': 'ʧ',
    'ts': 'ʦ',
    'dʒ': 'ʤ',
    'aɪ': 'I',
    'aʊ': 'W',
    'ɔø': 'ʋ',
    'ɔʏ': 'ʋ',  # the usual dictionary spelling of German eu/äu
    'eɪ': 'eː',  # not A/O: kikiri-german saw A 4 times and O never in training
    'oʊ': 'oː',
}

# In the canonical set, but (almost) never in the kikiri-german training data (data/hui_qwen/train.txt,
# counted 2026-10-04), so the acoustic model cannot say them. Symbol -> (occurrences, substitute).
# æ, ʌ and θ are allowed on purpose: they are planned finetuning targets (finetune_sentences.txt).
RARELY_TRAINED = {
    'ʔ': (0, 'leave it out'),
    'n̩': (0, 'ən'),
    'l̩': (55, 'əl'),
    'ʁ': (3, 'r before a vowel, else ɾ'),
    'A': (4, 'eː'),
    'O': (0, 'oː'),
    'ᵻ': (0, 'ɪ'),
    'ɚ': (0, 'ɜ'),
    'ɹ': (45, 'r before a vowel, else ɾ'),
    'w': (33, 'v'),
    'ð': (5, 'd or z'),
    'ɒ': (81, 'ɔ'),
}


def check_overrides() -> List[str]:
    '''Return a list of violation messages; empty if all overrides are clean.'''
    raw = load_raw_overrides()
    violations = []
    for section in SECTIONS:
        for key, value in raw.get(section, {}).items():
            where = f'{section}.{key!r}: {value!r}'
            for bad, good in UNCOMPRESSED.items():
                if bad in value:
                    violations.append(f'{where} contains uncompressed {bad!r} (use {good!r})')
            if COMBINING_TILDE in value:
                violations.append(f'{where} contains a nasalized vowel (use {value.replace(COMBINING_TILDE, "")!r})')
            unknown = sorted(set(unknown_symbols(value)) - {COMBINING_TILDE})
            if unknown:
                violations.append(f'{where} contains symbols outside the canonical set: {unknown}')
            for symbol in sorted(set(split_symbols(value)) & set(RARELY_TRAINED)):
                count, substitute = RARELY_TRAINED[symbol]
                violations.append(f'{where} contains {symbol!r}, trained only {count} times (use {substitute})')
    return violations


def main() -> int:
    violations = check_overrides()
    if violations:
        print(f'{len(violations)} override violation(s):')
        for v in violations:
            print(f'  {v}')
        return 1
    print('OK: all override phonemes are canonical.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
