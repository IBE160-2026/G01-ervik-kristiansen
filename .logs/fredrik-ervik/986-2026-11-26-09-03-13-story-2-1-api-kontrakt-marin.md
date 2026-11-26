# Story 2.1 API-kontrakt marin

## 2026-11-26 kl. 09:03 — Fredrik Ervik

### Oppgave
Fredrik ba meg fortsette der vi slapp 25.11. Story 2.1, API-kontrakten for kjerneflyten, var implementert og ferdig reviewet med `bmad-build`, men ikke avsluttet, committet eller logget.

### Plan
- Den forrige økten (25.11) ble ikke logget. Det som skjedde da, er hentet fra specen og git:
  - Grenen `story/2-1-api-kontrakten-for-kjerneflyten` ble laget fra `main` etter at Story 1.7 og Epic 1 ble satt til `done` (`e0042fc`).
  - Specen ble committet som `ready-for-dev` (`cc61fce`, baseline for storyen).
  - Implementeringen og reviewen (Blind Hunter, Edge Case Hunter og Verification Gap) ga 20 funn, ført i Review Triage Log i specen. 4 skulle rettes, og 16 ble avvist. Ingen ble utsatt.
- I dag:
  - Kontrollerte at de 4 rettelsene er i koden:
    - en test for at felt som kan være `null`, står under `required`
    - docstringen om nuller på slutten i JSON
    - `summary` med ø og `operationId` lik funksjonsnavnet
    - FR4–FR6 i docstringen til `sok_anlegg`
  - Kjørte verifiseringen i specen og akseptkriteriene.
  - Fortsatte `bmad-build` fra steg 4. Kjørte ikke reviewen på nytt, fordi triage-loggen var komplett og rettelsene var gjort.
- Spec: [spec-2-1-api-kontrakten-for-kjerneflyten.md](../../_bmad-output/implementation-artifacts/spec-2-1-api-kontrakten-for-kjerneflyten.md).

### Resultat
- `uv run pytest` ga 540 bestått (492 fra før og 48 nye) på omtrent 89 sekunder.
- `uv run python -m marin.api.openapi` skriver samme `openapi.json`, og testen som sammenligner fila med appen, består.
- `uv run uvicorn marin.api.app:app` starter uten feil. `/docs` svarer 200, skjemaet har de tre rutene, og `/api/anlegg?q=hitra` svarer 501 med «Søket er ikke bygget ennå. Det kommer i Story 2.4.».
- Ingen filer under `marin/kjerne`, `marin/kilder`, `marin/forbered` eller `marin/backtest` er endret siden `cc61fce`.
- Commit `05478f7`:
  - `marin.api` med `modeller.py`, `app.py` og `openapi.py`
  - `backend/openapi.json`
  - `test_api_modeller.py` og `test_api_app.py`
  - FastAPI, Pydantic og Uvicorn i `pyproject.toml` og `uv.lock`, med `httpx2` som dev-avhengighet
  - seksjonen API-et i README
- Specen står som `done`, og Story 2.1 står som `review` i sprint-status.
- Lukket i `issues.md`: Pydantic sender lusetall (Decimal) som JSON-tall (`Lusetall` i `modeller.py`, testet med `0.28`).
- Fredrik ba meg pushe og lage PR-en: [PR #9](https://github.com/IBE160-2026/G01-ervik-kristiansen/pull/9).
- Story 2.2 genererer frontend-typene fra `backend/openapi.json`, som kommer med 2.1. Fredrik valgte å flette PR #9 før grenen for 2.2 lages fra `main`.

### Åpne punkter
- Story 2.5: 404 for et ukjent anlegg må føres opp i `openapi.json` når ruten bygges (triage-funn 3 i spec-2-1).
- Story 2.3: sjekk at Vercels Python-runtime kjører `lifespan`, ellers lastes ikke datasettet.
- Epic 3: CORS tillater bare `GET`. Opplastingsrutene trenger `POST` og `Content-Type` i `allow_headers`.
