---
title: "Tilgjengelighetsgjennomgang: Marin UX-spesifikasjon"
reviewed: 2026-11-12
standard: WCAG 2.2 nivå AA
scope:
  - DESIGN.md (tokens, kontrast, komponenter)
  - EXPERIENCE.md (Accessibility Floor, tilstander, interaksjon, komponentoppførsel)
  - .working/directions-1.html (bare retning A), .working/key-forside.html, .working/key-opplasting.html (illustrasjoner, ikke kontrakt)
  - PRD NFR4 (../../prds/prd-Marin-2026-11-02/prd.md)
---

# Tilgjengelighetsgjennomgang – Marin

## Konklusjon

Spinene har et godt grunnlag. Alle tekstpar holder AA. Status vises med farge, symbol og tekst (NFR4). `lang="nb"` er satt, feilmeldingen får fokus og det er ingen animasjon. Jeg fant ingen kritiske brudd. Fem funn med høy alvorlighet må likevel rettes før arkitektur og epics bygger videre:

1. DESIGN.md sier at rød og grønn skilles på lyshet. Det stemmer ikke: de to fargene står i 1,06:1 mot hverandre.
2. Tekstalternativet for grafen dekker ikke prognoseverdiene eller trappen i grensen.
3. Teksten i SVG-grafen krymper under gulvet på 13px.
4. Feil og påkrevde valg i opplastingsskjemaet er bare delvis spesifisert.
5. Søkefeltet i toppfeltet på desktop har bare plassholdertekst og ingen søkeknapp.

**Antall funn:** kritisk 0 · høy 5 · middels 7 · lav 7.

---

## 1. Kontrastregnskap (regnet på nytt fra hex-verdiene i DESIGN.md)

Formelen er WCAG 2.x for relativ luminans. Krav: 4,5:1 for normal tekst, 3:1 for stor tekst og for ikke-tekstlige elementer (1.4.3 og 1.4.11).

### Tekst

| Par | Forgrunn | Bakgrunn | Utregnet | DESIGN.md sier | Krav | Resultat |
|---|---|---|---|---|---|---|
| Blekk på hvit | #111418 | #FFFFFF | 18,47 | 18,5 | 4,5 | OK |
| Sekundærtekst på hvit (også plassholder) | #4A5059 | #FFFFFF | 8,13 | 8,1 | 4,5 | OK |
| Aksent (lenke) på hvit | #0B3D91 | #FFFFFF | 10,04 | 10,0 | 4,5 | OK |
| Hvit på rød flate | #FFFFFF | #B3261E | 6,54 | 6,5 | 4,5 | OK |
| Mørk på gul flate | #1A1400 | #F5B800 | 10,26 | 10,3 | 4,5 | OK |
| Hvit på grønn flate | #FFFFFF | #1B6E4F | 6,19 | 6,2 | 4,5 | OK |
| Grå statustekst på hvit | #3F4650 | #FFFFFF | 9,53 | 9,5 | 4,5 | OK |
| Rødt symbol på hvit (merke, graf) | #B3261E | #FFFFFF | 6,54 | 6,5 | 3 / 4,5 | OK |
| Grønt symbol på hvit | #1B6E4F | #FFFFFF | 6,19 | 6,2 | 3 / 4,5 | OK |
| Gult symbol (mørk) på hvit | #1A1400 | #FFFFFF | ≈ 19 | – | 3 | OK |
| Blekk på aktiv rad (aksent-tone) | #111418 | #E7EDF7 | 15,70 | – | 4,5 | OK |
| Sekundærtekst på aktiv rad | #4A5059 | #E7EDF7 | 6,91 | – | 4,5 | OK |
| Retning A: metalinje med `opacity:.95` på rød | ≈#FBF4F4 | #B3261E | 6,02 | – | 4,5 | OK, men opasitet står ikke i spinen og bør ikke innføres |

Alle tallene i DESIGN.md stemmer, avrundet til én desimal.

### Ikke-tekstlige elementer (1.4.11)

| Element | Farge | Mot | Utregnet | Krav | Resultat |
|---|---|---|---|---|---|
| Skjemafeltkant (`border-strong`) | #8A919A | #FFFFFF | 3,18 | 3 | OK, men med liten margin (se M7) |
| Stiplet grå statuskant (2px boks, 1px merke) | #8A919A | #FFFFFF | 3,18 | 3* | OK. Stipling gir mindre «blekk» og svakere opplevd kontrast. |
| Analyseukelinje i graf (1px prikket) | #8A919A | #FFFFFF | 3,18 | 3 | Grenseverdi. Prikket 1px er svak ute i sollys. |
| «Ikke telt»-punkt (stiplet) | #8A919A | #FFFFFF | 3,18 | 3 | OK. Teksten «ikke telt» bærer meningen. |
| Gul flate mot hvit side | #F5B800 | #FFFFFF | 1,79 | – | Ikke nok alene. Kanten gjør jobben. |
| Gul kant mot hvit | #8A6A00 | #FFFFFF | 5,07 | 3 | OK. DESIGN.md oppgir ikke dette tallet, og det bør føres inn. |
| Gul kant mot gul flate | #8A6A00 | #F5B800 | 2,83 | – | Ikke relevant, siden grensen mot siden er kant mot hvit. |
| Rød og grønn flate mot hvit side | #B3261E / #1B6E4F | #FFFFFF | 6,54 / 6,19 | 3 | OK |
| Statusmerke-kant (`border`) | #E3E6EA | #FFFFFF | 1,25 | (3) | Godtas bare fordi merket ikke er interaktivt og teksten bærer meningen (se L1). |
| Rutenett | #E3E6EA | #FFFFFF | 1,25 | – | Dekorativt, OK |
| Målte punkter og linje (aksent) | #0B3D91 | #FFFFFF | 10,04 | 3 | OK |
| Trend gjennom vinduet, «redusert styrke» (retning A: `opacity .55` ≈ #7994C3) | #7994C3 | #FFFFFF | 3,07 | 3 | Grenseverdi. Spinen tallfester ikke «redusert styrke» (se M7). |
| Grenselinje (blekk 2px) | #111418 | #FFFFFF | 18,47 | 3 | OK |
| Grenselinje mot trendlinje | #111418 | #0B3D91 | 1,84 | – | Linjene skilles på strek og direkte etikett, ikke på kontrast (se M7) |
| Kryssingslinje rød / gul | #B3261E / #8A6A00 | #FFFFFF | 6,54 / 5,07 | 3 | OK |
| Fokusring (2px aksent, 2px avstand) | #0B3D91 | #FFFFFF | 10,04 | 3 | OK |
| Fokusring på aktiv rad | #0B3D91 | #E7EDF7 | 8,54 | 3 | OK |
| Aktiv rad (aksent-tone) mot hvit | #E7EDF7 | #FFFFFF | 1,18 | 3 hvis den er eneste fokusindikator | **Ikke godkjent alene** (se M3) |

\* 1.4.11 gjelder ikke strengt for statuskanten, fordi status også bæres av tekst. Kanten er likevel det eneste som skiller grå boks fra bakgrunnen.

### Statusfarger seg imellom og ved fargesynsvikt

Simuleringen er gjort etter Machado 2009 med full alvorlighetsgrad. ΔE er CIELAB 1976.

| Par | Normalt syn | Protanopi | Deuteranopi | Tritanopi |
|---|---|---|---|---|
| Rød #B3261E mot grønn #1B6E4F | kontrast **1,06:1**, L* 39,7 mot 41,1, ΔE 92 (bare kulør) | #534A1B mot #6C664D, ΔE 18, 1,54:1 | #756916 mot #615E51, ΔE 37, **1,17:1** | ΔE 104 |
| Rød #B3261E mot gul kant #8A6A00 (kryssingslinje i graf) | ΔE stor | ΔE 26 | #756916 mot #80720A, **ΔE 7,8** – praktisk talt like | ΔE 52 |
| Grønt symbol mot grått symbol #3F4650 | tydelig | ΔE 26 | ΔE 18,5 | ΔE 26 |

---

## 2. Funn

### Kritisk

Ingen.

### Høy

#### H1 – Rød og grønn har samme lyshet. Påstanden i DESIGN.md er feil.

- **Sted:** DESIGN.md › Colors, avsnittet under statustabellen («De skilles derfor også på lyshet og symbol, ikke bare på kulør»). EXPERIENCE.md › Key Flows UJ-1 steg 5 («Klimaks: fargen»). Responsive & Platform › Sollys.
- **WCAG:** 1.4.1 Bruk av farge. Kravet er formelt oppfylt fordi symbol og tekst følger med. Funnet gjelder NFR4 og produktets kjerneopplevelse.
- **Hvorfor det betyr noe:** #B3261E og #1B6E4F har relativ luminans som står i 1,06:1 mot hverandre (L* 39,7 mot 41,1). De skilles bare på kulør. Fire situasjoner gjør dem vanskelige å skille:
  - **Fargesynsvikt:** ved deuteranopi blir de oliven (#756916) mot gråoliven (#615E51), 1,17:1. Rundt 8 % av norske menn har rød-grønn fargesynsvikt, og målgruppen er driftsledere med stor andel menn.
  - **Sollys:** blending tar metningen først, og da gjenstår to like mørke flater.
  - **Skjermbilde:** et bilde som skrives ut eller vises i gråtoner, gir to like grå bokser.
  - **Små merker:** symbolet er 12–13px, og fargen på så små tegn er svært vanskelig å oppfatte.

  UJ-1 beskriver fargen som klimaks. Det er nettopp der fargen svikter for en del av brukerne og i felt. Symbol og tekst redder forståelsen, men spinen lover noe paletten ikke holder.
- **Forslag til tiltak:**
  1. Fjern eller rett påstanden om lyshet i DESIGN.md, og før inn tallet rød mot grønn = 1,06:1 som kjent begrensning.
  2. Velg ett av disse alternativene:
     - **(a) Skill fargene på lyshet.** Eksempel: mørkere rød #8F1A14 med hvit tekst (9,03:1) og lysere grønn #4CB07E med mørk tekst #0B1F14 (6,41:1). Da står rød mot grønn i 3,36:1. Ulempen er at grønn og gul havner nær hverandre i lyshet (1,5:1), så kombinasjonen må testes i en CVD-simulator og i gråtoner før den tas i bruk.
     - **(b) Behold fargene og styrk formkanalen.** Sett symbolet i statusboksen i en hvit sirkel eller rute med symbolet i statusfarge, minst 32px på desktop og 28px på mobil. Da skiller ✕ og ✓ seg tydelig også i gråtoner og i sollys.
  3. Legg inn en sjekk i README-sjekklista (NFR10): statusboksene for rød, gul, grønn og grå i gråtoner og med deuteranopi-simulering.

#### H2 – Tekstalternativet for grafen er ufullstendig

- **Sted:** EXPERIENCE.md › Accessibility Floor › Skjermleser, punkt 3. Component Patterns › Graf. State Patterns, tabellen (grå – ukjent område). DESIGN.md › Components › Graf.
- **WCAG:** 1.1.1 Ikke-tekstlig innhold, 1.3.1 Informasjon og relasjoner.
- **Hvorfor det betyr noe:** Oppsummeringen («Målte lusetall uke 38–42, trendlinje til uke 48 og grense 0,5. Trend når grensen i uke 44.») og ukestabellen er det eneste tekstalternativet. Mye av det grafen viser, finnes ikke i tekst:
  - **Prognoseverdiene:** hva trenden er i uke 43–48. Tabellen har bare målte uker.
  - **Grensen som trapp:** når vårgrensen på 0,2 slår inn, sier oppsummeringen fortsatt «grense 0,5». Det er direkte feil for en skjermleserbruker. Det er også særlig viktig fordi kryssingen ofte skyldes trappen og ikke stigende tall.
  - **Målte uker utenfor tabellen:** i grå-varianten i retning A viser grafen uke 37–42, mens tabellen viser 37–41.
  - **Hull i serien:** uker uten telling.
  - **Ukjent område:** ingen oppsummeringstekst er spesifisert, bare tegnforklaringen «Grensen er ukjent».

  I tillegg er oppsummeringen bare en `aria-label`. Den er usynlig for seende brukere som har problemer med å lese grafer, eller som står i sollys.
- **Forslag til tiltak:**
  - Utvid malen for oppsummeringen: «Målte lusetall uke 37–42, siste 0,41 i uke 42. Trenden er 0,48 i uke 44 og 0,55 i uke 46. Grensen er 0,5 til og med uke 47 og 0,2 fra uke 48. Trend når grensen i uke 44.»
  - Skriv en egen mal for «ukjent område» og en for «brudd nå».
  - Knytt grafen til en synlig figurtekst med `<figure>` + `<figcaption>` (eller `aria-describedby`), slik at teksten er tilgjengelig for alle.
  - Vurder en lukket `<details>`-blokk, «Vis tallene i grafen», med en tabell per uke i vinduet: målt, trend, grense.
  - Bruk `role="img"` på SVG, og la alle inndelinger i den være `aria-hidden`.

#### H3 – Teksten i SVG-grafen skalerer med viewBox og går under gulvet på 13px

- **Sted:** DESIGN.md › Typography (`chart-label`: «13px er gulvet også på mobil»). DESIGN.md › Layout & Spacing (bruddpunkt 600px). EXPERIENCE.md › Accessibility Floor › Tekststørrelse.
- **WCAG:** 1.4.4 Endring av tekststørrelse. 1.4.12 Tekstavstand (indirekte). Leselighet utendørs.
- **Hvorfor det betyr noe:** Retning A tegner grafen med fast `viewBox` (700 brede enheter på desktop, 330 på mobil) og `width:100%`. Skriftstørrelsen er i brukerenheter, så teksten skaleres med beholderen og ikke med CSS-piksler:
  - Rett over bruddpunktet, med viewport 600px og innhold ca. 536px, blir 13 enheter ≈ **10px**.
  - Ved 320px viewport, med innhold 288px og mobilgrafen, blir de ≈ **11,3px**.
  - Ren tekstzoom (for eksempel Firefox «Bare tekst») påvirker ikke SVG-tekst i brukerenheter i det hele tatt.

  Gulvet på 13px som DESIGN.md setter, holder derfor ikke i praksis. Akseetiketter, «Grense 0,5» og «uke 44» er nettopp det Kari leser ute.
- **Forslag til tiltak:** Gjør gulvet til et krav om *gjengitt* CSS-størrelse: «Grafetiketter er minst 13 CSS-px ved alle bredder og følger tekstzoom.» To mulige løsninger for arkitekturen:
  - Etiketter og tegnforklaring som HTML lagt over eller rundt SVG.
  - En viewBox som regnes ut fra faktisk bredde (ResizeObserver), slik at én enhet er én CSS-piksel.

  Ta 320px, 600px og 200 % tekstzoom med i sjekklista.

#### H4 – Opplastingsskjemaet: feil, påkrevde valg og fokus er bare delvis spesifisert

- **Sted:** EXPERIENCE.md › Component Patterns › Opplastingsskjema og Feilmelding. State Patterns › Feil i fil (FR24), Område må velges, Laster / leser fil. Accessibility Floor (feilmelding får fokus). DESIGN.md › Components › Opplastingsskjema, Feilmelding.
- **WCAG:** 3.3.1 Identifikasjon av feil, 3.3.2 Ledetekster eller instruksjoner, 3.3.3 Forslag ved feil, 1.3.1, 4.1.2 Navn, rolle, verdi, 4.1.3 Statusbeskjeder, 2.4.3 Fokusrekkefølge, 3.3.7 Overflødig inntasting.
- **Hvorfor det betyr noe:** Filfeil (FR24) er godt beskrevet: radnummer, hva som er galt og hvordan det rettes. Det er bra for 3.3.3. Følgende mangler:
  1. **Påkrevd område (sør/nord) og anleggsvalg.** Spinen sier «påkrevd før Vis prognose», men ikke hva som skjer hvis brukeren trykker «Vis prognose» uten å ha valgt. Er knappen deaktivert, eller kommer det en feilmelding? Deaktiverte knapper forklarer ikke hvorfor de ikke virker, og de nås ofte ikke med Tab.
  2. **Kobling til feltet.** Ingenting sier at filfeltet får `aria-invalid="true"` og `aria-describedby` som peker på feilmeldingen og hjelpeteksten. I skissen er «Fil» en `<span>` og ikke en `<label>`, og hjelpeteksten er ikke koblet til feltet. Spinen må ta stilling, ellers blir skissen fasit.
  3. **Fokus etter at brukeren har rettet fila.** Når ny fil leses inn uten feil, forsvinner feilmeldingen, og anleggsvalg eller områdevalg dukker opp. Hvor går fokus, og hva leses opp? Hvis det ikke er spesifisert, havner skjermleserbrukeren i et tomrom.
  4. **«Leser fila …»** er ikke definert som statusbeskjed (`role="status"`).
  5. **Lange feillister.** «Alle feil som finnes listes» kan bli hundrevis av linjer, og alt leses opp når boksen får fokus.
  6. **Dobbel opplesing.** Skissen kombinerer `role="alert"` med programmatisk fokus, og det gir dobbel opplesing i flere skjermlesere.
  7. **Områdevalget ved ny fil.** Ved ny opplasting i samme økt må brukeren velge område på nytt (3.3.7).
- **Forslag til tiltak:** Legg til en underseksjon «Skjemafeil» i EXPERIENCE.md:
  - «Vis prognose» er alltid aktiv. Mangler område eller anlegg, vises en feil ved gruppen («Velg område: sør eller nord.»), gruppen får `aria-invalid` og `aria-describedby`, og fokus flyttes til første radioknapp i gruppen.
  - Filfeltet er et ekte `<input type="file">` med `<label for>` «Fil» og `aria-describedby` = hjelpetekst. Ved feil kommer feilmeldingens id i tillegg, og feltet får `aria-invalid="true"`.
  - Feilmeldingen bruker *enten* fokus (`tabindex="-1"`) *eller* `role="alert"`, ikke begge. Anbefalt er fokus, med overskriften som tilgjengelig navn.
  - Vis de første 20 feilene og en linje om resten («… og 134 feil til av samme slag i rad 30–410.»).
  - Etter vellykket ny innlesing: statusbeskjeden «Fila er lest. Velg anlegg.» eller «Velg område.», og fokus til overskriften for neste steg.
  - Statusbeskjeden for «Leser fila …» ligger i en live-region som finnes i DOM fra starten.
  - Områdevalget beholdes hvis den nye fila er av samme type.

#### H5 – Søkefeltet i toppfeltet har ingen synlig etikett og ingen søkeknapp

- **Sted:** DESIGN.md › Components › Toppfelt og Søkefelt. EXPERIENCE.md › Component Patterns › Toppfelt og Søkefelt («Søket kjøres ved Enter eller knappen «Søk»»). Interaction Primitives. Skisse: retning A og key-opplasting (desktop-toppfeltet).
- **WCAG:** 3.3.2 Ledetekster eller instruksjoner, 1.3.1, 4.1.2, 2.5.3 Etikett i navn.
- **Hvorfor det betyr noe:** Toppfeltet på desktop viser søkefeltet med bare plassholderteksten «Søk anlegg – navn eller lokalitetsnr.». Plassholderen forsvinner når brukeren begynner å skrive. Den er ikke en etikett for talestyring, og den har dårlig støtte som tilgjengelig navn. Spinen lover dessuten en «Søk»-knapp som ikke finnes i toppfeltet. Brukere av talestyring og brukere som ikke vet at Enter sender skjemaet, står fast. Toppfeltet finnes på alle sider unntatt forsiden.
- **Forslag til tiltak:**
  - Gi feltet en etikett: enten synlig («Søk anlegg»), eller visuelt skjult `<label>` med samme tekst som plassholderen starter med.
  - Legg til en «Søk»-knapp, eventuelt ikon med tilgjengelig navn «Søk», minst 24 × 24px.
  - Pakk feltet i `<form role="search">`.
  - Før dette inn i DESIGN.md › Toppfelt og i tabellen over mikrotekst i EXPERIENCE.md.

### Middels

#### M1 – `aria-live` på hele statusboksen, og lastetilstand som ligner grå status

- **Sted:** EXPERIENCE.md › Accessibility Floor (Statusboksen … `aria-live="polite"`). State Patterns › Laster (detaljside). Component Patterns › Analyseukevelger.
- **WCAG:** 4.1.3 Statusbeskjeder, 1.3.1, 1.4.1 (visuelt), 3.2.2 Ved inndata (vurdert, se nedenfor).
- **Hvorfor det betyr noe:**
  1. **For lang opplesing.** Når hele regionen er live, leses navn, lokalitetsnr., sted, «Prognose regnet fra …», statusen og den forklarende setningen opp ved hver endring.
  2. **Mistet opplesing.** Hvis rammeverket bytter ut boksen i stedet for å oppdatere innholdet, går opplesingen tapt, fordi live-regionen må finnes før endringen.
  3. **Opplesing per pil.** I en lukket nedtrekksliste på Windows utløser piltastene `change` for hver uke. Hver pil gir ny utregning og ny opplesing, og den mellomliggende «Regner ut prognose …» leses også.
  4. **Lastetilstanden ser ut som grå status.** «Regner ut prognose …» i grå stiplet ramme ser ut som grå status («ingen prognose»). Et skjermbilde tatt i det øyeblikket er misvisende.

  3.2.2 er oppfylt, fordi valget endrer innhold og ikke kontekst.
- **Forslag til tiltak:**
  - Ikke gjør statusboksen live. Bruk en egen, visuelt skjult `role="status"` som alltid finnes i DOM, og som får én kort setning når resultatet er klart: «Uke 41, 2026: Varsel: grensen nås om 2 uker (uke 43).» Ikke les opp lastetilstanden.
  - Vent rundt 300 ms etter siste endring i velgeren før utregningen starter.
  - Gi lastetilstanden en egen visuell form, for eksempel heltrukken `{colors.border}`-ramme og teksten uten statussymbol, slik at den ikke kan forveksles med grå status.

#### M2 – Reflow er spesifisert for 200 %, men kravet er 320 CSS-px (400 %)

- **Sted:** EXPERIENCE.md › Accessibility Floor › Tekststørrelse. Responsive & Platform. DESIGN.md › Layout & Spacing. Component Patterns › Statusboks («Hele boksen er synlig uten rulling på desktop»).
- **WCAG:** 1.4.10 Dynamisk tilpasning (reflow), 1.4.12 Tekstavstand, 1.4.4.
- **Hvorfor det betyr noe:** 1.4.10 krever at innholdet fungerer i 320 CSS-px bredde (tilsvarer 400 % zoom på 1280px) uten vannrett rulling. Kjente risikoer i spesifikasjonen:
  - **Toppfeltet på mobil:** logo, «Søk / bytt» og «Last opp egne tall» med 14px mellomrom trenger ca. 290px, mens det er 288px tilgjengelig ved 320px og 16px marg. Toppfeltet må få bryte linje.
  - **Statusmerker:** de har `white-space:nowrap`, og fargeforklaringen har fast merkebredde på 96px. Begge kan klippes med økt tekstavstand (1.4.12).
  - **Statusboksen:** kravet om at den skal være synlig uten rulling på desktop, kan ikke holdes ved zoom og bør gjelde bare ved 100 %.
- **Forslag til tiltak:**
  - Skriv om kravet til «Siden fungerer ved 320 CSS-px bredde og 400 % zoom uten vannrett rulling, og med tekstavstand etter 1.4.12 uten tap av innhold.»
  - Toppfeltet bryter til to linjer ved behov.
  - Bruk `min-width` i stedet for fast `flex-basis` på merkene, og tillat linjebryting i merketekst over to ord.
  - Ta med 320px og bokmerket for tekstavstand i README-sjekklista.

#### M3 – Treflisten: «aktiv rad» og «piltaster» er et udefinert mønster

- **Sted:** DESIGN.md › Colors (aksent-tone «markerer aktiv rad i treflisten ved tastaturnavigering»). EXPERIENCE.md › Component Patterns › Trefliste og Søkefelt. Accessibility Floor › Tastatur. Skisse: key-forside, seksjon 2.
- **WCAG:** 2.4.7 Synlig fokus, 1.4.11, 2.4.3 Fokusrekkefølge, 4.1.2, 4.1.3.
- **Hvorfor det betyr noe:** Aksent-tonen #E7EDF7 står i 1,18:1 mot hvit. Er den eneste markering av aktiv rad, er fokus usynlig for mange. Det er heller ikke spesifisert om listen er vanlige lenker (Tab mellom rader) eller en combobox/listbox med piltaster og `aria-activedescendant`. Det er to helt forskjellige implementasjoner. I tillegg mangler to ting etter søk:
  - Ingen statusbeskjed med antall treff («3 anlegg funnet»). Bare «ingen treff» er live.
  - Ikke sagt hvor fokus havner. Søk fra toppfeltet navigerer til forsiden.
- **Forslag til tiltak:**
  - Velg det enkle mønsteret: en liste av vanlige lenker, Tab mellom radene, fokusring (`focus-ring`) på hele raden og aksent-tone bare som tillegg ved hover og fokus. Stryk «piltaster» for treflisten.
  - Etter søk: legg statusbeskjeden «N anlegg funnet for «lang»» i den samme `role="status"`-regionen som «ingen treff», og la fokus bli i søkefeltet. Ved søk fra toppfeltet får forsidens søkefelt fokus med søketeksten i.

#### M4 – Gul har ingen gul farge utenfor statusboksen, og rød og gul smelter sammen i grafen ved deuteranopi

- **Sted:** DESIGN.md › Colors (status nøytral) og Components › Statusmerke og Graf (kryssing). EXPERIENCE.md › Accessibility Floor (NFR4 «også i statusmerker og graf-markør»). Component Patterns › Fargeforklaring.
- **WCAG:** 1.4.1 (oppfylt via tekst og symbol), PRD NFR4. Gjelder forståelighet.
- **Hvorfor det betyr noe:**
  - **Gul i merker og graf.** Symbolet er #1A1400 (nesten svart), og kanten er #8A6A00 (mørk oliven). Fargeforklaringen viser «! Gul» uten noe som er gult. Kari kan ikke koble legenden til den gule statusboksen, og fargeleddet i NFR4 («farge + symbol + tekst») mangler i praksis for gul.
  - **Kryssingslinjen ved deuteranopi.** Rød (#B3261E) og gul kant (#8A6A00) blir #756916 og #80720A, med ΔE 7,8, altså i praksis samme farge. Bare det 13px store symbolet i etiketten skiller dem.
  - **Etiketten i grafen.** «✕ uke 44» har symbol og farge, men ingen statustekst.
- **Forslag til tiltak:**
  - Gi statusmerket en liten fylt rute eller prikk på 10–12px i `*-fill`, med `*-border`-kant og symbolet inni eller ved siden av (som «pill-mid» i retning B, men liten). Da holder «status nøytral», og gul blir faktisk gul. For gul: #F5B800 med kant #8A6A00 (5,07:1 mot hvit).
  - Gi kryssingsmarkøren ulik form per status, for eksempel kvadrat for rød og trekant for gul.
  - Skriv statusordet i etiketten: «✕ Varsel uke 44» og «! Følg med uke 46».

#### M5 – Sidetitler, fokus ved sidebytte og autofokus er ikke spesifisert

- **Sted:** EXPERIENCE.md › Information Architecture, Interaction Primitives og Accessibility Floor. Skisse: key-forside, seksjon 1 («Søkefeltet har fokus»).
- **WCAG:** 2.4.2 Sidetitler, 2.4.3 Fokusrekkefølge, 3.2.1 Ved fokus.
- **Hvorfor det betyr noe:** Rammeverket er ikke valgt, og en SPA bytter visning uten ny `<title>` og uten å flytte fokus. Skjermleserbrukere får da ikke vite at de er på detaljsiden, for eksempel etter «Vis prognose», valg i treflisten eller «Søk / bytt». Autofokus på søkefeltet ved første besøk gjør dessuten at skjermleseren hopper over intro og fargeforklaring, som er hele poenget med forsiden ved første besøk.
- **Forslag til tiltak:**
  - Spesifiser `<title>` per flate: «Langholmen – status uke 42, 2026 – Marin», «Finn anlegget ditt – Marin», «Last opp egne tall – Marin». Ved opplastede data: «Egne tall: Langholmen – …».
  - Ved hver navigering: fokus til `<h1>`.
  - Ingen autofokus ved første innlasting av forsiden. Autofokus på søkefeltet bare når brukeren kommer fra «Søk / bytt».

#### M6 – Målstørrelse: 44px gjelder bare mobil, og skissen holder ikke regelen

- **Sted:** EXPERIENCE.md › Interaction Primitives («Trykkflater minst 44 × 44 px på mobil»). DESIGN.md › Components (toppfelt, analyseukevelger, knapper, opplastingsskjema).
- **WCAG:** 2.5.8 Målstørrelse (minimum), 24 × 24 CSS-px eller nok avstand.
- **Hvorfor det betyr noe:**
  - **Desktop** har ingen minstemål. 2.5.8 gjelder alle bredder, og en PC kan også ha berøringsskjerm.
  - **Skissen:** lenkene i toppfeltet på mobil («Søk / bytt», «Last opp egne tall», 15px) har ingen `min-height` og er ca. 23px høye. Logoen er ikke en lenke.
  - **Radioknapper** for sør/nord er «standard radioknapper» (ca. 13px). De holder bare hvis etiketten er klikkbar og avstanden er stor nok.
  - **Ute på merden** brukes mobilen ofte med våte eller kalde fingre, og der trengs mer enn minstemålet.
- **Forslag til tiltak:** Skriv inn som regel: «Alle interaktive mål er minst 24 × 24 CSS-px på alle bredder og 44 × 44 på mobil. Det gjelder logo, toppfeltlenker, analyseukevelger, søkeknapp, filknapp, radioknapper med etikett og rader i treflisten. Radioknapper har klikkbar etikett over hele raden.»

#### M7 – Sollys: flere elementer ligger rett på 3:1, og noen tekster er små

- **Sted:** DESIGN.md › Colors (`border-strong`), Typography (`pill-xs` 12px, `chart-label` 13px, `meta-mobile` og `caption` 14px) og Components › Graf («redusert styrke», 1px prikket analyseukelinje, målelinje 1,25px i skissen). EXPERIENCE.md › Responsive & Platform › Sollys.
- **WCAG:** 1.4.11 er oppfylt, men med liten margin. Gjelder produktkravet om utendørs bruk.
- **Hvorfor det betyr noe:** Sollys og refleks kan redusere effektiv kontrast med en faktor 3–10. Elementer som ligger på 3,07–3,18:1, forsvinner først:
  - stiplet grå kant
  - analyseukelinjen
  - trendlinjen med 55 % styrke
  - kanten på skjemafeltene

  Grenselinjen (blekk) og trendlinjen (aksent) står i 1,84:1 mot hverandre og skilles på strek. Det holder bare så lenge strekene er tydelige. Avsnittet «Sollys» i spinen nevner bare statusboksens tekst.
- **Forslag til tiltak:**
  - Tallfest «redusert styrke» som egen farge med minst 4,5:1, for eksempel ved å la aksentfargen være heltrukken og skille historikk fra prognose bare med stiplet strek.
  - Analyseukelinjen 1,5px. Målelinjen minst 2px.
  - Vurder 2px stiplet kant også på grått statusmerke.
  - Løft `pill-xs` til 13px og `meta-mobile` til 15px.
  - Utvid avsnittet «Sollys» til hele siden, ikke bare statusboksen.

### Lav

#### L1 – Kanten på statusmerket (`border`, 1,25:1) er bare forsvarlig fordi merket ikke er interaktivt

- **Sted:** DESIGN.md › Components › Statusmerke. EXPERIENCE.md › Component Patterns › Statusmerke.
- **WCAG:** 1.4.11.
- **Hvorfor det betyr noe:** Dette er OK i dag. Blir merket klikkbart senere (samlet oversikt i neste versjon), feiler kanten.
- **Forslag til tiltak:** Skriv i DESIGN.md at interaktive merker skal ha kant på minst 3:1.

#### L2 – Ukestabellen: semantikk og «–»

- **Sted:** DESIGN.md og EXPERIENCE.md › Ukestabell.
- **WCAG:** 1.3.1.
- **Forslag til tiltak:**
  - Koble tabellen til `<h2>` med `aria-labelledby`, eller bruk `<caption>`.
  - Bruk `<th scope="col">`.
  - «–» i tallcellen leses som «tankestrek». Gi den visuelt skjult tekst «ikke telt», eller `aria-hidden` på streken når merknaden alltid følger.
  - Symbolet i merket «– Ikke telt» skal ligge i eget `aria-hidden`-element, slik det er gjort i fargeforklaringen.

#### L3 – Landemerker, overskrifter og logo

- **Sted:** DESIGN.md › Toppfelt. EXPERIENCE.md › Component Patterns › Toppfelt («Logoen går til forsiden»). Skisser.
- **WCAG:** 1.3.1, 2.4.1 Hoppe over blokker, 2.4.4, 2.4.6.
- **Hvorfor det betyr noe:**
  - Forsiden i skissen har ingen `<h1>`.
  - Logoen er en `<span>` i retning A, ikke en lenke.
  - Toppfeltet er kort, men landemerker eller en hopplenke er billig og løser 2.4.1 sikkert.
- **Forslag til tiltak:**
  - Forsiden får `<h1>` («Finn anlegget ditt», eller «Marin» skjult).
  - Logoen blir en lenke med navnet «Marin, til forsiden».
  - Bruk `<header>`, `<main>` og `<nav aria-label="Hovedmeny">`, og en hopplenke «Til innholdet».

#### L4 – «Prognose regnet fra uke 42, 2026» står også i grå status, der det ikke finnes noen prognose

- **Sted:** EXPERIENCE.md › Component Patterns › Statusboks og Annen mikrotekst. Skisse: retning A, grå-varianten.
- **WCAG:** 3.3.2 / forståelighet (kognitivt, ikke et strengt AA-krav).
- **Hvorfor det betyr noe:** Teksten sier at det er regnet en prognose, og den forklarende setningen rett under sier «Da lager Marin ingen prognose». Det er forvirrende, særlig i et skjermbilde som deles.
- **Forslag til tiltak:** Bruk «Analyseuke: uke 42, 2026» i grå status, eller i alle statuser.

#### L5 – Tidsgrenser og bevegelse bør skrives eksplisitt

- **Sted:** EXPERIENCE.md › State Patterns (Fane lukket / ny fil, Laster). Interaction Primitives.
- **WCAG:** 2.2.1 Justerbar hastighet, 2.3.3 (AAA, til orientering).
- **Hvorfor det betyr noe:** FR26 lar opplastede data forsvinne når appen startes på nytt. Hvis arkitekturen holder data i en serverøkt med utløpstid, blir det en tidsgrense uten varsel.
- **Forslag til tiltak:**
  - Skriv «Ingen tidsgrense eller økt-utløp i v1. Hvis opplastede data er borte, vises en melding med lenke til «Last opp egne tall».»
  - «Ingen animasjon» står allerede for lastetilstanden. Gjør det til en generell regel: ingen animasjon i graf og overganger, ingen myk rulling ved fokusflytting, og `prefers-reduced-motion` respekteres hvis noe skulle innføres.

#### L6 – Analyseukevelgeren har ca. 95 valg

- **Sted:** EXPERIENCE.md › Component Patterns › Analyseukevelger.
- **WCAG:** 2.1.1 er oppfylt med standard `<select>`. Gjelder brukbarhet.
- **Hvorfor det betyr noe:** Alle valg starter med «uke». Hurtigsøk ved å skrive tegn virker dårlig, og listen er lang å navigere med piltaster og skjermleser.
- **Forslag til tiltak:** Bruk `<optgroup label="2026">` og `<optgroup label="2025">`, og vurder verdier som «42 – uke 42, 2026», slik at hurtigsøk på ukenummer virker. Etiketten «Analyseuke» skal være koblet med `<label for>`, som i skissen.

#### L7 – Skissene avviker fra spinen på flere tilgjengelighetspunkter

- **Sted:** `.working/directions-1.html` (retning A), `key-opplasting.html`.
- **WCAG:** 1.4.11, 1.3.1, 3.3.2.
- **Hvorfor det betyr noe:** Spinen gjelder ved konflikt, men skisser blir ofte kopiert. Disse avvikene bør ikke følge med inn i implementasjonen:
  - Nedtrekkslista og søkefeltet i retning A har kant #E3E6EA (1,25:1). Spinen sier `border-strong`.
  - Grafetikettene på mobil er 11px, og «ikke telt» er 11,96px.
  - Metalinjen i statusboksen har `opacity:.95`.
  - «Fil» er en `<span>` uten kobling til feltet.
  - Feilteksten «lusetallet «0.3» er ikke et tall» i key-opplasting avviker fra spinens mer hjelpsomme melding om desimaltegn (3.3.3).
- **Forslag til tiltak:** Merk skissene med en kort liste over kjente avvik, eller rett dem før de gis videre til arkitektur.

---

## 3. Det som holder (sjekket og godkjent)

- **Tekstkontrast:** alle tekstpar i DESIGN.md er ≥ 4,5:1, og tallene i dokumentet stemmer.
- **NFR4:** statusboksen er selvforklarende i et skjermbilde. Anlegg, sted, analyseuke, symbol, R4-tekst og forklaring står i boksen, og ingenting i den er avhengig av farge alene. Ordene «Varsel», «Brudd nå», «Følg med» og «Ingen kryssing» skiller alvorlighetsgradene i tekst.
- **Gul flate:** har påbudt mørk kant (5,07:1 mot hvit), og gul brukes aldri som tekst.
- **Feilmeldingen** bruker ikke statusrødt, har ramme og overskrift, og sier hva som er galt og i hvilken rad (3.3.1, 3.3.3).
- **Språk:** `lang="nb"` er spesifisert. Symboler er `aria-hidden`, og teksten bærer meningen.
- **Fokusring:** 2px aksent med 2px avstand, 10,04:1 mot hvit. Ingen klebrige elementer som kan skjule fokus (2.4.11).
- **Analyseuka** endres uten kontekstskifte (3.2.2), og fokus og rulleposisjon beholdes.
- **Ingen funksjon finnes bare ved hover** (1.4.13 er ikke aktuell), og det er ingen animasjon.
- **Lenker er understreket** (1.4.1).
