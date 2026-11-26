# Story 2.3 kjøring lokalt og på Vercel marin

## 2026-11-26 kl. 13:29 — Fredrik Ervik

### Oppgave
Fredrik ba meg planlegge Story 2.3, kjøring lokalt og på Vercel, med `bmad-build` på grenen `story/2-3-kjoring-lokalt-og-pa-vercel`. Storyen tas først fordi Vercel Services (beta) er den største risikoen før fristen 15.12.2026.

### Plan
- **Steg 1–2:**
  - `epic-2-context.md` var gyldig.
  - Leste Story 2.3 i `epics.md`, AD-9 i arkitekturen og Vercels sider om Services, Python og FastAPI.
  - Jeg fant at det ikke fantes noen `vercel.json`. Prosjektet «g01-ervik-kristiansen» bygger uten Root Directory, og prosjektet «backend» feiler ved hver push. Produksjonsadressen svarer 404.
- **Fredriks valg:**
  - én spec for lokal kjøring og Vercel
  - Vercel Services i ett prosjekt, ikke reserveplanen
  - en egen norsk 404-side
  - en linje om telemetrien i README
  - `frontend/AGENTS.md` i `.gitignore`
- **Spec:** [spec-2-3-kjoring-lokalt-og-pa-vercel.md](../../_bmad-output/implementation-artifacts/spec-2-3-kjoring-lokalt-og-pa-vercel.md). Fredrik godkjente den med «Godkjenn og fortsett», og den ble committet som `ready-for-dev` (`9616518`, baseline).

### Resultat
- **Implementeringen**, gjort av en agent som bare hadde specen:
  - `marin.api.app` har fått `lag_app(frontend_bygg)`. Den monterer `frontend/out/` på `/` med `StaticFiles(html=True)` etter alle `/api`-rutene, når mappa finnes.
  - En skjult rute for GET og HEAD på `/api/{sti:path}` gir JSON 404.
  - `vercel.json` har `services`: `frontend` (Next.js) og `backend` (FastAPI, `marin.api.app:app`). Rewrites sender `/api/(.*)` til backend og resten til frontend.
  - `not-found.tsx` viser «Fant ikke siden.» og «Gå til forsiden».
  - README har en ny seksjon, «Kjøring», med utvikling, lokal kjøring og adressen på nett, og en linje om telemetrien.
  - `frontend/AGENTS.md` står i `.gitignore`.
- **Verifisert:**
  - `uv run pytest` gir 559 bestått (540 fra før og 19 nye i `test_api_statisk.py`), og `openapi.json` er uendret.
  - `npm run build` lager `out/404.html` med `lang="nb"` og den norske teksten, uten engelsk tekst og uten mørk modus.
  - Mot ekte uvicorn gir `/` og `/anlegg/?nr=1` 200, `/anlegg?nr=1` gir 307 og `/api/anlegg?q=x` gir 501 med JSON. `/api/finnes-ikke` gir 404 med JSON, og `/finnes-ikke` gir den norske 404-siden.
- **Review** med Blind Hunter, Edge Case Hunter og Verification Gap ga 24 funn, ført i Review Triage Log i specen:
  - **Rettet (7):**
    - en test mot det ekte bygget når det finnes
    - en test som lager appen i testen, så den ikke feiler hvis `npm run build` kjøres samtidig
    - kommentaren om HEAD
    - tre setninger i README
  - **Utsatt (2, `deferred-work.md`):** en norsk `global-error.tsx` i Story 2.4 og egne titler per side senest i Story 2.7.
  - **Avvist (15).** Blant dem er tre små avvik i API-svarene når bygget er montert: HEAD, skråstrek til slutt og andre metoder enn GET. Alle svarene er fortsatt JSON, og frontenden bruker ingen av dem.
- Commit `dc99958`. Specen står som `done`, og Story 2.3 står som `review` i sprint-status, med en kommentar om at Vercel-forhåndsvisningen gjenstår.
- Tre punkter fra Story 2.2 er løst i `issues.md`: `AGENTS.md`, telemetrien og 404-siden.

### Åpne punkter
- Fredrik må sette Framework Preset til «Services» med tom Root Directory på Vercel-prosjektet «g01-ervik-kristiansen». Så pushes grenen, og forhåndsvisningen sjekkes: `/`, `/api/anlegg?q=x` med JSON 501 og `/finnes-ikke` med den norske 404-siden. Når den virker, kobles prosjektet «backend» fra eller slettes. Story 2.3 er ikke ferdig før dette er gjort (AK 4).
- Vercels dokumentasjon sier at `modul:app` slås opp som en fil fra `backend/`, men koden ligger under `backend/src/`. Finner ikke Vercel appen, lages en liten fil i `backend/` som importerer den, og det føres i Implementation Notes.
- Story 2.4: `global-error.tsx` med norsk tekst og uten mørk modus.
- Senest Story 2.7: avgjør om sidene skal ha egne titler.
- Grenen er ikke pushet. Den har `670acbb`, `223f6de`, `9616518`, `dc99958` og denne loggen.
