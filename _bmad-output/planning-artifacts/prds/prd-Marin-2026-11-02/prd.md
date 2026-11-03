---
title: "PRD: Marin"
status: draft
created: 2026-11-03
updated: 2026-11-03
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
- **R6 / T1–T9:** testtilfeller med fasit
- **SK1–SK5:** suksesskriteriene i briefen, nummerert i samme rekkefølge

Hvert krav i PRD-en har en ID (FR, NFR), slik at epics, stories og tester kan vise til dem.

## 2. Mål

| ID | Mål | Måles ved |
|---|---|---|
| M1 | Brukeren får et forvarsel før grensen brytes, ikke bare et øyeblikksbilde | SK2 (backtest, minst 25 % treff) |
| M2 | Reglene er implementert riktig og kan kontrolleres av gruppen | SK1 (T1–T9 består) |
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
2. Appen regner prognosen på nytt med bare de dataene som fantes fram til den uka.
3. Brukeren ser hva Marin ville varslet da, og kan sammenligne med hva som faktisk skjedde de neste ukene.

### J3 Få prognose på egne lusetall

1. Brukeren går til opplastingssiden og laster opp en CSV-fil eller et Excel-uttrekk fra BarentsWatch.
2. Brukeren velger område (sør eller nord).
3. Appen validerer fila og viser feil på en forståelig måte, eller viser detaljsiden for de opplastede dataene.
4. Dataene forsvinner når økta avsluttes.

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
| FR7 | Brukeren kan velge analyseuke (ISO-år og ISO-uke) mellom 2025 uke 1 og 2026 uke 42. Standardvalg er 2026 uke 42. | J2 |
| FR8 | Prognosen for en valgt analyseuke bruker bare telling fra og med analyseuka og bakover. Data etter analyseuka påvirker ikke prognosen. | J2, SK2 |
| FR9 | Detaljsiden viser tydelig hvilken uke prognosen er regnet fra. | J2 |

### 5.4 Prognose og status

| ID | Krav | Sporing |
|---|---|---|
| FR10 | Appen finner gjeldende grense for et anlegg og en uke etter R1. | R1, T1–T4 |
| FR11 | Appen beregner trend med lineær regresjon etter R2: vindu på 5 uker, minst 3 tellinger, ISO-uke som x-verdi, årsskiftet som sammenhengende tid. | R2, T5, T8 |
| FR12 | Appen beregner «uker til grensen» med horisont 6 uker, og sammenligner estimatet for hver kommende uke med grensen som gjelder i den uka. | R2, R3, T5, T6 |
| FR13 | Appen håndterer spesialtilfellene i R2: brudd nå, for lite data og negative estimater (settes til 0). | R2, T9 |
| FR14 | Appen setter status (rød, gul, grønn, grå) og statustekst etter R4. | R4, T5–T9 |

### 5.5 Detaljside

| ID | Krav | Sporing |
|---|---|---|
| FR15 | Detaljsiden viser status med farge, symbol og tekst etter R4. | SK3, SK4 |
| FR16 | Detaljsiden viser en graf med målte lusetall i vinduet, trendlinja forlenget 6 uker fram og grensen per uke (som trapp når vårgrensen slår inn). | SK3, R3 |
| FR17 | Detaljsiden viser en tabell med de 5 ukene i vinduet (uke og lusetall, eller «ikke telt»). | SK3 |
| FR18 | Ved rød eller gul status viser detaljsiden estimert ISO-uke for når grensen nås. | SK3 |
| FR19 | Detaljsiden viser en kort, fast tekst om at prognosen er en enkel trendberegning og ikke en garanti, med treffandelen fra siste backtest. | M1, «Hva gjør dette annerledes» |
| FR20 | Ved grå status forklarer detaljsiden hvorfor det ikke finnes en prognose (for lite data eller ukjent område). | R4, T7, T9 |

### 5.6 Opplasting av egne lusetall

| ID | Krav | Sporing |
|---|---|---|
| FR21 | Brukeren kan laste opp en CSV-fil for ett anlegg med kolonnene `år`, `uke` og `voksne_hunnlus` (desimalpunktum). Tom verdi betyr uke uten telling. | J3 |
| FR22 | Brukeren kan laste opp et Excel-uttrekk i samme format som BarentsWatch-fila «Lakselus per fisk». Inneholder fila flere lokaliteter, velger brukeren én etter opplasting. | J3 |
| FR23 | Brukeren velger område (sør eller nord) ved opplasting. Grensen bestemmes ut fra valget etter R1. | J3, R1 |
| FR24 | Appen validerer fila og viser en feilmelding som sier hva som er galt og i hvilken rad: manglende kolonner, uke utenfor 1–53, negative eller ikke-numeriske lusetall og samme uke flere ganger. Ugyldige filer gir ingen prognose. | J3 |
| FR25 | Etter vellykket opplasting vises samme detaljside som for BarentsWatch-anlegg (FR15–FR20), med analyseuke lik siste uke i fila. | J3 |
| FR26 | Opplastede data lagres ikke. De forsvinner når økta avsluttes. | J3, NFR6 |

### 5.7 Backtest (utviklerverktøy)

| ID | Krav | Sporing |
|---|---|---|
| FR27 | Et skript kjører backtesten på hele datagrunnlaget etter definisjonen i SK2. Prognosen for hver uke bruker bare data fram til og med den uka. | SK2 |
| FR28 | Skriptet rapporterer antall grensekryssinger, antall treff, treffandel og andelen røde varsler som ikke ble fulgt av brudd innen 4 uker. Resultatet skrives til en fil i repoet, slik at FR19 kan vise treffandelen. | SK2, FR19 |
| FR29 | Backtesten vises ikke som egen side i appen i v1. | Beslutning 2026-11-03 |

## 6. Ikke-funksjonelle krav

| ID | Krav | Sporing |
|---|---|---|
| NFR1 | Appen kan kjøres lokalt etter README, med datasettet i repoet, uten API-nøkler, betalte kontoer eller nettilgang. | SK5 |
| NFR2 | T1–T9 finnes som automatiske tester og består. Testene kan kjøres med én kommando beskrevet i README. | SK1 |
| NFR3 | R1 testes i tillegg mot BarentsWatch-kolonnen `Lusegrense uke` som uavhengig fasit, med 0 avvik. | R1, addendum |
| NFR4 | Status kan forstås uten fargesyn: alltid farge, symbol og tekst sammen. | SK4 |
| NFR5 | Brukergrensesnittet er på norsk (bokmål). Uker vises som ISO-uker, f.eks. «uke 38, 2026». | SK3 |
| NFR6 | Appen behandler ingen personopplysninger. Lusetall per anlegg er offentlige data. | Tilbakemelding |
| NFR7 | Appen inneholder ingen KI eller språkmodell. Prognosen er ren statistikk. | Brief |
| NFR8 | Detaljsiden vises på under 2 sekunder på en vanlig bærbar PC etter at appen har startet. | SK3 |
| NFR9 | Ingen hemmeligheter eller nøkler ligger i repoet. Datasett ligger i `data/`, testdata i en egen testmappe. | Tilbakemelding, ryddighet |

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
2. **Detaljside:** anleggsnavn og -info, analyseuke-velger, statusboks, graf, ukestabell og usikkerhetstekst (FR7–FR20).
3. **Opplasting:** filvelger, valg av område, eventuelt valg av lokalitet, feilmeldinger (FR21–FR24).

Skisser av skjermbildene lages i arkitektur- eller UX-steget.

## 9. Omfang

**Med i v1:** alt i kapittel 5 og 6.

**Ute av v1** (fra briefen, pluss beslutningene 2026-11-03):
- Samlet oversikt over alle anlegg med status, filtrering og sortering
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
| R1 | FR3, FR10, FR23, NFR3 |
| R2 | FR2, FR11–FR13 |
| R3 | FR12, FR16 |
| R4 | FR14, FR15, FR20, NFR4 |
| R5 | Omfang (ute av v1) |
| R6 / T1–T9 | NFR2 |
| SK1 | NFR2 |
| SK2 | FR8, FR27, FR28 |
| SK3 | FR4, FR5, FR15–FR18 |
| SK4 | FR15, NFR4 |
| SK5 | FR1, NFR1 |

## 11. Forutsetninger og risiko

- **Treffsikkerhet:** den grove backtesten ga omtrent 29 % treff, og bare omtrent 14 % av de røde varslene ble fulgt av brudd. Mange røde varsler er altså falske alarmer. Det er et legitimt funn, og FR19 sørger for at brukeren får vite det.
- **Datakvalitet:** utdraget er et fast øyeblikksbilde lastet ned 27.10.2026. Senere rettinger hos BarentsWatch kommer ikke med.
- **Opplastede filer:** filer laget for hånd kan ha komma som desimaltegn, feil kolonnenavn eller hull. FR24 må håndtere dette uten at appen krasjer.
- **Kontroll på KI-ens arbeid:** regelkoden skrives med Claude Code. Fasiten i T1–T9 er regnet ut for hånd av gruppen og er kontrollen.

## 12. Åpne punkter

- **A1 Hvilken uke er t når brukeren velger analyseuke?** R2 sier at t er «uka med siste telling». Hvis siste telling før analyseuka var for flere uker siden, er det uklart om vinduet skal ligge rundt analyseuka (og gi «for lite data») eller rundt siste telling (og gi en prognose fra gamle data). Avgjøres før epics og stories, og føres eventuelt inn i R2.
- **A2 Område for Excel-opplasting:** skal brukeren velge område også når BarentsWatch-fila har kolonnen `Fylke`, eller skal appen bruke fylket som for det innebygde datasettet?
- **A3 Teknisk stack og arbeidsdeling** avklares med Ella i arkitektursteget.

## 13. Neste steg

1. Lukke A1 og A2.
2. Arkitektur: velge og begrunne stack, dataflyt og mappestruktur.
3. Epics og stories med henvisning til FR- og NFR-ID-ene.
