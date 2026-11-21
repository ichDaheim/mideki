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

## 1.5.0 – 2026-11-16

- output_fingerprint: `b9385613d542545985a6ad95d59410aabeaf3bae67624ba9e77ee59206e1777d`
- token_map_sha256: `3af12687579c50956ab35be02ab38da1b8d1f1713362266dc76c8e1729e95724`

554 neue Overrides, 280 bestehende geändert, keine entfernt. Sechs Golden-Sätze ändern sich: „Das Meeting
wurde gecancelt.“ (`mˈeːtɪŋ` → `mˈiːtɪŋ`, `ɡəkˈankəlt` → `ɡəkˈɛnsəlt`), „Eine Softwarelösung für alle.“
(`zˈɔftvarˌɛløːzˌʊŋ` → `sˈɔftvɛːɐlˌøːzʊŋ`) sowie Ollama, Oase, Prothese und USA (Vokale, siehe unten).

- Normalisierung: Ein Tag ohne Leerzeichen vor dem Monatsnamen wird als Ordinalzahl gelesen („Am 1.Januar“ →
  „Am ersten Januar“, bisher „Am eins.Januar“). Neuer Golden-Satz „Am 3.Mai feiern wir.“

- Geändert: Vokale, die im kikiri-de-Training (train.txt, 2,08 Mio. Wörter) fast nie vorkommen, durch die
  gut trainierte Form ersetzt, die espeak-ng selbst für die Grundwörter liefert: kurzes `o` (20-mal trainiert)
  → `oː` (223 Einträge, v. a. die -problem-Komposita: `pɾoblˌeːm` → `pɾoːblˌeːm`, wie „Problem“ →
  `pɾoːblˈeːm`), `aː` (246) → `ɑː` (37), kurzes `u` (8) → `uː`, kurzes `e` (161) → `eː`, `œː` (17) → `œɾ`,
  kurzes `y` in ü-Wörtern → `ʏ` (Honorarkürzung, Küchenchefin).
- Korrigiert: `fahrzeugmodelle(n)` endete auf `-ɛle(n)` statt `-ɛlə(n)`; `end-to-end` enthielt Punkte
  (`end.tu.end`, also Pausen) → `ˈɛnt tuː ˈɛnt`; `elysée-palast` hatte `eːː` → `eːlizˈeːpalˌast`.

Gefunden beim Schreiben von Ergänzungssätzen für das kikiri-de-Training: Wörter, die espeak-ng falsch liest.
Englisches „ei“ als `ɛɪ`, englisches -y am Wortende als kurzes `i`, `œɾ` statt `ɜː`, `v`/`ɔ` statt `w`/`ɒ`.
Komposita mit englischem Kopfwort liest espeak-ng meist deutsch („Softwarefehler“ → `zˈɔftvarˌeː…`,
„Jobcenter“ → `jɔpkˈɛntɜ`, „Nachtclub“ → `nˈaxtkluːp`); Schlüssel ohne Bindestrich decken die
Bindestrich-Schreibung mit ab.

- `en`:
  - Face, Game(s), Gaming, Gameplay, Hobby, Lobby/Lobbyist(in/en)/Lobbyismus, Story/Storys/Stories, Storyboard,
    Image(s) samt Imagefilm/-schaden/-kampagne (`ˈɪmɪʧ`), Meeting(s), Feature(s), Homeoffice, Coach/Coaching,
    gecancelt/canceln, Interview(s), Weekend(s), Wifi, Wow, Hollywood, Lockdown(s), Burnout, Knockout, Tower,
    Gateway, Workaround, World, Worst Case, Work-Life-Balance, Wordpress, Smartwatch, Hotdog, Blog(s),
    Hotspot(s), Hotline(s), Jogging/joggen/Jogger(in), Girl(s), Flirt/flirten, Nerd(s), E-Learning,
    Songwriter(in), Songtext(e), Clown(s), Sweater, Wireless, Bodyguard(s), Bodybuilding, Body.
  - Englische -y-Wörter mit kurzem `i`: Smoothie, Hoodie, Selfie, Hippie, Cookie, Rookie, Zombie, Barbie,
    Brownie, Teddy, Buddy, Penny, trendy, fancy, crazy, lucky, funny, sunny, Bully, Daily, Comedy, Energy,
    Privacy, Policy, Cherry, Cranberry, Hockey/Eishockey, Jockey, Money, Honey; Plurale und Komposita
    von Party, City, Baby, Lady, Teenager, Rugby, Country, Smiley, Junkie (espeak-ng: „Partys“ → `pˈaɾtyːs`).
  - `ʤ`: Jetlag, Jetset, Jetski, Privatjet, Jumbojet(s), Jazz-Komposita (Jazzband, Jazzclub, Jazzmusik …),
    Job-Komposita (Jobcenter, Jobbörse, Jobsuche, Nebenjob, Minijob, Traumjob …), jobben, Jeansjacke/-hose,
    Gentleman/Gentlemen, Challenge(s), College, Jeep(s), Joker, Jingle, Jukebox, Pager, Engineering,
    managen/gemanagt, Manager- und Management-Komposita (Projektmanager(in), Krisenmanagement …).
  - `æ`: Camping-Komposita, Camper, campen, Hackerangriff(e), Fanclub, Fanshop, Fanmeile, Fußballfans,
    Smartphone-/Handy-App, Feedbacks, Rapperin, Snackbar, Chatverlauf, Sandwichs, Blackouts, Flashmobs,
    Crashtests, Spamfilter, Trackpad, Hackathon, Tackling, Webcam(s).
  - `ʌ`: Bug(s), Hub, Love, Run/Running, Public, Bungee, Lucky, Company, Update-/Upgrade-/Backup-/Startup-
    Komposita (Sicherheitsupdate(s), geupdatet, upgedatet …), Club-Komposita (Nachtclub, Golfclub …),
    Lunchpaket, Sonntagsbrunch, Puzzleteil(e), Coversong, Coverbands, Drumsticks, Stand-up-Comedy.
  - `ɛɪ`: Dating/Dates, Mail-Komposita (Mailadresse, Spammail, Phishingmail, Rundmail …), Spaceshuttle,
    Cyberspace, Tape, Cake, Rave, Gate(s), skaten/Skater(in)/Skatepark, Stage, Shake/Milkshake(s), Steak(s),
    Hater, Stakeholder, Mainstream, Trainee(s), Pancake(s), Spraydose, Sprays, Hey, Mayday, Birthday;
    Namen Jane, Kate, James, Jake, Dave, Taylor, Grace.
  - Weitere: Software-/Hardware-/Server-/Service-/Workshop-/Shop-Komposita, Thriller-Komposita, Python-Kurs,
    Score, Highscore, Hardcore, Appstore, Walk, Moonwalk, Open Source, Musical(s), Dschungelcamp, Barkeeper,
    Beamer, Bands, Manchester, Chelsea, Seattle, Washington, Gin Tonic.
- `de_foreign`: Garagen-Komposita (Tiefgarage, Garagentor …), Ingenieurbüro, Etagenwohnung, jonglieren,
  Sabotage-/Spionage-/Massage-Komposita, Orangensaft/-schale/-marmelade, orangefarben, Logenplatz, Jurymitglied,
  Jurys, Gagen, Regieanweisung, Visagist(in), Engagements, Arrangements, couragiert, Jour fixe, Charge, Rouge,
  Prestige, Vernissage, Camouflage, Lingerie, Jeton(s), Bonjour; Analyse, Radio, Radiosender, Spion(e), Kakao,
  Zucchini, Joghurt, präzise, Tumore, Trikots, Rekord, Paris, Kenia, Marathon, Containerschiff(e),
  barrierefrei, Effizienzkerne(n), Spitzenkandidatin, Arbeitsagentur, Models, Kameramann, Quizabend u. a.
- `de_native`: Juhu, igitt, oje, Gehaltserhöhung, Terrasse, Dachterrasse, zuklappen, Kinderarbeit,
  Johannisbeeren, Gummibärchen, Handschuhfach, Konzerns, Betriebsrat, Bürgeramt, Rasenmäher, Sommerfest,
  Läuferinnen, Staatsschulden, Lagebesprechung, Erdgeschoss, Gesichtserkennung, Bilderkennung,
  Impfstoffe, Reedereien, Spätschicht, Rücksendekosten u. a.

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
