# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G01 – G01-ervik-kristiansen |
| **Product brief** | `_bmad-output/planning-artifacts/briefs/brief-Marin-2026-09-17/brief.md` (commit 50bffd3) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Problemet er konkret og godt forankret i et reelt domene. Dere viser til lakselusforskriften, grensene på 0,5 og 0,2 voksne hunnlus og forskjellen mellom å observere dagens tall på BarentsWatch og å få en prognose 2–3 uker frem i tid.
2. Dere har tatt bevisste og fornuftige avgrensninger. Live-integrasjon mot BarentsWatch, SMS/e-post-varsler, flere selskaper og avanserte prognosemodeller er flyttet ut av v1, og prognosemetoden er låst til enkel trendekstrapolering. Det gjør prosjektet langt mer gjennomførbart.

**De viktigste endringene:**

1. Suksesskriteriene kan ikke testes slik de står. «Målbar treffsikkerhet», «forståelig for en driftsleder» og «overbevisende konseptdemonstrasjon» må gjøres om til konkrete kriterier, for eksempel «gitt testdatasett X varsler appen overskridelse i uke 14 når grensen krysses i uke 16».
2. Reglene som prognosen og varslet bygger på, må skrives ut presist: hvilken grense som gjelder for hvilket område og hvilke uker, hvor mange uker historikk ekstrapoleringen bruker, og hva som gir grønn, gul og rød status. Det er disse reglene dere må kunne kontrollere at Claude Code har implementert riktig.
3. Avklar datagrunnlaget og de mange [ANTAGELSE]-punktene. Bestem om dere bruker et nedlastet utdrag fra BarentsWatch eller syntetiske data, og hvor fila skal ligge i repoet, slik at appen kan kjøres uten API-tilgang.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Middels**

**Sammenlignbart med:** Delmodulen 4.1 Prognoser og Demand Management i forslag 4) KI-støttet MRP II (vanskelig), men avgrenset til én modul og én enkel prognosemetode. Det plasserer prosjektet på nivå med 7) Kurs-FAQ-chatbot (middels).

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Middels | Trendekstrapolering, ulike grenser etter region og uke (0,2 i uke 16–21 i Midt-Norge og sørover) og beregning av «uker til grensen» må stemme. Temperatur og sesongmønster er nevnt som datakilder, men det står ikke hvordan de brukes i prognosen. |
| Datamodell – antall entiteter og relasjoner mellom dem | Lav | Anlegg, ukentlige lusetellinger og vanntemperatur, eventuelt område/sone. Oversiktlig. |
| Brukere, roller og innlogging | Lav | Én brukertype (driftsleder/fiskehelseansvarlig), og multi-tenant innlogging er ute av v1. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Lav | Briefen beskriver ingen språkmodell i appen. «Prediksjon» er her en statistisk beregning, ikke KI. Det er greit, men vær bevisst på ordbruken. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Lav | Live-API mot BarentsWatch er ute av v1. Hvis dere senere henter data via API, krever det registrering og nøkler. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Ingen sanntid i v1. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Lav–middels | Innlesing av historiske data fra CSV eller lignende. Avklar format og om brukeren skal kunne laste opp egne data. |
| Sikkerhet og personvern | Lav | Lusetall per anlegg er offentlige data, og det er ingen personopplysninger. |

**Hva vanskelighetsgraden betyr for dere:**

- _Middels:_ Et godt balansert valg. Pass på at kjerneflyten blir ferdig og stabil før dere legger til mer. For dere er kjerneflyten: velg anlegg → se historisk lusetrend → se prognoselinje og estimert uke for grenseoverskridelse → se statusfarge. Få den til å virke med kjente testdata før dere legger inn temperatur og sesongjustering.

### Gjennomførbarhet med BMAD og Claude Code

Dere skal planlegge med BMAD (product brief → PRD → arkitektur → epics og stories) og implementere med Claude Code. Vurderingen under tar hensyn til at det må være tid til hele denne flyten, og til testing, retting og README til slutt.

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | OK | Dashboard, prognose og statusindikator er tre avgrensede funksjonsområder. Det er realistisk, men git-loggen viser at dere bare har briefen så langt. Kom raskt i gang med PRD. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Mange [ANTAGELSE]-markeringer står fortsatt åpne, og reglene for prognose og statusfarge er ikke beskrevet. PRD-en vil arve disse hullene. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | Et web-dashboard med grafer og enkel regresjon passer godt for vanlige stakker, for eksempel Python med Streamlit eller en enkel webapp med et grafbibliotek. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Lineær trendekstrapolering er mulig å regne for hånd, men regionale grenser og eventuell temperaturjustering er lette å få subtilt feil. Lag små eksempler med fasit som dere regner ut selv. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | Risiko | Grensene og terskler for grønn/gul/rød egner seg godt for tester, men bare når de er skrevet ut som regler. Suksesskriteriene i dag gir ingen testtilfeller. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | OK | Med et datasett lagret i repoet og uten live-API kan sensor kjøre appen lokalt. Sørg for at dette står i PRD og README. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | OK | Ingen betalte tjenester er planlagt. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. Del prognosen i to trinn: v1 bruker ren trendekstrapolering på lusetall og regionale grenser. Temperatur- og sesongjustering legges som et tydelig neste trinn når v1 er testet. I dag står temperatur som datakilde uten at det er beskrevet hvordan den brukes.
2. Legg inn en enkel «tilbakeskuende test» (backtest) som egen funksjon: kjør prognosen på historiske data fram til uke N og sammenlign med hva som faktisk skjedde. Det gjør suksesskriteriet om treffsikkerhet målbart og løfter både testing og verdien av appen. Vurder også en enkel side der brukeren kan legge inn eller laste opp egne lusetall, så appen har mer reell funksjonalitet enn visning.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Tydelig: prognose og forvarsel 2–3 uker før lusegrensen krysses, i stedet for observasjon av nåsituasjonen. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | OK | Godt beskrevet med forskrift, konsekvenser (avlusing på kort varsel, tvangsslakting, MTB-reduksjon) og hvem som rammes. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | Juster | Dere nevner dashboard, trendlinje og varselnivå, men ikke hva brukeren faktisk gjør. Beskriv kjerneflyten i 3–5 steg og hvordan temperatur og sesong inngår. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Ærlig om at dette ikke er en teknisk «vollgrav», og at treffsikkerheten ikke er validert. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | OK | Driftsledere og fiskehelseansvarlige er tydelige. Si gjerne om de følger ett eller flere anlegg, siden det påvirker designet. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | Endre | Alle tre kriteriene er vage, og dere skriver selv at de er foreløpige. Legg til funksjonelle kriterier som «brukeren kan velge et anlegg og se estimert uke for grenseoverskridelse» og et målbart kriterium for treffsikkerhet mot historiske data. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Juster | Godt skille mellom inn og ute, men flere punkter er merket [ANTAGELSE]. Bekreft dem, og avklar om v1 skal dekke ett område eller hele kysten. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Utvidelse til flere anlegg og flere fiskehelseparametere er en naturlig retning og holdes utenfor v1. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Problemet er godt, men reglene for prognose og status mangler. Lukk [ANTAGELSE]-punktene og oppdater briefen i repoet, slik at historikken viser utviklingen. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Juster | Omfanget er realistisk, men en ren visning kan bli tynn. Backtest og egen dataregistrering gir mer å vise. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | Endre | Prognoseberegning og grenseregler er ideelle for automatiske tester, men kriteriene må skrives som sjekkbare regler først. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | OK | Tydelig bruker uten datafaglig bakgrunn. Skisser oversikt over anlegg og detaljsiden med trendlinje. Tenk på at statusfarger også må forstås uten fargesyn. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | OK | Ingen teknologivalg i briefen, og det er riktig. Velg en enkel stakk i arkitekturen og begrunn valget. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | OK | Mulig når datagrunnlaget ligger i repoet. Beskriv i README hvor dataene kommer fra og hvordan de er hentet. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Bestem en fast mappe for datasett og testdata, og hold eventuelle API-nøkler ute av repoet hvis dere senere bruker BarentsWatch-API-et. |

## 3. Neste steg for gruppen

1. Skriv om suksesskriteriene til 4–6 sjekkbare kriterier, blant annet ett for treffsikkerhet mot historiske data, og lukk eller bekreft [ANTAGELSE]-punktene.
2. Skriv ut reglene: grense per område og uke, antall uker i trendberegningen, terskler for grønn/gul/rød, og om og hvordan temperatur brukes i v1. Lag 2–3 små eksempler med fasit som senere kan bli tester.
3. Bestem datagrunnlaget (utdrag fra BarentsWatch eller syntetiske data), legg det i repoet og gå videre til PRD.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
