---
title: 'Story 1.3: Datasett fra BarentsWatch-utdraget'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'b2429f39c08e94bd0329f3a8290578a01d01a568'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Appen og backtesten trenger lusetallene fra BarentsWatch-utdraget som kjernens typer. Å lese de to Excel-filene tar omtrent 15 sekunder, og samme fil skal gi samme serie både som innebygde data og som opplasting (AD-12).

**Approach:** Én leser `marin.kilder.barentswatch` fra Excel-bytes til `(AnleggInfo, Serie)` og feil. Et skript `marin.forbered` skriver `datasett.json` med data til og med `SISTE_UKE` og sha256 for kildefilene. En modul eier formatet til `datasett.json`, og hashtesten og NFR3-testen kommer med. README får en del om dataene.

## Boundaries & Constraints

**Always:**
- Arknavnet «Lakselus per fisk» og kolonnenavnene står bare i `marin.kilder.barentswatch`. Påkrevde kolonner er `Lokalitetsnummer`, `År`, `Uke` og `Voksne hunnlus`. `Lokalitetsnavn`, `Kommune` og `Fylke` kan mangle. Kolonnene finnes etter navn i første rad, og andre kolonner ignoreres.
- `les(innhold: bytes, til_og_med: Uke | None = None)`. Rader etter `til_og_med` hoppes over før `AnleggInfo` og `Serie` lages (FR1). `forbered` sender `SISTE_UKE`, og opplastingen (Story 3.2) sender `None`.
- Navn, kommune og fylke hentes felt for felt fra den nyeste raden der feltet har verdi. Det presiserer «fylket fra nyeste rad» i AD-11 (avgjort 2026-11-23). Tom tekst eller bare mellomrom regnes som ingen verdi, og har ingen rad verdi, blir feltet `None`.
- Tom `Voksne hunnlus` gir `Telling(uke, None)`, og ingenting fylles inn (FR2). Lusetall gjøres om med `Decimal(str(v))`. Rader der alle cellene er tomme, hoppes over uten feil.
- `Feil(rad: int | None, melding: str)`: `rad` er radnummeret i regnearket (overskriften er rad 1), og `melding` begynner med «Rad N: » når raden er kjent. Ordlyden følger EXPERIENCE.md der den finnes. En rad med feil kommer ikke med. Ved duplikat beholdes den første raden.
- Leseren sjekker bare det som trengs for å lage kjernens typer: arket, påkrevde kolonner, heltall i `Lokalitetsnummer`, `År` og `Uke` (`int`, eller `float` med heltallsverdi, men ikke `bool`), gyldig ISO-uke, lusetall som er tall og ikke negative, og duplikater på `(lokalitetsnr, år, uke)`.
- Anleggene sorteres på lokalitetsnummer. `datasett.json` ligger i `backend/src/marin/data/`, er UTF-8 uten ASCII-escape og har lusetall som JSON-tall. Stiene regnes fra `importlib.resources.files("marin")`.
- `forbered` skriver ingen fil når leseren gir feil. Den skriver de 20 første feilene og antallet til stderr, og avslutter med kode 1.
- README beskriver hentingen slik: «Lastet ned 27.10.2026 fra BarentsWatch Fiskehelse som Excel-uttrekk «Lakselus per fisk», ett per år (2025 og 2026), for alle lokaliteter. Lisens: Norsk lisens for offentlige data (NLOD) 2.0.» Fredrik retter detaljene i PR-en (avgjort 2026-11-23).
- Kommentarer, docstrings og testnavn er på norsk. Grenen er `story/1-3-datasett-fra-barentswatch-utdraget`.

**Never:**
- Ingen FR24-regler som bare gjelder opplasting: årsgrensen 2000 til inneværende år, grensen på 4 MB, teksten for ukjent format og høyst 20 feil sortert i API-et. Det kommer i Story 3.2.
- `Lusegrense uke` leses aldri av leseren, bare av NFR3-testen.
- Ingen API, CSV-leser eller backtest. Kjernen endres ikke.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| Gyldig | to anlegg, tre uker hver, én tom verdi | to par sortert på nummer, og den tomme verdien er `None` | – |
| Kutt | 2026 uke 42 og 43, `til_og_med=Uke(2026, 42)` | bare uke 42 | – |
| Ulikt fylke | Trøndelag i uke 1, Nordland i uke 2, med radene i omvendt rekkefølge | fylke Nordland | – |
| Nyeste rad uten info | Juvika, MOLDE, Møre og Romsdal i uke 1–2, tomme felt i uke 3 | navn Juvika, kommune MOLDE, fylke Møre og Romsdal, og uke 3 er med i serien | – |
| Ulikt navn | Sloppegrunn i uke 1, Geitelva i uke 2 | navn Geitelva | – |
| Aldri info | alle radene uten navn, kommune og fylke | `AnleggInfo(nr, None, None, None)` | – |
| Duplikat | rad 6 og rad 9: samme anlegg, 2026 uke 34 | rad 6 beholdes | «Rad 9: uke 34, 2026 finnes allerede i rad 6.» |
| Ugyldig uke | uke 54 / 2025 uke 53 | – | «Rad 5: uke 54 finnes ikke. Uke må være 1–53.» / «Rad 5: 2025 har ikke uke 53.» |
| Ugyldig lusetall | `"abc"` / `-0.2` | – | «Rad 7: lusetallet «abc» er ikke et tall.» / «Rad 7: lusetallet «-0,2» er negativt.» |
| Ikke heltall | `År` tom, `Uke` = `"x"`, `Lokalitetsnummer` = `12.5` | – | «Rad 3: «År» mangler.» / «Rad 3: «Uke» må være et heltall, ikke «x».» |
| Kolonne mangler | ingen `Voksne hunnlus` | ingen anlegg | `Feil(None, "Fila mangler kolonnen «Voksne hunnlus».")` |
| Feil fil | bytes som ikke er xlsx, eller et annet arknavn | ingen anlegg | `Feil(None, "Fila er ikke et Excel-uttrekk fra BarentsWatch med arket «Lakselus per fisk».")` |
| `forbered` med feil | xlsx med duplikat | ingen fil, kode 1 | feilene på stderr |

</frozen-after-approval>

## Code Map

- `backend/src/marin/kjerne/modeller.py` -- `Uke` (ValueError ved ugyldig uke), `Telling` (krever Decimal, avrunder, ValueError ved negativt tall), `Serie` (ValueError ved duplikat; leseren finner duplikater selv for å få begge radnumrene) og `AnleggInfo` (ingen typesjekk, så leseren må sikre at `lokalitetsnr` er `int`, jf. issues.md fra 1.1).
- `backend/src/marin/kjerne/formatering.py` -- `format_uke` gir «uke 34, 2026» til duplikatmeldingen.
- `backend/src/marin/kjerne/konstanter.py` -- `SISTE_UKE`. `kjerne/omrade.py` og `kjerne/lusegrense.py` -- `omrade_fra_fylke` og `grense` til NFR3-testen.
- `backend/pyproject.toml` -- `dependencies = []`. openpyxl 3.1.5 legges til, med eksakt versjon som pytest.
- `backend/tests/test_kjerne_importer.py` -- gjelder bare `kjerne/`, så `kilder` og `forbered` kan importere openpyxl. Endres ikke.
- `data/barentswatch/*.xlsx` (committet, kontrollert 2026-11-23) -- 102 560 rader, 1 092 anlegg, 2025 uke 1–52 og 2026 uke 1–44, med 2 124 rader etter 2026 uke 42. Ingen duplikater og ingen ugyldige uker. Lusetallene er `int` eller `float` fra 0 til 8,3, med høyst 2 desimaler. En tom celle er `None`. 7 rader mangler navn, kommune og fylke: de tre anleggene 3877, 112525 og 450036 med én rad hver, og den siste raden til 12260 Juvika, 12371 Kalvøya, 10560 Kårvik og 13550 Marøy Nø, som ble tatt ut av akvakulturregisteret. Kuttet ved uke 42 endrer ikke navn, kommune eller fylke for noe anlegg. R1 gir 0 avvik mot `Lusegrense uke`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/pyproject.toml`, `backend/uv.lock` -- `uv add openpyxl==3.1.5` -- AD-12, stacken
- [x] `backend/src/marin/kilder/__init__.py`, `kilder/feil.py` -- pakken og `Feil` (frozen dataclass) -- felles for Excel nå og CSV senere
- [x] `backend/src/marin/kilder/barentswatch.py` -- `les(innhold, til_og_med=None) -> tuple[list[tuple[AnleggInfo, Serie]], list[Feil]]` etter reglene over -- FR1–FR3, AD-12
- [x] `backend/src/marin/kilder/datasett.py` -- `Datasett(siste_uke, kilder: {filnavn: sha256}, anlegg)` med `til_json`, `fra_json` og `last()` (fra pakken) -- formatet eies ett sted. Backtesten (1.6) og API-et (2.x) bruker `last()`
- [x] `backend/src/marin/forbered/__init__.py`, `forbered/__main__.py` -- `kjor(kildemappe, utfil) -> int`, og `__main__` finner stiene fra pakken -- AD-10
- [x] `backend/src/marin/data/datasett.json` -- lages med `forbered` og committes
- [x] `backend/tests/hjelp_xlsx.py` (i stedet for en fixture i `conftest.py`, se Implementation Notes) -- funksjoner som lager xlsx-bytes i minnet med openpyxl (rader, kolonner, arknavn) -- testdata uten binærfiler
- [x] `backend/tests/test_barentswatch.py`, `test_datasett.py`, `test_forbered.py` -- hver rad i matrisen, JSON fram og tilbake, og `forbered` mot en midlertidig mappe
- [x] `backend/tests/test_datasett_fil.py` -- hashene i den committede `datasett.json` stemmer med xlsx-filene (navn, antall og sha256), og ingen uke er etter `SISTE_UKE`
- [x] `backend/tests/test_nfr3.py` -- leser xlsx-filene direkte med openpyxl én gang per modul og sammenligner `grense(omrade_fra_fylke(fylke), uke)` med `Lusegrense uke` («Ukjent» tilsvarer `None`). Testen godtar 0 avvik, og alle utfylte fylker skal gi `sor` eller `nord` -- NFR3
- [x] `README.md` -- delen «Data»: kilde, lisens, nedlastingsdato, hvordan dataene ble hentet, `uv run python -m marin.forbered` og hvor filene ligger -- NFR9, NFR11

**Acceptance Criteria:**
- Gitt utdraget, når `uv run python -m marin.forbered` kjøres, så skrives `datasett.json` med 1 092 anlegg fra 2025 uke 1 til og med 2026 uke 42, og terminalen viser antall anlegg, uker med telling og uker uten telling. En ny kjøring gir en fil som er lik byte for byte.
- Gitt `datasett.json` og xlsx-filene, når hashtesten kjører, så feiler den hvis en hash, et filnavn eller antallet filer ikke stemmer.
- Gitt NFR3-testen, når den kjører, så gir den 0 avvik, og de 7 radene med «Ukjent» gir område `ukjent`.
- Gitt `uv run pytest`, når testene kjører, så består alle testene.

## Implementation Notes

- 2026-11-23: Implementert direkte i hovedøkten, som 1.1 og 1.2. Review med tre subagenter etterpå.
- **Sammenslåing av årsfilene:** leseren tar én fil, men de fleste anleggene finnes i begge filene. `forbered.slaa_sammen` samler tellingene i én serie, og samme uke i to filer gir en feil. Navn, kommune og fylke tas felt for felt fra den nyeste delen med verdi, sortert på siste uke. Det gir samme regel som i leseren så lenge filene ikke overlapper i tid, og det gjør de ikke (ett år per fil).
- **Testhjelp:** `hjelp_xlsx.py` er en vanlig modul med `rad` og `lag_xlsx`, ikke en fixture i `conftest.py`, fordi testene bruker funksjonene direkte, også i `parametrize`. pytest finner modulen fordi `tests/` ikke er en pakke.
- **Leseren** samler alle feilene i en rad, ikke bare den første. Rader etter `til_og_med` hoppes over uten kontroll av lusetall og duplikater. År utenfor kalenderen (for eksempel 0) gir «Rad N: året 0 finnes ikke i kalenderen.», som ikke står i matrisen.
- **Programkontroll:** også en helt ny `.venv` blir blokkert, og `python.exe` der har samme sha256 som den gamle. Å lage `.venv` på nytt hjelper altså ikke. Testene og `forbered` er kjørt med basistolken til Python 3.14 og `site.addsitedir('.venv/Lib/site-packages')`.
- **Resultat:** `forbered` gir 1 092 anlegg, 54 033 uker med telling og 46 403 uker uten telling (1,6 MB). To kjøringer ga filer som var like byte for byte. Det er 284 tester (210 før storyen), og de tar omtrent 19 sekunder, hvorav NFR3 tar 17.
- Anlegget som i planleggingen ble kalt «Marøy N», heter «Marøy Nø». Terminalen viste ø som �. Code Map er rettet.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Blind Hunter + Edge Case | Et svært stort lusetall (1e30) gir `decimal.InvalidOperation` ut av `les()` i stedet for en `Feil` | medium | patch | Reviewerne fant det med en probe, og testen bekrefter det. Opplastingen (3.2) ville gitt 500. Rettet: tall med `adjusted() >= 20` gir «Rad N: lusetallet «…» er for stort.». Testen er ny. |
| 2 | Blind Hunter + Edge Case | Ødelagt XML i arket gir `ParseError` ut av `les()`, fordi `read_only` først leser XML-en når radene hentes | medium | patch | Bekreftet: testen feiler uten fiksen. Rettet: `_rader` gjør feil fra openpyxl sin `iter_rows` om til formatfeil. Feil i leserens egen kode slipper fortsatt gjennom. Årsaken er lenket med `from`. |
| 3 | Blind Hunter + Edge Case | En feil `<dimension>` i fila gir falske «mangler kolonnen»-feil, og rader forsvinner uten feil (5 rader ble 1) | medium | patch | Bekreftet: testen feiler uten fiksen. Rettet med `ark.reset_dimensions()`. `datasett.json` er lik byte for byte etterpå. |
| 4 | Blind Hunter | Tall lagret som tekst («12260», «0.5») gir en melding som ser selvmotsigende ut | low | avvist | Specen godtar bare tallceller, og BarentsWatch-uttrekket har ingen tekst-tall. Ordlyden i feilmeldingene ved opplasting eies av Story 3.2. Ta det med der. |
| 5 | Blind Hunter + Edge Case (også claim) | En første rad med feil holder av uka, så en senere gyldig rad med samme uke også avvises, og meldingen viser til den avviste raden | false | avvist | Fila har uka to ganger, og meldingen sier akkurat det. Brukeren får begge feilene på én gang. Ingen bruker `anlegg` når det finnes feil: `forbered` stopper, og opplastingen viser ingen anlegg (AD-13). Valget er dokumentert med en test. |
| 6 | Blind Hunter + Edge Case + Verification Gap | `*.xlsx` treffer låsefilen Excel lager (`~$navn.xlsx`), så `forbered`, hashtesten og NFR3 feiler | medium | patch | Skjer når en kildefil er åpen i Excel på Windows. Rettet: `kildefiler()` hopper over `~$`, og `forbered` og begge testene bruker den. Testen er ny. |
| 7 | Blind Hunter | Feilmeldingen fra `slaa_sammen` mangler filer og rader, viser bare den første uka og bruker teksten fra kjernen. En tom `Serie` gir `IndexError` | low | avvist | `forbered` er et utviklerskript, og årsfilene overlapper ikke. Leseren lager aldri en tom serie. En bedre melding krever mer kode og har liten nytte. |
| 8 | Blind Hunter | README sier ikke at `SISTE_UKE` og testtallene må endres når utdraget byttes ut | low | patch | Rettet med ett avsnitt i README. |
| 9 | Blind Hunter + Verification Gap | Design Notes sier «via `float`», 1,5 MB, 15 s og viser mellomrom i eksempelet. Koden skriver fra Decimal, fila er 1,6 MB, og testene tar 17 s | low | avvist | Rettelsen er å endre denne specen, og det gjøres ikke i review. Docstringen i `datasett.py` og Implementation Notes er riktige. |
| 10 | Blind Hunter | Status i spec og sprint-status er ulike, og triage-loggen er tom | false | avvist | Steg 5 setter storyen til `review`, og loggen fylles nå. |
| 11 | Blind Hunter | `Datasett` har et `dict`-felt (kan ikke hashes), `last()` har ingen cache, og formatet har ingen versjon | low | avvist | Ingen hasher `Datasett`. API-et og backtesten laster fila én gang (AD-10). Et versjonsfelt har ingen bruker ennå. |
| 12 | Blind Hunter | `.gitattributes` mangler for `datasett.json` (store differ, CRLF ved checkout) | low | avvist | GitHub viser ikke så store differ uansett. Testen mot en ny kjøring sammenligner med `read_text`, som tåler CRLF. Etter `core.autocrlf` blir `git diff` tom. |
| 13 | Blind Hunter | «Trolig uten fisk» og «Har telt lakselus» blir ikke tatt med, så tomme anlegg og manglende rapporter ser like ut | false | avvist | FR2 sier at en uke med telling bare avgjøres av `Voksne hunnlus`. Ingen regel i R1–R4 bruker de andre kolonnene. |
| 14a | Blind Hunter | Ingen test for at rader etter kuttet hoppes over uten kontroll | low | patch | Testen `test_rader_etter_kuttet_kontrolleres_ikke` er ny. |
| 14b | Blind Hunter | Ingen test for ødelagt input til `fra_json` | low | avvist | Fila lages bare av `forbered`, og testen mot en ny kjøring dekker innholdet. |
| 14c | Blind Hunter | `forbered` skriver «1 uker» | low | avvist | Kosmetisk, og det skjer bare i testdata. Det ekte utdraget har tusenvis av uker. |
| 15 | Edge Case | Kildefiler uten rader til og med `SISTE_UKE` gir en tom `datasett.json` og kode 0 | low | avvist | Uvanlig, og `test_datasettet_har_alle_anleggene_sortert` (1 092 anlegg) feiler da. |
| 16 | Edge Case | Filer som overlapper i tid uten samme uke, gir navn eller fylke fra en eldre rad | low | avvist | Begrensningen står i docstringen for `slaa_sammen`. Det er ett år per fil. En sjekk ville lagt til en gren uten nytte i dag. |
| 17 | Edge Case | Et heltall som lusetall i `datasett.json` gir `TypeError` i `last()` | false | avvist | `til_json` skriver alltid 2 desimaler (`1.00`), så det kan bare skje i en håndredigert fil. |
| 18 | Verification Gap | Den committede `datasett.json` sammenlignes aldri med en ny kjøring av `forbered` | gap | patch | Testen `test_datasett_json_er_lik_en_ny_kjoring_av_forbered` er ny. Den gjør testene omtrent 19 s tregere, og README er oppdatert. |
| 19 | Verification Gap | Ingen test viser at nyeste fil vinner når filnavnene ikke står i tidsrekkefølge | gap | patch | Testen `test_info_fra_nyeste_fil_selv_naar_filnavnene_ikke_er_i_tidsrekkefolge` er ny. |

## Design Notes

Formatet til `datasett.json` (ett anlegg per linje, så diffene blir lesbare):

```json
{"siste_uke": {"ar": 2026, "uke": 42},
 "kilder": {"lakselus_per_fisk_2025.xlsx": "…sha256…", "lakselus_per_fisk_2026.xlsx": "…"},
 "anlegg": [
{"lokalitetsnr": 10560, "navn": "Kårvik", "kommune": "TROMSØ", "fylke": "Troms", "tellinger": [[2025, 1, null], [2025, 2, 0.12]]},
 …]}
```

- Lusetall skrives som JSON-tall via `float` og leses med `parse_float=Decimal`. Det er trygt fordi verdiene har høyst 2 desimaler. Ukene uten telling skrives som `null`, fordi `Serie` skal ha alle radene fra kilden (AD-11). Fila blir omtrent 1,5 MB.
- NFR3-testen og leseren går gjennom openpyxl hver for seg, og NFR3-testen gjør hele `uv run pytest` omtrent 15 sekunder tregere. Det godtar vi, fordi NFR2 krever at én kommando kjører alle testene.
- `files("marin")` er `backend/src/marin`, så `data/barentswatch/` ligger tre nivåer opp. Det gjelder bare utviklingsinstallasjonen, og det er den `forbered` er laget for.

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består. På Fredriks maskin blokkerer Programkontroll `.venv/Scripts/python.exe`, så der kjøres testene med basistolken: `<uv python 3.14>/python.exe -c "import site,sys; site.addsitedir('.venv/Lib/site-packages'); import pytest; sys.exit(pytest.main(['-q','-p','no:cacheprovider']))"`
- `uv run python -m marin.forbered` (eller med basistolken) -- expected: kode 0, `datasett.json` skrives, og `git diff` er tom ved en ny kjøring
