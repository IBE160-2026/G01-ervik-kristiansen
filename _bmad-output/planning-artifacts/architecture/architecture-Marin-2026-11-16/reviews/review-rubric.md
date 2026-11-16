---
type: spine-review
lens: rubrikk (good-spine-sjekklista)
target: ../ARCHITECTURE-SPINE.md
driving_spec: ../../../prds/prd-Marin-2026-11-02/prd.md
also_read: [../.memlog.md, brief.md, addendum.md, EXPERIENCE.md, DESIGN.md (utdrag), .gitignore, README.md]
reviewed: '2026-11-16'
verdict: 'Byggbar etter rettelser: 0 kritiske, 2 høye, 6 middels, 7 lave'
---

# Rubrikkgjennomgang: Architecture Spine for Marin

## Dom

Spinen er slank og godt bygd. Den fanger de viktigste stedene der byggerne kan gå i hver sin retning: reglene ligger bare i kjernen, tekstene lages i backend, Pydantic er fasit, serveren er tilstandsløs, og systemdatoen brukes ikke. Det er likevel hull på tre steder, og der vil to byggere (eller to KI-agenter) gjøre ulike valg: **hvordan appen bygges og kjøres ved innlevering og i utvikling**, **opplastingsflyten i AD-4**, og **hvem som eier formen på API-svarene før koden finnes**. Rett de to høye og de seks middels funnene før epics og stories skrives. De fleste rettelsene er én til tre setninger i en AD som finnes fra før, eller én ny AD.

## Sjekkpunktene

| Sjekkpunkt | Vurdering | Funn |
| --- | --- | --- |
| Låser de reelle delingspunktene for nivået under, og ingen mangler | Delvis. Kjernen av domenet er dekket. Opplasting, ukevalg, formatering og koblingen mellom utvikling og drift mangler. | H2, M1, M2, M3, M5 |
| Hver AD-regel kan håndheves og hindrer det den sier den hindrer | Stort sett. AD-1, AD-3 og AD-4 hindrer ikke divergensen helt. AD-2 sier imot lagtabellen. | M1, M2, H2, M6 |
| Ingenting under Deferred kan få enheter til å divergere | Delvis. «Detaljer i Pydantic-modellene» og begrunnelsen for «Publisering på nett» holder ikke. | M2, M4 |
| Dekker FR-ene og NFR-ene i PRD-en (Capability map) | Nesten. NFR3 og NFR11 mangler. FR7, FR22, FR25 og FR26 er bare delvis dekket. | L4, M2, H2 |
| Alle dimensjoner nivået eier er avgjort, utsatt eller ført som åpne punkter, også driftsrammen | Delvis. Miljøene er nevnt. Installasjon, bygg, stier, porter og drift er ikke omtalt, og spinen har ingen seksjon for åpne punkter. | H1, M3, M4, L2 |
| Overspesifisering | Lite. To eller tre små kutt. | O1–O3 |
| Mekanisk lint (`lint_spine.py`) | 6 lave funn, alle falske positiver | L7 |

---

## Høy

### H1: Hvordan appen kjøres ved innlevering er ikke låst (driftsrammen)

**Sjekkpunkt:** dimensjoner, driftsrammen. **Sted:** Structural Seed, «Miljøer» (linje 175), Konfigurasjon (linje 124), AD-9 og AD-10.

Spinen sier «Innlevering: `npm run build` (statisk eksport), deretter én `uvicorn`-prosess». Tre ting som avgjør om sensor får kjørt appen (SK5, NFR1), er ikke bestemt:

1. **`out/` står i `.gitignore` (linje 4).** Byggemappa `frontend/out/` kommer ikke med i repoet. Sensor må da ha Node ≥ 20.9, kjøre `npm ci` og bygge selv. Spinen sier verken at Node er et krav for sensor, eller at `frontend/out/` skal committes. Én bygger kan anta det ene og en annen det andre, og den som skriver README, gjetter.
2. **NFR1 sier «uten nettilgang».** `uv sync`, `npm ci` og eventuelt nedlasting av Python 3.14 med uv trenger nett. Spinen bør si hvordan NFR1 skal forstås («nett trengs bare ved installasjon, ikke for å kjøre»), ellers kan sensor lese kravet som brutt.
3. **Stiene avhenger av hvor kommandoen kjøres fra.** `pyproject.toml` ligger i `backend/`, men `data/barentswatch/`, `data/backtest/resultat.json` og `frontend/out/` ligger fra repo-roten. «Stier ligger i `marin.config`» sier ikke hva stiene regnes fra. Regnes de fra arbeidsmappa, kan backtesten skrive `resultat.json` ett sted mens API-et leser et annet, avhengig av hvor `uv run` startes. Feilen blir stille, fordi AD-10 med vilje lar FR19 vise teksten uten tall når fila mangler.

**Forslag:** Legg til én AD (sammen med M3), f.eks.:

> **AD-11 Kjøring, stier og miljøer.** Binds: NFR1, NFR9, SK5, AD-9, AD-10. Prevents: at app, backtest og tester leser og skriver ulike steder, og at utvikling og innlevering settes opp ulikt. Rule: Python-kommandoer kjøres fra `backend/`. `marin.config` regner alle stier fra repo-roten (`Path(__file__)`), aldri fra arbeidsmappa. Nett trengs bare ved installasjon (`uv sync`, `npm ci`). `frontend/out/` [committes / committes ikke, og Node ≥ 20.9 er da et krav for sensor]. *(+ reglene for porter, base-URL og statiske filer fra M3)*

**Handling:** Diskuter (valget om `out/` skal committes), og rett resten selv. Anbefaling: ikke commit `out/`. La heller README ha én fast rekkefølge: `uv sync` → `npm ci` → `npm run build` → `uv run uvicorn …`. Da slipper dere at en gammel build blir liggende i repoet.

### H2: AD-4 (opplasting) kan ikke bygges slik regelen står

**Sjekkpunkt:** delingspunkter og om regelen hindrer divergensen. **Sted:** AD-4 (linje 75–79), API-tabellen i AD-3 (linje 72–73), FR22, FR25 og FR26.

1. **Excel med flere anlegg (FR22) når serveren er tilstandsløs.** I tabellen står det at `POST /api/opplasting` svarer med «normalisert serie, liste over anlegg å velge fra, eller `feil[]`». Brukeren skal velge anlegg *etter* opplastingen, og serveren husker ingenting. Da må svaret enten inneholde serien for alle anleggene, eller så må frontend sende fila på nytt sammen med `lokalitetsnr`. Spinen sier ikke hvilken løsning som gjelder, og backend og frontend vil anta ulikt. Det er realistisk at noen laster opp et helt årsuttrekk fra BarentsWatch (ca. 5 MB, omtrent 1 000 lokaliteter, jf. addendumet). Å lese den fila to ganger med openpyxl kan ta flere sekunder.
2. **«Komponenttilstand» overlever ikke et sidebytte.** Flyten går fra `/opplasting` til `/anlegg?opplastet=1`, som er to ulike sider i Next. Tilstanden i opplastingssiden forsvinner når siden byttes. Serien må derfor ligge et felles sted, f.eks. en kontekst i rot-layouten eller en modul. Det stedet bør ha et navn, slik at opplastingsstoryen og detaljsidestoryen bruker det samme. Det er heller ikke bestemt hva som skjer når `/anlegg?opplastet=1` åpnes uten en serie i minnet, f.eks. etter omlasting eller når brukeren går tilbake etter å ha forlatt siden. FR26 krever at tilbakeknappen går til opplastingssiden.
3. **AD-4 sier imot FR26 slik den står i PRD-en.** FR26 sier «ligger bare i minnet til den kjørende appen» og «forsvinner … når appen startes på nytt». Med AD-4 ligger serien i fanen og overlever at serveren startes på nytt. Memloggen noterer «Krever omformulering av FR26», men PRD-en er ikke endret, og spinen har ikke ført dette som et åpent punkt.

**Forslag:** Legg til i Rule for AD-4:

> Den opplastede serien holdes i én klientmodul (`frontend/src/lib/opplastetSerie.ts`, gjort tilgjengelig via rot-layouten), aldri i sidekomponenten til `/opplasting`. Serien tømmes når `/anlegg?opplastet=1` forlates og når en ny fil velges. Åpnes `/anlegg?opplastet=1` uten serie i minnet, kaller siden `router.replace('/opplasting')`. Ved Excel med flere anlegg returnerer `POST /api/opplasting` `anlegg[]`, hver med anleggsinfo og normalisert serie. Fila leses én gang, og serveren holder ingenting.

Før i tillegg «FR26 omformuleres i PRD-en (minnet i nettleserfanen)» som et åpent punkt (se M4). **Handling:** Rett selv. Valget mellom alle serier i ett svar og ny opplasting med `lokalitetsnr` kan diskuteres, men anbefalingen er alle serier i ett svar.

---

## Middels

### M1: AD-1 hindrer ikke helt at appen og backtesten gir ulike svar

**Sted:** AD-1 (linje 49–53), FR27, FR27a og NFR3. Regelen sier at R1–R4 finnes én gang, men ikke at de **settes sammen** én gang. Backtesten kan kalle delfunksjonene (trend, grense) og bygge statusrekkefølgen i R4 selv. Da får vi akkurat divergensen AD-1 skal hindre (FR27: «Status for hver uke a er den statusen appen viser»). To andre veier til divergens er heller ikke stengt:

- **Parametere.** Ingenting hindrer at backtesten får CLI-flagg for vindu og horisont «for å eksperimentere». Det bryter FR27a.
- **`Lusegrense uke`.** BarentsWatch-kolonnen er en snarvei: en agent kan lese grensen rett fra kolonnen for det innebygde datasettet. Opplastede CSV-filer har ikke kolonnen, så de innebygde og de opplastede dataene ville fått grensen fra to ulike kilder. PRD §7 sier at kolonnen bare skal brukes som fasit i tester. NFR3 mangler i Capability map.

Regelen «Kjernen importerer ikke …» blir også håndhevet bare så lenge noen husker den i review.

**Forslag:** Legg til i Rule for AD-1: «Kjernen har ett offentlig inngangspunkt, `vurder(serie, omrade, analyseuke) -> Vurdering`, som både API-et og backtesten kaller. R2- og R4-parameterne er konstanter i kjernen og kan ikke overstyres (FR27a). `Lusegrense uke` leses bare i NFR3-testen, aldri inn i `Serie`. En pytest sjekker at `marin.kjerne` bare importerer fra stdlib og aldri kaller `date.today` eller `datetime.now` (AD-5).» **Handling:** Rett selv.

### M2: API-formen er utsatt til koden, men frontend skal bygges samtidig

**Sted:** AD-3 (linje 61–73) og Deferred-radene «Arbeidsdeling» og «Detaljer i Pydantic-modellene» (linje 222 og 227).

- Deferred begrunner utsettelsen av A3 med at «AD-3 gjør at backend og frontend kan bygges hver for seg». Samtidig er feltene i `Detaljsvar` utsatt til koden. `schema.ts` finnes først når Pydantic-modellene finnes. Bygges frontend parallelt, gjetter den feltene. Da glir formene fra hverandre, og det er nettopp det AD-3 skal hindre.
- Ingenting gjør at `schema.ts` blir generert på nytt. Glemmer noen det etter en endring i en modell, ser alt grønt ut til noe feiler mens appen kjører. Genereringen fra `/openapi.json` krever dessuten en kjørende server, og spinen har ingen kommando for det.
- **Velgbare uker og standard analyseuke (FR7, FR25, AD-5).** Ingen eier lista over uker i velgeren, og heller ikke regelen om at uke 53 bare finnes i ISO-år som har den. Uten en regel regner frontend ut ISO-uker med `Date` (en kjent feilkilde) eller skriver 2026 uke 42 fast. Da finnes «nå» to steder, selv om AD-5 sier at det bare skal ligge i `marin.config`.

**Forslag:** Legg til i Rule for AD-3: «`frontend/openapi.json` genereres fra `app.openapi()` med et skript (uten kjørende server) og committes. `npm run gen:api` lager `schema.ts` fra fila. En pytest sammenligner `app.openapi()` med den committede fila. Anleggsinfo, opplastingssvaret og `Detaljsvar` har `analyseuke` og `velgbare_uker`. Frontend regner aldri ut ISO-uker eller standard analyseuke.» Gi også Deferred-raden om arbeidsdeling en betingelse: «Første backend-story lager alle svarmodeller med stub-ruter (kontrakt først) før frontend-stories som bruker dem.» **Handling:** Rett selv.

### M3: Koblingen mellom frontend og backend i utvikling og ved innlevering er ikke låst

**Sted:** AD-9 (linje 109), Konfigurasjon (linje 124) og «Miljøer» (linje 175).

- **Porter, base-URL og CORS.** I utvikling kaller `next dev` (3000) `uvicorn` (8000) og trenger en absolutt base-URL. Ved innlevering brukes relativ `/api`. Spinen sier «Ingen miljøvariabler», og `.gitignore` utelater `.env.*`, så den vanlige løsningen (`.env.development`) blir ikke committet. Hver bygger vil improvisere sin egen variant av base-URL og CORS-origin.
- **Statiske filer.** Starlettes `StaticFiles(html=True)` gjør ikke `/anlegg` om til `anlegg.html`, som er det Next lager som standard. Uten `trailingSlash: true` i `next.config` (som gir `anlegg/index.html`) gir `/anlegg?nr=…` 404 ved innlevering, men virker i `next dev`. Feilen blir altså bare synlig i innleveringsoppsettet. Statikk-mounten på `/` må også registreres etter `/api`-ruterne.

**Forslag (inn i AD-11 fra H1):** «Porter: uvicorn 8000, next dev 3000. `frontend/src/api/` bruker `http://localhost:8000` når `process.env.NODE_ENV === 'development'`, ellers relativ sti. Backend slår på CORS bare for `http://localhost:3000`. `next.config` har `output: 'export'` og `trailingSlash: true`. FastAPI monterer `StaticFiles(directory=<repo>/frontend/out, html=True)` på `/` etter `/api`-ruterne.» **Handling:** Rett selv.

### M4: Avvik fra kildene er ikke ført som åpne punkter

Spinen har ingen seksjon for åpne punkter, og tre avvik fra kildene er ikke ført noe sted:

1. **FR26** (se H2): PRD-teksten passer ikke med AD-4. Memloggen sier at PRD-en må omformuleres.
2. **Recharts mot EXPERIENCE.md** (Responsive & Platform): «Ingen tunge tredjepartsbiblioteker kun for grafen; arkitekturen avgjør.» Memloggen sier at Recharts ble et «seed-valg (ikke spurt)». Arkitekturen fikk ansvaret for dette valget, men tok det uten å vurdere kravet om en lett side på mobil med dårlig dekning. En graf med punkter, linje og trapp er en liten SVG-komponent. Velg enten håndskrevet SVG, eller behold Recharts og før begrunnelsen i memloggen.
3. **README peker på `https://g01-ervik-kristiansen.vercel.app/`**, men spinen sier «bare lokal kjøring i v1». Deferred-raden «Publisering på nett» sier at appen «kan publiseres senere uten endring i arkitekturen». Det er for optimistisk for Vercel og andre serverløse verter: datasettet lastes inn i minnet ved oppstart (AD-4, NFR8), og den modellen kan ikke flyttes uendret til serverløse funksjoner. Avklar om kurset forventer en publisert URL. Ellers bør lenken fjernes og begrunnelsen dempes («krever en vert med en vedvarende prosess»).

**Forslag:** Legg til en kort seksjon «Åpne punkter» med disse tre, med eier og frist («før epics»). **Handling:** Diskuter punkt 2 og 3, og rett punkt 1 selv.

### M5: Tall og uker formateres to steder etter regler som ikke er skrevet ned

**Sted:** AD-2, AD-6 (linje 91) og Konvensjoner. Backend lager tekster med tall og uker (AD-2: «grensen på 0,5 i uke 38», «Siste telling 0,61»). Frontend formaterer tabellen, ukevelgeren og akseetikettene (AD-6: `formatLus`). Reglene står bare spredt i EXPERIENCE.md: lusetall med to desimaler (0,41), grenser som 0,5 og 0,2, uke som «uke 42, 2026», og året utelates inne i en setning når det er det samme som året for analyseuka. Med to implementasjoner i to språk og uten en felles regel får vi fort «0,50» i tabellen og «0,5» i teksten, eller «2026-W42».

**Forslag:** Legg til én rad i Konvensjoner: «Formatering | Lusetall: 2 desimaler med komma. Grenser: 0,5 og 0,2. Uke: «uke X, ÅÅÅÅ», året utelates i setninger når det er samme år som analyseuka. Backend (tekstene i kjernen) og frontend (`lib/format.ts`: `formatLus`, `formatUke`) følger samme regel og testes mot de samme eksemplene.» **Handling:** Rett selv.

### M6: AD-2 sier imot lagtabellen om hvem som lager feilene ved opplasting

**Sted:** AD-2 (linje 59), lagtabellen (linje 31), kildetreet (linje 184) og AD-5 (linje 85). AD-2 sier at «Kjernen lager … opplastingsfeil (FR24)». Lagtabellen og kildetreet legger valideringen i `kilder`, og AD-5 sier at «inneværende år» leses i `kilder`. Feilene gjelder rader i en fil og hører hjemme i `kilder`. En agent som følger AD-2 bokstavelig, kan flytte valideringen inn i kjernen og trenge filsystemet eller klokka der. Det bryter AD-1 og AD-5.

**Forslag:** Endre AD-2 til «Backend eier alle tekster som avhenger av data eller regler: kjernen lager regeltekstene, `kilder` lager FR24-feilene.» **Handling:** Rett selv.

---

## Lav

- **L1: Lasting av datasettet og testbarhet.** Spinen sier ikke *hvordan* API-et får datasettet. KI-agenter laster det ofte på modulnivå når modulen importeres. Da leser alle API-tester med TestClient de rundt 9 MB med Excel, og testdata i `backend/tests/data/` kan ikke byttes inn. Forslag (én setning i AD-4 eller i Konvensjoner): «Datasettet og backtestresultatet lastes i FastAPI-`lifespan` og hentes i rutene via en dependency, slik at tester kan bytte inn testdata.» Merk også at `uvicorn --reload` leser Excel-filene på nytt for hver lagring i utvikling. Da slår trolig betingelsen for «Mellomlagring av innlest Excel» til med en gang.
- **L2: Drift er ikke omtalt.** Logging, oppførsel når Excel-filene mangler ved oppstart (stopp med en tydelig melding, i motsetning til den myke feilen i AD-10) og maks filstørrelse ved opplasting er ikke nevnt. Før dem under Deferred med én linje hver, f.eks. «standardloggen til uvicorn, ingen egen logging eller overvåking i v1».
- **L3: Stack.** `uv`, `openapi-typescript` og `Vitest` står som «gjeldende» og har ingen låst versjon (linteren fanger ikke dette fordi feltet har tekst). Lås versjonene, eller skriv at `uv.lock` og `package-lock.json` eier dem. **Sjekk TypeScript 7.0.2:** 7.x er den nye native kompilatoren. Verktøy som bruker JS-API-et til TypeScript (openapi-typescript bygger AST med `typescript`-pakken, og Next typesjekker ved build) kan støtte den dårligere. Ta en kort test før oppsettet låses, eller lås til siste 5.x eller 6.x.
- **L4: Hull i Capability map.** NFR3 mangler (→ kjerne R1 og en test mot `Lusegrense uke`, se M1). NFR6 og NFR7 er bundet av AD-er, men mangler i kartet. NFR11 står i `binds` men ingen andre steder. Skriv «README, ikke arkitektur». FR27a (frosne parametere) bør nevnes i raden for FR27–FR29 (se M1).
- **L5: AD-7 kan håndheves av kompilatoren.** Skriv at `farge` og `arsak` er `Literal`/`Enum` i Pydantic, slik at `openapi-typescript` lager union-typer og en ukjent kode feiler ved kompilering. `farge` kan utledes av `arsak`, så la kjernen gjøre utledningen ett sted.
- **L6: `resultat.json` kan bli utdatert.** Endres kjernen etter backtestkjøringen, viser FR19 tall som ikke stemmer med koden. Forslag: «`resultat.json` kjøres på nytt og committes i samme commit som endrer `marin.kjerne`.»
- **L7: Lint.** `lint_spine.py` ga 6 lave «placeholder»-funn: `{lokalitetsnr}` (linje 70, 71, 103 og 109), `{detail}` (linje 123) og `{nr}` (linje 206). Alle er stiparametere eller FastAPI-feltnavn, ikke maltokens. Ingen handling.

---

## Overspesifisering (kandidater for å kutte)

Spinen er stort sett slank. Bare små kutt er aktuelle:

- **O1: Konvensjoner, Tilgjengelighet (linje 127).** Raden gjentar EXPERIENCE.md (Accessibility Floor) for én komponent. Siste halvdel (tekstoppsummering fra API-et) er allerede dekket av AD-2. Erstatt raden med «EXPERIENCE.md (Accessibility Floor) og DESIGN.md er bindende», eller kutt den.
- **O2: Konvensjoner, Styling (linje 126).** «Kun lys modus, systemfonter» er bestemt i DESIGN.md. Behold bare regelen om tokens i `@theme` og at komponentene bare bruker tokennavn. Det er den delen som hindrer divergens.
- **O3: AD-8 (linje 103).** «Ved 404 vises forsiden» gjentar konsekvens (4) for FR6b. Behold nøkkelen og modulen, og kutt resten.

**Ikke legg inn** som svar på denne gjennomgangen: venting på 300 ms i ukevelgeren, `Suspense` rundt `useSearchParams`, fokusflyt, feilmeldingstekster eller feltene i Pydantic-modellene ut over toppnivået. Det er detaljer for stories. Rettelsene over bør bli én til tre setninger i eksisterende AD-er, én ny AD-11 og en kort seksjon for åpne punkter, ikke nye kapitler.

---

## Dekning: PRD-krav mot spinen

| Krav | Dekket av | Status |
| --- | --- | --- |
| FR1–FR3 | `kilder`, kjerne R1, AD-1, AD-5, AD-6 | Dekket |
| FR4–FR6, FR6a | `api`, frontend `/`, AD-3 | Dekket |
| FR6b | AD-8 | Dekket |
| FR7 | AD-5, AD-6 | Delvis: ingen eier lista over velgbare uker (M2) |
| FR8–FR14 | AD-1, AD-6, AD-7 | Dekket, men inngangspunktet er ikke låst (M1) |
| FR15–FR20a (inkl. FR15a, FR15b, FR19) | AD-2, AD-7, AD-10 | Dekket, formateringen er uavklart (M5) |
| FR21, FR21b, FR23, FR23a, FR24 | `kilder`, AD-2, AD-4 | Dekket, AD-2 sier imot lagtabellen (M6) |
| FR22 | AD-3, AD-4 | Delvis: flyten for flere anlegg er ikke bestemt (H2) |
| FR25, FR25a | AD-3, AD-4 | Delvis: velgbare uker i fila (M2), overlevering mellom sider (H2) |
| FR26 | AD-4 | Delvis: sier imot PRD-teksten, og mekanismen er uklar (H2) |
| FR27–FR29, FR27a | AD-1, AD-10 | Dekket, FR27a er ikke låst (M1) |
| NFR1, NFR9 | AD-9, Konfigurasjon | Delvis: installasjon, bygg og stier (H1) |
| NFR2, NFR10 | Konvensjoner, Testing | Dekket |
| NFR3 | – | **Mangler** (M1, L4) |
| NFR4, NFR5 | AD-2, AD-7 | Dekket, NFR5-formatering (M5) |
| NFR6, NFR7 | AD-4, AD-8, AD-1 | Dekket, men mangler i kartet (L4) |
| NFR8 | AD-4 (minnet) | Dekket |
| NFR11 | – | **Mangler** (README-krav, merk som ikke arkitektur) |

## Driftsrammen

| Dimensjon | Status |
| --- | --- |
| Miljøer (utvikling, innlevering, test) | Navngitt. Koblingen mellom dem er ikke låst (M3) |
| Installasjon og bygg | Ikke omtalt: krav til Node, `out/` i `.gitignore`, forståelsen av NFR1 (H1) |
| Stier og arbeidsmappe | Ikke omtalt (H1) |
| Vert og leverandør | Avgjort (lokalt), men README-lenken til Vercel sier noe annet (M4) |
| Drift (logging, oppstartsfeil, grenser) | Ikke omtalt (L2) |
| Datalivssyklus (datasett, `resultat.json`) | Stort sett avgjort (AD-10), regel for utdatert fil mangler (L6) |

## Det som fungerer (behold)

- Paradigmet er navngitt og har et diagram for avhengighetsretning. Det er en regel, ikke pynt.
- AD-5 (ingen systemdato) og AD-6 (løpende ukenummer bare i kjernen, uker som `{ar, uke}`) stenger hele feilklassen T12 beskriver.
- AD-9 fanger en ikke-opplagt begrensning (statisk eksport, ingen dynamiske ruter) og velger URL-er med query-parametere. Det er riktig valg.
- AD-10 har en myk feil som passer med konsekvens (3) i FR19.
- AD-7 gir faste koder som frontend kan velge stil fra uten å tolke tekst.
- Deferred har en begrunnelse på hver rad, og de fleste versjonene i Stack er låst.

## Foreslått rekkefølge for rettelsene

1. H1 og M3 samlet i én AD-11 «Kjøring, stier og miljøer».
2. H2: tre setninger i AD-4, pluss FR26 som åpent punkt.
3. M2: kontrakt først, `velgbare_uker` og test for avvik i OpenAPI i AD-3.
4. M1: inngangspunkt, parametere, `Lusegrense uke` og importtest i AD-1.
5. M4 til M6 og de lave funnene, deretter O1 til O3.
