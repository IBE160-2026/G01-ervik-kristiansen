---
title: 'Story 1.2: Lusegrense og område (R1)'
type: 'feature'
created: '2026-11-19'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '57c4eb940f5e5d6212c207fd1e6453c043ff4de3'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Prognosen må sammenlignes med riktig lusegrense, og grensen avhenger av område og ISO-uke (R1). Kjernen har ingen grense og ingen områdelogikk ennå.

**Approach:** Legge til `Omrade` og `omrade_fra_fylke` (fylkesnavn → sør, nord eller ukjent, fra en lukket tabell) og `grense(omrade, uke)` og `er_brudd(verdi, grense)` i `marin.kjerne`, med T1–T4 og kanttilfellene som tester.

## Boundaries & Constraints

**Always:**
- Grensen er 0,2 i uke 16–21 (sør) og uke 21–26 (nord), ellers 0,5. Den avhenger bare av ukenummeret, ikke av året. En verdi ≥ grensen er brudd.
- Nord er Nordland, Troms, Finnmark og det tidligere «Troms og Finnmark». Alle andre nåværende og tidligere fylker i tabellen er sør. Tomt fylke, `None` eller et navn som ikke står i tabellen gir `ukjent`, og da finnes ingen grense (`None`). Alle som kaller `grense`, må håndtere `None`.
- Tabellen har bare de norske navneformene, slik BarentsWatch skriver dem, ikke de samiske og kvenske parallellnavnene (avgjort 2026-11-19).
- `grense` og `er_brudd` er strenge på typer, som resten av kjernen: `omrade` går gjennom `Omrade(omrade)` (ukjent kode gir `ValueError`), uka må være `Uke`, og `er_brudd` tar bare `Decimal` (ellers `TypeError`, også for `None` og flyttall). `er_brudd` avrunder ikke. Den som kaller, avrunder først (R2, AD-6).
- Område er aldri et felt i `Serie` eller `AnleggInfo` (AD-11). Kjernen importerer bare stdlib (AD-1).
- Kommentarer, docstrings og testnavn er på norsk. Arbeidet gjøres på grenen `story/1-2-lusegrense-og-omrade-r1` med PR til `main`.

**Never:**
- `Lusegrense uke` fra BarentsWatch brukes aldri som grense (NFR3-testen mot den kommer i Story 1.3).
- Ingen særskilte grenser for tillatelser med kapasitetsøkning (utenfor v1).
- Ingen linter.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| T1 | sør, uke 21 | 0,2 | – |
| T2 | sør, uke 22 | 0,5 | – |
| T3 | nord, uke 21 | 0,2 | – |
| T4 | nord, uke 20 | 0,5 | – |
| Kanter sør | sør, uke 15 / uke 16 | 0,5 / 0,2 | – |
| Kanter nord | nord, uke 26 / uke 27 | 0,2 / 0,5 | – |
| Året betyr ikke noe | sør, 2025 uke 21 og 2026 uke 21; nord, 2026 uke 53 | 0,2 og 0,2; 0,5 | – |
| Ukjent område | ukjent, hvilken som helst uke | `None` | – |
| Område som tekst | `grense("sor", Uke(2026, 21))` | 0,2 | `"sør"` eller `"xyz"` gir `ValueError`; `grense(Omrade.SOR, 21)` gir `TypeError` |
| Brudd | 0,50 mot 0,5 / 0,49 mot 0,5 / 0,20 mot 0,2 | brudd / ikke brudd / brudd | – |
| Brudd med feil type | grense `None`, verdi `None` eller verdi `0.5` (float) | – | `TypeError` |
| Nord-fylker | Nordland, Troms, Finnmark, Troms og Finnmark | nord | – |
| Sør-fylker | Trøndelag, Nord-Trøndelag, Sør-Trøndelag, Vestland, Agder, Viken, Hordaland og resten av tabellen | sør | – |
| Ukjent fylke | `""`, `"  "`, `None`, `"Svalbard"`, `"Ukjent"` | ukjent | – |
| Skrivemåte | `" Nordland "`, `"TRØNDELAG"`, `"troms  og finnmark"` | nord / sør / nord | – |

</frozen-after-approval>

## Code Map

- `backend/src/marin/kjerne/modeller.py` -- `Uke` er argumentet til `grense`. Område skal ikke inn her (AD-11).
- `backend/src/marin/kjerne/formatering.py` -- `format_grense` venter `Decimal` med 1 desimal, så grensene lagres som `Decimal("0.2")` og `Decimal("0.5")`.
- `backend/src/marin/kjerne/konstanter.py` -- brukes ikke. R1-grensene er lov, ikke regelparametere for backtesten.
- `backend/tests/test_kjerne_importer.py` -- sjekker nye moduler automatisk (`rglob`). Settet i `test_kjernen_har_moduler` utvides.
- Data (kontrollert 2026-11-19) -- utdraget har fylkene Rogaland, Møre og Romsdal, Nordland, Agder, Vestland, Trøndelag, Troms og Finnmark (aldri «Troms og Finnmark»). 7 rader mangler fylke, og akkurat de har `Lusegrense uke` = «Ukjent». Kolonnen er tekst («0.5», «0.2», «Ukjent»).

## Tasks & Acceptance

**Execution:**
- [x] `backend/src/marin/kjerne/omrade.py` -- `Omrade(StrEnum)` med `SOR = "sor"`, `NORD = "nord"` og `UKJENT = "ukjent"`. En lukket tabell med de 26 fylkesnavnene i Design Notes. `omrade_fra_fylke(fylke)` slår sammen alle mellomrom (også hardt mellomrom) til ett med `" ".join(fylke.split())` og bruker `casefold()` -- FR3, AD-11
- [x] `backend/src/marin/kjerne/lusegrense.py` -- konstantene `GRENSE_VAR = Decimal("0.2")` og `GRENSE_ELLERS = Decimal("0.5")` og vårukene per område. `grense(omrade, uke) -> Decimal | None` og `er_brudd(verdi, grense) -> bool` med typereglene over -- FR10, R1
- [x] `backend/tests/test_lusegrense.py` -- T1–T4 som `test_t1_…` til `test_t4_…`, og resten av matrisen for `grense` og `er_brudd`
- [x] `backend/tests/test_omrade.py` -- testen har sin egen utskrevne liste med de 26 navnene og sjekker at tabellen har nøyaktig dem, med riktig område. I tillegg ukjente navn og skrivemåter fra matrisen
- [x] `backend/tests/test_kjerne_importer.py` -- legg `omrade.py` og `lusegrense.py` til i settet over forventede moduler

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består T1–T4, navngitt etter T1–T4 (NFR2), og alle andre testene.
- Gitt I/O-matrisen, når testene leses, så har hver rad minst én test som kjører og består.
- Gitt fylkestabellen, når den sammenlignes med testens egen liste, så har den nøyaktig de 26 navnene, og bare Nordland, Troms, Finnmark og Troms og Finnmark gir `nord`.

## Implementation Notes

- 2026-11-19: Implementert direkte i hovedøkten, som Story 1.1. Review med tre subagenter etterpå.
- `FYLKER` og `VARUKER` er `MappingProxyType`, så de ikke kan endres ved et uhell. `omrade_fra_fylke` gir `TypeError` for noe annet enn tekst eller `None`, som resten av kjernen.
- Testen `test_vargrensen_gjelder_bare_i_vaarukene` går gjennom alle 53 ukene i 2026 og sjekker at bare de utskrevne vårukene gir 0,2.
- Windows Programkontroll blokkerer `pytest.exe` i `backend/.venv` på denne maskinen, så `uv run pytest` feiler. Kontrollert to ganger 2026-11-19. Testene er kjørt med `uv run python -m pytest`. Det gir 199 bestått før review og 210 etter.
- Etter review: `er_brudd` gir `ValueError` når verdien ikke er avrundet til 2 desimaler. `Omrade` sin docstring sier nå at bare «sor» og «nord» er koder i API-et, mens ukjent blir `null` (AD-13). Det retter påstanden i Design Notes om at alle tre kodene brukes direkte.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Edge Case + Blind Hunter | `er_brudd` godtar verdi som ikke er avrundet: 0,495 mot 0,5 gir «ikke brudd», men avrundet 0,50 er brudd | medium | patch | Bekreftet med probe. Samme feil som T12 advarer mot. Rettet: `verdi != avrund(verdi)` gir `ValueError`. Tester for 0,495, 0,4999, 0,199 og 0,500. |
| 2 | Edge Case + Blind Hunter | `er_brudd` avviser ikke NaN, uendelig eller negative tall | low | avvist | Kan ikke nås: tellinger valideres av `Telling`, og estimatet avrundes og settes til minst 0 (R2). NaN og uendelig gir nå uansett feil via `avrund`. Å legge til vakter gir mer kode uten nytte. |
| 3 | Edge Case + Blind Hunter | `grense(None, uke)` gir `ValueError`, ikke `TypeError` | low | avvist | Feiler høyt, og dette er nøyaktig det specen sier (`Omrade(omrade)`, ukjent kode gir `ValueError`). En ekstra typevakt endrer ikke hva den som kaller, ser. |
| 4 | Blind Hunter | Ingen test for at `grense(UKJENT, 21)` gir `TypeError` | low | patch | Rekkefølgen er riktig i dag, men en endring kunne gjort at ukjent område med feil uke ga `None` uten feil. Testen kjører nå for alle tre områdene. |
| 5 | Blind Hunter | `VARUKER` har ingen test for at den ikke kan endres | false | avvist | Den er en `MappingProxyType`, og verdiene er `range`, som ikke kan endres. Det finnes ingen feil å teste mot. |
| 6 | Blind Hunter | Docstring og testnavn lover at alle tre kodene er API-koder (AD-13) | low | patch | AD-13 sender `omrade_utledet` som `sor`, `nord` eller `null`, og `POST /api/prognose` avviser `ukjent` med 422. Retter docstring og gir testen nytt navn. |
| 7 | Blind Hunter | Manglende fylke og ukjent navn gir begge `ukjent`, og FR23/FR23a definerer ikke ukjent navn | false | avvist | Story 3.2 dekker begge (epics.md:1086): «mangler fylket, eller er det ukjent, … brukeren må velge område». |
| 8 | Blind Hunter | Hardt mellomrom er ikke testet | low | patch | Det var testet, men som et usynlig tegn i kildekoden, slik at reviewer ikke så det. Står nå som ` `, og «Nordland» med hardt mellomrom bak er lagt til. |
| 9 | Blind Hunter | AK 1 er verifisert med `uv run python -m pytest`, ikke med `uv run pytest` | medium | defer | Bekreftet: Windows Programkontroll blokkerer `pytest.exe` i `.venv`. Det er et problem med maskinen, ikke med denne storyen. Ført i deferred-work.md og issues.md. |
| 10 | Blind Hunter | Parameteren `grense` i `er_brudd` skygger for funksjonen `grense` | low | avvist | Ingen feil i dag, siden `er_brudd` ikke kaller `grense()`. Specen gir signaturen `er_brudd(verdi, grense)`. |
| 11 | Edge Case | Bindestrekvarianter (– eller mellomrom rundt) i fylkesnavn gir `ukjent` | low | avvist | BarentsWatch bruker vanlig bindestrek, og utdraget har ingen fylkesnavn med bindestrek. Ukjent gir et trygt og synlig valg av område (FR23a). Normalisering ville gjort koden mer kompleks. |
| 12 | Edge Case | Usynlige tegn (nullbredde, BOM) i fylkesnavn gir `ukjent` | low | avvist | Samme som nr. 11: openpyxl leser celler, ikke tekstfil med BOM, og resultatet er et trygt `ukjent`. |
| – | Verification Gap | Ingen hull funnet | – | – | – |

## Design Notes

- `Omrade` er en `StrEnum`, så `Omrade.SOR == "sor"`. Kodene `sor`, `nord` og `ukjent` kan da brukes direkte i API-et (AD-13) uten oversetting. Visningsordene «sør» og «nord» i områdeteksten (FR23) lages i Story 3.2.
- Modulen heter `lusegrense.py` og ikke `grense.py`, så modulen og funksjonen `grense` ikke får samme navn.
- `er_brudd` med `None` gir `TypeError`. R4 sjekker ukjent område først, og backtesten (Story 1.6) hopper over anlegg med ukjent område og uker uten telling, så ingen av delene skal nå `er_brudd`.
- Ingen Unicode-normalisering: ingen av navnene inneholder bokstaver som endres av NFC (å finnes ikke, og ø og æ har ingen dekomponert form).
- Fylkestabellen før normalisering (26 navn):
  - Nord: Nordland, Troms, Finnmark, Troms og Finnmark.
  - Sør:
    - Nåværende: Østfold, Akershus, Buskerud, Oslo, Innlandet, Vestfold, Telemark, Agder, Rogaland, Vestland, Møre og Romsdal, Trøndelag.
    - 2020–2023: Viken, Vestfold og Telemark.
    - Før 2020: Hedmark, Oppland, Aust-Agder, Vest-Agder, Hordaland, Sogn og Fjordane, Sør-Trøndelag, Nord-Trøndelag.

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består, også `test_t1` til `test_t4`
