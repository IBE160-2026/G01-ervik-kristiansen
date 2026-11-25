---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-Marin-2026-11-02/prd.md
  - _bmad-output/planning-artifacts/architecture/architecture-Marin-2026-11-16/ARCHITECTURE-SPINE.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/EXPERIENCE.md
  - _bmad-output/planning-artifacts/briefs/brief-Marin-2026-09-17/brief.md
  - _bmad-output/planning-artifacts/briefs/brief-Marin-2026-09-17/addendum.md
---

# Marin – epics og stories

## Oversikt

Dette dokumentet deler Marin v1 opp i epics og stories. Grunnlaget er kravene i PRD-en, UX-spesifikasjonen (DESIGN.md og EXPERIENCE.md), arkitekturen og briefen med addendum.

Kravtekstene under er forkortet. De testbare konsekvensene står i PRD-en, kap. 5, og kopieres inn i akseptansekriteriene til storyene som dekker kravene.

## Kravoversikt

### Funksjonelle krav

**Datagrunnlag (PRD 5.1)**

- FR1: Appen bruker lusetall fra BarentsWatch-utdraget i `data/barentswatch/`, fra 2025 uke 1 til og med 2026 uke 42. Senere uker leses ikke inn. Et skript lager en forhåndsbehandlet datafil som committes, og appen leser den fila (AD-10).
- FR2: En uke er «uke med telling» når `Voksne hunnlus` har en verdi. Uker uten verdi er uker uten telling, og ingen verdier fylles inn.
- FR3: Område (sør eller nord) utledes av `Fylke` etter R1. Mangler fylke, er området «ukjent».

**Søk og valg av anlegg (PRD 5.2)**

- FR4: Brukeren kan søke på lokalitetsnavn (delvis treff, uavhengig av store og små bokstaver) eller lokalitetsnummer.
- FR5: Treflisten viser lokalitetsnavn, lokalitetsnummer, kommune og fylke.
- FR6: Gir søket ingen treff, viser appen en melding om det.
- FR6a: Forsiden viser én setning om hva Marin er og en fargeforklaring for rød, gul, grønn og grå, hver med farge, symbol og navn. Forsiden ser lik ut ved første besøk og via «Bytt anlegg».
- FR6b: Marin husker sist viste innebygde anlegg per nettleser, og bare lokalitetsnummeret lagres. Finnes anlegget i datagrunnlaget, åpnes detaljsiden direkte med «Sist viste anlegg» og analyseuke 2026 uke 42. Ellers åpnes forsiden. Opplastede data huskes aldri.

**Analyseuke (PRD 5.3)**

- FR7: Brukeren kan velge analyseuke fra 2025 uke 1 til og med 2026 uke 42. Standard er 2026 uke 42. Uke 53 kan bare velges for ISO-år som har uke 53.
- FR8: Prognosen bruker bare tellinger til og med analyseuka. t er siste uke med telling til og med analyseuka og kan være høyst én uke eldre enn den. Er t eldre, vises «ingen ny telling» og ingen prognose.
- FR9: Statusboksen viser «Prognose regnet fra uke {uke}, {år}».

**Prognose og status (PRD 5.4)**

- FR10: Appen finner grensen for et anlegg og en uke etter R1.
- FR11: Appen beregner trend med lineær regresjon etter R2: vindu på 5 uker, minst 3 tellinger, løpende ukenummer som x-verdi og estimatet avrundet til 2 desimaler før det sammenlignes med grensen.
- FR12: Appen beregner uker til grensen med horisont 6 uker, regnet fra analyseuka. Estimatet for hver uke sammenlignes med grensen i den uka.
- FR13: Appen håndterer spesialtilfellene i R2: brudd nå, for lite data og negative estimater (settes til 0).
- FR14: Appen setter status (rød, gul, grønn, grå) og statustekst etter R4, i rekkefølgen ukjent område, ingen ny telling, brudd nå, for lite data, prognose.

**Detaljside (PRD 5.5)**

- FR15: Detaljsiden viser status med farge, symbol og tekst etter R4.
- FR15a: Under R4-teksten står én forklarende setning etter malene i EXPERIENCE.md. Retningsordet følger fortegnet på trendlinja, og grensen i setningen er grensen i den estimerte uka.
- FR15b: Statusboksen kan forstås alene i et skjermbilde. Den viser anleggsnavn, lokalitetsnummer, kommune, fylke, teksten fra FR9 og status.
- FR16: Grafen viser målte lusetall i vinduet, trendlinja forlenget til uke a + 6 og grensen per uke, som trapp når vårgrensen slår inn.
- FR17: Tabellen viser de 5 ukene i vinduet, med uke og lusetall eller «ikke telt».
- FR18: Ved rød eller gul status (unntatt brudd nå) vises estimert ISO-uke for når grensen nås, og antall uker dit regnet fra analyseuka.
- FR19: En fast tekst sier at prognosen er en enkel trendberegning og ikke en garanti, med treffandel og presisjon fra siste backtest. Mangler resultatfila, vises teksten uten tall.
- FR20: Ved grå status forklarer detaljsiden hvorfor det ikke finnes prognose.
- FR20a: Uten prognose (grå eller brudd nå) viser grafen og tabellen målte tall og grensen, men ingen trendlinje og ingen estimert uke. Ved «ingen ny telling» viser tabellen de 5 ukene før analyseuka.

**Opplasting av egne lusetall (PRD 5.6, tillegg til v1)**

- FR21: Brukeren kan laste opp en CSV-fil for ett anlegg med kolonnene `år`, `uke` og `voksne_hunnlus`, komma som skilletegn og desimalpunktum, i UTF-8 (med eller uten BOM) eller Windows-1252. Kolonnenavn leses uavhengig av store og små bokstaver. Tom verdi er uke uten telling.
- FR21b: Appen godtar også CSV med semikolon og desimalkomma (norsk Excel), med de samme tegnkodene som i FR21. Formatet finnes ut fra overskriftsraden. Kan kuttes alene. Da avvises slike filer med en feilmelding etter FR24.
- FR22: Brukeren kan laste opp et Excel-uttrekk i formatet til BarentsWatch-fila «Lakselus per fisk». Har fila flere anlegg, velger brukeren ett.
- FR23: Ved Excel med `Fylke` utleder appen området etter R1 og viser det med fylket først, for eksempel «Område: Trøndelag – grense som for sør». Brukeren velger ikke område.
- FR23a: Ved CSV, og ved Excel uten fylke, velger brukeren sør eller nord.
- FR24: Appen validerer fila og sier hva som er galt og i hvilken rad: ukjent format, manglende kolonner, år utenfor 2000 til inneværende år, uke utenfor 1–53 eller uke 53 i et år uten uke 53, negative eller ikke-numeriske lusetall, og samme uke flere ganger. Filer over 4 MB avvises, og nettleseren sjekker størrelsen før fila sendes. Ugyldige filer gir ingen prognose.
- FR25: Etter vellykket opplasting vises samme detaljside, med analyseuke lik uka på siste rad. Valgbare uker er alle ISO-uker fra første til siste rad. Intervallet i FR7 gjelder ikke.
- FR25a: Ved opplastede data står «Dine opplastede tall: {filnavn}» inne i statusboksen. «Sist viste anlegg» vises ikke.
- FR26: Opplastede data ligger bare i minnet i nettleserfanen, og serveren lagrer dem ikke. De forsvinner når fanen lukkes eller siden lastes på nytt, når brukeren forlater detaljsiden for dem, eller når en ny fil lastes opp. Tilbakeknappen fra detaljsiden går til opplastingssiden. Opplastingssiden har en lagringsnotis.

**Backtest (PRD 5.7, utviklerverktøy)**

- FR27: Et skript kjører backtesten på hele datagrunnlaget etter SK2. Status for uke a er appens status med analyseuke a, beregnet bare med data til og med a. Kryssinger og røde perioder bestemmes som i SK2.
- FR27a: Parameterne i R2 og R4 fryses før den endelige backtesten. Resultatet rapporteres uendret i README og refleksjonsrapporten, også under tersklene, og parameterne justeres ikke for å nå dem.
- FR28: Skriptet rapporterer antall kryssinger, treff, treffandel, antall varsler, presisjon og hvor mange kryssinger og varsler som er holdt utenfor. Et varsel er en uke med «✕ Varsel …», og det er fulgt av brudd hvis minst én telling i uke a + 1 til a + 4 er ≥ grensen i sin uke. Kryssinger før 2025 uke 9 og varsler etter 2026 uke 38 holdes utenfor. Resultatet skrives til fil sammen med parameterne.
- FR29: Backtesten vises ikke som egen side i appen i v1.

### Ikke-funksjonelle krav

- NFR1: Appen kan kjøres lokalt etter README, med datasettet i repoet, uten API-nøkler eller betalte kontoer. Nett trengs bare for å installere avhengigheter.
- NFR2: T1–T12 finnes som automatiske tester og består, og kan kjøres med én kommando fra README.
- NFR3: R1 testes i tillegg mot BarentsWatch-kolonnen `Lusegrense uke`, med 0 avvik.
- NFR4: Status kan forstås uten fargesyn: alltid farge, symbol og tekst sammen.
- NFR5: Grensesnittet er på norsk (bokmål). Uker vises som ISO-uker, for eksempel «uke 38, 2026».
- NFR6: Appen behandler ingen personopplysninger. Nettleseren lagrer bare lokalitetsnummeret til sist viste anlegg.
- NFR7: Appen inneholder ingen KI eller språkmodell. Prognosen er ren statistikk.
- NFR8: Detaljsiden vises på under 2 sekunder på en vanlig bærbar PC etter at appen har startet.
- NFR9: Ingen hemmeligheter eller nøkler i repoet. Kildedata i `data/`, datafila og backtestresultatet i backend-pakken, testdata i egen testmappe.
- NFR10: Automatiske tester utover T1–T12 for søk, analyseuke, opplasting (én testfil per feiltype og per godkjent format) og backtest (lite konstruert datasett regnet for hånd). Detaljsiden testes automatisk der verdien kan hentes uten nettleser. Resten kontrolleres manuelt etter en sjekkliste i README, som er en ordrett kopi av konsekvensene i PRD kap. 5.2, 5.3 og 5.5.
- NFR11: README oppgir datakilde (BarentsWatch, «Lakselus per fisk»), lisens (NLOD), nedlastingsdato (27.10.2026) og hvordan dataene ble hentet.
- NFR12: Appen er publisert på Vercel med samme funksjoner og data som lokalt, uten hemmeligheter. Adressen står i README. Opplastingen godtar høyst 4 MB fordi Vercel begrenser forespørsler til 4,5 MB.

### Tilleggskrav fra arkitekturen og briefen

**Startmal.** Arkitekturen binder ingen startmal. Utgangspunktet er strukturfrøet (mappetreet) og stack-tabellen i arkitekturen. Første story setter opp skjelettet: `backend/` som uv-prosjekt med Python 3.14 og `frontend/` med Next.js 16.4.6, TypeScript 5.9.3 og Tailwind 4.3.5.

**Regler og fasit fra briefen**

- AR1: Reglene R1–R4 i briefen er fasit for kjernen. Grensen er 0,2 i uke 16–21 (sør) og uke 21–26 (nord), ellers 0,5, og en verdi ≥ grensen er brudd. Statusteksten er ordrett R4-teksten.
- AR2: T1–T12 i briefen (R6) er fasit for testene. T5, T6, T8 og T10–T12 er kontrollert steg for steg (A4, `a4-handkontroll.md`).
- AR3: SK2 i briefen definerer kryssing, treff, rød periode, varsel og presisjon, og hvilke kryssinger og varsler som holdes utenfor. Tersklene er treffandel minst 25 % og presisjon minst 20 % (M1-C).

**Arkitekturbeslutninger (AD-1 til AD-15)**

- AR4 (AD-1): R1–R4 implementeres én gang i `marin.kjerne`, som bare importerer stdlib. En pytest sjekker importene. Inngangen `vurder(serie, omrade, analyseuke)` tar hele serien og ser selv bort fra tellinger etter analyseuka. Parameterne er konstanter i kjernen. `Lusegrense uke` brukes bare i tester. Frontend velger aldri status, trend, grense, vindu, tabellrader eller valgbare uker.
- AR5 (AD-2): Kjernen lager alle tekster som avhenger av data eller regelutfall: statustekst, forklarende setning, grå-forklaring, estimert uke, usikkerhetstekst, kryssingsetikett, tekstoppsummering og områdetekst. `kilder` lager opplastingsfeilene. Status sendes som `symbol`, `tekst` og `uke_tekst`. Testene sjekker `f"{symbol} {tekst}"` tegn for tegn mot briefen. Frontend eier bare faste tekster i `frontend/src/tekster.ts`.
- AR6 (AD-3): Pydantic-modellene i `marin.api` er kontrakten. `backend/openapi.json` committes, og en pytest feiler når den ikke stemmer. `frontend/src/api/schema.ts` genereres med openapi-typescript og redigeres aldri for hånd. Alle kall går gjennom `frontend/src/api/`. Første story i API-sporet lager modellene og tomme ruter, slik at backend og frontend kan bygges parallelt. Rutene er `GET /api/anlegg?q=`, `GET /api/anlegg/{nr}`, `GET /api/anlegg/{nr}/prognose?ar=&uke=`, `POST /api/opplasting?filnavn=` og `POST /api/prognose`.
- AR7 (AD-4): Serveren er tilstandsløs. Opplastet fil sendes som rå body (høyst 4 MB) og leses med `await request.body()`, aldri som multipart. Ingenting skrives til disk. En test laster opp en fil over 1 MB mens `tempfile` er satt til å feile.
- AR8 (AD-5): «Nå» er konstanten `SISTE_UKE = Uke(2026, 42)` og gjelder bare innebygde data. Kjernen leser aldri klokka. `inneverende_ar` sendes inn fra API-skallet.
- AR9 (AD-6): En uke er `{ar, uke}` i API-et. Kjernen avrunder med `Decimal` og `ROUND_HALF_UP` til 2 desimaler, både inndata og estimat. `round()` brukes aldri på lusetall. `format_lus`/`format_uke` (Python) og `formatLus`/`formatUke` (TypeScript) testes mot de samme vektorene i `backend/tests/data/format.json`.
- AR10 (AD-7): `status.farge ∈ {rod, gul, gronn, gra}` og `status.arsak ∈ {varsel, brudd_na, folg_med, ingen_kryssing, for_lite_data, ingen_ny_telling, ukjent_omrade}`. Frontend velger farge og stil bare fra kodene.
- AR11 (AD-8): `frontend/src/lib/husketAnlegg.ts` lagrer bare lokalitetsnummeret i `localStorage` under `marin.sistViste`, etter et vellykket `Detaljsvar` med `kilde = innebygd`. Modulen tåler at lagringen mangler eller feiler.
- AR12 (AD-9): Next.js bygges med `output: 'export'` og `trailingSlash: true`, uten route handlers, server actions, middleware, rewrites eller dynamiske ruter. Detaljsiden er `/anlegg/?nr={nr}` og `/anlegg/?opplastet=1`. Sider med `useSearchParams` pakkes i `<Suspense>`. Tre kjøremåter: utvikling (to prosesser, CORS bare i utvikling), lokalt (FastAPI monterer `frontend/out/` etter `/api`-rutene, ukjent `/api/*` gir JSON 404) og Vercel (to services, `vercel.json` med rewrites).
- AR13 (AD-10): `uv run python -m marin.forbered` lager `backend/src/marin/data/datasett.json` med sha256 av kildefilene. `uv run python -m marin.backtest` lager `backend/src/marin/data/backtest.json` med feltene `versjon`, `parametere`, `siste_uke`, `antall_kryssinger`, `antall_treff`, `antall_varsler`, `utelatt_kryssinger`, `utelatt_varsler`, `treffandel` og `presisjon`. Begge committes og leses med `importlib.resources`. Mangler backtestfila, er den ugyldig eller avviker parameterne, vises FR19 uten tall og en advarsel skrives til stderr. En pytest sjekker hashene.
- AR14 (AD-11): `marin.kjerne.modeller` eier `Uke`, `Telling`, `Serie` og `AnleggInfo`. `Serie` er sortert, har én telling per uke og gir `ValueError` ved duplikater. Område er aldri et felt i `Serie` eller `AnleggInfo`. `omrade_fra_fylke` bruker en lukket tabell over nåværende og tidligere fylkesnavn, og fylket hentes fra nyeste rad.
- AR15 (AD-12): `marin.kilder.barentswatch` er den eneste leseren for BarentsWatch-formatet. `forbered` og opplastingen bruker den. Duplikatnøkkelen er `(lokalitetsnr, år, uke)`. En test leser samme fil begge veier og sjekker at seriene er like.
- AR16 (AD-13): `POST /api/opplasting` svarer alltid HTTP 200 med `Opplastingssvar`. Har fila feil, er `anlegg` tom. CSV gir ett anlegg uten nummer og navn. Frontend sender aldri fila på nytt. `POST /api/prognose` krever `omrade ∈ {sor, nord}`. Begge prognoserutene bygger svaret med `bygg_detaljsvar`.
- AR17 (AD-14): `marin.kjerne.uker` er den eneste ISO-kalenderen. Valgbare uker og standarduke kommer fra API-et. Prognoserutene svarer 422 for uker utenfor lista. Frontend har ingen ISO-kalender.
- AR18 (AD-15): `frontend/src/lib/opplastetData.ts` holder opplastede data på modulnivå. De settes bare ved «Vis prognose» og tømmes av en lytter i rotlayouten ved ruteskifte og ved ny fil, aldri i en `useEffect`-opprydding. Mangler data på `/anlegg/?opplastet=1`, gjøres `router.replace('/opplasting/')`. Forsiden omdirigerer til husket anlegg bare første gang appen tegnes i fanen, til `/anlegg/?nr={nr}&husket=1`.

**Konvensjoner, stack og drift**

- AR19: Navngiving med norske fagord uten æ, ø og å i identifikatorer. Python `snake_case`, TypeScript `camelCase`, komponenter `PascalCase`, API-felt `snake_case`.
- AR20: Opplastingsfeil har formen `feil: [{rad, melding}]`, med radnummer som i regnearket. Backend sender de 20 første, sortert på rad, og `antall_feil`. Andre feil bruker FastAPIs `{detail}`. Ved nettverks- eller 5xx-feil viser frontend en generell feilmelding.
- AR21: Detaljsiden gjør én forespørsel per valgt analyseuke, 300 ms etter siste endring. Svar for en uke som ikke lenger er valgt, avbrytes med `AbortController`. Hele siden tegnes fra ett `Detaljsvar`.
- AR22: Ingen miljøvariabler eller hemmeligheter. `uv run pytest` kjører alle backendtester, `npm test` (Vitest) dekker `husketAnlegg`, `opplastetData`, `formatLus` og `formatUke`.
- AR23: Grafen er en egen SVG-komponent `TrendGraf` uten grafbibliotek. Den tegner bare `Detaljsvar.graf`.
- AR24: Stack med versjoner fra arkitekturen: Python 3.14, uv ≥ 0.12, FastAPI 0.163.1, Uvicorn 0.54.0, Pydantic 2.14.3, openpyxl 3.1.5, pytest 9.2.0, httpx2 2.16.2 (dev), Node ≥ 22.12, Next.js 16.4.6, React 19.3.1, TypeScript 5.9.3, Tailwind 4.3.5, openapi-typescript 7.13.0, Vitest 5.1.0.
- AR25: Publisering med Vercel Services (beta). Reserveplanen er to Vercel-prosjekter i samme repo, med API-base-URL og CORS som eneste endring.

**Føringer for rekkefølge og omfang (PRD kap. 9 og 13)**

- AR26: Første epic er kjernen (R1–R4 og SK2) og backtest-skriptet (FR27–FR28). Backtesten kjøres (A5) så snart den epicen er ferdig, før noen andre stories startes. Etterpå oppdateres PRD kap. 11, M1-C-vurderingen og eventuelt FR19.
- AR27: V1 er ferdig når prioritet 1 (kjerneflyt) og 2 (backtest) er ferdig og testet. Opplasting er et tillegg i rekkefølgen 3a Excel (FR22–FR26), 3b CSV med komma (FR21) og 3c norsk CSV (FR21b). FR21b kuttes først.
- AR28: Arbeidsdelingen mellom Fredrik og Ella (A3) avgjøres i dette steget.

### UX-designkrav

**Designtokens og layout**

- UX-DR1: Alle tokens fra DESIGN.md legges inn én gang som Tailwind `@theme` i `frontend/src/app/globals.css`: grunnpalett, statusfarger (`*-fill`, `*-on-fill`, `*-border`, `*-symbol` for rød, gul, grønn og grå), typografiroller for desktop og mobil, `rounded` og `spacing`. Bruddpunkt 600px. Systemfonter, ingen nedlasting. Bare lys modus. Komponentene bruker bare tokennavn.
- UX-DR2: Én kolonne, sentrert, maks 760px. Fast rekkefølge på detaljsiden: «Sist viste anlegg» (bare ved husket anlegg), tittel med sted, analyseukevelger, statusboks, graf med tegnforklaring og tekstoppsummering, ukestabell, usikkerhetstekst. Avstander fra spacing-tokens for desktop og mobil.
- UX-DR3: Siden fungerer ved 320 CSS-px bredde og 400 % zoom uten vannrett rulling, og med økt tekstavstand (WCAG 1.4.12). Toppfeltet bryter til to linjer ved behov. Statusmerker har minstebredde, ikke fast bredde.

**Komponenter**

- UX-DR4: Toppfelt. «Marin» som logo til venstre, som går til forsiden. Desktop: søkeskjema (etikett «Søk anlegg» visuelt skjult, felt og sekundærknapp «Søk») og «Bytt anlegg». Mobil: «Søk / bytt», som går til forsiden med søkefeltet i fokus. «Last opp egne tall» på begge bredder. På forsiden vises bare logo og «Last opp egne tall». Søk fra toppfeltet viser treflisten på forsiden.
- UX-DR5: Statusboks i fire varianter (`status-box-red|yellow|green|grey`), den eneste fulle fargeflaten. Innhold ovenfra: anleggsnavn, linja med lokalitetsnr., kommune og fylke, «Prognose regnet fra uke X, ÅÅÅÅ», symbolsirkel og R4-tekst (+ `uke_tekst`) på samme linje, og én forklarende setning. Gul har mørk kant. Grå er hvit med stiplet kant. Ingen interaktive elementer. Hele boksen er synlig uten rulling på desktop ved 100 % zoom, og den står over grafen på mobil.
- UX-DR6: Symbolsirkel: hvit sirkel på 52px (46px på mobil) med symbolet i minst 32px i statusens `*-symbol`-farge. Gul sirkel har kant, grå sirkel har stiplet kant. Symbolet har `aria-hidden`.
- UX-DR7: Statusboksen er en navngitt region («Status»). Bare statusoverskriften (R4-tekst + `uke_tekst`) er `aria-live="polite"`. Elementet finnes i siden fra start, og bare teksten byttes.
- UX-DR8: Lastetilstand i statusboksens plass: «Regner ut prognose …» på hvit flate med 1px heltrukken kant, uten statusfarge, stipling eller symbol. Den leses ikke opp og har ingen animasjon. Tittel og analyseukevelger vises med en gang.
- UX-DR9: Linja «Dine opplastede tall: {filnavn}» står inne i statusboksen under stedslinja, med «Dine opplastede tall:» i fet skrift og samme tekstfarge som boksen.
- UX-DR10: Statusmerke (pille): hvit bakgrunn, tynn kant, rund statusmarkør på 10px i statusens fyllfarge, symbol i statusens symbolfarge, og tekst. Størrelse `pill` (13px) eller `pill-xs` (12px). Ikke interaktivt. Gul får mørk kant, grå får stiplet kant.
- UX-DR11: Analyseukevelger: vanlig nedtrekksliste med etiketten «Analyseuke», verdier som «uke 42, 2026», nyeste først og minst 44px høy. Endringen gjelder med en gang, uten «Oppdater»-knapp. Anlegget og rulleposisjonen beholdes.
- UX-DR12: Søkefelt med knappen «Søk». Etiketten «Søk anlegg» er synlig på forsiden og visuelt skjult i toppfeltet. Plassholder «Søk anlegg – navn eller lokalitetsnr.» (desktop) og «Søk navn eller nr.» (mobil). Søket kjøres ved Enter eller knappen, ikke for hvert tastetrykk. Tomt søk gjør ingenting.
- UX-DR13: Trefliste: én rad per anlegg med navnet i vekt 600 og «Lokalitetsnr. 12345 · Hitra, Trøndelag» under. Hele raden er klikkbar og minst 44px høy. Sortert alfabetisk, vises også ved ett treff, ingen statusfarge. Aktiv rad ved tastaturnavigering får `accent-tint`.
- UX-DR14: Ingen treff: «Fant ingen anlegg som passer «{søk}». Søk på lokalitetsnavn eller lokalitetsnummer.» under søkefeltet. Søketeksten beholdes. Meldingen leses opp via `aria-live`.
- UX-DR15: Graf (`TrendGraf`): horisontale rutenettlinjer, målte punkter i aksentfarge med tynn linje mellom tellinger, hule punkter med «ikke telt» for uker uten telling, trendlinje heltrukken gjennom vinduet og stiplet fram i tid, grenselinje på 2px som trapp med etiketten «Grense 0,5», prikket analyseukelinje med «Prognose →» og kryssingsmarkør med etikett («✕ Varsel uke 44» eller «! Følg med uke 46»). Gul markør bruker mørk gulkant. X-aksen går fra første uke i vinduet til a + 6.
- UX-DR16: Grafen har tegnforklaringen «Målt lusetall», «Trend (stiplet = prognose)» og «Grense per uke». Uten prognose faller trendoppføringen bort. Ved ukjent område vises ingen grenselinje, og tegnforklaringen sier «Grensen er ukjent».
- UX-DR17: All tekst i grafen er minst 13 CSS-px slik den vises, ved alle bredder, og følger tekstzoom. Tekst i en SVG som skaleres med `viewBox`, oppfyller ikke kravet.
- UX-DR18: Grafen har `role="img"` med innholdet i SVG-en skjult for skjermleser. Under tegnforklaringen står den synlige tekstoppsummeringen fra API-et som figurtekst.
- UX-DR19: Ukestabell med kolonnene «Uke», «Voksne hunnlus» (høyrejustert, tabulære sifre) og «Merknad». Overskrift «De siste 5 ukene», eller «De 5 ukene før analyseuka» ved «ingen ny telling». Eldste uke øverst. Uke uten telling viser «–» og merket «– Ikke telt». Siste telling merkes «Siste telling». Ingen vannrett rulling på mobil.
- UX-DR20: Usikkerhetstekst nederst på detaljsiden i `meta` og sekundærfarge, med en tynn strek over (40px over, 20px til teksten). Vises for alle statuser.
- UX-DR21: Fargeforklaring på forsiden under overskriften «Statusfargene»: fire merker «✕ Rød», «! Gul», «✓ Grønn» og «– Grå», hvert med linjene «Brudd nå, eller grensen nås om 1–3 uker.», «Grensen kan nås om 4–6 uker.», «Ingen kryssing ventet innen 6 uker.» og «Ingen prognose: for lite data, ingen ny telling eller ukjent område.» Ingen fulle fargeflater.
- UX-DR22: Knapper: primær (fylt aksent) og sekundær (hvit med aksentkant), minst 44px høye. Én primærknapp per flate. Deaktivert stil (hvit, grå kant, sekundærtekst) bare mens fila leses.
- UX-DR23: Lenker i aksentfarge og understreket. Synlig fokusmarkering (2px aksent med 2px avstand) på alle interaktive elementer.

**Opplasting**

- UX-DR24: Opplastingsskjema: H1 «Last opp egne tall», ekte filfelt med etiketten «Fil», hjelpeteksten «CSV med kolonnene år, uke og voksne_hunnlus, eller Excel-uttrekk fra BarentsWatch.» og knappen «Velg fil». Deretter anleggsvalg («Velg anlegg», radioknapper med samme radoppsett som treflisten), områdevalg (sør/nord med hjelpeteksten «Nord: Nordland, Troms og Finnmark. Sør: alle andre fylker.», ingen forhåndsvalg) eller utledet område som tekst, og primærknappen «Vis prognose». Radioradene er klikkbare over hele raden og minst 44px høye. Lagringsnotisen «Fila lagres ikke. Tallene forsvinner når du går bort fra prognosen for dem, lukker fanen eller laster opp en ny fil.»
- UX-DR25: Mens fila leses, står «Leser fila …» under filvelgeren i en `role="status"`-region som finnes fra start, og «Vis prognose» er deaktivert.
- UX-DR26: Feilmelding: hvit boks med 2px mørk kant over skjemaet, uten statusrødt. Overskriften «Fila har N feil. Marin har ikke laget noen prognose.» kan få fokus. Feilene listes én per linje. Er det flere enn 20, vises de 20 første og «… og N feil til. Rett feilene over og se etter samme feil i resten av fila.» Mens fila har feil, vises bare feilmeldingen og filvelgeren.
- UX-DR27: Skjemafeil: filfeltet har `aria-describedby` til hjelpeteksten, og ved feil `aria-invalid="true"` og kobling til feilmeldingen. Trykkes «Vis prognose» uten valg, vises «Velg område: sør eller nord.» eller «Velg ett av anleggene i fila.» under gruppens overskrift, gruppen får `aria-invalid`, og fokus flyttes til første radioknapp i første gruppe med feil. Feil i fila flytter fokus til feiloverskriften. Etter rettet fil flyttes fokus til neste steg. Feil meldes med fokus, aldri med `role="alert"`. Felt med feil får 2px mørk kant.
- UX-DR28: Feiltekstene i `kilder` følger ordlyden i EXPERIENCE.md (State Patterns): ukjent format, manglende kolonner, år utenfor området, uke utenfor området eller uke 53, ugyldig lusetall, feil desimaltegn og duplikat. Kuttes FR21b, må teksten for ukjent format endres, fordi den nevner semikolonformatet.

**Tekster fra backend og frontend**

- UX-DR29: Kjernen lager den forklarende setningen etter malene i EXPERIENCE.md for alle sju statusene, med entall «1 uke» (T12) og året tatt med når uka ligger i et annet år enn analyseuka.
- UX-DR30: Kjernen lager tekstoppsummeringen under grafen etter malene for seks tilstander (prognose med kryssing, uten kryssing, brudd nå, for lite data, ingen ny telling, ukjent område). Grensen skrives som trapp når den endres i vinduet. Uker uten telling skrives «ikke telt».
- UX-DR31: Faste tekster i `frontend/src/tekster.ts`: forsideintro («Marin viser om lusetallene på anlegget ditt er på vei mot lusegrensen, og omtrent når grensen kan nås.»), «Finn anlegget ditt», «Statusfargene», etiketter, plassholdere, knapper, lagringsnotis, lastemeldinger, «Sist viste anlegg» og «Prognose regnet fra {uke}». Desimalkomma og «uke 42, 2026» overalt.

**Tilgjengelighet og kontroll**

- UX-DR32: Siden har `lang="nb"`. Alt kan brukes med tastatur, og Tab-rekkefølgen følger leserekkefølgen. Ingen funksjon bare ved hover. Trykkflater minst 44 × 44px på mobil. På desktop er felt og knapper minst 44px høye og tekstlenker minst 24 × 24px.
- UX-DR33: README-sjekklisten (NFR10) får i tillegg kontroll av de fire statusboksene i gråtoner og med deuteranopi-simulering, og kontroll ved 320px, 600px, 400 % zoom og 200 % tekstzoom.

**Ikke i v1:** mørk modus, full statusfarge utenfor statusboksen, samlet oversikt, dra-og-slipp, dele- eller eksportknapp, varsler.

### Dekningskart for FR

| FR | Epic | Kort |
|---|---|---|
| FR1 | Epic 1 | Utdraget til og med 2026 uke 42 blir `datasett.json` |
| FR2 | Epic 1 | Uke med telling, ingen utfylling |
| FR3 | Epic 1 | Område fra fylke |
| FR4 | Epic 2 | Søk på navn eller nummer |
| FR5 | Epic 2 | Treflisten med nummer, kommune og fylke |
| FR6 | Epic 2 | Melding ved ingen treff |
| FR6a | Epic 2 | Forside med intro og fargeforklaring |
| FR6b | Epic 2 | Husket anlegg |
| FR7 | Epic 2 | Valg av analyseuke |
| FR8 | Epic 1 og 2 | Regelen i kjernen (Epic 1), synlig når analyseuka velges (Epic 2) |
| FR9 | Epic 2 | «Prognose regnet fra» i statusboksen |
| FR10 | Epic 1 | Grense etter R1 |
| FR11 | Epic 1 | Trend med lineær regresjon |
| FR12 | Epic 1 | Uker til grensen fra analyseuka |
| FR13 | Epic 1 | Spesialtilfellene i R2 |
| FR14 | Epic 1 | Status og statustekst etter R4 |
| FR15 | Epic 2 | Status med farge, symbol og tekst |
| FR15a | Epic 2 | Forklarende setning |
| FR15b | Epic 2 | Statusboksen alene i et skjermbilde |
| FR16 | Epic 2 | Graf |
| FR17 | Epic 2 | Ukestabell |
| FR18 | Epic 2 | Estimert uke |
| FR19 | Epic 2 | Usikkerhetstekst med tall fra backtesten |
| FR20 | Epic 2 | Forklaring ved grå status |
| FR20a | Epic 2 | Graf og tabell uten prognose |
| FR21 | Epic 3 | CSV med komma (3b) |
| FR21b | Epic 3 | Norsk CSV (3c, kan kuttes) |
| FR22 | Epic 3 | Excel fra BarentsWatch (3a) |
| FR23 | Epic 3 | Område utledet av fylke |
| FR23a | Epic 3 | Brukeren velger område |
| FR24 | Epic 3 | Validering og feilmeldinger |
| FR25 | Epic 3 | Detaljside for opplastede data |
| FR25a | Epic 3 | «Dine opplastede tall» i statusboksen |
| FR26 | Epic 3 | Ingen lagring av opplastede data |
| FR27 | Epic 1 | Backtest-skript etter SK2 |
| FR27a | Epic 1 | Parametere fryst, resultat rapportert uendret |
| FR28 | Epic 1 | Treffandel, presisjon og utelatte tilfeller til `backtest.json` |
| FR29 | Epic 1 | Ingen side for backtesten |

| NFR | Epic |
|---|---|
| NFR1 | Epic 2 (lokal kjøring med én uvicorn) |
| NFR2 | Epic 1 |
| NFR3 | Epic 1 |
| NFR4 | Epic 2 |
| NFR5 | Epic 2 (tekster fra kjernen også i Epic 1) |
| NFR6 | Epic 2 og 3 |
| NFR7 | Epic 1 |
| NFR8 | Epic 2 |
| NFR9 | Epic 1 |
| NFR10 | Alle: backtestdata i Epic 1, søk, analyseuke og sjekkliste i Epic 2, testfiler for opplasting i Epic 3 |
| NFR11 | Epic 1 |
| NFR12 | Epic 2 (tidlig publisering), Epic 3 (4 MB-grensen) |

## Epic-liste

### Epic 1: Prognose som er testet og målt

Gruppen har en prognose som følger R1–R4 og består T1–T12 og NFR3, og vet treffandel og presisjon på hele datagrunnlaget. Tallene avgjør M1-C før noe av brukergrensesnittet bygges.

**FR som dekkes:** FR1, FR2, FR3, FR8, FR10, FR11, FR12, FR13, FR14, FR27, FR27a, FR28, FR29
**NFR:** NFR2, NFR3, NFR7, NFR9, NFR11, NFR10 (backtestdata)
**Tilleggskrav:** AR1–AR4, AR8, AR9, AR10, AR13, AR14, AR15, AR17, AR19, AR22, AR24 (backend), AR26

Innhold: backend-skjelett, kjernen (modeller, ISO-uker, R1–R4 og statustekst), BarentsWatch-leseren, `forbered` → `datasett.json`, SK2-funksjonene og `backtest` → `backtest.json`. Epicen deler seg i et dataspor (leser, `forbered`, NFR3) og et regelspor (R1–R4, T1–T12, SK2 og backtest). Den avsluttes med A5: backtesten kjøres, tallene rapporteres uendret, og PRD kap. 11 og M1-C-vurderingen oppdateres. Ingen stories i Epic 2 eller 3 starter før A5 er gjort (AR26).

### Epic 2: Kari ser status for anlegget sitt (J1 og J2)

Kari finner anlegget sitt og ser status, graf, ukestabell og usikkerhetstekst. Hun kan bytte analyseuke for å se hvordan varselet ville sett ut tidligere, og Marin husker anlegget til neste gang. Appen kjører lokalt etter README og er publisert på Vercel.

**FR som dekkes:** FR4, FR5, FR6, FR6a, FR6b, FR7, FR8 (i grensesnittet), FR9, FR15, FR15a, FR15b, FR16, FR17, FR18, FR19, FR20, FR20a
**NFR:** NFR1, NFR4, NFR5, NFR6, NFR8, NFR10 (søk, analyseuke og sjekkliste), NFR12
**Tilleggskrav:** AR5, AR6, AR9 (frontend), AR10, AR11, AR12, AR17, AR18 (husket anlegg), AR20, AR21, AR23, AR24 (frontend), AR25
**UX:** UX-DR1–UX-DR8, UX-DR10–UX-DR23, UX-DR29–UX-DR33

Innhold: API-kontrakten først (AD-3: Pydantic-modeller, tomme ruter og generert `schema.ts`), slik at backend og frontend kan bygges parallelt. Deretter frontend-skjelett med tokens og en tidlig publisering på Vercel, så beta-risikoen viser seg tidlig. Så forside og søk, detaljsiden, grafen, analyseuka, usikkerhetsteksten og husket anlegg. Usikkerhetsteksten bruker ordlyden i EXPERIENCE.md («varslet Marin rødt … røde varsler»), avgjort 2026-11-18.

### Epic 3: Kari får prognose på egne tall (J3, tillegg)

Kari laster opp egne lusetall fra Excel eller CSV og får samme detaljside som for anleggene i utdraget, uten at dataene lagres.

**FR som dekkes:** FR21, FR21b, FR22, FR23, FR23a, FR24, FR25, FR25a, FR26
**NFR:** NFR6, NFR10 (testfiler for opplasting), NFR12 (4 MB)
**Tilleggskrav:** AR7, AR15, AR16, AR18, AR20, AR27
**UX:** UX-DR9, UX-DR24–UX-DR28

Innhold: storyene bygges i rekkefølgen 3a Excel fra BarentsWatch (FR22, FR23, FR23a, FR24, FR25, FR25a, FR26), 3b CSV med komma (FR21) og 3c norsk CSV (FR21b). 3c er siste story og kuttes først. V1 kan leveres uten denne epicen.

### Avhengigheter og arbeidsdeling

Epic 2 bygger på Epic 1 (kjernen, `datasett.json` og `backtest.json`). Epic 3 bygger på Epic 1 og 2 (leseren, kjernen og detaljsiden). Ingen epic trenger en senere epic for å virke.

Arbeidsdelingen mellom Fredrik og Ella (A3) avgjøres per story når sprintplanen lages (avgjort 2026-11-18).

## Epic 1: Prognose som er testet og målt

Gruppen har en prognose som følger R1–R4 og består T1–T12 og NFR3, og vet treffandel og presisjon på hele datagrunnlaget. Tallene avgjør M1-C før noe av brukergrensesnittet bygges. Etter Story 1.2 kan Story 1.3 (dataspor) og Story 1.4 (regelspor) bygges parallelt.

### Story 1.1: Grunnmur for backend og kjerne

Som utvikler i gruppen,
vil jeg ha et backend-prosjekt med kjernens typer, ISO-kalender, avrunding og formatering,
slik at regelstoriene bygger på én felles form for uker og tall (AD-5, AD-6, AD-11, AD-14).

**Akseptansekriterier:**

**Gitt** et nytt klon av repoet
**Når** jeg kjører `uv sync` og `uv run pytest` i `backend/`
**Så** kjører testene og består
**Og** README beskriver de to kommandoene (NFR2), og mappene følger strukturfrøet i arkitekturen (`backend/src/marin/kjerne/`, `backend/tests/data/`, `.python-version` med 3.14)

**Gitt** modulen `marin.kjerne.modeller`
**Når** den importeres
**Så** finnes `Uke(ar, uke)`, `Telling(uke, verdi: Decimal | None)`, `Serie(tellinger)` og `AnleggInfo(lokalitetsnr, navn, kommune, fylke)`, der alle feltene i `AnleggInfo` kan være tomme
**Og** område er ikke et felt i noen av dem (AD-11)

**Gitt** tellinger som ikke er sortert
**Når** en `Serie` lages
**Så** er tellingene sortert stigende, og serien har ingen uker som ikke fantes i inndata
**Og** to tellinger for samme uke, eller en ugyldig uke (uke 0, uke 54 eller 2025 uke 53), gir `ValueError`

**Gitt** en telling med verdien 0,125
**Når** den lages
**Så** lagres 0,13 som `Decimal` (avrundet med `ROUND_HALF_UP`)
**Og** Pythons `round()` brukes ikke på lusetall noe sted i kjernen

**Gitt** ISO-kalenderen i `marin.kjerne.uker`
**Når** den testes
**Så** er `har_uke_53(2025)` usann og `har_uke_53(2026)` sann
**Og** `neste(Uke(2025, 52))` er `Uke(2026, 1)`, og `pluss(Uke(2025, 50), 3)` er `Uke(2026, 1)`
**Og** løpende ukenummer for 2025 uke 50, 51, 52 og 2026 uke 1, 2 er fem påfølgende heltall (T12)
**Og** `alle_uker(Uke(2025, 1), SISTE_UKE)` gir 94 uker

**Gitt** kjernen
**Når** den leses
**Så** er `SISTE_UKE = Uke(2026, 42)` en konstant, og ingen modul i kjernen leser klokka (AD-5)

**Gitt** testvektorene i `backend/tests/data/format.json`
**Når** `format_lus` og `format_uke` testes mot dem
**Så** blir 0,06 til «0,06», 0,5 som lusetall til «0,50», og `Uke(2026, 42)` til «uke 42, 2026»
**Og** vektorene inneholder også grensene, som skrives «0,5» og «0,2» (NFR5)

**Gitt** alle moduler i `marin.kjerne`
**Når** importtesten kjører
**Så** feiler den hvis en modul importerer noe annet enn stdlib og `marin.kjerne` (AD-1)

### Story 1.2: Lusegrense og område (R1)

Som utvikler i gruppen,
vil jeg at kjernen finner gjeldende grense for et område og en ISO-uke,
slik at prognosen sammenlignes med riktig grense (FR3, FR10).

**Akseptansekriterier:**

**Gitt** område og ISO-uke
**Når** `grense(omrade, uke)` kalles
**Så** gir sør uke 21 grensen 0,2 (T1), sør uke 22 grensen 0,5 (T2), nord uke 21 grensen 0,2 (T3) og nord uke 20 grensen 0,5 (T4)
**Og** sør uke 15 gir 0,5, sør uke 16 gir 0,2, nord uke 26 gir 0,2 og nord uke 27 gir 0,5

**Gitt** område `ukjent`
**Når** `grense` kalles
**Så** gir den ingen grense (`None`)

**Gitt** en verdi og en grense
**Når** kjernen avgjør om verdien er brudd
**Så** er 0,50 mot 0,5 brudd og 0,49 mot 0,5 ikke brudd (R1: verdi ≥ grensen er brudd)

**Gitt** et fylkesnavn
**Når** `omrade_fra_fylke(fylke)` kalles
**Så** gir Nordland, Troms, Finnmark og det tidligere «Troms og Finnmark» `nord`
**Og** Trøndelag, Nord-Trøndelag, Sør-Trøndelag og alle andre nåværende og tidligere fylker i den lukkede tabellen gir `sor`
**Og** tomt fylke, `None` eller et navn som ikke står i tabellen gir `ukjent` (AD-11)

**Gitt** testene for T1–T4
**Når** `uv run pytest` kjører
**Så** er de navngitt etter T1–T4 og består (NFR2)

### Story 1.3: Datasett fra BarentsWatch-utdraget

Som gruppe,
vil vi gjøre BarentsWatch-utdraget om til en kompakt datafil i backend-pakken,
slik at appen og backtesten leser de samme dataene raskt, uten å lese Excel når de kjører (FR1, FR2, FR3, AD-10, AD-12).

**Akseptansekriterier:**

**Gitt** Excel-bytes i formatet «Lakselus per fisk»
**Når** `marin.kilder.barentswatch` leser dem
**Så** gir den en liste med `(AnleggInfo, Serie)` og en liste med feil
**Og** arknavn, kolonnenavn og typer står bare i denne modulen

**Gitt** en rad uten verdi i `Voksne hunnlus`
**Når** fila leses
**Så** blir uka en telling med verdien `None`, og ingen verdi fylles inn (FR2)

**Gitt** et anlegg med ulikt fylke i ulike rader
**Når** fila leses
**Så** får `AnleggInfo` fylket fra nyeste rad (AD-11)

**Gitt** to rader med samme lokalitetsnummer, år og uke
**Når** fila leses
**Så** gir leseren en feil for duplikatet (AD-12)

**Gitt** xlsx-filene i `data/barentswatch/`
**Når** `uv run python -m marin.forbered` kjøres
**Så** skrives `backend/src/marin/data/datasett.json` med alle anlegg og tellinger fra 2025 uke 1 til og med 2026 uke 42
**Og** ingen uker etter 2026 uke 42 er med (FR1)
**Og** fila inneholder sha256 for hver kildefil
**Og** skriptet skriver antall anlegg og tellinger til terminalen, og stopper med en feilmelding hvis leseren gir én eller flere feil
**Og** stiene regnes fra pakken med `importlib.resources`, ikke fra arbeidsmappa

**Gitt** `datasett.json` og xlsx-filene
**Når** hashtesten kjører
**Så** feiler den hvis hashene ikke stemmer med filene

**Gitt** kolonnen `Lusegrense uke` i xlsx-filene
**Når** NFR3-testen leser den direkte fra filene
**Så** gir `grense(omrade_fra_fylke(fylke), uke)` samme grense i alle rader, med 0 avvik
**Og** rader der BarentsWatch oppgir grensen som «Ukjent», gir område `ukjent`
**Og** alle fylkesnavn i utdraget gir `sor` eller `nord`, unntatt for anlegg uten fylke

**Gitt** README
**Når** den leses
**Så** oppgir den datakilden (BarentsWatch, «Lakselus per fisk»), lisens (NLOD), nedlastingsdato (27.10.2026), hvordan dataene ble hentet og hvordan `forbered` kjøres (NFR11)
**Og** kildedataene ligger i `data/`, datafila i backend-pakken og testdata i `backend/tests/data/` (NFR9)

### Story 1.4: Trend og uker til grensen (R2 og R3)

Som utvikler i gruppen,
vil jeg at kjernen beregner trendlinja og uker til grensen etter R2 og R3,
slik at prognosen gir de samme tallene som fasiten i briefen (FR8, FR11, FR12, FR13).

**Akseptansekriterier:**

**Gitt** en serie og en analyseuke a
**Når** vinduet bestemmes
**Så** er t siste uke med telling til og med a, og vinduet er uke t − 4 til og med t
**Og** tellinger etter a brukes ikke (FR8)

**Gitt** tellingene i vinduet
**Når** trendlinja beregnes
**Så** brukes lineær regresjon med løpende ukenummer som x-verdi og bare ukene med telling
**Og** beregningen bruker ikke flyttall, og bare stdlib (NFR7)

**Gitt** fasiten i `briefs/brief-Marin-2026-09-17/a4-handkontroll.md`
**Når** testene for T5, T6, T8 og T12 kjører
**Så** gir T5 stigningen 0,06 og estimatene 0,48 i uke 37 og 0,54 i uke 38
**Og** T6 gir stigningen 0,02 og estimatene 0,20 i uke 15 og 0,22 i uke 16
**Og** T8 gir stigningen 0,04 per uke (ikke 0,08), og estimatene 0,48 i uke 43 og 0,52 i uke 44
**Og** T12 gir stigningen 0,04 og estimatet nøyaktig 0,50 i 2026 uke 3

**Gitt** et estimat med flere enn 2 desimaler
**Når** det sammenlignes med grensen
**Så** er det først avrundet til 2 desimaler med halvdeler opp

**Gitt** et anlegg i sør med tellingene 0,40 / 0,30 / 0,20 / 0,10 / 0,00 i uke 30–34 og analyseuke 34
**Når** estimatet for uke 35 beregnes
**Så** er det 0,00 og ikke −0,10 (FR13)

**Gitt** en trendlinje og analyseuke a
**Når** uker til grensen beregnes
**Så** er resultatet den første k fra 1 til 6 der estimatet i uke a + k er ≥ grensen i uke a + k
**Og** T5 gir 4 (uke 38), T6 gir 2 (uke 16), og T10 med analyseuke 41 gir 3 (uke 44, regnet fra analyseuka og ikke fra siste telling)
**Og** finnes ingen slik k, er resultatet «ingen kryssing innen 6 uker»
**Og** en test viser at T6 ville gitt ingen kryssing hvis grensen var 0,5 i alle ukene, og at kjernen derfor bruker grensen i hver uke (R3)

### Story 1.5: Status etter R4

Som utvikler i gruppen,
vil jeg ha én inngang, `vurder(serie, omrade, analyseuke)`, som gir status og statustekst etter R4,
slik at appen og backtesten alltid får samme svar (FR8, FR13, FR14, AD-1, AD-2, AD-7).

**Akseptansekriterier:**

**Gitt** at flere betingelser gjelder samtidig
**Når** `vurder` setter status
**Så** gjelder den første i rekkefølgen ukjent område, ingen ny telling, brudd nå, for lite data, prognose

**Gitt** en vurdering
**Når** resultatet leses
**Så** har det `farge` (`rod`, `gul`, `gronn` eller `gra`) og `arsak` (`varsel`, `brudd_na`, `folg_med`, `ingen_kryssing`, `for_lite_data`, `ingen_ny_telling` eller `ukjent_omrade`) (AD-7)
**Og** `symbol` er «✕», «!», «✓», «–» eller «?», `tekst` er R4-teksten uten symbol, og `uke_tekst` er «(uke Y)» ved varsel og følg med, ellers `null` (AD-2)
**Og** resultatet har `uker_til` og `estimert_uke` ved varsel og følg med, og ingen av dem ved grønn, grå eller brudd nå (FR18)
**Og** uker i statusteksten skrives med år når uka ligger i et annet år enn analyseuka, for eksempel «(uke 1, 2027)» og «– Ingen ny telling siden uke 50, 2025» med analyseuke 2026 uke 1 (EXPERIENCE.md, avgjort 2026-11-18). Ellers står bare ukenummeret, som i T10

**Gitt** T1–T12 i briefen
**Når** `uv run pytest` kjører
**Så** finnes alle tolv som automatiske tester og består (NFR2)
**Og** for T5–T12 er `f"{symbol} {tekst}"` tegn for tegn lik briefen: T5 og T8 «! Følg med: grensen kan nås om 4 uker», T6 «✕ Varsel: grensen nås om 2 uker», T7 «? Ukjent område: grensen kan ikke bestemmes», T9 «– For lite data», T10 med analyseuke 42 «– Ingen ny telling siden uke 40», T10 med analyseuke 41 «✕ Varsel: grensen nås om 3 uker», T11 «✕ Brudd nå» og T12 «✕ Varsel: grensen nås om 1 uke»

**Gitt** et anlegg i sør med 0,10 i alle ukene 36–40 og analyseuke 40
**Når** `vurder` kalles
**Så** er status grønn med teksten «✓ Ingen kryssing ventet innen 6 uker»

**Gitt** et anlegg i sør med telling 0,30 i uke 15, ingen telling i uke 16 og analyseuke 16
**Når** `vurder` kalles
**Så** er status «✕ Brudd nå», fordi siste verdi sammenlignes med grensen i analyseuka (0,2) og ikke i uke 15

**Gitt** tellingene fra T5 og en ekstra telling 0,90 i uke 36
**Når** `vurder` kalles med analyseuke 34
**Så** er svaret identisk med svaret uten tellingen i uke 36 (gul, grensen nås om 4 uker) (FR8)
**Og** med analyseuke 36 er status «✕ Brudd nå»

**Gitt** inngangen `vurder`
**Når** den kalles
**Så** tar den hele serien og ser selv bort fra tellinger etter analyseuka, og kallerne kutter aldri serien (AD-1)
**Og** vindu (5), minste antall tellinger (3), horisont (6) og rød ved 0–3 uker (brudd nå er 0 uker) er konstanter i kjernen som ikke kan overstyres med argumenter (FR27a)

### Story 1.6: Backtest etter SK2

Som gruppe,
vil vi ha et skript som måler treffandel og presisjon på hele datagrunnlaget etter SK2,
slik at vi vet hvor godt prognosen varsler brudd (FR27, FR27a, FR28, FR29).

**Akseptansekriterier:**

**Gitt** et anlegg og en analyseuke a fra 2025 uke 1 til `SISTE_UKE`
**Når** backtesten bestemmer status for a
**Så** er statusen svaret fra `vurder(hele serien, omrade, a)`, og backtesten kutter aldri serien selv (AD-1)

**Gitt** en uke w med telling
**Når** backtesten avgjør om w er en grensekryssing
**Så** er w en kryssing når verdien er ≥ grensen i uke w, og forrige telling (i uke w − 1, ellers w − 2) var under grensen i sin uke
**Og** har verken uke w − 1 eller w − 2 telling, er w ikke en kryssing

**Gitt** en kryssing i uke w
**Når** backtesten avgjør om den er et treff
**Så** er den et treff når den sammenhengende perioden med rød status (både varsel og brudd nå, avgjort 2026-11-18) som slutter i uke w − 1, begynte i uke w − 4, w − 3 eller w − 2
**Og** alle andre statuser, også grå, bryter en rød periode
**Og** rød status bare i uke w − 1, en periode som begynte i w − 5 eller tidligere, eller ingen rød status i w − 1, er ikke treff

**Gitt** en uke a med årsak `varsel` («✕ Varsel …», ikke «✕ Brudd nå»)
**Når** backtesten avgjør om varselet ble fulgt av brudd
**Så** er det fulgt av brudd når minst én telling i uke a + 1 til a + 4 er ≥ grensen i sin uke

**Gitt** kryssinger før 2025 uke 9 og varsler etter 2026 uke 38
**Når** treffandel og presisjon regnes
**Så** er de holdt utenfor andelene, og antallet står i `utelatt_kryssinger` og `utelatt_varsler`
**Og** anlegg med ukjent område gir ingen kryssinger og ingen varsler, fordi grensen ikke kan bestemmes

**Gitt** et lite, konstruert datasett i `backend/tests/data/` med forventede tall regnet ut for hånd av gruppen (NFR10)
**Når** testen kjører SK2-funksjonene på det
**Så** gir de riktig antall kryssinger, treff, varsler, varsler fulgt av brudd og utelatte
**Og** datasettet har minst ett treff, én kryssing med rød status bare uka før, én kryssing der den røde perioden begynte 5 uker før, én uke med brudd etter to uker uten telling, ett varsel fulgt av brudd, ett varsel uten brudd, én kryssing før 2025 uke 9 og ett varsel etter 2026 uke 38

**Gitt** `datasett.json`
**Når** `uv run python -m marin.backtest` kjøres
**Så** skrives `backend/src/marin/data/backtest.json` med feltene `versjon`, `parametere`, `siste_uke`, `antall_kryssinger`, `antall_treff`, `antall_varsler`, `utelatt_kryssinger`, `utelatt_varsler`, `treffandel` og `presisjon`, der andelene er tall fra 0 til 1 (AD-10)
**Og** `parametere` er kjernens konstanter, og resultatet skrives også til terminalen
**Og** SK2-funksjonene ligger i kjernen, og skriptet er bare et skall som leser og skriver filer

**Gitt** backtesten
**Når** den er ferdig
**Så** finnes den bare som skript, uten egen rute i API-et eller egen side (FR29)

### Story 1.7: Første backtestkjøring og rapport (A5)

Som gruppe,
vil vi kjøre backtesten med frosne parametere og rapportere resultatet uendret,
slik at vi vet om M1 holder før vi bygger brukergrensesnittet (A5, FR27a, AR26).

**Akseptansekriterier:**

**Gitt** at Story 1.1–1.6 er ferdige og `uv run pytest` består
**Når** backtesten kjøres for første gang
**Så** er parameterne de samme som i R2 og R4 (vindu 5, minst 3 tellinger, horisont 6, rød ved 0–3 uker, der brudd nå er 0 uker)
**Og** parameterne endres ikke etter at resultatet er sett (FR27a)

**Gitt** resultatet
**Når** det rapporteres
**Så** er `backtest.json` committet
**Og** README har en seksjon med antall kryssinger, treff, treffandel, antall varsler, presisjon, utelatte kryssinger og varsler, parameterne og datoen for kjøringen, uendret også om treffandelen er under 25 % eller presisjonen under 20 %

**Gitt** de nye tallene
**Når** PRD-en oppdateres
**Så** har kap. 11 («Treffsikkerhet») de nye tallene i stedet for skissen fra addendumet
**Og** er treffandelen under 25 % eller presisjonen under 20 %, er reaksjonen etter M1-C beskrevet i README og PRD-en
**Og** forskjellen fra skissen (omtrent 29 % treff og 14 % presisjon) er ført i `issues.md` som punkt for refleksjonsrapporten

**Gitt** at resultatet påvirker FR19 eller storyene i Epic 2
**Når** Story 1.7 avsluttes
**Så** er de oppdatert før Epic 2 starter
**Og** ingen stories i Epic 2 eller 3 er startet før denne storyen er ferdig (AR26)

## Epic 2: Kari ser status for anlegget sitt (J1 og J2)

Kari finner anlegget sitt og ser status, graf, ukestabell og usikkerhetstekst. Hun kan bytte analyseuke for å se hvordan varselet ville sett ut tidligere, og Marin husker anlegget til neste gang. Appen kjører lokalt etter README og er publisert på Vercel.

Når Story 2.1 er ferdig, kan backend (2.5 og 2.6) og frontend (2.2 og 2.3) bygges parallelt. Modellene for opplasting og lenken «Last opp egne tall» lages i Epic 3, så v1 uten opplasting ikke får ubrukte modeller eller en død lenke (avgjort 2026-11-18).

### Story 2.1: API-kontrakten for kjerneflyten

Som utvikler i gruppen,
vil jeg ha Pydantic-modellene og tomme ruter for kjerneflyten,
slik at backend og frontend kan bygges parallelt mot samme kontrakt (AD-3, AD-7).

**Akseptansekriterier:**

**Gitt** `marin.api`
**Når** modellene leses
**Så** finnes Pydantic-modeller for `Uke`, `AnleggInfo`, status, estimert uke, tabellrad, grafpunkt, kryssing, `Detaljsvar` og svaret fra `GET /api/anlegg/{lokalitetsnr}`, med feltene i minsteformen i AD-3
**Og** status har feltene `farge`, `arsak`, `symbol`, `tekst`, `uke_tekst` og `forklaring`, der `farge` og `arsak` bare tillater de faste kodene (AD-7)
**Og** feltnavn er `snake_case`, uker er `{ar, uke}`, «ikke telt» er `null` og lusetall er JSON-tall (konvensjonene)
**Og** modellene speiler kjernens typer én til én

**Gitt** appen
**Når** `uv run uvicorn marin.api.app:app --reload` startes
**Så** finnes rutene `GET /api/anlegg?q=`, `GET /api/anlegg/{lokalitetsnr}` og `GET /api/anlegg/{lokalitetsnr}/prognose?ar=&uke=`
**Og** de svarer HTTP 501 med `{detail}` til de er bygd

**Gitt** `backend/openapi.json`
**Når** `uv run pytest` kjører
**Så** feiler en test hvis fila ikke er lik skjemaet appen lager
**Og** README beskriver kommandoen som lager fila på nytt

**Gitt** utviklingsoppsettet med frontend på port 3000
**Når** nettleseren kaller API-et
**Så** tillater CORS bare opphavet `http://localhost:3000`, og ingen andre opphav (AD-9)

**Gitt** at API-et starter
**Når** det lastes
**Så** leses `datasett.json` én gang fra pakken med `importlib.resources` og holdes i minnet, slik at Story 2.4 og 2.5 kan bygges uavhengig av hverandre (AD-10)

### Story 2.2: Frontend-skjelett med designtokens

Som utvikler i gruppen,
vil jeg ha et Next.js-prosjekt med designtokens, faste tekster og genererte API-typer,
slik at alle sider bygges med samme tokens og samme kontrakt (AD-3, AD-6, AD-9, UX-DR1, UX-DR23, UX-DR31).

**Akseptansekriterier:**

**Gitt** `frontend/`
**Når** `npm install` og `npm run build` kjøres
**Så** bygges sidene `/` og `/anlegg/` som statiske filer i `frontend/out/` med Next.js 16.4.6, React 19.3.1, TypeScript 5.9.3 og Tailwind 4.3.5. Sidene er tomme skall som fylles i senere stories
**Og** `next.config.ts` har `output: 'export'` og `trailingSlash: true`
**Og** prosjektet har ingen route handlers, server actions, middleware, `rewrites` eller dynamiske ruter

**Gitt** tokenene i DESIGN.md
**Når** `frontend/src/app/globals.css` leses
**Så** står alle farger, typografiroller (desktop og mobil), `rounded` og `spacing` én gang i Tailwind `@theme`, med bruddpunkt på 600px
**Og** komponentene bruker bare tokennavn, ikke egne farge- eller pikselverdier
**Og** siden bruker systemfonter og har bare lys modus

**Gitt** rotlayouten
**Når** en side vises
**Så** har `<html>` `lang="nb"`, lenker er i aksentfarge og understreket, og alle interaktive elementer får synlig fokusmarkering (2px aksent med 2px avstand)

**Gitt** `backend/openapi.json`
**Når** typeskriptet kjøres
**Så** lages `frontend/src/api/schema.ts` med openapi-typescript 7.13.0, og fila redigeres aldri for hånd
**Og** alle kall til API-et går gjennom `frontend/src/api/`, med API-base `''` i bygget og `http://127.0.0.1:8000` når `NODE_ENV === 'development'`

**Gitt** faste tekster i grensesnittet
**Når** en komponent trenger en tekst som ikke kommer fra API-et
**Så** hentes den fra `frontend/src/tekster.ts` (AD-2)

**Gitt** testvektorene i `backend/tests/data/format.json`
**Når** `npm test` kjører
**Så** gir `formatLus` og `formatUke` i `frontend/src/lib/format.ts` de samme svarene som `format_lus` og `format_uke` i kjernen (AD-6)

### Story 2.3: Kjøring lokalt og på Vercel

Som sensor,
vil jeg kunne kjøre Marin lokalt etter én oppskrift og åpne den publiserte versjonen,
slik at jeg kan prøve appen uten nøkler eller kontoer (NFR1, NFR9, NFR12, AD-9).

**Akseptansekriterier:**

**Gitt** at `frontend/out/` finnes
**Når** uvicorn startes
**Så** viser `http://127.0.0.1:8000/` forsiden, og `/anlegg/` kan lastes direkte uten 404
**Og** de statiske filene er montert etter alle `/api`-rutene
**Og** en ukjent rute som `/api/finnes-ikke` gir JSON 404, ikke HTML
**Og** en pytest sjekker monteringen når `out/` finnes, og at appen starter uten `out/`

**Gitt** en maskin der avhengighetene er installert
**Når** appen kjører
**Så** trenger den ikke nett, API-nøkler, miljøvariabler eller betalte kontoer (NFR1)

**Gitt** `vercel.json` med servicen `frontend` (rot `frontend/`) og servicen `backend` (rot `backend/`, FastAPI-appen)
**Når** repoet publiseres på Vercel
**Så** går `/api/(.*)` til backend og alt annet til frontend, fra samme opphav og uten CORS
**Og** `/` gir forsiden, og `/api/anlegg?q=x` svarer med JSON fra FastAPI

**Gitt** at Vercel Services (beta) ikke virker
**Når** gruppen bytter til reserveplanen
**Så** brukes to Vercel-prosjekter i samme repo, med API-base-URL og CORS som eneste endring
**Og** byttet er ført i `issues.md` og i «Åpne punkter» i arkitekturen

**Gitt** README
**Når** den leses
**Så** beskriver den kjøring i utvikling (to prosesser), lokal kjøring (bygg og uvicorn) og adressen til den publiserte versjonen (NFR12)

### Story 2.4: Forside og søk

Som Kari,
vil jeg søke opp anlegget mitt på navn eller lokalitetsnummer og forstå statusfargene,
slik at jeg finner riktig anlegg første gang jeg bruker Marin (FR4, FR5, FR6, FR6a).

**Akseptansekriterier:**

**Gitt** søketeksten «langholm», «LANGHOLMEN» eller lokalitetsnummeret til Langholmen
**Når** `GET /api/anlegg?q=` kalles
**Så** er Langholmen med i svaret (delvis treff på navn uavhengig av store og små bokstaver, eller helt lokalitetsnummer) (FR4)
**Og** store og små bokstaver ignoreres også for æ, ø og å
**Og** treffene er sortert alfabetisk på navn av backend, med lokalitetsnummer, navn, kommune og fylke (FR5)
**Og** et søk uten treff gir en tom liste
**Og** automatiske tester dekker delvis treff, store og små bokstaver, lokalitetsnummer og ingen treff (NFR10)

**Gitt** forsiden
**Når** den vises
**Så** står introsetningen fra `tekster.ts` øverst, så «Statusfargene» med fire statusmerker («✕ Rød», «! Gul», «✓ Grønn», «– Grå»), hvert med sin forklarende linje (UX-DR10, UX-DR21)
**Og** forklaringen bruker ingen fulle fargeflater, bare den runde statusmarkøren (FR6a (1))
**Og** under «Finn anlegget ditt» står søkefeltet med synlig etikett «Søk anlegg» og primærknappen «Søk» (UX-DR12, UX-DR22)

**Gitt** søkefeltet
**Når** Kari trykker Enter eller «Søk»
**Så** vises treflisten, og tomt søk gjør ingenting
**Og** søket kjøres ikke for hvert tastetrykk

**Gitt** treff
**Når** treflisten vises
**Så** har hver rad navnet i vekt 600 og «Lokalitetsnr. 12345 · Hitra, Trøndelag» under, hele raden er en lenke til `/anlegg/?nr={lokalitetsnr}`, og raden er minst 44px høy (UX-DR13)
**Og** listen vises også ved ett treff, uten statusfarger
**Og** raden med tastaturfokus får `accent-tint`

**Gitt** et søk uten treff
**Når** svaret kommer
**Så** står «Fant ingen anlegg som passer «{søk}». Søk på lokalitetsnavn eller lokalitetsnummer.» under søkefeltet, og meldingen leses opp via `aria-live` (FR6, UX-DR14)
**Og** søketeksten står fortsatt i feltet

**Gitt** toppfeltet
**Når** en annen side enn forsiden vises
**Så** har det logoen «Marin» (lenke til forsiden), og på desktop et søkeskjema med visuelt skjult etikett «Søk anlegg», felt og sekundærknappen «Søk», og lenken «Bytt anlegg» (UX-DR4)
**Og** på mobil står bare lenken «Søk / bytt», som går til forsiden med søkefeltet i fokus
**Og** et søk fra toppfeltet viser treflisten på forsiden
**Og** på forsiden står bare logoen
**Og** toppfeltet bryter til to linjer ved smal skjerm i stedet for å gi vannrett rulling

### Story 2.5: Prognose for et anlegg i API-et

Som Kari,
vil jeg at Marin regner ut prognosen for anlegget mitt og en analyseuke,
slik at detaljsiden kan vise status, estimert uke, tabell og graf fra ett svar (FR7, FR8, FR16, FR17, FR18, FR20a, AD-13, AD-14).

**Akseptansekriterier:**

**Gitt** et lokalitetsnummer som finnes
**Når** `GET /api/anlegg/{lokalitetsnr}` kalles
**Så** svarer API-et med `AnleggInfo`, `analyseuker` fra 2026 uke 42 til 2025 uke 1 (nyeste først, 94 uker) og `standard_analyseuke` 2026 uke 42 (FR7 (1))
**Og** 2026 uke 43, 2024 uke 52 og 2025 uke 53 finnes ikke i lista (FR7 (2) og (3))
**Og** et nummer som ikke finnes, gir 404

**Gitt** et anlegg og en uke i lista
**Når** `GET /api/anlegg/{lokalitetsnr}/prognose?ar=&uke=` kalles
**Så** svarer API-et med et `Detaljsvar` med `kilde = innebygd`, bygd av `bygg_detaljsvar(info, serie, omrade, analyseuke, kilde)` med `vurder` fra kjernen (AD-1, AD-13)
**Og** en uke utenfor lista gir 422, og et ukjent nummer gir 404 (AD-14)
**Og** status, `symbol`, `tekst` og `uke_tekst` er uendret fra kjernen

**Gitt** et testdatasett i `backend/tests/data/` med anleggene fra T5–T12
**Når** API-testene kjører
**Så** gir T5 med analyseuke 34 `estimert_uke` uke 38 og `uker_til` 4, og T10 med analyseuke 41 gir uke 44 og 3 (FR18 (1) og (2))
**Og** grønn status, grå status og brudd nå gir ingen estimert uke (FR18 (3))
**Og** FR8 (1)–(3) gir samme svar gjennom API-et som i Story 1.5

**Gitt** et `Detaljsvar`
**Når** `tabell` leses
**Så** har den alltid 5 rader, eldste først, med uke, verdi eller `null` og om raden er siste telling
**Og** T8 med analyseuke 40 gir uke 36–40 med 0,20 / `null` / 0,28 / `null` / 0,36, og uke 40 er siste telling (FR17 (1))
**Og** T10 med analyseuke 42 («ingen ny telling») gir de 5 ukene før analyseuka, uke 37–41, med `null` / 0,28 / `null` / 0,36 / `null` (FR20a (2))

**Gitt** et `Detaljsvar`
**Når** `graf` leses
**Så** har den ett punkt per uke fra første uke i vinduet til analyseuke + 6, med målt verdi, trendverdi og grense (hver kan være `null`)
**Og** T5 med analyseuke 34 gir målte verdier i uke 30–34, trendverdier fra uke 30 til uke 40 og grensen 0,5 i alle ukene (FR16 (1))
**Og** T6 med analyseuke 14 gir grensen 0,5 til og med uke 15 og 0,2 i uke 16–20 (FR16 (2))
**Og** T8 gir `null` som målt verdi i uke 37 og 39, aldri 0 (FR16 (3))
**Og** trendverdiene er estimater avrundet til 2 desimaler, og negative verdier er 0
**Og** ved varsel og følg med har `kryssing` uka der trenden møter grensen og etiketten «✕ Varsel uke 44» eller «! Følg med uke 46», ellers er `kryssing` tom

**Gitt** at det ikke finnes prognose
**Når** `graf` leses
**Så** gir T11 (brudd nå) målte verdier i uke 29 og 30 og grensen, men ingen trendverdier og ingen kryssing (FR20a (1))
**Og** T7 (ukjent område) gir målte verdier, men grensen er `null` i alle punktene (FR20a (3))

**Gitt** tekstfeltene `forklaring`, `tekstoppsummering` og `usikkerhetstekst`
**Når** denne storyen er ferdig
**Så** finnes de i svaret som tomme strenger, og fylles med innhold i neste story

### Story 2.6: Forklarende tekster fra kjernen

Som Kari,
vil jeg få statusen forklart med vanlige ord og vite hvor sikker prognosen er,
slik at jeg forstår hva statusen betyr uten datafaglig bakgrunn (FR15a, FR19, FR20, UX-DR29, UX-DR30, AD-2).

**Akseptansekriterier:**

**Gitt** T5 med analyseuke 34 (anlegg i sør)
**Når** kjernen lager forklaringen
**Så** er den «Lusetallene har steget de siste ukene. Fortsetter trenden, kan anlegget passere grensen på 0,5 i uke 38.» (FR15a (1))

**Gitt** de sju statusene
**Når** kjernen lager forklaringen
**Så** følger den malene i EXPERIENCE.md (Voice and Tone), med nøyaktig én forklaring per status (FR15a (3))
**Og** T7 gir «Anlegget mangler fylke i datagrunnlaget. Da vet ikke Marin hvilken lusegrense som gjelder, og lager ingen prognose.» (FR15a (2), FR20 (3))
**Og** T9 gir «Bare 2 av de siste 5 ukene har telling. Marin trenger minst 3 tellinger for å lage en prognose.» (FR20 (1))
**Og** T10 med analyseuke 42 gir «Siste telling er fra uke 40, mer enn én uke før analyseuka. Da lager Marin ingen prognose. Grafen og tabellen viser målte tall og grensen.» (FR20 (2))
**Og** T11 gir «Siste telling (uke 30) var 0,60. Det er på eller over grensen på 0,5 som gjelder denne uka.»

**Gitt** en prognose med kryssing
**Når** retningsordet velges
**Så** gir stigende trend «har steget», fallende trend «har falt» og flat trend «har ligget stabilt»
**Og** grensen i setningen er grensen i den estimerte uka, så en kryssing i vårperioden gir «grensen på 0,2»

**Gitt** T6 med analyseuke 14
**Når** kjernen lager tekstoppsummeringen
**Så** er den «Målte lusetall uke 10–14, 2026: 0,10, 0,12, 0,14, 0,16 og 0,18. Siste telling 0,18 i uke 14. Trenden gir 0,20 i uke 15, 0,22 i uke 16, 0,24 i uke 17, 0,26 i uke 18, 0,28 i uke 19 og 0,30 i uke 20. Grensen er 0,5 til og med uke 15 og 0,2 fra uke 16. Trenden når grensen i uke 16.» (UX-DR30)
**Og** de andre tilstandene (uten kryssing, brudd nå, for lite data, ingen ny telling, ukjent område) følger sine maler i EXPERIENCE.md
**Og** uker uten telling skrives «ikke telt», og når grensen endres i vinduet, skrives hvert trinn med første uke, og med siste uke når et nytt trinn følger

**Gitt** `backtest.json` i pakken
**Når** usikkerhetsteksten lages
**Så** er den «Prognosen er en enkel trendberegning, ikke en garanti. I en test på data fra 2025–2026 varslet Marin rødt 2–4 uker før X % av bruddene. Av alle røde varsler ble Y % fulgt av brudd innen 4 uker.», med X og Y lest fra fila som hele prosent (FR19, ordlyd avgjort 2026-11-18)
**Og** tallene står ikke i koden, og endres fila, endres teksten neste gang appen startes (FR19 (1))
**Og** teksten er med i svaret for alle statuser, også grå (FR19 (2))
**Og** mangler fila, er den ugyldig eller avviker parameterne fra kjernens konstanter, er teksten bare «Prognosen er en enkel trendberegning, ikke en garanti.», appen krasjer ikke, og en advarsel skrives til stderr (FR19 (3), AD-10)
**Og** er `antall_varsler_med_brudd` × 5 < `antall_varsler` i fila (eksakt med antallene, ikke den avrundede `presisjon`), er teksten i stedet «Prognosen er en enkel trendberegning, ikke en garanti. Rød status betyr at du bør følge ekstra med, ikke at grensen helt sikkert brytes. I en test på data fra 2025–2026 varslet Marin rødt 2–4 uker før X % av bruddene. Av alle røde varsler ble Y % fulgt av brudd innen 4 uker.», med X og Y som over (reaksjonen på M1-C, låst 2026-11-25 før Story 1.7, som ga 13,3 % presisjon)

### Story 2.7: Detaljside med statusboks og ukestabell

Som Kari,
vil jeg se statusen for anlegget mitt øverst på en rolig side, med tallene uke for uke under,
slik at jeg vet om jeg må gjøre noe og kan sende statusen videre som skjermbilde (FR9, FR15, FR15a, FR15b, FR17, FR18, FR20, FR20a, NFR4, NFR5).

**Akseptansekriterier:**

**Gitt** `/anlegg/?nr={lokalitetsnr}`
**Når** siden åpnes
**Så** henter den anlegget og prognosen for standarduka, og hele siden tegnes fra ett `Detaljsvar` (AR21)
**Og** siden er pakket i `<Suspense>` med en nøytral reserve (AD-9)
**Og** et nummer som ikke finnes (404), sender brukeren til forsiden
**Og** ved nettverks- eller 5xx-feil vises en generell feilmelding fra `tekster.ts` (AR20)

**Gitt** detaljsiden
**Når** den vises
**Så** står anleggsnavnet som tittel med sted under, så statusboksen, ukestabellen og usikkerhetsteksten, i én kolonne på maks 760px (UX-DR2)

**Gitt** et `Detaljsvar`
**Når** statusboksen vises
**Så** har den fargevarianten for `farge`, og ovenfra: anleggsnavn, linja med lokalitetsnummer, kommune og fylke, «Prognose regnet fra uke X, ÅÅÅÅ», symbolsirkelen med R4-teksten og `uke_tekst`, og forklaringen (UX-DR5, FR15b (1))
**Og** T5 med analyseuke 34 gir gul boks med «! Følg med: grensen kan nås om 4 uker (uke 38)» (FR15 (1), FR18 (1))
**Og** T6 gir rød boks med «✕ Varsel: grensen nås om 2 uker (uke 16)», og T11 gir rød boks med «✕ Brudd nå» (FR15 (2))
**Og** for hver av de sju statustekstene er teksten på skjermen tegn for tegn lik briefen, med symbolet først, fordi frontend viser `symbol`, `tekst` og `uke_tekst` uendret (FR15 (3), AD-2)
**Og** «Prognose regnet fra» vises også ved grå status og brudd nå (FR9 (3))
**Og** ved ukjent område viser stedslinja det som finnes av kommune og fylke

**Gitt** statusboksen
**Når** den leses med skjermleser
**Så** er boksen en navngitt region («Status»), symbolet har `aria-hidden`, og bare statusoverskriften er `aria-live="polite"` (UX-DR6, UX-DR7)
**Og** elementet med statusoverskriften finnes i siden fra start, og bare teksten byttes
**Og** boksen har ingen interaktive elementer, og hele boksen er synlig uten rulling på desktop ved 100 % zoom

**Gitt** at prognosen ikke er klar
**Når** siden venter på svar
**Så** står «Regner ut prognose …» i statusboksens plass, med hvit flate og heltrukken nøytral kant, uten statusfarge, stipling eller symbol, og uten animasjon (UX-DR8)
**Og** lastemeldingen står utenfor live-elementet og leses ikke opp

**Gitt** ukestabellen
**Når** den vises
**Så** har den kolonnene «Uke», «Voksne hunnlus» (høyrejustert, tabulære sifre) og «Merknad», med eldste uke øverst (UX-DR19)
**Og** overskriften er «De siste 5 ukene», eller «De 5 ukene før analyseuka» ved «ingen ny telling» (FR20a)
**Og** ukene skrives «uke 36, 2026», uker uten telling viser «–» og merket «– Ikke telt», og siste telling har merknaden «Siste telling» (FR17 (2), NFR5)
**Og** tabellen får plass uten vannrett rulling på mobil

**Gitt** usikkerhetsteksten fra API-et
**Når** siden vises
**Så** står den nederst med en tynn strek over, for alle statuser (UX-DR20)

### Story 2.8: Trendgraf

Som Kari,
vil jeg se målte lusetall, trenden og grensen i en graf,
slik at jeg raskt ser om og hvor trenden møter grensen (FR16, FR20a, UX-DR15–UX-DR18, AR23).

**Akseptansekriterier:**

**Gitt** `Detaljsvar.graf`
**Når** `TrendGraf` tegner den
**Så** er grafen en egen SVG-komponent uten grafbibliotek, og den tegner bare punktene fra API-et uten å regne trend eller grense selv
**Og** grafen står mellom statusboksen og ukestabellen

**Gitt** en prognose
**Når** grafen vises
**Så** har den horisontale rutenettlinjer, målte punkter i aksentfarge med tynn linje mellom tellinger, trendlinje heltrukken gjennom vinduet og stiplet fram i tid, grenselinje på 2px som trapp med etiketten «Grense 0,5», og prikket analyseukelinje med «Prognose →» (UX-DR15)
**Og** T5 med analyseuke 34 viser 5 målte punkter, trendlinje fra uke 30 til uke 40 og flat grenselinje på 0,5 (FR16 (1))
**Og** T6 med analyseuke 14 viser grenselinja som en trapp fra 0,5 i uke 15 til 0,2 i uke 16–20 (FR16 (2))
**Og** i T8 vises uke 37 og 39 som hule punkter med «ikke telt» på x-aksen, og ingen punkter har verdien 0 (FR16 (3))
**Og** ved varsel og følg med står kryssingsmarkøren med etiketten fra API-et, og gul markør bruker den mørke gulkanten

**Gitt** at det ikke finnes prognose
**Når** grafen vises
**Så** gir T11 punktene i uke 29 og 30 og grenselinja, uten trendlinje og uten kryssingsmarkør (FR20a (1))
**Og** T7 gir målte punkter uten grenselinje, og tegnforklaringen sier «Grensen er ukjent» (FR20a (3))

**Gitt** tegnforklaringen
**Når** den vises
**Så** har den «Målt lusetall», «Trend (stiplet = prognose)» og «Grense per uke», og trendoppføringen faller bort uten prognose (UX-DR16)

**Gitt** en skjermbredde på 320px eller 200 % tekstzoom
**Når** grafen vises
**Så** er all tekst i grafen minst 13 CSS-px slik den vises, og den blir større med tekstzoom (UX-DR17)

**Gitt** grafen
**Når** den leses med skjermleser
**Så** har den `role="img"`, innholdet i SVG-en er skjult, og den er knyttet til den synlige tekstoppsummeringen som står under tegnforklaringen (UX-DR18)
**Og** grafen er ikke interaktiv

### Story 2.9: Bytte analyseuke

Som Kari,
vil jeg velge en tidligere analyseuke,
slik at jeg kan se om Marin ville varslet i tide før et brudd jeg husker (FR7, FR8, FR9, J2, UX-DR11).

**Akseptansekriterier:**

**Gitt** detaljsiden
**Når** den vises
**Så** står analyseukevelgeren mellom tittelen og statusboksen, med etiketten «Analyseuke», verdier som «uke 42, 2026» fra `analyseuker` i API-et (nyeste først) og `standard_analyseuke` valgt (FR7 (1))
**Og** velgeren er en vanlig nedtrekksliste, minst 44px høy
**Og** frontend har ingen ISO-kalender og lager ingen uker selv (AD-14)

**Gitt** at Kari velger 2026 uke 30
**Når** valget er gjort
**Så** står «Prognose regnet fra uke 30, 2026» i statusboksen (FR9 (1))
**Og** endringen gjelder uten egen «Oppdater»-knapp

**Gitt** at Kari bytter analyseuke til uke 25
**Når** det nye svaret kommer
**Så** endres teksten fra FR9, status, graf og tabell samtidig, og ingen av dem viser den gamle uka (FR9 (2), FR15b (3))
**Og** anlegget og rulleposisjonen beholdes

**Gitt** at Kari bruker piltastene i en lukket nedtrekksliste
**Når** uka endres flere ganger raskt
**Så** sendes forespørselen 300 ms etter siste endring, og svar for en uke som ikke lenger er valgt, avbrytes med `AbortController` (AR21)
**Og** skjermleseren leser bare den nye statusoverskriften, ikke navn, sted, forklaring eller lastemeldingen

### Story 2.10: Husket anlegg

Som Kari,
vil jeg at Marin åpner anlegget mitt direkte neste gang,
slik at onsdagssjekken går raskt (FR6a, FR6b, NFR6, AD-8, AD-15).

**Akseptansekriterier:**

**Gitt** et vellykket `Detaljsvar` med `kilde = innebygd`
**Når** detaljsiden vises
**Så** lagrer `frontend/src/lib/husketAnlegg.ts` bare lokalitetsnummeret i `localStorage` under `marin.sistViste` (AD-8)
**Og** nettleseren inneholder ingen lusetall fra Marin, bare lokalitetsnummeret (FR6b (5), NFR6)

**Gitt** at Kari har vist et anlegg med analyseuke 2025 uke 30
**Når** hun lukker fanen og åpner appen igjen i samme nettleser
**Så** sender forsiden henne til `/anlegg/?nr={nr}&husket=1`, med «Sist viste anlegg» over tittelen og analyseuke 2026 uke 42 (FR6b (1))
**Og** omdirigeringen skjer bare første gang appen tegnes i fanen (AD-15)

**Gitt** første besøk, eller at nettleserdataene er tømt
**Når** appen åpnes
**Så** vises forsiden (FR6b (2))

**Gitt** et husket lokalitetsnummer som ikke lenger finnes i datagrunnlaget
**Når** appen åpnes
**Så** vises forsiden uten feilmelding (FR6b (4))

**Gitt** at lagringen mangler eller feiler
**Når** `husketAnlegg` leser eller skriver
**Så** feiler ikke appen, og forsiden vises
**Og** Vitest dekker lagring, lesing og feilende lagring

**Gitt** et husket anlegg
**Når** Kari går til forsiden via «Bytt anlegg» eller logoen
**Så** vises forsiden med intro og fargeforklaring, uten omdirigering (FR6a (2))
**Og** «Sist viste anlegg» vises bare når siden er åpnet med `husket=1`

### Story 2.11: Sjekkliste og tilgjengelighetskontroll

Som sensor,
vil jeg ha en sjekkliste i README og en app som er kontrollert mot den,
slik at jeg kan se at kravene som ikke testes automatisk, er oppfylt (NFR4, NFR8, NFR10, NFR12, UX-DR3, UX-DR32, UX-DR33).

**Akseptansekriterier:**

**Gitt** PRD kap. 5.2, 5.3 og 5.5
**Når** README-sjekklisten lages
**Så** er den en ordrett kopi av de testbare konsekvensene der (NFR10)
**Og** den har i tillegg kontroll av de fire statusboksene i gråtoner og med deuteranopi-simulering, og kontroll ved 320px, 600px, 400 % zoom og 200 % tekstzoom (UX-DR33)

**Gitt** sjekklisten
**Når** gruppen går gjennom den lokalt og på Vercel
**Så** er hvert punkt krysset av med dato
**Og** avvik er rettet eller ført i `issues.md`

**Gitt** et skjermbilde i gråtoner av hver statusboks
**Når** det ses på
**Så** kan statusen leses ut av symbol og tekst (FR15 (4), NFR4)

**Gitt** 320 CSS-px bredde, 400 % zoom eller økt tekstavstand (WCAG 1.4.12)
**Når** forsiden og detaljsiden vises
**Så** er det ingen vannrett rulling, og ikke noe innhold går tapt (UX-DR3)

**Gitt** bare tastatur
**Når** Kari bruker forsiden og detaljsiden
**Så** kan alt nås og brukes med Tab, Shift+Tab, Enter, mellomrom og piltaster, Tab-rekkefølgen følger leserekkefølgen, og fokus er alltid synlig (UX-DR32)
**Og** ingen funksjon finnes bare ved hover, og trykkflatene er minst 44 × 44px på mobil

**Gitt** appen kjører på en vanlig bærbar PC
**Når** detaljsiden åpnes
**Så** vises den på under 2 sekunder, og målingen står i README (NFR8)

**Gitt** den publiserte versjonen
**Når** den sammenlignes med lokal kjøring
**Så** har den samme funksjoner og data, uten hemmeligheter (NFR12)
**Og** `uv run pytest` og `npm test` består

## Epic 3: Kari får prognose på egne tall (J3, tillegg)

Kari laster opp egne lusetall fra Excel eller CSV og får samme detaljside som for anleggene i utdraget, uten at dataene lagres. Storyene bygges i rekkefølgen 3a Excel (3.1–3.4), 3b CSV med komma (3.5) og 3c norsk CSV (3.6). Story 3.6 kuttes først, og v1 kan leveres uten hele epicen.

Hjelpeteksten og meldingen for ukjent format nevner bare formatene som er bygd, så teksten aldri lover et format som er kuttet. Tre beslutninger fra 2026-11-18 gjelder epicen: standarduka for opplastede data er den nyeste uka i fila, frontend sjekker størrelsen før fila sendes (Vercel stopper forespørsler over 4,5 MB før de når FastAPI), og CSV-filer leses som UTF-8 når de er gyldig UTF-8, ellers som Windows-1252, i begge formatene.

### Story 3.1: API-kontrakten for opplasting

Som utvikler i gruppen,
vil jeg ha modellene og tomme ruter for opplasting,
slik at backend og frontend for opplasting kan bygges parallelt mot samme kontrakt (AD-3, AD-13).

**Akseptansekriterier:**

**Gitt** `marin.api`
**Når** modellene leses
**Så** finnes `Opplastingssvar` (`filnavn`, `anlegg`, `feil`, `antall_feil`), `OpplastetAnlegg` (`info`, `serie`, `omrade_utledet`, `omrade_tekst`, `analyseuker`, `standard_analyseuke`), `Feil` (`rad` eller `null`, `melding`) og body for `POST /api/prognose` (`info`, `serie`, `omrade`, `analyseuke`), med formene i AD-3
**Og** `omrade_utledet` tillater `sor`, `nord` eller `null`, og `omrade` i prognosebody tillater bare `sor` og `nord`
**Og** `Detaljsvar.kilde` tillater `opplastet`

**Gitt** appen
**Når** den startes
**Så** finnes `POST /api/opplasting?filnavn=` (rå body, `application/octet-stream`) og `POST /api/prognose`, og begge svarer HTTP 501 til de er bygd

**Gitt** den nye kontrakten
**Når** `openapi.json` og `schema.ts` lages på nytt
**Så** består kontrakttesten, og frontend bygger med de nye typene

### Story 3.2: Lese og validere Excel-fil

Som Kari,
vil jeg at Marin leser Excel-uttrekket mitt fra BarentsWatch og sier tydelig hva som er galt,
slik at jeg kan rette fila selv (FR22, FR23, FR23a, FR24, FR25, AD-4, AD-12, AD-13).

**Akseptansekriterier:**

**Gitt** en fil sendt som rå body til `POST /api/opplasting?filnavn=`
**Når** API-et leser den
**Så** leses den med `await request.body()`, aldri som multipart, og ingenting skrives til disk eller holdes etter svaret (AD-4)
**Og** en test laster opp en fil over 1 MB mens `tempfile` er satt til å feile, og testen består

**Gitt** en fil over 4 MB
**Når** den sendes direkte til API-et (for eksempel ved lokal kjøring)
**Så** svarer API-et med feilen «Fila er større enn 4 MB. Last ned bare ditt eget anlegg fra BarentsWatch og prøv igjen.» uten radnummer, og ingen anlegg (FR24, NFR12)

**Gitt** en hvilken som helst fil
**Når** API-et svarer
**Så** er svaret HTTP 200 med `Opplastingssvar`, og har fila minst én feil, er `anlegg` tom (AD-13)
**Og** `feil` har de 20 første feilene sortert på rad, og `antall_feil` har totalen (AR20)
**Og** `rad` er radnummeret som i regnearket, der overskriften er rad 1, og `melding` er hele linja med «Rad N: » foran

**Gitt** en gyldig Excel-fil i BarentsWatch-formatet
**Når** den leses
**Så** brukes `marin.kilder.barentswatch`, den samme leseren som `forbered`, uten kutt ved `SISTE_UKE` (AD-12)
**Og** en test leser samme testfil som opplasting og gjennom leseren til `forbered`, og seriene er like
**Og** en fil med flere anlegg gir ett `OpplastetAnlegg` per anlegg (FR22)

**Gitt** en Excel-fil med feil
**Når** den valideres
**Så** gir den feilmeldinger med ordlyden i EXPERIENCE.md, for eksempel «Rad 4: året 1999 er utenfor 2000–{inneværende år}.», «Rad 5: uke 54 finnes ikke. Uke må være 1–53.», «Rad 5: 2025 har ikke uke 53.», «Rad 7: lusetallet «abc» er ikke et tall.» og «Rad 9: uke 34, 2026 finnes allerede i rad 6.» (FR24, UX-DR28)
**Og** negative lusetall og manglende kolonner gir egne meldinger, og meldingen for manglende kolonne nevner kolonnen som mangler
**Og** inneværende år sendes inn som `inneverende_ar` fra API-skallet, og testene setter det selv (AD-5)
**Og** en fil som ikke er xlsx, eller som mangler arket «Lakselus per fisk», gir meldingen for ukjent format, som nevner bare formatene som er bygd

**Gitt** et anlegg i en Excel-fil med utfylt `Fylke`
**Når** området bestemmes
**Så** er `omrade_utledet` utledet med `omrade_fra_fylke`, og `omrade_tekst` er for eksempel «Område: Trøndelag – grense som for sør» eller «Område: Nordland – grense som for nord» (FR23)
**Og** mangler fylket, eller er det ukjent, er `omrade_utledet` og `omrade_tekst` tomme, og brukeren må velge område (FR23a)

**Gitt** et gyldig anlegg i fila
**Når** valgbare uker lages
**Så** er `analyseuker` alle ISO-uker fra første til siste uke i fila, også uker uten rad imellom, nyeste først, og `standard_analyseuke` er den nyeste uka (FR25, AD-14)

**Gitt** testmappa `backend/tests/data/`
**Når** opplastingstestene kjører
**Så** finnes én testfil per feiltype og én gyldig Excel-fil med flere anlegg (NFR10)

### Story 3.3: Opplastingssiden

Som Kari,
vil jeg velge en fil, se hva Marin fant i den og rette feil,
slik at fila blir klar for en prognose (FR22, FR23, FR23a, FR24, FR26, UX-DR24–UX-DR27).

**Akseptansekriterier:**

**Gitt** toppfeltet på alle sider, også forsiden
**Når** det vises
**Så** har det lenken «Last opp egne tall» til `/opplasting/` på både desktop og mobil, med trykkflate på minst 44px på mobil (UX-DR4)

**Gitt** `/opplasting/`
**Når** siden vises
**Så** har den overskriften «Last opp egne tall», et ekte filfelt med etiketten «Fil», knappen «Velg fil» og en hjelpetekst koblet med `aria-describedby` som nevner bare formatene som er bygd (UX-DR24)
**Og** lagringsnotisen «Fila lagres ikke. Tallene forsvinner når du går bort fra prognosen for dem, lukker fanen eller laster opp en ny fil.» står på siden (FR26)

**Gitt** at Kari velger en fil
**Når** fila leses
**Så** står «Leser fila …» under filvelgeren i en `role="status"`-region som finnes i siden fra start, og «Vis prognose» er deaktivert til svaret kommer (UX-DR25)
**Og** fila sendes som rå bytes med filnavnet gjennom `frontend/src/api/`
**Og** en ny fil erstatter resultatet fra forrige fil (FR26)

**Gitt** en fil over 4 MB
**Når** Kari velger den
**Så** sendes den ikke, og siden viser feilen «Fila er større enn 4 MB. Last ned bare ditt eget anlegg fra BarentsWatch og prøv igjen.» fra `tekster.ts`, med samme ordlyd som i backend (avgjort 2026-11-18)

**Gitt** et svar med feil
**Når** feilmeldingen vises
**Så** står den i en hvit boks med 2px mørk kant over skjemaet, uten statusrødt, med overskriften «Fila har N feil. Marin har ikke laget noen prognose.» og én feil per linje (UX-DR26)
**Og** er `antall_feil` over 20, står de 20 første og «… og N feil til. Rett feilene over og se etter samme feil i resten av fila.»
**Og** fokus flyttes til overskriften i feilmeldingen, filfeltet får `aria-invalid="true"` og `aria-describedby` til feilmeldingen, og `role="alert"` brukes ikke (UX-DR27)
**Og** bare feilmeldingen og filvelgeren vises, og fila kan velges på nytt uten å laste siden

**Gitt** en Excel-fil med flere anlegg
**Når** svaret vises
**Så** står anleggene under overskriften «Velg anlegg» som standard radioknapper med samme radoppsett som treflisten (FR22)

**Gitt** et anlegg med utledet område
**Når** svaret vises
**Så** står `omrade_tekst` som vanlig tekst, for eksempel «Område: Trøndelag – grense som for sør», og den kan ikke endres (FR23)

**Gitt** et anlegg uten utledet område
**Når** svaret vises
**Så** står radioknappene sør og nord uten forhåndsvalg, med hjelpeteksten «Nord: Nordland, Troms og Finnmark. Sør: alle andre fylker.» (FR23a)
**Og** lastes en ny fil av samme type opp i samme økt, beholdes valget

**Gitt** at Kari trykker «Vis prognose» uten å ha valgt anlegg eller område
**Når** skjemaet sjekkes
**Så** står «Velg ett av anleggene i fila.» eller «Velg område: sør eller nord.» under gruppens overskrift, gruppen får `aria-invalid="true"`, og fokus flyttes til første radioknapp i den første gruppen med feil (UX-DR27)
**Og** feilteksten forsvinner når et valg er gjort
**Og** felt og grupper med feil har 2px mørk kant

**Gitt** at Kari laster opp en rettet fil
**Når** feilmeldingen forsvinner
**Så** flyttes fokus til «Velg anlegg» ved flere anlegg, ellers til første radioknapp i områdevalget, ellers til «Vis prognose» med «Område: …»-linja i `aria-describedby`

**Gitt** radioknappene
**Når** de brukes
**Så** er hele raden klikkbar og minst 44px høy

### Story 3.4: Prognose på opplastede data

Som Kari,
vil jeg se prognosen for mine egne tall på samme detaljside, uten at tallene lagres,
slik at jeg får status med ukas ferske telling (FR6b, FR23a, FR25, FR25a, FR26, AD-4, AD-13, AD-15).

**Akseptansekriterier:**

**Gitt** `POST /api/prognose` med `info`, `serie`, `omrade` og `analyseuke`
**Når** ruta kalles
**Så** svarer den med `Detaljsvar` med `kilde = opplastet`, bygd med `bygg_detaljsvar` (AD-13)
**Og** `omrade` som ikke er `sor` eller `nord`, gir 422, og en analyseuke utenfor uke-lista for serien gir 422 (AD-14)
**Og** serveren utleder ikke området på nytt, og lagrer ingenting

**Gitt** gyldige valg på opplastingssiden
**Når** Kari trykker «Vis prognose»
**Så** settes dataene i `frontend/src/lib/opplastetData.ts`, og siden går til `/anlegg/?opplastet=1` med `router.push` (AD-15)
**Og** for Excel med fylke sendes `omrade_utledet` videre som område

**Gitt** detaljsiden for opplastede data
**Når** den vises
**Så** er den samme detaljside som for anlegg i utdraget, med statusboks, graf, ukestabell og usikkerhetstekst (FR25)
**Og** analyseukevelgeren viser `analyseuker` fra opplastingssvaret, med den nyeste uka i fila valgt, og intervallet i FR7 gjelder ikke
**Og** tittelen er lokalitetsnavnet fra fila, og stedslinja viser kommune og fylke når fila har dem
**Og** «Dine opplastede tall: {filnavn}» står inne i statusboksen rett under stedslinja, med «Dine opplastede tall:» i fet skrift (FR25a, UX-DR9)
**Og** «Sist viste anlegg» vises ikke

**Gitt** at Kari har sett opplastede data
**Når** hun åpner appen på nytt
**Så** vises det sist viste innebygde anlegget eller forsiden, og opplastede data vises aldri, fordi `husketAnlegg` bare lagrer etter `kilde = innebygd` (FR6b (3))

**Gitt** opplastede data i minnet
**Når** Kari går fra detaljsiden til en annen side i samme fane (logo, «Bytt anlegg», søk eller «Last opp egne tall»)
**Så** tømmes dataene av lytteren i rotlayouten ved ruteskiftet, aldri i en `useEffect`-opprydding (AD-15, FR26)
**Og** dataene tømmes også når en ny fil velges, og de er borte når fanen lukkes eller siden lastes på nytt
**Og** dataene skrives aldri til `localStorage`, `sessionStorage`, IndexedDB eller disk (NFR6)

**Gitt** detaljsiden for opplastede data
**Når** Kari trykker nettleserens tilbakeknapp
**Så** kommer hun til opplastingssiden (FR26)
**Og** åpnes `/anlegg/?opplastet=1` uten data i minnet (ny lasting, fram-knapp eller direkte lenke), gjør siden `router.replace('/opplasting/')`

**Gitt** `opplastetData`
**Når** `npm test` kjører
**Så** dekker Vitest `sett`, `hent` og `tom`, og at ingenting havner i nettleserlagring
**Og** dataene overlever React Strict Mode i utvikling

### Story 3.5: CSV med komma (FR21)

Som Kari,
vil jeg laste opp lusetallene mine som en enkel CSV-fil,
slik at jeg kan bruke tall fra mitt eget regneark (FR21, FR23a, FR24).

**Akseptansekriterier:**

**Gitt** en CSV-fil med kolonnene `år`, `uke` og `voksne_hunnlus`, komma som skilletegn og desimalpunktum
**Når** `marin.kilder.csv` leser den
**Så** leses kolonnenavnene uavhengig av store og små bokstaver
**Og** fila leses som UTF-8 (med eller uten BOM) når den er gyldig UTF-8, ellers som Windows-1252 (avgjort 2026-11-18)
**Og** CSV-eksempelet i PRD kap. 7 gir 0,06 i uke 30, 0,12 i uke 31, ikke telt i uke 32 og 0,24 i uke 33, 2026
**Og** tom verdi blir uke uten telling (FR21)

**Gitt** en gyldig CSV-fil
**Når** API-et svarer
**Så** har svaret ett anlegg uten lokalitetsnummer og navn, og uten utledet område, så Kari må velge sør eller nord (FR23a, AD-13)
**Og** detaljsiden bruker filnavnet som tittel
**Og** valgbare uker og standarduke følger samme regel som for Excel

**Gitt** en CSV-fil med feil
**Når** den valideres
**Så** gjelder de samme FR24-reglene som for Excel, med radnummer
**Og** manglende kolonne gir «Fila mangler kolonnen «voksne_hunnlus». Kolonnene må hete år, uke og voksne_hunnlus.»
**Og** desimalkomma gir «Rad 7: «0,3» – fila bruker komma som skilletegn, så tallet må ha desimalpunktum (0.3).» (UX-DR28)

**Gitt** at CSV med komma er bygd
**Når** opplastingssiden og meldingen for ukjent format vises
**Så** nevner de CSV med komma og Excel-uttrekk fra BarentsWatch, og filfeltet godtar .csv og .xlsx

**Gitt** testmappa
**Når** testene kjører
**Så** finnes én testfil per feiltype og per godkjent variant, også UTF-8 med BOM og Windows-1252 (NFR10)

### Story 3.6: Norsk CSV (FR21b)

Som Kari,
vil jeg laste opp CSV-fila slik norsk Excel lagrer den,
slik at jeg slipper å endre innstillinger i regnearket (FR21b, FR24).

**Akseptansekriterier:**

**Gitt** en CSV-fil med semikolon som skilletegn og desimalkomma
**Når** den leses
**Så** finnes formatet ut fra overskriftsraden, og fila leses med samme regel for tegnkoding som i Story 3.5
**Og** det norske eksempelet i PRD kap. 7 gir samme serie som eksempelet med komma

**Gitt** en semikolonfil med desimalpunktum
**Når** den valideres
**Så** gir den «Rad 7: «0.3» – fila bruker semikolon, så tallet må ha desimalkomma (0,3).» (UX-DR28)

**Gitt** at norsk CSV er bygd
**Når** en fil med ukjent format lastes opp
**Så** er meldingen «Marin kjenner ikke igjen formatet. Marin godtar CSV med komma som skilletegn og punktum som desimaltegn, eller semikolon som skilletegn og komma som desimaltegn (norsk Excel), og Excel-uttrekk fra BarentsWatch.»
**Og** hjelpeteksten på opplastingssiden nevner også det norske formatet

**Gitt** testmappa
**Når** testene kjører
**Så** finnes testfiler for norsk CSV i Windows-1252 og UTF-8, og for feil desimaltegn (NFR10)

**Gitt** at gruppen kutter storyen ved tidsnød
**Når** v1 leveres
**Så** avvises semikolonfiler med meldingen for ukjent format fra Story 3.5, og README og PRD-en sier at FR21b er kuttet (AR27)
