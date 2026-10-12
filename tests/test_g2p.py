import pytest

from mideki import (
    G2P,
    check_overrides,
    normalize_text_de,
    render,
    split_symbols,
    symbols,
    token_map,
    unknown_symbols,
)


@pytest.fixture(scope='module')
def g2p():
    return G2P()


def test_token_map_is_dense_and_consistent():
    tm = token_map()
    ids = sorted(list(tm['special_tokens'].values()) + list(tm['symbol_to_id'].values()))
    assert ids == list(range(tm['vocab_size']))
    assert tm['vocab_size'] == 105
    assert len(symbols()) == 100


def test_split_symbols_longest_match():
    # l̩ is two code points but one symbol.
    assert split_symbols('rˈɛːʦl̩') == ['r', 'ˈ', 'ɛ', 'ː', 'ʦ', 'l̩']
    assert split_symbols('a b') == ['a', ' ', 'b']
    assert split_symbols('a§') == ['a', None]
    assert unknown_symbols('a§b') == ['§']


def test_overrides_are_canonical():
    assert check_overrides() == []


@pytest.mark.parametrize('text, expected', [
    ('Zeit', 'ʦˈIt'),
    ('Pfote', 'ꭧˈoːtə'),
    ('Kopf', 'kˈɔꭧ'),
    ('Heu', 'hˈʋ'),
    ('Rätsel', 'rˈɛːʦl̩'),
    ('sakrale', 'zakɾˈɑːlə'),
])
def test_known_words(g2p, text, expected):
    assert g2p(text)[0] == expected


def test_word_mode_output_is_canonical(g2p):
    ps, _ = g2p('Am 3.10.2026 kostete das 12,50 € (inkl. Versand) – oder?')
    assert unknown_symbols(ps.replace(' ', '')) == []


def test_word_mode_uses_citation_stress(g2p):
    # Every content word carries its own stress in word mode; sentence mode may drop it.
    word = g2p('Er ging um die Ecke.')[0]
    sentence = G2P('sentence')('Er ging um die Ecke.')[0]
    assert word.count('ˈ') >= sentence.count('ˈ')


def test_overrides_are_applied(g2p):
    assert g2p('PyTorch')[0] == 'pˈItɔːɾʧ'  # ɹ replaced by ɾ (ɹ: 45 times in the training data)


def test_word_cache_is_filled_and_reused():
    cache = {}
    g2p = G2P(cache=cache)
    first = g2p('Hallo Welt')[0]
    assert set(cache) == {'Hallo', 'Welt'}
    cache['Welt'] = 'X'
    assert g2p('Hallo Welt')[0] != first


def test_normalization():
    assert normalize_text_de('z. B. 3 Äpfel') == 'zum Beispiel drei Äpfel'
    assert normalize_text_de('um 14:30 Uhr') == 'um vierzehn Uhr dreißig'


def test_render_attaches_trailing_punctuation():
    assert render(['a', ',', 'b', '.']) == 'a, b.'


def test_invalid_mode():
    with pytest.raises(ValueError):
        G2P(mode='phrase')
