---
title: 'Story 1.7: Første backtestkjøring og rapport (A5)'
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

**Problem:** Backtest-skriptet finnes (Story 1.6), men er aldri kjørt på de ekte dataene. Gruppen vet derfor ikke om M1 (treffandel minst 25 %) og M1-C (presisjon minst 20 %) holder. Epic 2 kan ikke starte før tallene er rapportert (A5, FR27a, AR26).

**Approach:** Kjør `uv run python -m marin.backtest` én gang med de frosne parameterne, og commit `backtest.json`. Rapporter tallene uendret i README og PRD kap. 11. Gjelder reaksjonen på M1-C, oppdateres FR19-teksten og kap. 1 i PRD, EXPERIENCE.md og Story 2.6 før Epic 2 starter.

## Boundaries & Constraints

**Always:**
- Parameterne er vindu 5, minst 3 tellinger, horisont 6 og rød ved 0–3 uker. De står i `backtest.json` og er lik kjernens konstanter.
- Tallene rapporteres slik skriptet gir dem, også under tersklene (FR27a).
- Tersklene sjekkes eksakt med antallene, ikke med de avrundede andelene. M1 holder når treff × 4 ≥ kryssinger. M1-C slår inn når varsler med brudd × 5 < varsler.
- README får seksjonen `## Treffsikkerhet` med:
  - antall kryssinger, treff og treffandel
  - antall varsler, varsler fulgt av brudd og presisjon
  - utelatte kryssinger og varsler
  - parameterne og datoen for kjøringen
  - om M1 og M1-C holder
  
  Prosentene skrives med én desimal og desimalkomma, som i sammendraget fra skriptet.
- PRD kap. 11 («Treffsikkerhet») får de nye tallene i stedet for skissen og nevner skissen (omtrent 29 % treff og 14 % presisjon) til sammenligning. Videre i PRD-en:
  - A5 settes til gjort.
  - Punkt 4 og 5 i kap. 13 settes til gjort.
  - Statusen blir `final`, og `updated` settes til datoen for kjøringen.
  - Statuslinja øverst sier at A5 er gjort.
- `.logs/fredrik-ervik/issues.md` får et åpent punkt for refleksjonsrapporten: forskjellen fra skissen, med begge tallparene.
- Kjøringen starter først når gruppen har kontrollert fasiten i `backend/tests/data/backtest_liten.md` for hånd og signaturlinja er fylt ut og committet på denne grenen (avgjort 2026-11-25).
- M1-C-tekstene ble låst før kjøringen (avgjort 2026-11-25) og brukes uendret hvis M1-C slår inn:
  - FR19: «Prognosen er en enkel trendberegning, ikke en garanti. Rød status betyr at du bør følge ekstra med, ikke at grensen helt sikkert brytes. I en test på data fra 2025–2026 varslet Marin rødt 2–4 uker før X % av bruddene. Av alle røde varsler ble Y % fulgt av brudd innen 4 uker.»
  - Første setning i PRD kap. 1: «Marin er en web-app som gir driftsledere og fiskehelseansvarlige ved norske lakseoppdrettsanlegg en tidlig indikator på at anlegget kan være på vei mot å bryte lakselusgrensen.»
- Er treffandelen under 25 %, sier README, PRD kap. 11 og punktet for refleksjonsrapporten at SK2 og M1 ikke er oppfylt. Appens tekster endres bare av M1-C, slik PRD-en sier (avgjort 2026-11-25).

**Never:**
- Ingen endring i kode under `backend/src/`, i parameterne, i `datasett.json` eller i briefen.
- Ingen ny kjøring for å få andre tall. Stopper skriptet med en feil, stoppes storyen og feilen rapporteres. Koden rettes ikke i denne storyen.
- FR19-teksten bygges ikke i kode (Story 2.6). Ingen story i Epic 2 eller 3 startes.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Begge holder | treff × 4 ≥ kryssinger, og varsler med brudd × 5 ≥ varsler | README og PRD sier at M1 og M1-C holder. FR19, kap. 1, EXPERIENCE.md og Story 2.6 endres ikke | N/A |
| M1-C slår inn | varsler med brudd × 5 < varsler | den låste setningen erstatter første setning i PRD kap. 1. Den låste FR19-teksten legges til som teksten for presisjon under 20 % i PRD FR19, EXPERIENCE.md linje 111 og Story 2.6. README og PRD beskriver reaksjonen | N/A |
| M1 holder ikke | treff × 4 < kryssinger | README og PRD sier at SK2 og M1 ikke er oppfylt. Ingen tekster i appen endres av dette | N/A |
| Ikke signert | signaturlinja i `backtest_liten.md` er tom | ingen kjøring | storyen stoppes og det rapporteres |
| Akkurat på terskelen | nøyaktig 25 % eller 20 % | holder, fordi kravet er «minst» | N/A |
| Ny kjøring | den committede `backtest.json` og `kjor` til `tmp_path` | byte-like filer | testen feiler |
| Skriptet feiler | traceback eller ValueError | ingen `backtest.json` committes | storyen stoppes og feilen rapporteres |

</frozen-after-approval>

## Code Map

- `backend/src/marin/backtest/__init__.py` -- `resultatfil()` og `kjor(datasett, utfil, ut=None) -> int`. `__main__.py` bruker `datasettfil()` fra `marin.forbered`. Endres ikke.
- `backend/src/marin/kjerne/treffsikkerhet.py` -- `Backtestresultat` (`til_json`, `sammendrag`) og `PARAMETERE`. Endres ikke.
- `backend/tests/test_datasett_fil.py:31` -- forbildet for testen «den committede fila er lik en ny kjøring».
- `backend/tests/test_trend.py:309` -- låser parameterne (5, 3, 6, 3).
- `README.md` -- avsnittet om backtesten, med setningen «Skriptet skal ikke kjøres før Story 1.7 …», og linja «… tar omtrent 35 sekunder».
- `_bmad-output/planning-artifacts/prds/prd-Marin-2026-11-02/prd.md` -- linje 3 (status), 5 (`updated`), 17 (statuslinja), 21 (kap. 1), 74 (reaksjonen på M1-C), 179 (FR19), 330 (kap. 11), 345 (A5) og 353–354 (kap. 13).
- `_bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/EXPERIENCE.md:111` -- usikkerhetsteksten.
- `_bmad-output/planning-artifacts/epics.md:819-823` -- FR19 i Story 2.6.
- Git Bash bruker cp1252. Kjør skriptet med `PYTHONIOENCODING=utf-8`, ellers vises «ø» og «–» feil.

## Tasks & Acceptance

**Execution:**
- [ ] `backend/src/marin/data/backtest.json` -- kjør `uv run python -m marin.backtest` én gang i `backend/`, og ta vare på de fire linjene fra terminalen i Implementation Notes -- den første og offisielle kjøringen (A5).
- [ ] `backend/tests/test_backtest_fil.py` -- to tester: den committede fila er byte-lik en ny `kjor` til `tmp_path`, og `parametere` og `siste_uke` i fila er lik kjernens konstanter -- endres koden senere, feiler testen til tallene er rapportert på nytt.
- [ ] `README.md` -- bytt setningen om at skriptet ikke skal kjøres, med seksjonen `## Treffsikkerhet` etter Boundaries, og rett tiden testene tar etter en ny måling.
- [ ] `prd.md` -- kap. 11, A5, kap. 13, status og `updated` etter Boundaries, og reaksjonen etter matrisen.
- [ ] `EXPERIENCE.md` og `epics.md` -- bare hvis M1-C slår inn: den låste FR19-teksten legges til som teksten for presisjon under 20 %, ved siden av den vanlige teksten (EXPERIENCE.md linje 111) og i Story 2.6 linje 823. Den vanlige teksten blir stående, fordi Story 2.6 velger tekst etter presisjonen i fila (FR19 (1)).
- [ ] `.logs/fredrik-ervik/issues.md` -- punktet for refleksjonsrapporten.

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 490 fra før.
- Gitt `git diff` mot baseline, når endringene leses, så er ingen filer under `backend/src/` endret, bortsett fra den nye `backtest.json`.
- Gitt README, PRD kap. 11 og `backtest.json`, når de sammenlignes, så er antallene og prosentene de samme overalt.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Testen for ny kjøring tar omtrent 13 sekunder, og hele suiten går fra omtrent 37 til omtrent 50 sekunder. Den er med fordi den gjør FR27a etterprøvbar: endres kjernen etter rapporten, feiler testen, og tallene må kjøres og rapporteres på nytt i stedet for å bli stående stille.

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består
- `git status --short src/` -- expected: bare `src/marin/data/backtest.json` er ny

**Manual checks:**
- Tallene i README og PRD kap. 11 er lik `backtest.json` og terminalteksten i Implementation Notes.
