---
title: 'Story 1.7: Første backtestkjøring og rapport (A5)'
type: 'feature'
created: '2026-11-25'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '609f383d49756191465f6a45f72d42bb8b770970'
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
- [x] `backend/src/marin/data/backtest.json` -- kjør `uv run python -m marin.backtest` én gang i `backend/`, og ta vare på de fire linjene fra terminalen i Implementation Notes -- den første og offisielle kjøringen (A5).
- [x] `backend/tests/test_backtest_fil.py` -- to tester: den committede fila er byte-lik en ny `kjor` til `tmp_path`, og `parametere` og `siste_uke` i fila er lik kjernens konstanter -- endres koden senere, feiler testen til tallene er rapportert på nytt.
- [x] `README.md` -- bytt setningen om at skriptet ikke skal kjøres, med seksjonen `## Treffsikkerhet` etter Boundaries, og rett tiden testene tar etter en ny måling.
- [x] `prd.md` -- kap. 11, A5, kap. 13, status og `updated` etter Boundaries, og reaksjonen etter matrisen.
- [x] `EXPERIENCE.md` og `epics.md` -- bare hvis M1-C slår inn: den låste FR19-teksten legges til som teksten for presisjon under 20 %, ved siden av den vanlige teksten (EXPERIENCE.md linje 111) og i Story 2.6 linje 823. Den vanlige teksten blir stående, fordi Story 2.6 velger tekst etter presisjonen i fila (FR19 (1)).
- [x] `.logs/fredrik-ervik/issues.md` -- punktet for refleksjonsrapporten.

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 490 fra før.
- Gitt `git diff` mot baseline, når endringene leses, så er ingen filer under `backend/src/` endret, bortsett fra den nye `backtest.json`.
- Gitt README, PRD kap. 11 og `backtest.json`, når de sammenlignes, så er antallene og prosentene de samme overalt.

## Implementation Notes

Forutsetningen var oppfylt: signaturlinja i `backtest_liten.md` er fylt ut og committet i `609f383` (baseline). `backtest.json` fantes ikke før kjøringen.

Den første og offisielle kjøringen ble gjort 2026-11-25 i Git Bash, i `backend/`, med `PYTHONIOENCODING=utf-8 uv run python -m marin.backtest`. Den tok omtrent 19 sekunder og ga exit-kode 0. De fire linjene fra terminalen, uendret:

```text
Skrev backtest.json for uke 1, 2025 til uke 42, 2026.
Kryssinger: 778 (44 før uke 9, 2025 er holdt utenfor). Treff: 127. Treffandel: 16,3 %.
Varsler: 5161 (281 etter uke 38, 2026 er holdt utenfor). Fulgt av brudd: 687. Presisjon: 13,3 %.
Parametere: vindu 5 uker, minst 3 tellinger, horisont 6 uker, rød ved 0–3 uker.
```

`backtest.json` har `treffandel` 0.1632 og `presisjon` 0.1331. Tersklene sjekket eksakt med antallene:

- M1: 127 × 4 = 508 < 778, så M1 holder ikke (SK2 og M1 er ikke oppfylt).
- M1-C: 687 × 5 = 3435 < 5161, så M1-C slår inn.

Det gir radene «M1-C slår inn» og «M1 holder ikke» i matrisen. Endret etter dem: PRD kap. 1 (låst setning), FR19 i PRD, en ny rad etter EXPERIENCE.md linje 111 og Story 2.6 linje 823 (låst FR19-tekst ved siden av den vanlige), reaksjonen i PRD kap. 2, kap. 11, A5, kap. 13, status og `updated`, README og `issues.md`.

Utenom listen: docstringen i `test_backtest.py` sa at ingen test kjører backtesten på de ekte dataene. Den sier nå at det gjelder testene i den fila, og viser til `test_backtest_fil.py`.

`uv run pytest` etterpå: 492 tester består (490 fra før og 2 nye), på omtrent 53 sekunder i to målinger. Den nye testen av en ny kjøring tar omtrent 18 sekunder.

Kontroll i steg 3 (orkestratoren):
- `uv run pytest` ga 492 bestått på 64 sekunder. Testen av en ny kjøring tok 22 sekunder, så tiden varierer med maskinen.
- Antallene og prosentene i README, PRD kap. 11 og `issues.md` er lik `backtest.json` og terminaltekstene.
- De to låste tekstene står ordrett der de skal.
- Den låste blokken er lik den i `609f383`.

Matrisen i specen har sju rader, og bare «Ny kjøring» gjelder kode. Den dekkes av `test_backtest_json_er_lik_en_ny_kjoring_av_backtest`. De andre seks radene gjelder hva som skrives i dokumentene, og om kjøringen skjer. De er kontrollert for hånd mot diffen:
- terskelregningen
- signaturen i baseline
- exit-koden 0

Bare radene «M1-C slår inn» og «M1 holder ikke» gjaldt for denne kjøringen.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Verification Gap + Edge Case | README sier at testen feiler til tallene er rapportert på nytt, men testen sjekker bare at `backtest.json` er lik en ny kjøring | low | patch | Bekreftet: kjøres skriptet på nytt, består testen selv om README og PRD kap. 11 har de gamle tallene. Setningen rettes, så det står at ny rapport er et manuelt steg. |
| 2 | Blind Hunter | README sier at usikkerhetsteksten på detaljsiden er endret, men detaljsiden finnes ikke ennå | low | patch | Bekreftet: bare kravene er endret (PRD, EXPERIENCE.md og Story 2.6). Appen viser teksten først fra Story 2.6. |
| 3 | Edge Case + Blind Hunter | Story 2.6 sier «presisjonen i fila under 20 %», og PRD FR19 sier ikke hvordan teksten velges | low | patch | Bekreftet: den naturlige lesningen er den avrundede `presisjon`, og 0,19996 lagres som 0,2000. Specen sier at tersklene sjekkes eksakt med antallene. Story 2.6 og FR19 skal si antallene. |
| 4 | Blind Hunter | Tidene spriker: testdocstringen har faste sekunder, og Design Notes i specen sier 13 og 50 sekunder | low | patch | Sekundene i docstringen fjernes, fordi målingene varierer fra 18 til 22 sekunder. Delen om Design Notes avvises, fordi fiksen er å endre specen. Målingene står i Implementation Notes. |
| 5 | Blind Hunter + Edge Case | Punkter i `issues.md` som storyen løste, står fortsatt åpne | low | patch | Bekreftet for disse punktene: signaturen, PYTHONIOENCODING, PRD til `final`, ny kjøring med FR27 og testtiden i README. Lukkes i sesjonsloggen, som eier `issues.md`. |
| 6 | Blind Hunter | Det vanlige eksempelet i PRD FR19 sier «ga Marin varsel … Av alle varsler», mens Story 2.6 og EXPERIENCE.md sier «varslet Marin rødt … Av alle røde varsler» | low | defer | Bekreftet, men avviket fantes før: ordlyden ble avgjort 2026-11-18 i Story 2.6 uten at FR19 ble rettet. Ført i `deferred-work.md`. |
| 7 | Edge Case | `test_backtest_fil.py` gir FileNotFoundError uten forklaring hvis `backtest.json` mangler | low | avvist | Testen feiler høylytt, og fila er committet. Det er lite trolig at noen møter dette, og fiksen er en ny vakt. |
| 8 | Edge Case + Blind Hunter | Reserveteksten når fila mangler, har ikke M1-C-forbeholdet | low | avvist | Teksten velges etter tallene i fila (FR19 (1)). Uten fil vet appen ikke presisjonen. Fila er committet og testet, så reserveteksten vises bare når noe allerede er galt. Fiksen krever en ny beslutning. |
| 9 | Edge Case | En senere kjøring med presisjon ≥ 20 % gir normal tekst i appen, mens PRD og README sier tidlig indikator | low | avvist | Dette er hypotetisk. En ny kjøring må rapporteres på nytt (nr. 1), og da endres dokumentene også. |
| 10 | Edge Case + Blind Hunter | Sprint-status sier `in-progress`, mens specen sier `in-review` | false | avvist | Steg 5 i bmad-build setter `review`, som i 1.6. |
| 11 | Blind Hunter | Docstringen i `backend/src/marin/backtest/__init__.py` sier at den første kjøringen er Story 1.7 | false | avvist | Setningen er fortsatt sann: den første kjøringen ble gjort i Story 1.7. |
| 12 | Blind Hunter | Matrisekontrollen i Implementation Notes går ikke opp | low | avvist | Fiksen er å endre specen. |
| 13 | Blind Hunter | Den andre testen i `test_backtest_fil.py` tilfører lite, mangler en melding og sjekker ikke `versjon` | false | avvist | Den gjør ingen skade. Specen ba om den, og byte-testen fanger det samme. |
| 14 | Blind Hunter | PRD kap. 11 har resultater i stedet for en risiko, og den gjenværende risikoen er borte | false | avvist | Raden sier at SK2 og M1 ikke er oppfylt, og at reaksjonen på M1-C slo inn. Reaksjonen er tiltaket mot falske alarmer. |
| 15 | Blind Hunter | Kap. 13 i PRD sier ikke hva som kommer etterpå | low | avvist | Epic 2 står i `epics.md` og sprint-status. Innholdet ligger utenfor intensjonen. |
| 16 | Blind Hunter | UJ-2 i EXPERIENCE.md («om hun kan stole på varselet») og M1-raden rammer Marin som et pålitelig varsel | false | avvist | M1-raden er målet som ble målt, og skal stå. I UJ-2 sjekker Kari selv om hun kan stole på varselet, og det passer med en tidlig indikator. |
| 17 | Blind Hunter | `backtest.json` mangler grensene for utelatte og datasettets identitet | false | avvist | Feltlista er låst i AD-10 (som nr. 12 i 1.6). Byte-testen feiler hvis grensene eller dataene endres, og Verification Gap har bekreftet det. |

## Design Notes

Testen for ny kjøring tar omtrent 13 sekunder, og hele suiten går fra omtrent 37 til omtrent 50 sekunder. Den er med fordi den gjør FR27a etterprøvbar: endres kjernen etter rapporten, feiler testen, og tallene må kjøres og rapporteres på nytt i stedet for å bli stående stille.

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består
- `git status --short src/` -- expected: bare `src/marin/data/backtest.json` er ny

**Manual checks:**
- Tallene i README og PRD kap. 11 er lik `backtest.json` og terminalteksten i Implementation Notes.
