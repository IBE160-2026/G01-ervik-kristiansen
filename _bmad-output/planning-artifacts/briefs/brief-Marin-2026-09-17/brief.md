---
title: "Product Brief: Marin"
status: draft
created: 2026-09-17
updated: 2026-10-27
---

# Product Brief: Marin

## Executive Summary

Marin er et prediktivt varslingssystem for norske lakseoppdrettere som gir forvarsel — typisk 2-3 uker i forkant — om at et anlegg er på vei mot å overskride den lovpålagte lakselusgrensen. I dag rapporterer oppdrettere ukentlige lusetall til Mattilsynet og kan følge status på BarentsWatch, men dette er observasjon av nåsituasjonen, ikke en prognose. Driftsledere og fiskehelseansvarlige oppdager i praksis en forestående overskridelse først når den er nært forestående eller allerede et faktum.

Marin snur dette fra reaktivt til proaktivt: systemet trekker en trendlinje gjennom de siste ukenes lusetall for anlegget og sammenligner den med grensen som gjelder i hver av de kommende ukene. Når anlegget er på vei mot å krysse grensen, varsler systemet — med nok margin til at tiltak (avlusing, brønnbåt, biologisk kontroll) kan planlegges og gjennomføres før overskridelsen inntreffer, i stedet for som en hastesak etter at den har skjedd.

Prosjektet realiseres i første omgang som en konseptuell demo/prototype basert på et nedlastet utdrag av historiske lusetall fra BarentsWatch, lagret i repoet — ikke en produksjonsklar tjeneste med sanntidsintegrasjon. Prognosen er ren statistikk (lineær regresjon); appen inneholder ingen KI.

## Problemet

Lakselusforskriften (FOR-2012-12-05-1140) pålegger norske oppdrettsanlegg en grense på i gjennomsnitt under 0,5 voksne hunnlus per fisk, og en strengere grense på under 0,2 i en vårperiode for å skjerme utvandrende vill laksesmolt (uker og områder står i R1). Oppdrettere rapporterer ukentlige lusetall til Mattilsynet, og BarentsWatch Fiskehelse aggregerer og viser dette åpent, med historikk tilbake til 2012.

Problemet er ikke mangel på data — det er mangel på fremoverskuende innsikt. Driftsledere og fiskehelseansvarlige ser dagens og fjorårets tall, men må selv vurdere om utviklingen er i ferd med å bli kritisk. Når grensen nærmer seg eller overskrides:

- Avlusing må gjennomføres på kort varsel, ofte med stress for fisken og høye kostnader (brønnbåt, kjemikalier, personell)
- Ved gjentatte eller alvorlige overskridelser kan Mattilsynet pålegge tvangsutslakting
- Anlegget risikerer bøter og reduksjon i tillatt biomasse (MTB) ved neste tildeling
- Fiskevelferden svekkes, og omdømmet til anlegget/selskapet kan ta skade.

Den reelle smerten er størst for mellomstore/mindre oppdrettsselskaper uten egne dataanalyseressurser — store konsern har trolig allerede intern kapasitet til å gjøre denne typen prognosearbeid manuelt. Ikke bekreftet med reelle brukere.

## Løsningen

I v1 bruker Marin én datakilde: historiske lusetall per anlegg fra BarentsWatch (ukentlig rapportering til Mattilsynet), hentet som et nedlastet utdrag og lagret i repoet.

Systemet tilpasser en rett linje (lineær regresjon) til de siste ukenes lusetall og trekker den fremover. For hver kommende uke sammenlignes estimatet med grensen som gjelder i den uka. Resultatet er et estimat på hvor mange uker det er til grensen nås, og en statusfarge. Driftsleder/fiskehelseansvarlig får varsel når grensen ventes nådd innen 3 uker, med nok tid til å planlegge og iverksette tiltak fremfor å reagere i siste liten. Reglene står i neste seksjon.

Vanntemperatur og sesongmønster påvirker lusas livssyklus sterkt, men brukes ikke i prognosen i v1. Det er planlagt som neste trinn når v1 er testet (R5). Sesongen er likevel med i v1 gjennom den strengere vårgrensen (R1).

Presentasjonsformen er et web-dashboard (status per anlegg, trendlinje, varselnivå), ikke en ren varslingstjeneste via SMS/e-post.

## Regler for prognose og varsel

Reglene har faste ID-er, slik at PRD, stories og tester kan vise til dem.

### R1 Gjeldende lusegrense

Grensen gjelder gjennomsnittlig antall voksne hunnlus per fisk i anlegget (lakselusforskriften § 8):

| Område | Uker (ISO) | Grense |
|---|---|---|
| Nord-Trøndelag og sørover («sør») | 16 t.o.m. 21 | 0,2 |
| Nordland, Troms og Finnmark («nord») | 21 t.o.m. 26 | 0,2 |
| Alle områder, øvrige uker | — | 0,5 |

- Grensen er «færre enn». En verdi **≥ grensen** er brudd.
- Uker er ISO-uker.
- Et anlegg er «nord» når det ligger i Nordland, Troms eller Finnmark, ellers «sør». Forskriften bruker fortsatt «Nord-Trøndelag», selv om fylket ikke finnes lenger; «Nord-Trøndelag og sørover» betyr i praksis hele Trøndelag og alt sør for det.
- Særskilte grenser for tillatelser med kapasitetsøkning er ute av v1.
- Ordlyden er kontrollert mot Lovdata: _[dato fylles inn av Fredrik]_.

### R2 Trendberegning

- **Historikk:** de 5 siste ukene med lusetall (N = 5), til og med uke t, der t er uka med siste telling.
- **Metode:** lineær regresjon (minste kvadraters metode) med ISO-uke som x-verdi og lusetall som y-verdi. Årsskiftet (uke 52/53 → uke 1) behandles som sammenhengende tid.
- **Uker til grensen:** for hver kommende uke t + k, der k = 1, 2, …, 6 (horisont H = 6), beregnes estimert verdi fra linja og sammenlignes med grensen i den uka (R3). Uker til grensen er den første k der estimatet er ≥ grensen. Finnes ingen slik k, er resultatet «ingen kryssing innen 6 uker».
- **Spesialtilfeller:**
  - *Flat eller fallende trend:* ingen unntak. Regelen sjekkes på samme måte, fordi grensen kan falle til 0,2 om våren.
  - *Allerede over grensen:* er siste målte verdi ≥ grensen som gjelder i uke t, blir uker til grensen 0 og status «brudd nå». Ingen prognose beregnes.
  - *For få datapunkter:* mangler det telling i noen av de 5 siste ukene, beregnes ingen prognose, og appen viser «for lite data».
  - *Negative estimater:* et estimat under 0 settes til 0.

### R3 Grensen prognosen sammenlignes mot

Estimatet for uke t + k sammenlignes med grensen som gjelder i uke t + k (R1), ikke grensen som gjelder i dag. Eksempel: et anlegg i sør med siste telling i uke 14 sammenlignes mot 0,5 i uke 15 og mot 0,2 i uke 16–20.

### R4 Statusfarge

Status bestemmes av uker til grensen fra R2:

| Status | Betingelse | Vises som |
|---|---|---|
| Rød | brudd nå (0 uker), eller grensen nås om 1–3 uker | «✕ Brudd nå» / «✕ Varsel: grensen nås om X uker» |
| Gul | grensen nås om 4–6 uker | «! Følg med: grensen kan nås om X uker» |
| Grønn | ingen kryssing innen 6 uker | «✓ Ingen kryssing ventet innen 6 uker» |
| Grå | for lite data | «– For lite data» |

- Status vises alltid med tekst og symbol i tillegg til farge, slik at den kan forstås uten fargesyn.
- Rød status er det som regnes som «varsel» i suksesskriteriene og backtesten.

### R5 Temperatur og sesong i v1

Vanntemperatur og sesongjustering av trenden brukes ikke i v1. Prognosen bygger bare på lusetall. Sesongen er likevel med gjennom vårgrensen i R1. Temperatur- og sesongjustering er planlagt som neste trinn når v1 er testet.

### R6 Testtilfeller med fasit

Tabellen er utgangspunkt for automatiske tester. Fasit regnes ut av gruppen for hånd, ikke av KI.

| ID | Regel | Inndata | Forventet resultat |
|---|---|---|---|
| T1 | R1 | Sør, uke 21 | Grense 0,2 |
| T2 | R1 | Sør, uke 22 | Grense 0,5 |
| T3 | R1 | Nord, uke 21 | Grense 0,2 |
| T4 | R1 | Nord, uke 20 | Grense 0,5 |
| T5 | R2, R4 | Fem ukers lusetall for ett anlegg: _[fylles inn av gruppen]_ | Estimert uke for grensen og farge: _[regnes ut for hånd av gruppen]_ |
| T6 | R3 | Anlegg i sør, siste telling i uke 14: _[lusetall fylles inn av gruppen]_ | Sammenlignes mot 0,5 i uke 15 og 0,2 i uke 16–20. Uke og farge: _[regnes ut for hånd av gruppen]_ |

## Hva gjør dette annerledes

BarentsWatch Fiskehelse og det åpne tredjepartsprosjektet «oppdretter» (varselsystem for lakselus, sykdom, soner og brønnbåter fra åpne norske kilder — det eneste beslektede verktøyet identifisert så langt) viser og aggregerer *dagens* og *historiske* tall godt. De svarer på «hva er situasjonen nå». Marins differensiering er å svare på «hva vil situasjonen være om 2-3 uker» — en prognose, ikke bare et øyeblikksbilde.

Dette er ikke en unik teknisk «vollgrav» — det er en tydelig retningsvalgt fordel (prediktivt fremfor observerende), og skal presenteres ærlig som det. Prediksjonsmetoden i v1 er avklart som enkel trendekstrapolering, ikke en mer avansert tidsseriemodell. Metodens faktiske treffsikkerhet i praksis er ikke validert ennå og er en sentral usikkerhet i prosjektet, ikke en avklart styrke.

## Hvem dette tjener

**Primærbrukere:** Driftsledere og fiskehelseansvarlige ved norske lakseoppdrettsanlegg. De trenger tidlig, pålitelig varsel for å kunne planlegge avlusingstiltak, bestille brønnbåtkapasitet og disponere personell — fremfor å håndtere en akutt overskridelse. Suksess for dem er et varsel de kan stole på og handle på i tide.

Sekundærbrukere kan være produksjonssjefer/regionledere som følger flere anlegg samtidig, men dette er ikke bekreftet eller utforsket videre.

## Suksesskriterier

Hvert kriterium viser til reglene (R) og testtilfellene (T) over.

1. **Regelkorrekthet:** Testtilfellene T1–T6 (R6) kjører som automatiske tester og består.
2. **Treffsikkerhet (backtest):** Prognosen kjøres uke for uke på det historiske datasettet, med bare data fram til hver uke. En grensekryssing er en uke der målt verdi er ≥ grensen (R1) mens uka før var under. En kryssing regnes som treff hvis anlegget første gang fikk rød status (R4) 2–4 uker før kryssingen. Minst _[X] %_ av kryssingene skal være treff; X fastsettes av gruppen før backtesten kjøres. Andelen røde varsler som ikke ble fulgt av en kryssing, rapporteres sammen med treffandelen.
3. **Kjerneflyt:** Brukeren kan velge et anlegg og se de 5 siste ukenes lusetall, trendlinjen, estimert uke for grensen og statusen (R2–R4).
4. **Lesbar uten fargesyn:** Hver status vises med tekst og symbol i tillegg til farge (R4).
5. **Kjørbar for sensor:** Appen kan kjøres lokalt etter README, med datasettet som ligger i repoet, uten API-nøkler eller nettilgang.

## Omfang

**Inn i første versjon**:
- Dashboard som viser status og historisk lusetrend per anlegg — bekreftet presentasjonsform
- Prediktivt varsel med estimert tidshorisont mot lovpålagt grense, basert på lineær regresjon (R2, R3)
- Statusfarge med tekst og symbol (R4)
- Nedlastet utdrag av historiske lusetall fra BarentsWatch som datagrunnlag, lagret i `data/barentswatch/` i repoet

**Ute av første versjon**:
- Sanntids/live-integrasjon mot BarentsWatch API
- Mobilapp
- Automatiske varsler via SMS/e-post/push — bekreftet ute, web/dashboard er valgt presentasjonsform
- Støtte for flere selskaper/multi-tenant innlogging
- Andre fiskehelseparametere enn lakselus
- Mer avansert prediksjonsmodell utover enkel trendekstrapolering — bekreftet ute av v1
- Temperatur- og sesongjustering av prognosen — planlagt neste trinn etter at v1 er testet (R5)
- Særskilte lusegrenser for tillatelser med kapasitetsøkning (R1)

## Visjon

Om konseptet lykkes, kan Marin bli et verktøy oppdrettsselskaper bruker på tvers av alle sine anlegg for å redusere avlusingskostnader, forbedre fiskevelferd og unngå bøter og tvangstiltak — ved systematisk å ligge i forkant av grenseverdiene i stedet for å reagere på dem. En naturlig videreutvikling er å utvide prognosemodellen til flere fiskehelseparametere (f.eks. sykdom) utover lakselus, men dette er ikke en bekreftet retning.
