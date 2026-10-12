# mideki

Deutsche Graphem-zu-Phonem-Umwandlung (G2P) mit einem kanonischen, versionierten
Phonem-Symbolset. Grundlage für kikiri-german.

```python
from mideki import G2P

g2p = G2P()                   # Wortmodus (Standard)
phonemes, _ = g2p('Die sakrale Kirche öffnet um 14:30 Uhr.')
# 'diː zakɾˈɑːlə kˈɪɾçə ˈœfnət ˈʊm fˈiːɾʦeːn ˈuːɾ dɾˈIsɪç.'
```

## Was das Paket macht

1. **Normalisierung**: Zahlen, Datumsangaben, Uhrzeiten, Währungen, Abkürzungen und
   Telefonnummern werden ausgeschrieben (`normalize_text_de`).
2. **Overrides**: Für Marken, Anglizismen und Wörter, die espeak-ng falsch ausspricht,
   gibt es handgeschriebene Phoneme (`data/de_overrides.json`).
3. **espeak-ng**: Alles andere phonemisiert espeak-ng 1.52.0 (gebündelt über
   `espeakng-loader`, nie die System-Installation).
4. **Kompression**: Diphthonge und Affrikaten werden zu je einem Symbol zusammengefasst
   (`aɪ`→`I`, `aʊ`→`W`, `ɔø`→`ʋ`, `ts`→`ʦ`, `tʃ`→`ʧ`, `pf`→`ꭧ`), Nasalvokale entnasaliert.

## Wortmodus und Satzmodus

- `G2P()` bzw. `G2P(mode='word')` phonemisiert jedes Wort einzeln (Zitierform, jedes
  Inhaltswort betont). So wurden die Trainingsdaten von PL-BERT-de, ASR-de und kikiri-german
  erzeugt. **Modelle, die darauf trainiert sind, brauchen diesen Modus auch bei der Inferenz.**
- `G2P(mode='sentence')` gibt espeak-ng den ganzen Satz, die Betonung verteilt sich über
  den Satz. Nur zum Vergleich.

Im Wortmodus lässt sich über `G2P(cache=...)` ein Wort-Cache übergeben, damit große
Korpora nicht mehrfach durch espeak-ng laufen.

## Symbolset

`token_map_de.json` (105 Einträge: 5 Sonder-Token, 100 Symbole) ist die Nummerierungs-Autorität
für alle darauf trainierten Modelle und darf nur erweitert, nie umnummeriert werden.
`phoneme_set_de.json` beschreibt jedes Symbol mit Beispiel und Häufigkeit.
Einige Symbole bestehen aus zwei Codepoints (`l̩`, `n̩`); Phonem-Strings deshalb immer mit
`split_symbols()` zerlegen, nie zeichenweise.

## Versionierung

Die Downstream-Modelle hängen an zwei Dingen, die getrennt abgesichert sind:

- **Token-IDs**: `token_map_de.json` wird nur erweitert; `token_map_sha256()` identifiziert sie.
- **Phonem-Ausgabe**: `output_fingerprint()` identifiziert sie (Hash über die
  Golden-Sätze in `data/golden_de.tsv` und das Override-Lexikon).

Beide Hashes gehören in jeden Modell-Checkpoint und sollten beim Laden verglichen werden.

Versionsnummern folgen [SemVer](https://semver.org/lang/de/), bezogen auf die Ausgabe:
MAJOR = API- oder Token-Map-Bruch, **MINOR = Phonem-Ausgabe ändert sich**,
PATCH = Ausgabe bitgenau gleich. Projekte pinnen daher auf MINOR:

```toml
dependencies = ["mideki~=1.0.0"]   # 1.0.x, aber nicht 1.1
# oder ohne PyPI, per Git-Tag:
dependencies = ["mideki @ git+https://github.com/ichDaheim/mideki@v1.0.0"]
```

`mideki-check-golden` prüft, ob eine Installation die erwartete Ausgabe erzeugt
(z. B. nach einem Plattformwechsel).

### Ablauf bei Änderungen an Overrides oder Logik

1. Änderung machen; `uv run pytest` zeigt in `test_golden_output_unchanged` jede
   veränderte Ausgabe.
2. Ist die Änderung gewollt: `uv run mideki-check-golden --update` schreibt die neuen
   Ausgaben nach `data/golden_de.tsv` und gibt den neuen Fingerabdruck aus. Für neues
   Verhalten neue Sätze (nur Text, ohne Tab) in die Datei eintragen, `--update` ergänzt sie.
3. MINOR-Version in `pyproject.toml` erhöhen, Eintrag mit beiden Hashes in
   `CHANGELOG.md`; `test_changelog_records_current_fingerprints` erzwingt das.
4. Commit, dann Tag `vX.Y.Z` setzen und pushen.

## Entwicklung

```bash
uv sync
uv run pytest
uv run mideki-check-overrides                   # nach jeder Änderung an de_overrides.json
uv run mideki-check-golden                      # Golden-Ausgabe prüfen (--update nach gewollter Änderung)
```

Lizenz: Apache 2.0. Herkunft und Änderungen: siehe `NOTICE.md`.
