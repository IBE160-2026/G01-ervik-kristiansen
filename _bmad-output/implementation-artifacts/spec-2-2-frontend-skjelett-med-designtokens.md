---
title: 'Story 2.2: Frontend-skjelett med designtokens'
type: 'feature'
created: '2026-11-26'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: '28aacd4d641b91a8a4dbdda9d17eedcb16fbbf82'
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
- [x] `frontend/package.json` og `frontend/package-lock.json` -- avhengighetene etter Boundaries, og skriptene `dev` og `build`.
- [x] `frontend/next.config.ts`, `frontend/tsconfig.json` og `frontend/postcss.config.mjs` -- statisk eksport, streng TypeScript og `@tailwindcss/postcss`.
- [x] `frontend/src/app/globals.css` -- `@theme static` med tokenene, og grunnreglene for body, lenker og fokus.
- [x] `frontend/src/app/layout.tsx`, `frontend/src/app/page.tsx` og `frontend/src/app/anlegg/page.tsx` -- rotlayouten og to tomme sider med en `<main>`.
- [x] `frontend/src/tekster.ts` -- de faste tekstene.
- [x] `README.md` -- seksjonen «Frontend»: Node ≥ 22.12, `npm install`, `npm run dev` (port 3000, åpne `http://localhost:3000`) og `npm run build`.

**Acceptance Criteria:**
- Gitt `npm install` og `npm run build` i `frontend/`, når bygget kjører, så lykkes det uten konflikter i avhengighetene.
- Gitt `uv run pytest` i `backend/`, når testene kjører, så består alle 540, og ingen filer under `backend/` er endret mot baseline.
- Gitt `globals.css` og DESIGN.md, når tokenene sammenlignes, så står hvert token én gang med samme verdi. Ingen fil under `src/` utenfor `globals.css` har fargekoder, pikselverdier eller fontnavn.

## Implementation Notes

- Filene er skrevet for hånd. `tsconfig.json` har `strict`, `noUncheckedIndexedAccess` og aliaset `@/*` → `src/*`. `next build` endret den ikke.
- `globals.css` har `color-scheme: light` på `html` i tillegg til grunnreglene, så nettleseren ikke tegner skjemaelementer i mørk modus.
- Typografirollene er `--text-<rolle>` med `--font-weight`, `--letter-spacing` og `--line-height` der DESIGN.md har dem. Det gir 125 variabler i `@theme`.
- Matrisen har ingen automatiske tester. Denne delen av specen har ingen testløper, fordi Vitest kom med i den utskilte specen. Radene er sjekket slik:
  - **Bygg:** `npm run build`. `out/index.html` og `out/anlegg/index.html` har `lang="nb"`, `<title>Marin</title>` og `<main></main>`.
  - **Token og standardtema:** et bygg med en midlertidig fil med klasser, som ble slettet etterpå. `bg-accent`, `text-title-mobile`, `desktop:text-title` (under `@media (min-width:600px)`), `px-page-x` og `rounded-default` ga regler. `bg-blue-500`, `p-4`, `md:block`, `text-sm` og `font-bold` ga ingen.
  - **Tokenene:** et engangsskript sammenlignet `@theme` med frontmatteren: 24 + 23 + 3 + 35 tokens, ingen dubletter, ingen ekstra og ingen avvik.
- `next dev` i Next 16.4 lager `frontend/AGENTS.md` når den merker at en KI-agent kjører den. Implementeringsagenten slettet fila, fordi den ikke hører til storyen.
- Det første `next build` slo på Next sin anonyme telemetri. Den gjelder maskinen, ikke prosjektet, og specen sier ikke noe om den.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Verification Gap | Ingen test som kan kjøres på nytt, sjekker at `@theme` er lik frontmatteren i DESIGN.md. Engangsskriptet er slettet | low | defer | Kommer ferdig verifisert fra revieweren: en endret eller slettet token gir ingen feil noe sted. Denne delen av specen har ingen testløper, så testen hører til Vitest i den utskilte specen (`deferred-work.md`). |
| 2 | Verification Gap | Ingen sjekk finner farger, pikselverdier eller klasser med egne verdier (`p-[13px]`) under `src/` | low | defer | Kommer ferdig verifisert. Det finnes ingen komponenter ennå, så sjekken ville bestått uten å teste noe. Den legges til sammen med den første testløperen (`deferred-work.md`). |
| 3 | Verification Gap | Kommentaren i `globals.css` sier at bare tokenene gir klasser, men klasser med egne verdier gir CSS | low | patch | Bekreftet: `bg-[#123456]` og `font-[600]` gir CSS. Kommentaren rettes. Samme setning i Design Notes er en del av specen og blir stående. |
| 4 | Edge Case | `--*: initial` fjerner også `--spacing`, så `p-0`, `m-0`, `gap-0`, `inset-0` og `top-0` gir ingen CSS | low | defer | Bekreftet. Henger sammen med 17: tilbakestillingen fjerner verdier som komponenter etter DESIGN.md kan trenge. Fiksen legger til tokens som ikke står i DESIGN.md. Story 2.4 er første story med komponenter og må velge (`deferred-work.md`). |
| 5 | Edge Case | `rounded` uten navn gir ingen CSS, og kommentaren sier feilaktig at det ikke kan finnes et token for den | low | patch | Bekreftet: `--radius: 6px` gir `.rounded`. Navnet `--radius-default` beholdes, slik Design Notes bestemmer, og bare kommentaren rettes. |
| 6 | Edge Case | `container` får `max-width: 600px` fra det eneste bruddpunktet | low | avvist | Bekreftet, men utviklerne bruker neppe `container` i vanlig arbeid: DESIGN.md bruker `content-max-width` (760px). Det finnes ingen fiks i koden, bare råd om hvilken klasse som skal brukes. |
| 7 | Edge Case | `out/404.html` er Next sin engelske standardside, og den blir svart i mørk modus | low | avvist | Bekreftet. Siden vises bare for ukjente stier, og brukerne går via lenker til `/` og `/anlegg/?nr=…`. Fiksen er en ny side med tekster som verken specen eller UX har bestemt. Tas opp med Fredrik. |
| 8 | Edge Case | `engines` gir bare en advarsel på Node under 22.12 | low | avvist | Node 20 nådde EOL 2026-04-30, og README oppgir kravet. Fiksen legger til en ny konfigurasjonsfil (`.npmrc`). |
| 9 | Edge Case | `next dev` lager `frontend/AGENTS.md` på nytt, og fila kan bli med i senere commits | low | defer | Bekreftet av implementeringen. Fiksen gjelder en fil med instruksjoner til agenter (`agentRules: false` eller en linje i `.gitignore`), og Fredrik må avgjøre om fila er ønsket (`deferred-work.md`). |
| 10 | Edge Case | Ingen favicon, så nettleseren får 404 på `/favicon.ico` | low | avvist | Brukeren merker ingenting. Ikonet er et designvalg som ingen spec har bestemt. |
| 11 | Edge Case | `/anlegg?nr=…` uten skråstrek gir 404 hvis serveren ikke omdirigerer | low | patch | Henger sammen med 20. Omdirigeringen hører til Story 2.3 (AD-9). Kommentaren i `next.config.ts` rettes til `/anlegg/?nr=…` og sier at formen uten skråstrek krever omdirigeringen. |
| 12 | Edge Case | README bør nevne `npm ci`, ellers kan `npm install` skrive om lockfila | false | avvist | `npm install` bruker versjonene i `package-lock.json` når `package.json` stemmer med den. Implementeringen installerte på nytt fra en tom mappe, og lockfila var byte-lik. Specen krever `npm install`. |
| 13 | Edge Case | Den andre kodeblokken i README gjentar `cd frontend`, som feiler hvis leseren allerede står i `frontend/` | low | avvist | Hver blokk i README starter fra rotmappa, også i seksjonen «API-et», som har `cd backend` to ganger. Å endre bare denne seksjonen ville gjort README ulik seg selv. |
| 14 | Edge Case | Specen står som `in-review`, men sprint-status står som `in-progress` | false | avvist | bmad-build setter sprint-status til `review` når storyen presenteres (steg 5), slik som for Story 2.1. |
| 15 | Blind Hunter | Ingenting holder tokenene i takt med DESIGN.md, og skriptet ble kastet | low | defer | Samme som 1. |
| 16 | Blind Hunter | `--*: initial` stopper ikke klasser med egne verdier. Kommentaren og matriseraden lover for mye, og ingen sjekk finnes | low | patch | Kommentaren rettes sammen med 3, og sjekken utsettes sammen med 2. Matriseraden «Standardtema» nevner bare `bg-blue-500`, `p-4` og `md:`, og den stemmer. |
| 17 | Blind Hunter | `font-semibold` og `font-bold` gir ingen CSS, men DESIGN.md krever vekt 600 (trefliste, ukestabell) og 700 (`uploaded-data-line`) | low | defer | Bekreftet i DESIGN.md linje 479 og 491. `font-[600]` virker og er verken en farge eller en pikselverdi. Valget mellom det og egne vekttokens tas i Story 2.4, sammen med 4 (`deferred-work.md`). |
| 18 | Blind Hunter | `body` har ikke tekstrollen `body`, så tekst uten rolleklasse får 16px/1,5 på alle bredder | low | patch | Bekreftet: `body` setter bare font og farger. Grunnregelen får størrelse og linjehøyde fra `body-mobile` og `body` fra bruddpunktet `desktop`. |
| 19 | Blind Hunter | 404-siden er engelsk og bruker Next sin egen stil | low | avvist | Samme som 7. |
| 20 | Blind Hunter | Kommentaren i `next.config.ts` bruker `/anlegg?nr=…`, ikke formen i arkitekturen | low | patch | Bekreftet. Rettes sammen med 11. |
| 21 | Blind Hunter | `frontend/package-lock.json` er ikke med i diffen | false | avvist | Fila ble holdt utenfor review-diffen med vilje, fordi den er generert. Den ligger i `frontend/`, versjonene er kontrollert, og den committes med storyen. |
| 22 | Blind Hunter | Implementation Notes mangler resultatet av `uv run pytest` og den manuelle sjekken med `npm run dev` | low | avvist | Fiksen er å endre specen. `uv run pytest` ga 540 bestått, og resultatene står i commit-meldingen og sesjonsloggen. |
| 23 | Blind Hunter | Node 22.12 er ikke testet, bare 26.7 | maybe-false | avvist | For å avgjøre det må `npm install` og `npm run build` kjøres på Node 22.12. Next 16.4.6 og Tailwind 4.3.5 krever mindre, og om det feiler, er det bare `low`. Vercels Node-versjon hører til Story 2.3. |
| 24 | Blind Hunter | «125 variabler» i Implementation Notes er én for mye: `--*: initial` er ikke en variabel | low | avvist | Bekreftet: det er 124 variabler pluss tilbakestillingen. Fiksen er å endre specen. |
| 25 | Blind Hunter | Statusen er ulik i specen og sprint-status, og den utskilte specen har ingen nøkkel i sprint-status | false | avvist | Statusen: samme som 14. Den utskilte delen står i `deferred-work.md`. Hvordan den skal spores, tas opp med Fredrik når storyen presenteres. |
| 26 | Blind Hunter | Ingenting hindrer at `frontend/AGENTS.md` kommer tilbake | low | defer | Samme som 9. |
| 27 | Blind Hunter | Telemetrien er nevnt, men ingen har bestemt noe | low | defer | Telemetrien følger av at stacken har Next.js (arkitekturen), ikke av koden i storyen. Uten miljøvariabler kan den bare slås av per maskin (`npx next telemetry disable`). Fredrik avgjør (`deferred-work.md`). |
| 28 | Blind Hunter | README bør nevne `npm ci` | false | avvist | Samme som 12. |
| 29 | Blind Hunter | README sier ikke hvordan `out/` kan vises | low | avvist | Utenfor intensjonen: montering av `out/` er Story 2.3, og ACene der dekker README. |

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
