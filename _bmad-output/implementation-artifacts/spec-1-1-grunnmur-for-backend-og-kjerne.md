---
title: 'Story 1.1: Grunnmur for backend og kjerne'
type: 'feature'
created: '2026-11-19'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '72f2eaaee069c0e524315b0a42c34a1cad334adb'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Repoet har ingen kode ennå. Regelstoriene 1.2–1.6 trenger én felles form for uker, tellinger og tall. Ellers kan appen, backtesten og testene gi ulike svar rundt årsskiftet, uke 53 og avrunding.

**Approach:** Opprette `backend/` som uv-prosjekt med Python 3.14 og pakken `marin.kjerne`, med modeller, ISO-kalender, avrunding og formatering, og tester som består med `uv run pytest`.

## Boundaries & Constraints

**Always:**
- Kjernen importerer bare stdlib og `marin.kjerne` (AD-1) og leser aldri klokka. `SISTE_UKE = Uke(2026, 42)` er en konstant.
- Lusetall er `Decimal`, avrundet til 2 desimaler med `ROUND_HALF_UP`. `round()` brukes aldri på lusetall.
- Identifikatorer bruker norske fagord uten æ, ø og å, i `snake_case`. Område er aldri et felt i `Serie` eller `AnleggInfo`.
- Kommentarer, docstrings og testnavn er på norsk. Æ, ø og å er lov i tekst, men ikke i identifikatorer (avgjort 2026-11-19).
- Arbeidet gjøres på grenen `story/1-1-grunnmur-for-backend-og-kjerne` og flettes til `main` med en PR (én gren per story, avgjort 2026-11-19).

**Never:**
- Ingen regler (R1–R4), ingen BarentsWatch-leser, ingen API og ingen frontend i denne storyen. Ingen avhengigheter som ikke brukes ennå (FastAPI, openpyxl og andre kommer i storyene som trenger dem).
- Ingen flyttall i kjernen.
- Ingen linter eller formatter (ruff venter, avgjort 2026-11-19).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Usortert serie | tellinger i vilkårlig rekkefølge | `Serie.tellinger` er stigende, uten nye uker | – |
| Duplikat | to tellinger for samme uke | – | `ValueError` |
| Ugyldig uke | `Uke(2025, 0)`, `Uke(2025, 54)`, `Uke(2025, 53)` | – | `ValueError` |
| Avrunding | `Telling(u, Decimal("0.125"))` | `verdi == Decimal("0.13")` | – |
| Flyttall | `Telling(u, 0.1)` | – | `TypeError` |
| Negativt | `Telling(u, Decimal("-0.01"))` | – | `ValueError` |
| Uke 53 | `har_uke_53(2025)` / `har_uke_53(2026)` | `False` / `True` | – |
| Årsskifte | `neste(Uke(2025, 52))`, `pluss(Uke(2025, 50), 3)` | `Uke(2026, 1)` begge | – |
| Løpende ukenummer | 2025 uke 50–52, 2026 uke 1–2 | fem påfølgende heltall (T12) | – |
| Intervall | `alle_uker(Uke(2025, 1), SISTE_UKE)` | 94 uker, stigende | – |
| Format | lus 0,06 / lus 0,5 / grense 0,5 / `Uke(2026, 42)` | «0,06» / «0,50» / «0,5» / «uke 42, 2026» | – |

</frozen-after-approval>

## Code Map

- `README.md` -- har bare tittel, lenke og medlemmer. Får en seksjon om backend og tester.
- `.gitignore` -- dekker allerede `.venv/`, `__pycache__/` og `.pytest_cache/`. Ingen endring.
- `data/barentswatch/*.xlsx` -- røres ikke (Story 1.3). Lusetallene kommer som `float` eller `int` fra openpyxl, med høyst 2 desimaler (kontrollert 2026-11-19).
- Verktøy -- uv 0.12.10 og CPython 3.14.7 er installert.

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml`, `backend/.python-version`, `backend/uv.lock` -- uv-prosjekt `marin` med src-layout og `uv_build`, `requires-python >=3.14`, ingen kjøreavhengigheter, dev-gruppe `pytest==9.2.0` og `testpaths = ["tests"]` -- grunnmur (NFR2)
- [x] `backend/src/marin/__init__.py`, `backend/src/marin/kjerne/__init__.py` -- pakkene
- [x] `backend/src/marin/kjerne/modeller.py` -- `Uke` (frozen, ordnet på `(ar, uke)`, validert med `date.fromisocalendar`), `Telling` (avrunder med `tall.avrund`, `TypeError` for alt annet enn `Decimal`/`None`, `ValueError` for negative tall), `Serie` (tuple, sortert, `ValueError` ved duplikat) og `AnleggInfo` (alle felt valgfrie) -- AD-11
- [x] `backend/src/marin/kjerne/uker.py` -- `har_uke_53`, `lopende`, `fra_lopende`, `neste`, `pluss` (også negativ n), `mellom(fra, til) -> int` og `alle_uker(fra, til)` (begge ender med) -- AD-14
- [x] `backend/src/marin/kjerne/konstanter.py` -- `SISTE_UKE`. Regelparameterne fra Story 1.4 og 1.5 samles her -- AD-5
- [x] `backend/src/marin/kjerne/tall.py` -- `avrund(Decimal) -> Decimal` -- AD-6
- [x] `backend/src/marin/kjerne/formatering.py` -- `format_lus` (alltid 2 desimaler), `format_grense` (1 desimal) og `format_uke` («uke 42, 2026») -- AD-6, NFR5
- [x] `backend/tests/data/format.json` -- vektorer for lus, grense og uke, som frontend gjenbruker i Story 2.2
- [x] `backend/tests/test_modeller.py`, `test_uker.py`, `test_formatering.py` -- hele I/O-matrisen. JSON leses med `parse_float=Decimal`
- [x] `backend/tests/test_kjerne_importer.py` -- AST-sjekk av alle moduler i `marin.kjerne`: bare `sys.stdlib_module_names` og `marin.kjerne`, ingen kall til `round`, ingen `datetime.now`/`date.today`/`time` -- AD-1, AD-5, AD-6
- [x] `README.md` -- seksjonen «Backend og tester» med `cd backend`, `uv sync` og `uv run pytest`

**Acceptance Criteria:**
- Gitt et nytt klon, når `uv sync` og `uv run pytest` kjøres i `backend/`, så består alle testene.
- Gitt en modul i `marin.kjerne` som importerer noe utenfor stdlib, kaller `round` eller leser klokka, når testene kjøres, så feiler importtesten.
- Gitt README, når den leses, så beskriver den de to kommandoene.

## Implementation Notes

- 2026-11-19: Implementert direkte i hovedøkten, ikke av en subagent. Fredrik sa ja til subagenter i review-steget.
- `Serie` har egen `__init__` som tar en vilkårlig iterable av `Telling` og lagrer en sortert tuple. Et element som ikke er `Telling`, gir `TypeError`.
- `alle_uker(fra, til)` med `til` før `fra` gir `ValueError`.
- `Telling` avviser også NaN og uendelig (`ValueError`) og gjør −0 om til 0,00.
- `format.json` har lusetall med 2 desimaler, slik API-et sender dem, så frontend ikke trenger egen avrunding.
- `uv.lock` har 7 pakker: pytest 9.2.0 med avhengigheter, blant annet colorama på Windows. `uv run pytest` gir 102 bestått.
- Etter review: `avrund` gir aldri −0,00 (null normaliseres der, og `Telling` bruker den). Importtesten fanger `round` i alle former. Docstringen i `kjerne/__init__.py` sier hva testen dekker. `pyproject.toml` krever uv 0.12 eller nyere. Ny `tests/test_tall.py`. `uv run pytest` gir 113 bestått.

## Spec Change Log

## Review Triage Log

Review 2026-11-19, runde 1. Lag: VG = Verification Gap, BH = Blind Hunter, EC = Edge Case Hunter. Verification Gap fant ingen hull i verifiseringen.

| Funn | Verdikt | Bevis og rute |
|---|---|---|
| VG-1 `avrund` og `format_lus` gir «−0,00» | medium | Reprodusert: `avrund(-0.004)` gir `-0.00`, og `max(…, 0)` beholder det. Story 1.4 setter negative estimater til 0. Patch: null normaliseres i `avrund`, med test i `test_tall.py`. |
| VG-2 Docstringen lover I/O-sjekk, og `round` slipper gjennom indirekte | low | Reprodusert: `finn_brudd` ga `[]` for `builtins.round`, `r = round` og `open('f')`. Patch: docstringen sier hva testen dekker, og `round` fanges som navn og attributt. |
| VG-3 `from marin import kjerne` avvises | low | Reprodusert, men ingen kjernemodul bruker den formen, og testen feiler høylytt. Avvist: lite sannsynlig, og rettelsen trenger en ny gren. |
| BH-1 «−0,00» | medium | Samme som VG-1. Patch. |
| BH-2 I/O, dynamisk import og indirekte `round` sjekkes ikke | low | Docstring og `round`: patch som VG-2. Dynamisk import (`importlib`, `__import__`): avvist som lite sannsynlig, og rettelsen er en ny vakt. |
| BH-3 Ingen sjekk for flyttall og æ, ø, å i identifikatorer | low | Kjernen har ingen av delene nå, og Story 1.4 har eget AC om flyttall. Avvist. |
| BH-4 Decimal-konteksten: 1E+27 gir `InvalidOperation` | low | Ingen kode endrer konteksten, og opplastede tall valideres i `kilder` (Story 3.2). Avvist. |
| BH-5 `Uke(10**20, 1)` gir `OverflowError` | false | Kjørt: Python 3.14 gir `ValueError`. |
| BH-6 Sprint-status står på `in-progress` mens specen er `in-review` | false | Steg 5 setter sprint-status til `review`. |
| BH-7 Ingen CI, og `uv sync` uten `--locked` | low | CI er utsatt i arkitekturen (Deferred). `uv sync` bruker `uv.lock` når den stemmer med `pyproject.toml`. Avvist. |
| BH-8 Kravet til uv-versjon håndheves ikke | low | Eldre uv gir uklare feil. Patch: `[tool.uv] required-version = ">=0.12"`. |
| BH-9 `konstanter.py` sier «R2 og R4» | false | Horisonten H = 6 er definert i R2 i briefen, og FR27a sier «parameterne i R2 og R4». |
| BH-10 `format.json` sier «2 desimaler», «Frontend har» står i presens, og Pydantic sender Decimal som streng | low | Teksten i `format.json` og docstringen: patch. Pydantic gjelder Story 2.1: defer. |
| BH-11 `AnleggInfo` har ingen typesjekk | low | `omrade_fra_fylke` gir `ukjent` for tomt fylke (Story 1.2), og lokalitetsnummer er heltall i utdraget. Avvist, men verdt å huske i Story 1.3. |
| EC-1 `InvalidOperation` ved verdier ≥ 1E26 | low | Som BH-4. Avvist. |
| EC-2 `format_lus` med −0, negative tall og NaN | medium | −0: patch som VG-1. Negative tall og NaN kan ikke nå `format_lus` (`Telling` avviser dem, og estimater settes til 0). Avvist. |
| EC-3 `format_grense` med 0,25, −0 eller NaN | low | Grensene er bare 0,5 og 0,2 (R1). Avvist. |
| EC-4 `round` via `builtins`, alias, `map` eller `__round__` | low | Reprodusert. Patch som VG-2. |
| EC-5 Klokka via `timeit`, `os.times`, `uuid1` eller `asyncio` | low | Lite sannsynlig i regelkjernen, og rettelsen er en ny forbudsliste. Avvist. |
| EC-6 Dynamisk import og `getattr` | low | Som EC-5. Avvist. |
| EC-7 Docstringen lover «ingen I/O» | low | Reprodusert med `open('f')`. Patch som VG-2. |
| EC-8 `from marin import kjerne` og relative importer i underpakker | low | Som VG-3. Kjernen har ingen underpakker. Avvist. |
| EC-9 Et heltall i `format.json` gir `TypeError` | false | Lus-vektorene har ingen heltall, og et heltall ville feilet testen høylytt. |
| EC-10 `AnleggInfo` med blankt fylke eller nummer som tekst | low | Som BH-11. Avvist. |
| EC-11 (claim) Importtesten dekker bare bokstavelige former | low | `round` fanges nå i alle former (patch), og docstringen sier hva testen dekker. Sjeldne klokkekilder og dynamisk import er avvist (EC-5, EC-6). |
| EC-12 (claim) `format_lus` gir «NaN» | low | NaN kan ikke nå `format_lus`. Avvist. |

## Design Notes

- Løpende ukenummer er `(ordinal for ISO-mandagen − 1) // 7`. Alle mandager har ordinal ≡ 1 (mod 7), så tallene blir påfølgende heltall over årsskifter og uke 53. `fra_lopende(n)` går motsatt vei via `date.fromordinal(n * 7 + 1)`.
- `Telling` godtar ikke `float`. Kildene i Story 1.3 konverterer med `Decimal(str(v))`, slik at for eksempel 0,145 ikke blir 0,14 på grunn av binære flyttall.
- `Uke` valideres i `modeller` med stdlib (`date.fromisocalendar`) for å unngå sirkulær import med `uker`. All ukearitmetikk ligger i `uker`.

## Verification

**Commands:**
- `cd backend && uv sync && uv run pytest` -- expected: alle testene består
