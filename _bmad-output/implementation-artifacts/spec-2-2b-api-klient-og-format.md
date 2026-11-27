---
title: 'Story 2.2 (resten): API-typer, API-klient og format.ts med Vitest'
type: 'feature'
created: '2026-11-27'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'b061069eb6caa628db06ff7d18ab769a84137361'
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
- [x] `frontend/package.json` og `frontend/package-lock.json` -- de to avhengighetene og skriptene `test` og `typer`.
- [x] `frontend/src/api/schema.ts` -- lages med `npm run typer`.
- [x] `frontend/src/api/klient.ts` -- `apiBase()`, `ApiFeil` og `hentJson<T>(sti, signal?)`.
- [x] `frontend/src/api/typer.ts` -- et typenavn per skjema i Code Map, fra `components['schemas']`.
- [x] `frontend/src/lib/format.ts` -- `formatLus` og `formatUke`.
- [x] `frontend/tests/` -- `schema.test.ts`, `klient.test.ts` (med `vi.stubGlobal('fetch', …)` og `vi.stubEnv`), `format.test.ts`, `tokens.test.ts` og `egne-verdier.test.ts`, som til sammen dekker matrisen.
- [x] `frontend/src/app/not-found.tsx` -- kommentaren på linje 15 bruker tokennavnene `target-min` og `target-min-inline` i stedet for «44px» og «24px», ellers feiler sjekken for egne verdier.
- [x] `README.md` -- `npm test`, og at `npm run typer` kjøres etter `uv run python -m marin.api.openapi`.

**Acceptance Criteria:**
- Gitt `npm install` i `frontend/`, når `npm test` kjører, så består alle testene, og ingen test består fordi vektorene eller tokenlistene er tomme.
- Gitt `npm run build`, når bygget kjører, så lykkes det med testene med i typesjekken, og `out/` får ingen ny side.
- Gitt `uv run pytest` i `backend/`, når testene kjører, så består alle, og ingenting under `backend/` er endret mot baseline.
- Gitt en midlertidig feil i hver av tokenene, en fil under `src/` og `openapi.json`, når `npm test` kjører, så feiler riktig test. Feilene fjernes etterpå.

## Implementation Notes

- **Lockfila:**
  - Vitest 5.1.0 krever Vite, så npm installerte Vite 8.4.0 av seg selv. Vite står bare i `package-lock.json`, fordi specen forbyr andre nye avhengigheter i `package.json`.
  - Et skript som sammenlignet `packages` før og etter, fant 72 nye oppføringer, alle `dev`, og ingen endrede eller fjernede. De 195 slettede linjene i diffen kommer av at oppføringer har flyttet seg.
- **`klient.ts`:**
  - `ApiFeil` setter `name` til `'ApiFeil'`.
  - `detail` blir `null` bare når kroppen ikke er JSON (`SyntaxError`). Avbrudd og nettverksfeil slipper gjennom også når de kommer mens feilsvaret leses.
- **`formatLus`** skriver aldri «-0,00», på samme måte som kjernen.
- **Tokentesten:**
  - Leseren støtter bare formene DESIGN.md bruker. Andre former, som doble anførselstegn eller lister i en tokenseksjon, gir en feil med linjenummer.
  - Testfila har egne tester av leseren og sammenligningen, så en ødelagt sjekk ikke kan bestå uten å si fra.
- **Sjekken for egne verdier:**
  - Treffet er hele klassen, for eksempel `font-[600]`, også med variant (`desktop:font-[600]`). Derfor kan en klasse i `TILLATT` dekke alle variantene.
  - Fontnavnene leses fra `--font-sans` i `globals.css`.
- **Verifisert:**
  - `npm test` gir 72 bestått i 5 filer. Alle radene i matrisen har en test som kjørte.
  - `npm run build` lykkes, og `out/` har de samme sidene som før (`/`, `/anlegg/` og 404). Implementeringen la inn en midlertidig typefeil i `tests/` og så at bygget feilet, så testene er med i typesjekken.
  - `uv run pytest` i `backend/` gir 561 bestått, og `git diff --stat b061069 -- backend` er tom.
  - Implementeringen la inn 264 midlertidige feil med et skript:
    - hver variabel i `@theme` med endret verdi, og slettet
    - en dublett, to ekstra tokens og `--*: initial` flyttet
    - åtte egne verdier i `src/app/page.tsx` og en ny `.css`-fil
    - en endring i `openapi.json`

    Alle feilet i riktig test og nevnte tokenet eller fila. Etterpå var alle filene tilbake som før.
  - Stikkprøve i steg 3: `13px` og `#0B3D91` i en kommentar i `page.tsx` ga `src/app/page.tsx:5: #0B3D91` og `src/app/page.tsx:5: 13px`.
- **Etter reviewen** (patchene i Review Triage Log):
  - Sjekken for egne verdier finner også:
    - `/[…]`, `rem` og `em`
    - `lab(`, `lch(`, `hwb(`, `color(` og `color-mix(`
    - breddeklasser med tall, som `border-2` og `stroke-2`
    - `[…]` med `:` eller `&`

    Den leser også `.js`, `.jsx`, `.mjs` og `.svg`, og godtar `&#160;`. En ny test sjekker at bare filer under `api/` kaller `fetch`.
  - Tokentesten sjekker at hodet er `@theme static`, og har tester for feilgrenene i begge leserne.
  - `schema.test.ts` sjekker at `scripts.typer` er kommandoen testen kjører. `klient.test.ts` setter `NODE_ENV` til `test` før hver test.
  - `vitest.config.mts` har aliaset `@` → `src/`, og `format.test.ts` importerer fra `@/lib/format`.
    - Fila heter `.mts` fordi Vite advarte om ESM i en fil som lastes som CommonJS, når den het `vitest.config.ts` og `package.json` ikke har `"type": "module"`.
    - `tsconfig.json` har fått `**/*.mts` i `include`, så `next build` fortsatt typesjekker den.
  - `npm test` gir 105 bestått uten advarsler, og `npm run build` lykkes.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Blind Hunter | Sjekken for egne verdier slipper gjennom `bg-accent/[0.37]`, `1rem`, tall i `style`, navngitte farger, `lab(` og lignende, og filer som ikke er `.ts`, `.tsx` eller `.css` | low | patch (delvis) | Bekreftet. Rettes: `/[…]`, `rem` og `em`, fargefunksjonene og filtypene. Avvist: navngitte farger, fordi lista er lang og gir falske treff i kode, og tall i `style`, fordi det krever tolking av koden og SVG-koordinater er vanlige tall. |
| 2 | Blind Hunter | Falske treff: `PR #123`, `#add` og `[navn:string]` | low | patch (delvis) | Rettes sammen med 31: `#` rett etter `&` (HTML-entiteter som `&#160;`) godtas. Avvist: `PR #123`, fordi PR-numrene har to sifre fram til fristen, `#add`, fordi ankere i appen har norske navn, og `[navn:string]` uten mellomrom, som er uvanlig. |
| 3 | Blind Hunter | Hele `globals.css` er unntatt, også `@layer base` | low | avvist | Bekreftet, men unntaket står i Design Notes og i `deferred-work.md`. `2px` i fokusmarkeringen kommer fra `focus-ring` i DESIGN.md. Fiksen krever enten en endring i `globals.css`, som specen forbyr, eller at `2px` tillates overalt. |
| 4 | Blind Hunter | Ingenting sjekker at `fetch` bare brukes i `src/api/` | low | patch | Bekreftet. En test som bruker samme filliste som sjekken for egne verdier, er en liten tilføyelse og holder akseptkriteriet i `epics.md` (AD-3). |
| 5 | Blind Hunter | `typer.ts` holdes ikke i takt med `schema.ts`, og `kilde` har ikke eget typenavn | low | avvist | Et nytt skjema uten typenavn gir en kompileringsfeil så snart en komponent importerer det, så ingen får feil type. Typenavnet for `kilde` kan lages når Epic 3 trenger det. |
| 6 | Blind Hunter | `schema.test.ts` gjentar argumentene i stedet for å lese `scripts.typer` | low | patch | Bekreftet. Én sjekk av at `scripts.typer` er nøyaktig kommandoen testen kjører. |
| 7 | Blind Hunter | `@/` virker ikke i Vitest, og `format.ts` importerer med `@/` | low | patch | Bekreftet med en midlertidig test: `import { tekster } from '@/tekster'` ga «Cannot find package '@/tekster'». `format.ts` virker bare fordi importen er `import type`. Fiksen er `vitest.config.ts` med et alias, uten nye avhengigheter. |
| 8 | Blind Hunter | `hentJson` kaster `SyntaxError` ved 2xx uten JSON, og avbrudd mens et 2xx-svar leses er ikke testet | low | avvist | API-et svarer alltid med JSON ved 2xx (FastAPI-modellene). En `SyntaxError` er ikke et avbrudd, så kalleren viser den generelle meldingen. Fiksen legger til en ny gren. |
| 9 | Blind Hunter | `formatLus` runder ikke som backend ved mer enn 2 desimaler | low | avvist | Bekreftet for `1.005`. Lusetallene i tabellen og grafen har høyst 2 desimaler (`modeller.py:62` runder tellingene), og forutsetningen står i docstringen. Trendverdiene lages først i Story 2.5. Avrunding som er lik `ROUND_HALF_UP` for flyttall, er mer enn en direkte rettelse. |
| 10 | Blind Hunter | Feilgrenene i leseren av frontmatteren og hele `lesTheme` er ikke testet | low | patch | Bekreftet: bare doble anførselstegn og en liste er testet. Tester for dublett, tekst etter anførselstegnet, manglende anførselstegn, to `@theme`-blokker og en deklarasjon uten kolon er små tilføyelser. |
| 11 | Blind Hunter | Tokentesten sjekker ikke at blokka er `@theme static` | low | patch | Bekreftet: mønsteret godtar `@theme` uten `static`. Uten `static` forsvinner variabler som ingen klasse bruker, som SVG-fargene i Story 2.8. |
| 12 | Blind Hunter | `package-lock.json` er ikke med i diffen | false | avvist | Lockfila ble holdt utenfor review-diffen med vilje, fordi den er generert. Et skript sammenlignet `packages` før og etter: 72 nye oppføringer, alle `dev`, og ingen endret eller fjernet (Implementation Notes). |
| 13 | Blind Hunter | `engines` er `>=22.12`, men Vitest krever `^22.12.0 \|\| ^24.0.0 \|\| >=26.0.0` | low | avvist | Node 23 og 25 er versjoner uten langtidsstøtte og har nådd EOL. `engines` gir bare en advarsel, og verdien ble bestemt i Story 2.2. |
| 14 | Blind Hunter | CORS-kommentaren i `apiBase()` er upresis | low | patch | Bekreftet: backend tillater bare `http://localhost:3000`, og kommentaren får det eksakte opphavet. At `127.0.0.1:3000` og port 3001 ikke virker i utvikling, kommer fra CORS-regelen i Story 2.1. README ber leseren åpne `http://localhost:3000`. |
| 15 | Blind Hunter | 404 står ikke i `openapi.json` eller `schema.ts` | low | avvist | Punktet står allerede i `issues.md` for Story 2.5 (funn 3 i spec-2-1), og backend kan ikke endres i denne storyen. |
| 16 | Blind Hunter | `medLf` står i to testfiler | low | avvist | Hjelperen er to linjer. En felles hjelpefil gir en fil til uten at noe blir sikrere. |
| 17 | Verification Gap | `schema.ts` sjekkes bare av `npm test`, og ingenting kjører den automatisk | medium | defer | Kommer ferdig verifisert. Repoet har ingen CI, og Vercel kjører ingen tester. README ber om `npm run typer` etter `marin.api.openapi`. Å lukke gapet krever CI eller ett felles verifiseringssteg (`deferred-work.md`). |
| 18 | Edge Case | 2xx med tom kropp eller uten JSON | low | avvist | Samme som 8. |
| 19 | Edge Case | `detail` er en tom streng | low | avvist | `detail` kommer fra backendkoden, som aldri sender tom tekst. Fiksen legger til en gren. |
| 20 | Edge Case | `sti` uten skråstrek først, eller en hel adresse | low | avvist | Stiene står fast i kallene per rute (Story 2.4, 2.7 og 2.9), og en feil sti feiler med en gang i utvikling. Fiksen legger til en sjekk. |
| 21 | Edge Case | Siden åpnet på `127.0.0.1:3000` eller port 3001 gir CORS-feil | low | patch | Samme som 14. |
| 22 | Edge Case | `hentJson` på serveren under prerendering | low | avvist | Sidene henter i nettleseren etter `useSearchParams` (epic-konteksten). Et kall under `next build` feiler med en tydelig feil, og det er riktig. |
| 23 | Edge Case | `formatLus` med mer enn 2 desimaler | low | avvist | Samme som 9. |
| 24 | Edge Case | `formatLus` med `NaN`, `Infinity` eller `1e21` | false | avvist | JSON kan ikke ha `NaN` eller `Infinity`, og API-et sender bare lusetall. |
| 25 | Edge Case | Et nytt skjema uten typenavn | low | avvist | Samme som 5. |
| 26 | Edge Case | Filer under `src/` med andre endelser leses ikke | low | patch | Bekreftet: bare `.ts`, `.tsx` og `.css` leses. Rettes sammen med 1, med `.js`, `.jsx`, `.mjs` og `.svg`. |
| 27 | Edge Case | Egne verdier i `globals.css` utenfor `@theme` | low | avvist | Samme som 3. |
| 28 | Edge Case | Navngitte farger, og `lab(`, `lch(`, `hwb(`, `color(` og `color-mix(` | low | patch (delvis) | Fargefunksjonene rettes sammen med 1. Navngitte farger avvises, som i 1. TrendGraf (Story 2.8) skal bruke `var(--color-…)`. |
| 29 | Edge Case | `border-2` og lignende klasser, og tall i `style` | low | patch (delvis) | Bekreftet ved kompilering med `--*: initial`: `outline-offset-2` og `underline-offset-2` gir `2px`, og `stroke-2` gir `stroke-width: 2`. Bredder som tall rettes sammen med 1. Velger Story 2.4 slike klasser, legges de i `TILLATT`. Tall i `style` avvises, som i 1. |
| 30 | Edge Case | `[--gap:1rem]`, `[@supports(…)]:`, `[.dark_&]:` og `p-(--x)` | low | patch (delvis) | Bekreftet for hakeparentesene, som rettes sammen med 1 med ett mønster for `[…]` uten mellomrom som har `:` eller `&`. `p-(--x)` avvises: klassen viser til en CSS-variabel, og den kan være et token. |
| 31 | Edge Case | Falske treff for `#123`, `&#8203;` og `#add` | low | patch (delvis) | Samme som 2. |
| 32 | Edge Case | `font:` som kortform, `FONT-FAMILY` og `--font-sans` i en kommentar | low | avvist | Det finnes ingen andre CSS-filer enn `globals.css`, og komponentene bruker Tailwind-klasser. `font: 16px …` fanges av mønsteret for `px`. |
| 33 | Edge Case | Testene feiler med `NODE_ENV=development` i skallet | low | patch | Bekreftet: Vitest gjør `process.env.NODE_ENV ??= "test"`, så «sender signalet videre til fetch» feiler da. Fiksen er én `beforeEach` med `vi.stubEnv('NODE_ENV', 'test')`. |
| 34 | Edge Case | En test som kjøres på nytt, bruker samme `Response` | false | avvist | Vitest er ikke satt opp med `retry` eller `repeats`, og hver rad i `it.each` kjøres én gang. |
| 35 | Edge Case | Leseren godtar feil innrykk, så et token havner under feil forelder | low | avvist | Et token under feil forelder får et annet variabelnavn, og da feiler sammenligningen med «mangler» eller «står i @theme, men ikke i DESIGN.md». Testen blir ikke grønn. Fiksen legger til flere grener. |
| 36 | Edge Case | Stien til `openapi-typescript/bin/cli.js` kan flytte seg | false | avvist | `openapi-typescript` er en direkte dev-avhengighet, så npm legger den øverst i `node_modules`, og versjonen er låst eksakt. |
| 37 | Edge Case | Matrisen sier «en fil under `src/`», men `globals.css` og andre filtyper leses ikke | low | patch (delvis) | Filtypene rettes (26). Unntaket for `globals.css` står i Design Notes og i `deferred-work.md` (3). |

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
