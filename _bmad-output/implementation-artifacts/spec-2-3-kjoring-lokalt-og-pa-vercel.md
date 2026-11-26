---
title: 'Story 2.3: Kjøring lokalt og på Vercel'
type: 'feature'
created: '2026-11-26'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Marin kan ikke kjøres som én prosess eller åpnes på nett. FastAPI serverer ikke frontend-bygget. Vercel-prosjektene publiserer ingenting: https://g01-ervik-kristiansen.vercel.app svarer 404, og prosjektet «backend» feiler ved hver push (NFR1, NFR12, AD-9).

**Approach:** FastAPI monterer `frontend/out/` etter alle `/api`-rutene når mappa finnes. `vercel.json` setter opp Vercel Services med `frontend` og `backend` i ett prosjekt. Next-bygget får en norsk 404-side, og README beskriver de tre kjøremåtene.

## Boundaries & Constraints

**Always:**
- **Lokal kjøring:** Når `frontend/out/` finnes, monterer appen mappa på `/` med Starlettes `StaticFiles(html=True)`, etter alle `/api`-rutene. Uten mappa starter appen som før. Testene kan gi appen en midlertidig mappe i stedet for det ekte bygget.
- **Ukjente stier:** En ukjent sti under `/api/` gir FastAPIs JSON 404 (`{"detail": …}`), også når mappa er montert. Denne ruten står ikke i skjemaet, så `openapi.json` er uendret.
- **Vercel:** `vercel.json` i rotmappa bruker `services`:
  - `frontend`: rot `frontend/`, rammeverk `nextjs`
  - `backend`: rot `backend/`, rammeverk `fastapi`, `entrypoint` `marin.api.app:app`
  
  `rewrites` sender `/api/(.*)` til `backend` og `/(.*)` til `frontend`, fra samme opphav. CORS og API-basen er uendret.
- **Oppstart på Vercel:** Vercel må kjøre `lifespan`. `/api/anlegg?q=x` svarer med FastAPIs JSON (501 med norsk `detail` til Story 2.4), ikke 500.
- **Fredrik i Vercel:** Fredrik setter Framework Preset til «Services» på prosjektet «g01-ervik-kristiansen», med rotmappa som Root Directory. Når forhåndsvisningen virker, kobler han fra eller sletter prosjektet «backend».
- **404-siden:** `frontend/src/app/not-found.tsx` viser «Fant ikke siden.» og lenken «Gå til forsiden» (til `/`). Tekstene ligger i `tekster.ts`, og siden bruker bare tokens. `out/404.html` har `lang="nb"`, ingen engelsk tekst fra Next og ingen mørk modus.
- **README:** En seksjon om kjøring beskriver:
  - utvikling med to prosesser: uvicorn med `--reload` på port 8000, og `npm run dev` på port 3000 (åpne `http://localhost:3000`)
  - lokal kjøring: `npm run build`, deretter uvicorn, og åpne `http://127.0.0.1:8000`
  - adressen https://g01-ervik-kristiansen.vercel.app
  
  README sier også at Next sender anonym telemetri, og at den slås av med `npx next telemetry disable`.
- **`.gitignore`:** har `frontend/AGENTS.md`.

**Never:**
- Ingen søk, prognose eller nye API-ruter (Story 2.4 og 2.5). Ingen endring i modellene, `openapi.json`, `marin.kjerne`, `marin.kilder`, `marin.forbered` eller `marin.backtest`.
- Ingen `experimentalServices`, `bindings` eller miljøvariabler. Ingen `.vercel/` i repoet.
- Ingen reserveplan med to Vercel-prosjekter. Hvis Services ikke virker, stopper vi og spør Fredrik.
- Lokal kjøring krever ikke nett, nøkler, miljøvariabler eller kontoer (NFR1).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Forside | mappa er montert, `GET /` | 200 med `index.html` | N/A |
| Detaljside direkte | `GET /anlegg/?nr=1` | 200 med `anlegg/index.html` | N/A |
| Uten skråstrek | `GET /anlegg?nr=1` | omdirigering til `/anlegg/?nr=1` | N/A |
| API først | `GET /api/anlegg?q=x`, mappa er montert | samme 501-svar som uten mappa | N/A |
| Ukjent API-sti | `GET /api/finnes-ikke`, mappa er montert | — | 404 med JSON `{"detail": …}`, ikke HTML |
| Ukjent side | `GET /finnes-ikke`, mappa er montert | — | 404 med `404.html` |
| Uten bygg | `frontend/out/` finnes ikke | appen starter, og `/api`-rutene virker | `/` gir JSON 404 |
| Vercel | forhåndsvisning av grenen | `/` gir forsiden, `/api/anlegg?q=x` gir JSON fra FastAPI, og `/finnes-ikke` gir den norske 404-siden | virker ikke Services, stopper vi og spør Fredrik |

</frozen-after-approval>

## Code Map

- `backend/src/marin/api/app.py` -- `app`, `levetid` (leser datasettet), CORS og de tre rutene. Monteringen kommer etter rutene. `hent_datasett` leser `app.state.datasett`.
- `backend/tests/test_api_app.py` -- bruker `with TestClient(app)`. Testen ved linje 99 sammenligner `openapi.json` med appen og må fortsatt bestå.
- `backend/pyproject.toml` -- pakken `marin` bygges med `uv_build`, krever Python 3.14 og har `uv.lock`. Dataene i `src/marin/data` er på 1,6 MB.
- `frontend/next.config.ts` -- `output: 'export'` og `trailingSlash: true` gir `out/index.html`, `out/anlegg/index.html` og `out/404.html`.
- `frontend/src/app/layout.tsx`, `frontend/src/app/globals.css` og `frontend/src/tekster.ts` -- rotlayouten, tokenene og de faste tekstene som 404-siden bygger på.
- `README.md` -- seksjonene «Backend og tester», «API-et» og «Frontend». Hver kodeblokk starter fra rotmappa.
- `.gitignore` -- seksjonen «Next.js / Node».
- **Vercel i dag:**
  - Prosjektet «g01-ervik-kristiansen» har ingen Root Directory. Forhåndsvisningene får adresser som `g01-ervik-kristiansen-git-<gren>-fredrik-ervik.vercel.app` og krever innlogging.
  - Prosjektet «backend» har rot `backend/` og feiler.
  - Produksjonsadressen svarer 404.
- **Vercel Services (vercel.com/docs/services og /kb/guide/python-backend-on-vercel, lest 2026-11-26):**
  - `services` med `root`, `framework` og `entrypoint` (`modul:app`, regnet fra `root`)
  - `rewrites` på toppnivå med `"destination": { "service": "<navn>" }`, der første treff gjelder
  - backend får hele stien (`/api/anlegg`)
  - Framework Preset må være «Services»
  
  Dokumentasjonen sier ingenting om src-layout, `lifespan` eller statisk eksport.

## Tasks & Acceptance

**Execution:**
- [ ] `backend/src/marin/api/app.py` -- monteringen av `frontend/out/` når mappa finnes, og JSON 404 for ukjente stier under `/api/`.
- [ ] `backend/tests/test_api_statisk.py` -- matriseradene for lokal kjøring, med en midlertidig mappe som har `index.html`, `anlegg/index.html` og `404.html`.
- [ ] `frontend/src/app/not-found.tsx` og `frontend/src/tekster.ts` -- den norske 404-siden.
- [ ] `vercel.json` -- `services` og `rewrites` etter Boundaries.
- [ ] `.gitignore` -- `frontend/AGENTS.md`.
- [ ] `README.md` -- de tre kjøremåtene, adressen og telemetrien.

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 540 fra før, og `openapi.json` er uendret.
- Gitt `npm run build` i `frontend/` og deretter `uv run uvicorn marin.api.app:app` i `backend/`, når `http://127.0.0.1:8000/` og `/anlegg/` åpnes, så vises forsiden og detaljsiden uten 404.
- Gitt `out/404.html` etter bygget, når fila leses, så har den «Fant ikke siden.», `lang="nb"` og ingen engelsk tekst eller `prefers-color-scheme: dark` fra Next.
- Gitt forhåndsvisningen på Vercel etter push, når Fredrik åpner den, så stemmer Vercel-raden i matrisen, og sjekken «Vercel – g01-ervik-kristiansen» består.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

`StaticFiles(html=True)` gir `index.html` for mapper og omdirigerer `/anlegg` til `/anlegg/` med spørringen. Den gir `404.html` med status 404 for filer som ikke finnes. Fordi monteringen ligger på `/`, ville den også tatt ukjente stier under `/api/`. En skjult rute (`include_in_schema=False`) for `GET` og `HEAD` på `/api/{sti:path}`, registrert etter de andre rutene og før monteringen, gir derfor FastAPIs JSON 404. Den gjelder bare `GET` og `HEAD`. Med alle metoder ville en feil metode på en kjent rute, som `POST /api/anlegg`, fått 404 i stedet for 405.

Mappa er `frontend/out/`, regnet fra rotmappa i repoet ut fra plasseringen til `app.py`. På Vercel er roten til backend `backend/`, så mappa finnes ikke der, og appen monterer ingenting. En fabrikk, som `lag_app(frontend_mappe)`, gjør at testene kan bruke en midlertidig mappe. `app = lag_app(...)` står fortsatt på modulnivå for uvicorn og Vercel.

Vercel må kunne importere `marin.api.app:app`. Hvis forhåndsvisningen viser at pakken ikke er installert, kan en liten fil i `backend/` importere appen. Det føres da i Implementation Notes.

## Verification

**Commands:**
- `uv run pytest` i `backend/` -- expected: alle består
- `git diff --exit-code backend/openapi.json` -- expected: ingen endring
- `npm run build` i `frontend/` -- expected: lykkes, og `out/404.html` er den norske siden

**Manual checks:**
- Etter bygget: start `uv run uvicorn marin.api.app:app` og åpne `/`, `/anlegg/?nr=1`, `/anlegg?nr=1`, `/api/finnes-ikke` og `/finnes-ikke`.
- Etter commit: push grenen. Fredrik åpner forhåndsvisningen og sjekker Vercel-raden i matrisen.
