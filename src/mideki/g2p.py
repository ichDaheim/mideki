"""G2P: German text -> canonical phoneme string."""

from __future__ import annotations

from typing import Dict, Iterable, List, Literal, MutableMapping, Optional, Tuple

from .espeak import EspeakG2P
from .normalize import normalize_text_de
from .overrides import OVERRIDE_WORD_RE, find_phrase_override
from .segment import segment_text

Mode = Literal['word', 'sentence']

# Punctuation that attaches to the preceding phoneme fragment without a space.
_TRAILING_PUNCT = frozenset('.,!?;:%)]}»”')


def render(parts: Iterable[str]) -> str:
    '''Join phoneme fragments with single spaces, attaching trailing punctuation.'''
    rendered = ''
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if not rendered:
            rendered = part
        elif part[0] in _TRAILING_PUNCT:
            rendered += part
        else:
            rendered += ' ' + part
    return rendered


class G2P:
    '''German G2P: normalize text, apply overrides, phonemize the rest with espeak-ng.

    Two modes with different stress patterns:

    - `'word'` (default): every word is phonemized in isolation (citation form,
      one primary stress per content word). This is how PL-BERT-de, ASR-de
      and the kikiri-german training data were phonemized, so models trained on
      them must be fed word-mode phonemes at inference time too.
    - `'sentence'`: espeak-ng sees the whole span and distributes stress over
      the sentence. Kept for comparison; not compatible with the models above.

    Args:
        mode: `'word'` or `'sentence'`.
        cache: optional mapping `word -> phonemes` used in word mode. Pass a
            persistent dict to avoid re-running espeak-ng for known words.
    '''

    def __init__(self, mode: Mode = 'word', cache: Optional[MutableMapping[str, str]] = None):
        if mode not in ('word', 'sentence'):
            raise ValueError(f"mode must be 'word' or 'sentence', got {mode!r}")
        self.mode = mode
        self.cache: MutableMapping[str, str] = {} if cache is None else cache
        self.espeak = EspeakG2P(language='de')

    def __call__(self, text: str) -> Tuple[str, None]:
        normalized = normalize_text_de(text)
        if self.mode == 'word':
            return self._word_mode(normalized), None
        return self._sentence_mode(normalized), None

    def phonemize_words(self, words: Iterable[str]) -> Dict[str, str]:
        '''Phonemize words in isolation, using and filling the cache.'''
        missing = sorted({w for w in words if w not in self.cache})
        for word, phonemes in zip(missing, self.espeak.phonemize_words(missing)):
            self.cache[word] = phonemes
        return {w: self.cache[w] for w in words}

    def _word_mode(self, normalized: str) -> str:
        segments = segment_text(normalized)
        resolved = self.phonemize_words([s.surface for s in segments if s.phonemes is None])
        return render(s.phonemes if s.phonemes is not None else resolved[s.surface] for s in segments)

    def _sentence_mode(self, normalized: str) -> str:
        # Overrides replace their span; everything between them goes to espeak-ng in context.
        parts: List[str] = []
        cursor = 0
        matches = list(OVERRIDE_WORD_RE.finditer(normalized))
        i = 0
        while i < len(matches):
            end_index, phonemes = find_phrase_override(normalized, matches, i)
            if phonemes is None:
                i += 1
                continue
            preceding = normalized[cursor:matches[i].start()]
            if preceding.strip():
                parts.append(self.espeak(preceding)[0])
            parts.append(phonemes)
            cursor = matches[end_index].end()
            i = end_index + 1
        if cursor == 0:
            return self.espeak(normalized)[0] if normalized.strip() else ''
        trailing = normalized[cursor:]
        if trailing.strip():
            parts.append(self.espeak(trailing)[0])
        return render(parts)
