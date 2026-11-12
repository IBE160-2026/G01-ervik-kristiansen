---
title: "EXPERIENCE: Marin"
status: final
created: 2026-11-11
updated: 2026-11-12
sources:
  - ../../prds/prd-Marin-2026-11-02/prd.md
  - ../../briefs/brief-Marin-2026-09-17/brief.md
---

# Marin – opplevelse

## Foundation

- **Formfaktor:** web, responsiv. PC på kontoret og mobil ute på anlegget er begge førsteklasses.
- **UI-rammeverk:** ikke valgt. Arkitektursteget avgjør (PRD A3). Denne spinen beskriver bare oppførsel.
- **Visuell identitet:** `DESIGN.md`. Token-henvisninger her bruker krøllparentes-syntaks (f.eks. `{colors.accent}`) mot DESIGN.md.
- **Modus:** kun lys modus i v1.
- **Språk:** norsk bokmål (NFR5).
- **Stakes:** kursleveranse som skal vurderes av sensor og brukes som grunnlag for arkitektur og epics. Kravene har ID-er i PRD-en, og denne spinen viser til dem uten å gjenta dem.
- **Visuelle referanser:** nøkkelskissene `mockups/key-detaljside.html` (detaljside: rød status på desktop og mobil, opplastede data, grå status), `mockups/key-forside.html` (forside: første besøk, trefliste, ingen treff), `mockups/key-opplasting.html` (opplasting: skjema, anleggsvalg, feil i fil) og `mockups/key-oversikt-skisse.html` (samlet oversikt, ikke del av v1). Beslutningshistorikk: `.working/color-themes-1.html` (tema 3 «Klar hvit») og `.working/directions-1.html` (retning A «Rolig rapport»). Ved konflikt mellom skisser og spinene gjelder spinene.

## Information Architecture

| Flate | Nås fra | Formål | Krav |
|---|---|---|---|
| **Forside / søk** | Åpning uten husket anlegg; «Bytt anlegg» / «Søk / bytt»; logoen; søk fra toppfeltet | Søke opp og velge anlegg. Ved første besøk også én setning om hva Marin er og en fargeforklaring. Opplasting nås via «Last opp egne tall» i toppfeltet. | FR4, FR5, FR6, NFR4, NFR5; UX-1 og UX-2 (se *Avvik og tillegg til PRD*) |
| **Detaljside** | Valg i treflisten; åpning med husket anlegg; vellykket opplasting | Status for ett anlegg for valgt analyseuke: statusboks, graf, ukestabell, usikkerhetstekst. Skisse: `mockups/key-detaljside.html` | FR7–FR20a, FR25, NFR4, NFR5, NFR8 |
| **Opplasting** | «Last opp egne tall» i toppfeltet, også på forsiden (oppfyller lenkekravet i PRD §8) | Laste opp CSV eller Excel, velge eller se område, velge anlegg, se feil | FR21–FR24, FR26 |

Krav uten egen flate: FR1–FR3 (datagrunnlag), FR27–FR28 (backtest-skript; tallene vises i usikkerhetsteksten, FR19). FR29: backtesten har ingen side. Samlet oversikt over alle anlegg er ute av v1.

**Ruting ved åpning («husk siste anlegg»).**

1. Marin husker sist viste innebygde anlegg per nettleser og enhet, uten innlogging. Teknikk for lagring avgjøres i arkitektur.
2. Finnes et husket anlegg, åpner Marin detaljsiden for det direkte, med «Sist viste anlegg» over tittelen. Analyseuka er standardvalget 2026 uke 42 (FR7). Analyseuka huskes ikke.
3. Finnes ikke noe husket anlegg (første besøk eller tømt nettleser), åpner Marin forsiden med intro og fargeforklaring.
4. Husket anlegg oppdateres hver gang detaljsiden vises for et innebygd anlegg. Opplastede data huskes aldri (FR26, NFR6).
5. Finnes ikke det huskede anlegget lenger i datagrunnlaget, åpnes forsiden som ved første besøk. Forsiden ser lik ut enten den nås ved første besøk eller via «Bytt anlegg»: intro og fargeforklaring vises alltid der. Det gir én tilstand mindre, og forsiden besøkes sjelden når anlegget huskes.

## Voice and Tone

Merkevarestemme og visuell holdning ligger i `DESIGN.md` (Brand & Style). Her er mikrotekst.

Tonen er **forklarende**, ikke bare kort og saklig. Brukeren har god kjennskap til lus og lusegrenser, men ingen datafaglig bakgrunn.

**Faste regler**

- **R4-teksten står uendret.** Statusteksten i statusboksen er nøyaktig teksten i briefens R4, fordi T5–T12 tester den. Den står som overskrift. Under den kommer én forklarende setning.
- **Uker:** ISO-uker, skrevet «uke 42, 2026» (NFR5). Inne i en setning der året er åpenbart: «uke 44». Året tas med når uka ligger i et annet år enn analyseuka (f.eks. «uke 2, 2027»).
- **Tall:** desimalkomma, to desimaler for lusetall (0,41), grensene som 0,5 og 0,2.
- **Sted:** kommune og fylke, «Hitra, Trøndelag». Aldri «sør» eller «nord» som etikett. Unntak: opplastingssiden viser utledet område etter FR23 med fylket først og regelen forklart («Område: Trøndelag – grense som for sør»), og områdevalget for CSV bruker sør/nord med hjelpetekst om hvilke fylker som hører til (FR23a).
- **Begreper:** «anlegg», «analyseuke», «telling», «grensen» som i PRD-ens ordliste.

**Statustekst (R4) og forklarende setning**

| Status | Overskrift (R4, uendret) + uke | Forklarende setning (maler, unntatt der kilde er oppgitt) |
|---|---|---|
| Rød – varsel | «✕ Varsel: grensen nås om X uker» + « (uke Y)» | «Lusetallene har steget de siste ukene. Fortsetter trenden, passerer anlegget grensen på 0,5 i uke 44.» (eksempel fra memlog) |
| Rød – brudd nå | «✕ Brudd nå» | «Siste telling (uke 42) var 0,61. Det er på eller over grensen på 0,5 som gjelder denne uka.» |
| Gul | «! Følg med: grensen kan nås om X uker» + « (uke Y)» | «Lusetallene har steget de siste ukene. Fortsetter trenden, kan anlegget passere grensen på 0,5 i uke 46.» |
| Grønn | «✓ Ingen kryssing ventet innen 6 uker» | «Fortsetter trenden fra de siste ukene, holder anlegget seg under grensen de neste 6 ukene.» |
| Grå – for lite data | «– For lite data» | «Bare 2 av de siste 5 ukene har telling. Marin trenger minst 3 tellinger for å lage en prognose.» |
| Grå – ingen ny telling | «– Ingen ny telling siden uke X» | «Siste telling er fra uke 40, mer enn én uke før analyseuka. Da lager Marin ingen prognose. Grafen og tabellen viser målte tall og grensen.» (fra retning A-skissen) |
| Grå – ukjent område | «? Ukjent område: grensen kan ikke bestemmes» | «Anlegget mangler fylke i datagrunnlaget. Da vet ikke Marin hvilken lusegrense som gjelder, og lager ingen prognose.» |

Entall: «grensen nås om 1 uke» (T12). Retningsordet i første del av setningen («har steget», «har falt», «har ligget stabilt») følger fortegnet på trendlinja. Grensen i setningen er grensen som gjelder i uke Y (0,2 i vårperioden).

**Tekstoppsummering under grafen**

Synlig figurtekst under grafen (se *Accessibility Floor*). Tall med desimalkomma og to desimaler; grensen per uke skrives som trapp når vårgrensen slår inn i vinduet (sør uke 16–21, nord uke 21–26, R1). Eksemplene er for et anlegg i sør.

| Tilstand | Mal (eksempel) |
|---|---|
| Rød varsel / gul (prognose med kryssing) | «Målte lusetall uke 10–14, 2026: 0,08, 0,10, ikke telt, 0,14 og 0,16. Siste telling 0,16 i uke 14. Trenden gir 0,18 i uke 15, 0,20 i uke 16, 0,22 i uke 17, 0,24 i uke 18, 0,26 i uke 19 og 0,28 i uke 20. Grensen er 0,5 til og med uke 15 og 0,2 fra uke 16. Trenden når grensen i uke 16.» |
| Grønn (prognose uten kryssing) | «Målte lusetall uke 37–42, 2026: … Siste telling 0,12 i uke 42. Trenden gir 0,13 i uke 43, … og 0,18 i uke 48. Grensen er 0,5 i alle ukene. Trenden når ikke grensen innen uke 48.» |
| Rød – brudd nå | «Målte lusetall uke 37–42, 2026: … Siste telling 0,61 i uke 42, som er på eller over grensen på 0,5. Ingen trendlinje.» |
| Grå – for lite data | «Målte lusetall uke 38–42, 2026: 0,21, ikke telt, ikke telt, 0,25 og ikke telt. Grensen er 0,5 i alle ukene. Ingen trendlinje: for få tellinger.» |
| Grå – ingen ny telling | «Målte lusetall uke 35–40, 2026: … Siste telling 0,30 i uke 40. Ingen telling i uke 41–42. Grensen er 0,5 i alle ukene. Ingen trendlinje.» |
| Grå – ukjent område | «Målte lusetall uke 37–42, 2026: … Siste telling 0,30 i uke 42. Grensen er ukjent fordi anlegget mangler fylke, så grafen viser ingen grenselinje. Ingen trendlinje.» |

Regelen for grensen: én grense skrives «Grensen er 0,5 i alle ukene»; når den endres i vinduet, skrives hvert trinn med første og siste uke («0,5 til og med uke 15 og 0,2 fra uke 16 til og med uke 21»). Uker uten telling skrives «ikke telt».

**Annen mikrotekst**

| Sted | Tekst |
|---|---|
| Forside, intro | «Marin viser om lusetallene på anlegget ditt er på vei mot lusegrensen, og omtrent når grensen kan nås.» |
| Forside, overskrift over fargeforklaringen | «Statusfargene» (fra skissen) |
| Fargeforklaring, merkelapper | «✕ Rød», «! Gul», «✓ Grønn», «– Grå» (symbolet i statusfarge, fra skissen) |
| Fargeforklaring, linjer | «Brudd nå, eller grensen nås om 1–3 uker.» / «Grensen kan nås om 4–6 uker.» / «Ingen kryssing ventet innen 6 uker.» / «Ingen prognose: for lite data, ingen ny telling eller ukjent område.» (fra skissen) |
| Forside, overskrift over søket | «Finn anlegget ditt» (fra skissen) |
| Søkefelt, etikett | «Søk anlegg» (fra skissen). Synlig på forsiden; visuelt skjult i toppfeltet på desktop |
| Søkefelt, plassholder | Desktop: «Søk anlegg – navn eller lokalitetsnr.» (fra skissen). Mobil: «Søk navn eller nr.» |
| Søkeknapp (forside og toppfelt på desktop) | «Søk» |
| Opplasting, overskrift (H1) | «Last opp egne tall» (fra skissen) |
| Opplasting, feltetikett | «Fil» (fra skissen) |
| Opplasting, hjelpetekst for fil | «CSV med kolonnene år, uke og voksne_hunnlus, eller Excel-uttrekk fra BarentsWatch.» (fra skissen) |
| Opplasting, filknapp | «Velg fil» (fra skissen) |
| Opplasting, anleggsvalg (Excel, FR22) | Overskrift «Velg anlegg» (fra skissen); standard radioknapper |
| Opplasting, utledet område (FR23) | «Område: Trøndelag – grense som for sør» (fylket fra fila) |
| Opplasting, overskrift i feilmelding | «Fila har N feil. Marin har ikke laget noen prognose.» (fra skissen, f.eks. «Fila har 3 feil.») |
| Opplasting, flere enn 20 feil | De 20 første feilene, så «… og N feil til. Rett feilene over og se etter samme feil i resten av fila.» |
| Opplasting, mens fila leses | «Leser fila …» |
| Opplasting, område ikke valgt | «Velg område: sør eller nord.» |
| Opplasting, anlegg ikke valgt | «Velg ett av anleggene i fila.» |
| Detaljside, lastetilstand | «Regner ut prognose …» |
| Statusboks, opplastede data | «Dine opplastede tall: {filnavn}» (f.eks. «Dine opplastede tall: lusetall_langholmen.csv») |
| Ingen treff (FR6) | «Fant ingen anlegg som passer «{søk}». Søk på lokalitetsnavn eller lokalitetsnummer.» |
| Over analyseuka i statusboksen | «Prognose regnet fra uke 42, 2026» (fra skissen) |
| Usikkerhetstekst (FR19) | «Prognosen er en enkel trendberegning, ikke en garanti. I en test på data fra 2025–2026 varslet Marin rødt 2–4 uker før X % av bruddene. Av alle røde varsler ble Y % fulgt av brudd innen 4 uker.» (PRD FR19) |
| Opplasting, om lagring (FR26) | «Fila lagres ikke. Tallene forsvinner når du går bort fra prognosen for dem, lukker fanen eller laster opp en ny fil.» |

| Gjør | Ikke gjør |
|---|---|
| «Fortsetter trenden, passerer anlegget grensen i uke 44.» | «Prognose: kryssing t+2.» |
| «Hitra, Trøndelag» | «Sør» |
| «uke 42, 2026» | «2026-W42», «42/26» |
| «Rad 7: lusetallet «abc» er ikke et tall.» | «Ugyldig input.» |
| Forklar hvorfor det ikke finnes prognose | Tom graf uten forklaring |

## Component Patterns

Oppførsel. Visuell spesifikasjon ligger i `DESIGN.md` (Components). Navnene er de samme i begge filene.

| Komponent | Brukes på | Regler for oppførsel |
|---|---|---|
| **Toppfelt** | Alle flater | Logoen går til forsiden. Desktop: søkeskjema (etikett «Søk anlegg», visuelt skjult; søkefelt; knappen «Søk») + «Bytt anlegg». Mobil: «Søk / bytt» går til forsiden med søkefeltet i fokus. «Last opp egne tall» går til opplasting. Søk fra toppfeltet viser treflisten på forsiden. På forsiden skjules søkefeltet og «Bytt anlegg» («Søk / bytt» på mobil), fordi siden har sitt eget søk; bare logo og «Last opp egne tall» vises. |
| **Statusboks** | Detaljside | Selvforklarende i et skjermbilde, uten resten av siden: anleggsnavn, lokalitetsnr., kommune og fylke, «Prognose regnet fra uke X, ÅÅÅÅ», symbol i hvit sirkel (`{components.status-symbol-badge}`) + R4-tekst (+ «(uke Y)» ved rød varsel og gul, FR18), én forklarende setning. Ved opplastede data også linja «Dine opplastede tall: {filnavn}» (UX-5). Hele boksen er synlig uten rulling på desktop ved 100 % zoom og står over grafen på mobil. Oppdateres når analyseuka endres. Ingen interaktive elementer inne i boksen. Fargen følger `{components.status-box-red}` / `{components.status-box-yellow}` / `{components.status-box-green}` / `{components.status-box-grey}`. |
| **Statusmerke** | Ukestabell, fargeforklaring | Ikke interaktivt. Har alltid tekst ved siden av symbolet. Fylles aldri med statusfarge. |
| **Analyseukevelger** | Detaljside | Nedtrekksliste, nyeste uke øverst. Innebygde data: 2026 uke 42 til 2025 uke 1, standard 2026 uke 42 (FR7). Uke 53 bare for ISO-år som har den. Opplastede data: bare ukene fila dekker, standard siste uke i fila (FR25). Valg regner prognosen på nytt med bare data til og med valgt uke (FR8) og oppdaterer statusboks, graf, tabell og «Prognose regnet fra». Anlegget og rulleposisjonen beholdes. |
| **Søkefelt** | Forside, toppfelt (desktop) | Delvis treff på navn uten hensyn til store og små bokstaver, eller lokalitetsnummer (FR4). Søket kjøres ved Enter eller knappen «Søk», ikke for hvert tastetrykk. Tomt søk gjør ingenting. |
| **Trefliste** | Forside | Viser navn, lokalitetsnr., kommune og fylke (FR5). Hele raden er klikkbar og åpner detaljsiden. Sortert alfabetisk på navn; vises også ved ett treff. Ingen status i listen (ingen samlet oversikt i v1). |
| **Graf** | Detaljside | Viser målte lusetall i vinduet, trendlinja 6 uker fram og grensen per uke som trapp (FR16). Uten prognose (grå eller brudd nå): bare målte tall og grense, ingen trend og ingen kryssingsmarkør (FR20a). Ikke interaktiv i v1. Under grafen står en synlig tekstoppsummering med målte verdier, prognoseverdier per uke, grensen per uke og kryssingsuka (maler i *Voice and Tone*, se også *Accessibility Floor*). |
| **Ukestabell** | Detaljside | 5 rader, eldste øverst. Overskrift «De siste 5 ukene», eller «De 5 ukene før analyseuka» ved «ingen ny telling» (FR17, FR20a). Uke uten telling: «–» og statusmerket «– Ikke telt». Siste telling merkes «Siste telling». |
| **Usikkerhetstekst** | Detaljside, nederst | Fast tekst etter FR19 med tallene fra siste backtest (FR28). Vises for alle statuser. |
| **Fargeforklaring** | Forside | Fire rader: rød (brudd nå, eller grensen nås om 1–3 uker), gul (grensen kan nås om 4–6 uker), grønn (ingen kryssing ventet innen 6 uker), grå (ingen prognose: for lite data, ingen ny telling eller ukjent område). Innholdet følger R4. |
| **Opplastingsskjema** | Opplasting | Steg: 1) velg fil (.csv, .xlsx); 2) Marin leser fila; 3) ved behov: velg anlegg med standard radioknapper (Excel med flere anlegg, FR22) og velg område sør/nord (CSV, eller Excel uten fylke, FR23a), eller se utledet område (Excel med fylke, FR23); 4) «Vis prognose» åpner detaljsiden (FR25). Ny opplasting erstatter forrige (FR26). Påkrevde valg, feilkobling og fokus: se *Skjemafeil* under State Patterns. |
| **Feilmelding** | Opplasting | Vises over skjemaet, og overskriften får fokus (se *Skjemafeil*). Overskrift «Fila har N feil. Marin har ikke laget noen prognose.» Sier hva som er galt og i hvilken rad (FR24). Feilene listes én per linje; er det flere enn 20, vises de 20 første og en linje om resten. Mens fila har feil, skjules anleggsvalg, områdevalg og «Vis prognose»; bare feilmeldingen og filvelgeren vises. Fila kan velges på nytt uten å laste siden. |
| **Knapp** | Opplasting, søk | Primærknapp for hovedhandlingen på flaten («Vis prognose», «Søk»). Én primærknapp per flate. Knappen i toppfeltets søkeskjema er sekundær. Knapper deaktiveres bare mens fila leses; ellers er «Vis prognose» alltid aktiv, og manglende valg gir feilmelding (se *Skjemafeil*). |

## State Patterns

**Detaljside – status** (R4). Rekkefølge når flere betingelser gjelder samtidig; den første som slår til, gjelder:

1. Ukjent område → grå
2. Ingen ny telling → grå
3. Brudd nå → rød
4. For lite data → grå
5. Rød, gul eller grønn etter prognosen

Brudd nå går foran for lite data, så et brudd skjules aldri (T11).

| Tilstand | Statusboks | Graf | Ukestabell |
|---|---|---|---|
| Rød – varsel (1–3 uker) | `{components.status-box-red}`, R4 + «(uke Y)» | Målt, trend, grense, kryssingsmarkør i uke Y | De siste 5 ukene |
| Rød – brudd nå | `{components.status-box-red}`, «✕ Brudd nå» | Målt og grense, ingen trend (FR20a) | De siste 5 ukene |
| Gul (4–6 uker) | `{components.status-box-yellow}`, R4 + «(uke Y)» | Målt, trend, grense, kryssingsmarkør | De siste 5 ukene |
| Grønn | `{components.status-box-green}` | Målt, trend, grense, ingen markør | De siste 5 ukene |
| Grå – for lite data | `{components.status-box-grey}` + forklaring (FR20) | Målt og grense, ingen trend | De siste 5 ukene |
| Grå – ingen ny telling | `{components.status-box-grey}` + forklaring | Målt og grense, ingen trend | De 5 ukene før analyseuka |
| Grå – ukjent område | `{components.status-box-grey}` + forklaring. Stedslinja viser det som finnes av kommune og fylke | Målt, ingen grenselinje fordi grensen er ukjent; tegnforklaringen sier «Grensen er ukjent» | De siste 5 ukene |

**Andre tilstander**

| Tilstand | Flate | Behandling |
|---|---|---|
| Første besøk | Forside | Introsetning, fargeforklaring, søkefelt. Lenken til opplasting står bare i toppfeltet. |
| Åpning med husket anlegg | Detaljside | Rett til detaljsiden, «Sist viste anlegg» over tittelen. |
| Ingen treff | Forside | Melding etter FR6 under søkefeltet. Søketeksten beholdes. |
| Laster | Detaljside | Tittel og analyseukevelger vises med en gang; i statusboksens plass står «Regner ut prognose …» i `{components.status-loading}` til svaret kommer: heltrukken nøytral kant, ingen statusfarge, ingen stipling og intet symbol, så lastingen ikke kan forveksles med grå status. Lastetilstanden leses ikke opp. Målet er under 2 sekunder (NFR8). Ingen animasjon. |
| Laster / leser fil | Opplasting | «Leser fila …» under filvelgeren, i en `role="status"`-region som finnes i siden fra start; «Vis prognose» er deaktivert (`{components.button-primary}` deaktivert) til fila er lest. |
| Feil i fil (FR24) | Opplasting | Feilmelding med rad. Ingen prognose. Anleggsvalg, områdevalg og «Vis prognose» skjules; bare feilmeldingen og filvelgeren vises. Typer og ordlyd: |
| | | Ukjent format: «Marin kjenner ikke igjen formatet. Marin godtar CSV med komma som skilletegn og punktum som desimaltegn, eller semikolon som skilletegn og komma som desimaltegn (norsk Excel), og Excel-uttrekk fra BarentsWatch.» |
| | | Manglende kolonner: «Fila mangler kolonnen «voksne_hunnlus». Kolonnene må hete år, uke og voksne_hunnlus.» |
| | | År utenfor området: «Rad 4: året 1999 er utenfor 2000–{inneværende år}.» |
| | | Uke utenfor området: «Rad 5: uke 54 finnes ikke. Uke må være 1–53.» / «Rad 5: 2025 har ikke uke 53.» |
| | | Ugyldig lusetall: «Rad 7: lusetallet «-0,2» er negativt.» / «Rad 7: lusetallet «abc» er ikke et tall.» |
| | | Feil desimaltegn: «Rad 7: «0.3» – fila bruker semikolon, så tallet må ha desimalkomma (0,3).» / «Rad 7: «0,3» – fila bruker komma som skilletegn, så tallet må ha desimalpunktum (0.3).» |
| | | Duplikat: «Rad 9: uke 34, 2026 finnes allerede i rad 6.» |
| Excel med flere anlegg | Opplasting | Liste over anleggene i fila under overskriften «Velg anlegg», samme radoppsett som treflisten, med standard radioknapper. Brukeren velger ett (FR22). |
| Område utledet | Opplasting | Tekst med fylket først og regelen forklart: «Område: Trøndelag – grense som for sør» (FR23; avviker fra eksempelet i PRD, se UX-4 i *Avvik og tillegg til PRD*). Ikke redigerbart. |
| Område må velges | Opplasting | Radioknapper sør/nord, påkrevd før «Vis prognose» (FR23a). Hjelpetekst som sier hvilke fylker som hører til: «Nord: Nordland, Troms og Finnmark. Sør: alle andre fylker.» Ingen forhåndsvalg. Lastes en ny fil av samme type opp i samme økt, beholdes valget. |
| Opplastede data vist | Detaljside | Samme detaljside (FR25). Tittelen er lokalitetsnavnet fra Excel, eller filnavnet for CSV; stedslinja viser kommune og fylke når fila har dem. Inne i statusboksen står «Dine opplastede tall: {filnavn}» (`{components.uploaded-data-line}`), så et skjermbilde viser at tallene er brukerens egne og ikke BarentsWatch-utdraget (UX-5). «Sist viste anlegg» vises ikke. |
| Navigerer bort fra opplastede data | Detaljside → annen flate | Opplastede data forkastes når brukeren forlater detaljsiden for dem i samme fane (logo, «Bytt anlegg», søk, «Last opp egne tall»). Nettleserens tilbakeknapp går da til opplastingssiden, ikke tilbake til prognosen. Ingen tidsgrense ellers (UX-7, presisering av FR26). |
| Fane lukket / ny fil | — | Opplastede data er borte (FR26). Neste åpning følger rutingen for husket innebygd anlegg. |
| Tastaturfokus | Alle | Synlig `{components.focus-ring}` på alle interaktive elementer. |

**Skjemafeil (opplasting)**

- **Filfeltet** er et ekte filfelt med koblet etikett «Fil». `aria-describedby` peker på hjelpeteksten. Har fila feil, får feltet `aria-invalid="true"`, og `aria-describedby` peker også på feilmeldingen.
- **Påkrevde valg.** «Vis prognose» er alltid aktiv når den vises. Trykker brukeren uten å ha valgt område (sør/nord) eller anlegg (Excel med flere anlegg), vises feilteksten rett under gruppens overskrift: «Velg område: sør eller nord.» eller «Velg ett av anleggene i fila.» Gruppen (radioknappene med felles overskrift) får `aria-invalid="true"` og `aria-describedby` som peker på feilteksten (og på hjelpeteksten for område). Fokus flyttes til første radioknapp i den første gruppen med feil (anleggsvalget står før områdevalget). Feilteksten forsvinner når et valg er gjort.
- **Fokus etter innlesing med feil i fila:** fokus flyttes til overskriften i feilmeldingen («Fila har N feil. …»), som kan få fokus programmatisk. Skjermleseren leser overskriften; resten av lista leses i vanlig leserekkefølge.
- **Fokus etter at fila er rettet og lastet opp på nytt:** feilmeldingen forsvinner, og fokus flyttes til neste steg: overskriften «Velg anlegg» ved Excel med flere anlegg, ellers første radioknapp i områdevalget (CSV, eller Excel uten fylke). Trengs ingen valg (Excel med fylke og ett anlegg), flyttes fokus til «Vis prognose», som har «Område: …»-linja i `aria-describedby`.
- **Ingen dobbel opplesing.** Feilmeldinger meldes med programmatisk fokus, ikke med `role="alert"`. Fokus og `role="alert"` brukes aldri på samme element. Bare «Leser fila …» bruker en `role="status"`-region, og den får ikke fokus.

## Interaction Primitives

- Klikk og trykk for å handle. Ingen funksjon finnes bare ved hover.
- Analyseuke velges i en vanlig nedtrekksliste; endringen gjelder med en gang, uten egen «Oppdater»-knapp.
- Søk sendes med Enter eller «Søk».
- Fil velges med nettleserens filvelger. Dra-og-slipp er ikke med i v1.
- Skjermbilde av statusboksen tas med enhetens eget verktøy. Marin har ingen dele- eller eksportknapp i v1 (varsler og deling er ute av v1).
- Trykkflater: alle interaktive mål er minst 44 × 44 CSS-px på mobil (`{spacing.target-min}`): logo, toppfeltlenker, analyseukevelger, søkefelt og søkeknapp, filknapp, radioknapper (klikkbar etikett over hele raden) og rader i treflisten. På desktop er felt, nedtrekksliste og knapper også minst 44px høye, og tekstlenker minst 24 × 24 CSS-px (`{spacing.target-min-inline}`).
- **Ikke i v1:** mørk modus, full statusfarge utenfor statusboksen, samlet oversikt, varsler på SMS, e-post eller push.

## Accessibility Floor

Oppførsel. Kontrast og farger ligger i `DESIGN.md` (Colors).

- **Status uten fargesyn (NFR4):** status vises alltid med farge, symbol og tekst sammen, også i statusmerker og grafmarkør. Rød og grønn har samme lyshet (1,06:1), så i statusboksen står symbolet stort i en hvit sirkel (`{components.status-symbol-badge}`, minst 32px) og skiller statusene i gråtoner, i sollys og ved fargesynsvikt. Kryssingsetiketten i grafen har statusordet («✕ Varsel uke 44»). Symbolet er skjult for skjermleser (`aria-hidden`), siden teksten bærer meningen.
- **Kontrast:** WCAG 2.x AA. Tekstparene i DESIGN.md er alle ≥ 4,5:1; gul har alltid mørk kant fordi gul mot hvitt er 1,8:1. Skjemafelt har kant på minst 3:1 (`{colors.border-strong}`).
- **Tastatur:** alt kan nås og brukes med Tab, Shift+Tab, Enter, mellomrom og piltaster. Tab-rekkefølgen følger leserekkefølgen: toppfelt, analyseukevelger, innhold. Nedtrekksliste, radioknapper og filvelger er standard skjemaelementer.
- **Skjermleser:**
  - Siden har `lang="nb"`.
  - Statusboksen er en navngitt region («Status»), men boksen som helhet er ikke live. Bare statusoverskriften (R4-teksten med eventuell «(uke Y)») er `aria-live="polite"`. Elementet finnes i siden fra start og beholdes; bare teksten byttes når ny status er klar. Når analyseuka endres, leses dermed bare den nye statusoverskriften opp, ikke navn, sted og forklarende setning. Lastetilstanden («Regner ut prognose …») står utenfor live-elementet og leses ikke opp. Utregningen starter ca. 300 ms etter siste endring i velgeren, så piltaster i en lukket nedtrekksliste ikke gir én opplesing per uke.
  - Grafen er et bilde for skjermleser (`role="img"`, innholdet i SVG-en skjult) og er knyttet til en **synlig** tekstoppsummering under grafen (figurtekst, ikke bare `aria-label`). Oppsummeringen er for alle, også seende som har vansker med å lese grafer eller står i sollys. Den inneholder målte verdier, prognoseverdier per uke, grensen per uke med vårtrappen (0,5 / 0,2) og kryssingsuka. Grå tilstander, inkludert ukjent område, har egne maler (se *Tekstoppsummering under grafen* i Voice and Tone). Ukestabellen er i tillegg tekstalternativet for de siste 5 målte ukene.
  - Feil ved opplasting: se *Skjemafeil* (fokus på feiloverskriften, ingen `role="alert"`).
  - Ingen treff (FR6) leses opp via `aria-live`.
- **Tekststørrelse og reflow:** siden fungerer ved 320 CSS-px bredde og 400 % zoom uten vannrett rulling, og med økt tekstavstand (WCAG 1.4.12) uten at innhold går tapt. Toppfeltet bryter til to linjer ved behov. Kravet om at statusboksen er synlig uten rulling på desktop gjelder ved 100 % zoom. Tekst i grafen er minst 13 CSS-px ved alle bredder og følger tekstzoom (DESIGN.md Typography). Sjekklista (NFR10) tester 320px, 600px, 400 % zoom og 200 % tekstzoom.
- **Uke uten telling** skrives «ikke telt» i tekst, ikke bare som tomt felt.

## Key Flows

Navnene følger PRD-ens brukerreiser (J1–J3).

### UJ-1 (J1 Sjekk status for mitt anlegg) – Kari, onsdagssjekken

Kari er driftsleder på et anlegg på Hitra i Trøndelag. Onsdag morgen sjekker hun Marin fast på kontor-PC-en. Hun vil vite status. Skisse av det hun ser: `mockups/key-detaljside.html`.

1. Kari åpner Marin. Anlegget hennes er husket, så detaljsiden åpner direkte med «Sist viste anlegg», tittelen og «Hitra, Trøndelag». Analyseuka er «uke 42, 2026».
2. Statusboksen står øverst med farge, symbol og R4-tekst.
3. Hun ser på grafen og fargekoden for et raskt innblikk: målte tall, trendlinja og hvor den møter grensen.
4. Deretter leser hun ukestabellen for å se de faktiske tallene uke for uke.
5. **Klimaks:** fargen. Er den grønn eller gul, puster Kari lettet ut. Er den rød, gir det stress.
6. Etterpå: grønn – normal drift. Gul – hun snakker med en medarbeider. Rød – hun tar skjermbilde av statusboksen og sender det til dem som er ute på merden, så de kan sette i gang tiltak.
7. Mottakerne åpner skjermbildet på mobil og forstår det uten å åpne Marin: anlegg, sted, analyseuke, status og når grensen nås står i boksen.

Første gang (ingen husket anlegg): Kari kommer til forsiden, leser setningen om hva Marin er og fargeforklaringen, søker «Langholmen», velger anlegget i treflisten (FR4–FR5), og fra da av åpner Marin det direkte.

Feil: søket gir ingen treff → meldingen etter FR6, Kari prøver lokalitetsnummeret i stedet. Grå status → forklaringen i statusboksen sier hvorfor det ikke finnes prognose (FR20).

Risiko: mottakerne ute på merden har dårlig dekning. Derfor skal statusboksen være selvforklarende som bilde, og siden skal være lett (se *Responsive & Platform*).

### UJ-2 (J2 Se hvordan varselet ville sett ut tidligere) – Kari sjekker om hun kan stole på varselet

Kari husker et brudd fra i vår. Hun vil se om Marin ville varslet i tide, for å vite om hun kan stole på varselet.

1. På detaljsiden for anlegget sitt åpner Kari analyseukevelgeren.
2. Hun velger en uke noen uker før bruddet hun husker.
3. Marin regner på nytt med bare data til og med den uka (FR8). Statusboksen viser «Prognose regnet fra uke X, 2026» (FR9), og graf og tabell følger.
4. Hun leser statusen og den forklarende setningen.
5. **Klimaks:** Kari ser om Marin ville varslet rødt i tide før bruddet – og dermed om hun kan stole på varselet hun får nå.
6. For å se hva som faktisk skjedde, velger hun en senere analyseuke (J2 steg 3) og ser «✕ Brudd nå».
7. Usikkerhetsteksten nederst gir henne også treffandelen fra backtesten (FR19).

Feil: uka hun velger har «– Ingen ny telling siden uke X» (telling annenhver uke) → forklaringen sier hvorfor, og hun velger uka etter.

### UJ-3 (J3 Få prognose på egne lusetall) – Kari laster opp ukas telling

Kari har nettopp talt lus denne uka. Tallet er ikke med i utdraget, og hun vil se prognosen med de nyeste tallene.

1. Fra detaljsiden velger Kari «Last opp egne tall».
2. Hun velger en CSV-fil med de siste ukene, lagret fra sitt eget regneark (semikolon og desimalkomma, FR21).
3. Marin leser fila. Siden det er CSV, ber Marin henne velge område; hun velger sør (FR23a).
4. Hun trykker «Vis prognose».
5. Detaljsiden for de opplastede dataene åpner med analyseuke lik siste uke i fila (FR25).
6. **Klimaks:** Kari ser prognosen med sin egen ferske telling – status og når grensen eventuelt nås, regnet med tallene fra denne uka.
7. Dataene lagres ikke (FR26). Neste gang hun åpner Marin, kommer det huskede anlegget fra utdraget.

Feil: fila har «0.3,» i én rad → feilmeldingen sier hvilken rad og hva som er galt (FR24). Kari retter i regnearket og laster opp på nytt. Fila er Excel fra BarentsWatch med flere anlegg → hun velger sitt anlegg, og området vises utledet av fylke (FR22, FR23).

Ikke i v1: å legge inn enkelttall i BarentsWatch-serien for et innebygd anlegg. Kari laster opp hele serien hun vil bruke, og den vises som eget datasett.

## Responsive & Platform

| Bredde | Oppførsel |
|---|---|
| Desktop (≥ 600px) | Én kolonne, maks `{spacing.content-max-width}`. Toppfelt med søkeskjema (skjult etikett «Søk anlegg», felt og knappen «Søk»), «Bytt anlegg» og «Last opp egne tall» (på forsiden bare «Last opp egne tall»). Typografi fra desktop-tokens. |
| Mobil (< 600px) | Samme én kolonne og samme rekkefølge. Toppfelt med «Søk / bytt» (og «Last opp egne tall»; på forsiden bare «Last opp egne tall»). Søkefeltet ligger på forsiden med plassholderen «Søk navn eller nr.». Mobiltokens (`*-mobile`) for type og luft. Ukestabellen får plass uten vannrett rulling. |

- **Mobil ute på anlegget, dårlig dekning:** siden holdes lett. Systemfonter, ingen bilder, grafen som SVG. Ingen tunge tredjepartsbiblioteker kun for grafen; arkitekturen avgjør.
- **Skjermbilde:** statusboksen er en selvstendig blokk med all nødvendig tekst, så den gir mening når den beskjæres ut.
- **Sollys:** statusboksens fulle flater har sterk tekstkontrast (6,2–10,3:1). Rød og grønn flate er like lyse, så i sollys er det det store symbolet i hvit sirkel som skiller dem.
- **Smal skjerm og zoom:** fungerer ned til 320 CSS-px bredde uten vannrett rulling (se *Accessibility Floor*).
- Ingen mobilapp i v1; mobil er den samme nettsiden.

## Avvik og tillegg til PRD

Hvert UX-tillegg har en midlertidig ID (UX-1, UX-2, …). Hvert av dem trenger en FR i PRD-en (ny FR eller presisering av en eksisterende, via `bmad-prd` eller `bmad-correct-course`) før epics og stories lages. Til da kan epics vise til UX-ID-en.

| ID | Tema | Hva UX bestemmer | Konsekvens for PRD |
|---|---|---|---|
| UX-1 | Husk siste anlegg | Marin husker sist viste innebygde anlegg per nettleser og enhet, uten innlogging, og åpner det direkte. Gjelder ikke opplastede data. | **Ny FR trengs** (ikke i PRD v1). Må forenes med FR26 og NFR6: bare anleggets ID lagres lokalt, ingen lusetall eller personopplysninger. |
| UX-2 | Forklaring ved første besøk | Forsiden har én setning om hva Marin er og en fargeforklaring for de fire statusene. | Tillegg til PRD §8 Forside (som bare nevner søkefelt, trefliste og lenke). FR trengs (ny FR eller presisering av §8). |
| UX-3 | Forklarende setning under status | Under R4-teksten kommer én forklarende setning. R4-teksten er uendret. | Tillegg til FR15/FR18; FR trengs. T5–T12 tester fortsatt bare R4-teksten. Malene trenger egne kontrollpunkter i README-sjekklista (NFR10). |
| UX-4 | Områdetekst ved opplasting | Utledet område ved Excel-opplasting vises med fylket først og regelen forklart: «Område: Trøndelag – grense som for sør». | Avviker fra eksempelteksten i PRD FR23 («Område: sør (Vestland)»). Oppførselen er den samme; bare ordlyden endres. FR23 må presiseres. |
| UX-5 | «Dine opplastede tall» i statusboksen | Når detaljsiden viser opplastede data, står «Dine opplastede tall: {filnavn}» inne i statusboksen, så et skjermbilde ikke kan forveksles med BarentsWatch-tall. | Tillegg til FR25; FR trengs. |
| UX-6 | Statusboksen inneholder anleggsnavn og sted | Navn, lokalitetsnr., kommune, fylke og analyseuke gjentas inne i statusboksen for skjermbilde. | Presisering av FR15 og FR9; FR trengs. |
| UX-7 | Opplastede data forkastes ved navigering bort | Opplastede data forkastes når brukeren forlater detaljsiden for dem i samme fane; tilbakeknappen går til opplastingssiden. Lagringsnotisen sier dette. | Presisering av FR26 (som bare nevner lukket fane og ny fil); FR trengs. |
| – | Samlet oversikt | Skissert i `mockups/key-oversikt-skisse.html` som mulig neste versjon (PRD §9). Ikke del av v1. I skissen vises R4-teksten med symbolet i statusmerket. | Ingen endring i v1. Skissen er grunnlag om oversikten tas inn i en senere versjon. |
