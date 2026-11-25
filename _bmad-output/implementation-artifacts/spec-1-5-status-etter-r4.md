---
title: 'Story 1.5: Status etter R4'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'cd1b63ab825791b17981a42f69b0b877d10f8be4'
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Kjernen har byggeklossene fra R1–R3, men ingen inngang som gir status. Appen og backtesten må få samme status og tekst for samme serie, område og analyseuke (FR8, FR13, FR14, AD-1, AD-2, AD-7).

**Approach:** `marin.kjerne.status.vurder(serie, omrade, analyseuke) -> Vurdering` går gjennom R4 i fast rekkefølge med byggeklossene fra `marin.kjerne.trend` og lager statuskodene og R4-teksten tegn for tegn som i briefen. Forklaringssetningene (FR15a, FR20) kommer i Story 2.6.

## Boundaries & Constraints

**Always:**
- Rekkefølgen (første som slår til): 1) ukjent område, 2) ingen ny telling: t finnes og `mellom(t, a) > 1`, 3) brudd nå: `er_brudd(verdi i t, grense(omrade, a))`, med grensen i analyseuka, 4) for lite data: `len(vindu) < MINSTE_TELLINGER`, 5) prognose: `uker_til_grensen` gir rød ved 1–`MAKS_UKER_ROD`, gul ved høyere og grønn ved `None`.
- Finnes ingen telling til og med a, blir statusen «– For lite data», fordi 0 av de 5 siste ukene har telling (R2). Ingen ny tekst (avgjort 2026-11-23).
- `Vurdering` (frossen dataclass): `farge: Farge`, `arsak: Arsak`, `symbol`, `tekst`, `uke_tekst: str | None`, `estimert_uke: EstimertUke | None`, `siste_telling: Telling | None` og `trend: Trend | None`. `EstimertUke(uke: Uke, uker_til: int)` har samme form som `estimert_uke` i `Detaljsvar` (AD-3). `Farge` og `Arsak` er `StrEnum` med kodene fra AD-7.
- `estimert_uke` og `uke_tekst` («(uke Y)») finnes bare ved varsel og følg med (FR18). `trend` finnes bare ved varsel, følg med og ingen kryssing. `siste_telling` er `siste_telling(serie, a)` for alle statuser.
- Tekstene i `tekst` står uten symbol. `f"{symbol} {tekst}"` er tegn for tegn lik briefens R4: «✕ Brudd nå», «✕ Varsel: grensen nås om X uker», «! Følg med: grensen kan nås om X uker», «✓ Ingen kryssing ventet innen 6 uker», «– For lite data», «– Ingen ny telling siden uke X» og «? Ukjent område: grensen kan ikke bestemmes». Symbolene er ✕ U+2715, ! U+0021, ✓ U+2713, – U+2013 og ? U+003F. Ved X = 1 står «1 uke» (T12).
- Uker i tekstene får år bare når året er et annet enn analyseukas: «uke 40», men «uke 50, 2025» og «(uke 1, 2027)» (EXPERIENCE.md).
- `konstanter.py` får `MAKS_UKER_ROD = 3`. `vurder` har bare de tre argumentene, så ingen parameter kan overstyres (FR27a).
- `vurder(serie: Serie, omrade: Omrade | str, analyseuke: Uke)` tar hele serien. Tellinger etter a brukes ikke (FR8). Alle tre argumentene sjekkes før regel 1. Feil type gir TypeError, også et område som ikke er tekst. En ukjent områdekode gir ValueError.

**Never:**
- Ingen forklarende setning, grafdata, tabell, API eller backtest. Ingen endring i `trend.py`, R1 eller `avrund`.

## I/O & Edge-Case Matrix

Alle er i sør med analyseuke a lik siste uke, hvis ikke annet står. T5, T6, T8, T10 og T12 bruker tellingene fra `test_trend.py`.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| T5 | uke 30–34 | gul, `folg_med`, «! Følg med: grensen kan nås om 4 uker», «(uke 38)», `EstimertUke(uke 38, 4)` | N/A |
| T6 | uke 10–14 | rød, `varsel`, «✕ Varsel: grensen nås om 2 uker», «(uke 16)» | N/A |
| T7 | T5-tellingene, `Omrade.UKJENT` | grå, «? Ukjent område: grensen kan ikke bestemmes», `uke_tekst` `None` | N/A |
| T8 | uke 36, 38, 40 | «! Følg med: grensen kan nås om 4 uker», «(uke 44)» | N/A |
| T9 | 0,20 i uke 38 og 0,30 i uke 40 | grå, `for_lite_data`, «– For lite data» | N/A |
| T10 | T8-tellingene, a = 42 og a = 41 | «– Ingen ny telling siden uke 40». Med a = 41: «✕ Varsel: grensen nås om 3 uker», «(uke 44)» | N/A |
| T11 | 0,30 i uke 29 og 0,60 i uke 30 | rød, `brudd_na`, «✕ Brudd nå», `estimert_uke` `None` | N/A |
| T12 | 2025 u50 til 2026 u2 | «✕ Varsel: grensen nås om 1 uke», «(uke 3)» | N/A |
| Grønn | 0,10 i uke 36–40 | grønn, `ingen_kryssing`, «✓ Ingen kryssing ventet innen 6 uker» | N/A |
| Grense i a | 0,30 i uke 15, ingen telling i uke 16, a = 16 | «✕ Brudd nå» (grensen 0,2 i uke 16) | N/A |
| FR8 | T5 + 0,90 i uke 36 | a = 34: lik vurderingen uten uke 36. a = 36: «✕ Brudd nå» | N/A |
| År i tekst | siste telling 2025 u50, a = 2026 u1 | «– Ingen ny telling siden uke 50, 2025» | N/A |
| År og uke 53 | 0,26 / 0,30 / 0,34 / 0,38 / 0,42 i 2026 u48–52, a = 2026 u52. 2026 har uke 53 (0,46), og 2027 u1 gir 0,50, som i `test_horisonten_over_uke_53_er_ett_steg_per_uke` | «✕ Varsel: grensen nås om 2 uker», «(uke 1, 2027)» | N/A |
| Ingen telling | a = 2026 u34. Tom serie, eller bare tomme uker og tellinger etter a | grå, `for_lite_data`, «– For lite data», `siste_telling` `None` | N/A |
| Feil inn | områdekode «vest», eller serie og uke av feil type | — | ValueError og TypeError |

</frozen-after-approval>

## Code Map

- `backend/src/marin/kjerne/trend.py` -- `siste_telling`, `vindu`, `trendlinje` (ValueError ved færre enn 3), `uker_til_grensen` (ValueError ved ukjent område, `None` ved ingen kryssing). `vindu` sjekker ikke alderen på t. Endres ikke.
- `backend/src/marin/kjerne/lusegrense.py` -- `grense(omrade, uke)` og `er_brudd`. `backend/src/marin/kjerne/omrade.py` -- `Omrade(StrEnum)`.
- `backend/src/marin/kjerne/uker.py` -- `mellom`, `pluss`. `backend/src/marin/kjerne/formatering.py` -- `format_uke` gir alltid år.
- `backend/src/marin/kjerne/konstanter.py` -- `VINDU`, `MINSTE_TELLINGER`, `HORISONT`. Docstringen sier at rød-grensen kommer hit.
- `backend/tests/test_lusegrense.py` -- T1–T4 finnes som `test_t1_…`–`test_t4_…`. `backend/tests/test_trend.py` -- hjelperne `lag_serie` og `fortlopende`, tellingene T5, T6, T8 og T12 og `test_parameterne_er_fryst_etter_fr27a`. `backend/tests/hjelp_xlsx.py` er forbildet for en delt hjelpemodul.
- `backend/tests/data/format.json` -- vektorene som frontend også testes mot. Gjelder bare `format_lus`, `format_grense` og `format_uke`.
- `backend/tests/test_kjerne_importer.py` -- settet over moduler får `status.py`.

## Tasks & Acceptance

**Execution:**
- [x] `backend/src/marin/kjerne/konstanter.py` -- `MAKS_UKER_ROD: Final = 3`, og oppdatert docstring
- [x] `backend/src/marin/kjerne/formatering.py` -- `format_uke_i_tekst(uke, analyseuke)`: «uke 44» i samme år, ellers «uke 1, 2027». Docstringen sier at den bare brukes i backend, fordi backend eier statustekstene (AD-2), og derfor ikke har vektorer i `format.json`
- [x] `backend/src/marin/kjerne/status.py` -- `Farge`, `Arsak`, `EstimertUke`, `Vurdering` og `vurder` etter Boundaries
- [x] `backend/tests/hjelp_serie.py` -- flytt `lag_serie`, `fortlopende` og T5, T6, T8 og T12 hit fra `test_trend.py`
- [x] `backend/tests/test_trend.py` -- importer hjelperne fra `hjelp_serie`. `test_parameterne_er_fryst_etter_fr27a` sjekker også `MAKS_UKER_ROD == 3`
- [x] `backend/tests/test_formatering.py` -- `format_uke_i_tekst` i samme og i et annet år, begge veier
- [x] `backend/tests/test_status.py` -- én test per rad i matrisen. Fasiten heter `test_t5_…` til `test_t12_…` og sjekker `f"{symbol} {tekst}"` mot briefen. I tillegg: en tabell med de 7 årsakene og riktig `farge` og `symbol` for hver, og at `estimert_uke`, `uke_tekst` og `trend` bare finnes der Boundaries sier
- [x] `backend/tests/test_kjerne_importer.py` -- legg `status.py` til i settet over moduler

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 359 fra før, og T1–T12 finnes som navngitte tester.
- Gitt I/O-matrisen, når testene leses, så har hver rad minst én test som kjører og består.
- Gitt `vurder`, når signaturen leses, så tar den bare `serie`, `omrade` og `analyseuke`.

## Implementation Notes

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Verification Gap | Ingen `vurder`-test har tellinger før t − 4, så en endring som dropper vinduet, blir ikke fanget | medium | patch | Bekreftet med en mutasjon: alle 53 testene i `test_status.py` består når vinduet erstattes med alle tellinger til og med a. Kontrollert: 0,10 i uke 20–22 og 0,30 i uke 33–34 med a = 34 gir «– For lite data». 5,00 i uke 29 foran T5 gir samme vurdering som T5 alene. To tilfeller legges til. |
| 2 | Blind Hunter | Øvre del av gul (5 og 6 uker) og grønn ved 7 uker er ikke testet gjennom `vurder` | low | patch | Bekreftet: bare 3 og 4 uker er testet. 0,43/0,44/0,45, 0,42/0,43/0,44 og 0,41/0,42/0,43 i uke 30–32 med a = 32 gir 5 uker «(uke 37)», 6 uker «(uke 38)» og grønn. En parametrisert test legges til. |
| 3 | Blind Hunter | `test_nord_har_vargrensen_i_uke_21_26` tester ikke det navnet sier | low | patch | Bekreftet: testen viser bare at nord ikke har vårgrense i uke 15–20. 0,30 i uke 20 i nord gir «✕ Brudd nå» med a = 21 (grensen 0,2), og «– For lite data» med a = 20. Det tilfellet legges til. |
| 4 | Blind Hunter | Stien til `a4-handkontroll.md` i docstringen finnes ikke fra repo-roten | low | patch | Bekreftet: `briefs/…` mangler `_bmad-output/planning-artifacts/`. Stien er kopiert fra `test_trend.py` til `hjelp_serie.py` og rettes begge steder. |
| 5 | Blind Hunter | Docstringen i `hjelp_serie.py` sier at fasiten står ett sted, men T9, T11 og FLAT står i `test_status.py` | false | avvist | «Dem» i docstringen er T5, T6, T8 og T12, som begge testfilene bruker. T9, T11 og FLAT brukes bare i `test_status.py`, så de står også ett sted. |
| 6 | Blind Hunter | Docstringen i `trend.py` sier «Status kommer i Story 1.5.» | low | defer | Bekreftet (linje 14). Specen forbyr endringer i `trend.py` (Never), så linja rettes i en senere story. |
| 7 | Blind Hunter | `Vurdering` mangler det Story 2.6 trenger: antall tellinger i vinduet, grensen og analyseuka | low | defer | Bekreftet for antallet («Bare 2 av de siste 5 ukene …»): `vurder` regner det ut og kaster det. Grensen og analyseuka har API-et selv, fordi det kaller `vurder` med dem. Feltene er låst i intensjonen, så 2.6 må velge mellom et nytt felt og et nytt kall til `vindu`. |
| 8 | Edge Case + Blind Hunter | `EstimertUke` godtar `uker_til` som er 0, negativ eller over `HORISONT` | low | avvist | Bare `vurder` lager den, med `uker_til` fra `uker_til_grensen`, som alltid er 1–6. Ingen kaller som kan lage en ugyldig, er vist, og fiksen er en ny vakt. |
| 9 | Edge Case + Blind Hunter | `Vurdering` sjekker ikke at farge, symbol og felt passer med årsaken | low | avvist | Alle vurderinger lages i `_vurdering` fra `_FARGE_OG_SYMBOL`, og tabellen er testet for alle 7 årsakene. Fiksen er en ny `__post_init__`-vakt uten noen kjent kaller. |
| 10 | Edge Case | t i år 1, uke 1–4, eller en analyseuke sent i år 9999 gir ValueError fra datoregningen | false | avvist | Som nr. 15 og 16 i Story 1.4: det kan ikke skje med data fra 2000 og senere (FR24), og feilen er tydelig. |
| 11 | Blind Hunter | Sprint-status står som `in-progress`, mens specen er `in-review` | false | avvist | Steg 5 i bmad-build setter `review` når endringen presenteres (som nr. 11 i Story 1.4). |
| 12 | Blind Hunter | Implementation Notes og Spec Change Log er tomme, og matrisen sier at tellingene ligger i `test_trend.py` | low | avvist | Fiksen er å endre specen. Matrisen er låst, og oppgavelista sier at tellingene flyttes til `hjelp_serie.py`. |
| 13 | Blind Hunter | Ingen test har uker etter t som finnes, men er tomme | false | avvist | En slik regresjon fanges allerede. «uke 16 uten verdi» i `test_brudd_na_bruker_grensen_i_analyseuka` har en tom rad etter t, og «bare tomme uker» i `test_ingen_telling_til_og_med_a_gir_for_lite_data` har bare tomme rader. |
| 14 | Blind Hunter | To overflødige asserts: `estimert_uke is None` i T11 og siste linje i AD-7-testen | false | avvist | De gjør ingen skade. Assertet i T11 speiler matriseraden («`estimert_uke` `None`»). |

## Design Notes

`siste_telling` og `trend` er med i `Vurdering`, slik at Story 2.5 og 2.6 (tabell, graf og forklaring) bruker den samme linja og ikke regner den ut på nytt. Backtesten trenger bare `farge` og `arsak`. `forklaring` er ikke et felt: Story 2.6 lager den som en egen funksjon av `Vurdering`, og API-et setter den inn i `status`. Da trenger ikke `Vurdering` å endres. For «ingen telling» gir malen i EXPERIENCE.md «Bare 0 av de siste 5 ukene …», så 2.6 må vurdere ordlyden der.

```python
v = vurder(serie, Omrade.SOR, Uke(2026, 34))   # T5
(v.farge, v.arsak) == (Farge.GUL, Arsak.FOLG_MED)
f"{v.symbol} {v.tekst}" == "! Følg med: grensen kan nås om 4 uker"
(v.uke_tekst, v.estimert_uke) == ("(uke 38)", EstimertUke(Uke(2026, 38), 4))
```

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består
