# Changelog

Versionierung (siehe README, Abschnitt „Versionierung“):

- **MAJOR**: inkompatible API-Änderung oder Bruch der Token-Map.
- **MINOR**: Die Phonem-Ausgabe ändert sich für irgendeine Eingabe (Overrides,
  Normalisierung, Kompression, espeak-ng). Modelle, die auf einer älteren MINOR-Version
  trainiert wurden, sehen dann eine andere Eingabeverteilung.
- **PATCH**: Die Ausgabe bleibt bitgenau gleich (Bugfixes ohne Ausgabeänderung, Doku,
  Performance).

Jeder Eintrag nennt `output_fingerprint()` und `token_map_sha256()` der Version;
`tests/test_versioning.py` prüft, dass der Eintrag der aktuellen Version den aktuellen
Fingerabdruck enthält.

## 1.1.0 – 2026-10-18

- output_fingerprint: `62b0b6ef62563fde6a9b39407266de49dab18855f24f87528fc164269572945e`
- token_map_sha256: `3af12687579c50956ab35be02ab38da1b8d1f1713362266dc76c8e1729e95724`

85 neue Overrides, keine bestehenden geändert oder entfernt. Die Golden-Sätze sind unverändert.

- `en`: u. a. Trump/Donald Trump, live und Live-Komposita (Livemusik, Livestream …), online/offline mit Komposita,
  Wallet, Store, Times/Financial Times, iPhone, Tucson.
- `de_foreign`: u. a. Macron, Elysée-Palast, Kanada/Kanadier, Latino/Latina, Arizona, Patagonien, US, US-Kongress,
  Illegalität, Girokonto/Girocard, Handys.
- `de_native`: u. a. geplant (mit Beugungsformen), Krawall, Massenprotest, vorherrschend/Vorherrschaft, EU und
  EU-Komposita, Knappheit, Mobilfunkprovider.
- `brand`: Bloomberg.

## 1.0.0 – 2026-10-12

- output_fingerprint: `e8abfdb49e61096ac178d4beb12d7b481d0c4d9d029f0e94ca2274e15167fb60`
- token_map_sha256: `3af12687579c50956ab35be02ab38da1b8d1f1713362266dc76c8e1729e95724`

Erste Veröffentlichung. Die Ausgabe im Wortmodus entspricht dem Stand, auf dem
PL-BERT-de, ASR-de und kikiri-german trainiert wurden.
