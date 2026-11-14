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

## 1.4.0 – 2026-11-14

- output_fingerprint: `cd4a3502bf5abe304bcd43c50a707c8d9b118a334581f10a03b27ef76d1ca7b7`
- token_map_sha256: `3af12687579c50956ab35be02ab38da1b8d1f1713362266dc76c8e1729e95724`

436 neue Overrides, einer geändert (`ki`), keine entfernt. Ein Golden-Satz ändert sich
(„… mit KI und Machine Learning.“: `kˌɑːˈiː` → `kˈɑː ˈiː`).

- Normalisierung: KByte/kByte, MByte, GByte, TByte, PByte (auch mit Plural-s) werden zu
  Kilobyte, Megabyte, Gigabyte, Terabyte, Petabyte ausgeschrieben. Bisher buchstabierte
  espeak-ng das Präfix („GByte“ → `ɡˈeː bˈIt`).
- Normalisierung: Hz, kHz/KHz, MHz/Mhz, GHz/Ghz, THz werden zu Hertz, Kilohertz,
  Megahertz, Gigahertz, Terahertz ausgeschrieben (bisher buchstabiert: „GHz“ →
  `ɡˌeːhˌɑːʦˈɛt`). „mHz“ (Millihertz) bleibt unverändert.
- Normalisierung: Bindestriche an einer Byte- oder Hertz-Einheit werden zu Leerzeichen, und
  „1“ davor wird „ein“: „1-TByte-SSD“ → „ein Terabyte SSD“, „1 GHz“ → „ein Gigahertz“
  (bisher ging das Kompositum als Ganzes an espeak-ng, am Override vorbei:
  `…tˈeːrabˌyːtə…`).
- `brand`: ChatGPT(s), GPT(s), GPT-drei/-vier/-fünf, GPT-4o, GPT-4o-mini (englisch
  buchstabiert, `ʤˌiːpiːtˈiː`); Microsoft(s); Touch-MacBook.
- `en`: Prompt(s), Prompting, Prompt-Engineering(s), Agents, AI-Agents, agentic, Tool Use;
  Performance, Core(s), Neural Engine(s), Cloud(s); High School(s)/Highschool(s), CEO(s);
  Area Control Centre/Center(s), Federal Aviation Administration, Ground Stop(s);
  Elon Musk(s), Musk(s).
- `de_foreign`:
  - `ki` jetzt `kˈɑː ˈiː` (zwei betonte Buchstaben) statt `kˌɑːˈiː`.
  - KI-Komposita mit Leerzeichen nach `ˈiː`: KI-Modell(e/s/en), KI-Unterstützung(en),
    KI-generiert(e/en/er/es/em), KI-Tool(s), KI-Agents, KI-Workflow(s), KI-Aufgabe(n).
    Ohne Override geht ein Bindestrich-Wort als Ganzes an espeak-ng (z. B. „KI-Hersteller“
    → `kˌɑːˈiːhˈɛɾʃtɛlɜ`).
  - Kilo-/Mega-/Giga-/Tera-/Petabyte(s) mit `bˌIt`/`bˌIʦ` (espeak-ng las `bˌyːtə`), dazu
    die Kurzformen kbyte, mbyte, gbyte, tbyte, pbyte(s) für Schreibweisen, die die
    Normalisierung nicht erfasst („Gbyte“, „GBYTE“).
  - Kilo-/Mega-/Giga-/Terahertz mit `hˌɛɾʦ` (espeak-ng verschluckte das h:
    „Gigahertz“ → `ɡˈiːɡɑːɜʦ`).
  - Prompting-Erfahrung(en), Prompt-Vorlage(n).
  - Performancekern(e/s/en), AI-Einheit(en), Supercore(s), Agentin(nen), Webseite(n),
    Medienbericht(e/s/en), Alice(s), FAA, CNN.
  - 160 Komposita auf -problem (je mit -e/-en/-s), z. B. Kommunikations-, Sicherheits-,
    Gesundheits-, Verbindungs-, Qualitäts-, Liquiditäts-, Wirtschafts-, Luxus-, Rechtsproblem
    (Hauptbetonung auf dem Bestimmungswort, `pɾoblˌeːm` mit Nebenbetonung; espeak-ng:
    „Sicherheitsproblem“ → `zˈɪçɜhˌIʧpɾɔbləm`).
  - Honorar(e/s/en), Honorarkürzung(en).
  - Chef-Wörter mit `ʃˈɛf` (espeak-ng: „Chefin“ → `çˈeːfɪn`): Chefin(nen),
    Fraktionschef(s), Ex-/Vize-Chefin(nen), 23 weitere Komposita auf -chefin(nen) (Partei-, Konzern-, Regierungs-, Bundesbank-, Polizei-,
    Geheimdienstchefin …), dazu Chefarzt/-ärztin, Chefkoch/-köchin, Chefredakteur(in),
    Chefredaktion, Chefetage(n), Chefsache, Chefsessel, Chefposten, Chefökonom(in),
    Chefermittler(in), Chefankläger(in), Chefdiplomat(in), Chefstratege/-strategin,
    Chefvolkswirt(in), Chefentwickler(in), Chefideologe, Chefdirigent(in), Chefsekretärin,
    Chefunterhändler(in) samt Flexionsformen.
- `de_native`:
  - bergauf, bergab (zwei betonte Teile).
  - Basismodell(e/s/en).
  - Lotse/Lotsin, Fluglotse/Fluglotsin samt Pluralen (espeak-ng: „Lotse“ → `lˈɔtzə`).
  - Sprechstunde(n), Privatsprechstunde(n).
  - HNO (`hˈɑː ˈɛn ˈoː`) und HNO-Komposita: HNO-Arzt/-Ärztin/-Ärzte, HNO-Praxis/-Praxen,
    HNO-Arztpraxis, HNO-Klinik, HNO-Heilkunde, HNO-Bereich.
  - Praxen (espeak-ng: `pɾˈɑːksən`) sowie Arzt-, Hausarzt-, Zahnarzt-, Facharzt-,
    Tierarzt-, Landarztpraxen.

## 1.3.0 – 2026-11-07

- output_fingerprint: `96679055de8b4a9df52057f5f1ee44d97cf8ad4151a9e8c47eaa6264bb08ac45`
- token_map_sha256: `3af12687579c50956ab35be02ab38da1b8d1f1713362266dc76c8e1729e95724`

63 neue Overrides, keine geändert oder entfernt. Golden-Datei unverändert.

- Override-Suche behält Umlaute: `normalize_for_lookup` entfernt ä/ö/ü nicht mehr (andere
  Akzente weiterhin). Bisher griffen Umlaut-Schlüssel auch für die Form ohne Umlaut, z. B.
  wurde „Gasforderung“ als „Gasförderung“ gesprochen; „Singvögel“ hätte „Singvogel“
  überschrieben. Eingaben mit weggelassenen Umlauten („Mullcontainer“) treffen keinen
  Override mehr und gehen an espeak-ng.
- `en`: Ocean Steamship(s).
- `de_foreign`: Vagabund(en) (Betonung auf der letzten Silbe).
- `de_native`: hinweg- mit Formen von blicken, sehen, gehen, täuschen, setzen, kommen,
  helfen, trösten, fegen (Betonung `hɪnvˈɛk…` statt `hˈɪnvɛɡ…`); geatmet (langes `ɑː`) mit ein-/aus-/
  auf-/durch-; Schmalspurbahn(en); Ortschaft(en); Laubbaum/-bäume; Paß; Pfadbiegung(en);
  Singvögel(n) (`f` statt `v`).

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
