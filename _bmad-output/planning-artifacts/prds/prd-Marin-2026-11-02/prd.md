---
title: "PRD: Marin"
status: final
created: 2026-11-03
updated: 2026-11-11
inputs:
  - briefs/brief-Marin-2026-09-17/brief.md
  - briefs/brief-Marin-2026-09-17/addendum.md
  - briefs/brief-Marin-2026-09-17/tilbakemelding-product-brief.md
---

# PRD: Marin

## 1. Formål og bakgrunn

Marin er en web-app som gir driftsledere og fiskehelseansvarlige ved norske lakseoppdrettsanlegg et forvarsel om at anlegget er på vei mot å bryte lakselusgrensen. Appen trekker en trendlinje gjennom de siste ukenes lusetall og sammenligner den med grensen som gjelder i hver av de kommende ukene.

Problemet, løsningen og avgrensningene er beskrevet i product brief (`briefs/brief-Marin-2026-09-17/brief.md`). PRD-en gjentar ikke reglene. Den viser til dem med ID:

- **R1–R5:** regler for grense, trend, sammenligning, statusfarge og temperatur
- **R6 / T1–T12:** testtilfeller med fasit
- **SK1–SK5:** suksesskriteriene i briefen, nummerert i samme rekkefølge

Hvert krav i PRD-en har en ID (FR, NFR), slik at epics, stories og tester kan vise til kravet.

**Ordliste**

| Begrep | Betydning |
|---|---|
| Anlegg | Én lokalitet i BarentsWatch-dataene, identifisert med lokalitetsnummer. «Anlegg» og «lokalitet» betyr det samme. |
| Telling | En uke der `Voksne hunnlus` har en verdi (FR2). |
| Analyseuke (a) | Uka brukeren ser prognosen fra. Bare data til og med a brukes (FR7–FR8). |
| t | Siste uke med telling til og med a, høyst én uke eldre enn a (R2). Vinduet for trendlinja slutter i t. |
| Uker til grensen | Antall uker fra a til første uke der estimatet er ≥ grensen (R2, R3). |
| Kryssing | En uke med telling ≥ grensen der forrige telling var under (SK2). |
| Rød periode | Sammenhengende uker med rød status. Alle andre statuser bryter den (SK2). |

## 2. Mål

| ID | Mål | Måles ved |
|---|---|---|
| M1 | Brukeren får et forvarsel før grensen brytes, ikke bare et øyeblikksbilde | SK2 (backtest, minst 25 % treff) |
| M2 | Reglene er implementert riktig og kan kontrolleres av gruppen | SK1 (T1–T12 består) |
| M3 | Brukeren forstår status på ett anlegg uten datafaglig bakgrunn | SK3, SK4 |
| M4 | Sensor kan kjøre appen og testene selv | SK5 |

## 3. Brukere

**Primærbruker:** driftsleder eller fiskehelseansvarlig ved ett oppdrettsanlegg. Har god kjennskap til lakselus og lusegrensene, men ingen datafaglig bakgrunn. Vil vite: *Hvor lenge har jeg før grensen nås, og hvor sikker er den vurderingen?*

**Sensor/fagperson:** vil kjøre appen lokalt, prøve den på kjente historiske situasjoner og se at reglene stemmer.

Sekundærbrukere (regionledere med mange anlegg) er ikke utforsket og er ikke med i v1. Derfor har v1 ingen samlet oversikt over alle anlegg.

## 4. Brukerreiser

### J1 Sjekk status for mitt anlegg

1. Brukeren åpner appen og søker opp anlegget sitt på navn eller lokalitetsnummer.
2. Brukeren velger anlegget fra treflisten.
3. Detaljsiden viser status (farge, symbol og tekst), de siste ukenes lusetall, trendlinja fram i tid, grensen per uke og estimert uke for når grensen nås.
4. Brukeren vurderer om tiltak må planlegges.

### J2 Se hvordan varselet ville sett ut tidligere

1. Fra detaljsiden velger brukeren en tidligere uke, f.eks. noen uker før en kjent overskridelse.
2. Appen regner prognosen på nytt med bare de dataene som fantes til og med den uka.
3. Brukeren ser hva Marin ville varslet da. For å se hva som faktisk skjedde, velger brukeren en senere analyseuke.

### J3 Få prognose på egne lusetall

1. Brukeren går til opplastingssiden og laster opp en CSV-fil eller et Excel-uttrekk fra BarentsWatch.
2. For Excel-filer med fylke viser appen området den har utledet. For CSV-filer og Excel-filer uten fylke velger brukeren område (sør eller nord).
3. Appen validerer fila og viser feil på en forståelig måte, eller viser detaljsiden for de opplastede dataene.
4. Dataene lagres ikke. De forsvinner når fanen lukkes, når en ny fil lastes opp, eller når appen startes på nytt (FR26).

## 5. Funksjonelle krav

### 5.1 Datagrunnlag

| ID | Krav | Sporing |
|---|---|---|
| FR1 | Appen leser lusetall fra BarentsWatch-utdraget i `data/barentswatch/` (2025 uke 1 til og med 2026 uke 42). Uker etter 2026 uke 42 leses ikke inn. | Omfang, SK5 |
| FR2 | En uke regnes som «uke med telling» når `Voksne hunnlus` har en verdi. Uker uten verdi regnes som uker uten telling, og ingen verdier fylles inn. | R2 |
| FR3 | Område (sør/nord) utledes av kolonnen `Fylke` etter R1. Mangler fylke, får anlegget område «ukjent». | R1 |

### 5.2 Søk og valg av anlegg

| ID | Krav | Sporing |
|---|---|---|
| FR4 | Brukeren kan søke etter anlegg på lokalitetsnavn (delvis treff, uavhengig av store og små bokstaver) eller lokalitetsnummer. | SK3 |
| FR5 | Treflisten viser lokalitetsnavn, lokalitetsnummer, kommune og fylke, slik at anlegg med like navn kan skilles fra hverandre. | SK3 |
| FR6 | Gir søket ingen treff, viser appen en melding om det. | — |

### 5.3 Analyseuke

| ID | Krav | Sporing |
|---|---|---|
| FR7 | Brukeren kan velge analyseuke (ISO-år og ISO-uke) fra og med 2025 uke 1 til og med 2026 uke 42. Standardvalg er 2026 uke 42. Uke 53 kan bare velges for ISO-år som har uke 53. | J2 |
| FR8 | Prognosen for en valgt analyseuke bruker bare tellinger til og med analyseuka. Data etter analyseuka påvirker ikke prognosen. t er siste uke med telling til og med analyseuka, og kan være høyst én uke eldre enn analyseuka. Er t eldre enn det, gir appen ingen prognose og viser «ingen ny telling» (R2, R4). | J2, SK2, R2, T10 |
| FR9 | Detaljsiden viser tydelig hvilken uke prognosen er regnet fra. | J2 |

### 5.4 Prognose og status

| ID | Krav | Sporing |
|---|---|---|
| FR10 | Appen finner gjeldende grense for et anlegg og en uke etter R1. | R1, T1–T4 |
| FR11 | Appen beregner trend med lineær regresjon etter R2: vindu på 5 uker, minst 3 tellinger, løpende ukenummer som x-verdi (årsskiftet er ett steg på +1), og estimatet avrundet til 2 desimaler før sammenligning med grensen. | R2, T5, T8, T12 |
| FR12 | Appen beregner «uker til grensen» med horisont 6 uker, regnet fra analyseuka (ikke fra siste telling), og sammenligner estimatet for hver kommende uke med grensen som gjelder i den uka. | R2, R3, T5, T6 |
| FR13 | Appen håndterer spesialtilfellene i R2: brudd nå, for lite data og negative estimater (settes til 0). | R2, T9 |
| FR14 | Appen setter status (rød, gul, grønn, grå) og statustekst etter R4, inkludert rekkefølgen når flere betingelser gjelder samtidig (ukjent område, ingen ny telling, brudd nå, for lite data, prognose). | R4, T5–T12 |

### 5.5 Detaljside

| ID | Krav | Sporing |
|---|---|---|
| FR15 | Detaljsiden viser status med farge, symbol og tekst etter R4. | SK3, SK4 |
| FR16 | Detaljsiden viser en graf med målte lusetall i vinduet, trendlinja forlenget 6 uker fram og grensen per uke (som trapp når vårgrensen slår inn). | SK3, R3 |
| FR17 | Detaljsiden viser en tabell med de 5 ukene i vinduet (uke og lusetall, eller «ikke telt»). | SK3 |
| FR18 | Ved rød eller gul status viser detaljsiden estimert ISO-uke for når grensen nås, og antall uker dit, regnet fra analyseuka. | SK3, R2, T10 |
| FR19 | Detaljsiden viser en kort, fast tekst om at prognosen er en enkel trendberegning og ikke en garanti. Teksten viser begge tallene fra siste backtest i et språk brukeren forstår: hvor stor andel av bruddene Marin varslet rødt 2–4 uker før (treffandel), og hvor stor andel av de røde varslene som ble fulgt av brudd innen 4 uker. Eksempel: «I en test på data fra 2025–2026 varslet Marin rødt 2–4 uker før X % av bruddene. Av alle røde varsler ble Y % fulgt av brudd innen 4 uker.» | M1, SK2, «Hva gjør dette annerledes» |
| FR20 | Ved grå status forklarer detaljsiden hvorfor det ikke finnes en prognose (for lite data, ingen ny telling eller ukjent område). | R4, T7, T9, T10 |
| FR20a | Når det ikke finnes prognose (grå status eller brudd nå), viser grafen og tabellen målte lusetall og grensen, men ingen trendlinje og ingen estimert uke. Ved «ingen ny telling» viser tabellen de 5 ukene før analyseuka. | R4, T7, T9–T11 |

### 5.6 Opplasting av egne lusetall

| ID | Krav | Sporing |
|---|---|---|
| FR21 | Brukeren kan laste opp en CSV-fil for ett anlegg med kolonnene `år`, `uke` og `voksne_hunnlus`. Appen godtar to formater og finner formatet ut fra overskriftsraden: komma som skilletegn med desimalpunktum, eller semikolon som skilletegn med desimalkomma (norsk Excel). Kolonnenavn leses uavhengig av store og små bokstaver, og fila kan være i UTF-8 eller Windows-1252. Tom verdi betyr uke uten telling. | J3 |
| FR22 | Brukeren kan laste opp et Excel-uttrekk i samme format som BarentsWatch-fila «Lakselus per fisk». Inneholder fila flere anlegg, velger brukeren ett etter opplasting. | J3 |
| FR23 | Ved Excel-opplasting der `Fylke` er utfylt, utleder appen område av `Fylke` etter R1, på samme måte som for det innebygde datasettet. Appen viser brukeren området (f.eks. «Område: sør (Vestland)»). Brukeren velger ikke område. | J3, R1 |
| FR23a | Ved CSV-opplasting, og ved Excel-opplasting der `Fylke` mangler eller er tom, velger brukeren område (sør eller nord). Grensen bestemmes ut fra valget etter R1. | J3, R1 |
| FR24 | Appen validerer fila og viser en feilmelding som sier hva som er galt og i hvilken rad: ukjent format (feilmeldingen nevner de to formatene som godtas), manglende kolonner, år utenfor 2000 til inneværende år, uke utenfor 1–53, eller uke 53 i et ISO-år som ikke har uke 53, negative eller ikke-numeriske lusetall, og samme uke flere ganger. Ugyldige filer gir ingen prognose. | J3 |
| FR25 | Etter vellykket opplasting vises samme detaljside som for BarentsWatch-anlegg (FR15–FR20a), med analyseuke lik siste uke i fila. Brukeren kan velge analyseuke blant ukene fila dekker. Intervallet i FR7 gjelder ikke for opplastede data. | J3 |
| FR26 | Opplastede data ligger bare i minnet til den kjørende appen og skrives aldri til disk. De forsvinner når fanen lukkes, når en ny fil lastes opp, eller når appen startes på nytt. | J3, NFR6 |

### 5.7 Backtest (utviklerverktøy)

| ID | Krav | Sporing |
|---|---|---|
| FR27 | Et skript kjører backtesten på hele datagrunnlaget etter definisjonen i SK2. Status for hver uke a er den statusen appen viser med analyseuke a, beregnet bare med data til og med a. Kryssinger og røde perioder bestemmes som i SK2: forrige telling i uke w − 1 eller w − 2, og alle andre statuser bryter en rød periode. | SK2, FR8 |
| FR27a | Parameterne i R2 og R4 (vindu 5 uker, minst 3 tellinger, horisont 6 uker, rød ved 0–3 uker) fryses før den endelige backtesten. Resultatet rapporteres uendret i README og refleksjonsrapporten, også om treffandelen er under 25 %. Parameterne justeres ikke for å nå terskelen. | SK2 |
| FR28 | Skriptet rapporterer antall grensekryssinger, antall treff, treffandel og andelen røde varsler som ikke ble fulgt av brudd innen 4 uker. Resultatet skrives til en fil i repoet, slik at FR19 kan vise både treffandelen og andelen røde varsler som ble fulgt av brudd. | SK2, FR19 |
| FR29 | Backtesten vises ikke som egen side i appen i v1. | Beslutning 2026-11-03 |

## 6. Ikke-funksjonelle krav

| ID | Krav | Sporing |
|---|---|---|
| NFR1 | Appen kan kjøres lokalt etter oppskriften i README, med datasettet i repoet, uten API-nøkler, betalte kontoer eller nettilgang. | SK5 |
| NFR2 | T1–T12 finnes som automatiske tester og består. Testene kan kjøres med én kommando beskrevet i README. | SK1 |
| NFR3 | R1 testes i tillegg mot BarentsWatch-kolonnen `Lusegrense uke` som uavhengig fasit, med 0 avvik. | R1, addendum |
| NFR4 | Status kan forstås uten fargesyn: alltid farge, symbol og tekst sammen. | SK4 |
| NFR5 | Brukergrensesnittet er på norsk (bokmål). Uker vises som ISO-uker, f.eks. «uke 38, 2026». | SK3 |
| NFR6 | Appen behandler ingen personopplysninger. Lusetall per anlegg er offentlige data. | Tilbakemelding |
| NFR7 | Appen inneholder ingen KI eller språkmodell. Prognosen er ren statistikk. | Brief |
| NFR8 | Detaljsiden vises på under 2 sekunder på en vanlig bærbar PC etter at appen har startet. | SK3 |
| NFR9 | Ingen hemmeligheter eller nøkler ligger i repoet. Datasett ligger i `data/`, testdata i en egen testmappe. | Tilbakemelding, ryddighet |
| NFR10 | Utover T1–T12 finnes automatiske tester for søk (FR4–FR6: delvis treff, store og små bokstaver, lokalitetsnummer, ingen treff), analyseuke (FR8: data etter analyseuka påvirker ikke prognosen), opplasting (FR21–FR24: én testfil per feiltype og per godkjent format, i testmappa) og backtest (FR27: et lite, konstruert datasett med kryssinger og treff regnet ut for hånd). Detaljsiden (FR15–FR20a) kontrolleres manuelt etter en sjekkliste i README. | Tilbakemelding (testing) |
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

## 8. Skjermbilder

1. **Forside / søk:** søkefelt, trefliste (FR4–FR6) og lenke til opplasting.
2. **Detaljside:** anleggsnavn og -info, analyseuke-velger, statusboks, graf, ukestabell og usikkerhetstekst (FR7–FR20a).
3. **Opplasting:** filvelger, valg eller visning av område, eventuelt valg av anlegg, feilmeldinger (FR21–FR24).

Skisser av skjermbildene lages i arkitektur- eller UX-steget.

## 9. Omfang

**Med i v1:** alt i kap. 5 og 6.

**Prioritet:** kjerneflyten skal være ferdig og stabil før noe annet bygges.

1. Kjerneflyt: datagrunnlag, søk, analyseuke, prognose og detaljside (FR1–FR20a), med T1–T12.
2. Backtest-skript (FR27–FR29).
3. Opplasting av egne lusetall (FR21–FR26). Kuttes først ved tidsnød.

**Tillegg i PRD-en utover briefens omfang:** valg av analyseuke (J2, FR7–FR9) og opplasting av egne lusetall (J3, FR21–FR26). Begge er bevisste tillegg. Briefens omfang nevner dem ikke.

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
| R6 / T1–T12 | NFR2 (T10: FR8, FR18, FR20; T11: FR14; T12: FR11) |
| SK1 | NFR2, NFR10 |
| SK2 | FR8, FR19, FR27, FR27a, FR28 |
| SK3 | FR4, FR5, FR15–FR18, NFR5, NFR8 |
| SK4 | FR15, NFR4 |
| SK5 | FR1, NFR1, NFR11 |

## 11. Forutsetninger og risiko

- **Treffsikkerhet:** tallene under er fra den grove skissen i addendumet (2026-10-29), regnet før A1, før uker til grensen ble regnet fra analyseuka og før SK2 ble presisert 2026-11-11. Skissen ga omtrent 29 % treff, og bare omtrent 14 % av de røde varslene ble fulgt av brudd. Tallene må regnes på nytt med FR27, og marginen til 25 % kan bli mindre. Mange røde varsler er altså falske alarmer. Det er et legitimt funn, og FR19 sørger for at brukeren får vite det. V1 har bevisst ingen terskel for andelen falske alarmer: den rapporteres (FR28) og vises (FR19), men avgjør ikke om SK2 er oppfylt.
- **Datakvalitet:** utdraget er et fast øyeblikksbilde lastet ned 27.10.2026. Senere rettinger hos BarentsWatch kommer ikke med.
- **Opplastede filer:** filer laget for hånd kan ha komma som desimaltegn, feil kolonnenavn eller hull. FR21 godtar de to vanlige formatene, og FR24 avviser resten med en forståelig feilmelding uten at appen krasjer.
- **Kontroll på KI-ens arbeid:** regelkoden skrives med Claude Code. Gruppen skal regne ut fasiten i T1–T12 for hånd før regelkoden skrives. Denne fasiten er kontrollen. Fasit som ikke er kontrollert ennå, er merket i briefen (A4).

## 12. Åpne punkter

- ~~**A1 Hvilken uke er t når brukeren velger analyseuke?**~~ Avgjort 2026-11-11: t er siste uke med telling til og med analyseuka, høyst én uke eldre enn analyseuka. Ellers grå status «ingen ny telling». Ført inn i R2, R4 og T10 i briefen og i FR8, FR20 og NFR2.
- ~~**A2 Område for Excel-opplasting**~~ Avgjort 2026-11-11: område utledes av `Fylke` når det finnes. Brukeren velger område for CSV og for Excel uten fylke. Ført inn i FR23, FR23a, J3 og kap. 8.
- **A3 Teknisk stack og arbeidsdeling:** avklares med Ella i arkitektursteget.
- **A4 Håndkontroll av fasit:** gruppen regner ut fasiten for T5, T6, T8 og T10–T12 for hånd og fjerner merkingen i briefen. Eier: gruppen. Må være gjort før epics og stories.

## 13. Neste steg

1. UX-steget: skisser av skjermbildene i kap. 8, og en skisse av samlet oversikt som mulig neste versjon.
2. Arkitektursteget: velge og begrunne stack, dataflyt og mappestruktur (A3).
3. Håndkontroll av fasit T5, T6, T8 og T10–T12 (A4).
4. Epics og stories med henvisning til FR- og NFR-ID-ene.
5. Kjøre backtesten med FR27 og oppdatere tallene i kap. 11.
