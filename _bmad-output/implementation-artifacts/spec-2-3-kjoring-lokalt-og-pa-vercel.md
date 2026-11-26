---
title: 'Story 2.3: Kjøring lokalt og på Vercel'
type: 'feature'
created: '2026-11-26'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '9616518dc020adacb2ab452b6edcd962527ca738'
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
- [x] `backend/src/marin/api/app.py` -- monteringen av `frontend/out/` når mappa finnes, og JSON 404 for ukjente stier under `/api/`.
- [x] `backend/tests/test_api_statisk.py` -- matriseradene for lokal kjøring, med en midlertidig mappe som har `index.html`, `anlegg/index.html` og `404.html`.
- [x] `frontend/src/app/not-found.tsx` og `frontend/src/tekster.ts` -- den norske 404-siden.
- [x] `vercel.json` -- `services` og `rewrites` etter Boundaries.
- [x] `.gitignore` -- `frontend/AGENTS.md`.
- [x] `README.md` -- de tre kjøremåtene, adressen og telemetrien.

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 540 fra før, og `openapi.json` er uendret.
- Gitt `npm run build` i `frontend/` og deretter `uv run uvicorn marin.api.app:app` i `backend/`, når `http://127.0.0.1:8000/` og `/anlegg/` åpnes, så vises forsiden og detaljsiden uten 404.
- Gitt `out/404.html` etter bygget, når fila leses, så har den «Fant ikke siden.», `lang="nb"` og ingen engelsk tekst eller `prefers-color-scheme: dark` fra Next.
- Gitt forhåndsvisningen på Vercel etter push, når Fredrik åpner den, så stemmer Vercel-raden i matrisen, og sjekken «Vercel – g01-ervik-kristiansen» består.

## Implementation Notes

- **Appen:**
  - De tre rutene ligger i en `APIRouter` (`ruter`).
  - `lag_app(frontend_bygg=FRONTEND_BYGG)` lager appen med samme tittel, `lifespan`, CORS og operationId som før.
  - `FRONTEND_BYGG` er `Path(__file__).resolve().parents[4] / "frontend" / "out"`.
  - `app = lag_app()` står fortsatt på modulnivå.
- **Med bygget montert** svarer appen annerledes på tre forespørsler, alle med JSON. Ingen av dem brukes av frontenden, og på Vercel monteres ingenting. Se funn 2, 3 og 17 i Review Triage Log.
  - `HEAD` på en kjent rute gir 404 i stedet for 405.
  - `/api/anlegg/` med skråstrek til slutt gir 404 i stedet for 307.
  - Andre metoder enn GET og HEAD til en ukjent `/api/`-sti gir 405 i stedet for 404.
- **404-siden:** `not-found.tsx` bruker bare tokenklasser. Lenken er minst 44px høy på mobil og 24px på desktop. Tekstene ligger i `tekster.ikkeFunnet`.
- **Sjekket lokalt** (`npm run build` med `NEXT_TELEMETRY_DISABLED=1`):
  - `out/404.html` har `lang="nb"`, «Fant ikke siden.» og «Gå til forsiden», og verken engelsk tekst eller `prefers-color-scheme`.
  - JS-fila for Next sin innebygde feilside har fortsatt mørk modus. Den er utsatt i `deferred-work.md`.
  - Mot ekte `uv run uvicorn marin.api.app:app` gir `/` og `/anlegg/?nr=1` 200, og `/anlegg?nr=1` gir 307 til `/anlegg/?nr=1`. `/api/anlegg?q=x` gir 501 med JSON, `/api/finnes-ikke` gir 404 med JSON, og `/finnes-ikke` gir 404 med den norske siden.
- **Vercel er ikke sjekket ennå.** Det skjer med forhåndsvisningen etter push.
  - Vercels side om Python-runtimen (lest 2026-11-26) sier at `modul:app` slås opp som en fil regnet fra roten (`marin/api/app.py`). Hos oss ligger fila i `backend/src/marin/api/app.py`, så reserven i Design Notes kan bli nødvendig.
  - Ifølge samme side støttes Python 3.14 og `lifespan`, og funksjonene kan være opptil 500 MB.
- **Reserven for importen trengtes.** Det første bygget på Vercel (`7156991`) feilet med `[ENTRYPOINT_NOT_FOUND] Service "backend" has entrypoint "marin/api/app.py" but that path does not exist.`
  - `backend/vercel_inngang.py` legger `src/` først i importstien og importerer `app` fra `marin.api.app`.
  - `vercel.json` peker på `vercel_inngang:app`.
  - To tester sjekker at inngangen gir den samme appen, og at `vercel.json` peker dit (`fdbd05b`).
- **Vercel er sjekket 2026-11-26** på forhåndsvisningen av `fdbd05b` (`dpl_BYKWaQEjTi3AZkXC8RrVHHriui6y`), med `vercel curl`. Sjekken «Vercel – g01-ervik-kristiansen» består.
  - `/` og `/anlegg/?nr=1` gir 200 med `lang="nb"`.
  - `/anlegg?nr=1` gir 308 til `/anlegg/?nr=1`.
  - `/api/anlegg?q=x` gir 501 med JSON og norsk `detail`. Avhengigheten leser datasettet først, så `lifespan` har kjørt.
  - `/api/anlegg/10560/prognose?ar=2026&uke=10` gir 501 med JSON.
  - `/api/finnes-ikke` gir 404 med JSON fra FastAPI.
  - `/finnes-ikke` gir 308 til `/finnes-ikke/`, som gir 404 med den norske siden.
- **Sjekken «Vercel – backend» feiler fortsatt.** Den kommer fra det gamle prosjektet, som Fredrik skal koble fra eller slette.
- `vercel curl` la til en hemmelighet av typen «Protection Bypass for Automation» på Vercel-prosjektet (`prj_JAHvyBU5tCa0bBCREKXJSlKH0VRA`). Den gjelder til den trekkes tilbake under Deployment Protection.

## Spec Change Log

## Review Triage Log

Svarene under er sjekket med TestClient mot `lag_app(FRONTEND_BYGG)` og `lag_app(None)`. Alle API-svarene er JSON, også med bygget montert.

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Verification Gap | Ingen test serverer det ekte `frontend/out/`. AK 2 og 3 er bare sjekket for hånd, og fixture-filene skjuler en endret mappestruktur eller en manglende `not-found.tsx` | low | patch | Kommer ferdig verifisert fra revieweren: bygget virker i dag, men et bygg uten `trailingSlash` eller uten den norske 404-siden gir grønne tester. Rettes med en test som bruker det ekte bygget når det finnes. |
| 2 | Verification Gap | `POST /api/finnes-ikke` med bygget gir 405 (`Allow: GET, HEAD`), uten bygget 404 | low | reject | Bekreftet. Svaret er fortsatt JSON. Frontenden sender ingen andre metoder enn GET, og en rettelse krever en ny gren i den skjulte ruten. |
| 3 | Blind Hunter | `GET /api/anlegg/?q=x` gir 404 med bygget, men 307 til `/api/anlegg?q=x` uten | low | reject | Bekreftet. Frontenden kaller rutene uten skråstrek til slutt, og en rettelse krever en omdirigering i den skjulte ruten. |
| 4 | Blind Hunter | `GET /api` gir `404.html` med bygget, men JSON 404 uten | false | reject | Dette gjør også Vercel: `/api/(.*)` treffer ikke `/api`, så stien går til frontend og gir 404-siden. Regelen i specen gjelder stier under `/api/`. |
| 5 | Blind Hunter | Feil metode gir andre svar med bygget: `POST` til en ukjent sti gir 405, og `Allow` for `POST /api/anlegg` blir `GET, HEAD` i stedet for `GET` | low | reject | Bekreftet. Statusen for den kjente ruten er fortsatt 405 med JSON. Samme grunn som nr. 2. |
| 6 | Blind Hunter | Testene avhenger av om det finnes et lokalt bygg, og rekkefølgen sjekkes bare når bygget finnes | false | reject | `test_api_rutene_kommer_foran_bygget` og de andre testene på `lag_app(bygg)` sjekker rekkefølgen uten det ekte bygget. `test_api_app.py` og `test_api_statisk.py` består med og uten `frontend/out/` (41 tester begge gangene). |
| 7 | Blind Hunter | I utvikling serverer backend også et gammelt bygg på port 8000, og README sier ikke fra | false | reject | README ber om å åpne port 3000 i utvikling. Den sier også at FastAPI serverer `frontend/out/` når mappa finnes, og at bygget må lages på nytt etter endringer. |
| 8 | Blind Hunter | Appen sier ikke fra om bygget ble funnet. `parents[4]` stemmer bare når pakken er installert redigerbart | low | reject | `uv sync`, som README bruker, installerer pakken redigerbart. En logglinje er ny oppførsel som ingen kjøremåte i specen trenger. |
| 9 | Blind Hunter | Specen er uferdig: `in-review`, tomme avkrysningsbokser og tomme Implementation Notes | — | reject | Rettelsen er å endre specen for denne storyen. `in-review` er statusen arbeidsflyten setter, og boksene og notatene fylles ut før storyen legges fram. |
| 10 | Blind Hunter | Vercel er ikke sjekket, men diffen ser ferdig ut | false | reject | AK 4 og Vercel-raden er den manuelle sjekken etter push i Verification. Storyen settes ikke til `done` før Fredrik har sett forhåndsvisningen. |
| 11 | Blind Hunter | README sier at appen er publisert, men nevner ikke innstillingene i Vercel | low | patch | Den som setter opp prosjektet på nytt, får et bygg som feiler uten Framework Preset «Services». En setning i «På nett» retter det. |
| 12 | Blind Hunter | «tre måter … trengs ikke nett» gjelder ikke den tredje måten, som er på nett | low | patch | Setningen skal bare gjelde de to lokale måtene. |
| 13 | Blind Hunter | Next sin innebygde feilside, på engelsk og med mørk modus, er med i hver side og vises når appen krasjer i nettleseren | medium | defer | Bekreftet i `out/_next/static/chunks/` (`--next-error-*` under `prefers-color-scheme: dark`). Den fantes før denne storyen, fra Story 2.2. Sidene har ingen kode som kan krasje ennå, så `global-error.tsx` hører til når den første klientkoden kommer (2.4). |
| 14 | Blind Hunter | AK 3 har ingen automatisk sjekk mot det ekte bygget | low | patch | Samme rotårsak som nr. 1, rettes med samme test. |
| 15 | Blind Hunter | `/404/`, `/404.html` og `/_not-found/` gir 404-siden med status 200 | low | reject | Bekreftet. Ingen lenker går dit, og en rettelse krever en egen underklasse av `StaticFiles`. |
| 16 | Blind Hunter | 404-siden har fanetittelen «Marin», så tittelen sier ikke at siden ikke ble funnet | low | defer | Alle sidene har tittelen «Marin» fra rotlayouten i Story 2.2. Titler per side avgjøres samlet, senest med detaljsiden i 2.7. |
| 17 | Edge Case Hunter | `HEAD /api/anlegg?q=x` gir 404 med bygget, men 405 uten | low | reject | Bekreftet. Frontenden sender ikke HEAD, og en rettelse krever en ny gren i den skjulte ruten. |
| 18 | Edge Case Hunter | Andre metoder enn GET og HEAD til en ukjent `/api/`-sti gir 405 i stedet for JSON 404 | low | reject | Samme som nr. 2. |
| 19 | Edge Case Hunter | Skråstrek til slutt (`/api/anlegg/`, `/docs/`) gir 404 med bygget, men 307 uten | low | reject | Samme som nr. 3. `/docs/` gir 404-siden med bygget. |
| 20 | Edge Case Hunter | `/api` og `/API/x` går til bygget og gir HTML | false | reject | Samme som nr. 4. Appen bruker ingen av disse adressene. |
| 21 | Edge Case Hunter | `test_appen_monterer_det_ekte_bygget_bare_nar_det_finnes` kan feile hvis `frontend/out/` lages eller slettes mens testene kjører, og gir `AttributeError` hvis `FRONTEND_BYGG` er `None` | low | patch | Appen lages ved import og mappa sjekkes senere, så et `npm run build` under en kjøring på 18 minutter kan få testen til å feile. Rettes ved å lage appen i testen. `None` skjer aldri i dette repoet, siden fila ligger fire nivåer under rotmappa. |
| 22 | Edge Case Hunter | README sier at en ukjent adresse under `/api/` gir JSON 404, men det gjelder bare GET og HEAD | false | reject | Setningen handler om adresser som åpnes i nettleseren, altså GET. Andre metoder får også JSON (405). |
| 23 | Edge Case Hunter | Kommentaren i `lag_app` sier at en feil metode på en kjent rute fortsatt gir 405, men HEAD gir 404 | low | patch | Bekreftet. Kommentaren skal si at det gjelder andre metoder enn GET og HEAD. |
| 24 | Edge Case Hunter | README sier at bygget serveres på alle adresser utenom `/api/`, men `/docs`, `/redoc` og `/openapi.json` hører også til FastAPI | low | patch | Bekreftet. Rettes med ordlyden. |

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
