# Epic 2 Context: Kari ser status for anlegget sitt (J1 og J2)

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Kari er driftsleder på et anlegg på Hitra og har ingen datafaglig bakgrunn. Hun søker opp anlegget sitt og får en detaljside med status (farge, symbol og tekst), en forklarende setning, graf, ukestabell og usikkerhetstekst. Hun kan velge en tidligere analyseuke for å se hva Marin ville vist da, og Marin åpner anlegget hennes direkte neste gang. Epicen er kjerneflyten i v1: API-et, Next.js-frontenden, lokal kjøring etter README og publisering på Vercel. Den bygger på kjernen, `datasett.json` og `backtest.json` fra Epic 1, som er ferdig. Backtesten ga en treffandel på 16,3 % og en presisjon på 13,3 %. Presisjonen er under 20 %, så reaksjonen på M1-C gjelder: Marin presenteres som en tidlig indikator, og usikkerhetsteksten sier at rød status betyr at brukeren bør følge ekstra med.

## Stories

- Story 2.1: API-kontrakten for kjerneflyten
- Story 2.2: Frontend-skjelett med designtokens
- Story 2.3: Kjøring lokalt og på Vercel
- Story 2.4: Forside og søk
- Story 2.5: Prognose for et anlegg i API-et
- Story 2.6: Forklarende tekster fra kjernen
- Story 2.7: Detaljside med statusboks og ukestabell
- Story 2.8: Trendgraf
- Story 2.9: Bytte analyseuke
- Story 2.10: Husket anlegg
- Story 2.11: Sjekkliste og tilgjengelighetskontroll

## Requirements & Constraints

- **Søk:**
  - Søket gir delvis treff på lokalitetsnavn uavhengig av store og små bokstaver, også for æ, ø og å, eller treff på helt lokalitetsnummer.
  - Backend sorterer treffene alfabetisk. Treflisten viser navn, lokalitetsnummer, kommune og fylke.
  - Ingen treff gir en melding, og søketeksten blir stående.
  - Søket kjøres ved Enter eller «Søk», aldri for hvert tastetrykk. Tomt søk gjør ingenting.
- **Forside:** én introsetning og en fargeforklaring for rød, gul, grønn og grå, hver med farge, symbol og navn. Forsiden ser lik ut ved første besøk og via «Bytt anlegg».
- **Husket anlegg:** nettleseren lagrer bare lokalitetsnummeret, aldri lusetall eller analyseuke. Finnes anlegget, åpnes detaljsiden direkte med «Sist viste anlegg» og analyseuke 2026 uke 42. Ellers vises forsiden, også når nummeret ikke lenger finnes, og da uten feilmelding.
- **Analyseuke:**
  - Brukeren velger fra 2025 uke 1 til og med 2026 uke 42 (94 uker). Standard er 2026 uke 42.
  - Uke 53 finnes bare for ISO-år som har den, og 2025 har den ikke.
  - Prognosen bruker bare tellinger til og med analyseuka.
  - «Prognose regnet fra uke X, ÅÅÅÅ» står i statusboksen for alle statuser. Ved bytte av uke endres denne teksten, status, graf og tabell samtidig.
- **Detaljside:**
  - Statusteksten er tegn for tegn lik briefen, med symbolet først.
  - Under statusteksten står nøyaktig én forklarende setning etter malene i EXPERIENCE.md. Retningsordet («har steget», «har falt» eller «har ligget stabilt») følger fortegnet på trendlinja. Grensen i setningen er grensen i den estimerte uka. Det står «1 uke» i entall, og året tas med når uka ligger i et annet år enn analyseuka.
  - Statusboksen kan forstås alene som skjermbilde. Den viser navn, lokalitetsnummer, kommune, fylke, analyseuke og status.
  - Estimert ISO-uke og antall uker dit, regnet fra analyseuka, vises bare ved varsel og følg med.
  - Grafen viser målte tall i vinduet, trenden til analyseuke + 6 og grensen per uke som trapp.
  - Tabellen viser 5 uker, med eldste uke øverst og «ikke telt» der det mangler telling.
  - Uten prognose (grå status eller brudd nå) vises ingen trend og ingen estimert uke. Ved «ingen ny telling» viser tabellen de 5 ukene før analyseuka. Ved ukjent område vises ingen grenselinje.
- **Usikkerhetstekst:**
  - Teksten vises for alle statuser, også grå.
  - X og Y leses fra `backtest.json` som hele prosent og står aldri i koden.
  - M1-C-varianten brukes når `antall_varsler_med_brudd` × 5 < `antall_varsler`, regnet eksakt med antallene og ikke med den avrundede andelen. Det gjelder dagens fil, som gir 16 % og 13 %.
  - Ordlyden er «varslet Marin rødt … Av alle røde varsler …». Eksempelet «ga Marin varsel» er utdatert.
  - Mangler fila, er den ugyldig eller avviker parameterne fra kjernens konstanter, er teksten bare «Prognosen er en enkel trendberegning, ikke en garanti.». Appen krasjer ikke, og en advarsel skrives til stderr.
- **Generelt:**
  - Grensesnittet er på norsk bokmål, med desimalkomma og uker skrevet «uke 42, 2026».
  - Status vises alltid med farge, symbol og tekst sammen.
  - Appen behandler ingen personopplysninger, og detaljsiden vises på under 2 sekunder.
  - Ved kjøring trengs ikke nett, nøkler, miljøvariabler eller betalte kontoer.
  - Den publiserte versjonen har samme funksjoner og data som den lokale, og adressen står i README.
- **Testing:**
  - Automatiske tester dekker søk (delvis treff, store og små bokstaver, nummer og ingen treff) og analyseuke.
  - De dekker også alle verdier på detaljsiden som kan hentes uten nettleser: tekster, tabellrader, estimert uke og grafpunkter.
  - Resten kontrolleres med en README-sjekkliste. Den er en ordrett kopi av de testbare konsekvensene for søk, analyseuke og detaljside.
  - Sjekklisten har i tillegg kontroll i gråtoner og med deuteranopi-simulering, og ved 320px, 600px, 400 % zoom og 200 % tekstzoom.

## Technical Decisions

- **Kontrakten først:** Pydantic-modellene i `marin.api` er fasit og speiler kjernens typer én til én.
  - `backend/openapi.json` committes, og en pytest feiler ved avvik.
  - `frontend/src/api/schema.ts` genereres med openapi-typescript og redigeres aldri for hånd.
  - Alle kall går gjennom `frontend/src/api/`. API-basen er `''` i bygget og `http://127.0.0.1:8000` når `NODE_ENV === 'development'`.
- **Ruter:**
  - `GET /api/anlegg?q=` gir `[AnleggInfo]`.
  - `GET /api/anlegg/{lokalitetsnr}` gir `AnleggInfo`, `analyseuker` (nyeste først) og `standard_analyseuke`, eller 404.
  - `GET /api/anlegg/{lokalitetsnr}/prognose?ar=&uke=` gir `Detaljsvar`. En uke utenfor lista gir 422, og et ukjent nummer gir 404.
  - Opplastingsrutene lages i Epic 3.
- **`Detaljsvar`** har formen `{kilde, anlegg, analyseuke, status{farge, arsak, symbol, tekst, uke_tekst, forklaring}, estimert_uke{uke, uker_til}|null, tabell[5]{uke, verdi|null, siste_telling}, graf{punkter[{uke, malt, trend, grense}], kryssing{uke, tekst}|null}, tekstoppsummering, usikkerhetstekst}`.
  - Svaret bygges av `bygg_detaljsvar(info, serie, omrade, analyseuke, kilde)`, som kaller `vurder` med hele serien. Området kommer fra `omrade_fra_fylke`.
  - Feltnavn er i `snake_case`, uker er `{ar, uke}`, «ikke telt» er `null` og lokalitetsnummer er heltall.
  - Lusetall er JSON-tall. Pydantic v2 gjør `Decimal` om til streng som standard, så det må overstyres.
  - Feil sendes som FastAPIs `{detail}` med riktig statuskode. Ved nettverks- eller 5xx-feil viser frontend en generell melding fra `tekster.ts`.
- **Tekster og regler:**
  - Kjernen lager alle tekster som avhenger av data eller regelutfall: statustekst, forklaring, grå-forklaring, estimert uke, usikkerhetstekst, kryssingsetikett («✕ Varsel uke 44») og tekstoppsummering.
  - Frontend viser disse tekstene uendret. Faste tekster ligger bare i `frontend/src/tekster.ts`.
  - Frontend velger farge og stil bare ut fra `farge` og `arsak`. Den regner aldri ut status, trend, grense, vindu, tabellrader, x-område eller valgbare uker, og den har ingen ISO-kalender.
- `datasett.json` og `backtest.json` leses én gang ved oppstart med `importlib.resources` og holdes i minnet.
- **Statisk frontend:** Next.js bygges med `output: 'export'` og `trailingSlash: true`, uten route handlers, server actions, middleware, `rewrites` eller dynamiske ruter. Detaljsiden er `/anlegg/?nr={nr}`, med `&husket=1` ved omdirigering. Sider som bruker `useSearchParams`, pakkes i `<Suspense>` med en nøytral reserve.
- **Henting:** detaljsiden sender én forespørsel per valgt analyseuke, 300 ms etter siste endring. Svar for en uke som ikke lenger er valgt, avbrytes med `AbortController`. Hele siden tegnes fra ett `Detaljsvar`.
- **Husket anlegg:** `frontend/src/lib/husketAnlegg.ts` lagrer i `localStorage` under `marin.sistViste`, bare etter et vellykket `Detaljsvar` med `kilde = innebygd`. Modulen tåler at lagringen mangler eller feiler. Forsiden omdirigerer bare første gang appen tegnes i fanen, til `/anlegg/?nr={nr}&husket=1`.
- **Graf:** `TrendGraf` er en egen SVG-komponent uten grafbibliotek. Den tegner bare `Detaljsvar.graf`.
- **Formatering:** `formatLus` og `formatUke` i `frontend/src/lib/format.ts` testes mot de samme vektorene som kjernen, i `backend/tests/data/format.json`.
- **Kjøremåter:**
  - Utvikling: `npm run dev` kjører på port 3000 og `uv run uvicorn marin.api.app:app --reload` på port 8000. CORS tillater bare `http://localhost:3000`.
  - Lokalt: `npm run build` lager `frontend/out/`. FastAPI monterer mappa etter alle `/api`-rutene, bare når mappa finnes. En ukjent `/api/*`-rute gir JSON 404.
  - Vercel Services (beta): `vercel.json` har servicene `frontend` og `backend`. `/api/(.*)` går til backend og resten til frontend, fra samme opphav.
  - Reserveplan: to Vercel-prosjekter, der bare API-base-URL og CORS endres. Byttet føres i `issues.md`.
- **Tester:** `uv run pytest` kjører backendtestene, også testene for `openapi.json` og monteringen. `npm test` kjører Vitest for `husketAnlegg`, `formatLus` og `formatUke`.
- **Stack:**
  - Backend: FastAPI 0.163.1, Uvicorn 0.54.0, Pydantic 2.14.3 og httpx2 2.16.2 (dev).
  - Frontend: Node ≥ 22.12, Next.js 16.4.6, React 19.3.1, TypeScript 5.9.3, Tailwind 4.3.5, openapi-typescript 7.13.0 og Vitest 5.1.0.
- **Navngiving:** norske fagord uten æ, ø og å. Python bruker `snake_case`, TypeScript `camelCase` og komponenter `PascalCase`.

## UX & Interaction Patterns

- **Visuell stil:** «Rolig rapport» på hvit flate med én marineblå aksent.
  - Full statusfarge brukes bare i statusboksen. Statusmerker og fargeforklaring har hvit bakgrunn, tynn kant og en liten rund markør.
  - Gul har alltid mørk kant. Grå er hvit med stiplet kant.
  - Alle tokens fra DESIGN.md står én gang som Tailwind `@theme` i `frontend/src/app/globals.css`, og komponentene bruker bare tokennavn.
  - Siden bruker systemfonter og bare lys modus, med bruddpunkt på 600px.
- **Detaljsiden** har én kolonne på maks 760px, i denne rekkefølgen:
  1. «Sist viste anlegg», bare ved `husket=1`
  2. tittel med sted
  3. analyseukevelger
  4. statusboks
  5. graf med tegnforklaring og tekstoppsummering
  6. ukestabell
  7. usikkerhetstekst, med en tynn strek over
- **Statusboks:**
  - Innhold ovenfra: navn, stedslinje, «Prognose regnet fra …», symbol i hvit sirkel med R4-teksten og `uke_tekst`, og til slutt forklaringen.
  - Boksen har ingen interaktive elementer og er synlig uten rulling på desktop ved 100 % zoom.
  - Boksen er en navngitt region («Status»). Bare statusoverskriften er `aria-live="polite"`. Elementet finnes fra start, og bare teksten byttes. Symbolet har `aria-hidden`.
- **Lasting:** «Regner ut prognose …» står i statusboksens plass, på hvit flate med heltrukken nøytral kant. Den har ingen statusfarge, stipling, symbol eller animasjon, og står utenfor live-elementet. Tittelen og velgeren vises med en gang.
- **Analyseukevelger:**
  - Velgeren er en vanlig nedtrekksliste med etiketten «Analyseuke». Verdiene kommer fra API-et, med nyeste uke først.
  - Valget gjelder med en gang, uten «Oppdater»-knapp, og anlegget og rulleposisjonen beholdes.
  - Skjermleseren leser bare opp den nye statusoverskriften.
- **Toppfelt:**
  - Logoen «Marin» går til forsiden.
  - På desktop står et søkeskjema med skjult etikett og sekundærknappen «Søk», og lenken «Bytt anlegg».
  - På mobil står lenken «Søk / bytt», som går til forsiden med fokus i søkefeltet.
  - På forsiden står bare logoen. Lenken «Last opp egne tall» kommer i Epic 3.
- **Graf:**
  - Grafen er ikke interaktiv. Den har `role="img"`, og innholdet i SVG-en er skjult for skjermleser.
  - En synlig tekstoppsummering står under grafen som figurtekst.
  - All tekst i grafen er minst 13 CSS-px slik den vises, og følger tekstzoom. Tekst i en SVG som skaleres med `viewBox`, oppfyller ikke kravet.
- **Tilgjengelighet:**
  - Siden har `lang="nb"`. Alt kan brukes med tastatur, og Tab-rekkefølgen følger leserekkefølgen.
  - Fokusmarkeringen er synlig: 2px aksent med 2px avstand. Lenker er i aksentfarge og understreket.
  - Ingen funksjon finnes bare ved hover. Trykkflater er minst 44 × 44px på mobil, og felt og knapper er minst 44px høye.
  - Siden har ingen vannrett rulling ved 320px bredde, 400 % zoom og økt tekstavstand. Toppfeltet bryter til to linjer ved behov.

## Cross-Story Dependencies

- Epic 1 er ferdig og leverer `vurder`, ISO-kalenderen, `grense`, `omrade_fra_fylke`, `format_lus`/`format_uke`, `datasett.json` og `backtest.json`.
- Story 2.1 (kontrakten) kommer først. Deretter kan backend (2.5, så 2.6) og frontend (2.2, så 2.3) bygges parallelt. 2.4 og 2.5 er uavhengige av hverandre. 2.3 trenger bygget fra 2.2.
- 2.5 lar `forklaring`, `tekstoppsummering` og `usikkerhetstekst` stå som tomme strenger, og 2.6 fyller dem.
- 2.7 tegner detaljsiden fra `Detaljsvar`. 2.8 (grafen mellom statusboksen og tabellen), 2.9 (ukevelgeren) og 2.10 (husket anlegg) bygger på 2.7. 2.11 (sjekklisten, lokalt og på Vercel) kommer sist.
- Epic 3 gjenbruker detaljsiden og `bygg_detaljsvar` for opplastede data (`kilde = opplastet`, `/anlegg/?opplastet=1`). Modeller, ruter og lenke for opplasting lages ikke i denne epicen.
- Disse åpne punktene fra Epic 1 står i `_bmad-output/implementation-artifacts/deferred-work.md`:
  - Story 2.1 må sørge for at lusetall sendes som JSON-tall.
  - `Vurdering` mangler antall tellinger i vinduet. Forklaringen ved «for lite data» trenger dette tallet, så Story 2.6 må skaffe det.
  - `uv run pytest` blokkeres av Windows Programkontroll på Fredriks maskin. Bruk `uv run python -m pytest` i stedet.
