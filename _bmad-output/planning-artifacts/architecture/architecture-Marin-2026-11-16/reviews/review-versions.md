---
review: versjoner og teknologikombinasjon (reality check)
target: ../ARCHITECTURE-SPINE.md, ../.memlog.md
date: 2026-11-16
method: registre (PyPI JSON, npm registry), offisielle dokumenter (nextjs.org, tailwindcss.com, pandas.pydata.org), kildekode (Starlette 1.10.0, FastAPI 0.163.1, CPython 3.14), uv pip compile og npm lock-only-oppløsning i en egen mappe. Ingen persondata sendt.
---

# Review: versjoner og teknologivalg i Marin-spinen

## Konklusjon

**Delvis kontrollert.** Alle versjonene i Stack-tabellen finnes og var de nyeste i registrene 2026-11-16, så memlog-påstanden stemmer. **Kombinasjonen** er derimot ikke kontrollert. To valg i spinen stopper bygget eller innleveringen slik de står:

1. **TypeScript 7.0.2 sammen med `openapi-typescript` (AD-3).** `npm install` feiler med ERESOLVE. Funnet er reprodusert.
2. **`output: 'export'` med standard `trailingSlash`, servert av FastAPI `StaticFiles` (AD-9).** `/anlegg?nr=…` gir 404 når siden lastes direkte eller oppdateres.

I tillegg er Node-gulvet feil, og noen nødvendige avhengigheter mangler i Stack-tabellen. Funnene står under, sortert etter alvorlighet.

---

## Funn

### F1 — Høy (blokkerer): TypeScript 7.0.2 virker ikke med `openapi-typescript`

**Bevis**

- `typescript@7.0.2` (npm) eksporterer bare `"." → ./lib/version.cjs`, og den fila inneholder bare `version` og `versionMajorMinor`. Den klassiske JS-kompilator-API-en (`ts.factory`, `createProgram`) finnes ikke. Det som finnes, ligger under `typescript/unstable/*`.
- `openapi-typescript@7.13.0` er siste versjon (2026-02-11). Den har `peerDependencies: { typescript: "^5.x" }`, og `dist/lib/ts.mjs` gjør `import ts from 'typescript'` og bruker `ts.factory.*` overalt.
- Reprodusert: `npm install --package-lock-only` med next 16.4.6, react 19.3.1, typescript 7.0.2 og openapi-typescript 7.13.0 gir `ERESOLVE … peer typescript@"^5.x" from openapi-typescript@7.13.0`. Med `--legacy-peer-deps` vil generatoren krasje når den kjører, fordi `ts.factory` er `undefined`. Dette er utledet av koden ovenfor, ikke kjørt.
- Next.js 16.4.6 tåler TS 7. `next build` bruker prosjektets lokale `tsc` CLI som standard (nextjs.org/docs/app/api-reference/config/typescript, «Using TypeScript 7», lastUpdated 2026-08-25). Problemet ligger altså i verktøyene rundt, ikke i Next.
- Samme feilklasse gjelder ESLint: `eslint-config-next@16.4.6` → `typescript-eslint@8.72.2`, som har peer `typescript >=4.8.4 <6.1.0`. Med TS 7 gir installasjonen bare advarsler (`ERESOLVE overriding peer dependency`), men linting av `.ts`-filer vil feile når den kjører.

**Forslag:** Lås **`typescript` til `5.9.3`**, den nyeste 5.x. Det er den eneste versjonen som samtidig oppfyller openapi-typescript (`^5.x`), typescript-eslint (`<6.1.0`) og Next 16 (minimum 5.1.0). Oppløsningen er kontrollert uten konflikter: next 16.4.6, react/react-dom 19.3.1, recharts 3.10.1, react-is 19.3.1, tailwindcss og @tailwindcss/postcss 4.3.5, vitest 5.1.0, openapi-typescript 7.13.0, @types/react 19.3.0 og typescript 5.9.3. Ta TS 7 inn igjen først når `openapi-typescript` støtter den.

*Alternativ (anbefales ikke):* behold TS 7 og kjør generatoren isolert med `npx -p typescript@5.9.3 -p openapi-typescript@7.13.0 openapi-typescript …`. Da har prosjektet to TypeScript-versjoner, og generering krever nett.

### F2 — Høy (blokkerer innlevering): `/anlegg?nr=…` gir 404 ved direkte lasting og oppdatering

**Bevis**

- Next-dokumentasjonen (Static Exports, lastUpdated 2026-08-09) sier: standard `trailingSlash: false` gir `/me.html`, og `trailingSlash: true` gir `/me/index.html`. Spinen sier ikke noe om `trailingSlash`, så bygget gir `out/anlegg.html` og `out/opplasting.html`.
- Starlette 1.10.0 `StaticFiles.get_response` med `html=True` prøver tre ting: (1) eksakt fil, (2) katalog + `index.html` med 307-omdirigering til avsluttende `/` der spørrestrengen beholdes, (3) `404.html`. **Den prøver aldri `<sti>.html`.**
- Følgen er at `/anlegg?nr=123` bare virker ved klientnavigering fra forsiden. Oppdatering, bokmerke, ny fane eller en delt lenke gir `404.html` med status 404. `next dev` skjuler feilen, så den viser seg først i innleveringsmodus (NFR1-sjekklisten).

**Forslag (skrives inn i AD-9)**

- `next.config.ts`: `output: 'export'` og **`trailingSlash: true`**. Da blir det `out/anlegg/index.html`, og Starlette omdirigerer `/anlegg?nr=123` → `/anlegg/?nr=123` og serverer `index.html`. Det trengs ingen egen kode.
- Montér `StaticFiles` på `"/"` **etter** at `/api`-ruterne er registrert. Legg også en `/api/{path:path}`-rute som gir JSON-404 foran monteringen. Ellers får ukjente `/api`-kall `404.html` i stedet for `{detail}`, og det bryter konvensjonen for feil.
- Legg en test eller et punkt i README-sjekklisten: `GET /anlegg?nr=<kjent nr>` gir 200 etter `npm run build`.

### F3 — Middels: `StaticFiles` krasjer oppstart og pytest når `frontend/out/` mangler

**Bevis:** Starlette 1.10.0 `StaticFiles.__init__` har `check_dir=True` som standard og kaster `RuntimeError("Directory '…' does not exist")`. Spinen beskriver utvikling med `uvicorn --reload` før noe frontend-bygg, og `uv run pytest` bruker TestClient, som importerer appen. På en fersk klone feiler begge.

**Forslag:** Montér bare når `OUT_DIR.is_dir()`, og logg en melding ellers. Bruk ikke `check_dir=False`, for det flytter feilen til 500 ved første forespørsel. Skriv det inn i AD-9.

### F4 — Middels: Nødvendige avhengigheter mangler i Stack

Kontrollert med `uv pip compile` for Python 3.14 / `x86_64-pc-windows-msvc` / `--only-binary :all:`. Det ga 35 pakker, alle med ferdige hjul (wheels).

| Pakke | Versjon | Hvorfor |
| --- | --- | --- |
| `python-multipart` | 0.0.34 | `POST /api/opplasting` (multipart). FastAPI 0.163.1 feiler allerede når ruten defineres: *«Form data requires "python-multipart" to be installed»*. |
| `httpx2` (dev) | 2.16.2 | Starlette 1.10.0 `testclient.py` importerer `httpx2`. Vanlig `httpx` er bare en utfasingsreserve med advarsel. Konvensjonen «FastAPI TestClient» krever den. |
| `react-is` | 19.3.1 | Peer-avhengighet til Recharts 3. README-en sier at den «må matche installert react». |
| `@tailwindcss/postcss` + `postcss` | 4.3.5 + gjeldende | Tailwind v4 i Next (tailwindcss.com, Next.js-guide). |
| `@types/react`, `@types/react-dom` | 19.3.0 | TS-typer for React 19.3. |

Unngå `fastapi[standard]` som snarvei. Den drar inn opentelemetry-sdk, fastapi-cli, jinja2, email-validator m.m., og det trengs ikke her.

### F5 — Middels: Node-gulvet «≥ 20.9» er feil

**Bevis**

- Node 20 nådde EOL 2026-04-30 (endoflife.date).
- `vitest@5.1.0` krever `^22.12.0 || ^24.0.0 || >=26.0.0`, `vite@8.3.8` krever `^20.19.0 || >=22.12.0`, og `jsdom@31.0.1` (hvis den brukes til `localStorage`-tester) krever `^22.22.2 || ^24.15.0 || >=26.0.0`.
- 20.9 er bare Next sitt eget minimum.

**Forslag:** Skriv «Node.js ≥ 22.12, anbefalt 24 LTS (24.22.3) eller 26 LTS (26.13.1); lokalt 26.7» og sett `"engines": { "node": ">=22.12" }` i `package.json`. Lokal 26.7.0 er grei, men 26 ble LTS 2026-10-28, og 26.13.1 er siste patch.

### F6 — Middels: `useSearchParams` krever `<Suspense>`, og de vanlige alternativene er sperret ved eksport

**Bevis:** I `useSearchParams`-dokumentasjonen (lastUpdated 2026-11-06) står det: *«During production builds, a static page that calls useSearchParams from a Client Component must be wrapped in a Suspense boundary, otherwise the build fails»*. Feilen viser seg ikke i `next dev`. Alternativene `connection()`, `force-dynamic` og `searchParams`-prop i en serverside krever dynamisk rendering, og det virker ikke med `output: 'export'`.

**Forslag (skrives inn i AD-9):** `app/anlegg/page.tsx` skal være en serverkomponent som rendrer `<Suspense fallback={…}><AnleggKlient /></Suspense>`, og `useSearchParams` brukes bare i klientkomponenten. Fallback skal være nøytral og ikke det `aria-live`-elementet som har statusoverskriften. Det samme gjelder `?opplastet=1`.

### F7 — Lav: «gjeldende» i stedet for låste versjoner

- `openapi-typescript`: lås til **7.13.0**. Hvilken versjon man får, avgjør hvilken TypeScript som er mulig, se F1.
- `Vitest`: lås til **5.1.0**. Den setter Node-gulvet, se F5.
- `uv`: lokalt 0.12.10, siste 0.13.8. «gjeldende» holder, men vurder `[tool.uv] required-version = ">=0.12"`.
- Python: legg `.python-version` = `3.14` i `backend/`. 3.15.2 finnes allerede. Alle hjul finnes også for cp315, så ingenting brytes, men oppsettet blir mer reproduserbart. Siste patch er 3.14.10.

### F8 — Lav: MIME-typer fra Windows-registeret kan ødelegge JS/CSS fra `StaticFiles`

**Bevis:** I CPython 3.14 kaller `Lib/mimetypes.py` `db.read_windows_registry()` i `init()`, og `add_type` overskriver de innebygde typene. Det er en kjent feil (bpo-43975, fortsatt åpen) at `.js` kan bli `text/plain` på maskiner der annen programvare har endret `HKCR\.js\Content Type`. Starlette `FileResponse` bruker `mimetypes.guess_type`. Nettlesere avviser stilark med feil MIME-type.

**Forslag:** Kall `mimetypes.add_type("text/javascript", ".js")` og `mimetypes.add_type("text/css", ".css")` ved oppstart, før `StaticFiles` monteres. Det er to linjer som forsikring for NFR1 på ukjente Windows-PC-er.

### F9 — Lav: Tailwind v4 `@theme` sammen med Recharts-farger

**Bevis:** Tailwind-dokumentasjonen (Theme) sier: *«By default only used CSS variables will be generated … use the `static` theme option»*. Recharts får farger som SVG-props (`stroke`, `fill`), ikke som utility-klasser. `var(--color-…)` kan derfor peke på en variabel som ikke finnes i CSS-en.

**Forslag:** Bruk `@theme static { … }` for status- og graftokenene. Vurder også `--color-*: initial;` slik at bare DESIGN.md-tokenene finnes. Det håndhever konvensjonen «aldri rå fargekoder». Recharts-komponentene må ligge i `'use client'`-filer.

### F10 — Lav: Klart for kodegenerering, med ett forbehold

FastAPI 0.163.1 gir OpenAPI **3.1.0** (`applications.py`), og openapi-typescript 7 støtter det. `separate_input_output_schemas` står på som standard. Hvis samme Pydantic-modell (f.eks. `Serie`) brukes både i svar (`/api/opplasting`) og i forespørsel (`/api/prognose`) og har felt med standardverdier, kan `schema.ts` få navnene `Serie-Input` og `Serie-Output`. **Forslag:** `FastAPI(separate_input_output_schemas=False)`, eller bevisst godta de to navnene i AD-3.

### F11 — Lav: API-adresse i utvikling når «ingen miljøvariabler» gjelder

I utvikling kjører `next dev` på :3000 og `uvicorn` på :8000. Ved innlevering er det samme opphav. `rewrites` virker ikke med `output: 'export'`. **Forslag:** La `frontend/src/api/` velge base ut fra `process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : ''`. Next setter den selv, så det er ikke en brukerkonfigurert miljøvariabel. Slå på CORS-mellomvaren i FastAPI bare for `http://localhost:3000`.

### F12 — Lav: Hvor den opplastede serien holdes (AD-4) i App Router

AD-4 sier «komponenttilstand». Navigering fra `/opplasting` til `/anlegg?opplastet=1` avmonterer sidekomponenten, så serien må ligge i en klientkontekst i en felles layout, for eksempel rot-layout eller en rutegruppe. Den forsvinner ved oppdatering, og det passer med FR26. **Forslag:** Skriv inn hvor serien bor, og hva `/anlegg?opplastet=1` viser når serien mangler (forsiden eller opplastingssiden).

### Info

- `next/image` med standard-loader virker ikke ved eksport. Bruker dere bilder, trengs `images: { unoptimized: true }`. Spinen har systemfonter og ingen bilder, så det er greit nå.
- Next 16 har omdøpt `middleware` til `proxy`. AD-9 bør si «proxy (tidligere middleware)», slik at forbudet treffer det nye navnet.
- Route handlers med `GET` + `force-static` *er* støttet ved eksport. Spinens totale forbud er strengere enn nødvendig, men greit.
- Turbopack er standard for `next dev` og `next build` i Next 16. `next lint` er fjernet, så ESLint kjøres eventuelt direkte (se F1).

---

## Kontrollert og i orden

### Python (PyPI, 2026-11-16)

| Spine | Registeret | Publisert | Vurdering |
| --- | --- | --- | --- |
| Python 3.14 | 3.14.10 siste patch (3.15.2 finnes) | — | OK. Lås patch via `.python-version` (F7). |
| FastAPI 0.163.1 | 0.163.1 (siste) | 2026-11-15 | OK. Krever starlette ≥ 0.46, løser til 1.10.0. Ren Python. |
| Uvicorn 0.54.0 | 0.54.0 (siste) | 2026-09-25 | OK. `[standard]` gir httptools 0.9.0 (cp314 win) og watchfiles 1.3.0 (abi3) for `--reload`. |
| Pydantic 2.14.3 | 2.14.3 (siste) | 2026-11-05 | OK. pydantic-core 2.50.4 har cp314 win_amd64-hjul. |
| pandas 3.1.1 | 3.1.1 (siste) | 2026-11-04 | OK. Har cp314 win_amd64-hjul. Krever numpy ≥ 2.3.3 på 3.14, løser til 2.5.5 (cp314 win). pyarrow er valgfri. |
| openpyxl 3.1.5 | 3.1.5 (siste) | 2024-06-28 | OK. Er nøyaktig pandas 3 sitt minimum (`pandas[excel]: openpyxl>=3.1.5`). Ren Python, ingen kjent 3.14-feil. Lavt utgivelsestempo. Ved treg oppstart: `python-calamine` 0.9.1 (cp314 win) som `engine="calamine"`. |
| pytest 9.2.0 | 9.2.0 (siste) | 2026-10-27 | OK. |
| uv «gjeldende» | 0.13.8 (lokalt 0.12.10) | 2026-11-12 | OK (F7). |

Merknader om pandas 3 for `kilder/`, fra whatsnew v3.0.0:

- Ny standard string-dtype: tekstkolonner er ikke lenger `object`.
- Copy-on-Write er eneste modus, så kjedet tilordning virker ikke.
- Datoparsing bruker mikrosekunder som standard.
- Sett `dtype` eksplisitt for `lokalitetsnr` (heltall) og uke-kolonner i stedet for å stole på inferens.

### Frontend (npm, 2026-11-16)

| Spine | Registeret | Publisert | Vurdering |
| --- | --- | --- | --- |
| Next.js 16.4.6 | 16.4.6 (latest) | 2026-11-09 | OK. engines `>=20.9.0`, peer react `^19`. |
| React 19.3.1 | 19.3.1 (latest) | — | OK. react-dom 19.3.1 har peer `react ^19.3.1`. |
| TypeScript 7.0.2 | 7.0.2 (latest) | — | **Finnes, men passer ikke (F1). Bruk 5.9.3.** |
| Tailwind CSS 4.3.5 | 4.3.5 (latest) | 2026-11-06 | OK. `@theme` er riktig mekanisme. Krever `@tailwindcss/postcss` (F4) og `@theme static` for SVG-farger (F9). |
| Recharts 3.10.1 | 3.10.1 (latest) | 2026-07-25 | OK med React 19. Peer `react ^19.0.0`, krever `react-is` 19.3.1 (F4). |
| openapi-typescript «gjeldende» | 7.13.0 | 2026-02-11 | OK med TS 5.x og OpenAPI 3.1. Lås versjonen (F7). |
| Vitest «gjeldende» | 5.1.0 | 2026-11-02 | OK. Hever Node-gulvet (F5). Lås versjonen. |
| Node.js ≥ 20.9 (lokalt 26.7) | 26 LTS siden 2026-10-28, siste 26.13.1; 20 EOL 2026-04-30 | — | **Gulvet er feil (F5).** |

### Next 16 `output: 'export'` mot AD-9

| Punkt | Spinen | Fakta (nextjs.org) | Status |
| --- | --- | --- | --- |
| Dynamiske ruter | Forbudt, bruker `?nr=` | Krever `generateStaticParams`. Spørrestreng virker. | OK |
| Route handlers | Forbudt | Bare `GET` + `force-static` virker | OK (strengere) |
| Middleware/proxy | Forbudt | Proxy virker ikke | OK, bruk nytt navn |
| Server actions, rewrites, headers, cookies | Forbudt eller ikke brukt | Virker ikke | OK |
| `useSearchParams` | Ikke nevnt | Må ligge i `<Suspense>`, ellers feiler bygget | **F6** |
| `next/image` | Ikke brukt | Standard-loader virker ikke | Info |
| Filnavn og `trailingSlash` | Ikke nevnt | `false` gir `x.html`, `true` gir `x/index.html` | **F2** |

---

## Foreslått Stack-tabell

| Name | Version |
| --- | --- |
| Python | 3.14 (`.python-version`; 3.14.10) |
| uv | ≥ 0.12 (siste 0.13.8) |
| FastAPI | 0.163.1 |
| python-multipart | 0.0.34 |
| Uvicorn | 0.54.0 (`[standard]`) |
| Pydantic | 2.14.3 |
| pandas | 3.1.1 |
| openpyxl | 3.1.5 |
| pytest | 9.2.0 |
| httpx2 (dev, TestClient) | 2.16.2 |
| Node.js | ≥ 22.12 (anbefalt 24 LTS eller 26 LTS; lokalt 26.7) |
| Next.js | 16.4.6 (`output: 'export'`, `trailingSlash: true`) |
| React / React DOM | 19.3.1 |
| TypeScript | **5.9.3** (ikke 7.x før openapi-typescript støtter det) |
| Tailwind CSS / @tailwindcss/postcss | 4.3.5 |
| Recharts / react-is | 3.10.1 / 19.3.1 |
| openapi-typescript | 7.13.0 |
| Vitest | 5.1.0 |

## Kilder og metode

- PyPI JSON-API (`/pypi/<pkg>/json`): fastapi, uvicorn, pydantic, pydantic-core, pandas, openpyxl, pytest, starlette, numpy, python-multipart, httpx2, watchfiles, httptools, python-calamine, uv.
- npm-registeret: next, react, react-dom, typescript (7.0.2-manifest og `lib/version.cjs`), tailwindcss, @tailwindcss/postcss, recharts (3.10.1-manifest og README), openapi-typescript (7.13.0 `package.json` og `dist/lib/ts.mjs`), vitest, vite, jsdom, typescript-eslint, eslint-config-next.
- endoflife.date: nodejs (20, 24, 26) og python.
- nextjs.org: Static Exports (2026-08-09), TypeScript (2026-08-25), useTypeScriptCli (2026-08-03), useSearchParams (2026-11-06), missing-suspense-with-csr-bailout, Upgrading to v16 (2026-11-06), bloggen Next.js 16.3 (2026-08-03).
- tailwindcss.com: Next.js-guide og Theme.
- pandas.pydata.org: whatsnew v3.0.0.
- Kildekode: Starlette 1.10.0 `staticfiles.py` og `testclient.py`; FastAPI 0.163.1 `dependencies/utils.py` og `applications.py`; CPython 3.14 `Lib/mimetypes.py`.
- Egne kontroller i en midlertidig mappe utenfor repoet:
  - `uv pip compile` (Python 3.14, Windows x64, bare hjul): 35 pakker løst.
  - `npm install --package-lock-only --ignore-scripts` med TS 7.0.2: ERESOLVE.
  - Samme med TS 5.9.3: løst uten konflikter.
  - Samme med ESLint og TS 7: bare peer-override-advarsler.
