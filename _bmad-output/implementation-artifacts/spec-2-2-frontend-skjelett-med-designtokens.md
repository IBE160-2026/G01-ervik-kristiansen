---
title: 'Story 2.2: Frontend-skjelett med designtokens'
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

**Problem:** Det finnes ingen frontend ennå. Sidene i Story 2.4 og 2.7–2.10 trenger et Next.js-prosjekt med de samme tokenene og faste tekstene, og Story 2.3 trenger et statisk bygg å servere (AD-9).

**Approach:** `frontend/` får et lite Next.js-prosjekt med statisk eksport og to tomme sider, `/` og `/anlegg/`. Tokenene fra DESIGN.md står én gang i Tailwind `@theme`, og rotlayouten har språk, font, lenker og fokusmarkering. API-typene, API-klienten og `format.ts` med Vitest er skilt ut i en egen spec (`deferred-work.md`).

## Boundaries & Constraints

**Always:**
- Versjonene står eksakt (uten `^`) i `package.json`, og `package-lock.json` committes:
  - `next` 16.4.6, `react` og `react-dom` 19.3.1, `typescript` 5.9.3
  - `tailwindcss` og `@tailwindcss/postcss` 4.3.5, og `postcss` 8.5.33
  - `@types/react` og `@types/react-dom` 19.3.0, og `@types/node` 22.20.7
  
  `engines` er `"node": ">=22.12"`.
- `next.config.ts` har `output: 'export'` og `trailingSlash: true`. `npm run build` lager `out/index.html` og `out/anlegg/index.html`.
- `src/app/globals.css` har `@theme static`, som starter med `--*: initial`. Deretter står alle tokenene i frontmatteren til DESIGN.md én gang, med samme navn og verdi:
  - 24 farger
  - 23 typografiroller, også mobilvariantene
  - 3 `rounded`
  - 35 `spacing`
  
  Det eneste bruddpunktet er `desktop` på 600px. Alle rollene har samme fontstabel, så den står én gang som `--font-sans`.
- Rotlayouten har `<html lang="nb">`, systemfonten, `ink` på `surface` og bare lys modus. Lenker er i `accent` og understreket. Alle interaktive elementer får `:focus-visible` med 2px heltrukket `accent` og 2px avstand (DESIGN.md `link` og `focus-ring`).
- Faste tekster ligger bare i `src/tekster.ts`. I denne storyen er det bare appnavnet «Marin», som brukes i `<title>`.

**Never:**
- Ingen `schema.ts`, API-klient, `format.ts`, Vitest eller openapi-typescript (den utskilte specen).
- Ingen toppfelt, søk, forsideinnhold, detaljside, graf, `useSearchParams` eller `<Suspense>` (Story 2.4 og 2.7–2.10).
- Ingen montering av `out/` i FastAPI og ingen `vercel.json` (Story 2.3). Ingen endring under `backend/`.
- Ingen route handlers, server actions, `middleware`/`proxy`, `rewrites`, dynamiske ruter, `next/font` eller bilder.
- Ingen `create-next-app`, ESLint, Prettier eller andre verktøy utenfor stacken. Ingen miljøvariabler.
- Ingen farger, pikselverdier eller fonter i komponentene utenfor tokenene, og ingen mørk modus.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Bygg | `npm install` og `npm run build` i `frontend/` | `out/index.html` og `out/anlegg/index.html` med `<html lang="nb">` og `<title>Marin</title>` | N/A |
| Token | en komponent bruker `bg-accent`, `text-title-mobile desktop:text-title` eller `px-page-x` | klassene gir CSS med verdiene fra DESIGN.md | N/A |
| Standardtema | en komponent bruker `bg-blue-500`, `p-4` eller `md:` | ingen CSS lages, fordi bare tokenene finnes | N/A |

</frozen-after-approval>

## Code Map

- `_bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/DESIGN.md:11-189` -- tokenene i frontmatteren. Linje 367–371 har `link` og `focus-ring`, og linje 414–460 har tabellene for desktop og mobil.
- `_bmad-output/planning-artifacts/architecture/architecture-Marin-2026-11-16/reviews/review-versions.md` -- begrunner versjonene:
  - F1: TypeScript 5.9.3
  - F4: avhengighetene som mangler i Stack
  - F5: Node-gulvet
  - F9: `@theme static`
  
  I Next 16 heter middleware `proxy`, og `next lint` finnes ikke lenger.
- `.gitignore` -- dekker allerede `node_modules/`, `.next/`, `out/`, `next-env.d.ts` og `*.tsbuildinfo`.
- `README.md` -- seksjonen «API-et» (linje 19). Seksjonen «Frontend» legges etter den.

## Tasks & Acceptance

**Execution:**
- [ ] `frontend/package.json` og `frontend/package-lock.json` -- avhengighetene etter Boundaries, og skriptene `dev` og `build`.
- [ ] `frontend/next.config.ts`, `frontend/tsconfig.json` og `frontend/postcss.config.mjs` -- statisk eksport, streng TypeScript og `@tailwindcss/postcss`.
- [ ] `frontend/src/app/globals.css` -- `@theme static` med tokenene, og grunnreglene for body, lenker og fokus.
- [ ] `frontend/src/app/layout.tsx`, `frontend/src/app/page.tsx` og `frontend/src/app/anlegg/page.tsx` -- rotlayouten og to tomme sider med en `<main>`.
- [ ] `frontend/src/tekster.ts` -- de faste tekstene.
- [ ] `README.md` -- seksjonen «Frontend»: Node ≥ 22.12, `npm install`, `npm run dev` (port 3000, åpne `http://localhost:3000`) og `npm run build`.

**Acceptance Criteria:**
- Gitt `npm install` og `npm run build` i `frontend/`, når bygget kjører, så lykkes det uten konflikter i avhengighetene.
- Gitt `uv run pytest` i `backend/`, når testene kjører, så består alle 540, og ingen filer under `backend/` er endret mot baseline.
- Gitt `globals.css` og DESIGN.md, når tokenene sammenlignes, så står hvert token én gang med samme verdi. Ingen fil under `src/` utenfor `globals.css` har fargekoder, pikselverdier eller fontnavn.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Tailwind v4 lager utility-klasser av navnene i `@theme`. Mobilrollene er egne tokens, og komponentene skriver mobil først: `text-title-mobile desktop:text-title`. Et utsnitt:

```css
@theme static {
  --*: initial;
  --breakpoint-desktop: 600px;
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --color-accent: #0B3D91;
  --text-title: 34px;
  --text-title--font-weight: 600;
  --text-title--letter-spacing: -0.01em;
  --radius-default: 6px;
  --spacing-page-x: 32px;
}
```

- **`--*: initial`:** fjerner standardtemaet, så komponentene ikke kan bruke farger, størrelser, avstander eller bruddpunkter som ikke er tokens.
- **`static`:** gjør at alle variablene finnes i CSS-en, også de som ingen klasse bruker. `TrendGraf` (Story 2.8) trenger det for SVG-farger.
- **`rounded.DEFAULT`:** blir `--radius-default`, fordi `rounded` uten navn ikke peker på et token i v4.

## Verification

**Commands (i `frontend/`):**
- `npm install` -- expected: ingen `ERESOLVE`
- `npm run build` -- expected: lykkes, og `out/index.html` og `out/anlegg/index.html` finnes
- `uv run pytest` i `backend/` -- expected: 540 bestått

**Manual checks:**
- Sammenlign `@theme` med frontmatteren i DESIGN.md (24 + 23 + 3 + 35 tokens), for eksempel med et engangsskript.
- Se i den bygde CSS-en at `bg-accent` og `desktop:text-title` gir regler, og at `bg-blue-500` og `p-4` ikke gjør det.
- `npm run dev`, og åpne `/` og `/anlegg/`: `lang="nb"`, systemfont og hvit bakgrunn. CSS-en har regelen for `:focus-visible`.
