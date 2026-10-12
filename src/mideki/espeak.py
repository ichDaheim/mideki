"""espeak-ng phonemization for German with symbol compression.

Derived from `EspeakG2P` in misaki/espeak.py (hexgrad/misaki, Apache License
2.0), modified as described in NOTICE.md:

- The tie-compression table only contains sequences that occur in German
  espeak-ng output (a^ɪ -> I, a^ʊ -> W, ɔ^ø -> ʋ, t^s -> ʦ, t^ʃ -> ʧ,
  p^f -> ꭧ, d^ʒ -> ʤ, d^z -> ʣ, s^s -> S).
- Untied pf/tʃ/ts are compressed as well, independent of position. espeak-ng
  only tie-marks them word-initially, but "Kopf" and "Pfote" contain the same
  affricate.
- Nasal vowels are denasalized (combining tilde removed). espeak-ng nasalizes
  French loanwords inconsistently and the training audio has almost no
  nasalized vowels, so a dedicated symbol would stay untrained.

phonemizer is pinned to the espeak-ng build bundled with `espeakng-loader`
(espeak-ng 1.52.0). A system espeak-ng 1.50 mispronounces German "ur" before
a consonant ("Wurm", "kurz"). Do not fall back to the system installation.
"""

from typing import List, Tuple

import espeakng_loader
import phonemizer
from phonemizer.backend.espeak.wrapper import EspeakWrapper

EspeakWrapper.set_library(espeakng_loader.get_library_path())
EspeakWrapper.set_data_path(espeakng_loader.get_data_path())

# Tie sequence -> single symbol, German subset only.
TIE_COMPRESSION = (
    ('a^ɪ', 'I'),
    ('a^ʊ', 'W'),
    ('d^z', 'ʣ'),
    ('d^ʒ', 'ʤ'),
    ('p^f', 'ꭧ'),
    ('s^s', 'S'),
    ('t^s', 'ʦ'),
    ('t^ʃ', 'ʧ'),
    ('ɔ^ø', 'ʋ'),  # German eu/äu, e.g. "Heu" (espeak-de ties ɔ^ø, not ɔ^ɪ)
)
UNTIED_AFFRICATES = (('pf', 'ꭧ'), ('tʃ', 'ʧ'), ('ts', 'ʦ'))
COMBINING_TILDE = '̃'


def postprocess(raw: str) -> str:
    '''Apply the German symbol compression to raw espeak-ng output.

    Shared by sentence and word phonemization so both produce identical
    symbols for the same espeak-ng output.
    '''
    ps = raw
    for old, new in TIE_COMPRESSION:
        ps = ps.replace(old, new)
    # Remaining tie characters and hyphens carry no sound.
    ps = ps.replace('^', '').replace('-', '')
    for old, new in UNTIED_AFFRICATES:
        ps = ps.replace(old, new)
    ps = ps.replace(COMBINING_TILDE, '')
    return ps.strip()


class EspeakG2P:
    '''German espeak-ng phonemization with symbol compression.'''

    def __init__(self, language: str = 'de'):
        self.language = language
        self.backend = phonemizer.backend.EspeakBackend(
            language=language,
            preserve_punctuation=True,
            with_stress=True,
            tie='^',
            language_switch='remove-flags',
        )

    def __call__(self, text: str) -> Tuple[str, None]:
        '''Phonemize a whole text span in sentence context.'''
        # Parentheses would be dropped by espeak-ng; route them through guillemets.
        text = text.replace('«', chr(8220)).replace('»', chr(8221))
        text = text.replace('(', '«').replace(')', '»')
        ps = self.backend.phonemize([text])
        if not ps:
            return '', None
        ps = postprocess(ps[0])
        ps = ps.replace('«', '(').replace('»', ')')
        return ps, None

    def phonemize_words(self, words: List[str]) -> List[str]:
        '''Phonemize each word in isolation (citation form), in one espeak-ng call.

        Words must not contain spaces or punctuation; see `segment.segment_text`.
        '''
        if not words:
            return []
        return [postprocess(ps) for ps in self.backend.phonemize(list(words))]
