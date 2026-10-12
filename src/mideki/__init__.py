"""mideki: German grapheme-to-phoneme conversion with a canonical symbol set."""

from importlib.metadata import version as _version

from .g2p import G2P, render
from .golden import check_golden, golden_cases, output_fingerprint
from .normalize import normalize_text_de
from .override_checks import check_overrides
from .overrides import override_for
from .segment import Segment, segment_text
from .symbols import (
    phoneme_set,
    punctuation_symbols,
    split_symbols,
    symbols,
    token_map,
    token_map_sha256,
    unknown_symbols,
)

__version__ = _version('mideki')

__all__ = [
    'G2P',
    'Segment',
    'check_golden',
    'check_overrides',
    'golden_cases',
    'normalize_text_de',
    'output_fingerprint',
    'override_for',
    'phoneme_set',
    'punctuation_symbols',
    'render',
    'segment_text',
    'split_symbols',
    'symbols',
    'token_map',
    'token_map_sha256',
    'unknown_symbols',
]
