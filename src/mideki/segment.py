"""Split normalized German text into word segments for word-level phonemization.

Mirrors the control flow of `G2P` in sentence mode (overrides are matched on
the full normalized word list, spanning up to four words), but leaves plain
words unphonemized so that callers can batch and cache espeak-ng calls.

Canonical punctuation symbols become their own literal segments. Anything
that is neither a word nor canonical punctuation (dashes, currency and math
symbols, emoji, control characters) is dropped instead of being passed
through as a fake phoneme.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

import regex

from .overrides import OVERRIDE_WORD_RE, find_phrase_override
from .symbols import punctuation_symbols

_WORD_CHAR = r'[\p{L}\p{M}\d]'
_WORD_PATTERN = rf"{_WORD_CHAR}+(?:['\-]{_WORD_CHAR}+)*"
_WORD_RE = regex.compile(_WORD_PATTERN)


@dataclass
class Segment:
    surface: str
    phonemes: Optional[str]  # None: still to be phonemized by espeak-ng
    source: str  # 'override' | 'espeak' | 'literal'


@lru_cache(maxsize=None)
def _token_re() -> 'regex.Pattern':
    punct_class = ''.join(regex.escape(c) for c in punctuation_symbols())
    return regex.compile(rf'{_WORD_PATTERN}|[{punct_class}]|\S')


def tokenize_words(text: str) -> List[str]:
    '''Split normalized text into words, punctuation and other single characters.'''
    return _token_re().findall(text) if text else []


def is_word(token: str) -> bool:
    return bool(_WORD_RE.fullmatch(token))


def is_canonical_punct(token: str) -> bool:
    return token in punctuation_symbols()


def _plain_segments(span: str) -> List[Segment]:
    out = []
    for token in tokenize_words(span):
        if is_word(token):
            out.append(Segment(token, None, 'espeak'))
        elif is_canonical_punct(token):
            out.append(Segment(token, token, 'literal'))
    return out


def segment_text(normalized_text: str) -> List[Segment]:
    '''Segment text that has already been passed through `normalize_text_de`.'''
    segments: List[Segment] = []
    matches = list(OVERRIDE_WORD_RE.finditer(normalized_text))
    cursor = 0
    i = 0
    while i < len(matches):
        match = matches[i]
        end_index, phonemes = find_phrase_override(normalized_text, matches, i)
        if phonemes is None:
            i += 1
            continue
        preceding = normalized_text[cursor:match.start()]
        if preceding.strip():
            segments.extend(_plain_segments(preceding))
        surface = normalized_text[match.start():matches[end_index].end()]
        segments.append(Segment(surface, phonemes, 'override'))
        cursor = matches[end_index].end()
        i = end_index + 1
    trailing = normalized_text[cursor:]
    if trailing.strip():
        segments.extend(_plain_segments(trailing))
    return segments
