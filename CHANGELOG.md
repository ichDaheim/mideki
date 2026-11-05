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

## 1.2.0 – 2026-11-05

- output_fingerprint: `055b8a2860f7976181dce6650632111e0eaf1ff70d11d306f79140148dca21de`
- token_map_sha256: `3af12687579c50956ab35be02ab38da1b8d1f1713362266dc76c8e1729e95724`

344 neue Overrides, 14 bestehende geändert, keine entfernt. Fünf Golden-Sätze ändern sich (CUDA, Ollama, Learning,
Chance, Fan).

- `en`: u. a. Gaming-Begriffe (Shooter/Ego-Shooter/First-Person-Shooter, Gamer, E-Sport/E-Sportler, Counter-Strike,
  Playstation, Quake, Duke Nukem, X-Wing, TIE Fighter, Joystick, Cursor), Fan, The Guardian, Joe Biden, Supreme Court,
  Midterms, Blazer, Rancher, Vote.
- `de_foreign`: u. a. Rakete mit über 100 Komposita, Marschflugkörper, Bilanz, Konsequenz/konsequent, Container,
  Initiative, positiv, Chance, Devise(n), Psychotherapie, Selenskyj, Arena, Display/Handydisplay, X-/Y-/Z-Achse, Pilot
  (Pilotprojekt, Autopilot, Copilot), Profi mit Komposita (Profisport, Fußballprofi …), Controller, Spiel-/Filmstudio.
- `de_native`: u. a. Wasserknappheit, betont, Verankerung/verankert, Suchthilfe, Hansestadt, Gesäßtasche,
  (Erd-)Gasförderung, Profispieler, Fehlanzeige, suboptimal, letztendlich, Studienteilnehmer.
- Geändert: Auslaut-„a“ als `ɑː` statt `a` (CUDA, Llama, Ollama, Nvidia, Samantha, North Carolina, Latina, Arizona,
  Patagonia, Kanada); englisches `ɜː` durch `œɾ` ersetzt (BERT, Surface, Learning), weil `ɜ` im Training nur die
  deutsche „-er“-Endung ist; Fans `fˈɛns` → `fˈæns`.

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
