# Story 2.2b API-klient og format marin

## 2026-11-27 kl. 10:30 — Fredrik Ervik

### Oppgave
Fredrik ba meg bygge resten av Story 2.2 med `bmad-build`: API-typene i `schema.ts`, API-klienten og `format.ts` med Vitest, testen for tokenene og sjekken for egne verdier. Arbeidet går på grenen `story/2-2b-api-klient-og-format`, under samme nøkkel i sprint-status. Story 2.4 og 2.7 trenger dette.

### Plan
- **Steg 1:**
  - `epic-2-context.md` var gyldig.
  - Intensjonen kom fra tre punkter i `deferred-work.md` og akseptkriteriene for Story 2.2 i `epics.md`.
  - Repoet har en egen, nyere kopi av `bmad-build` (29.10), og den ble brukt.
- **Steg 2:**
  - Undersøkte `openapi.json`, `formatering.py`, `format.json`, frontmatteren i DESIGN.md og `globals.css`.
  - openapi-typescript 7.13.0 og Vitest 5.1.0 finnes på npm.
  - Kommentaren i `not-found.tsx` hadde «44px» og «24px» og måtte endres, ellers ville sjekken for egne verdier feile.
  - Ingen åpne spørsmål.
- **Fredriks valg:**
  - Specen ble holdt samlet, selv om den var på omtrent 2 400 tokens.
  - «Godkjenn og fortsett».
- **Spec:** [spec-2-2b-api-klient-og-format.md](../../_bmad-output/implementation-artifacts/spec-2-2b-api-klient-og-format.md), committet som `ready-for-dev` (`b061069`, baseline).

### Resultat
- **Implementeringen**, gjort av en agent som bare hadde specen:
  - `openapi-typescript` 7.13.0 og `vitest` 5.1.0 er låst eksakt, med skriptene `test` og `typer`. Vite 8.4.0 kom med av seg selv og står bare i lockfila.
  - `src/api/schema.ts` lages med `npm run typer`. `src/api/klient.ts` har `apiBase()`, `ApiFeil` og `hentJson`, og `src/api/typer.ts` har 12 typenavn.
  - `src/lib/format.ts` har `formatLus` og `formatUke`.
  - Fem testfiler i `frontend/tests/`.
  - README har `npm test` og `npm run typer`.
- **Verifisert:**
  - `npm test` gir 72 bestått. `npm run build` lykkes, og testene er med i typesjekken.
  - `uv run pytest` gir 561 bestått, og `backend/` er uendret.
  - Implementeringen la inn 264 midlertidige feil, og alle feilet i riktig test. Jeg tok i tillegg en stikkprøve i `page.tsx`.
  - Lockfila har 72 nye oppføringer, alle `dev`, og ingen eksisterende er endret (sjekket med et skript).
- **Review** med Blind Hunter, Edge Case Hunter og Verification Gap ga 37 funn, ført i Review Triage Log:
  - **Rettet (16), helt eller delvis:**
    - Sjekken for egne verdier finner også `/[…]`, `rem` og `em`, flere fargefunksjoner, breddeklasser som `border-2` og `[…]` med `:` eller `&`. Den leser også `.js`, `.jsx`, `.mjs` og `.svg`, og godtar `&#160;`.
    - En ny test sjekker at `fetch` bare brukes i `src/api/`.
    - Tokentesten sjekker `@theme static` og feilgrenene i begge leserne.
    - `schema.test.ts` sjekker `scripts.typer`.
    - `klient.test.ts` tåler `NODE_ENV=development`.
    - `vitest.config.mts` har aliaset `@` → `src/`.
    - CORS-kommentaren nevner `http://localhost:3000`.
  - **Utsatt (1, `deferred-work.md`):** ingen CI kjører `npm test`, så en utdatert `schema.ts` kan nå `main`.
  - **Avvist (20)**, blant dem:
    - `SyntaxError` ved 2xx uten JSON
    - avrunding i `formatLus` ved mer enn 2 desimaler
    - navngitte farger
    - unntaket for hele `globals.css`
- Etter rettelsene ga Vite en advarsel om ESM i `vitest.config.ts`. Jeg ga fila navnet `vitest.config.mts` og la `**/*.mts` til i `tsconfig.json`. Etterpå gir `npm test` 105 bestått uten advarsler, `npm run build` lykkes og `uv run pytest` gir 561 bestått.
- Commit `cb64dd5`. Specen står som `done`, og Story 2.2 står som `review` i sprint-status.
- Punktet om den utskilte delen av Story 2.2 er løst i `issues.md`.
- Fredrik ba meg pushe grenen og lage PR-en: [PR #12](https://github.com/IBE160-2026/G01-ervik-kristiansen/pull/12).
- Fredrik valgte å beholde hemmeligheten «Protection Bypass for Automation» til etter innleveringen 15.12.2026, så jeg kan sjekke forhåndsvisningene med `vercel curl`.
- Fredrik ba meg slette Vercel-prosjektet «backend». Jeg sjekket først at det var det gamle prosjektet fra 19.11 (Root Directory `backend`, Python), at ingenting i repoet viste til det, og at ingen lokal mappe var koblet til det. Så slettet jeg det med `vercel project delete backend --confirm-name backend`. Bare «g01-ervik-kristiansen» er igjen. Sjekken «Vercel – backend» feilet på PR-commiten fordi pushen kom før slettingen. Punktet er løst i `issues.md`.

### Åpne punkter
- Story 2.4: breddeklasser med tall (`border-2`, `outline-offset-2`) og klasser som `font-[600]` feiler nå sjekken for egne verdier. Legg dem i `TILLATT` i `frontend/tests/egne-verdier.test.ts`, eller lag tokens.
- Ingen CI kjører `npm test`. Kjør `npm test` i `frontend/` før hver PR, særlig når `openapi.json` er endret (`deferred-work.md`).
- Story 2.5: rund trendverdiene i `Grafpunkt` til 2 desimaler i API-et hvis frontend skal skrive dem med `formatLus`. Funksjonen bruker `toFixed` og runder ikke som `ROUND_HALF_UP` ved flere desimaler.
- Trekk tilbake hemmeligheten «Protection Bypass for Automation» etter innleveringen 15.12.2026.
- Beskrivelsen i `backend/tests/data/format.json` nevner `formatGrense` i frontend, men den funksjonen ble ikke laget. Rett beskrivelsen i en story som får endre backend.
