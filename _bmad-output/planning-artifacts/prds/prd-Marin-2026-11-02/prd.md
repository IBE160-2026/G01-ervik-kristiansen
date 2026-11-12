---
title: "PRD: Marin"
status: draft
created: 2026-11-03
updated: 2026-11-12
inputs:
  - briefs/brief-Marin-2026-09-17/brief.md
  - briefs/brief-Marin-2026-09-17/addendum.md
  - briefs/brief-Marin-2026-09-17/tilbakemelding-product-brief.md
  - prds/prd-Marin-2026-11-02/tilbakemelding-prd.md
---

# PRD: Marin

> **Status: utkast.** PRD-en settes til `final` når håndkontrollen av fasit (A4) og den første backtestkjøringen (A5) er gjort, og tallene i kap. 11 er oppdatert.

## 1. Formål og bakgrunn

Marin er en web-app som gir driftsledere og fiskehelseansvarlige ved norske lakseoppdrettsanlegg et forvarsel om at anlegget er på vei mot å bryte lakselusgrensen. Appen trekker en trendlinje gjennom de siste ukenes lusetall og sammenligner den med grensen som gjelder i hver av de kommende ukene.

Problemet, løsningen og avgrensningene er beskrevet i product brief (`briefs/brief-Marin-2026-09-17/brief.md`).

**Normativ kilde.** Briefen i commit `536e09f` er normativ for reglene R1–R5, testtilfellene T1–T12 og suksesskriteriene SK1–SK5. Tabellen under er en kortversjon, slik at kravene kan leses uten briefen. Hvis kortversjonen og briefen er uenige, gjelder briefen. Endres briefen, oppdateres PRD-en og commit-hashen her samme dag.

| Regel | Kortversjon | Brief |
|---|---|---|
| Grense | 0,2 voksne hunnlus per fisk i uke 16–21 (sør) og uke 21–26 (nord), ellers 0,5. En verdi ≥ grensen er brudd. Nord = Nordland, Troms og Finnmark, ellers sør. | R1 |
| Vindu | De 5 siste ukene, t − 4 til og med t. Minst 3 uker med telling, ellers «for lite data». t er høyst én uke eldre enn analyseuka, ellers «ingen ny telling». | R2 |
| Trend | Lineær regresjon med løpende ukenummer som x (årsskiftet er ett steg på +1). Estimatet avrundes til 2 desimaler, og negative estimater settes til 0. | R2 |
| Horisont | Uke a + 1 til og med a + 6, regnet fra analyseuka a. Hver uke sammenlignes med grensen som gjelder i den uka. | R2, R3 |
| Statusfarge | Rød: brudd nå eller grensen nås om 1–3 uker. Gul: 4–6 uker. Grønn: ingen kryssing innen 6 uker. Grå: ingen prognose. | R4 |
| Rekkefølge | 1) ukjent område, 2) ingen ny telling, 3) brudd nå, 4) for lite data, 5) prognose. Den første som slår til, gjelder. | R4 |

Andre ID-er fra briefen som brukes i PRD-en:

- **R6 / T1–T12:** testtilfeller med fasit
- **SK1–SK5:** suksesskriteriene i briefen, nummerert i samme rekkefølge

Hvert krav i PRD-en har en ID (FR, NFR), slik at epics, stories og tester kan vise til kravet. De åpne punktene A1–A5 (kap. 12) er PRD-ens egne ID-er. Briefen bruker ikke A-ID-er.

**Ordliste**

| Begrep | Betydning |
|---|---|
| Anlegg | Én lokalitet i BarentsWatch-dataene, identifisert med lokalitetsnummer. «Anlegg» og «lokalitet» betyr det samme. |
| Område | «Sør» eller «nord» etter R1. Avgjør hvilken vårgrense som gjelder. Mangler fylke, er området «ukjent» (FR3). |
| Grense | Lusegrensen for et område i en bestemt uke (R1). |
| Telling | En uke der `Voksne hunnlus` har en verdi (FR2). |
| Analyseuke (a) | Uka brukeren ser prognosen fra. Bare data til og med a brukes (FR7–FR8). |
| t | Siste uke med telling til og med a, høyst én uke eldre enn a (R2). Vinduet for trendlinja slutter i t. |
| Estimat | Verdien trendlinja gir for en kommende uke, avrundet til 2 desimaler (R2). |
| Uker til grensen | Antall uker fra a til første uke der estimatet er ≥ grensen (R2, R3). |
| Brudd nå | Siste målte verdi er ≥ grensen som gjelder i analyseuka. Gir rød status uten prognose (R2, R4). |
| Status | Resultatet appen viser for et anlegg og en analyseuke: rød, gul, grønn eller grå, alltid med symbol og tekst (R4). |
| Varsel | Rød status. Bare rød status regnes som varsel i backtesten og suksesskriteriene (R4, SK2). |
| Kryssing | En uke med telling ≥ grensen der forrige telling var under (SK2). |
| Rød periode | Sammenhengende uker med rød status. Alle andre statuser bryter den (SK2). |
| Treffandel | Andelen kryssinger der en rød periode begynte 2–4 uker før (SK2, M1). |
| Presisjon | Andelen varsler som ble fulgt av brudd innen 4 uker (M1-C, FR28). |
| Detaljside | Skjermbildet som viser status, graf, tabell og forklaringer for ett anlegg og én analyseuke (kap. 5.5, kap. 8). |

## 2. Mål

| ID | Mål | Måles ved |
|---|---|---|
| M1 | Brukeren får et forvarsel før grensen brytes, ikke bare et øyeblikksbilde | SK2: treffandel minst 25 % i backtesten |
| M1-C | Motmål til M1: varslene skal ikke være så ofte falske at de mister verdi | Presisjon (FR28), rapportert ved siden av treffandelen og vist i FR19. Se reaksjonen under. |
| M2 | Reglene er implementert riktig og kan kontrolleres av gruppen | SK1 (T1–T12 består) |
| M3 | Brukeren forstår status på ett anlegg uten datafaglig bakgrunn | SK3, SK4 |
| M4 | Sensor kan kjøre appen og testene selv | SK5 |

**Reaksjon på M1-C, bestemt før tallet er kjent:** er presisjonen under **20 %** i den endelige backtesten, omformuleres FR19-teksten og beskrivelsen i kap. 1, slik at Marin presenteres som en *tidlig indikator* som sier at brukeren bør følge ekstra med, ikke som et pålitelig varsel. M1-C avgjør ikke om SK2 er oppfylt.

## 3. Brukere

**Primærbruker:** driftsleder eller fiskehelseansvarlig ved ett oppdrettsanlegg. Har god kjennskap til lakselus og lusegrensene, men ingen datafaglig bakgrunn. Vil vite: *Hvor lenge har jeg før grensen nås, og hvor sikker er den vurderingen?*

**Sensor/fagperson:** vil kjøre appen lokalt, prøve den på kjente historiske situasjoner og se at reglene stemmer.

Sekundærbrukere (regionledere med mange anlegg) er ikke utforsket og er ikke med i v1. Derfor har v1 ingen samlet oversikt over alle anlegg.

## 4. Brukerreiser

Hovedpersonen i alle tre reisene er Kari, driftsleder på et anlegg på Hitra i Trøndelag (område sør). Hun kjenner lusegrensene godt, men har ingen datafaglig bakgrunn. Samme person brukes i UX-dokumentet (`ux-designs/ux-Marin-2026-11-11/EXPERIENCE.md`).

### J1 Sjekk status for mitt anlegg

*Onsdag morgen sitter Kari på kontoret. Siste telling er lagt inn, og hun vil vite om hun må planlegge avlusing de neste ukene.*

1. Kari åpner appen og søker opp anlegget sitt på navn eller lokalitetsnummer (FR4, FR6).
2. Hun velger anlegget fra treflisten, der kommune og fylke skiller det fra anlegg med samme navn (FR5).
3. Detaljsiden viser status med farge, symbol og tekst, de siste ukenes lusetall, trendlinja fram i tid, grensen per uke og estimert uke for når grensen nås (FR15–FR18).
4. Kari vurderer om tiltak må planlegges. Teksten om usikkerhet minner henne om hvor ofte varslene slår til (FR19).

### J2 Se hvilken status Marin ville vist tidligere

*Kari husker et brudd i vår og vil vite om Marin ville gitt varsel i tide, før hun stoler på statusen hun ser nå.*

1. Fra detaljsiden velger Kari en tidligere analyseuke, f.eks. noen uker før bruddet (FR7).
2. Appen regner prognosen på nytt med bare de dataene som fantes til og med den uka (FR8), og viser hvilken uke prognosen er regnet fra (FR9).
3. Kari ser hva Marin ville vist da. For å se hva som faktisk skjedde, velger hun en senere analyseuke.

### J3 Få prognose på egne lusetall

*Kari har nettopp talt lus. Tallet er ikke med i utdraget, og hun vil se prognosen med de nyeste tallene.*

1. Kari går til opplastingssiden og laster opp et Excel-uttrekk fra BarentsWatch eller en CSV-fil fra sitt eget regneark (FR21, FR21b, FR22).
2. For Excel-filer med fylke viser appen området den har utledet. For CSV-filer og Excel-filer uten fylke velger Kari område, sør eller nord (FR23, FR23a).
3. Appen validerer fila og viser feil på en forståelig måte (FR24), eller viser detaljsiden for de opplastede dataene (FR25).
4. Dataene lagres ikke. De forsvinner når fanen lukkes, når en ny fil lastes opp, eller når appen startes på nytt (FR26).

## 5. Funksjonelle krav

Krav som gjelder det brukeren ser, har **testbare konsekvenser** med konkrete verdier. En story er ferdig når alle konsekvensene for kravene den dekker, er oppfylt. Eksemplene bruker data fra testtilfellene i briefen (R6), og fasiten arver forbeholdet i A4 til den er kontrollert for hånd.

### 5.1 Datagrunnlag

| ID | Krav | Sporing |
|---|---|---|
| FR1 | Appen leser lusetall fra BarentsWatch-utdraget i `data/barentswatch/` (2025 uke 1 til og med 2026 uke 42). Uker etter 2026 uke 42 leses ikke inn. | Omfang, SK5 |
| FR2 | En uke regnes som «uke med telling» når `Voksne hunnlus` har en verdi. Uker uten verdi regnes som uker uten telling, og ingen verdier fylles inn. | R2 |
| FR3 | Område (sør/nord) utledes av kolonnen `Fylke` etter R1. Mangler fylke, får anlegget område «ukjent». | R1 |

### 5.2 Søk og valg av anlegg

| ID | Krav | Sporing |
|---|---|---|
| FR4 | Brukeren kan søke etter anlegg på lokalitetsnavn (delvis treff, uavhengig av store og små bokstaver) eller lokalitetsnummer. | J1, SK3 |
| FR5 | Treflisten viser lokalitetsnavn, lokalitetsnummer, kommune og fylke, slik at anlegg med like navn kan skilles fra hverandre. | J1, SK3 |
| FR6 | Gir søket ingen treff, viser appen en melding om det. | J1 |

### 5.3 Analyseuke

| ID | Krav | Sporing |
|---|---|---|
| FR7 | Brukeren kan velge analyseuke (ISO-år og ISO-uke) fra og med 2025 uke 1 til og med 2026 uke 42. Standardvalg er 2026 uke 42. Uke 53 kan bare velges for ISO-år som har uke 53. | J2 |
| FR8 | Prognosen for en valgt analyseuke bruker bare tellinger til og med analyseuka. Data etter analyseuka påvirker ikke prognosen. t er siste uke med telling til og med analyseuka, og kan være høyst én uke eldre enn analyseuka. Er t eldre enn det, gir appen ingen prognose og viser «ingen ny telling» (R2, R4). | J2, SK2, R2, T10 |
| FR9 | Detaljsiden viser teksten «Prognose regnet fra uke {uke}, {år}» i statusboksen. | J2 |

**Testbare konsekvenser**

- **FR7** (1) Uten eget valg er analyseuka 2026 uke 42. (2) 2026 uke 43 og 2024 uke 52 kan ikke velges. (3) 2025 uke 53 finnes ikke i valget, fordi ISO-året 2025 har 52 uker.
- **FR8** (1) Anlegg i sør med tellingene fra T5 (uke 30–34: 0,06 / 0,12 / 0,18 / 0,24 / 0,30) og en ekstra telling 0,90 i uke 36: prognosen med analyseuke 34 er identisk med prognosen når tellingen i uke 36 fjernes (gul, grensen nås om 4 uker). (2) Samme data med analyseuke 36 gir «✕ Brudd nå». (3) T10: analyseuke 42 med siste telling i uke 40 gir «– Ingen ny telling siden uke 40» og ingen prognose.
- **FR9** (1) Velges 2026 uke 30, står det «Prognose regnet fra uke 30, 2026». (2) Byttes analyseuka til uke 25, endres teksten, status, graf og tabell (FR15–FR17) samtidig. Ingen av dem viser den gamle uka. (3) Teksten vises også ved grå status og ved brudd nå.

### 5.4 Prognose og status

| ID | Krav | Sporing |
|---|---|---|
| FR10 | Appen finner gjeldende grense for et anlegg og en uke etter R1. | R1, T1–T4 |
| FR11 | Appen beregner trend med lineær regresjon etter R2: vindu på 5 uker, minst 3 tellinger, løpende ukenummer som x-verdi (årsskiftet er ett steg på +1), og estimatet avrundet til 2 desimaler før sammenligning med grensen. | R2, T5, T8, T12 |
| FR12 | Appen beregner «uker til grensen» med horisont 6 uker, regnet fra analyseuka (ikke fra siste telling), og sammenligner estimatet for hver kommende uke med grensen som gjelder i den uka. | R2, R3, T5, T6 |
| FR13 | Appen håndterer spesialtilfellene i R2: brudd nå, for lite data og negative estimater (settes til 0). | R2, T9 |
| FR14 | Appen setter status (rød, gul, grønn, grå) og statustekst etter R4, inkludert rekkefølgen når flere betingelser gjelder samtidig (ukjent område, ingen ny telling, brudd nå, for lite data, prognose). | R4, T5–T12 |

FR10–FR14 er beregninger. De testes automatisk med T1–T12 (NFR2) og trenger ingen egne konsekvenser utover fasiten i briefen.

### 5.5 Detaljside

| ID | Krav | Sporing |
|---|---|---|
| FR15 | Detaljsiden viser status med farge, symbol og tekst etter R4. | J1, SK3, SK4 |
| FR16 | Detaljsiden viser en graf med målte lusetall i vinduet, trendlinja forlenget til uke a + 6 og grensen per uke (som trapp når vårgrensen slår inn). | J1, SK3, R3 |
| FR17 | Detaljsiden viser en tabell med de 5 ukene i vinduet (uke og lusetall, eller «ikke telt»). | J1, SK3 |
| FR18 | Ved rød eller gul status (unntatt brudd nå) viser detaljsiden estimert ISO-uke for når grensen nås, og antall uker dit, regnet fra analyseuka. | J1, SK3, R2, T10 |
| FR19 | Detaljsiden viser en kort, fast tekst om at prognosen er en enkel trendberegning og ikke en garanti. Teksten viser treffandelen og presisjonen fra siste backtest i et språk brukeren forstår. Eksempel: «I en test på data fra 2025–2026 ga Marin varsel 2–4 uker før X % av bruddene. Av alle varsler ble Y % fulgt av brudd innen 4 uker.» Er presisjonen under 20 %, gjelder reaksjonen på M1-C. | M1, M1-C, SK2, brief: «Hva gjør dette annerledes» |
| FR20 | Ved grå status forklarer detaljsiden hvorfor det ikke finnes en prognose (for lite data, ingen ny telling eller ukjent område). | R4, T7, T9, T10 |
| FR20a | Når det ikke finnes prognose (grå status eller brudd nå), viser grafen og tabellen målte lusetall og grensen, men ingen trendlinje og ingen estimert uke. Ved «ingen ny telling» viser tabellen de 5 ukene før analyseuka. | R4, T7, T9–T11 |

**Testbare konsekvenser**

- **FR15** (1) T5 med analyseuke 34 gir gul farge og teksten «! Følg med: grensen kan nås om 4 uker». (2) T6 gir rød farge og «✕ Varsel: grensen nås om 2 uker». T11 gir rød farge og «✕ Brudd nå». (3) For hver av de sju statustekstene i R4 er teksten på skjermen tegn for tegn lik teksten i briefen, med symbolet først. (4) I et skjermbilde i gråtoner kan statusen fortsatt leses ut av symbol og tekst (NFR4).
- **FR16** (1) T5 med analyseuke 34: grafen viser 5 målte punkter (uke 30–34), en trendlinje fra uke 30 til uke 40 og en flat grenselinje på 0,5. (2) T6 med analyseuke 14: grenselinja er 0,5 i uke 15 og faller som en trapp til 0,2 i uke 16–20. (3) T8: uker uten telling (37 og 39) vises ikke som punkter, og ingen punkter vises med verdien 0.
- **FR17** (1) T8 med analyseuke 40: tabellen har radene uke 36–40 med 0,20 / ikke telt / 0,28 / ikke telt / 0,36. (2) Ukene skrives som ISO-uker på formen «uke 36, {år}» (NFR5). (3) Byttes analyseuka, viser tabellen vinduet for den nye uka.
- **FR18** (1) T5 med analyseuke 34: estimert uke er uke 38, og antall uker dit er 4. Den nøyaktige ordlyden bestemmes i UX-steget. (2) T10 med analyseuke 41: uke 44, om 3 uker, regnet fra analyseuka og ikke fra siste telling. (3) Ved grønn status, grå status og brudd nå vises ingen estimert uke.
- **FR19** (1) Tallene X og Y leses fra resultatfila til backtesten (FR28), ikke skrevet fast inn i koden. Endres fila, endres teksten neste gang appen startes. (2) Teksten vises for alle statuser, også grå. (3) Mangler resultatfila, vises teksten uten tall, og appen krasjer ikke.
- **FR20** (1) T9 gir «– For lite data» og en forklaring om at færre enn 3 av de 5 siste ukene har telling. (2) T10 med analyseuke 42 gir «– Ingen ny telling siden uke 40» og en forklaring om at siste telling er mer enn én uke eldre enn analyseuka. (3) T7 gir «? Ukjent område: grensen kan ikke bestemmes» og en forklaring om at anlegget mangler fylke i datasettet.
- **FR20a** (1) T11 (brudd nå): grafen viser punktene i uke 29 og 30 og grensen, uten trendlinje og uten estimert uke. (2) T10 med analyseuke 42: tabellen viser uke 37–41 med ikke telt / 0,28 / ikke telt / 0,36 / ikke telt. (3) T7: grafen og tabellen viser målte lusetall, men ingen grenselinje, fordi grensen ikke kan bestemmes.

### 5.6 Opplasting av egne lusetall

Opplasting er et tillegg til v1 (kap. 9) og bygges i denne rekkefølgen: Excel fra BarentsWatch (FR22) først, deretter CSV med komma (FR21), og til slutt norsk CSV-format (FR21b). FR21b kan kuttes alene.

| ID | Krav | Sporing |
|---|---|---|
| FR21 | Brukeren kan laste opp en CSV-fil for ett anlegg med kolonnene `år`, `uke` og `voksne_hunnlus`, komma som skilletegn, desimalpunktum og tegnkoden UTF-8. Kolonnenavn leses uavhengig av store og små bokstaver. Tom verdi betyr uke uten telling. | J3 |
| FR21b | Appen godtar også CSV med semikolon som skilletegn og desimalkomma (norsk Excel), og tegnkoden Windows-1252. Formatet finnes ut fra overskriftsraden. Kuttes FR21b, avviser appen slike filer med en feilmelding etter FR24. | J3 |
| FR22 | Brukeren kan laste opp et Excel-uttrekk i samme format som BarentsWatch-fila «Lakselus per fisk». Inneholder fila flere anlegg, velger brukeren ett etter opplasting. | J3 |
| FR23 | Ved Excel-opplasting der `Fylke` er utfylt, utleder appen område av `Fylke` etter R1, på samme måte som for det innebygde datasettet. Appen viser brukeren området (f.eks. «Område: sør (Vestland)»). Brukeren velger ikke område. | J3, R1 |
| FR23a | Ved CSV-opplasting, og ved Excel-opplasting der `Fylke` mangler eller er tom, velger brukeren område (sør eller nord). Grensen bestemmes ut fra valget etter R1. | J3, R1 |
| FR24 | Appen validerer fila og viser en feilmelding som sier hva som er galt og i hvilken rad: ukjent format (feilmeldingen nevner formatene som godtas), manglende kolonner, år utenfor 2000 til inneværende år, uke utenfor 1–53, eller uke 53 i et ISO-år som ikke har uke 53, negative eller ikke-numeriske lusetall, og samme uke flere ganger. Ugyldige filer gir ingen prognose. | J3 |
| FR25 | Etter vellykket opplasting vises samme detaljside som for BarentsWatch-anlegg (FR15–FR20a), med analyseuke lik siste uke i fila. Brukeren kan velge analyseuke blant ukene fila dekker. Intervallet i FR7 gjelder ikke for opplastede data. | J3 |
| FR26 | Opplastede data ligger bare i minnet til den kjørende appen og skrives aldri til disk. De forsvinner når fanen lukkes, når en ny fil lastes opp, eller når appen startes på nytt. | J3, NFR6 |

### 5.7 Backtest (utviklerverktøy)

| ID | Krav | Sporing |
|---|---|---|
| FR27 | Et skript kjører backtesten på hele datagrunnlaget etter definisjonen i SK2. Status for hver uke a er den statusen appen viser med analyseuke a, beregnet bare med data til og med a. Kryssinger og røde perioder bestemmes som i SK2: forrige telling i uke w − 1 eller w − 2, og alle andre statuser bryter en rød periode. | SK2, FR8 |
| FR27a | Parameterne i R2 og R4 (vindu 5 uker, minst 3 tellinger, horisont 6 uker, rød ved 0–3 uker) fryses før den endelige backtesten. Resultatet rapporteres uendret i README og refleksjonsrapporten, også om treffandelen er under 25 % eller presisjonen under 20 %. Parameterne justeres ikke for å nå tersklene. | SK2, M1-C |
| FR28 | Skriptet rapporterer antall grensekryssinger, antall treff, treffandel og presisjon (andelen varsler som ble fulgt av brudd innen 4 uker). Resultatet skrives til en fil i repoet, slik at FR19 kan vise både treffandelen og presisjonen. | SK2, M1-C, FR19 |
| FR29 | Backtesten vises ikke som egen side i appen i v1. | Beslutning 2026-11-03 (kap. 9) |

## 6. Ikke-funksjonelle krav

«Tilbakemelding» i sporingskolonnen viser til foreleserens tilbakemelding på product brief (`briefs/brief-Marin-2026-09-17/tilbakemelding-product-brief.md`).

| ID | Krav | Sporing |
|---|---|---|
| NFR1 | Appen kan kjøres lokalt etter oppskriften i README, med datasettet i repoet, uten API-nøkler, betalte kontoer eller nettilgang. | SK5 |
| NFR2 | T1–T12 finnes som automatiske tester og består. Testene kan kjøres med én kommando beskrevet i README. | SK1 |
| NFR3 | R1 testes i tillegg mot BarentsWatch-kolonnen `Lusegrense uke` som uavhengig fasit, med 0 avvik. | R1, addendum |
| NFR4 | Status kan forstås uten fargesyn: alltid farge, symbol og tekst sammen. | SK4 |
| NFR5 | Brukergrensesnittet er på norsk (bokmål). Uker vises som ISO-uker, f.eks. «uke 38, 2026». | SK3 |
| NFR6 | Appen behandler ingen personopplysninger. Lusetall per anlegg er offentlige data. | Tilbakemelding (sikkerhet og personvern) |
| NFR7 | Appen inneholder ingen KI eller språkmodell. Prognosen er ren statistikk. | Brief |
| NFR8 | Detaljsiden vises på under 2 sekunder på en vanlig bærbar PC etter at appen har startet. | SK3 |
| NFR9 | Ingen hemmeligheter eller nøkler ligger i repoet. Datasett ligger i `data/`, testdata i en egen testmappe. | Tilbakemelding (ryddighet i repoet) |
| NFR10 | Utover T1–T12 finnes automatiske tester for søk (FR4–FR6: delvis treff, store og små bokstaver, lokalitetsnummer, ingen treff), analyseuke (konsekvensene for FR7 og FR8), opplasting (FR21–FR24: én testfil per feiltype og per godkjent format, i testmappa) og backtest (FR27: et lite, konstruert datasett med kryssinger og treff regnet ut for hånd). Konsekvensene for detaljsiden (FR9, FR15–FR20a) testes automatisk der verdien kan hentes ut uten nettleser (tekster, tabellrader, estimert uke). Resten kontrolleres manuelt etter en sjekkliste i README. Sjekklisten er en ordrett kopi av konsekvensene i kap. 5.3 og 5.5. | Tilbakemelding (kvalitetssikring og testing) |
| NFR11 | README oppgir datakilden (BarentsWatch, «Lakselus per fisk»), lisens (NLOD), nedlastingsdato (27.10.2026) og hvordan dataene ble hentet. | Tilbakemelding, SK5 |

## 7. Data

**BarentsWatch-utdraget** (`data/barentswatch/lakselus_per_fisk_2025.xlsx` og `..._2026.xlsx`, ark «Lakselus per fisk»). Kolonner appen bruker:

| Kolonne | Bruk |
|---|---|
| `År`, `Uke` | ISO-år og ISO-uke |
| `Lokalitetsnummer`, `Lokalitetsnavn` | Identifisere og søke opp anlegg |
| `Kommune`, `Fylke` | Vises i treflisten. `Fylke` gir område (R1) |
| `Voksne hunnlus` | Lusetallet prognosen bygger på |
| `Lusegrense uke` | Bare som fasit i tester (NFR3), ikke i selve beregningen |

Øvrige kolonner (sjøtemperatur, produksjonsområde, koordinater og andre lusestadier) brukes ikke i v1.

**CSV for opplasting** (FR21), eksempel:

```
år,uke,voksne_hunnlus
2026,30,0.06
2026,31,0.12
2026,32,
2026,33,0.24
```

Samme fil i norsk format (FR21b):

```
år;uke;voksne_hunnlus
2026;30;0,06
2026;31;0,12
2026;32;
2026;33;0,24
```

## 8. Skjermbilder

1. **Forside / søk:** søkefelt, trefliste (FR4–FR6) og lenke til opplasting.
2. **Detaljside:** anleggsnavn og -info, analyseuke-velger, statusboks med «Prognose regnet fra», graf, ukestabell og usikkerhetstekst (FR7–FR20a).
3. **Opplasting:** filvelger, valg eller visning av område, eventuelt valg av anlegg, feilmeldinger (FR21–FR24).

Skissene ligger i UX-steget (`ux-designs/ux-Marin-2026-11-11/mockups/`).

## 9. Omfang

**V1 er ferdig** når prioritet 1 og 2 er ferdig og testet. Opplasting (prioritet 3) er et tillegg. V1 kan leveres uten opplasting.

1. **Kjerneflyt:** datagrunnlag, søk, analyseuke, prognose og detaljside (FR1–FR20a), med T1–T12 og konsekvensene i kap. 5.3 og 5.5.
2. **Backtest-skript** (FR27–FR29).
3. **Tillegg: opplasting av egne lusetall** (FR21–FR26), i denne rekkefølgen:
   - 3a. Excel fra BarentsWatch: FR22, FR23, FR23a, FR24, FR25, FR26.
   - 3b. CSV med komma og UTF-8: FR21.
   - 3c. CSV i norsk format: FR21b. Kuttes først ved tidsnød.

**Tillegg i PRD-en utover briefens omfang:** valg av analyseuke (J2, FR7–FR9) og opplasting av egne lusetall (J3, FR21–FR26). Begge er bevisste tillegg. Briefens omfang nevner dem ikke.

**Beslutninger 2026-11-03** (gruppens PRD-utkast, ført i `.memlog.md`): ingen samlet oversikt over anlegg i v1, backtesten finnes bare som skript (FR29), og opplastede data lagres ikke (FR26).

**Ute av v1** (fra briefen, pluss beslutningene 2026-11-03):

- Samlet oversikt over alle anlegg med status, filtrering og sortering (skisseres i UX-steget som mulig neste versjon, men bygges ikke i v1)
- Backtest som side i appen (finnes bare som skript, FR27–FR29)
- Lagring av opplastede data
- Sanntidsintegrasjon mot BarentsWatch-API-et
- Varsler på SMS, e-post eller push, og mobilapp
- Innlogging og flere selskaper
- Andre fiskehelseparametere enn lakselus
- Mer avansert prognosemodell, og temperatur- og sesongjustering (R5)
- Særskilte lusegrenser for tillatelser med kapasitetsøkning

## 10. Sporing fra brief til krav

| Brief | Dekket av |
|---|---|
| R1 | FR3, FR10, FR23, FR23a, NFR3 |
| R2 | FR2, FR8, FR11–FR13, FR18 |
| R3 | FR12, FR16 |
| R4 | FR14, FR15, FR20, FR20a, NFR4 |
| R5 | Omfang (ute av v1) |
| R6 / T1–T12 | NFR2 (T10: FR8, FR18, FR20; T11: FR14; T12: FR11). T5–T11 er også eksempeldata i konsekvensene i kap. 5.3 og 5.5. |
| SK1 | NFR2, NFR10 |
| SK2 | FR8, FR19, FR27, FR27a, FR28 |
| SK3 | FR4, FR5, FR15–FR18, NFR5, NFR8 |
| SK4 | FR15, NFR4 |
| SK5 | FR1, NFR1, NFR11 |

## 11. Forutsetninger og risiko

| Forutsetning eller risiko | Eier |
|---|---|
| **Treffsikkerhet:** tallene er fra den grove skissen i addendumet (2026-10-29), regnet før A1, før uker til grensen ble regnet fra analyseuka og før SK2 ble presisert 2026-11-11. Skissen ga omtrent 29 % treff og omtrent 14 % presisjon. Tallene regnes på nytt med FR27 (A5), og marginen til 25 % kan bli mindre. Er presisjonen fortsatt rundt 14 %, er den under grensen i M1-C, og Marin skal da presenteres som en tidlig indikator. | Gruppen (A5) |
| **Datakvalitet:** utdraget er et fast øyeblikksbilde lastet ned 27.10.2026. Senere rettinger hos BarentsWatch kommer ikke med. | Fredrik |
| **Opplastede filer:** filer laget for hånd kan ha komma som desimaltegn, feil kolonnenavn eller hull. FR21 og FR21b godtar de vanlige formatene, og FR24 avviser resten med en forståelig feilmelding uten at appen krasjer. | Den som bygger opplasting (avklares i A3) |
| **Kontroll på KI-ens arbeid:** regelkoden skrives med Claude Code. Gruppen regner ut fasiten i T1–T12 for hånd før regelkoden skrives. Denne fasiten er kontrollen. Fasit som ikke er kontrollert ennå, er merket «[FASIT MÅ KONTROLLERES FOR HÅND AV GRUPPEN]» i briefen (se A4). | Gruppen (A4) |
| **Briefen og PRD-en i takt:** reglene står i kortversjon i kap. 1. Endres briefen uten at PRD-en oppdateres, kan krav og fasit gli fra hverandre. | Fredrik |

## 12. Åpne punkter

A1–A5 er PRD-ens egne ID-er og har ingen sammenheng med briefen.

- ~~**A1 Hvilken uke er t når brukeren velger analyseuke?**~~ Avgjort 2026-11-11: t er siste uke med telling til og med analyseuka, høyst én uke eldre enn analyseuka. Ellers grå status «ingen ny telling». Ført inn i R2, R4 og T10 i briefen og i FR8, FR20 og NFR2.
- ~~**A2 Område for Excel-opplasting**~~ Avgjort 2026-11-11: område utledes av `Fylke` når det finnes. Brukeren velger område for CSV og for Excel uten fylke. Ført inn i FR23, FR23a, J3 og kap. 8.
- **A3 Teknisk stack og arbeidsdeling:** avklares med Ella i arkitektursteget. Eier: Fredrik og Ella.
- **A4 Håndkontroll av fasit:** gruppen regner ut fasiten for T5, T6, T8 og T10–T12 for hånd og fjerner merkingen i briefen. Gir håndregningen et annet svar, rettes briefen, kortversjonen i kap. 1 og konsekvensene i kap. 5 samme dag. Eier: gruppen. Må være gjort før epics og stories.
- **A5 Første backtestkjøring:** kjør FR27 så tidlig som mulig, før epics og stories, og oppdater tallene i kap. 11. Tallene avgjør om M1 holder, og om reaksjonen på M1-C slår inn. Eier: gruppen.

## 13. Neste steg

1. Håndkontroll av fasit for T5, T6, T8 og T10–T12 (A4).
2. Implementere backtest-skriptet (FR27–FR28) tidlig og kjøre det (A5). Oppdatere kap. 11, M1-C-vurderingen og eventuelt FR19.
3. Sette PRD-en til `final` når A4 og A5 er gjort.
4. Arkitektursteget: velge og begrunne stack, dataflyt og mappestruktur (A3).
5. Epics og stories med henvisning til FR- og NFR-ID-ene. README-sjekklisten for detaljsiden kopieres fra konsekvensene i kap. 5.3 og 5.5.
