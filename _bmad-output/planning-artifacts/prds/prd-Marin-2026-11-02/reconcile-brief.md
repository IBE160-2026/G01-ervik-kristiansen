---
title: "Avstemming: product brief mot PRD"
input: briefs/brief-Marin-2026-09-17/brief.md (status final, oppdatert for A1 2026-11-11)
prd: prds/prd-Marin-2026-11-02/prd.md (status draft)
dato: 2026-11-11
---

# Avstemming: product brief mot PRD (Marin)

Denne fila sammenligner briefen med PRD-en. Den leter etter ting PRD-en dropper uten å si det, sier imot eller sporer feil. Ingen av dokumentene er endret.

## Sammendrag

| # | Avvik | Alvorlighet |
|---|---|---|
| G1 | FR19 viser bare treffandelen. Andelen falske alarmer (SK2) vises ikke, selv om kap. 11 sier at FR19 sørger for at brukeren får vite om dem | Høy |
| G2 | Etter A1 kan t ligge én uke før analyseuka, og «om X uker» telles fra t. Hverken briefen eller PRD-en sier om teksten og fargen gjelder fra t eller fra analyseuka | Høy |
| G3 | Ingen rekkefølge mellom statusene: ukjent område, ingen ny telling, for lite data og brudd nå | Middels |
| G4 | Ved opplasting velger brukeren område når fylke mangler (FR23a). Det går imot R1, der manglende fylke gir «ukjent område», og avviket er ikke ført tilbake til briefen | Middels |
| G5 | Opplasting av egne data (J3, FR21–FR26) og valg av analyseuke (J2) er nytt omfang som ikke står i briefen. Det er ikke merket som et tillegg | Middels |
| G6 | Briefen lover et «dashboard» med «historisk lusetrend per anlegg». PRD-en viser bare vinduet på 5 uker, og har ingen oversikt | Middels |
| G7 | Sporingstabellen i kap. 10 er ikke oppdatert etter A1, og T1–T10 sporer bare til NFR2 | Middels |
| G8 | Spesialtilfellene brudd nå, negative estimater og årsskiftet har ingen T-case med fasit. FR13 sporer bare til T9 | Middels |
| G9 | FR16 og FR18 sier ikke hva grafen og estimert uke viser ved brudd nå og grå status | Lav |
| G10 | Rammen fra briefen er svekket: «ikke bekreftet med reelle brukere» og målgruppen (mellomstore og mindre selskaper) er borte | Lav |
| G11 | Gamle metadata: `updated: 2026-11-03`, og «Lukke A1 og A2» står fortsatt i kap. 13 | Lav |
| G12 | PRD-en innfører ID-ene SK1–SK5 og «Beslutning 2026-11-03», men disse finnes ikke som ID-er eller som dokument i briefen | Lav |

**Kontroll av A1 (FR8, FR14, FR20, NFR2):** FR8 stemmer med R2. t er siste telling til og med analyseuka, høyst én uke eldre, ellers «ingen ny telling». FR14 (T5–T10), FR20 (nevner «ingen ny telling» og T10) og NFR2 (T1–T10) er også konsistente. Det som gjenstår er følgene av A1: hva X betyr (G2), rekkefølgen mellom statusene (G3) og sporingstabellen (G7). FR8 har også en uheldig formulering: «telling fra og med analyseuka og bakover» bør være «til og med analyseuka».

**Dekning av reglene:** R1–R6, T1–T10 og SK1–SK5 er alle dekket av minst ett FR eller NFR. Omfanget som er ute av v1 i briefen, finnes igjen i kap. 9 i PRD-en. «Ingen KI» er dekket av NFR7, og at gruppen regner fasit for hånd står i kap. 11. «Prognose, ikke øyeblikksbilde» er dekket av M1, og ærlighet om usikkerhet av FR19, men delvis (G1).

---

## Funn i detalj

### G1 Andelen falske alarmer når ikke brukeren (høy)

- **Brief:** SK2 sier at andelen røde varsler som ikke ble fulgt av brudd innen 4 uker, skal rapporteres sammen med treffandelen. «Hva gjør dette annerledes» sier at treffsikkerheten er en sentral usikkerhet og skal presenteres ærlig.
- **PRD:** FR19 viser «treffandelen fra siste backtest». FR28 skriver bare treffandelen til fil «slik at FR19 kan vise» den. Kap. 11 sier at omtrent 86 % av de røde varslene er falske alarmer, og at «FR19 sørger for at brukeren får vite det».
- **Hvorfor det betyr noe:** Kravene sier ikke det kap. 11 lover. Det viktigste ærlighetspunktet, at de fleste røde varsler er falske alarmer, kan falle bort i implementeringen.
- **Forslag:** Utvid FR19: vis treffandelen og andelen røde varsler uten brudd innen 4 uker. Utvid FR28: skriv begge tallene til fila. Legg til SK2 som sporing på FR19.

### G2 Hva «X uker» betyr når t ligger før analyseuka (høy)

- **Brief:** R2 sier at k telles fra t, og at t kan være analyseuka − 1. R4 setter farge etter k: rød ved 1–3, gul ved 4–6. T10 sier at analyseuke 41 med de samme dataene «gir prognose som i T8», altså «grensen nås om 4 uker (uke 44)», med gul status. Fra analyseuke 41 er uke 44 bare 3 uker unna.
- **PRD:** FR8 overtar definisjonen av t. FR9 sier at detaljsiden viser «hvilken uke prognosen er regnet fra», uten å si om det er t eller analyseuka. FR14 og FR18 sier ingenting om dette.
- **Hvorfor det betyr noe:** Brukeren leser «om 4 uker» fra uka som er valgt, men det reelle tallet kan være 3. Det kan gi gul status der rød ville vært riktig sett fra analyseuka. Horisonten (6 uker) og «ingen kryssing innen 6 uker» blir på samme måte forskjøvet én uke. Dette påvirker også backtesten (SK2: rød 2–4 uker før kryssingen).
- **Forslag:** Ta stilling til det eksplisitt, helst i briefen (R2 og R4) først og så i FR9 og FR18. Det enkleste er å beholde k fra t og la detaljsiden vise både t («siste telling: uke 40») og den estimerte ISO-uka. Statusteksten bør da bruke ISO-uke i stedet for eller i tillegg til «om X uker». Det andre alternativet er å telle k fra analyseuka og regne T8 og T10 på nytt.

### G3 Rekkefølgen mellom statusene er udefinert (middels)

- **Brief:** R1 (ukjent område), R2 (ingen ny telling, for lite data, brudd nå) og R4 lister statusene, men sier ikke hvilken som sjekkes først.
- **PRD:** FR13 og FR14 viser til R2 og R4 uten noen rekkefølge.
- **Hvorfor det betyr noe:** Det finnes overlappende tilfeller. Et anlegg uten fylke og med gammel telling kan få to grå statuser. En gammel siste telling ≥ grensen kan gi enten «brudd nå» eller «ingen ny telling». Siste telling i uke t med bare 2 tellinger i vinduet og verdi ≥ grensen kan gi enten brudd nå eller for lite data. To utviklere kan gjøre dette ulikt, og T-casene avslører det ikke.
- **Forslag:** Fastsett rekkefølgen i R4, for eksempel ukjent område → ingen ny telling → brudd nå → for lite data → prognose. Legg til minst ett T-case som overlapper. Vis til rekkefølgen i FR14.

### G4 Brukeren velger område ved opplasting, mot R1 (middels)

- **Brief:** R1 sier at et anlegg uten fylke ikke får prognose og får status «ukjent område». Omfanget nevner ikke opplasting.
- **PRD:** FR23a og J3 (beslutning A2): ved CSV, og ved Excel uten fylke, velger brukeren sør eller nord.
- **Hvorfor det betyr noe:** Den samme BarentsWatch-raden uten fylke gir «ukjent område» i det innebygde datasettet, men en prognose når den lastes opp. R1 sier at grensen ikke kan bestemmes uten fylke. PRD-en lar brukeren bestemme den, men sier ikke at dette er et unntak fra R1.
- **Forslag:** Før unntaket inn i briefen (R1: «ved opplasting kan brukeren velge område») eller merk det som et bevisst avvik i PRD-en med henvisning til A2. Vurder å vise at området er valgt av brukeren, ikke utledet.

### G5 Nytt omfang er ikke merket som tillegg til briefen (middels)

- **Brief:** I omfanget for v1 er datagrunnlaget bare utdraget som ligger i repoet. Det står ingenting om opplasting eller om å velge analyseuke.
- **PRD:** J2 og FR7–FR9 lar brukeren velge analyseuke. J3 og FR21–FR26 gir opplasting av CSV og Excel. Kap. 9 sier «fra briefen, pluss beslutningene 2026-11-03» bare om det som er ute, ikke om det som er lagt til.
- **Hvorfor det betyr noe:** Opplasting er en betydelig utvidelse med validering, øktdata og valg av område, og den kan ikke spores til noe behov i briefen. Uten en kilde er det uklart om dette er bestemt med veileder eller sensor.
- **Forslag:** Legg til en linje i kap. 9: «Med i v1 utover briefen: valg av analyseuke (J2) og opplasting (J3), beslutning <dato/kilde>». Oppdater omfanget i briefen eller legg ved et beslutningsnotat.

### G6 «Dashboard» og «historisk lusetrend» er snevret inn (middels)

- **Brief:** Løsningen beskriver et «web-dashboard (status per anlegg, trendlinje, varselnivå)». Omfanget for v1 nevner et «dashboard som viser status og historisk lusetrend per anlegg».
- **PRD:** Kap. 8 har bare søk og en detaljside. FR16 og FR17 viser bare vinduet på 5 uker og 6 uker fram. En samlet oversikt er tatt ut av v1 (kap. 3 og 9).
- **Hvorfor det betyr noe:** En leser av briefen forventer et dashboard og lengre historikk. Det er gode grunner til at PRD-en har valgt annerledes, men den sier ikke at den tolker briefen.
- **Forslag:** Skriv i kap. 8 eller 9 at «dashboard» i v1 betyr detaljsiden per anlegg. Avklar om «historisk lusetrend» skal gi en lengre graf (f.eks. hele 2025–2026) i tillegg til vinduet, eller at J2 dekker behovet.

### G7 Sporingstabellen er ikke oppdatert etter A1 (middels)

- **Brief:** R2 og R4 inneholder nå regelen om ingen ny telling, og T10 finnes.
- **PRD:** Kap. 10 sporer R2 til FR2 og FR11–FR13, og R4 til FR14, FR15, FR20 og NFR4. FR8 mangler i begge radene, og FR18 mangler under R4. «R6 / T1–T10 → NFR2» viser ikke hvilket FR hver T tester. Kap. 12 sier at A1 er «ført inn i FR8, FR20 og NFR2», men kap. 10 viser ikke det.
- **Hvorfor det betyr noe:** Når epics og stories lages ut fra kap. 10, kan FR8 og T10 havne utenfor en story med regelansvar.
- **Forslag:** Legg FR8 til R2 og R4, og FR18 til R4. Legg til en kolonne eller tabell T → FR, for eksempel T1–T4 → FR10, T5 → FR11, FR12 og FR14, T6 → FR12, T7 → FR3 og FR20, T8 → FR11, T9 → FR13, T10 → FR8 og FR20.

### G8 Spesialtilfeller uten T-case med fasit (middels)

- **Brief:** R2 definerer brudd nå, negative estimater satt til 0, flat eller fallende trend uten unntak, og årsskiftet som sammenhengende tid. Ingen av T1–T10 tester disse. SK1 måler bare T1–T10.
- **PRD:** FR11 (årsskiftet) og FR13 (brudd nå og negative estimater) sporer bare til T9 og T5/T8. NFR2 krever bare T1–T10.
- **Hvorfor det betyr noe:** Bare to–tre av spesialtilfellene har fasit regnet for hånd. Det som er vanskeligst å få riktig, er årsskiftet med uke 52 eller 53 → 1. Brudd nå er den viktigste røde statusen.
- **Forslag:** Legg til T11–T13 i briefen (brudd nå, årsskiftet, negativt estimat og flat trend mot vårgrensen) og utvid NFR2. Alternativt kan PRD-en kreve egne tester for disse uten fasit fra briefen.

### G9 Graf og estimert uke i tilfeller uten prognose (lav)

- **Brief:** R2 sier at ved brudd nå beregnes ingen prognose. Ved grå status finnes det heller ingen.
- **PRD:** FR16 sier at trendlinja alltid forlenges 6 uker fram. FR18 viser estimert ISO-uke «ved rød eller gul», men rød omfatter brudd nå, der det ikke finnes noe estimat.
- **Forslag:** Legg til i FR16: ingen trendlinje ved brudd nå eller grå status, bare målte verdier og grensen. Presiser i FR18: gjelder ikke brudd nå.

### G10 Rammen fra briefen er svekket (lav)

- **Brief:** Smerten er størst hos mellomstore og mindre selskaper uten analyseressurser, og dette er «ikke bekreftet med reelle brukere». Primærbrukeren vil ha et varsel de «kan stole på».
- **PRD:** Kap. 3 sier «ett oppdrettsanlegg», med ingen datafaglig bakgrunn. Segmentet og forbeholdet om at brukerne ikke er bekreftet er borte, og kap. 11 nevner ikke risikoen. PRD-en legger til spørsmålet «hvor sikker er den vurderingen?», men svarer bare med en global treffandel i FR19.
- **Forslag:** Legg inn en risiko i kap. 11: brukerbehovet er ikke validert med reelle brukere. Nevn segmentet kort i kap. 3. Vurder å omformulere brukerens spørsmål slik at det ikke lover mer sikkerhet enn appen kan gi.

### G11 Gamle metadata (lav)

- **PRD:** Frontmatter sier `updated: 2026-11-03`, men A1 og A2 ble avgjort 2026-11-11. Kap. 13 punkt 1 sier «Lukke A1 og A2».
- **Forslag:** Sett `updated: 2026-11-11` og fjern punkt 1 i kap. 13.

### G12 ID-er som ikke finnes i kilden (lav)

- **PRD:** Bruker SK1–SK5 som ID-er. Briefen nummererer suksesskriteriene 1–5, men har ikke prefikset SK. FR29 sporer til «Beslutning 2026-11-03», og NFR6 og NFR9 sporer til «Tilbakemelding», men ingen av disse har en entydig henvisning.
- **Forslag:** Gi suksesskriteriene ID-ene SK1–SK5 i briefen, eller behold forklaringen i kap. 1. Vis til fil eller logg for beslutningen 2026-11-03 og til `tilbakemelding-product-brief.md`.

## Mindre merknader

- FR8: «fra og med analyseuka og bakover» bør være «til og med analyseuka».
- FR13 nevner ikke «flat eller fallende trend: ingen unntak» fra R2. Det er dekket indirekte av FR12, men bør nevnes, fordi det er nettopp dette T6 tester.
- M1 er målt ved SK2 (minst 25 %), men ingen FR eller NFR gjør 25 % til et akseptkrav. FR27 og FR28 bare rapporterer tallet. Det bør avklares om resultatet av backtesten er et krav eller et funn. Briefen sier at «appens egen backtest er den som avgjør».
- FR25 setter analyseuka til «siste uke i fila». Er den siste raden tom, kan resultatet bli «ingen ny telling» med en gang. Vurder å bruke «siste uke med telling».
