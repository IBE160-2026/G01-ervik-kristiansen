---
title: 'Story 2.2 (resten): API-typer, API-klient og format.ts med Vitest'
type: 'feature'
created: '2026-11-27'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Story 2.2 mangler fortsatt fire ting fra `epics.md` og `deferred-work.md`: genererte API-typer, én vei til API-et, `formatLus` og `formatUke` testet mot kjernens vektorer, og sjekker som holder tokenene i takt med DESIGN.md. Story 2.4 og 2.7 trenger dem, og frontenden har ingen testløper ennå.

**Approach:** Vitest blir testløperen i `frontend/`. `npm run typer` lager `src/api/schema.ts` med openapi-typescript, og en test feiler når fila er utdatert. `src/api/` får API-basen, én hentehjelper og typenavnene, og `src/lib/format.ts` får de to funksjonene. To tester sjekker `@theme` mot DESIGN.md og at `src/` ikke har egne verdier.

## Boundaries & Constraints

**Always:**
- `openapi-typescript` 7.13.0 og `vitest` 5.1.0 står eksakt i `devDependencies`, og `package-lock.json` committes. Skriptene er `test` (`vitest run`) og `typer` (`openapi-typescript ../backend/openapi.json -o src/api/schema.ts`).
- `schema.ts` er bare utdata fra `npm run typer` og redigeres aldri for hånd.
- API-basen er `http://127.0.0.1:8000` når `process.env.NODE_ENV === 'development'`, ellers `''`.
- Hentehjelperen gir JSON-svaret ved 2xx. Ved andre statuser kaster den `ApiFeil` med `status` og `detail`: teksten når `detail` er en streng, ellers `null`. Nettverksfeil og avbrudd fra `AbortSignal` slipper uendret gjennom.
- `formatLus(verdi: number)` gir 2 desimaler med komma, og `formatUke(uke: Uke)` gir «uke 42, 2026». Begge testes mot `lus` og `uke` i `backend/tests/data/format.json`.
- Tokentesten bruker DESIGN.md som fasit og leser frontmatteren uten nye avhengigheter.
- Testene ligger i `frontend/tests/`, og testnavn og kommentarer er på norsk.

**Never:**
- Ingen kall per rute, komponenter eller sider (Story 2.4, 2.7 og 2.9), og ingen `formatGrense`.
- Ingen endring under `backend/`, i `globals.css` eller i DESIGN.md.
- Ingen andre nye avhengigheter (som en YAML-leser, jsdom eller ESLint), og ingen miljøvariabler.
- Ingen `fetch` utenfor `src/api/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Typer i takt | `openapi.json` er endret uten `npm run typer` | `npm test` feiler og ber om `npm run typer` | N/A |
| Svar 2xx i bygget | `hentJson('/api/anlegg?q=x')` | kaller `fetch('/api/anlegg?q=x')` og gir JSON-svaret | N/A |
| Svar i utvikling | samme kall med `NODE_ENV=development` | kaller `fetch('http://127.0.0.1:8000/api/anlegg?q=x')` | N/A |
| 404 | svaret er `{"detail": "Fant ikke anlegget."}` | — | `ApiFeil` med 404 og teksten |
| 422 eller 5xx | `detail` er en liste, eller kroppen er ikke JSON | — | `ApiFeil` med statusen og `detail: null` |
| Token avviker | en token i `@theme` har annen verdi, mangler, står to ganger eller er ekstra | `npm test` feiler og nevner tokenet | N/A |
| Egen verdi | en fil under `src/` har `#0B3D91`, `13px`, `Arial` eller `p-[13px]` | `npm test` feiler og nevner fila | N/A |

</frozen-after-approval>

## Code Map

- `frontend/package.json` -- versjonene fra Story 2.2, låst uten `^`, og skriptene `dev` og `build`.
- `frontend/tsconfig.json` -- `include` dekker `**/*.ts`, så `next build` typesjekker også `tests/`. Aliaset `@/*` virker ikke i Vitest uten konfigurasjon, så testene bruker relative importer.
- `backend/openapi.json` -- OpenAPI 3.1.0 med tre ruter og skjemaene `AnleggInfo`, `Anleggsvar`, `Arsak`, `Detaljsvar`, `EstimertUke`, `Farge`, `Graf`, `Grafpunkt`, `Kryssing`, `Status`, `Tabellrad` og `Uke`. Fila lages av `uv run python -m marin.api.openapi`.
- `backend/tests/test_api_app.py:99` -- mønsteret for testen av `schema.ts`: fila lages på nytt i en midlertidig mappe og sammenlignes med den committede, med `\r\n` gjort om til `\n`.
- `backend/src/marin/kjerne/formatering.py` -- `format_lus` og `format_uke`. `format_grense` og `format_uke_i_tekst` får ingen motpart i frontend.
- `backend/tests/data/format.json` -- vektorene. Nøkkelen `grense` brukes ikke i frontend.
- `_bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/DESIGN.md:11-189` -- frontmatteren med `colors`, `typography`, `rounded` og `spacing`. Verdiene står med eller uten enkle anførselstegn, og `#` etter en verdi starter en kommentar (fargene står i anførselstegn).
- `frontend/src/app/globals.css` -- `@theme static` med 124 variabler etter `--*: initial`. Se Design Notes.
- `frontend/src/app/not-found.tsx:15` -- eneste treff på mønstrene for egne verdier i `src/` i dag, i en kommentar.
- `README.md:32` -- seksjonen «Frontend».

## Tasks & Acceptance

**Execution:**
- [ ] `frontend/package.json` og `frontend/package-lock.json` -- de to avhengighetene og skriptene `test` og `typer`.
- [ ] `frontend/src/api/schema.ts` -- lages med `npm run typer`.
- [ ] `frontend/src/api/klient.ts` -- `apiBase()`, `ApiFeil` og `hentJson<T>(sti, signal?)`.
- [ ] `frontend/src/api/typer.ts` -- et typenavn per skjema i Code Map, fra `components['schemas']`.
- [ ] `frontend/src/lib/format.ts` -- `formatLus` og `formatUke`.
- [ ] `frontend/tests/` -- `schema.test.ts`, `klient.test.ts` (med `vi.stubGlobal('fetch', …)` og `vi.stubEnv`), `format.test.ts`, `tokens.test.ts` og `egne-verdier.test.ts`, som til sammen dekker matrisen.
- [ ] `frontend/src/app/not-found.tsx` -- kommentaren på linje 15 bruker tokennavnene `target-min` og `target-min-inline` i stedet for «44px» og «24px», ellers feiler sjekken for egne verdier.
- [ ] `README.md` -- `npm test`, og at `npm run typer` kjøres etter `uv run python -m marin.api.openapi`.

**Acceptance Criteria:**
- Gitt `npm install` i `frontend/`, når `npm test` kjører, så består alle testene, og ingen test består fordi vektorene eller tokenlistene er tomme.
- Gitt `npm run build`, når bygget kjører, så lykkes det med testene med i typesjekken, og `out/` får ingen ny side.
- Gitt `uv run pytest` i `backend/`, når testene kjører, så består alle, og ingenting under `backend/` er endret mot baseline.
- Gitt en midlertidig feil i hver av tokenene, en fil under `src/` og `openapi.json`, når `npm test` kjører, så feiler riktig test. Feilene fjernes etterpå.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

**Tokentesten** regner ut hvilke variabler `@theme` skal ha fra frontmatteren, og sammenligner navn og verdier eksakt:
- `colors.x` blir `--color-x`, og `spacing.x` blir `--spacing-x`.
- `rounded` blir `--radius-sm`, `--radius-default` og `--radius-full`.
- `typography.r` blir `--text-r` (`fontSize`), og `--text-r--font-weight`, `--text-r--letter-spacing` og `--text-r--line-height` når rollen har dem.
- Alle rollene har samme `fontFamily`, og den blir `--font-sans`. Testen sjekker at den er lik i alle rollene.
- I tillegg kommer `--breakpoint-desktop: 600px` som eneste `--breakpoint-*`, og `--*: initial` står først.

**Sjekken for egne verdier** leser alle `.ts`-, `.tsx`- og `.css`-filer under `src/` unntatt `app/globals.css` og `api/schema.ts`. Kommentarer sjekkes også, så de skal bruke tokennavn. Den finner:
- fargekoder (`#0B3D91`, `rgb(`, `hsl(`, `oklch(`)
- pikselverdier (`13px`)
- fontnavn fra fontstabelen og `font-family`
- klasser med egne verdier i hakeparentes (`p-[13px]`, `min-[700px]:`)

Lista `TILLATT` i testen er tom. Velger Story 2.4 `font-[600]` framfor egne vekttokens, legges klassen inn der (`deferred-work.md`).

**Testen av `schema.ts`** kjører samme kommando som `npm run typer`, med `process.execPath` og `openapi-typescript/bin/cli.js` uten skall, til en midlertidig fil.

```ts
export class ApiFeil extends Error {
  constructor(readonly status: number, readonly detail: string | null) {
    super(detail ?? `API-et svarte ${status}`);
  }
}
export async function hentJson<T>(sti: string, signal?: AbortSignal): Promise<T>
```

## Verification

**Commands (i `frontend/`):**
- `npm install` -- expected: ingen `ERESOLVE`
- `npm test` -- expected: alle testene består
- `npm run build` -- expected: lykkes
- `uv run pytest` i `backend/` -- expected: alle består
- `git diff --stat {baseline} -- backend` -- expected: tom
