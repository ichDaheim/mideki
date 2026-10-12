"""Golden output: fixed sentences with their expected word-mode phonemes.

Downstream models were trained on mideki's word-mode output, so any change to
it (overrides, normalization, postprocessing, espeak-ng) changes their
training distribution. `data/golden_de.tsv` records the current output for a
representative set of sentences; `check_golden()` reports every deviation.

`output_fingerprint()` identifies the phoneme output of a release: a hash
over the golden cases and the override lexicon. Store it with trained models
next to `token_map_sha256()` and compare at load time.

    mideki-check-golden            # verify this installation
    mideki-check-golden --update   # rewrite expected outputs after a deliberate change

File format: `text<TAB>phonemes` per line, `#` starts a comment line. Lines
without a tab are new inputs; `--update` fills in their phonemes.
"""

from __future__ import annotations

import hashlib
import json
import sys
from importlib.resources import files
from typing import List, Optional, Tuple

from .g2p import G2P
from .overrides import load_raw_overrides

_GOLDEN = files('mideki') / 'data' / 'golden_de.tsv'


def _read_lines() -> List[str]:
    return _GOLDEN.read_text(encoding='utf-8').splitlines()


def golden_cases() -> List[Tuple[str, str]]:
    '''(text, expected phonemes) pairs from `data/golden_de.tsv`.'''
    cases = []
    for line in _read_lines():
        if not line.strip() or line.startswith('#'):
            continue
        text, sep, expected = line.partition('\t')
        if not sep:
            raise ValueError(f'golden_de.tsv: no expected output for {text!r} (run mideki-check-golden --update)')
        cases.append((text, expected))
    return cases


def output_fingerprint() -> str:
    '''SHA-256 identifying the phoneme output: golden cases plus override lexicon.

    Computed from parsed content, so line endings and the overrides' `_comment`
    don't affect it.
    '''
    raw = load_raw_overrides()
    lexicon = {key: value for key, value in raw.items() if not key.startswith('_')}
    payload = json.dumps(
        {'golden': golden_cases(), 'overrides': lexicon},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def check_golden(g2p: Optional[G2P] = None) -> List[str]:
    '''Mismatches between the current word-mode output and the golden file.'''
    g2p = g2p or G2P()
    mismatches = []
    for text, expected in golden_cases():
        actual = g2p(text)[0]
        if actual != expected:
            mismatches.append(f'{text!r}\n    expected: {expected}\n    actual:   {actual}')
    return mismatches


def update_golden(path: str) -> int:
    '''Rewrite the expected outputs in `path` from the current output. Returns #changed lines.'''
    g2p = G2P()
    with open(path, encoding='utf-8') as f:
        lines = f.read().splitlines()
    out, changed = [], 0
    for line in lines:
        if not line.strip() or line.startswith('#'):
            out.append(line)
            continue
        text = line.partition('\t')[0]
        new = f'{text}\t{g2p(text)[0]}'
        changed += new != line
        out.append(new)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    return changed


def main() -> int:
    if sys.argv[1:] == ['--update']:
        # Writes the source file; only meaningful in an editable/source checkout.
        path = str(_GOLDEN)
        changed = update_golden(path)
        print(f'{changed} line(s) updated in {path}')
        print(f'output_fingerprint: {output_fingerprint()}')
        return 0
    if sys.argv[1:]:
        print('usage: mideki-check-golden [--update]')
        return 2
    mismatches = check_golden()
    if mismatches:
        print(f'{len(mismatches)} golden mismatch(es):')
        for m in mismatches:
            print(f'  {m}')
        return 1
    print(f'OK: {len(golden_cases())} golden cases match.')
    print(f'output_fingerprint: {output_fingerprint()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
