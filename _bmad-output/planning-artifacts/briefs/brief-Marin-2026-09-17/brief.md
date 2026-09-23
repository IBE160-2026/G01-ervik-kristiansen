---
title: "Product Brief: Marin"
status: draft
created: 2026-09-17
updated: 2026-09-23
---

# Product Brief: Marin

## Executive Summary

Marin er et prediktivt varslingssystem for norske lakseoppdrettere som gir forvarsel — typisk 2-3 uker i forkant — om at et anlegg er på vei mot å overskride den lovpålagte lakselusgrensen. I dag rapporterer oppdrettere ukentlige lusetall til Mattilsynet og kan følge status på BarentsWatch, men dette er observasjon av nåsituasjonen, ikke en prognose. Driftsledere og fiskehelseansvarlige oppdager i praksis en forestående overskridelse først når den er nært forestående eller allerede et faktum.

Marin snur dette fra reaktivt til proaktivt: ved å kombinere historiske lusetall (BarentsWatch/Mattilsynet), vanntemperatur og sesongmønster, predikerer systemet lusetrenden fremover i tid og varsler når et anlegg er på vei mot å krysse grensen — med nok margin til at tiltak (avlusing, brønnbåt, biologisk kontroll) kan planlegges og gjennomføres før overskridelsen inntreffer, i stedet for som en hastesak etter at den har skjedd.

[ANTAGELSE: Prosjektet realiseres i første omgang som en konseptuell demo/prototype med syntetiske og/eller historiske data — ikke en produksjonsklar tjeneste med sanntidsintegrasjon.]

## Problemet

Lakselusforskriften (FOR-2012-12-05-1140) pålegger norske oppdrettsanlegg en grense på i gjennomsnitt under 0,5 voksne hunnlus per fisk, og en strengere grense på under 0,2 i Midt-Norge og sørover i ukene 16-21 (våren, for å skjerme utvandrende vill laksesmolt). Oppdrettere rapporterer ukentlige lusetall til Mattilsynet, og BarentsWatch Fiskehelse aggregerer og viser dette åpent, med historikk tilbake til 2012.

Problemet er ikke mangel på data — det er mangel på fremoverskuende innsikt. Driftsledere og fiskehelseansvarlige ser dagens og fjorårets tall, men må selv vurdere om utviklingen er i ferd med å bli kritisk. Når grensen nærmer seg eller overskrides:

- Avlusing må gjennomføres på kort varsel, ofte med stress for fisken og høye kostnader (brønnbåt, kjemikalier, personell)
- Ved gjentatte eller alvorlige overskridelser kan Mattilsynet pålegge tvangsutslakting
- Anlegget risikerer bøter og reduksjon i tillatt biomasse (MTB) ved neste tildeling
- Fiskevelferden svekkes, og omdømmet til anlegget/selskapet kan ta skade

[ANTAGELSE: Den reelle smerten er størst for mellomstore/mindre oppdrettsselskaper uten egne dataanalyseressurser — store konsern har trolig allerede intern kapasitet til å gjøre denne typen prognosearbeid manuelt. Ikke bekreftet med reelle brukere.]

## Løsningen

Marin henter og kombinerer tre datakilder per anlegg:

- Historiske lusetall (BarentsWatch/Mattilsynet, ukentlig rapportering)
- Vanntemperatur
- Sesongmønster (lusas livssyklus er sterkt temperatur- og årstidsavhengig)

Fra dette produserer systemet en prognose ved enkel trendekstrapolering på de historiske lusetallene: er anlegget på vei mot å krysse den gjeldende grensen, og i så fall — omtrent når. Driftsleder/fiskehelseansvarlig får et varsel 2-3 uker før terskelen forventes nådd, med nok tid til å planlegge og iverksette tiltak fremfor å reagere i siste liten.

Presentasjonsformen er et web-dashboard (status per anlegg, trendlinje, varselnivå), ikke en ren varslingstjeneste via SMS/e-post.

## Hva gjør dette annerledes

BarentsWatch Fiskehelse og det åpne tredjepartsprosjektet «oppdretter» (varselsystem for lakselus, sykdom, soner og brønnbåter fra åpne norske kilder — det eneste beslektede verktøyet identifisert så langt) viser og aggregerer *dagens* og *historiske* tall godt. De svarer på «hva er situasjonen nå». Marins differensiering er å svare på «hva vil situasjonen være om 2-3 uker» — en prognose, ikke bare et øyeblikksbilde.

Dette er ikke en unik teknisk «vollgrav» — det er en tydelig retningsvalgt fordel (prediktivt fremfor observerende), og skal presenteres ærlig som det. Prediksjonsmetoden i v1 er avklart som enkel trendekstrapolering, ikke en mer avansert tidsseriemodell. [ANTAGELSE: Metodens faktiske treffsikkerhet i praksis er ikke validert ennå og er en sentral usikkerhet i prosjektet, ikke en avklart styrke.]

## Hvem dette tjener

**Primærbrukere:** Driftsledere og fiskehelseansvarlige ved norske lakseoppdrettsanlegg. De trenger tidlig, pålitelig varsel for å kunne planlegge avlusingstiltak, bestille brønnbåtkapasitet og disponere personell — fremfor å håndtere en akutt overskridelse. Suksess for dem er et varsel de kan stole på og handle på i tide.

[ANTAGELSE: Sekundærbrukere kan være produksjonssjefer/regionledere som følger flere anlegg samtidig, men dette er ikke bekreftet eller utforsket videre.]

## Suksesskriterier

- Prognosemodellen viser målbar treffsikkerhet mot historiske data (varslet overskridelse faktisk inntraff innenfor det varslede tidsvinduet)
- Dashboardet er forståelig og brukbart for en driftsleder uten datafaglig bakgrunn
- Systemet demonstrerer verdien tydelig nok til å fungere som en overbevisende konseptdemonstrasjon for kurset (IBE160)

[ANTAGELSE: Foreløpig forslag — bør konkretiseres etter hvert som prosjektet modnes.]

## Omfang

**Inn i første versjon**:
- Dashboard som viser status og historisk lusetrend per anlegg — bekreftet presentasjonsform
- Prediktivt varsel med estimert tidshorisont mot lovpålagt grense, basert på enkel trendekstrapolering — bekreftet metode
- Enkel visuell statusindikasjon (f.eks. grønn/gul/rød) basert på nærhet til grensen [ANTAGELSE]
- Bruk av syntetiske og/eller historiske data (BarentsWatch) som datagrunnlag [ANTAGELSE]

**Ute av første versjon**:
- Sanntids/live-integrasjon mot BarentsWatch API [ANTAGELSE]
- Mobilapp [ANTAGELSE]
- Automatiske varsler via SMS/e-post/push — bekreftet ute, web/dashboard er valgt presentasjonsform
- Støtte for flere selskaper/multi-tenant innlogging [ANTAGELSE]
- Andre fiskehelseparametere enn lakselus [ANTAGELSE]
- Mer avansert prediksjonsmodell utover enkel trendekstrapolering — bekreftet ute av v1

## Visjon

Om konseptet lykkes, kan Marin bli et verktøy oppdrettsselskaper bruker på tvers av alle sine anlegg for å redusere avlusingskostnader, forbedre fiskevelferd og unngå bøter og tvangstiltak — ved systematisk å ligge i forkant av grenseverdiene i stedet for å reagere på dem. [ANTAGELSE: En naturlig videreutvikling er å utvide prognosemodellen til flere fiskehelseparametere (f.eks. sykdom) utover lakselus, men dette er ikke en bekreftet retning.]
