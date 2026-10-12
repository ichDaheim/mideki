"""Canonical German phoneme symbol set and token map.

`token_map_de.json` is the numbering authority for every model trained on
top of mideki (PL-BERT-de, ASR-de, kikiri-german). It is append-only:
once a model has been trained, existing IDs must never change.

Some canonical symbols span two code points (`l̩`, `n̩`: consonant plus
combining syllabic mark), so phoneme strings must be split with a
longest-match tokenizer, never code point by code point.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from importlib.resources import files
from typing import Dict, List, Optional, Tuple

_DATA = files('mideki') / 'data'

# Espeak-ng transliteration artifact kept in the token map for ID stability
# (see NOTICE.md, "aneinander"). It never carries a real sound.
ARTIFACT_SYMBOLS = frozenset({'1'})


def _read_json(name: str) -> dict:
    return json.loads((_DATA / name).read_text(encoding='utf-8'))


@lru_cache(maxsize=None)
def token_map() -> dict:
    '''The raw `token_map_de.json` (special tokens, symbol IDs, vocab size).'''
    return _read_json('token_map_de.json')


@lru_cache(maxsize=None)
def phoneme_set() -> dict:
    '''The raw `phoneme_set_de.json` (symbols grouped by category, with descriptions).'''
    return _read_json('phoneme_set_de.json')


def token_map_sha256() -> str:
    '''SHA-256 of `token_map_de.json` as shipped, used to pin trained models to a vocabulary.'''
    return hashlib.sha256((_DATA / 'token_map_de.json').read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def symbols() -> Tuple[str, ...]:
    '''All canonical symbols (phonemes, markers, punctuation) in ID order.'''
    symbol_to_id: Dict[str, int] = token_map()['symbol_to_id']
    return tuple(sorted(symbol_to_id, key=symbol_to_id.__getitem__))


@lru_cache(maxsize=None)
def punctuation_symbols() -> Tuple[str, ...]:
    '''The canonical punctuation symbols, passed through literally by the G2P.'''
    return tuple(entry['symbol'] for entry in phoneme_set()['categories']['punctuation'])


@lru_cache(maxsize=None)
def _by_length() -> Tuple[Tuple[int, frozenset], ...]:
    lengths: Dict[int, set] = {}
    for symbol in symbols():
        lengths.setdefault(len(symbol), set()).add(symbol)
    return tuple((n, frozenset(lengths[n])) for n in sorted(lengths, reverse=True))


def split_symbols(phonemes: str) -> List[Optional[str]]:
    '''Split a phoneme string into canonical symbols by longest match.

    Spaces are returned as `' '` (word boundaries). Characters that are not
    part of any canonical symbol are returned as `None` at their position,
    so callers decide whether that is an error or an `[UNK]`.
    '''
    out: List[Optional[str]] = []
    i = 0
    while i < len(phonemes):
        if phonemes[i] == ' ':
            out.append(' ')
            i += 1
            continue
        for n, group in _by_length():
            candidate = phonemes[i:i + n]
            if len(candidate) == n and candidate in group:
                out.append(candidate)
                i += n
                break
        else:
            out.append(None)
            i += 1
    return out


def unknown_symbols(phonemes: str) -> List[str]:
    '''Characters in `phonemes` that do not belong to any canonical symbol.'''
    unknown = []
    i = 0
    for piece in split_symbols(phonemes):
        if piece is None:
            unknown.append(phonemes[i])
            i += 1
        else:
            i += len(piece)
    return unknown
