# Story 2.2 frontend-skjelett marin

## 2026-11-26 kl. 10:41 — Fredrik Ervik

### Oppgave
Fredrik flettet PR #9 (Story 2.1) selv og ba meg sette Story 2.1 til `done` og begynne på Story 2.2, frontend-skjelett med designtokens, med `bmad-build`.

### Plan
- Laget grenen `story/2-2-frontend-skjelett-med-designtokens` fra `main` etter flettingen (`95605ea`). Satte Story 2.1 til `done` (`0378659`).
- Story 2.2 lager typene fra `openapi.json` fra Story 2.1. Derfor valgte Fredrik å flette PR #9 før grenen ble laget, i stedet for å bygge videre på grenen for 2.1.
- `bmad-build` steg 1–2:
  - `epic-2-context.md` var gyldig.
  - Leste Story 2.2 i `epics.md`, tokenene i DESIGN.md, AD-2, AD-6, AD-9 og Stack i arkitekturen, `review-versions.md` og `formatering.py` med `format.json`.
- Det første utkastet av specen var på omtrent 2 900 tokens. Fredrik valgte å dele den og godkjente med «Godkjenn og fortsett»:
  - Story 2.2 nå: Next-prosjektet, tokenene, rotlayouten og `tekster.ts`.
  - Utskilt til en egen spec i `deferred-work.md`: `schema.ts` med openapi-typescript, API-klienten og `format.ts` med Vitest.
- Mine valg i specen:
  - eksakte versjoner, også `postcss` 8.5.33 og `@types/node` 22.20.7
  - `@theme static` med `--*: initial`, så standardtemaet til Tailwind er borte
  - `rounded.DEFAULT` heter `--radius-default`
  - filene skrives for hånd, ikke med `create-next-app`
- Spec: [spec-2-2-frontend-skjelett-med-designtokens.md](../../_bmad-output/implementation-artifacts/spec-2-2-frontend-skjelett-med-designtokens.md), committet som `ready-for-dev` (`28aacd4`, baseline).

### Resultat
- En implementeringsagent som bare hadde specen, laget `frontend/`:
  - `package.json` og `package-lock.json`
  - `next.config.ts`, `tsconfig.json` og `postcss.config.mjs`
  - `globals.css` med 125 linjer i `@theme`
  - `layout.tsx` og to tomme sider
  - `tekster.ts`
  - seksjonen «Frontend» i README
- Jeg kontrollerte selv:
  - **Bygget:** `npm run build` lager `out/index.html` og `out/anlegg/index.html`, begge med `lang="nb"` og `<title>Marin</title>`.
  - **Tokenene:** et engangsskript fant alle 24 + 23 + 3 + 35 tokenene fra DESIGN.md, uten avvik, dubletter eller ekstra.
  - **Klassene:** et bygg med en midlertidig fil viste at `bg-accent` og `desktop:text-title` (under `min-width:600px`) gir CSS, mens `bg-blue-500`, `p-4`, `md:`, `text-sm` og `font-bold` ikke gjør det.
  - **Versjonene:** lockfila har nøyaktig versjonene i specen, og `npm install` endrer den ikke.
  - **Backend:** `uv run pytest` ga 540 bestått, og ingenting under `backend/` er endret.
- Review med Blind Hunter, Edge Case Hunter og Verification Gap ga 29 funn, ført i Review Triage Log i specen.
  - **Rettet (4):**
    - kommentaren om hva `--*: initial` stopper (klasser med egne verdier virker fortsatt)
    - kommentaren om `rounded`
    - `body` får tekstrollen `body` (16px/1,55 under 600px, 18px/1,55 fra 600px)
    - URL-en `/anlegg/?nr=…` i kommentaren i `next.config.ts`
  - **Utsatt (5, `deferred-work.md`):**
    - en test for at tokenene er like DESIGN.md
    - en sjekk for egne verdier under `src/`
    - skriftvekter og nullverdier i Story 2.4
    - `frontend/AGENTS.md`
    - telemetrien i Next
  - **Avvist (20).**
- Byggene jeg kjørte selv, hadde `NEXT_TELEMETRY_DISABLED=1`.
- Commit `cb19042`. Specen står som `done`, og Story 2.2 står som `review` i sprint-status. Ingenting er pushet.

### Åpne punkter
- Den utskilte delen av Story 2.2 trenger en egen spec: `schema.ts`, API-klienten og `format.ts` med Vitest, i tillegg til testen for tokenene og sjekken for egne verdier. Story 2.2 er ikke ferdig før den er bygget, og Story 2.4 og 2.7 trenger den. Fredrik må avgjøre om den skal bygges på samme gren før PR-en, eller få en egen nøkkel i sprint-status.
- Fredrik må avgjøre `frontend/AGENTS.md`: skal den committes, stoppes med `agentRules: false` eller stå i `.gitignore`?
- Fredrik må avgjøre om README skal be brukeren slå av telemetrien med `npx next telemetry disable`.
- Story 2.4: velg skriftvekter (`font-[600]` eller vekttokens) og nullverdier (`p-0`, `top-0`), som `--*: initial` har fjernet.
- Next sin standard 404-side (`out/404.html`) er på engelsk og blir svart i mørk modus. Den vises for ukjente stier når Story 2.3 serverer bygget. Avgjør om appen skal ha en egen norsk 404-side.
