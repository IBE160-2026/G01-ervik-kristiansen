# PRD Quality Review — PRD: Marin

## Overall verdict
PRD-en er stram og godt egnet som grunnlag for videre arbeid. Kjernelogikken (grense, trend, status) er knyttet til regler i briefen som har håndregnet fasit (R1–R6, T1–T10), avgrensningene er tydelige, og sporingen mellom krav og brief går begge veier. Risikoen ligger i kantene: FR19 lover å fortelle brukeren om falske alarmer, men krever bare at treffandelen vises. Opplastingsflyten (FR21–FR26) og visningen av grå status og «brudd nå» på detaljsiden er heller ikke spesifisert godt nok til at stories kan skrives uten å gjette. Til slutt henger kap. 13 og metadata etter beslutningene fra 2026-11-11.

## Decision-readiness — adequate
Beslutningene står som beslutninger og er datert. Det gjelder FR29 («Beslutning 2026-11-03»), A1 og A2, som er lukket med tydelig utfall (§12), og at regionledere er tatt ut med begrunnelse (§3: «Derfor har v1 ingen samlet oversikt»). §11 er ærlig om svak presisjon: «bare omtrent 14 % av de røde varslene ble fulgt av brudd. Mange røde varsler er altså falske alarmer». Dette er sjelden god ærlighet.

Det som mangler, er en beslutningsregel for tilfellet der backtesten bommer. M1 måles med «minst 25 % treff», og den grove backtesten ga omtrent 29 %, altså en margin på bare 4 prosentpoeng. PRD-en sier ikke hva gruppen gjør hvis appens egen backtest (som briefen sier «avgjør») havner under 25 %. FR29 mangler også begrunnelse for hva som ble gitt opp. Leseren ser at backtesten ikke blir en side, men ikke hvorfor.

### Findings
- **medium** Ingen plan hvis SK2 ikke nås (§2 M1, §11 «Treffsikkerhet») — Marginen er liten (29 % mot 25 %), og appens egen backtest kan gi et annet tall enn skissen. Det står ikke om svaret da er å justere parametere (vindu, horisont), rapportere avviket ærlig eller noe annet. *Fix:* Legg til én setning i §11 eller §12 om hva gruppen gjør hvis treffandelen havner under 25 %, og om parametere i R2 kan endres etter backtesten.
- **low** FR29 mangler begrunnelse (§5.7 FR29) — «Beslutning 2026-11-03» uten begrunnelse. *Fix:* Skriv en halv setning om hvorfor, f.eks. omfang og tid, og at resultatet likevel synes gjennom FR19.

## Substance over theater — strong
Lite pynt. To personer, og begge driver krav. Primærbrukeren gir FR15–FR20 og NFR4–NFR5, og sensoren gir NFR1–NFR3. Målene i §2 er knyttet til målbare SK-er. Ikke-funksjonelle krav har konkrete, produktspesifikke betingelser («0 avvik» mot `Lusegrense uke`, «uten API-nøkler, betalte kontoer eller nettilgang», «farge, symbol og tekst sammen»). Differensieringen er lånt fra briefen og framstilt nøkternt. NFR7 («ingen KI») og NFR6 tilfører lite som krav, men de svarer på konkret tilbakemelding og koster ingenting.

### Findings
- **low** NFR8 er delvis et adjektiv (§6 NFR8) — «på en vanlig bærbar PC» og «etter at appen har startet» lar oppstartstiden være ubegrenset. Innlesing av to Excel-filer kan ta tid, og det er der sensor merker det. *Fix:* Legg til en øvre grense for oppstart, eller presiser at innlesingen ikke regnes med og hvorfor det er greit.

## Strategic coherence — adequate
Tesen er tydelig og bærer dokumentet: «et forvarsel … ikke bare et øyeblikksbilde» (§1, M1). Kravene følger tesen. Analyseuke og tilbakeblikk (FR7–FR9, J2) gjør prognosen etterprøvbar, og backtesten (FR27–FR28) validerer tesen direkte i stedet for å måle aktivitet. MVP-en er problemløsende, og avgrensningen passer til det.

Svakheten er motmålet. Andelen falske alarmer blir bare rapportert (FR28) og har ingen terskel, og den når ikke brukeren fullt ut (se Done-ness, FR19). Et varsel som er falsk alarm 86 % av gangene, undergraver «et varsel de kan stole på» (briefen, Hvem dette tjener). PRD-en navngir problemet, men gjør det ikke til et kriterium. M3 («forstår status … uten datafaglig bakgrunn») måles med SK3 og SK4, som sjekker at elementene finnes, ikke at brukeren forstår dem. Uten tilgang til brukere er det greit, men koblingen bør kalles det den er.

### Findings
- **medium** Motmålet har ingen terskel eller tolkning (§2, FR28, §11) — Andelen falske alarmer rapporteres, men PRD-en sier ikke hva som er akseptabelt eller hvordan tallet skal brukes. *Fix:* Legg til andelen falske alarmer som eget, observert motmål i §2 (f.eks. M1b, «rapporteres, ingen terskel i v1»), slik at det blir et synlig mål og ikke bare et utdata.
- **low** M3 måles med funksjonssjekk, ikke forståelse (§2 M3) — *Fix:* Skriv at M3 er en proxy i v1, eller legg til en enkel gjennomgang med én fagperson, hvis det er realistisk.

## Done-ness clarity — adequate
Kjernen er sterk. FR10–FR14 viser til R1–R4 med testtilfeller med fasit (T1–T10), og det er bedre enn det de fleste PRD-er klarer. FR8 er presist etter A1. FR24 lister konkrete valideringsfeil og krever at radnummeret vises.

Hullene ligger i det reglene ikke dekker: hva detaljsiden viser når det ikke finnes noen prognose, og opplastingsflyten. Her må en utvikler gjette.

### Findings
- **high** FR19 oppfyller ikke det §11 lover (§5.5 FR19, §11 «Treffsikkerhet») — §11 sier at mange røde varsler er falske alarmer, og at «FR19 sørger for at brukeren får vite det». FR19 krever bare «treffandelen fra siste backtest». Treffandelen (andelen kryssinger som ble varslet) sier ingenting om hvor ofte rødt er falsk alarm. Briefen (SK2) sier at de to tallene skal rapporteres sammen. Brukeren får dermed det mest flatterende tallet og ikke det mest relevante. *Fix:* Utvid FR19 til å vise både treffandel og andelen røde varsler uten brudd innen 4 uker, i klart språk (f.eks. «Omtrent 1 av 7 røde varsler ble fulgt av brudd»). Ta med hva som vises hvis resultatfila fra FR28 mangler.
- **medium** Detaljsiden er uspesifisert for grå status og «brudd nå» (FR16–FR18, FR20) — FR16 krever «trendlinja forlenget 6 uker fram», men R2 sier at det ikke beregnes noen prognose ved «brudd nå», «for lite data» og «ingen ny telling». FR17 viser «de 5 ukene i vinduet», men ved «ingen ny telling» er t (og dermed vinduet) ikke definert. FR18 viser «estimert ISO-uke» ved rød status, men ved «brudd nå» finnes det ikke noe estimat. *Fix:* Legg til ett krav eller en tabell som sier hvilke elementer (graf, trendlinje, grense, tabell, estimert uke) som vises for hver status, og hvilket vindu tabellen bruker når t mangler (f.eks. de 5 ukene til og med analyseuka).
- **medium** Komma som desimaltegn er motstridende (FR21, FR24, §11 «Opplastede filer») — FR21 krever desimalpunktum, og §11 sier at FR24 «må håndtere» komma. FR24 lister ikke komma blant feilene. Utvikleren vet ikke om komma skal godtas eller gi feilmelding. *Fix:* Bestem dette i FR24: enten godtas komma, eller så gir det feilmeldingen «ikke-numerisk lusetall i rad N».
- **medium** Opplastingsflyten har udefinerte kanttilfeller (FR21, FR22, FR24–FR26) — (a) Kan brukeren endre analyseuke på opplastede data? FR7 begrenser valget til 2025 uke 1–2026 uke 42, mens FR25 setter analyseuka til «siste uke i fila». (b) Regnes uker som mangler helt i fila (ingen rad) likt med tom verdi? (c) Fanger valideringen opp uke 53 i år som bare har 52 ISO-uker, og uker som ikke ligger i rekkefølge? (d) Hva er «økta» (FR26) i en lokal app: fanen, nettleseren eller serverprosessen? *Fix:* Legg til en kort presisering for hvert punkt i FR24–FR26. (d) kan eventuelt merkes som noe arkitekturen avgjør.
- **low** «Lokalitetsnummer» i søk er tvetydig (FR4) — «delvis treff» gjelder navn. Det står ikke om nummer må treffe eksakt. *Fix:* Skriv «eksakt lokalitetsnummer» eller «delvis».

## Scope honesty — adequate
§9 har en reell liste over hva som er ute, med opphav («fra briefen, pluss beslutningene 2026-11-03»), og «Med i v1: alt i kapittel 5 og 6» er utvetydig. §7 sier eksplisitt hvilke kolonner som ikke brukes. De åpne punktene er få og ekte (bare A3 er åpen, og den hører hjemme i arkitekturen), og det passer innsatsnivået.

Det som mangler, er merking av antakelser. PRD-en har ingen `[ASSUMPTION]`-tagger. Briefen sier om primærbrukerens smerte: «Ikke bekreftet med reelle brukere», men §3 beskriver primærbrukeren og hva hun «vil vite» som etablert fakta.

### Findings
- **medium** Brukerbehovet er ikke merket som ubekreftet (§3) — Brukeren som «vil vite: Hvor lenge har jeg før grensen nås, og hvor sikker er den vurderingen?» er en antakelse som briefen selv flagger. *Fix:* Legg til `[ASSUMPTION: primærbrukerens behov er ikke bekreftet med reelle brukere (brief, Problemet)]` og en kort antakelsesindeks på slutten, eller samle punktet i §11.
- **medium** NFR3 «0 avvik» kan kollidere med en ting som er tatt ut (NFR3, §9 siste punkt) — Hvis BarentsWatch-kolonnen `Lusegrense uke` viser særskilte grenser for tillatelser med kapasitetsøkning, eller «Ukjent» for anlegg uten fylke, gir R1 slik den er implementert i v1, avvik per definisjon. *Fix:* Presiser i NFR3 hvilke rader som er unntatt (anlegg uten fylke, eventuelle særskilte grenser), eller skriv «0 avvik, unntatt rader merket …», etter at dataene er kontrollert.

## Downstream usability — adequate
ID-ene er stabile, og sporingen går begge veier (krav → R/SK i hver tabell, og brief → krav i §10). Alle henvisninger til briefen (R1–R6, T1–T10, SK1–SK5) finnes og stemmer, også T10 og A1-endringene. SK-nummereringen (1–5 i briefen → SK1–SK5) er forklart i §1. Skjermbildene i §8 knytter FR-områder til sider, og det hjelper UX-steget.

Det som trekker ned, er at PRD-en mangler en ordliste, mens domenebegrepene er mange og noe ustabile. Dessuten er §10 ikke komplett i retningen brief → krav.

### Findings
- **medium** Ingen ordliste. Begrepene «anlegg» og «lokalitet» brukes om hverandre (FR4–FR5, FR22, §7) — FR22 skriver «flere lokaliteter, velger brukeren én», mens resten av dokumentet bruker «anlegg». «Analyseuke», «t», «uke med telling», «område», «uker til grensen» og «økt» er sentrale, men definert spredt eller bare i briefen. *Fix:* Legg til en kort ordliste (5–8 begreper), og bestem at «anlegg» er brukerbegrepet og «lokalitet» datakolonnen.
- **low** §10 er ufullstendig (§10) — R2- og R4-radene mangler FR8 (som sporer til R2 og T10), SK3-raden mangler NFR5 og NFR8, og SK2-raden mangler FR19. *Fix:* Generer §10 som et omvendt oppslag fra sporingskolonnene.

## Shape fit — strong
Formen passer: en lokal prototype med én primærbruker og en sensor. Det er tre korte brukerreiser som hver dekker en reell flyt (status, tilbakeblikk og opplasting), og de er ikke pyntet med personas. Kapittelet om data (§7) og CSV-eksempelet er riktig vekting for et produkt som står og faller på data. Valget om å vise til briefens regler i stedet for å gjenta dem holder PRD-en kort og unngår at to kilder kommer ut av takt. Fordi dokumentet ligger øverst i kjeden (UX → arkitektur → stories), blir ordlisten og sporingen viktigere. Det er dekket under Downstream usability.

## Mechanical notes
- **ID-kontinuitet:** `FR23a` bryter nummereringen. Det er akseptabelt som midlertidig løsning, men det bør nummereres om (FR24 → …) før epics viser til ID-ene, eller så bør det beholdes bevisst med en merknad.
- **Utdatert innhold:** §13 punkt 1 «Lukke A1 og A2» er allerede gjort (§12). Frontmatter har `updated: 2026-11-03`, men beslutningene er fra 2026-11-11. `status: draft` bør vurderes.
- **Henvisninger til briefen:** Alle R-, T- og SK-henvisninger er kontrollert mot briefen og stemmer. NFR3 sporer til «addendum», som er briefens addendum og står i `inputs`, så det er greit.
- **Antakelsesindeks:** Den finnes ikke, og det finnes heller ingen inline-tagger. Se Scope honesty.
- **Hovedpersoner i brukerreisene:** J1–J3 bruker «Brukeren» = primærbruker fra §3. Det er tilstrekkelig, men kan gjøres eksplisitt («Driftsleder åpner appen …»).
- **FR6** har sporing «—». Det er greit, men kan spores til J1.
