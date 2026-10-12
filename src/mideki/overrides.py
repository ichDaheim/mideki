"""Pronunciation overrides: hand-written phonemes for words espeak-ng gets wrong.

A small lexicon layer on top of espeak-ng for English/brand/tech terms
(GitHub, PyTorch, CUDA, ...), a few foreign-origin German words and native
German words that espeak-ng garbles (`de_native`). Override phonemes bypass
espeak-ng and therefore must already use the compressed canonical symbols;
`override_checks.check_overrides` enforces that.

Lookup keys are matched after `normalize_for_lookup()`: casefold, NFKD, strip
combining marks, fold "+" -> "plus", "&" -> "and", "@" -> "at", keep
alphanumerics. Ported from the semidark/misaki fork (Apache License 2.0).
"""

import json
import re
import unicodedata
from importlib.resources import files
from typing import List, Optional, Tuple

SECTIONS = ('brand', 'en', 'de_foreign', 'de_native')
MAX_OVERRIDE_TOKENS = 4

_LOOKUP_REPLACEMENTS = {'+': 'plus', '&': 'and', '@': 'at'}

# Word-ish tokens for override matching. Captures internal "-"/"'" (espeak-ng,
# zero-shot) and a trailing "+" (Disney+) so single tokens with joiners match
# their normalized override key. Space-separated multi-word brands are not
# matched here by design.
OVERRIDE_WORD_RE = re.compile(
    r"[0-9A-Za-zÀ-ÖØ-öø-ÿß]+(?:['\-][0-9A-Za-zÀ-ÖØ-öø-ÿß]+)*\+?"
)


def normalize_for_lookup(text: str) -> str:
    '''Collapse a word to its override lookup key ("Prime Video" -> "primevideo").'''
    text = unicodedata.normalize('NFKD', text.casefold())
    parts = []
    for char in text:
        if unicodedata.category(char) == 'Mn':
            continue
        replacement = _LOOKUP_REPLACEMENTS.get(char)
        if replacement is not None:
            parts.append(replacement)
        elif char.isalnum():
            parts.append(char)
    return ''.join(parts)


def load_raw_overrides() -> dict:
    '''The raw `de_overrides.json` content.'''
    path = files('mideki') / 'data' / 'de_overrides.json'
    return json.loads(path.read_text(encoding='utf-8'))


def _build_lookup():
    # Priority on key collisions: brand > en > de_foreign > de_native (first writer wins).
    raw = load_raw_overrides()
    lookup = {}
    for section in SECTIONS:
        for key, value in raw.get(section, {}).items():
            lookup.setdefault(normalize_for_lookup(key), value)
    aliases = {normalize_for_lookup(k): normalize_for_lookup(v) for k, v in raw.get('aliases', {}).items()}
    return lookup, aliases


_OVERRIDES, _OVERRIDE_ALIASES = _build_lookup()


def override_for(text: str) -> Optional[str]:
    '''Override phonemes for a word or phrase, or None if it is not overridden.'''
    key = normalize_for_lookup(text)
    if not key:
        return None
    key = _OVERRIDE_ALIASES.get(key, key)
    return _OVERRIDES.get(key)


def find_phrase_override(text: str, matches: List[re.Match], start_index: int) -> Tuple[Optional[int], Optional[str]]:
    '''Longest override starting at `matches[start_index]`, spanning up to MAX_OVERRIDE_TOKENS words.

    Returns `(end_index, phonemes)` with `end_index` inclusive, or `(None, None)`.
    '''
    max_end = min(len(matches), start_index + MAX_OVERRIDE_TOKENS)
    for end_index in range(max_end, start_index, -1):
        start = matches[start_index].start()
        end = matches[end_index - 1].end()
        phonemes = override_for(text[start:end])
        if phonemes is not None:
            return end_index - 1, phonemes
    return None, None
