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
- **Vercel:**
  - Fredrik satte Framework Preset til «Services». Jeg pushet grenen.
  - Det første bygget (`7156991`) feilet med `ENTRYPOINT_NOT_FOUND`, fordi Vercel lette etter `backend/marin/api/app.py`.
  - Fredrik logget inn med `npx vercel login`, så jeg kunne lese loggen med `vercel inspect --logs`.
  - Reserven fra specen løste det: `backend/vercel_inngang.py` legger `src/` i importstien og importerer appen, og `vercel.json` peker på `vercel_inngang:app`. To nye tester sjekker dette (`fdbd05b`, 44 bestått i API-testene).
  - Det andre bygget lyktes, og sjekken «Vercel – g01-ervik-kristiansen» består.
- **Forhåndsvisningen**, sjekket med `vercel curl`:
  - `/` og `/anlegg/?nr=1` gir 200 med `lang="nb"`.
  - `/api/anlegg?q=x` gir 501 med JSON, så `lifespan` har kjørt.
  - `/api/finnes-ikke` gir 404 med JSON.
  - `/finnes-ikke` gir 308 til `/finnes-ikke/` og deretter den norske 404-siden.
  - AK 4 er oppfylt. Resultatene står i Implementation Notes i specen.
- `vercel curl` la til en hemmelighet av typen «Protection Bypass for Automation» på Vercel-prosjektet uten å spørre. Jeg sa ikke fra om det på forhånd.
- Fredrik ba meg pushe og lage PR-en: [PR #11](https://github.com/IBE160-2026/G01-ervik-kristiansen/pull/11), med grenen fram til `ba00cf4`.

### Åpne punkter
- Koble fra eller slett Vercel-prosjektet «backend». Det feiler ved hver push.
- Avgjør om hemmeligheten «Protection Bypass for Automation» skal trekkes tilbake (Settings → Deployment Protection).
- Flett PR #11 når Fredrik ber om det. Produksjonsadressen virker først når grenen er flettet til `main`. Denne logglinjen er committet lokalt etter PR-en og ikke pushet.
- Story 2.4: `global-error.tsx` med norsk tekst og uten mørk modus.
- Senest Story 2.7: avgjør om sidene skal ha egne titler.

## 2026-11-27 kl. 10:30 — Fredrik Ervik

### Oppgave
Fredrik ba meg flette PR #11 og gå videre med resten av Story 2.2.

### Plan
- Flette PR #11 med en merge-commit, sjekke produksjonsadressen og sette Story 2.3 til `done` på neste gren, som før.

### Resultat
- PR #11 er flettet med `gh pr merge 11 --merge` (`0b68175`).
- Sjekken «Vercel – g01-ervik-kristiansen» består på `main`. «Vercel – backend» feiler fortsatt.
- Produksjonsadressen https://g01-ervik-kristiansen.vercel.app virker uten innlogging:
  - `/` og `/anlegg/?nr=1` gir 200 med `lang="nb"`.
  - `/api/anlegg?q=x` gir 501 med JSON, så datasettet er lastet.
  - `/api/finnes-ikke` gir 404 med JSON.
  - `/finnes-ikke/` gir 404 med den norske siden.
- Story 2.3 står som `done` i sprint-status (`a021f39`, på grenen `story/2-2b-api-klient-og-format`).

### Åpne punkter
- Koble fra eller slett Vercel-prosjektet «backend» (står i `issues.md`).
- Avgjør om hemmeligheten «Protection Bypass for Automation» skal trekkes tilbake (står i `issues.md`).
