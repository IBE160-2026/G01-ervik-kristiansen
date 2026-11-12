# Spine Pair Review – Marin

Gjennomgått: `DESIGN.md` og `EXPERIENCE.md` (begge `status: draft`, 2026-11-11), med `.memlog.md`, `.working/*.html`, PRD (`prd-Marin-2026-11-02/prd.md`) og brief (`brief-Marin-2026-09-17/brief.md`) som kontekst. Kalibrering: kursleveranse IBE160, vurderes av sensor og brukes videre til arkitektur og epics/stories. Ingen spinefiler er endret.

## Overall verdict

Spineparet er solid nok til å bygge på. Alle fargetokener har hex-verdi, alle `{token}`-henvisninger går opp, alle kontrastpåstander stemmer når de regnes ut, R4-tekstene er gjengitt ordrett, og J1–J3 har hver sin Key Flow med navngitt person, klimaks og feilvei. Ingen funn er kritiske eller høye. Det svakeste området er visuelle referanser: to nøkkelskisser (`key-forside.html`, `key-opplasting.html`) er ikke lenket fra spinene, DESIGN.md kaller dem fortsatt «ikke skissert», og skissene har små avvik fra spinene som må rettes før de flyttes til `mockups/`. Ellers mangler det mest tilstandsregler rundt opplastede data, mål for trykkflater og noen meldinger uten visuell spesifikasjon. Dette er ting en utvikler ellers vil måtte gjette på.

## 1. Flow coverage – strong

Kontrollert: brukerreisene J1, J2 og J3 i PRD kap. 4 mot EXPERIENCE.md Key Flows. Alle tre har en navngitt person (Kari), nummererte steg, et merket klimaks og en feilvei. J1 dekker både åpning med husket anlegg og første besøk med søk, og det samsvarer med PRD J1 steg 1–2. J2 dekker «velg senere uke for å se hva som skjedde» (PRD J2 steg 3). J3 dekker CSV med områdevalg, Excel med flere anlegg og utledet område, feil i fil og FR26.

### Findings
- Ingen funn. (Navnebruken i overskriftene er tatt med under kategori 7.)

## 2. Token completeness – adequate

Kontrollert: 24 fargetokener, 20 typografitokener, 3 radius-tokener, 28 spacing-tokener og 19 komponentobjekter i frontmatter, og alle `{path.to.token}` i prosaen i begge filer. Alle henvisninger går opp, og ingen fargetokener mangler hex. Mørk modus er uttrykkelig utenfor v1, så det trengs ingen par for lys og mørk. Kontrastpåstandene er regnet ut på nytt og stemmer (se *Mechanical notes*).

### Findings
- **medium** Det finnes ingen tokener for størrelsen på interaktive elementer. `analysis-week-select` har innvendig luft `{spacing.control-y}` 6px. Med `meta` 16px gir det en kontroll på omtrent 33px, mens EXPERIENCE.md krever trykkflater på minst 44 × 44 px på mobil. Knapp, søkefelt, radioknapper og filvelger har ingen tokener for padding eller typografi. Skissene bruker 8px/18px og `min-height: 44px` på mobil, men det står ikke i spinen (DESIGN.md Components «Analyseukevelger», «Knapp», «Søkefelt»; EXPERIENCE.md Interaction Primitives). *Fix:* Legg inn `spacing.control-min-height` (44px på mobil), padding-tokener for knapp og felt, og en `typography.button`. Bruk dem i `components.button-*`, `search-field` og `analysis-week-select`.
- **medium** Det mangler visuell spesifikasjon for andre tilstander enn standardtilstanden. EXPERIENCE.md sier at knappen er deaktivert under «Leser fila …», men DESIGN.md har ingen verdier for deaktivert knapp. Hover- og trykktilstand for knapp, lenke og rad i treflisten er heller ikke beskrevet (DESIGN.md Components «Knapp», «Trefliste»; EXPERIENCE.md State Patterns «Laster / leser fil»). *Fix:* Legg til `disabled`-verdier for `button-primary` og `button-secondary` (f.eks. `{colors.border-strong}` som flate eller kant og tekstfarge med kontrast ≥ 3:1). Avgjør om hover skal brukes. Hvis ja, beskriv det i tokens.
- **low** Mål for grafen er ikke tokenisert: høyde eller sideforhold, linjetykkelser (unntatt grenselinja på 2px), punktstørrelse og hva «redusert styrke» på historisk trend betyr som opasitet (DESIGN.md Components «Graf»). *Fix:* Legg verdiene i `components.trend-graph`, f.eks. `trend-history-opacity`, `point-radius`, `line-width` og `aspect-ratio`.
- **low** EXPERIENCE.md bruker kortformene `` `-yellow` `` / `` `-green` `` / `` `-grey` `` etter `{components.status-box-red}`. Det er ikke gyldige henvisninger (EXPERIENCE.md Component Patterns «Statusboks»). *Fix:* Skriv alle fire ut i sin helhet.

## 3. Component coverage – adequate

Kontrollert: 15 komponenter i DESIGN.md (toppfelt, statusboks, statusmerke, analyseukevelger, søkefelt, trefliste, graf, ukestabell, usikkerhetstekst, fargeforklaring, knapp, opplastingsskjema, feilmelding, lenke, fokusmarkering) mot 13 rader i EXPERIENCE.md Component Patterns, og elementer som bare nevnes i State Patterns og Voice and Tone. Navnene er like i begge filer. Reglene for oppførsel er konkrete og viser til FR-ID-er.

### Findings
- **medium** Det er uklart hvordan treflisten skal betjenes med tastatur. DESIGN.md gir `active-background: {colors.accent-tint}` for «aktiv rad i treflisten ved tastaturnavigering», og det tyder på en listbox med piltaster. EXPERIENCE.md sier bare at «hele raden er klikkbar», og Accessibility Floor nevner piltaster generelt (DESIGN.md Colors «Aksent-tone» og Components «Trefliste»; EXPERIENCE.md Component Patterns «Trefliste»). En utvikler kan ikke avgjøre om radene skal være lenker som nås med Tab eller en listbox med `aria-activedescendant`. *Fix:* Velg én modell. Er radene lenker, er aksent-tonen fokus- og hover-markering. Er det en listbox, beskriv rekkefølgen for piltaster, Enter og Escape.
- **medium** Flere tekstelementer har oppførsel og tekst, men ingen visuell spesifikasjon: meldingen ved ingen treff (FR6), «Regner ut prognose …» i grå ramme, «Leser fila …», lagringsnotisen (FR26), hjelpeteksten for områdevalg og «Område: …»-linja, og stedslinja under tittelen på detaljsiden (EXPERIENCE.md State Patterns og Voice and Tone; ingen tilsvarende i DESIGN.md Components). *Fix:* Lag en felles komponent i DESIGN.md, f.eks. `inline-message` / `help-text`, med typografi og farge (`{typography.meta}`, `{colors.ink-secondary}`), og vis til den fra hver tilstand.
- **low** «Lenke» og «Fokusmarkering» har rader i DESIGN.md, men ikke i Component Patterns. Fokus er dekket i State Patterns og Accessibility Floor, men lenke er ikke dekket noe sted (f.eks. om lenker åpnes i samme fane, eller hvordan «Søk / bytt» oppfører seg som lenke eller knapp). *Fix:* Legg til en kort rad for Lenke, eller si i Component Patterns at begge kun er visuelle.

## 4. State coverage – adequate

Kontrollert: hver flate i IA. **Forside**: første besøk, trefliste, ingen treff, tomt søk og husket anlegg som er borte. **Detaljside**: sju statustilstander i rekkefølgen fra R4, laster, åpning med husket anlegg, opplastede data, tastaturfokus. **Opplasting**: leser fil, sju feiltyper, Excel med flere anlegg, utledet område, område må velges. Rekkefølgen og den ordrette R4-teksten stemmer med briefen.

### Findings
- **medium** Statusboksen fra opplastede data ser lik ut som statusboksen fra BarentsWatch-data. Boksen skal kunne skjermdumpes og sendes til folk på merden (UJ-1 steg 6–7), men ingenting i den viser at tallene er brukerens egne og ikke det offentlige utdraget (EXPERIENCE.md State Patterns «Opplastede data vist»; DESIGN.md Components «Statusboks»). *Fix:* Legg en fast linje i statusboksen og på siden for opplastede data, f.eks. «Egne tall fra fil: lusetall_langholmen.csv», og beskriv utseendet i DESIGN.md.
- **medium** Det er ikke bestemt hva som skjer med opplastede data når brukeren navigerer bort i samme fane, f.eks. med logoen, «Bytt anlegg» eller søk. FR26 sier at dataene lever til fanen lukkes eller en ny fil lastes opp, men det står ikke om Kari kan komme tilbake til dem, om de forkastes eller om nettleserens tilbakeknapp viser dem igjen (EXPERIENCE.md State Patterns «Fane lukket / ny fil»; Key Flows UJ-3). *Fix:* Legg inn en regel, f.eks. «Opplastede data forkastes når brukeren forlater detaljsiden for dem; tilbake-knappen går til opplastingssiden», eller den motsatte, og vis til FR26.
- **medium** Regelen for retningsord i den forklarende setningen («har steget» / «har falt» / «har ligget stabilt» følger fortegnet på trendlinja) har ingen terskel for når trenden regnes som stabil. Malene for rød og gul har dessuten «har steget» skrevet inn fast, og R2 sier at en flat eller fallende trend kan gi kryssing om våren (EXPERIENCE.md Voice and Tone, merknaden under tabellen for statustekst). Det kan ikke lages et kontrollpunkt for dette i README-sjekklista (NFR10). *Fix:* Angi en terskel for stigningen b (f.eks. |b| < 0,01 per uke = «har ligget stabilt»), og skriv malene med retningsordet som variabel.
- **low** Noen tilstander ved opplasting mangler: startsiden før noen fil er valgt, tom fil eller fil med bare overskriftsrad, feiltekster for Excel-fil som mangler kolonner (dagens tekst nevner bare CSV-kolonnene), og hva som skjer med «Vis prognose» før område er valgt (deaktivert eller feilmelding) (EXPERIENCE.md State Patterns «Feil i fil», «Område må velges»). *Fix:* Legg til radene i tabellen Andre tilstander.
- **low** Det er ikke beskrevet hva som skjer på appnivå hvis datagrunnlaget ikke kan lastes, og heller ikke URL-struktur, dyplenker eller tilbake-knapp. Skissene viser `?sok=lang` og `/last-opp` (EXPERIENCE.md Information Architecture). *Fix:* Si at arkitekturen avgjør dette, eller angi om detaljsiden skal ha en egen URL. Det avgjør om tilbake-knappen fungerer etter valg av analyseuke.
- **low** Det står ikke hvor fokus havner etter sideskift: fra treflisten til detaljsiden, og fra «Vis prognose» til detaljsiden (EXPERIENCE.md Accessibility Floor). *Fix:* F.eks. «Fokus settes på sidetittelen (H1) etter navigasjon.»

## 5. Visual reference coverage – thin

Kontrollert: `mockups/` og `wireframes/` finnes ikke ennå (forfremming skjer etter gjennomgangen, og det er ikke regnet som funn). `imports/` er tom. `.working/` har fem filer. `color-themes-1.html` og `directions-1.html` er lenket fra DESIGN.md Brand & Style og EXPERIENCE.md Foundation. `key-oversikt-skisse.html` er lenket fra EXPERIENCE.md «Avvik og tillegg til PRD». At spinene gjelder ved konflikt, står én gang i hver fil.

### Findings
- **medium** `key-forside.html` og `key-opplasting.html` er ikke lenket fra noen av spinene. DESIGN.md sier i tillegg at begge flatene er uskissert: «Fargeforklaring … Ikke skissert» og «Opplastingsskjema … ikke skissert» (DESIGN.md Components). EXPERIENCE.md merker samtidig mye tekst «(fra skissen)» som kommer fra nettopp disse filene. *Fix:* Fjern «ikke skissert». Lenk `key-forside.html` fra EXPERIENCE.md IA og forsiden og fra DESIGN.md «Fargeforklaring» og «Trefliste», og `key-opplasting.html` fra «Opplastingsskjema» og «Feilmelding». Skriv hva hver fil viser.
- **medium** Skissene har avvik fra spinene som må rettes før de forfremmes, ellers bygger noen etter feil kilde. (a) `key-forside.html` har en egen lenke «Last opp egne tall» nede på siden (`<p class="upl">`, linje 120/139/170/194), men spinen sier at lenken ikke gjentas på siden. (b) `key-opplasting.html` viser «Rad 7: lusetallet «0.3» er ikke et tall.», men EXPERIENCE.md har en egen melding for feil desimaltegn. (c) Bildeteksten i `key-opplasting.html` viser til «Område: sør (Vestland)»-mønsteret, som er forlatt. *Fix:* Rett de tre stedene i skissene før forfremming, eller skriv i spinen at de er kjente avvik.
- **low** Henvisningene ligger bare øverst (Brand & Style og Foundation). De er ikke lenket der de er relevante, f.eks. retning A ved DESIGN.md «Statusboks», «Graf» og «Ukestabell» og ved EXPERIENCE.md State Patterns for detaljsiden. *Fix:* Lenk inn ved hver aktuell komponent eller tilstand når filene flyttes til `mockups/`.

## 6. Bloat & overspecification – adequate

Kontrollert: pikselverdier mot tokener, om innhold fra kildene gjentas, tabeller mot prosa, og om noen seksjoner ikke har en leser. Teksten er stort sett stram. PRD-krav vises til med ID og gjentas ikke. DESIGN.md Brand & Style har redaksjonell stemme, slik den skal.

### Findings
- **low** Den samme `fontFamily`-stabelen står 20 ganger i `typography` (DESIGN.md frontmatter). *Fix:* Nevn stabelen én gang i Typography-prosaen, eller ha et eget token som de andre viser til. Spesifikasjonen tillater begge.
- **low** Tabellene i Typography og Layout & Spacing gjentar pikselverdiene fra frontmatter ved siden av tokennavnene. Da kan verdiene komme i utakt (DESIGN.md Typography og Layout & Spacing). *Fix:* Behold tokennavn og bruk i tabellene, og la verdiene stå bare i frontmatter.
- **low** Opphavsmerkene «(fra skissen)», «(fra memlog)» og «(fra retning A-skissen)» i mikroteksttabellene er prosesshistorikk og ikke beslutninger (EXPERIENCE.md Voice and Tone). *Fix:* Fjern dem. Opphavet står allerede i memloggen.

## 7. Inheritance discipline – adequate

Kontrollert: `sources` i begge filer peker til `../../prds/prd-Marin-2026-11-02/prd.md` og `../../briefs/brief-Marin-2026-09-17/brief.md`, og begge går opp. Navnene på J1–J3 er ordrette fra PRD. R4-tekstene er ordrette fra briefen, også «?» for ukjent område. Rekkefølgen for status er identisk med R4. Komponentnavnene er like i begge filer. Token-henvisningene i EXPERIENCE.md finnes i DESIGN.md. Avvik fra PRD er samlet i en egen tabell med konsekvenser, og det er godt arbeid.

### Findings
- **medium** «Husk siste anlegg» er et nytt krav som styrer rutingen ved åpning, J1 og første besøk. Det finnes ikke i PRD-en og har ingen ID (EXPERIENCE.md «Avvik og tillegg til PRD», IA «Ruting ved åpning»). Epics og stories skal vise til FR-ID-er (PRD kap. 13 steg 4), så kravet blir uten sporbarhet til PRD-en er oppdatert. Det samme gjelder forklaringen ved første besøk og den forklarende setningen. *Fix:* Gi tilleggene midlertidige ID-er i avvikstabellen (f.eks. UX-A1–UX-A5), som epics kan vise til. Oppdater også PRD-en via `bmad-prd` eller `bmad-correct-course` før epics lages.
- **low** Overskriftene i Key Flows bruker prefikset «UJ-1/UJ-2/UJ-3», som ikke finnes i kildene. PRD bruker J1–J3 (EXPERIENCE.md Key Flows). *Fix:* Bruk «J1 Sjekk status for mitt anlegg – Kari, onsdagssjekken» osv.
- **low** Voice and Tone sier at begrepene «anlegg», «analyseuke», «telling» og «grensen» brukes «som i PRD-ens ordliste». «Grensen» står ikke i ordlista (der står «Uker til grensen»), og synonymet «lokalitet» er ikke nevnt, selv om UI-en bruker «lokalitetsnr.» og «lokalitetsnavn» (EXPERIENCE.md Voice and Tone «Begreper»). *Fix:* Skriv at «lokalitet» bare brukes i «lokalitetsnr.» og «lokalitetsnavn», og at «grensen» betyr lusegrensen etter R1.

## 8. Shape fit – strong

Kontrollert: DESIGN.md har seksjonene i kanonisk rekkefølge (Brand & Style → Colors → Typography → Layout & Spacing → Elevation & Depth → Shapes → Components → Do's and Don'ts), og ingen mangler. EXPERIENCE.md har alle obligatoriske standardseksjoner. Responsive & Platform er med, og den trengs fordi det er to bredder og et bruddpunkt på 600px. Den egne seksjonen «Avvik og tillegg til PRD» fortjener plassen sin, fordi den er overleveringen til PRD og arkitektur. Frontmatter har både spesifikasjonsfeltene (`name`, `description`, tokener) og prosjektfelt (`title`, `status`, `sources`).

### Findings
- **low** Inspiration & Anti-patterns er utelatt. Memloggen sier at det ikke ble oppgitt eksterne referanser, men `.working/` inneholder forkastede alternativer: tema 1, 2 og 4 i `color-themes-1.html` og retning B og C i `directions-1.html`. Kort grunngitte avslag hjelper sensor og senere endringer (EXPERIENCE.md, seksjonen mangler). *Fix:* Legg til en kort seksjon med de forkastede retningene og grunnen til avslaget (f.eks. «kontrollpanel-oppsett forkastet: for urolig»), eller skriv én linje om hvorfor seksjonen er utelatt.

## Mechanical notes

- **Token-henvisninger:** alle `{colors.*}`, `{typography.*}`, `{spacing.*}`, `{rounded.*}` og `{components.*}` i begge filer finnes i DESIGN.md frontmatter. `spacing.topbar-gap`, `statusbox-line-gap`, `pill-y` og `pill-x` er definert, men brukes ikke i prosa eller komponenter (statusmerket bør vise til `pill-y`/`pill-x`). Det er ufarlig.
- **Kontrast, regnet ut på nytt (WCAG):** ink 18,47:1 · ink-secondary 8,13:1 · border-strong 3,18:1 (så vidt over 3:1, ingen margin) · accent 10,04:1 · rød på fill 6,54:1 · gul tekst på fill 10,26:1 · gul fill mot hvit 1,79:1 · status-yellow-border mot hvit 5,07:1 · grønn 6,19:1 · grå tekst 9,53:1 · ink på accent-tint 15,70:1 · accent på accent-tint 8,54:1. Alle påstander i DESIGN.md stemmer.
- **R4-tekster:** alle seks er ordrette fra briefen R4. Entall (T12) og tillegget «(uke Y)» (FR18) er beskrevet. Merk at tillegget «(uke Y)» bør bygges som et eget element, slik at testene T5–T12 kan sjekke R4-strengen uendret.
- **Navnekonsistens:** de norske komponentnavnene (Toppfelt, Statusboks, Statusmerke, Analyseukevelger, Søkefelt, Trefliste, Graf, Ukestabell, Usikkerhetstekst, Fargeforklaring, Opplastingsskjema, Feilmelding, Knapp) er like i begge filer og knyttet til token-nøkler på engelsk i DESIGN.md. Det er konsekvent.
- **Frontmatter:** begge filer har `status: draft` og `updated: 2026-11-11`, mens memloggen er oppdatert 2026-11-12. Feltet `updated` bør settes ved ferdigstilling.
- **Mermaid:** brukes ikke.
- **Skisser mot spine (spinene gjelder):** i tillegg til avvikene i kategori 5 bruker `directions-1.html` 11px grafetiketter på mobil. DESIGN.md har bevisst 13px som gulv. Avviket er dokumentert og trenger ingen tiltak.
