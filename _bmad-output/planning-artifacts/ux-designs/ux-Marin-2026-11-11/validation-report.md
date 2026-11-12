# Valideringsrapport – Marin

- **DESIGN.md:** `_bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/DESIGN.md`
- **EXPERIENCE.md:** `_bmad-output/planning-artifacts/ux-designs/ux-Marin-2026-11-11/EXPERIENCE.md`
- **Kjørt:** 2026-11-12T08:58:49+01:00

## Samlet vurdering

Spineparet er solid nok til å bygge på. Alle fargetokener har hex-verdi, alle `{token}`-henvisninger går opp, alle kontrastpåstander stemmer når de regnes ut, R4-tekstene er gjengitt ordrett, og J1–J3 har hver sin Key Flow med navngitt person, klimaks og feilvei. Rubrikkgjennomgangen fant ingen kritiske eller høye funn. Det svakeste området er visuelle referanser: to nøkkelskisser (`key-forside.html`, `key-opplasting.html`) er ikke lenket fra spinene, DESIGN.md kaller dem fortsatt «ikke skissert», og skissene har små avvik som må rettes før de flyttes til `mockups/`. Ellers mangler det mest tilstandsregler rundt opplastede data, mål for trykkflater og visuell spesifikasjon for noen meldinger.

Tilgjengelighetsgjennomgangen (WCAG 2.2 AA) skjerper bildet: den fant fem høye funn som bør rettes før arkitektur og epics. Viktigst er at DESIGN.md sier at rød og grønn skilles på lyshet, mens de faktisk står i 1,06:1 mot hverandre – nettopp der UJ-1 legger klimakset. I tillegg er tekstalternativet for grafen ufullstendig (prognoseverdier og vårgrensen mangler), grafetiketter krymper under 13px-gulvet, skjemafeil i opplastingen er bare delvis spesifisert, og søkefeltet i toppfeltet mangler etikett og søkeknapp. Flere middels funn overlapper rubrikken (treflistens tastaturmønster, trykkflater, fokus ved sidebytte, skisseavvik), så de samme få rettingene løser begge sett.

## Kategorivurderinger

- Flytdekning (Flow coverage) – sterk
- Token-kompletthet (Token completeness) – tilstrekkelig
- Komponentdekning (Component coverage) – tilstrekkelig
- Tilstandsdekning (State coverage) – tilstrekkelig
- Visuelle referanser (Visual reference coverage) – tynn
- Oppblåsing og overspesifisering (Bloat & overspecification) – tilstrekkelig
- Arvedisiplin (Inheritance discipline) – tilstrekkelig
- Formtilpasning (Shape fit) – sterk

## Funn etter alvorlighet

### Kritisk (0)

Ingen.

### Høy (5)

**[Tilgjengelighet]** – H1 Rød og grønn har samme lyshet; påstanden i DESIGN.md er feil (§ DESIGN.md Colors; EXPERIENCE.md Key Flows UJ-1 steg 5; Responsive & Platform › Sollys)
#B3261E og #1B6E4F står i 1,06:1 (L* 39,7 mot 41,1) og skilles bare på kulør. Ved deuteranopi 1,17:1; i sollys, gråtoner og på 12–13px symboler praktisk talt like. UJ-1 kaller fargen klimakset.
Fix: Rett påstanden og før inn 1,06:1 som kjent begrensning. Velg (a) lyshetsskille (f.eks. rød #8F1A14 / grønn #4CB07E med mørk tekst) eller (b) symbol i hvit sirkel ≥ 32px desktop / 28px mobil. Legg gråtone- og deuteranopi-sjekk i NFR10-sjekklista.

**[Tilgjengelighet]** – H2 Tekstalternativet for grafen er ufullstendig (§ EXPERIENCE.md Accessibility Floor › Skjermleser pkt. 3; Component Patterns › Graf; DESIGN.md Components › Graf)
Mangler prognoseverdier, grensetrappen («grense 0,5» også når 0,2 gjelder), målte uker utenfor tabellen, hull og mal for ukjent område. Oppsummeringen er bare en usynlig `aria-label`.
Fix: Utvid malen med siste måling, trendverdier og grense per periode; egne maler for ukjent område og brudd nå; synlig `<figure>`/`<figcaption>`; vurder «Vis tallene i grafen»-tabell; `role="img"` på SVG.

**[Tilgjengelighet]** – H3 SVG-teksten skalerer med viewBox og går under 13px-gulvet (§ DESIGN.md Typography `chart-label`, Layout & Spacing; EXPERIENCE.md Accessibility Floor › Tekststørrelse)
13 enheter ≈ 10px ved 600px viewport og ≈ 11,3px ved 320px; tekstzoom virker ikke på SVG-tekst.
Fix: «Grafetiketter er minst 13 CSS-px ved alle bredder og følger tekstzoom.» HTML-etiketter over SVG eller viewBox fra faktisk bredde. Test 320px, 600px og 200 % tekstzoom.

**[Tilgjengelighet]** – H4 Opplastingsskjemaet: feil, påkrevde valg og fokus delvis spesifisert (§ EXPERIENCE.md Component Patterns › Opplastingsskjema, Feilmelding; State Patterns; DESIGN.md Components)
Uavklart: «Vis prognose» uten valg, `aria-invalid`/`aria-describedby`, fokus etter rettet fil, «Leser fila …» som status, lange feillister, dobbel opplesing, områdevalg ved ny fil.
Fix: Ny underseksjon «Skjemafeil»: knappen alltid aktiv med feil ved gruppen; ekte `<input type="file">` med `<label>`; fokus *eller* `role="alert"`; vis 20 første feil + oppsummering; statusbeskjed og fokus etter vellykket innlesing; live-region fra start; behold områdevalg.

**[Tilgjengelighet]** – H5 Søkefeltet i toppfeltet har ingen etikett og ingen søkeknapp (§ DESIGN.md Components › Toppfelt, Søkefelt; EXPERIENCE.md Component Patterns › Toppfelt, Søkefelt)
Bare plassholdertekst på desktop, og lovet «Søk»-knapp finnes ikke.
Fix: `<label>` «Søk anlegg» (synlig eller skjult), «Søk»-knapp ≥ 24 × 24px, `<form role="search">`, og før det inn i DESIGN.md › Toppfelt og mikroteksttabellen.

### Middels (17)

**[Token-kompletthet]** – Ingen tokener for størrelsen på interaktive elementer (§ DESIGN.md Components «Analyseukevelger», «Knapp», «Søkefelt»; EXPERIENCE.md Interaction Primitives)
Analyseukevelgeren blir ca. 33px mot krav 44 × 44 px på mobil; knapp, felt, radio og filvelger mangler padding/typografi-tokener.
Fix: `spacing.control-min-height` (44px mobil), padding-tokener og `typography.button`, brukt i `components.button-*`, `search-field`, `analysis-week-select`.

**[Token-kompletthet]** – Ingen visuell spesifikasjon for deaktivert, hover og trykk (§ DESIGN.md Components «Knapp», «Trefliste»; EXPERIENCE.md State Patterns «Laster / leser fil»)
Knappen skal være deaktivert under «Leser fila …», men har ingen verdier.
Fix: `disabled`-verdier for `button-primary`/`button-secondary`; avgjør og tokeniser hover.

**[Komponentdekning]** – Uklart hvordan treflisten betjenes med tastatur (§ DESIGN.md Colors «Aksent-tone», Components «Trefliste»; EXPERIENCE.md Component Patterns «Trefliste»)
Lenker med Tab eller listbox med `aria-activedescendant` er uavklart.
Fix: Velg én modell og beskriv tastene.

**[Komponentdekning]** – Tekstelementer uten visuell spesifikasjon (§ EXPERIENCE.md State Patterns, Voice and Tone)
Ingen treff, «Regner ut prognose …», «Leser fila …», lagringsnotis, hjelpetekst for område, «Område: …» og stedslinja.
Fix: Felles `inline-message` / `help-text`-komponent med `{typography.meta}` og `{colors.ink-secondary}`.

**[Tilstandsdekning]** – Statusboks fra opplastede data ser lik ut som BarentsWatch-data (§ EXPERIENCE.md State Patterns «Opplastede data vist»; DESIGN.md Components «Statusboks»)
Skjermdumper kan ikke skilles.
Fix: Fast linje «Egne tall fra fil: <filnavn>» i boksen og på siden, med utseende i DESIGN.md.

**[Tilstandsdekning]** – Uavklart hva som skjer med opplastede data ved navigering bort (§ EXPERIENCE.md State Patterns «Fane lukket / ny fil»; Key Flows UJ-3)
Fix: Skriv en regel for logo, «Bytt anlegg», søk og tilbake-knapp, med henvisning til FR26.

**[Tilstandsdekning]** – Ingen terskel for «stabil» trend; retningsord hardkodet (§ EXPERIENCE.md Voice and Tone)
Fix: Terskel for b (f.eks. |b| < 0,01 per uke) og retningsordet som variabel i malene.

**[Visuelle referanser]** – `key-forside.html` og `key-opplasting.html` er ikke lenket, og DESIGN.md kaller dem «ikke skissert» (§ DESIGN.md Components «Fargeforklaring», «Opplastingsskjema»; EXPERIENCE.md IA)
Fix: Fjern «ikke skissert» og lenk skissene inn ved relevante komponenter og flater med en linje om hva de viser.

**[Visuelle referanser]** – Skissene avviker fra spinene (§ .working/key-forside.html l. 120/139/170/194; .working/key-opplasting.html)
Ekstra opplastingslenke på forsiden, feil desimalfeiltekst, forlatt «Område: sør (Vestland)»-mønster.
Fix: Rett før forfremming, eller før dem opp som kjente avvik.

**[Arvedisiplin]** – Nye krav uten ID («Husk siste anlegg» m.fl.) (§ EXPERIENCE.md «Avvik og tillegg til PRD», IA «Ruting ved åpning»)
Fix: Midlertidige ID-er UX-A1–UX-A5 og PRD-oppdatering via `bmad-prd` eller `bmad-correct-course` før epics.

**[Tilgjengelighet]** – M1 `aria-live` på hele statusboksen; lastetilstand ligner grå status (§ EXPERIENCE.md Accessibility Floor; State Patterns › Laster; Analyseukevelger)
Fix: Egen skjult `role="status"` med én kort setning, ca. 300 ms debounce, egen visuell form for lastetilstand.

**[Tilgjengelighet]** – M2 Reflow spesifisert for 200 %, kravet er 320 CSS-px (400 %) (§ EXPERIENCE.md Accessibility Floor, Responsive & Platform; DESIGN.md Layout & Spacing)
Fix: Skriv om kravet, la toppfeltet bryte, `min-width` på merker, 320px og tekstavstand i sjekklista.

**[Tilgjengelighet]** – M3 Treflisten: «aktiv rad» og «piltaster» er et udefinert mønster (§ DESIGN.md Colors; EXPERIENCE.md Trefliste, Søkefelt)
Aksent-tonen 1,18:1 holder ikke som eneste fokusindikator; ingen treffantall-beskjed.
Fix: Vanlige lenker med Tab og `focus-ring`; stryk piltaster; statusbeskjed «N anlegg funnet …»; fokus blir i søkefeltet.

**[Tilgjengelighet]** – M4 Gul er ikke gul utenfor statusboksen; rød og gul smelter sammen ved deuteranopi (§ DESIGN.md Colors, Statusmerke, Graf; EXPERIENCE.md Fargeforklaring)
Fix: Liten fylt prikk i `*-fill` i merket, ulik markørform per status, statusord i grafetiketten.

**[Tilgjengelighet]** – M5 Sidetitler, fokus ved sidebytte og autofokus ikke spesifisert (§ EXPERIENCE.md IA, Interaction Primitives, Accessibility Floor)
Fix: `<title>` per flate, fokus til `<h1>` ved navigering, autofokus bare fra «Søk / bytt».

**[Tilgjengelighet]** – M6 Målstørrelse: 44px bare mobil, og skissen holder ikke regelen (§ EXPERIENCE.md Interaction Primitives; DESIGN.md Components)
Fix: Alle mål ≥ 24 × 24 CSS-px overalt og 44 × 44 på mobil; klikkbar etikett over hele raden for radioknapper.

**[Tilgjengelighet]** – M7 Sollys: flere elementer ligger rett på 3:1, noen tekster små (§ DESIGN.md Colors, Typography, Graf; EXPERIENCE.md Responsive & Platform › Sollys)
Fix: Tallfest «redusert styrke» ≥ 4,5:1, tykkere linjer, `pill-xs` 13px og `meta-mobile` 15px, utvid «Sollys» til hele siden.

### Lav (20)

**[Token-kompletthet]** – Grafens mål er ikke tokenisert (§ DESIGN.md Components «Graf»)
Fix: `trend-history-opacity`, `point-radius`, `line-width`, `aspect-ratio` i `components.trend-graph`.

**[Token-kompletthet]** – Kortformede token-henvisninger for statusboks (§ EXPERIENCE.md Component Patterns «Statusboks»)
Fix: Skriv alle fire `{components.status-box-*}` ut.

**[Komponentdekning]** – «Lenke» og «Fokusmarkering» mangler i Component Patterns (§ DESIGN.md Components; EXPERIENCE.md Component Patterns)
Fix: Kort rad for Lenke, eller si at begge kun er visuelle.

**[Tilstandsdekning]** – Manglende opplastingstilstander (§ EXPERIENCE.md State Patterns «Feil i fil», «Område må velges»)
Fix: Legg til startside, tom fil, Excel-kolonnefeil og «Vis prognose» uten område.

**[Tilstandsdekning]** – Appnivå-feil, URL-struktur og tilbake-knapp ikke beskrevet (§ EXPERIENCE.md Information Architecture)
Fix: Overlat eksplisitt til arkitekturen, eller angi egen URL for detaljsiden.

**[Tilstandsdekning]** – Fokus etter sideskift ikke angitt (§ EXPERIENCE.md Accessibility Floor)
Fix: «Fokus settes på sidetittelen (H1) etter navigasjon.»

**[Visuelle referanser]** – Henvisningene ligger bare øverst (§ DESIGN.md Brand & Style; EXPERIENCE.md Foundation)
Fix: Lenk inn ved hver komponent og tilstand når filene flyttes til `mockups/`.

**[Oppblåsing]** – Samme `fontFamily`-stabel 20 ganger (§ DESIGN.md frontmatter `typography`)
Fix: Nevn den én gang eller bruk et eget token.

**[Oppblåsing]** – Tabellene gjentar pikselverdier fra frontmatter (§ DESIGN.md Typography, Layout & Spacing)
Fix: Behold bare tokennavn og bruk i tabellene.

**[Oppblåsing]** – Opphavsmerker i mikroteksttabellene (§ EXPERIENCE.md Voice and Tone)
Fix: Fjern «(fra skissen)» o.l.

**[Arvedisiplin]** – «UJ-1/2/3» i stedet for PRD-ens J1–J3 (§ EXPERIENCE.md Key Flows)
Fix: Bruk J1–J3 med PRD-navnene.

**[Arvedisiplin]** – Begrepslista avviker fra PRD-ens ordliste (§ EXPERIENCE.md Voice and Tone «Begreper»)
Fix: Avklar «lokalitet» og «grensen».

**[Formtilpasning]** – Inspiration & Anti-patterns er utelatt (§ EXPERIENCE.md)
Fix: Kort seksjon med forkastede retninger og grunn, eller én linje om utelatelsen.

**[Tilgjengelighet]** – L1 Statusmerkets kant (1,25:1) er bare forsvarlig fordi merket ikke er interaktivt (§ Statusmerke)
Fix: Interaktive merker skal ha kant ≥ 3:1.

**[Tilgjengelighet]** – L2 Ukestabellen: semantikk og «–» (§ Ukestabell)
Fix: `<caption>`/`aria-labelledby`, `<th scope="col">`, skjult «ikke telt», symbol i `aria-hidden`.

**[Tilgjengelighet]** – L3 Landemerker, overskrifter og logo (§ Toppfelt)
Fix: `<h1>` på forsiden, logo som lenke, landemerker og hopplenke.

**[Tilgjengelighet]** – L4 «Prognose regnet fra …» i grå status (§ EXPERIENCE.md Statusboks, Annen mikrotekst)
Fix: «Analyseuke: uke 42, 2026».

**[Tilgjengelighet]** – L5 Tidsgrenser og bevegelse bør skrives eksplisitt (§ EXPERIENCE.md State Patterns, Interaction Primitives)
Fix: «Ingen tidsgrense i v1», melding hvis data er borte, generell regel om ingen animasjon.

**[Tilgjengelighet]** – L6 Analyseukevelgeren har ca. 95 valg (§ EXPERIENCE.md Analyseukevelger)
Fix: `<optgroup>` per år og verdier som «42 – uke 42, 2026».

**[Tilgjengelighet]** – L7 Skissene avviker fra spinen på tilgjengelighetspunkter (§ .working/directions-1.html, key-opplasting.html)
Fix: Merk kjente avvik eller rett skissene før arkitektur.

## Mekaniske merknader

- Alle token-henvisninger går opp; `spacing.topbar-gap`, `statusbox-line-gap`, `pill-y`, `pill-x` er ubrukt.
- Alle kontrastpåstander i DESIGN.md stemmer; gul kant mot hvit (5,07:1) bør føres inn; rød mot grønn innbyrdes er 1,06:1.
- R4-tekstene er ordrette; «(uke Y)» bør være eget element for testene T5–T12.
- Komponentnavn er konsistente i begge filer.
- `updated: 2026-11-11` i begge filer bør oppdateres ved ferdigstilling.
- Mermaid brukes ikke.

## Gjennomgangsfiler

- `review-rubric.md`
- `review-accessibility.md`
