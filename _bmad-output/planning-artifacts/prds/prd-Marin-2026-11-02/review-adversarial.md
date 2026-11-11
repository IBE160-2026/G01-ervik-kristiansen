---
title: "Adversarial review: PRD Marin"
reviewed: prd.md (draft, updated 2026-11-03, A1/A2 avgjort 2026-11-11)
against: ../../briefs/brief-Marin-2026-09-17/brief.md (R1–R6, T1–T10, SK1–SK5) og addendum.md
lens: adversarial (bmad-review)
date: 2026-11-11
---

# Adversarial review av PRD: Marin

## Konklusjon

PRD-en er ryddig og godt sporet, men kjernen i prognosen er fortsatt tvetydig etter A1: det er ikke definert om «uker til grensen» telles fra t eller fra analyseuka, og rekkefølgen mellom statusene er ikke fastsatt. Dermed kan to utviklere lage to ulike apper som begge består T1–T10, og SK2-backtesten kan gi ulik treffandel avhengig av tolkning. PRD-en bør ikke gå videre til epics og stories før funnene markert kritisk og høy er lukket.

| Alvorlighet | Antall |
|---|---|
| Kritisk | 2 |
| Høy | 9 |
| Middels | 8 |
| Lav | 6 |
| **Totalt** | **25** |

Hvert funn har: **Lokasjon**, **Problem**, **Tiltak** og **Konsekvens hvis det ikke rettes**.

---

## Kritisk

### K1 Uker til grensen telles fra t, men brukeren leser det fra analyseuka

- **Lokasjon:** FR8, FR9, FR12, FR18. Brief R2 (uker til grensen, t + k), R4, T10 («Med analyseuke 41 gir samme data prognose som i T8»).
- **Problem:** Etter A1 kan t være analyseuka − 1. R2 definerer k = 1…6 fra t, og T10 sier at analyseuke 41 med siste telling i uke 40 gir *samme* prognose som T8, altså «grensen nås om 4 uker (uke 44)». Sett fra uke 41 er det 3 uker. Ved k = 1 og t = analyseuka − 1 er «grensen nås om 1 uke» i realiteten *denne uka*. Det er ikke sagt om
  1. statusteksten «om X uker» skal regnes fra t eller fra analyseuka,
  2. rød/gul-grensene (1–3 / 4–6) gjelder k fra t eller fra analyseuka,
  3. horisonten på 6 uker gjelder fra t (da ser brukeren bare 5 uker fram fra analyseuka),
  4. FR9 «hvilken uke prognosen er regnet fra» betyr analyseuka eller t,
  5. «brudd nå» sjekkes mot grensen i uke t eller i analyseuka (eksempel: sør, telling 0,30 i uke 15, analyseuke 16. Grensen i uke 15 er 0,5, så ikke brudd nå. Men i uke 16 er grensen 0,2, og anlegget er reelt i brudd.)
- **Tiltak:** Bestem én referanseuke og skriv det rett inn i FR12/FR14/FR18: f.eks. «k regnes fra t. Teksten viser antall uker fra analyseuka (k − (analyseuke − t)). Er det tallet 0 eller mindre, vises rød "Brudd ventet denne uka".» Legg til et testtilfelle T11 for t = analyseuke − 1 med forventet tekst, og et for vårgrensen som faller mellom t og analyseuka.
- **Konsekvens:** Brukeren får oppgitt én uke for mye forvarsel i alle uker der siste telling er fra uka før, altså rundt halvparten av ukene ved telling annenhver uke. Backtesten (SK2) teller røde perioder fra ulike uker avhengig av tolkning, så treffandelen er ikke reproduserbar.

### K2 SK2 kan justeres til å bestå, og tallet er ikke regnet på nytt etter A1

- **Lokasjon:** M1, FR27, FR28, kap. 11 «Treffsikkerhet». Brief SK2, addendum «Grov backtest».
- **Problem:** Terskelen på 25 % er satt *etter* at skissen ga 28–29 %, og «appens egen backtest er den som avgjør». Gruppen skriver altså både modellen, backtesten og fasiten for backtesten. I tillegg er definisjonen åpen på punkter som flytter treffandelen:
  - Bryter en grå uke («ingen ny telling», «for lite data») en «sammenhengende periode med rød status», eller hoppes den over? A1 innfører nye grå uker som ikke fantes i skissen.
  - Hvilken uke er statusen knyttet til: analyseuka eller t (se K1)?
  - 26 brudd etter en uke uten telling er ikke kryssinger og faller ut av nevneren.
  - Det finnes ikke noe tak på falske alarmer, bare rapportering. Flere røde varsler gir ikke straff.
  - Skissen (28,8 %) er kjørt før A1. Ingen har sjekket at 25 % fortsatt holder med A1-regelen.
- **Tiltak:** Skriv backtest-algoritmen som pseudokode i PRD-en (iterasjon over analyseuker, hvilken uke statusen tilskrives, hvordan grå uker behandles i en rød periode). Lås den før appens backtest kjøres. Kjør skissen på nytt med A1 og før tallet inn i kap. 11. Vurder et tak eller en minstegrense for andelen røde varsler fulgt av brudd (i dag ca. 14 %), eller i det minste et krav om at tallet ikke blir lavere enn i skissen. Legg inn noen håndregnede backtest-tilfeller (kryssing med rød periode som starter 1, 2, 4 og 5 uker før, og med en grå uke midt i) som automatiske tester.
- **Konsekvens:** Sensor kan med rette si at suksesskriteriet er tilpasset resultatet. Tvetydighetene gjør at treffandelen kan «tolkes over 25 %» i stedet for å måles.

---

## Høy

### H1 Rekkefølgen mellom statusene er ikke definert

- **Lokasjon:** FR8, FR13, FR14, FR20. Brief R1, R2 (spesialtilfeller), R4.
- **Problem:** Flere tilstander kan gjelde samtidig, og verken PRD eller brief sier hvilken som vinner:
  - ukjent område + ingen ny telling
  - ingen ny telling + siste telling ≥ grensen (grå «ingen ny telling» eller rød «brudd nå»?)
  - for lite data + siste telling ≥ grensen (R2 sier «brudd nå: ingen prognose beregnes», så trengs det 3 tellinger for å melde brudd?)
  - ingen ny telling + for lite data
- **Tiltak:** Legg til en eksplisitt beslutningsrekkefølge i FR14, f.eks.: 1) ukjent område, 2) ingen ny telling, 3) brudd nå, 4) for lite data, 5) prognose. Legg til testtilfeller for minst brudd nå med under 3 tellinger og ukjent område med gammel telling.
- **Konsekvens:** Et anlegg som er i brudd kan vises som grått «for lite data». Det er den farligste feilen en varslingsapp kan gjøre, og ingen test fanger den.

### H2 Årsskiftet og ISO-uke 53 er ikke spesifisert presist nok

- **Lokasjon:** FR7, FR11, FR24. Brief R2 («ISO-uke som x-verdi … årsskiftet som sammenhengende tid»).
- **Problem:** «ISO-uke som x-verdi» tatt bokstavelig gir x = 52, 1, 2 over årsskiftet. Det er ikke sagt hvordan den sammenhengende tidsaksen skal lages. 2026 har 53 ISO-uker (1. januar 2026 er en torsdag), 2025 har 52. FR24 godtar «uke 1–53» uavhengig av år, så 2025 uke 53 blir godtatt selv om den ikke finnes. Horisonten t + k over årsskiftet (f.eks. t = 2026 uke 50 i en opplastet fil) må gi 2026 uke 53 og så 2027 uke 1–2. Ingen T-test dekker årsskiftet.
- **Tiltak:** Definer x eksplisitt (f.eks. antall uker siden mandag i ISO-uke 1, 2025, regnet fra ISO-datoer) og krev bruk av et ISO-kalenderbibliotek. FR24: avvis uke 53 for år som ikke har ISO-uke 53. Legg til testtilfeller med vindu over 2025→2026 og horisont over 2026 uke 53 → 2027.
- **Konsekvens:** Feil stigningstall og feil uke for grensen rundt nyttår. Det oppdages ikke i T1–T10.

### H3 Ingen regel for desimalpresisjon og avrunding ved sammenligning med grensen

- **Lokasjon:** FR11, FR12, FR13. Brief R1 («≥ grensen er brudd»), T5, T6, T8.
- **Problem:** Regresjonsestimater er flyttall. Data med 0,1 / 0,2 / 0,3 / 0,4 gir estimat «0,5» som i flyttall kan bli 0,49999999999999994 og dermed *ikke* ≥ 0,5. Addendum viser 49 rader som er nøyaktig lik grensen. Fasiten i T5, T6 og T8 forutsetter eksakt desimalregning. Det er heller ikke sagt hvordan estimater og lusetall rundes av i visningen.
- **Tiltak:** Bestem regelen: f.eks. «estimatet rundes til 2 desimaler (halv opp) før sammenligning», eller bruk av desimaltyper. Legg til et testtilfelle der estimatet treffer grensen nøyaktig.
- **Konsekvens:** Én uke forskjell i «uker til grensen» mellom implementasjoner, og T-tester som består eller feiler avhengig av plattform og rekkefølgen på summeringen.

### H4 Analyseuke for opplastede data kolliderer med FR7

- **Lokasjon:** FR7, FR8, FR25, J3.
- **Problem:** FR7 begrenser analyseuka til 2025 uke 1–2026 uke 42. FR25 setter analyseuka til «siste uke i fila», som kan være 2024 eller 2027. Det er uklart om
  - «siste uke» betyr siste rad eller høyeste (år, uke), og hva som skjer når fila ikke er sortert,
  - siste uke med eller uten telling (ender fila med to tomme uker, blir det straks grått «ingen ny telling»),
  - analyseuke-velgeren finnes for opplastede data. FR25 viser til FR15–FR20, ikke FR7–FR9, men skjermbilde 2 har velgeren.
- **Tiltak:** Skriv i FR25: analyseuka er høyeste (år, uke) i fila. Velgeren vises og er begrenset til fila sitt intervall. FR7-grensene gjelder bare det innebygde datasettet.
- **Konsekvens:** Utvikleren må gjette. Den enkleste implementasjonen klemmer analyseuka inn i 2025–2026 og gir feil eller tom prognose for opplastede filer.

### H5 Valideringen av opplastede filer har store hull

- **Lokasjon:** FR21, FR22, FR23, FR24, kap. 11 «Opplastede filer».
- **Problem:** Kap. 11 sier at FR24 må håndtere komma som desimaltegn, men FR24 sier ikke om komma skal avvises eller godtas. Det mangler også:
  - tegnkoding og BOM (kolonnenavnet `år` med «å» brytes av Excel-lagret CSV i Windows-1252, og semikolon som skilletegn i norsk Excel),
  - validering av `år` (tomt, 1999, 3000),
  - uke 53 i år uten uke 53 (H2),
  - om manglende rader og tomme verdier betyr det samme,
  - usortert rekkefølge,
  - tom fil, bare overskrift, svært store filer,
  - urimelig høye lusetall,
  - hvilke av sjekkene som gjelder Excel. «I hvilken rad» og «samme uke flere ganger» for Excel med flere lokaliteter må gjelde per lokalitet,
  - Excel der `Fylke` er fylt ut i noen rader og tom i andre (FR23 og FR23a overlapper da).
- **Tiltak:** Lag en valideringstabell i FR24: regel, eksempel, feilmelding, og om fila avvises eller får en advarsel. Ta inn komma, semikolon, koding, `år` og Excel-spesifikke regler. Lag testfiler for hver regel i testmappen (NFR9).
- **Konsekvens:** Den første fila en bruker lager i norsk Excel feiler med en uforståelig melding eller krasjer appen, altså akkurat det kap. 11 sier ikke skal skje.

### H6 FR19 viser ikke falske alarmer, selv om kap. 11 sier den gjør det

- **Lokasjon:** FR19, FR28, kap. 11 «Treffsikkerhet».
- **Problem:** Kap. 11 sier at mange røde varsler er falske alarmer og at «FR19 sørger for at brukeren får vite det». FR19 viser bare treffandelen. Andelen røde varsler fulgt av brudd (ca. 14 %) er det tallet brukeren trenger når status er rød, og det vises ikke. Det er heller ikke sagt hva som skjer hvis resultatfila fra FR28 mangler eller er laget med en eldre versjon av koden.
- **Tiltak:** FR19 skal vise begge tallene. FR28 skal legge en versjon/dato i resultatfila. Appen skal vise en tydelig tekst hvis fila mangler, i stedet for å krasje eller vise et gammelt tall uten å si det.
- **Konsekvens:** Brukeren får et for positivt inntrykk av et rødt varsel. Kap. 11 lover noe som ingen FR gir.

### H7 J2 lover sammenligning med det som faktisk skjedde, men ingen FR gir det

- **Lokasjon:** J2 trinn 3, FR8, FR16, FR17.
- **Problem:** J2 sier at brukeren «kan sammenligne med hva som faktisk skjedde de neste ukene». FR16 og FR17 viser bare de 5 ukene i vinduet og trendlinja. FR8 sier at data etter analyseuka ikke påvirker prognosen, men sier ikke om de skal *vises*. En utvikler kan med god samvittighet skjule dem.
- **Tiltak:** Legg til et krav: «Ved analyseuke før siste uke i datasettet viser grafen målte verdier for de 6 ukene etter analyseuka, tydelig skilt fra vinduet. De påvirker ikke prognosen.» Eller stryk løftet fra J2.
- **Konsekvens:** Demoen av J2, som er den viktigste måten å overbevise sensor om at forvarselet virker, mangler den delen som viser at det virker.

### H8 T1–T10 dekker ikke reglene som er lettest å gjøre feil

- **Lokasjon:** NFR2, kap. 10 (R6 / T1–T10 → NFR2). Brief R6, SK1.
- **Problem:** SK1 er bestått når T1–T10 består, men det finnes ingen test for: «brudd nå», negative estimater satt til 0, rekkefølgen mellom statusene (H1), årsskiftet (H2), estimat lik grensen (H3) eller tekst-forskyvningen i K1. T7 («fem ukers lusetall») og T9 («telling bare i uke t − 2 og t») mangler konkrete verdier, område og analyseuke, så fasiten er ikke fullstendig. T1–T4 tester bare den ene enden av vårperiodene. NFR3 dekker R1, men ingen ting tilsvarende finnes for R2–R4.
- **Tiltak:** Utvid R6 med T11–T16 for tilfellene over, med konkrete tall. Fyll ut T7 og T9. Endre SK1/NFR2 til «alle testtilfeller i R6».
- **Konsekvens:** SK1 kan bestås av en implementasjon som melder grønt for et anlegg i brudd. Testene gir falsk trygghet, også som kontroll på kode skrevet med KI (kap. 11).

### H9 Område utledes fra fritekst-fylke med «ellers sør» som standard

- **Lokasjon:** FR3, FR23. Brief R1 («Et anlegg er nord når … ellers sør»).
- **Problem:** Regelen er en negativ liste: alt som ikke er Nordland, Troms eller Finnmark, er sør. For det innebygde datasettet fanger NFR3 dette. For Excel-opplasting gjør det ikke det: «troms», «Troms og Finnmark», «Finnmárku», «Nordland fylke» eller en skrivefeil blir stille til «sør», og vårgrensen settes til feil uker.
- **Tiltak:** Bruk en positiv liste over gyldige fylkesnavn for både nord og sør, normaliser (store/små bokstaver, mellomrom, «Troms og Finnmark»). Ukjent verdi gir feil eller lar brukeren velge område (som FR23a), ikke «sør».
- **Konsekvens:** Et nordlig anlegg får sørgrense i uke 16–20 og 0,5 i uke 22–26. Varselet blir feil akkurat i perioden der grensen er strengest.

---

## Middels

### M1 Ikke definert hva detaljsiden viser ved grå status

- **Lokasjon:** FR16, FR17, FR20. Brief R4 («Ingen ny telling siden uke X»).
- **Problem:** Ved «ingen ny telling» er t ikke definert innenfor regelen, så «de 5 ukene i vinduet» (FR17) og grafen (FR16) mangler grunnlag. «Siden uke X» er udefinert når lokaliteten aldri har telt. Ifølge addendum har 165 av 1 092 lokaliteter ingen telling i det hele tatt, og de dukker opp i søket.
- **Tiltak:** Definer hva graf og tabell viser for hver grå status (f.eks. vinduet som slutter i analyseuka). Legg til en egen tekst for «ingen telling i datasettet», eller fjern slike lokaliteter fra søket.
- **Konsekvens:** Tom graf, krasj eller teksten «siden uke undefined» for 15 % av lokalitetene.

### M2 NFR8 kan ikke testes som den står

- **Lokasjon:** NFR8.
- **Problem:** «Vanlig bærbar PC» er ikke definert. Det er ikke sagt hva som måles (første visning, bytte av analyseuke, opplasting), og det er ingen grense for oppstartstid. Å lese inn ca. 100 000 rader fra xlsx kan ta lang tid, og NFR8 unntar dette eksplisitt («etter at appen har startet»).
- **Tiltak:** Angi maskin (f.eks. «gruppens egne bærbare»), handlingen som måles og hvordan det måles. Legg til et krav til oppstartstid (f.eks. under 30 sekunder), eller krev forhåndsprosessert data.
- **Konsekvens:** Kravet kan verken bestås eller feile, og sensor kan oppleve at appen «henger» ved oppstart uten at noe krav er brutt.

### M3 NFR1 «uten nettilgang» stemmer ikke med vanlig installasjon

- **Lokasjon:** NFR1, brief SK5.
- **Problem:** Installasjon av avhengigheter (npm/pip) krever nett. Biblioteker for grafer og fonter fra CDN gjør at appen ikke virker uten nett. Det er uklart om kravet gjelder installasjon eller kjøring.
- **Tiltak:** Skriv «etter installasjon av avhengigheter etter README krever appen ikke nettilgang. Ingen ressurser lastes fra CDN.»
- **Konsekvens:** Uklart om SK5 er oppfylt. En CDN-avhengighet kan gi tom graf hos sensor.

### M4 M3 «forstår status» måles bare ved at elementene finnes

- **Lokasjon:** M3, SK3, SK4, FR15–FR18.
- **Problem:** SK3 og SK4 sjekker at farge, symbol, tekst, graf og tabell vises. Ingen ting måler om en driftsleder uten datafaglig bakgrunn forstår dem. Brief og PRD sier selv at brukerne ikke er intervjuet.
- **Tiltak:** Legg til en enkel brukertest (f.eks. 3 personer får 3 skjermbilder og skal si hva status betyr og når grensen nås), eller endre M3 til noe som faktisk måles.
- **Konsekvens:** M3 kan meldes oppfylt uten at noe er undersøkt.

### M5 De første ukene i 2025 får «for lite data» av feil grunn

- **Lokasjon:** FR1, FR7, FR27.
- **Problem:** Datasettet starter i 2025 uke 1, så analyseuke 2025 uke 1–2 kan aldri ha 3 tellinger i vinduet, og uke 3–4 har avkortet vindu. Appen viser «for lite data» når grunnen er at datasettet starter der. Backtesten tar med disse ukene.
- **Tiltak:** Begrens FR7 til 2025 uke 5 og utover, eller gi en egen tekst. Si i FR27 at backtesten starter når vinduet er fullt.
- **Konsekvens:** Misvisende status og en liten skjevhet i backtesten.

### M6 «Samme format som BarentsWatch» og søk på lokalitetsnummer er tvetydige

- **Lokasjon:** FR4, FR22.
- **Problem:** FR22 sier ikke hvilke kolonner som er obligatoriske, hvilket ark som leses, eller om overskriften må ligge i rad 1. FR4 sier «delvis treff» for navn, men ikke om lokalitetsnummer skal gi eksakt treff eller treff på starten av nummeret. Æ/ø/å i søk er heller ikke nevnt.
- **Tiltak:** List obligatoriske kolonner (som i kap. 7) og arknavn i FR22. Skriv at nummersøk gir treff på starten av nummeret (eller eksakt).
- **Konsekvens:** Filer eksportert på en litt annen måte blir avvist. Søket oppfører seg ulikt fra det sensor forventer.

### M7 Samme anlegg gir grått i appen og prognose ved opplasting

- **Lokasjon:** FR3, FR23a. Brief R1, T7.
- **Problem:** Et anlegg uten fylke gir grått «ukjent område» i det innebygde datasettet, men om samme data lastes opp som Excel uten fylke, velger brukeren område og får prognose. Brukerens valg blir ikke kontrollert. Det kan være greit, men det er ikke skrevet som en bevisst beslutning.
- **Tiltak:** Skriv beslutningen og begrunnelsen inn i FR23a, eller la også det innebygde datasettet tilby valg av område.
- **Konsekvens:** Sensor ser inkonsekvent oppførsel og kan lese det som en feil.

### M8 Grafen: startpunkt for trendlinja og hvilke uker grensen vises for

- **Lokasjon:** FR16.
- **Problem:** «Trendlinja forlenget 6 uker fram» sier ikke om det er fra t eller fra analyseuka (henger sammen med K1). «Grensen per uke» sier ikke om grensen gjelder vinduet, horisonten eller begge.
- **Tiltak:** Skriv: x-aksen går fra t − 4 til t + 6, trendlinja og grensetrappen dekker hele aksen, og analyseuka markeres.
- **Konsekvens:** Grafen og teksten kan vise ulike uker for når grensen nås.

---

## Lav

### L1 Dokumentet er ikke oppdatert etter beslutningene 2026-11-11

- **Lokasjon:** frontmatter (`updated: 2026-11-03`), kap. 12 A1, kap. 13 punkt 1. Brief frontmatter (`status: final`, `updated: 2026-10-29`).
- **Problem:** Kap. 13 sier fortsatt «Lukke A1 og A2», som er gjort. A1 sier at NFR2 er endret, men NFR2 har ingen endring. Briefen er endret (R2, R4, T10) uten ny dato.
- **Tiltak:** Oppdater datoer og kap. 13. Rett eller fjern henvisningen til NFR2.
- **Konsekvens:** Senere steg vet ikke hvilken versjon som gjelder.

### L2 «Økta avsluttes» er ikke definert

- **Lokasjon:** FR26, J3 trinn 4.
- **Problem:** Lukket fane, omstart av server, tidsavbrudd? Midlertidige filer på disk?
- **Tiltak:** Skriv f.eks. «data holdes bare i minnet og forsvinner når fanen lukkes eller appen stoppes. Ingen filer skrives til disk.»
- **Konsekvens:** Liten, men FR26 kan ikke verifiseres.

### L3 «Siden uke X» uten år stemmer ikke med NFR5

- **Lokasjon:** NFR5, FR18, brief R4.
- **Problem:** NFR5 krever «uke 38, 2026», men R4-tekstene sier «siden uke X». Rundt nyttår er «siden uke 52» tvetydig.
- **Tiltak:** Bruk formatet i NFR5 i alle statustekster.
- **Konsekvens:** Uklar tekst rundt årsskiftet.

### L4 Ingen kontroll av det innebygde datasettet

- **Lokasjon:** FR1, FR3.
- **Problem:** FR24 sjekker duplikater i opplastede filer, men ingen ting sier hva som skjer ved dupliserte rader for samme lokalitet og uke i BarentsWatch-filene, eller om `Fylke` er ulikt for samme lokalitet i 2025- og 2026-fila.
- **Tiltak:** Legg til en kontroll ved innlesing som logger eller stopper ved duplikater og ulikt fylke.
- **Konsekvens:** Stille feil i sjeldne tilfeller.

### L5 Detaljsiden for CSV-opplasting mangler anleggsinfo

- **Lokasjon:** FR21, FR25, kap. 8 punkt 2.
- **Problem:** CSV-fila har ikke navn, nummer, kommune eller fylke, men detaljsiden skal vise «anleggsnavn og -info».
- **Tiltak:** Skriv hva som vises (f.eks. filnavnet og valgt område).
- **Konsekvens:** Liten, men utvikleren må gjette.

### L6 Ingen grense for antall treff i søket

- **Lokasjon:** FR4–FR6.
- **Problem:** Søket på «a» kan gi hundrevis av treff. Ingen ting er sagt om maks antall, sortering eller tomt søk.
- **Tiltak:** Angi sortering og en grense (f.eks. 50 treff og «avgrens søket»).
- **Konsekvens:** Lang, usortert liste og en dårligere opplevelse av SK3.

---

## Merknader

- K1, H1 og M8 henger sammen: alle følger av at A1 ble lagt inn i R2 uten at R2–R4 ble skrevet om rundt to ulike uker (t og analyseuka). Løs dem samlet.
- K2 og H6 overlapper: begge handler om at backtesten og det brukeren får vite om treffsikkerheten ikke henger sammen.
- Scope-listen i kap. 9 er ellers godt støttet av FR/NFR (FR26, FR29, NFR1, NFR7). Det eneste løftet uten krav bak er sammenligningen i J2 (H7).
