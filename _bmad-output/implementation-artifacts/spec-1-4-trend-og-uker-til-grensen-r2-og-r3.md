---
title: 'Story 1.4: Trend og uker til grensen (R2 og R3)'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'b47bb274d6f4c743980352b7a681d5e4bea23d10'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/_bmad-output/planning-artifacts/briefs/brief-Marin-2026-09-17/a4-handkontroll.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Kjernen kan finne grensen (R1), men ikke regne prognosen. Story 1.5 (status), backtesten og detaljsiden trenger vinduet, trendlinja og uker til grensen etter R2 og R3, med de samme tallene som fasiten T5, T6, T8, T10 og T12 (FR8, FR11–FR13).

**Approach:** En ny modul `marin.kjerne.trend` med fire byggeklosser: `siste_telling`, `vindu`, `trendlinje` og `uker_til_grensen`. Regresjonen regnes eksakt med brøker, og estimatene kommer ut som `Decimal` avrundet med halvdeler opp. Status og `vurder` kommer i Story 1.5.

## Boundaries & Constraints

**Always:**
- `siste_telling(serie, analyseuke) -> Telling | None`: siste telling med verdi til og med a. Tellinger etter a og uker uten verdi brukes ikke (FR8).
- `vindu(serie, analyseuke) -> tuple[Telling, ...]`: tellingene med verdi i uke t − 4 til og med t, stigende. Tom når t mangler. `vindu` sjekker ikke om t er for gammel. Det gjør status i 1.5.
- `trendlinje(tellinger) -> Trend`: minste kvadraters metode med `uker.lopende(uke)` som x. Krever minst `MINSTE_TELLINGER` tellinger, alle med verdi og ulike uker, ellers ValueError. `Trend.stigning` er en `Fraction` per uke.
- `Trend.estimat(uke) -> Decimal`: eksakt verdi på linja. Under 0 blir 0,00 (FR13), ellers avrundet til 2 desimaler med halvdeler opp.
- `uker_til_grensen(trend, omrade, analyseuke) -> int | None`: første k fra 1 til `HORISONT` der `er_brudd(trend.estimat(a + k), grense(omrade, a + k))`. Grensen hentes for hver uke (R3), og k telles fra a, ikke fra t. `None` betyr «ingen kryssing innen 6 uker». Ukjent område gir ValueError.
- `konstanter.py` får `VINDU = 5`, `MINSTE_TELLINGER = 3` og `HORISONT = 6` (FR27a). Ingen parametre kan overstyres.
- Regresjonen bruker `fractions.Fraction` og aldri flyttall. `tall.avrund_brok(Fraction) -> Decimal` avrunder eksakt med halvdeler opp, med samme resultat som `avrund` og aldri −0,00.
- Feil type inn gir TypeError, som i resten av kjernen. Kommentarer, docstrings og testnavn er på norsk.

**Never:**
- Ingen status, `vurder`, farger eller tekster (Story 1.5), og ingen graf- eller tabelldata (Epic 2).
- Kalleren kutter aldri serien. Funksjonene ser selv bort fra tellinger etter a.
- Ingen `round()`, `float` eller nye avhengigheter. Ingen endring i `avrund`, `Serie` eller R1.

## I/O & Edge-Case Matrix

Alle er i sør med analyseuke a lik siste uke, hvis ikke annet står.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| T5 | uke 30–34: 0,06 / 0,12 / 0,18 / 0,24 / 0,30 | stigning 0,06, estimat 0,48 i uke 37 og 0,54 i uke 38, 4 uker | N/A |
| T6 og R3 | uke 10–14: 0,10 / 0,12 / 0,14 / 0,16 / 0,18 | stigning 0,02, 0,20 i uke 15 og 0,22 i uke 16, 2 uker. Nord (0,5 i uke 15–20) gir `None` | N/A |
| T8 | uke 36, 38, 40: 0,20 / 0,28 / 0,36 | stigning 0,04 (ikke 0,08), 0,48 i uke 43 og 0,52 i uke 44, 4 uker | N/A |
| T10b | T8-tellingene, a = 41 | samme linje, 3 uker (uke 44) | N/A |
| T12 | 2025 u50 til 2026 u2: 0,30 / 0,34 / 0,38 / 0,42 / 0,46 | stigning 0,04, nøyaktig 0,50 i 2026 u3, 1 uke | N/A |
| FR13 | uke 30–34: 0,40 / 0,30 / 0,20 / 0,10 / 0,00 | estimat 0,00 i uke 35, ikke −0,10 | N/A |
| Halv opp | uke 30–34: 0 / 0 / 0 / 0,35 / 0,40 | eksakt 0,495 i uke 35 blir 0,50, 1 uke | N/A |
| FR8 | T5 pluss 9,99 i uke 35, a = 34 | samme t, vindu og svar som T5 | N/A |
| Tom uke | a har `Telling(a, None)` | t = a − 1, og vinduet er a − 5 til a − 1 | N/A |
| Ingen telling | ingen verdi til og med a | `siste_telling` gir `None`, `vindu` gir () | N/A |
| Uke 53 | horisonten går over 2026 u53 | 2026 u53 og 2027 u1 er ett steg | N/A |
| For få | 2 tellinger (T9) | — | ValueError i `trendlinje` |
| Ukjent | `Omrade.UKJENT` | — | ValueError i `uker_til_grensen` |

</frozen-after-approval>

## Code Map

- `backend/src/marin/kjerne/uker.py` -- `lopende`, `pluss`, `mellom`. Brukes som de er.
- `backend/src/marin/kjerne/lusegrense.py` -- `grense(omrade, uke)` og `er_brudd(verdi, grense)`, som krever avrundet verdi. Brukes som de er.
- `backend/src/marin/kjerne/tall.py` -- `avrund(Decimal)`. Får `avrund_brok` ved siden av.
- `backend/src/marin/kjerne/konstanter.py` -- `SISTE_UKE`. Docstringen sier allerede at R2-parameterne skal hit.
- `backend/src/marin/kjerne/modeller.py` -- `Serie.tellinger` er sortert, med én telling per uke og `verdi` som er `None` eller avrundet `Decimal`.
- `backend/tests/test_kjerne_importer.py` -- forbyr `round`, klokka og andre imports enn stdlib i `kjerne/`. Settet over moduler får `trend.py`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/src/marin/kjerne/konstanter.py` -- `VINDU`, `MINSTE_TELLINGER` og `HORISONT` som `Final`, med docstring om FR27a
- [x] `backend/src/marin/kjerne/tall.py` -- `avrund_brok(verdi: Fraction) -> Decimal`, eksakt med halvdeler opp og bort fra null, som `ROUND_HALF_UP`
- [x] `backend/src/marin/kjerne/trend.py` -- `siste_telling`, `vindu`, `Trend` (frossen dataclass) med `estimat`, `trendlinje` og `uker_til_grensen` etter Boundaries
- [x] `backend/tests/test_tall.py` -- `avrund_brok` gir det samme som `avrund` for alle tusendeler fra −1 til 1, og 1/3 gir 0,33, 2/3 gir 0,67 og 1/200 gir 0,01. Flyttall og Decimal gir TypeError
- [x] `backend/tests/test_trend.py` -- én test per rad i matrisen. Fasiten heter `test_t5_…`, `test_t6_…`, `test_t8_…`, `test_t10_…` og `test_t12_…`. I tillegg: manglende rader og rader med `None` gir samme svar
- [x] `backend/tests/test_kjerne_importer.py` -- legg `trend.py` til i settet over moduler

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 292 fra før.
- Gitt I/O-matrisen, når testene leses, så har hver rad minst én test som kjører og består.
- Gitt kildekoden i `kjerne/trend.py`, når den leses, så finnes ingen `float`, `round` eller Decimal-divisjon i regresjonen.

## Implementation Notes

- `Trend` har feltene `stigning`, `x_snitt` og `y_snitt` (alle `Fraction`). Linja går gjennom (x̄, ȳ), der x̄ er snittet av løpende ukenummer. `estimat` regner ȳ + b · (x − x̄) eksakt, setter negative verdier til 0 og avrunder med `avrund_brok`.
- `avrund_brok` godtar bare `Fraction`. Også `int` gir TypeError. Resultatet lages som `Decimal(f"{hundredeler}E-2")`, som er eksakt og ikke avhenger av presisjonen i konteksten.
- `uker_til_grensen` gir TypeError når `omrade` ikke er tekst, og ellers ValueError for ukjente koder via `Omrade(omrade)`, som `grense`.
- `test_trend.py` har også en ast-test som viser at `trend.py` ikke bruker `float`, flyttallskonstanter eller `Decimal(...)`.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Verification Gap + Blind Hunter | Ingen test viser at regresjonen er eksakt. Er ȳ regnet med Decimal-divisjon, består alle testene | medium | patch | Bekreftet av Verification Gap med en mutasjon: 2136 tester består. 0,00 / 0,01 / 0,33 i uke 30, 31 og 34 gir eksakt 0,495 i uke 36 og 2 uker, mens Decimal gir 0,49 og 3 uker. Testen med 0,495 har bare endelige desimaltall og fanger det ikke. |
| 2 | Verification Gap (andre funn) | Kommentaren i ast-testen sier at ingen Decimal deles i `trend.py`, men testen finner bare kall til `Decimal(...)` | low | patch | Samme rotårsak som nr. 1. Kommentaren rettes, og den nye testen i nr. 1 dekker regnestykket. |
| 3 | Blind Hunter | 2 001 parametriserte avrundingstester tar testtallet fra 292 til 2 342 | low | patch | Bekreftet: testtallet blir misvisende, for eksempel i rapporten. At kjøringen gikk fra 38 til 62 sekunder, skyldtes ikke dette. Etter fiksen tar den fortsatt 56 sekunder, og nesten all tiden går i de to testene som leser hele Excel-utdraget (28 og 23 sekunder). Én test med løkke sjekker det samme. |
| 4 | Blind Hunter | R3 er bare testet der vårgrensen begynner i sør. Slutten på vårperioden og vårukene i nord er ikke testet | low | patch | Koden er riktig, men en feil som brukte laveste grense i hele horisonten, ville ikke blitt fanget. Backtesten går gjennom begge overgangene hvert år. To tester legges til. |
| 5 | Blind Hunter | Områdekoder som tekst («sor», «nord», «vest») er ikke testet i `uker_til_grensen` | low | patch | Signaturen tar `Omrade | str`. Bare «ukjent» er testet. En parametrisert test legges til. |
| 6 | Blind Hunter | `test_feil_type_gir_typeerror` har 11 tilfeller i én løkke, og `trendlinje(serie)` feiler i `tuple()`, ikke i sjekken | low | patch | Bekreftet: `Serie` kan ikke itereres. Testen parametriseres med id-er, og tilfellet beskrives som det er. |
| 7 | Blind Hunter | Fem `pytest.raises(ValueError)` uten `match=` | low | patch | Testene består også om en annen regel kaster ValueError. `match=` legges til. |
| 8 | Blind Hunter + Edge Case | `trendlinje` godtar tellinger over mer enn ett vindu eller etter a | low | patch | Skjer bare om noen går utenom `vindu`. En ny sjekk ville vært en regel specen ikke har. Docstringen sier nå at tellingene skal komme fra `vindu`. |
| 9 | Blind Hunter | Modul-docstringen i `trend.py` sier at funksjonene ikke kutter serien, og nevner ikke `Trend` | low | patch | Formuleringen er uklar. Den skrives om: den som kaller, trenger aldri å kutte serien. |
| 10 | Edge Case | Med feil type for analyseuka og ukjent område gir `uker_til_grensen` ValueError i stedet for TypeError | low | patch | Bekreftet: typesjekken for analyseuka kommer etter `Omrade(omrade)`. Sjekken flyttes opp. |
| 11 | Blind Hunter | Sprint-status skulle stått som `review`, ikke `in-progress` | false | avvist | Steg 5 i bmad-build setter `review` når endringen presenteres, slik det skjedde i 1.3 (`8299ef1`). |
| 12 | Blind Hunter | Kravet om at t høyst er én uke eldre, mangler i `konstanter.py` | false | avvist | FR27a fryser fire parametre: vindu, minste antall tellinger, horisont og rød ved 0–3 uker. Regelen om én uke kommer fra § 6 og er en del av statusen (FR8) i Story 1.5. |
| 13 | Blind Hunter | «For lite data» kan bare sjekkes ved å fange ValueError | false | avvist | Story 1.5 kan sammenligne `len(vindu(...))` med `MINSTE_TELLINGER`, så tallet står fortsatt ett sted. |
| 14 | Edge Case | Et estimat på 10²⁶ eller mer gir `InvalidOperation` i `er_brudd` | false | avvist | Leseren avviser lusetall med 20 sifre eller mer, og 1.5 stopper gamle t før trenden. Ellers feiler koden med en tydelig feil. |
| 15 | Edge Case | t i år 1, uke 1–4, gir ValueError fra `date.fromordinal` | false | avvist | Kan ikke skje med data fra 2000 og senere (FR24), og feilen er tydelig. |
| 16 | Edge Case | Analyseuke sent i år 9999 gir ValueError midt i horisonten | false | avvist | Kan ikke skje med årene appen godtar, og feilen er tydelig. |
| 17 | Edge Case | Samme som nr. 8: regresjonen kan bruke data utenfor vinduet | low | patch | Slått sammen med nr. 8, som har samme rotårsak. |
| 18 | Blind Hunter | Ast-testen sjekker mindre enn akseptansekriterium 3 | medium | patch | Samme rotårsak som nr. 1 og rettes med den samme testen. |

## Design Notes

Hvorfor brøker: med `Decimal` blir ȳ = 0,34/3 rundet av etter 28 sifre. Et estimat som eksakt er x,xx5, kan da havne på x,xx4999… og rundes ned. Det kan flytte en kryssing én uke. Håndkontrollen A4 er regnet med eksakte brøker, og `Fraction` gir de samme tallene. Bare sluttsvaret blir `Decimal`, slik AD-6 krever.

```python
trend = trendlinje(vindu(serie, a))      # ValueError ved færre enn 3
trend.stigning == Fraction("0.06")       # T5
trend.estimat(Uke(2026, 38)) == Decimal("0.54")
uker_til_grensen(trend, Omrade.SOR, a)   # 4, eller None
```

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består
