---
title: 'Story 1.6: Backtest etter SK2'
type: 'feature'
created: '2026-11-25'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Kjernen gir status per uke, men ingenting måler hvor godt statusen varsler brudd. Gruppen trenger treffandel og presisjon etter SK2 for å vite om M1 holder (FR27, FR27a, FR28, FR29, AD-1, AD-10).

**Approach:** SK2-funksjonene ligger som rene funksjoner i `marin.kjerne.treffsikkerhet` og henter status bare fra `vurder`. `uv run python -m marin.backtest` er et tynt skall som leser `datasett.json`, kaller kjernen og skriver `backtest.json` og et sammendrag i terminalen. Den første ekte kjøringen er Story 1.7.

## Boundaries & Constraints

**Always:**
- Status for uke a er `vurder(hele serien, omrade, a)` for hver a fra `FORSTE_UKE` (2025 uke 1) til `SISTE_UKE`. Ingen kaller kutter serien (AD-1). Området er `omrade_fra_fylke(info.fylke)`.
- Kryssing: uke w med telling der verdien er ≥ grensen i uke w (`er_brudd`), og forrige telling, i w − 1 eller ellers w − 2, er under grensen i sin uke. En uke uten verdi er ikke en telling. Har verken w − 1 eller w − 2 en telling, er w ikke en kryssing. Ukjent område gir ingen kryssinger.
- Treff: den sammenhengende perioden med rød status (`Farge.ROD`, altså varsel og brudd nå) som slutter i w − 1, begynte i w − 4, w − 3 eller w − 2. Alle andre farger bryter perioden. `er_treff(kryssing, rode_uker)` tar ukene med rød status, så den kan testes uten regresjon.
- Varsel: uke a med `Arsak.VARSEL`. Den er fulgt av brudd når minst én telling i a + 1 til a + 4 er ≥ grensen i sin uke.
- Kryssinger før 2025 uke 9 (`FORSTE_KRYSSING`) og varsler etter 2026 uke 38 (`SISTE_VARSEL`) holdes utenfor og telles i `utelatt_kryssinger` og `utelatt_varsler`.
- `Backtestresultat` (frossen dataclass i kjernen) har feltene fra AD-10 og i tillegg `antall_varsler_med_brudd`, som er telleren i presisjonen. Rekkefølgen i fila er `versjon`, `parametere`, `siste_uke`, `antall_kryssinger`, `antall_treff`, `antall_varsler`, `antall_varsler_med_brudd`, `utelatt_kryssinger`, `utelatt_varsler`, `treffandel` og `presisjon`. `versjon` er 1. `parametere` er `{"vindu", "minste_tellinger", "horisont", "maks_uker_rod"}` med kjernens konstanter. `siste_uke` er `{ar, uke}`. `treffandel` er treff/kryssinger og `presisjon` er varsler med brudd/varsler. Begge regnes eksakt og avrundes til 4 desimaler med halvdeler opp. Er nevneren 0, gir det ValueError.
- `til_json()` gir teksten i fila: alle tall er JSON-tall uten flyttall, og `json.loads(tekst, parse_float=Decimal)` gir de samme verdiene. Samme resultat gir alltid samme tekst. Fila skrives som UTF-8 med `\n`.
- Skallet skriver fire linjer til terminalen. `<P>` og `<Q>` er prosent med én desimal, halvdeler opp og desimalkomma (for eksempel «28,3»), regnet fra antallene. Ukene og parameterne kommer fra konstantene:
  `Skrev backtest.json for uke 1, 2025 til uke 42, 2026.`
  `Kryssinger: <K> (<U> før uke 9, 2025 er holdt utenfor). Treff: <T>. Treffandel: <P> %.`
  `Varsler: <V> (<W> etter uke 38, 2026 er holdt utenfor). Fulgt av brudd: <B>. Presisjon: <Q> %.`
  `Parametere: vindu 5 uker, minst 3 tellinger, horisont 6 uker, rød ved 0–3 uker.`
- Et lite, konstruert datasett i `backend/tests/data/` har forventede tall regnet ut for hånd (NFR10). Det har minst ett treff, én kryssing med rød status bare uka før, én kryssing der den røde perioden begynte 5 uker før, én uke med brudd etter to uker uten telling, ett varsel fulgt av brudd, ett varsel uten brudd, én kryssing før 2025 uke 9, ett varsel etter 2026 uke 38 og ett anlegg med ukjent område.
- Fasiten for det lille datasettet: KI lager datasettet og regner tallene, med begrunnelse per anlegg i `backtest_liten.md`. Gruppen kontrollerer tallene for hånd før PR-en flettes, som med A4 (avgjort 2026-11-25).

**Never:**
- Ingen kjøring på de ekte dataene og ingen `backtest.json` i `src/marin/data/` (Story 1.7). Ingen rute, side eller lesing av `backtest.json` i API-et (FR29, Epic 2). Ingen FR19-tekst.
- Ingen endring i `status.py`, `trend.py`, `lusegrense.py` eller parameterne. Ingen parameter kan overstyres (FR27a).

## I/O & Edge-Case Matrix

Alle er i sør i 2026, hvis ikke annet står.

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Kryssing uka før | 0,40 i uke 30, 0,50 i uke 31 | kryssing i uke 31 | N/A |
| Kryssing w − 2 | 0,40 i uke 30, tom uke 31, 0,55 i uke 32 | kryssing i uke 32 | N/A |
| To tomme uker | 0,40 i uke 29, tomme uker 30–31, 0,60 i uke 32 | ingen kryssing | N/A |
| Allerede over | 0,50 i uke 30, 0,60 i uke 31 | ingen kryssing | N/A |
| Grense i sin uke | 0,30 i uke 15 og 16 | kryssing i uke 16 (0,5 → 0,2). 0,30 i uke 21 og 22 gir ingen | N/A |
| Ukjent område | tellingene fra «Kryssing uka før» og T6, med `Omrade.UKJENT` | ingen kryssinger og ingen varsler (i sør gir de én kryssing og ett varsel) | N/A |
| Treff | kryssing i uke 31, rød i uke 27–30, 28–30 eller 29–30 | treff | N/A |
| Ikke treff | rød bare i uke 30, rød i uke 26–30 eller ingen rød i uke 30 | ikke treff | N/A |
| Brutt periode | kryssing i uke 31, rød i uke 26 og 28–30 | treff (perioden begynte i uke 28) | N/A |
| Over årsskiftet | kryssing i 2026 uke 2, rød i 2025 uke 51 til 2026 uke 1 | treff (begynte w − 3) | N/A |
| Brudd etter varsel | varsel i uke 30, ≥ grensen i uke 34, eller bare i uke 35 | fulgt av brudd, eller ikke | N/A |
| Vårgrense etter varsel | varsel i uke 12, 0,25 i uke 16 | fulgt av brudd (grensen 0,2) | N/A |
| Utelatte | kryssing i 2025 uke 8 og uke 9, varsel i 2026 uke 38 og uke 39 | uke 8 og uke 39 telles som utelatt, uke 9 og uke 38 er med | N/A |
| Lite datasett | `backend/tests/data/` | antall kryssinger, treff, varsler, varsler med brudd og utelatte er lik tallene regnet ut for hånd | N/A |
| Tom nevner | datasett uten kryssinger eller uten varsler | — | ValueError |

</frozen-after-approval>

## Code Map

- `backend/src/marin/kjerne/status.py` -- `vurder(serie, omrade, analyseuke) -> Vurdering` med `farge` og `arsak`. `Farge.ROD` er både varsel og brudd nå. Endres ikke.
- `backend/src/marin/kjerne/lusegrense.py` -- `grense(omrade, uke)` (None ved ukjent) og `er_brudd(verdi, grense)` (≥). `omrade.py` -- `omrade_fra_fylke(fylke)`.
- `backend/src/marin/kjerne/uker.py` -- `alle_uker(fra, til)` (inklusive), `pluss`, `mellom` og `lopende`. `Uke` kan sorteres og hashes. 2026 har uke 53, så 2025 uke 1 til 2026 uke 42 er 94 uker.
- `backend/src/marin/kjerne/konstanter.py` -- `SISTE_UKE`, `VINDU`, `MINSTE_TELLINGER`, `HORISONT` og `MAKS_UKER_ROD`. Her legges `FORSTE_UKE`.
- `backend/src/marin/kjerne/modeller.py` -- `Serie.tellinger` er en sortert tuple og kan ikke itereres direkte. Det finnes ingen oppslag fra uke til verdi, så lag en dict per serie.
- `backend/src/marin/kjerne/tall.py` -- `avrund_brok(Fraction)` gir 2 desimaler med halvdeler opp. Bruk samme metode (ROUND_HALF_UP) for 4 desimaler.
- `backend/src/marin/kilder/datasett.py` -- `Datasett.fra_json(tekst)` og `last()`. `til_json()` er forbildet for deterministisk JSON uten flyttall.
- `backend/src/marin/forbered/__init__.py` -- forbildet for skallet: `datasettfil()` (bruk den om igjen), `kjor(..., ut=None, feilut=None) -> int`, `files("marin")`, og `__main__.py` med `sys.exit(kjor(...))`.
- `backend/tests/test_forbered.py` -- testmønsteret: `tmp_path`, `io.StringIO` som `ut`, eksakt tekst og byte-lik fil ved ny kjøring.
- `backend/tests/test_kjerne_importer.py` -- bare stdlib og `marin.kjerne` i kjernen, og ingen `round`. Modulsettet må få `treffsikkerhet.py`.
- `backend/tests/hjelp_serie.py` -- `lag_serie`, `fortlopende` og T5.
- `README.md` -- `uv run python -m marin.forbered` står i linje 35–38.

## Tasks & Acceptance

**Execution:**
- [ ] `backend/src/marin/kjerne/konstanter.py` -- `FORSTE_UKE: Final = Uke(2025, 1)`, den første analyseuka for de innebygde dataene
- [ ] `backend/src/marin/kjerne/treffsikkerhet.py` -- `FORSTE_KRYSSING`, `SISTE_VARSEL`, `kryssinger(serie, omrade)`, `er_treff(kryssing, rode_uker)`, `fulgt_av_brudd(serie, omrade, varsel)`, `Backtestresultat` med `til_json()`, og `backtest(anlegg: Iterable[tuple[Serie, Omrade | str]]) -> Backtestresultat` etter Boundaries
- [ ] `backend/src/marin/backtest/__init__.py` og `__main__.py` -- `resultatfil()` (pakkens `data/backtest.json`) og `kjor(datasett, utfil, ut=None) -> int`, som leser med `Datasett.fra_json`, kaller `backtest`, skriver fila og skriver sammendraget
- [ ] `backend/tests/data/backtest_liten.json` og `backtest_liten.md` -- det lille datasettet i formatet til `datasett.json`, og tallene regnet ut for hånd med begrunnelse per anlegg
- [ ] `backend/tests/test_treffsikkerhet.py` -- én test per rad i matrisen, og en test som sjekker tallene for det lille datasettet mot `backtest_liten.md`
- [ ] `backend/tests/test_backtest.py` -- `kjor` på det lille datasettet til `tmp_path`: feltene og verdiene i fila, eksakt terminaltekst, byte-lik fil ved ny kjøring, ingen `\r\n`, og stien til `resultatfil()`
- [ ] `backend/tests/test_kjerne_importer.py` -- legg `treffsikkerhet.py` til i modulsettet
- [ ] `README.md` -- kommandoen `uv run python -m marin.backtest` ved siden av `marin.forbered`, med en setning om at den første kjøringen og tallene kommer i Story 1.7

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 424 fra før.
- Gitt I/O-matrisen, når testene leses, så har hver rad minst én test som kjører og består.
- Gitt `marin.backtest`, når koden leses, så kaller skallet bare `Datasett.fra_json`, `backtest` og `til_json` og regner ingenting selv, og `backend/src/marin/data/backtest.json` finnes ikke.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

`er_treff` tar et sett med røde uker i stedet for serien. Da kan reglene for røde perioder testes med uker skrevet rett inn, uten å regne regresjon, og `backtest` lager settet fra `vurder` én gang per anlegg. En full kjøring er omtrent 1 092 anlegg × 94 uker, eller rundt 100 000 kall til `vurder`, og tar omtrent 13 sekunder. Derfor kjører ingen test på de ekte dataene.

`antall_varsler_med_brudd` er med i fila fordi akseptansekriteriet krever tallet, og fordi FR19 (Epic 2) da kan regne hele prosent fra antallene og ikke fra en andel som allerede er avrundet.

```python
er_treff(Uke(2026, 31), {Uke(2026, w) for w in (28, 29, 30)})   # True, begynte w − 3
er_treff(Uke(2026, 31), {Uke(2026, w) for w in (26, 27, 28, 29, 30)})   # False, begynte w − 5
```

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består
