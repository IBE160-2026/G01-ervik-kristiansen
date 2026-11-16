---
type: spine-review
lens: adversarial (byggerpar som følger alle AD-er og likevel bygger inkompatibelt)
target: ../ARCHITECTURE-SPINE.md
driving_spec: ../../../prds/prd-Marin-2026-11-02/prd.md
also_read: [../.memlog.md, EXPERIENCE.md, brief.md (R1–R4, T1–T12), addendum.md (dataanalyse)]
reviewed: '2026-11-16'
verdict: 'Ikke klar for epics og stories: 1 kritisk, 6 høye, 5 middels, 6 lave'
---

# Adversarial review av arkitekturspinen: Marin

## Dom

Spinen låser de store valgene godt. Reglene ligger bare i kjernen, serveren er tilstandsløs, typene genereres fra Pydantic, statuskodene er faste og systemdatoen brukes ikke. Men spinen låser for lite av *formene* i grenseflatene mellom enhetene:

- **`Serie` er udefinert.** Det viktigste delte objektet er nevnt fire steder og definert ingen steder. Området for opplastede data kan bæres både i serien og ved siden av den.
- **Opplastingsflyten er ingen protokoll.** Excel med flere anlegg, valgbare analyseuker og overføringen fra opplastingssiden til detaljsiden er bare beskrevet som en liste endepunkter.

Dermed kan to byggere, eller to KI-økter, følge AD-1 til AD-10 bokstavelig og likevel levere deler som ikke virker sammen. Feilene viser seg sent: når opplasting kobles på (prioritet 3), når backtesten kjøres (A5), eller først ved innleveringsbygget.

**Anbefaling:** lukk K1 og H1–H6 med nye eller strammede AD-er før epics og stories skrives. Forslagene står samlet i avsnittet *Foreslåtte AD-er*, klare til å limes inn.

| Alvorlighet | Antall |
| --- | --- |
| Kritisk | 1 |
| Høy | 6 |
| Middels | 5 |
| Lav | 6 |
| **Totalt** | **18** |

Hvert funn har disse delene:

- **Lokasjon**
- **Byggerpar:** A og B, som begge holder seg innenfor AD-ene
- **Hvorfor AD-ene ikke stopper det**
- **Konsekvens**
- **Tiltak**

## Metode

Gjennomgangen ser på enhetene ett nivå under spinen:

- **Backend:** `kjerne`, `kilder` (innebygd Excel, opplastet Excel og CSV), `api` (søk, anleggsinfo, to prognoseruter og opplasting) og `backtest`.
- **Frontend:** sidene `/`, `/anlegg` og `/opplasting`, med `src/api/` og `src/lib/`.

For hvert par ble det laget to byggere som leser spinen hver for seg. Der spinen tier, tar hver av dem det mest naturlige valget. Et par er et hull når begge valgene er lovlige etter AD-ene, men ikke passer sammen. Funnene er rangert etter hvor sannsynlig avviket er i praksis, ikke bare etter hvor ille det er i teorien.

---

## Kritisk

### K1 `Serie` har ingen eier og ingen form, og området kan bæres to steder

- **Lokasjon:**
  - lagtabellen («→ normalisert `Serie`»)
  - AD-1 (kjernen importerer ikke fra `kilder`)
  - AD-3 (`POST /api/opplasting` gir «normalisert serie», `POST /api/prognose` tar «(serie, område, analyseuke)»)
  - AD-4
  - konvensjonen «Område er `sor`, `nord` eller `ukjent`»
  - Deferred: «Detaljer i Pydantic-modellene»
- **Byggerpar:**
  - **A, `kilder` (opplasting):** lager `kilder/serie.py` med `Serie(lokalitetsnr: int, navn, kommune, fylke, omrade, tellinger: dict[(ar, uke), float])`. Området fylles ut med R1 fra fylket. En CSV uten fylke får `omrade="ukjent"`, som konvensjonen tillater. Uker uten verdi droppes, fordi serien skal være «normalisert».
  - **B, `kjerne`:** kan ikke importere `kilder.Serie` (AD-1), så B lager sin egen `list[Telling(ar, uke, verdi | None)]` der tomme uker er med.
  - **C, `api` (`POST /api/prognose`):** tar imot `{serie, omrade, analyseuke}`. Serien er «normalisert» og har allerede et `omrade`-felt, så C sender `serie.omrade` videre til kjernen.
  - **D, frontend `/opplasting`:** brukeren velger sør, og D sender `{serie: <slik den kom>, omrade: "sor", analyseuke}`.
- **Hvorfor AD-ene ikke stopper det:** AD-3 gjør Pydantic til fasit, men Deferred overlater formen til koden. Den som skriver Pydantic-modellen først, bestemmer formen. Ingen AD sier:
  - hvilket av de to områdefeltene som gjelder
  - om uker uten verdi er med i serien
  - hvor kjernens inndatatype bor
- **Konsekvens:** Hver CSV-opplasting gir «? Ukjent område: grensen kan ikke bestemmes», selv om brukeren valgte sør. T1–T12 består likevel, fordi de kaller kjernen direkte. I tillegg:
  - **Lokalitetsnummer:** `lokalitetsnr: int` er påkrevd hos A, men en CSV har ikke lokalitetsnummer. Det gir enten 422 eller et oppdiktet `0`, som så vises i statusboksen (FR15b).
  - **Tett eller glissen serie:** valget flytter standard analyseuke, og dermed status (se H3).
  - **Tre definisjoner av samme ting:** kjernens inndata, utdata fra `kilder` og formen i API-et. Det gir to oversettelser i `api`, én per prognoserute, som kan gli fra hverandre. Den ene ruta kan for eksempel glemme FR19-teksten.
  - **Avrunding av inndata:** ingen sier hvor den skjer. Et opplastet tall på 0,199 er brudd hvis `kilder` runder (0,20 ≥ 0,2), men ikke hvis bare kjernen runder estimatene. Tabellen viser «0,20» i begge tilfeller.
- **Tiltak:**
  - Ny **AD-11**: `Serie` defineres én gang, i kjernen, og området er aldri en del av den.
  - **AD-13**: ett felles `bygg_detaljsvar` for begge prognoserutene.

---

## Høy

### H1 To Excel-lesere for samme BarentsWatch-format

- **Lokasjon:**
  - lagtabellen («BarentsWatch-Excel, opplastet Excel og CSV → normalisert `Serie`»)
  - FR1, FR22 og FR23 («på samme måte som for det innebygde datasettet»)
  - PRD kap. 9: FR1 er prioritet 1, FR22 er prioritet 3a
  - addendum: én rad per lokalitet per uke, også uker uten rapport, og 2026 uke 43–44 er ufullstendige
- **Byggerpar:**
  - **A, innebygd laster (prioritet 1):**
    - leser med `pd.read_excel(sti, sheet_name="Lakselus per fisk")`
    - kutter etter `SISTE_UKE` og fjerner rader uten `Voksne hunnlus` med `dropna`
    - leser lokalitetsnummer som `int` og validerer ingenting
  - **B, opplastet Excel (prioritet 3a):** bygges uker senere, kanskje av en annen person eller KI-økt.
    - leser rad for rad med `openpyxl` for å få radnumrene FR24 krever
    - beholder tomme uker og leser lokalitetsnummer som tekst
    - validerer etter FR24, men kutter ikke
- **Hvorfor AD-ene ikke stopper det:** Spinen sier at `kilder` gjør begge deler, men ikke at det skal være én leser. Begge følger AD-1 (ingen regler i `kilder`) og AD-5 (A bruker `SISTE_UKE`).
- **Konsekvens:**
  - **Samme fil, ulike svar:** Kari laster opp nøyaktig samme 2026-fil som ligger i `data/barentswatch/`. Hun får en annen standard analyseuke (2026 uke 44 i stedet for 42, med de ufullstendige ukene fra addendumet) og en annen serie for samme anlegg. Det er nettopp «ulike svar for samme serie», som AD-1 skal hindre.
  - **Naiv sammenslåing:** slår noen sammen leserne uten å tenke seg om, følger kuttet etter uke 42 med inn i opplastingen. Da forsvinner nettopp de nye ukene brukeren lastet opp for å få med (J3).
  - **Dobbelt vedlikehold:** kolonnenavn, arknavn og typen til lokalitetsnummeret står to steder.
- **Tiltak:** ny **AD-12**: én leser for BarentsWatch-formatet.

### H2 Opplastingen er en liste med mulige svar, ikke en protokoll

- **Lokasjon:**
  - AD-3: `POST /api/opplasting` gir «normalisert serie, liste over anlegg å velge fra, eller `feil[]`»
  - AD-4: ingenting holdes på serveren etter svaret
  - FR22–FR24
  - EXPERIENCE: «Opplastingsskjema», «Excel med flere anlegg», «Område utledet»
- **Byggerpar:**
  - **A, `api` (opplasting):** serveren er tilstandsløs. Ved flere anlegg svarer den derfor bare `{anlegg: [...]}` og venter at frontend sender fila på nytt med `?lokalitetsnr=` for å få serien. Ved ett anlegg svarer den `{serie}`. Svaret har altså tre mulige former.
  - **B, frontend `/opplasting`:** leser tabellraden som ett svar med alt i og venter `{anlegg: [{…, serie}]}`, slik at valget kan gjøres lokalt uten ny opplasting.
- **Hvorfor AD-ene ikke stopper det:** Begge byggerne er tilstandsløse og bruker endepunktet i AD-3. Tabellen sier ikke om svaret er en union eller ett objekt, og heller ikke hvor mange kall et anleggsvalg krever.
- **Konsekvens:** Integrasjonen feiler på første ekte BarentsWatch-fil. Hullet trekker med seg flere uavklarte spørsmål:
  - **Duplikatsjekken** (FR24, «samme uke flere ganger»): CSV-byggeren sjekker på (år, uke). Gjenbrukes den for Excel, får en fil med 1 092 anlegg tusenvis av «duplikater» og avvises alltid. Nøkkelen må være (lokalitetsnr, år, uke).
  - **Feil i rader for andre anlegg** enn det brukeren skal velge: avvises hele fila, eller bare det anlegget? Det er ikke avgjort.
  - **Fylke per anlegg, ikke per fil:** FR23 og FR23a er formulert per fil. I en fil med flere anlegg kan ett anlegg ha fylke og et annet mangle det, så frontend må vite per anlegg om brukeren skal velge område.
  - **Størrelse:** et fullt utdrag har rundt 50 000 rader per år (addendum). Variant A leser en xlsx på 4–5 MB to ganger, og med `openpyxl` tar det flere sekunder hver gang. Variant B sender et par MB JSON til fanen. Begge virker, men valget må tas én gang.
- **Tiltak:** ny **AD-13**: opplastingssvaret har én form.

### H3 Ingen eier for listen over valgbare analyseuker og standarduka

- **Lokasjon:**
  - AD-3: ingen endepunkt eller felt for valgbare uker
  - AD-5: `SISTE_UKE` ligger i `marin.config`
  - AD-6: løpende ukenummer bare i kjernen
  - FR7 og FR25 («blant ukene fila dekker», «siste uke i fila»)
  - EXPERIENCE: «Analyseukevelger»
- **Byggerpar:**
  - **A, frontend `/anlegg`:** skriver `FORSTE = {2025, 1}`, `SISTE = {2026, 42}` og en egen `harUke53(ar)` i TypeScript. For opplastede data lager A ukelisten fra serien i minnet og bruker siste element som standard.
  - **B, backend:** holder `SISTE_UKE` i `config` og lar kjernen eie ISO-kalenderen. For opplastede data dropper `kilder` enten tomme rader (glissen serie) eller beholder dem (tett serie), alt etter hvem som skrev koden.
- **Hvorfor AD-ene ikke stopper det:** AD-1 forbyr frontend å regne ut status, trend, grense og estimert uke, men ikke å regne ut ISO-uker. AD-5 gjør `SISTE_UKE` til en backendkonstant, men ingen AD sier hvordan frontend får vite verdien.
- **Konsekvens:**
  - **Flere kopier:** `SISTE_UKE` finnes to steder. ISO-kalenderen finnes tre steder: i kjernen (T12), i `kilder` (FR24, uke 53) og i frontend (FR7).
  - **Uke 53:** 2026 har uke 53, fordi 1. januar 2026 er en torsdag. En opplastet fil som går over nyttår 2026/27, treffer akkurat dette tilfellet. En håndskrevet frontendkalender som antar 52 uker, hopper over uka.
  - **«Ukene fila dekker» har tre tolkninger:** radene i fila, ukene med telling, eller alle ISO-uker fra første til siste rad. Med telling annenhver uke gir tolkningene ulike lister. Kan Kari velge uke 41 i T10-situasjonen?
  - **Standarduka endrer status:** en fil som slutter med `2026,33,` (tom verdi) gir analyseuke 33 med tett serie, men 32 med glissen serie. «Uker til grensen» telles fra analyseuka (R2). Krysser trenden grensen i uke 36, gir det 3 uker og rød i det ene bygget, men 4 uker og gul i det andre.
  - **Uker etter `SISTE_UKE`:** en opplastet fil kan gå forbi `SISTE_UKE`, og til og med forbi dagens uke, fordi FR24 tillater hele inneværende år. Gjenbruker velgeren intervallet for innebygde data, forsvinner de nyeste ukene.
- **Tiltak:** ny **AD-14**: backend leverer valgbare analyseuker og standarduke, og kjernen eier ISO-kalenderen.

### H4 Nettlesertilstanden har ingen eier: opplastede data mellom sidene, og hva «ved åpning» betyr

- **Lokasjon:**
  - AD-4 («komponenttilstand», «forkastes når brukeren forlater detaljsiden»)
  - AD-8 («Ved åpning sjekkes nummeret»)
  - AD-9: `/opplasting` og `/anlegg?opplastet=1` er ulike sider
  - FR6a (2), FR6b og FR26
  - EXPERIENCE: «Ruting ved åpning», «Navigerer bort fra opplastede data» og «Område må velges» (valget beholdes ved ny fil i samme økt)
- **Byggerpar 1, opplastingssiden mot detaljsiden:**
  - **Variant 1:** A (`/opplasting`) holder serie, område og filnavn i `useState` på siden, slik AD-4 sier bokstavelig, og navigerer så til `/anlegg?opplastet=1`. Opplastingssiden forsvinner, og dataene er borte før detaljsiden får dem.
  - **Variant 2:** A legger dataene i en React-context i rotlayouten. B (`/anlegg`) tømmer dem i en `useEffect`-opprydding når siden forlates. I utvikling kjører React Strict Mode, som er standard i Next App Router, effektene to ganger: montering, opprydding og ny montering. Dataene tømmes da før de vises, men bare under `next dev`.
  - **Oppfrisking:** ingen har bestemt hva som skjer når brukeren laster `/anlegg?opplastet=1` på nytt og dataene er borte. Det kan bli blank side, krasj eller omdirigering.
- **Byggerpar 2, forsiden mot toppfeltet:**
  - **A, forsiden `/`:** leser `husketAnlegg` når siden lastes, og gjør `router.replace('/anlegg?nr=…')`. Det er «ved åpning» lest bokstavelig.
  - **B, toppfeltet:** logoen, «Bytt anlegg» og «Søk / bytt» lenker til `/`, slik EXPERIENCE sier.
  - **Resultat:** med et husket anlegg sendes brukeren straks tilbake til detaljsiden. Forsiden og søket kan ikke nås, og FR6a (2) brytes.
  - **Etiketten «Sist viste anlegg»:** detaljsiden vet ikke om den ble åpnet fra minnet. En naturlig test er `nr === husketAnlegg.hent()`, men den er alltid sann etter første visning, fordi detaljsiden selv lagrer nummeret hver gang den vises (EXPERIENCE, punkt 4).
- **Hvorfor AD-ene ikke stopper det:** AD-4 sier «komponenttilstand», men ikke hvilken komponent. AD-8 sier «ved åpning», men ikke hva åpning er.
- **Konsekvens:**
  - Opplastingen virker ikke, eller virker bare i det ene miljøet.
  - Med et husket anlegg kommer brukeren ikke tilbake til forsiden.
  - Etiketten «Sist viste anlegg» vises feil.
- **Tiltak:** ny **AD-15** (én eier for nettlesertilstand utenfor URL-en) og strammet **AD-9** (`&husket=1`).

### H5 Teksteierskapet har hull akkurat der backend og frontend møtes

- **Lokasjon:**
  - AD-2 (listen over backendtekster) og AD-6 (`formatLus`)
  - FR9, FR15 (3), FR18 og FR23
  - EXPERIENCE «Statusboks»: R4 + «(uke Y)»
  - EXPERIENCE «Accessibility Floor»: live-overskriften er «R4-teksten med eventuell (uke Y)»
  - kryssingsetiketten «✕ Varsel uke 44» i grafen
  - «Ukestabell»: overskriften og merket «Siste telling»
- **Byggerpar for statusoverskriften:**
  - **A, `kjerne`:** returnerer `overskrift = "! Følg med: grensen kan nås om 4 uker"`, tegn for tegn som briefen, slik AD-2 og T5 krever. I tillegg lager A en egen FR18-tekst, fordi AD-2 nevner «estimert uke-teksten (FR18)» som en egen tekst.
  - **B, frontend:** følger EXPERIENCE og viser overskriften med « (uke 38)» i det ene `aria-live`-elementet. Da har B bare dårlige valg:
    - B kan lime sammen tekst. Det bryter regelen om at frontend aldri endrer en tekst fra API-et, og det går galt med årstallet («uke 2, 2027»).
    - B kan vise FR18-teksten fra A som en ekstra linje, men den linja finnes ikke i UX-en.
  - **Hvis A i stedet legger « (uke 38)» inn i overskriften:** da feiler T5–T12 og FR15 (3).
- **Tekster som ingen av listene nevner:**
  - FR9 «Prognose regnet fra uke 42, 2026»
  - FR23 «Område: Trøndelag – grense som for sør», som avhenger av R1
  - kryssingsetiketten i grafen
  - tabelloverskriften «De 5 ukene før analyseuka», som avhenger av status
  - merket «Siste telling» (hvilken rad som er t, bestemmes av R2)

  Hver av dem kan lages både i backend og i frontend uten å bryte AD-2. Frontendlisten i AD-2 er bare «knapper, overskrifter, intro …», så den lukker ingenting.
- **Tall og uker formateres to steder:** kjernen skriver «0,5» og «0,41» i setningene, mens frontend formaterer tabell og akser med `formatLus`. Brukes `formatLus` på grensen, står det «0,50» i grafen og «0,5» i setningen rett under. Ukeformatet «uke 36, 2026» skrives også i begge ender.
- **Hvorfor AD-ene ikke stopper det:** AD-2 lister backendtekstene uten å skille mellom R4-teksten som testes og overskriften som vises. Listen over frontendtekster er åpen.
- **Konsekvens:**
  - Skjermleseren leser noe annet enn det testene sjekker.
  - Statusboksen skal kunne leses alene i et skjermbilde, men kan vise feil år for kryssingsuka.
  - Samme grense skrives på to måter på samme skjerm.
- **Tiltak:** stram **AD-2** og legg feltene inn i skjelettet i **AD-3**:
  - Backend eier alle tekster som inneholder data eller avhenger av et regelutfall.
  - Frontend eier en lukket liste med faste tekster og velger mellom dem bare ut fra AD-7-kodene.
  - Overskriften får to felt: `overskrift_r4`, som testes, og `overskrift`, som vises.
  - `formatLus`/`formatUke` og de tilsvarende Python-funksjonene testes mot samme testvektorer.

### H6 Ingen eier for FR8-kuttet, så backtesten kan se framtida

- **Lokasjon:**
  - AD-1 og AD-5 («Kjernen tar analyseuka som argument»)
  - FR8
  - FR27 («beregnet bare med data til og med a»)
  - AD-10
- **Byggerpar:**
  - **A, `kjerne`:** `lag_prognose(tellinger, omrade, analyseuke)` antar at kalleren allerede har kuttet serien ved analyseuka. A bruker analyseuka til horisonten og til sjekken for «ingen ny telling». «Siste målte verdi» (brudd nå) hentes som siste element i lista.
  - **B, `api` (`GET …/prognose`):** kutter serien ved analyseuka før kallet. Appen gir riktig svar.
  - **C, `backtest`:** sender hele serien for hver a, fordi «kjernen tar analyseuka som argument».
  - **D, `api` (`POST /api/prognose`):** skrevet av en annen person enn B, og kutter ikke.
- **Hvorfor AD-ene ikke stopper det:** AD-1 sier at alle kaller kjernen, men ikke hvem som kutter serien.
- **Konsekvens:**
  - **Backtesten bruker framtidige tellinger** til «brudd nå» og til å finne t. Treffandelen (SK2, M1) og presisjonen (M1-C, FR19) blir feil, uten at noen test feiler, fordi T1–T12 bare gir kjernen selve vinduet.
  - **FR8 virker bare for innebygde anlegg,** ikke for opplastede data.
  - **Konsekvensen er stor fordi A5 skal kjøres tidlig:** backtestkjøringen avgjør M1 og reaksjonen på M1-C.
- **Tiltak:** stram **AD-1**:
  - Kjernens inngang tar hele serien, og kjernen kutter selv.
  - Backtesten bruker samme inngang som API-et.
  - FR8 (1) testes både mot kjernen og mot backtesten.

---

## Middels

### M1 `Detaljsvar` sier ikke hva grafen og tabellen får, så frontend kan velge vinduet selv

- **Lokasjon:**
  - AD-1: frontend får ikke regne ut status, trend, grense og estimert uke. Vinduet, t og tabellradene er ikke nevnt.
  - AD-3 («`Detaljsvar`») og AD-6
  - FR16, FR17 og FR20a
- **Byggerpar:**
  - **A, `api` og `kjerne`:** sender `vindu: [{uke, verdi}]`, `trend: {stigning, konstantledd}` og `grense_per_uke`.
  - **B, frontend `/anlegg`:** har hele serien i minnet for opplastede data og plukker selv ut de 5 siste ukene før analyseuka. B regner også trendverdiene ut fra stigning og konstantledd. Men konstantleddet er uttrykt i løpende ukenummer, som etter AD-6 bare skal brukes inne i kjernen.
- **Konsekvens:**
  - **Vinduet ved «ingen ny telling»:** her er tabellen de 5 ukene før analyseuka, ikke t − 4 til t (FR20a (2)). Det går lett galt når vinduet regnes ut to steder.
  - **Graf i frontend:** grafens x-område (fra første uke i vinduet til a + 6) og grensetrappa over årsskiftet må da regnes ut i frontend.
  - **To kodeveier:** for innebygde anlegg kan ikke B gjøre det samme, fordi serien ikke ligger i fanen. De to visningene får hver sin kode.
- **Tiltak:**
  - Stram **AD-1**: frontend velger aldri vindu, t, tabellrader eller x-område.
  - Gi **AD-3** et skjelett for `Detaljsvar` med ferdige data:
    - `tabell.rader`: 5 rader, eldste først, med `siste_telling`
    - `graf.punkter`: ett punkt per uke, med `malt`, `trend` og `grense`
    - `kryssing`

### M2 `resultat.json` har ingen fast form, og reserveløsningen skjuler feilen

- **Lokasjon:** AD-10, FR19 (1)–(3), M1-C.
- **Byggerpar:**
  - **A, `backtest`:** skriver `{"kryssinger": 823, "treff": 240, "treffandel": 0.2916, "presisjon": 0.14}`.
  - **B, `api`:** leser `treffandel_prosent` og `presisjon_prosent`.
- **Hvorfor AD-ene ikke stopper det:** AD-10 beskriver innholdet med ord. Nøkler, enhet (andel eller prosent) og avrunding er ikke bestemt, og det finnes ingen felles modell. Etter diagrammet importerer ikke `backtest` fra `api`, og `api` importerer ikke fra `backtest`.
- **Konsekvens:**
  - **Feilen blir usynlig:** B finner ikke feltet og regner fila som ugyldig. FR19 vises da uten tall, og appen starter, akkurat slik AD-10 foreskriver. Feilen ser ut som riktig oppførsel og blir ikke oppdaget.
  - **M1-C og avrunding er uavklart:** ingen AD sier hvem som bytter til M1-C-ordlyden når presisjonen er under 20 %, eller hvordan prosenten avrundes.
- **Tiltak:** stram **AD-10**:
  - Skjemaet blir en dataklasse i kjernen, og en test skriver og leser fila.
  - Kjernen eier M1-C-teksten og avrundingen.
  - En ugyldig fil gir en tydelig advarsel ved oppstart.

### M3 Innleveringsbygget: FastAPI finner ikke `/anlegg`, og API-adressen i utvikling er ikke bestemt

- **Lokasjon:** AD-9, Structural Seed (Miljøer).
- **Byggerpar 1, sidene:**
  - **A, frontend:** bruker standard `next.config` (`output: 'export'`, uten `trailingSlash`). Eksporten blir da `out/anlegg.html` og `out/opplasting.html`.
  - **B, `api`:** monterer `StaticFiles(directory="frontend/out", html=True)` på `/`.
  - **Resultat:** Starlette legger ikke til `.html` på stien. Åpner brukeren `/anlegg?nr=…` direkte, eller laster siden på nytt, får hun Nexts `404.html`. Navigering inne i appen virker, så feilen viser seg først når sensor trykker F5 på detaljsiden.
  - **Rekkefølge:** monteres `/` før API-rutene er registrert, skygger den for `/api/*`.
- **Byggerpar 2, API-adressen i utvikling:**
  - **A, frontend:** kaller relativ `/api` og legger inn `rewrites` mot port 8000. Next støtter ikke `rewrites` sammen med `output: 'export'`.
  - **B, `api`:** slår på CORS for `localhost:3000` og venter at frontend bruker en absolutt adresse.
- **Konsekvens:** Begge byggerparene følger AD-9. Likevel virker enten innleveringen (NFR1, SK5) eller utviklingsoppsettet ikke.
- **Tiltak:** stram **AD-9**:
  - Sett `trailingSlash: true`.
  - Monter `StaticFiles` sist, og bare hvis `frontend/out` finnes.
  - Bestem API-basen: `''` i bygget, `http://127.0.0.1:8000` under `next dev`.
  - Legg til en røyktest i pytest.

### M4 R1 får ulike fylkesnavn fra innebygde og opplastede data

- **Lokasjon:**
  - AD-1 (R1 i kjernen)
  - FR3 og FR23
  - R1: «nord» når Nordland, Troms eller Finnmark, «ellers sør»
  - FR24: år fra og med 2000
- **Byggerpar:**
  - **A, `kjerne` (R1):** `"nord" if fylke in {"Nordland", "Troms", "Finnmark"} else "sor"`. Det gir 0 avvik mot `Lusegrense uke` for 2025–2026 (NFR3).
  - **B, `kilder` (opplasting):** sender fylket videre slik det står i fila.
- **Hvorfor AD-ene ikke stopper det:** De innebygde dataene har et lukket sett fylkesnavn, mens opplastede filer har et åpent sett. Det kan være eldre utdrag (FR24 tillater år fra 2000), mellomrom eller andre skrivemåter. Ingen AD sier hva et ukjent fylkesnavn betyr.
- **Konsekvens:**
  - **Feil grense uten feilmelding:** står det «Troms og Finnmark» eller et samisk eller tospråklig navn, gir «ellers sør» grensen for sør til et anlegg i nord: 0,2 i uke 16–21 i stedet for uke 21–26. Om eldre BarentsWatch-utdrag faktisk bruker datidens fylkesnavn, må sjekkes. Uansett gjelder hullet.
  - **Flere fylker per anlegg:** en fil kan ha flere fylkesverdier for samme anlegg. Det er ikke avgjort hvilken som gjelder, eller hvilken som vises i «Område: …».
- **Tiltak:** ta inn i **AD-11**:
  - R1 slår opp i en lukket tabell over kjente fylkesnavn, både nåværende og tidligere.
  - Et ukjent fylkesnavn som ikke er tomt, behandles som om fylket mangler. Ved opplasting velger brukeren da område. For innebygde data blir området `ukjent`.
  - Fylket for et anlegg er verdien på den nyeste raden.

### M5 Opplastingsfeil: radnummer, prefiks og taket på 20 har to mulige eiere

- **Lokasjon:**
  - konvensjonen «Feil»: `feil: [{rad, melding}]`, meldingen ferdig på norsk
  - AD-2 og FR24
  - EXPERIENCE: «Feil i fil», «Opplasting, flere enn 20 feil» og «Fila har N feil»
- **Byggerpar:**
  - **Radnummer:** CSV-byggeren bruker pandas-indeksen + 1, så første datarad er 1. Excel-byggeren bruker radnummeret fra `openpyxl`, der overskriften er rad 1 og første datarad er rad 2. Samme feil får ulikt radnummer etter filtype, og bare ett av dem stemmer med det Kari ser når hun åpner fila i Excel.
  - **Prefiks:** backend skriver «Rad 7: lusetallet «abc» er ikke et tall.» i `melding`, og frontend legger til «Rad {rad}: » foran. Resultatet blir «Rad 7: Rad 7: …». Det kan også bli motsatt: ingen av dem legger til prefikset.
  - **Taket på 20:** backend kutter `feil` til 20 for å levere «ferdige» feil, og frontend viser «Fila har 20 feil» for en fil med 57. Kutter ingen av dem, får en Excel-fil i feil format en liste på tusenvis av linjer.
  - **Feil i hele fila** (ukjent format, manglende kolonne) har ikke noe radnummer, men `rad` er ikke definert som valgfri.
- **Hvorfor AD-ene ikke stopper det:** Konvensjonen gir formen `{rad, melding}`, men ikke hva `rad` teller, om prefikset står i `melding`, eller hvem som kutter lista.
- **Konsekvens:** Feilmeldingene peker på feil rad, får dobbelt prefiks, eller gir feil antall feil i overskriften.
- **Tiltak:** stram konvensjonen «Feil»:
  - `rad` er det fysiske radnummeret slik regnearket viser det, der overskriften er rad 1. Feil i hele fila har `null`.
  - `melding` er hele linja, med prefikset.
  - Backend sender de 20 første feilene og `antall_feil`.
  - Frontend lager bare overskriften og halelinja, med faste tekster.

---

## Lav

### L1 Søk: sortering og antall treff

- **Problem:** `GET /api/anlegg?q=` sier ikke hvem som sorterer.
  - Python sorterer i kodepunktrekkefølge, med «Å» før «Æ» og «Ø».
  - `localeCompare('nb')` gir norsk rekkefølge: Æ, Ø, Å.

  Sorterer både backend og frontend, kan rekkefølgen i lista hoppe. Et søk på «a» gir dessuten hundrevis av treff.
- **Tiltak:**
  - Backend sorterer med norsk nøkkel og har et tak på antall treff, for eksempel 50 treff + `flere_treff: bool`.
  - Frontend sorterer aldri.

### L2 Anleggsinfo i fire modeller

- **Problem:** Fire svar bærer de samme anleggsfeltene:
  - treff i søket
  - `GET /api/anlegg/{nr}`
  - anleggslista ved opplasting («samme radoppsett som treflisten»)
  - topplinja i `Detaljsvar`

  Fire Pydantic-modeller gir fire genererte TypeScript-typer, og en felles `AnleggRad`-komponent må godta alle.
- **Tiltak:** én `AnleggInfo` i AD-3 som brukes overalt. `lokalitetsnr` kan være `null`, men bare for CSV.

### L3 Gamle svar ved rask ukebytting

- **Problem:** Prognosen regnes ut 300 ms etter siste endring i velgeren. Har frontend to kall ute samtidig, kan svaret for den gamle uka komme sist. FR9 (2) krever at ingenting viser den gamle uka.
- **Tiltak:**
  - `Detaljsvar.analyseuke` gjentar uka som faktisk ble brukt.
  - Frontend forkaster svar som ikke gjelder den valgte uka.
  - FR9-linja tegnes ut fra svaret, ikke ut fra velgeren.

### L4 CSV-formatgjenkjenning er delt på to stories

- **Problem:** FR21 (3b) og FR21b (3c) bygges hver for seg, og FR21b kan kuttes.
  - FR21-byggeren dekoder strengt som UTF-8 og svarer «ukjent format» før FR21b-koden får se fila.
  - Ingen sier hvordan BOM behandles (Excel lagrer «CSV UTF-8» med BOM).
  - Feilmeldingene om feil desimaltegn krever at begge formatene er kjent.
- **Tiltak:** én beslutningstabell i `kilder.csv`:
  - Tegnkoden prøves i rekkefølgen BOM, UTF-8, Windows-1252.
  - Skilletegnet leses fra overskriftsraden.
  - FR21b er en egen gren som kan slås av.

### L5 Serien valideres ikke på nytt i `POST /api/prognose`

- **Problem:** Serien kommer tilbake fra nettleseren, men FR24-valideringen ligger i `kilder` og kjører bare på filer. Den som bygger prognoseruta, har to dårlige valg:
  - stole på serien, slik at en duplikatuke eller uke 54 gir 500 fra kjernen
  - kopiere FR24-reglene inn i Pydantic, slik at reglene finnes to steder
- **Tiltak:**
  - Kjernens `Serie` sjekker sine egne invarianter: sortert, unike uker og gyldig ISO-uke.
  - Brudd gir `ValueError`, som `api` gjør om til 422.
  - FR24 brukes bare på filer.

### L6 «Inneværende år» har ingen vei inn i testene

- **Problem:** AD-5 sier at øvre årsgrense leses i `kilder` «og sendes inn», men ikke hvor den sendes inn. En test som venter at en fil fra 2027 avvises, blir rød 1. januar 2027.
- **Tiltak:**
  - Valideringen tar `inneverende_ar: int` som parameter.
  - Bare API-ruta leser klokka.
  - Testene sender inn 2026.

---

## Foreslåtte AD-er

Formatet følger spinen. Nye AD-er er merket `[PROPOSED]`. For AD-er som finnes fra før, står bare tillegget.

### AD-11 — `Serie` defineres én gang, i kjernen, uten område [PROPOSED]

- **Binds:** FR1–FR3, FR8, FR21–FR25, FR27, NFR2, NFR3
- **Prevents:** tre ulike former for serien, at området bæres to steder, og at inndata avrundes ulikt for opplastede og innebygde data (K1, M4, L5)
- **Rule:**
  - **Typene:** `marin.kjerne.modeller` (bare stdlib) eier `Uke(ar, uke)`, `Telling(uke, verdi: float | None)`, `Serie(tellinger)` og `AnleggInfo(lokalitetsnr: int | None, navn: str | None, kommune: str | None, fylke: str | None)`.
  - **Serien:**
    - `Serie` er sortert stigende og har én telling per uke som finnes som rad i kilden. Tom verdi er `None`. Ingen uker diktes opp.
    - `Serie` sjekker egne invarianter (unike uker, gyldig ISO-uke) og gir `ValueError` ved brudd.
  - **Avrunding:**
    - Inndata avrundes bare ett sted: kjernen avrunder hver verdi til 2 desimaler, halvdeler opp, når `Serie` lages. `kilder` avrunder aldri.
    - Dette er et forslag. Gruppen kan i stedet velge at FR24 avviser tall med mer enn 2 desimaler. Poenget er at regelen står ett sted.
  - **Område:**
    - Område er aldri et felt i `Serie` eller `AnleggInfo`. Det er alltid et eget argument til kjernen.
    - Innebygde anlegg får område fra `kjerne.omrade_fra_fylke(fylke)`, som returnerer `sor`, `nord` eller `ukjent`.
    - R1 slår opp i en lukket tabell over kjente fylkesnavn, både nåværende og tidligere. Et tomt eller ukjent navn gir `ukjent`.
    - Fylket for et anlegg er verdien på den nyeste raden.
    - Opplastede data får område fra forespørselen (AD-13).
  - **Modellene i API-et:** `kilder` returnerer kjernens typer, og `api` speiler dem én til én i Pydantic (`SerieDto = {tellinger: [{ar, uke, verdi}]}`).

### AD-12 — Én leser for BarentsWatch-formatet [PROPOSED]

- **Binds:** FR1, FR3, FR22–FR24, NFR3
- **Prevents:** at samme fil gir ulik serie som innebygd og som opplastet data, og at FR1-kuttet lekker inn i opplastingen (H1)
- **Rule:**
  - **Én funksjon:** `kilder.barentswatch` har én funksjon som gjør rader om til `list[(AnleggInfo, Serie)]` pluss `feil`. Arknavn, kolonnenavn og typer står bare der.
  - **Innebygd laster:** bruker funksjonen på begge filene, kutter etter `SISTE_UKE` og krever null feil. Kuttet etter `SISTE_UKE` (FR1) gjøres bare her. Gir dataene feil, stopper oppstarten med en tydelig melding.
  - **Opplasting:** bruker samme funksjon, kjører i tillegg FR24-reglene og kutter ikke.
  - **Duplikater:** nøkkelen for duplikatsjekken er (lokalitetsnr, år, uke).
  - **Test:** en testfil i `backend/tests/data/` leses begge veier, og testen sjekker at seriene er like til og med `SISTE_UKE`.

### AD-13 — Opplastingssvaret har én form [PROPOSED]

- **Binds:** FR21–FR25a
- **Prevents:** ulike tolkninger av «serie, liste … eller feil», at fila må lastes opp på nytt, og område per fil i stedet for per anlegg (H2, K1)
- **Rule:**
  - **Svaret fra opplastingen:** `POST /api/opplasting` svarer alltid HTTP 200 med:
    - `Opplastingssvar = {filnavn, anlegg: [OpplastetAnlegg], feil: [Feil], antall_feil}`
    - `OpplastetAnlegg = {info: AnleggInfo, serie, omrade_utledet: 'sor' | 'nord' | null, omrade_tekst: str | null, analyseuker: [Uke], standard_analyseuke}`
  - **CSV** gir ett anlegg, og `info` har verken nummer eller navn. Frontend viser da `filnavn` som tittel.
  - **Feil:** har fila minst én feil, uansett hvor, er `anlegg` tom (FR24: ugyldige filer gir ingen prognose).
  - **Valg av anlegg:** frontend velger anlegg lokalt og sender aldri fila på nytt.
  - **Prognosekallet:**
    - `POST /api/prognose` tar `{info, serie, omrade: 'sor' | 'nord', analyseuke}`.
    - `omrade` er påkrevd, og `ukjent` gir 422.
    - For Excel med fylke kopierer frontend `omrade_utledet`. Serveren utleder ikke området på nytt.
  - **Én funksjon for svaret:** begge prognoserutene bygger svaret med `bygg_detaljsvar(info, serie, omrade, analyseuke, kilde)`.

### AD-14 — Backend leverer valgbare analyseuker, og kjernen eier ISO-kalenderen [PROPOSED]

- **Binds:** FR7, FR8, FR24, FR25, FR27, AD-5, AD-6
- **Prevents:** at `SISTE_UKE` og logikken for uke 53 finnes i flere kopier, og at samme fil får ulik standarduke (H3)
- **Rule:**
  - **Én ISO-kalender:** `marin.kjerne.uker` er den eneste ISO-kalenderen i systemet (`neste`, `pluss`, `mellom`, `alle_uker(fra, til)`, `har_uke_53`).
    - `kilder` bruker den til FR24, og `backtest` bruker den til å gå gjennom ukene og til «w − 1 eller w − 2».
    - Løpende ukenummer forlater aldri kjernen.
  - **Valgbare uker:** `GET /api/anlegg/{lokalitetsnr}` og hvert `OpplastetAnlegg` inneholder `analyseuker` (nyeste først) og `standard_analyseuke`.
    - **Innebygde data:** fra 2025 uke 1 til og med `SISTE_UKE`. Standard er `SISTE_UKE`.
    - **Opplastede data:** alle ISO-uker fra første til siste rad i fila, også uker uten rad. Standard er uka på siste rad, uansett om den har verdi. Gruppen må bekrefte at dette er riktig tolkning av FR25.
  - **Ugyldig uke:** prognoserutene svarer 422 for en uke som ikke står i lista.
  - **Frontend:** har ingen kode for ISO-kalenderen og ingen kopi av `SISTE_UKE`.

### AD-15 — Én eier for nettlesertilstand utenfor URL-en [PROPOSED]

- **Binds:** FR6a, FR6b, FR25, FR25a, FR26, NFR6
- **Prevents:** at dataene forsvinner mellom opplastingen og detaljsiden, at forsiden ikke kan nås, og feil som bare viser seg med Strict Mode i utvikling (H4)
- **Rule:**
  - **Opplastede data:** `frontend/src/lib/opplastetData.ts` eier dem som en variabel på modulnivå, med funksjonene `sett`, `hent` og `tom`. Dataene ligger verken i React-state på en side eller i nettleserlagring.
    - **Innhold:** `{filnavn, anlegg: OpplastetAnlegg, omrade}`, pluss sist valgte område per filtype (EXPERIENCE: «Område må velges»).
    - **Settes:** bare av `/opplasting` når brukeren trykker «Vis prognose», rett før `router.push('/anlegg?opplastet=1')`.
    - **Tømmes:**
      - av en lytter i rotlayouten ved hvert ruteskifte til en annen side enn `/anlegg?opplastet=1`
      - når brukeren velger en ny fil
      - aldri i en `useEffect`-opprydding på detaljsiden
    - **Mangler data:** er lageret tomt på `/anlegg?opplastet=1`, gjør siden `router.replace('/opplasting')`.
  - **Husket anlegg:**
    - «Ved åpning» (AD-8) betyr første gang appen tegnes i nettleserfanen. `husketAnlegg.ts` har et flagg i minnet. Forsiden omdirigerer bare når flagget ikke er satt, og setter flagget uansett.
    - Omdirigeringen går til `/anlegg?nr={nr}&husket=1`. Detaljsiden viser «Sist viste anlegg» bare når `husket=1` står i URL-en.
    - Detaljsiden lagrer nummeret etter et vellykket `Detaljsvar` med `kilde = 'innebygd'`, aldri for opplastede data.
  - **Navigasjon:** all intern navigasjon bruker Next `<Link>` eller `router`, aldri `<a href>` til egne sider.

### Stramming av AD-1 [PROPOSED]

Legg til i **Rule**:

- **FR8-kuttet:** kjernens offentlige inngang tar hele serien og analyseuka. Kjernen ser selv bort fra tellinger etter analyseuka (FR8). Kallere kutter aldri serien.
- **Backtest:** `backtest` henter status fra den samme inngangen som `api` bruker til `Detaljsvar.status`.
- **Frontend:** velger aldri vindu, t, tabellrader, x-område eller hvilke uker som er valgbare. Alt dette kommer ferdig fra API-et.
- **Test:** FR8 (1) testes både mot kjernen og mot backtesten.

### Stramming av AD-2 [PROPOSED]

Erstatt siste setning i **Rule** med:

- **Backend** lager alle tekster som inneholder data eller avhenger av et regelutfall. Det gjelder også:
  - FR18 og «(uke Y)»
  - kryssingsetiketten i grafen
  - områdeteksten i FR23
  - linjene i opplastingsfeilene
- **Statusoverskriften:** `Detaljsvar.status` har to felt:
  - `overskrift_r4` er tegn for tegn som briefen og testes av T5–T12.
  - `overskrift` er R4-teksten + « (uke Y)», med årsregelen fra EXPERIENCE.

  Frontend viser bare `overskrift`, i live-elementet.
- **Frontend** eier bare tekstene i `frontend/src/tekster.ts`:
  - knapper, etiketter og overskrifter
  - introen, fargeforklaringen og lagringsnotisen
  - laste- og valgmeldingene
  - «Prognose regnet fra {uke}» og «Dine opplastede tall: {filnavn}»
  - «Fila har {antall_feil} feil …» og «… og {n} feil til»
- **Valg av fast tekst:** frontend velger mellom faste tekster bare ut fra AD-7-kodene, for eksempel tabelloverskriften ved `ingen_ny_telling`.
- **Formatering:**
  - `formatLus` (alltid 2 desimaler) og `formatUke` («uke 36, 2026») i frontend, og `format_lus` og `format_uke` i kjernen, testes mot de samme testvektorene i `backend/tests/data/format.json`.
  - Frontend formaterer aldri grenseverdier.

### Stramming av AD-3 [PROPOSED]

Legg til et minsteskjelett. Detaljene eies fortsatt av koden.

```text
Detaljsvar = {
  kilde: 'innebygd' | 'opplastet',
  anlegg: AnleggInfo,
  analyseuke: Uke,                                   # uka som faktisk ble brukt
  status: { farge, arsak, overskrift_r4, overskrift, forklaring },
  estimert_uke: { uke: Uke, uker_til: int } | null,
  tabell: { rader: [{ uke, verdi | null, siste_telling: bool }] },  # alltid 5, eldste først
  graf: { punkter: [{ uke, malt | null, trend | null, grense | null }],
          kryssing: { uke, tekst } | null },
  tekstoppsummering: str,
  usikkerhetstekst: str
}
```

- **`AnleggInfo`** er én modell. Den brukes i søk, anleggsinfo, opplasting og `Detaljsvar`.
- **Søkesvaret** sorteres av backend i norsk rekkefølge og har et tak på antall treff.

### Stramming av AD-9 [PROPOSED]

Legg til i **Rule**:

- **Next:** `next.config` har `trailingSlash: true`.
- **FastAPI:** monterer `StaticFiles(directory=frontend/out, html=True)` på `/` etter alle `/api`-ruter, og bare hvis mappa finnes.
- **API-adresse:**
  - `frontend/src/api/` bruker tom base (`''`) i bygget og `http://127.0.0.1:8000` når `NODE_ENV === 'development'`.
  - Next bruker ingen `rewrites`.
  - Backend tillater CORS fra `localhost:3000`.
- **Røyktest:** en pytest sjekker at `/anlegg/?nr=…` og `/opplasting/` gir 200, og at `/api/anlegg?q=…` gir JSON. Testen hoppes over når `out/` ikke finnes.

### Stramming av AD-10 [PROPOSED]

Legg til i **Rule**:

- **Skjema:** skjemaet er dataklassen `kjerne.Backtestresultat`, med feltene `versjon`, `antall_kryssinger`, `antall_treff`, `treffandel` og `presisjon`. Treffandel og presisjon er andeler fra 0 til 1.
- **Lesing og skriving:** `backtest` skriver og `api` leser fila bare gjennom `til_json` og `fra_json`. En test skriver og leser fila og sjekker at resultatet er likt.
- **FR19-teksten:**
  - Kjernen lager teksten og avrunder til hele prosent, halvdeler opp.
  - Når presisjonen er under 0,20, bytter kjernen til M1-C-ordlyden.
- **Manglende eller ugyldig fil:** gir FR19-teksten uten tall, som før, og i tillegg en advarsel på stderr ved oppstart.

### Stramming av konvensjonen «Feil» [PROPOSED]

- **Form:** `feil: [{rad: int | null, melding}]`.
- **`rad`:** radnummeret slik regnearket eller teksteditoren viser det, der overskriftsraden er rad 1. Feil i hele fila har `null`.
- **`melding`:** hele linja, med «Rad N: » foran.
- **Antall:** backend sender de 20 første feilene, sortert på rad, og `antall_feil`.
- **Årsgrense:** valideringen tar `inneverende_ar` som parameter (AD-5).

---

## Det spinen gjør godt

- **AD-1:** den funksjonelle kjernen, uten I/O og pandas, gjør R1–R4 testbare og lar appen og backtesten dele reglene. Det eneste hullet er hvem som kutter serien (H6).
- **AD-6 og AD-7:** faste statuskoder og `{ar, uke}` overalt lukker de vanligste avvikene mellom frontend og backend.
- **AD-4:** en tilstandsløs server er riktig valg for FR26. Det som mangler, er en eier for tilstanden i frontend (H4).
- **AD-10:** at `resultat.json` leses ved oppstart, holder tallene i FR19 ute av koden. Det som mangler, er et skjema (M2).

## Anbefalt rekkefølge

1. **AD-11 og AD-13**, før noen story for opplasting eller `POST /api/prognose` skrives (K1, H2).
2. **AD-12, AD-14 og strammet AD-1**, før første story for datagrunnlaget (FR1) og for backtesten (FR27, A5). A5 skal kjøres tidlig (H1, H3, H6).
3. **Strammet AD-2 og AD-3**, før første story for detaljsiden (H5, M1).
4. **AD-15 og strammet AD-9**, før storyene for forsiden og rutingen (H4, M3).
5. **Strammet AD-10 og konvensjonen «Feil»**, sammen med de storyene de gjelder (M2, M5).
