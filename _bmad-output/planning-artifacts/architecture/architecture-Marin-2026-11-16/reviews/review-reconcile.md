---
title: "Avstemming: arkitekturspine mot kildene"
reviewed: ARCHITECTURE-SPINE.md (draft, 2026-11-16) og .memlog.md
date: 2026-11-16
sources:
  - ../../../prds/prd-Marin-2026-11-02/prd.md
  - ../../../briefs/brief-Marin-2026-09-17/brief.md
  - ../../../briefs/brief-Marin-2026-09-17/addendum.md
  - ../../../ux-designs/ux-Marin-2026-11-11/DESIGN.md
  - ../../../ux-designs/ux-Marin-2026-11-11/EXPERIENCE.md
---

# Avstemming av arkitekturspinen mot kildene

**Omfang:** bare arkitekturnivå. Gjennomgangen ser etter krav og stille føringer i kildene som spinen dropper, motsier eller lar være så åpne at to byggere kan gå hver sin vei. Detaljer som koden eier, er utelatt (se siste avsnitt).

**Metode:** alle fem kildene og begge memlogene (arkitektur og PRD) er lest i sin helhet. Tre påstander er sjekket direkte: størrelsen på BarentsWatch-filene i `data/barentswatch/` (5,1 MB og 4,3 MB), antall ISO-uker per år (2025: 52, 2026: 53, 2020: 53) og hvordan Pythons `round()` runder halvdeler.

## Konklusjon

**Dom: godkjent med endringer.** Spinen holder i hovedsak. R1–R4 ligger i én ren kjerne, backend eier tekstene, statuskodene er faste, reglene bruker ingen systemdato, og nettleseren lagrer bare lokalitetsnummeret. Fem høye funn bør likevel lukkes i spinen før epics og stories:

- opplastede filer over 1 MB havner på disk med FastAPIs standardoppsett
- det er ikke bestemt hvordan statusoverskriften er bygd opp
- rutingen mellom forsiden og husket anlegg kan gjøre forsiden umulig å nå
- backtesten mangler en definisjon av presisjon og en plass for SK2-logikken
- regelen «halvdeler rundes opp» er falt ut

Ingen av funnene krever en ny stack.

## Oversikt

| # | Alvor | Tema | Berører | Forslag |
|---|---|---|---|---|
| F1 | Høy | Opplastet fil kan havne på disk | AD-4, FR26, FR22 | Fiks |
| F2 | Høy | Statusoverskriften: symbol, R4-tekst og «(uke Y)». Lista over tekster backend eier, er ufullstendig | AD-2, AD-7, FR9, FR15, FR18, FR23, NFR2, tilgjengelighet | Fiks |
| F3 | Høy | Ruting: forsiden mot husket anlegg, og opplastet detaljside uten data | AD-4, AD-8, AD-9, FR6a, FR6b, FR26, UX-7 | Fiks |
| F4 | Høy | Backtest: presisjon er udefinert, SK2-logikken ligger utenfor kjernen, og resultatfila mangler parameterne | AD-1, AD-6, AD-10, FR27, FR27a, FR28, M1-C | Fiks og flagg til PRD |
| F5 | Høy | Avrunding: «halvdeler rundes opp» mangler | AD-6, R2, T12 | Fiks |
| F6 | Middels | Uker: ISO-uke 53, velgbare uker, ukeformat og kuttet ved `SISTE_UKE` | AD-1, AD-5, AD-6, FR1, FR7, FR17, FR24, FR25, NFR5 | Fiks |
| F7 | Middels | Opplasting via en tilstandsløs server: flere anlegg, ny validering og område | AD-3, AD-4, FR22–FR25, R1 | Fiks |
| F8 | Middels | Graf: Recharts mot UX-kravene om vekt, tekststørrelse og `role="img"` | Stack, konvensjonene for tilgjengelighet | Fiks eller flagg |
| F9 | Middels | Utdaterte svar når analyseuka byttes | FR9 (2), EXPERIENCE (300 ms) | Fiks |
| F10 | Lav | NFR3 mangler i testkonvensjonen | NFR3, PRD kap. 7 | Fiks |
| F11 | Lav | Fra fylke til område i opplastede filer | R1, FR23, FR24 | Flagg |
| F12 | Lav | To tallformater (lusetall og grense) i to språk | AD-6, EXPERIENCE Voice and Tone | Fiks |
| F13 | Lav | FR19 ved presisjon under 20 %, og faste tekster som avhenger av R4-parameterne | AD-2, AD-10, FR6a, FR19, FR27a | Flagg |
| F14 | Lav | HTTP-cache og «nettleseren inneholder ingen lusetall» | NFR6, FR6b (5) | Fiks |

## Funn

### F1 Høy – Opplastet fil kan havne på disk

**Kilder:** PRD FR26 («skrives aldri til disk») og FR22 («samme format som BarentsWatch-fila»). Spinen, AD-4: «Ingenting skrives til disk».

**Problem:** FastAPI bygger på Starlette, og Starlette legger opplastede filer i en `SpooledTemporaryFile`. Den skrives til en midlertidig fil på disk når fila er større enn 1 MB. Det gjelder både `UploadFile` og `bytes = File()`, fordi Starlette mellomlagrer fila før FastAPI ser innholdet. BarentsWatch-filene i repoet er på 5,1 MB (2025) og 4,3 MB (2026). Et Excel-uttrekk i samme format (FR22, J3) går altså via disk med standardoppsettet. Spinen sier bare «multipart». En bygger som følger spinen bokstavelig, bryter derfor FR26 uten å merke det.

**Forslag:** Legg til i AD-4 at opplastingen leses helt i minnet. Det kan gjøres på to måter: som rå forespørselskropp (`await request.body()`, med filnavnet i en egen header), eller med en grense for mellomlagring i Starlette som er større enn største tillatte fil. Sett en største filstørrelse, f.eks. 20 MB, og bestem hva svaret er når fila er for stor. Lag en test som laster opp en fil over 1 MB mens `tempfile.TemporaryFile` er satt til å kaste en feil.

### F2 Høy – Statusoverskriften er ikke entydig

**Kilder:**

- Brief R4: tekstene har symbolet først («✕ Brudd nå»).
- PRD FR15 (3): «tegn for tegn lik teksten i briefen, med symbolet først».
- PRD FR18 (estimert uke).
- EXPERIENCE: symbolet står i en hvit sirkel og har `aria-hidden`. Bare «R4-teksten med eventuell «(uke Y)»» har `aria-live`.
- DESIGN: symbolsirkelen og R4-teksten står på samme linje.

**Problem 1 – symbolet finnes to steder.** Etter AD-2 lager kjernen «statusoverskriften (R4, tegn for tegn som briefen)», og frontend endrer aldri en tekst fra API-et. Etter AD-7 velger frontend symbolet ut fra statuskodene. Da finnes symbolet to steder, og tre løsninger er like rimelige:

- (a) API-et sender «✕ Varsel: …», og frontend viser symbolet i sirkelen i tillegg. Da står symbolet to ganger, og skjermleseren leser det opp i live-regionen.
- (b) Frontend fjerner symbolet fra teksten. Det bryter AD-2.
- (c) API-et sender teksten uten symbol. Da kan ikke T5–T12 sammenligne tegn for tegn med briefen.

Det er heller ikke bestemt om «(uke Y)» er en del av overskriften fra API-et eller et eget felt. Ligger «(uke Y)» i overskriften, er teksten ikke lenger lik briefen.

**Problem 2 – lista over tekster backend eier, er ufullstendig.** AD-2 nevner ikke:

- FR9 «Prognose regnet fra uke X, ÅÅÅÅ». NFR10 vil ha den testet uten nettleser.
- FR23 «Område: Trøndelag – grense som for sør». Teksten er avledet av R1.
- Kryssingsetiketten i grafen, som kombinerer status og uke («✕ Varsel uke 44»).
- FR25a «Dine opplastede tall: {filnavn}».
- Overskriften «Fila har N feil» og grensen på 20 feil. Det er ikke sagt om backend sender alle feilene og frontend viser de 20 første.

AD-2 sier også at *kjernen* lager opplastingsfeilene (FR24), mens lagtabellen legger valideringen i `kilder`.

**Forslag:** Bestem feltene i AD-2 og AD-7, for eksempel:

- `status.symbol` («✕», «!», «✓», «–» eller «?»)
- `status.tekst` (R4-teksten uten symbol)
- `status.uke_tekst` («(uke 16)» eller `null`)

Frontend viser `symbol` i sirkelen med `aria-hidden`, og `tekst` + `uke_tekst` i live-elementet. Testene sjekker `f"{symbol} {tekst}"` mot briefen. Velg om symbolet kommer fra API-et eller fra en fast tabell fra kode til symbol i frontend, ikke begge. Utvid lista i AD-2 med FR9, FR23 og kryssingsetiketten. Skriv at backend sender alle feil, at frontend viser de 20 første, og at feilmeldingene lages i `kilder`.

### F3 Høy – Ruting mellom forside, husket anlegg og opplastede data

**Kilder:**

- PRD FR6a (2): forklaringen vises også når brukeren kommer via «Bytt anlegg» og har et husket anlegg.
- PRD FR6b (1)–(4) og FR26 (tilbakeknappen går til opplastingssiden).
- EXPERIENCE «Ruting ved åpning».
- EXPERIENCE «Toppfelt»: logoen og «Bytt anlegg» går til forsiden, «Søk / bytt» går dit med fokus i søkefeltet, og søk fra toppfeltet viser treflisten på forsiden.
- EXPERIENCE «Navigerer bort fra opplastede data».

**Problem:** AD-8 sier hva som lagres, og AD-9 gir to URL-er for detaljsiden. Men forsiden har bare én URL (`/`), og den skal oppføre seg på to måter:

- Når appen åpnes, skal den sende brukeren videre til det huskede anlegget.
- Via «Bytt anlegg» eller logoen skal den vise intro og søk, selv om et anlegg er husket.

En bygger som sjekker husket anlegg hver gang `/` lastes, gjør forsiden umulig å nå når et anlegg er husket. Detaljsiden må også vite om den ble åpnet fra husket anlegg («Sist viste anlegg») eller fra treflisten.

For opplastede data er det ikke sagt hva `/anlegg?opplastet=1` viser når serien mangler. Det skjer når siden lastes på nytt, når den åpnes i en ny fane, og når brukeren går tilbake hit etter å ha forlatt den. UX-7 krever at tilbakeknappen da går til opplastingssiden.

I tillegg er «komponenttilstand» i AD-4 tvetydig. Serien lages på `/opplasting` og brukes på `/anlegg`. Den må derfor leve over sidebyttet, f.eks. i en kontekst i rot-layouten. Da må den også tømmes aktivt når brukeren forlater detaljsiden.

**Forslag:** Utvid AD-9 med en liten rutetabell som bestemmer:

- hvilken innlasting som sender videre til husket anlegg, f.eks. bare `/` uten parametre ved første innlasting i fanen
- hvilken URL lenkene til forsiden bruker uten videresending, f.eks. `/?sok`
- `/?q=…` for søk fra toppfeltet
- `/anlegg?nr=…&husket=1` for «Sist viste anlegg»

For opplastede data: serien ligger i én modul eller kontekst over sidene og tømmes når detaljsiden forlates. Mangler serien, gjør `/anlegg?opplastet=1` en `replace` til `/opplasting`. Det gir også tilbakeknappen som UX-7 krever.

### F4 Høy – Backtesten mangler definisjon, plassering og sporbarhet

**Kilder:**

- Brief SK2.
- PRD FR27, FR27a, FR28 og M1-C (terskel på 20 %).
- PRD-ordlista: «Varsel: rød status» og «Presisjon: andelen varsler som ble fulgt av brudd innen 4 uker».
- Addendum: «4 774 røde prognosevarsler (ikke «brudd nå»)».

**Problem 1 – definisjonen av presisjon er åpen.** Kildene sier ikke:

- om et varsel er hver uke med rød status eller hver rød periode
- om «brudd nå» teller med. Ordlista sier at rød status er varsel, mens addendumet holdt «brudd nå» utenfor.
- om «brudd innen 4 uker» betyr en måling som er ≥ grensen, eller en kryssing etter SK2

Kantene er heller ikke avklart. Røde uker i 2026 uke 39–42 kan ikke etterprøves, fordi dataene slutter i uke 42. Kryssinger i 2025 uke 1–4 kan ikke ha rød status 2–4 uker før. Valgene flytter Y i FR19 og avgjør om M1-C slår inn. Avklaringen hører hjemme i PRD-en, men spinen binder FR28 uten å flagge den.

**Problem 2 – SK2-logikken har ingen plass.** Kryssing (forrige telling i uke w − 1 eller w − 2), rød periode og treff krever ukeregning over årsskiftet. AD-6 sier at løpende ukenummer bare brukes inne i kjernen, men spinen legger FR27–FR28 i skript-skallet `backtest/`. Da må skallet enten regne uker selv, som bryter AD-6 og gir en ny kilde til årsskiftefeil, eller bruke `{ar, uke}` direkte, som gir feil over årsskiftet. NFR10 krever dessuten en test med kryssinger og treff regnet ut for hånd, og den er lettest å skrive mot rene funksjoner.

**Problem 3 – resultatfila sier ikke hva den er regnet med.** FR27a fryser parameterne (vindu 5, minst 3 tellinger, horisont 6, rød ved 0–3 uker), men AD-10 lagrer bare tallene. Endres en parameter i kjernen etter siste kjøring, viser FR19 tall fra en annen modell, og ingenting sier fra.

**Forslag:**

- (a) Legg SK2-evalueringen (kryssing, rød periode, treff og presisjon) som rene funksjoner i kjernen. `backtest/` leser bare data og skriver fila.
- (b) La `resultat.json` ta med parameterne, siste uke i datagrunnlaget og nevnerne. Ved oppstart sammenligner API-et parameterne med konstantene i kjernen. Er de ulike, vises FR19 uten tall, som når fila mangler.
- (c) Flagg definisjonen av presisjon og kantene som et åpent punkt til PRD-en, og avklar det før A5.

### F5 Høy – «Halvdeler rundes opp» mangler

**Kilder:** brief R2 («Halvdeler rundes opp»), T12 («Uten avrunding kan flyttall gi 0,4999…»).

**Problem:** AD-6 sier «avrundet til 2 desimaler i kjernen», men ikke hvordan. Pythons `round()` runder halvdeler til nærmeste partall og regner med binære flyttall. Sjekket: `round(0.495, 2)` gir 0,49, `round(0.125, 2)` gir 0,12, og `round(0.285, 2)` gir 0,28. Etter R2 skal 0,495 bli 0,50, som er ≥ grensen 0,5. Et estimat på nøyaktig 0,495 gir altså kryssing etter briefen, men ingen kryssing med `round()`. Regresjon på lusetall med 2 desimaler gir ofte estimater med 5 i tredje desimal, så dette vil skje i backtesten. Ingen av T1–T12 har et tilfelle med en halvdel, så testene fanger det ikke.

**Forslag:** Skriv i AD-6 hvordan estimatet regnes og rundes av:

- Lusetall leses som `Decimal` fra tekst.
- Regresjonen regnes eksakt med `fractions.Fraction` eller `Decimal`. Begge er i standardbiblioteket og passer med AD-1.
- Estimatet rundes til slutt med `ROUND_HALF_UP`.
- Sammenligningen med grensen bruker den avrundede verdien.

Bestem også om innleste lusetall med mer enn 2 desimaler (fra CSV) skal rundes av eller brukes som de er. Legg til et testtilfelle med estimat 0,495.

### F6 Middels – Ukene har ingen samlet eier

**Kilder:**

- PRD FR1: uker etter 2026 uke 42 leses ikke inn.
- PRD FR7: uke 53 kan bare velges for ISO-år som har den.
- PRD FR17 (2) og NFR5: «uke 36, 2026».
- PRD FR24: uke 53 i et år uten uke 53 gir feil.
- PRD FR25: analyseuka velges blant ukene fila dekker, og standard er siste uke.
- EXPERIENCE: «Året tas med når uka ligger i et annet år enn analyseuka (f.eks. «uke 2, 2027»)».
- Brief R2: løpende ukenummer.

**Problem:**

- **ISO-uke 53 trengs tre steder:** i kjernen (løpende ukenummer, T12), i `kilder` (valideringen i FR24) og i analyseukevelgeren (FR7). 2026 har 53 ISO-uker, så opplastinger fra slutten av 2026 vil møte uke 53, og horisonten a + 6 vil gå gjennom den. AD-6 sier at løpende ukenummer bare brukes i kjernen, men verken at `kilder` skal bruke kjernens ISO-funksjoner, eller hvor ukelista i velgeren kommer fra.
- **Velgbare uker og standarduke står ikke i API-kontrakten.** For innebygde data må frontend kjenne `SISTE_UKE` og 2025 uke 1. For opplastede data må den kjenne ukene fila dekker. Uten et felt i API-et vil noen skrive `2026, 42` og ukeregning inn i TypeScript. Da finnes `SISTE_UKE` to steder, og frontend regner uker, mot AD-1 og AD-5.
- **Ukeformatet har ingen eier.** AD-6 gir `formatLus` for tall, men ingen tilsvarende regel for uker:
  - «uke 36, 2026» i tabell og velger
  - «uke 44» inne i setninger
  - årstallet tatt med når uka er i et annet år enn analyseuka

  Backend skriver uker i tekstene sine. Frontend skriver uker i tabellen, velgeren, grafen og kryssingsetiketten. Uten én regel vil to byggere velge ulikt.
- **Kuttet ved `SISTE_UKE` må bare gjelde det innebygde datasettet.** Excel-opplasting bruker samme format (FR22) og trolig samme leser i `kilder`. Brukes kuttet der også, forsvinner Karis ferske telling (J3), og det er hele poenget med opplastingen. AD-5 sier bare at `SISTE_UKE` «styrer siste uke i datagrunnlaget».

**Forslag:**

- Utvid AD-6: alle ISO-funksjoner (har året uke 53, neste og forrige uke, løpende ukenummer) ligger i kjernen, og `kilder` og `backtest` bruker dem.
- La API-et sende `analyseuker` og `standard_analyseuke` for både innebygde og opplastede data.
- Bestem én regel for ukeformat og hvem som eier den. Enten sender API-et ferdige ukeetiketter, eller frontend har én `formatUke(uke, analyseuke)` med samme regel som backend.
- Skriv i AD-5 at kuttet ved `SISTE_UKE` bare gjelder det innebygde datasettet.

### F7 Middels – Opplasting via en tilstandsløs server

**Kilder:**

- PRD FR22: fila kan ha flere anlegg, og brukeren velger ett etter opplasting.
- PRD FR23: område utledes av `Fylke`, og «Brukeren velger ikke område».
- PRD FR23a, FR24 og J3 trinn 4.
- Brief R1: «ukjent område» gjelder bare det innebygde datasettet.

**Problem:**

- **Svarformen ved flere anlegg er åpen.** Etter AD-3 svarer `POST /api/opplasting` med «normalisert serie, liste over anlegg å velge fra, eller `feil[]`». Ved en Excel-fil med flere anlegg vet vi ikke om svaret har seriene for alle anleggene, eller om frontend sender fila på nytt med valgt lokalitetsnummer. Et fullt BarentsWatch-uttrekk har over 1 000 lokaliteter og rundt 50 000 rader per år. Det er heller ikke sagt om valideringen i FR24 gjelder hele fila eller bare det valgte anlegget.
- **Serien fra nettleseren valideres ikke på nytt.** `POST /api/prognose` tar imot serie, område og analyseuke fra nettleseren. Spinen sier ikke at serien skal valideres på nytt etter FR24.
- **FR23 kan omgås.** Når området sendes fra nettleseren, kan et utledet område byttes ut. Begrunnelsen for A2 («samme data gir samme svar som innebygd datasett») hviler da på at frontend sender riktig verdi tilbake.
- **`ukjent` er åpen for opplastede data.** Konvensjonene tillater `ukjent` som område, men koden skal ikke kunne brukes for opplastede data (R1, FR23a).

**Forslag:**

- Bestem svarformen ved flere anlegg. Anbefalt: alle anleggene med serie i ett svar, siden fila uansett er lest, og med største filstørrelse fra F1.
- La serien ta med `fylke` når fila har det. Da utleder `POST /api/prognose` området selv når `fylke` finnes, og godtar bare `sor` eller `nord` fra brukeren når den mangler.
- Kjør samme validering i `POST /api/prognose` som ved opplasting (feil gir 422).

### F8 Middels – Grafen: Recharts mot UX-kravene

**Kilder:**

- EXPERIENCE, Responsive & Platform: «Ingen tunge tredjepartsbiblioteker kun for grafen; arkitekturen avgjør».
- EXPERIENCE, Component Patterns: grafen er «Ikke interaktiv i v1».
- EXPERIENCE, Accessibility Floor: grafen har `role="img"`, og innholdet i SVG-en er skjult.
- EXPERIENCE, Interaction Primitives: «Ingen funksjon finnes bare ved hover».
- DESIGN, Typography: «Tekst i en SVG som skaleres med `viewBox` … følger ikke tekstzoom; arkitekturen velger hvordan kravet oppfylles».

**Problem:** Spinen velger Recharts (memlog: «Seed-valg, ikke spurt») uten å svare på de tre punktene UX sendte videre til arkitekturen:

- vekten på siden ved svak mobildekning
- grafetiketter på minst 13 CSS-px som følger tekstzoom
- en graf som er et ikke-interaktivt bilde for skjermleser

Recharts bruker ofte verktøytips ved hover. I Recharts 3 skal `accessibilityLayer` være på som standard, og da kan grafen få tastaturfokus (bør sjekkes mot 3.10.1). Det strider mot `role="img"` og tabulatorrekkefølgen i EXPERIENCE. To byggere vil løse dette ulikt, eller ikke løse det.

**Forslag:** Velg ett av to i spinen:

- (a) En egen SVG-komponent. Grafen har bare rundt 11 uker, punkter, to linjer og en trapp.
- (b) Recharts med faste regler: ingen `Tooltip`, `accessibilityLayer={false}`, en ytre `role="img"` knyttet til tekstoppsummeringen, SVG-innholdet med `aria-hidden`, og etiketter som følger tekstzoom.

Skriv valget i konvensjonene under «Tilgjengelighet».

### F9 Middels – Utdaterte svar når analyseuka byttes

**Kilder:** PRD FR9 (2): «endres teksten, status, graf og tabell (FR15–FR17) samtidig. Ingen av dem viser den gamle uka». EXPERIENCE: utregningen starter ca. 300 ms etter siste endring i velgeren, lastetilstanden leses ikke opp, og bare statusoverskriften er live.

**Problem:** Spinen sier ikke hvordan detaljsiden henter data når analyseuka byttes. Uten en regel kan et sent svar for en uke som ikke lenger er valgt, komme etter svaret for den nye uka og bli vist. Statusoverskriften kan også bli lest opp for hver uke brukeren blar forbi. Det gjelder særlig `POST /api/prognose`, der hele serien sendes hver gang.

**Forslag:** Legg til i konvensjonene:

- Detaljsiden henter én gang per analyseuke, etter 300 ms uten endring i velgeren.
- En forespørsel for en uke som ikke lenger er valgt, avbrytes (`AbortController`), eller svaret ignoreres.
- Hele detaljsiden tegnes fra ett `Detaljsvar`.

### F10 Lav – NFR3 mangler i testkonvensjonen

**Kilder:** PRD NFR3 (R1 testes mot `Lusegrense uke` med 0 avvik). PRD kap. 7: `Lusegrense uke` brukes «bare som fasit i tester (NFR3), ikke i selve beregningen».

**Problem:** Testkonvensjonen nevner T1–T12 og NFR10, men ikke NFR3. Spinen sier heller ikke at `Lusegrense uke` skal holdes ute av `Serie`. Ligger kolonnen i serien, er det fristende å bruke den som grense. Da er R1 ikke lenger testet, og grensen mangler for opplastede data og for ukene i horisonten.

**Forslag:** Ta NFR3 med i testkonvensjonen, og skriv at `kilder` bare leser `Lusegrense uke` til denne testen, aldri inn i `Serie`.

### F11 Lav – Fra fylke til område i opplastede filer

**Kilder:** brief R1 («nord» = Nordland, Troms eller Finnmark, «ellers sør»), PRD FR23, FR24 (år fra og med 2000).

**Problem:** For det innebygde datasettet er koblingen fra fylke til område kontrollert (NFR3, 0 avvik). Opplastede Excel-filer kan derimot være fra 2000 og senere og ha historiske fylkesnavn, f.eks. «Troms og Finnmark» (2020–2023). Krever koden eksakt treff og bruker «ellers sør», blir slike anlegg sør. Da gjelder feil vårgrense, uten at noen merker det.

**Forslag:** Skriv i AD-1 (R1) at koblingen er en lukket liste i kjernen. Lista normaliserer store og små bokstaver og mellomrom, og den tar med historiske navn. Et ukjent fylkesnavn i en opplastet fil behandles som manglende fylke, så brukeren velger område (FR23a). Avklar dette med gruppen, fordi det presiserer «ellers sør» i R1.

### F12 Lav – To tallformater i to språk

**Kilder:** EXPERIENCE Voice and Tone («to desimaler for lusetall (0,41), grensene som 0,5 og 0,2»). DESIGN, graf: «Grense 0,5», og y-aksen «0,0; 0,2; 0,4».

**Problem:** AD-6 har én hjelpefunksjon, `formatLus`, med to desimaler. Grensen skal skrives «0,5», ikke «0,50», og aksen med én desimal. Backend skriver de samme tallene i tekstene sine med sin egen formatering. Uten en felles regel kan grafen og teksten skrive samme grense ulikt.

**Forslag:** Definer to formater i AD-6: lusetall med 2 desimaler, og grense og akse uten null til slutt. Bruk samme regel i Python-tekstene og i hjelperen i TypeScript.

### F13 Lav – FR19 under 20 %, og tekster som avhenger av R4-parameterne

**Kilder:** PRD M1-C, FR19 og FR27a. EXPERIENCE, fargeforklaringen («grensen nås om 1–3 uker», «4–6 uker», «innen 6 uker»).

**Problem:** Det er ikke sagt om FR19-teksten byttes automatisk når presisjonen i resultatfila er under 20 %, eller om teksten skrives om én gang for hånd etter A5. Fargeforklaringen på forsiden er en fast tekst i frontend etter AD-2. Tallene i den er likevel R4-parameterne, og de kan endres fram til de fryses (FR27a).

**Forslag:** Bestem i AD-10 om backend velger tekstvariant ut fra `presisjon < 0,20`, eller om teksten er redaksjonell og endres i kjernen etter A5. Skriv at tekstene på forsiden må oppdateres hvis parameterne endres før de fryses.

### F14 Lav – HTTP-cache

**Kilder:** PRD FR6b (5): «Nettleseren inneholder ingen lusetall fra Marin, bare lokalitetsnummeret». NFR6.

**Problem:** AD-8 holder lusetall ute av `localStorage`. Men `GET /api/anlegg/{nr}/prognose` sendes uten regler for mellomlagring, så nettleseren kan legge svaret med lusetall i HTTP-cachen. Strengt lest bryter det FR6b (5).

**Forslag:** Send `Cache-Control: no-store` på alle svar fra `/api`, og skriv det i konvensjonene.

## FR26-avviket

Det er kjent at AD-4 endrer FR26 fra «minnet til den kjørende appen» til «nettleserfanen», og det er ført i memloggen. Avviket berører også dette:

1. **Serveren kan likevel skrive fila til disk (F1).** Det gjelder uavhengig av omformuleringen.
2. **PRD J3 trinn 4 må endres.** Trinnet har samme ordlyd som FR26 («når appen startes på nytt») og må endres sammen med FR26. Når serien ligger i nettleseren, overlever dataene at serveren startes på nytt, så den delen av FR26 gjelder ikke lenger.
3. **Tilbakeknappen er ikke løst (F3).** Kravet i FR26 og UX-7 om at tilbakeknappen går til opplastingssiden, løses ikke av AD-4 eller AD-9 alene.
4. **FR23 svekkes (F7).** Området kommer nå fra nettleseren.
5. **Uten konflikt:** lagringsnotisen i EXPERIENCE nevner ikke omstart og passer allerede med AD-4. NFR6 og FR6b (3) passer også.

**Forslag:** Før avviket inn i AD-4 som en egen linje, f.eks. «Avvik fra PRD FR26 og J3 trinn 4: …, PRD-en oppdateres». Da står det ikke bare i memloggen.

## Kontrollert uten funn

- R1 (vårperioden per område, sør uke 16–21 og nord uke 21–26), R3 (grensen per uke i horisonten), rekkefølgen i R4 og de sju statusårsakene: dekket av AD-1 og AD-7.
- Analyseuka og t: kjernen tar analyseuka som argument og bruker ingen systemdato (AD-5).
- NFR7 (ingen KI), NFR1 og NFR9 (ingen nøkler, data i `data/`, testdata i egen mappe) og NFR11 (README).
- Lagring for FR6b: bare lokalitetsnummeret lagres, appen tåler at lagringen mangler, og 404 gir forsiden (AD-8).
- FR19 når resultatfila mangler (AD-10).
- Statusfarger, bare lys modus, systemfonter og tokens: konvensjonen for styling følger DESIGN.md.
- NFR8: datasettet ligger i minnet fra oppstart. Oppstartstiden er utenfor kravet.
- Tone: backend eier de forklarende tekstene (AD-2), og de kan testes med pytest (NFR10).

## Andre observasjoner (utenfor avstemmingen, bør sjekkes)

- **TypeScript 7.0:** versjonen bygger på en ny kompilator. `openapi-typescript` lager typene med TypeScripts JS-API, og Next.js bruker TypeScript i bygget. Sjekk at begge virker med 7.0.2 før AD-3 låses. Hvis ikke, fest TypeScript til siste versjon som virker.
- **Statisk eksport (AD-9):** Next.js lager som standard `anlegg.html` ved statisk eksport. `StaticFiles(html=True)` i FastAPI ser etter `anlegg/index.html`, ikke `anlegg.html`. Uten `trailingSlash: true` i Next eller en egen reserverute gir `/anlegg?nr=…` 404 i oppsettet for innlevering.

## Bevisst utelatt (story-nivå)

- Eksemplene på tekstoppsummering i EXPERIENCE dekker 6 uker («uke 37–42»), mens vinduet er på 5.
- FR16 (3) sier at uker uten telling ikke vises som punkter, mens DESIGN tegner et hult punkt på x-aksen for «ikke telt».
- Radnummer i feilmeldinger (rad i fila eller rad med data), største antall søketreff, og ordlyden «X % av bruddene» i FR19, der treffandelen gjelder kryssinger.
