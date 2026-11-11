---
title: "Avstemming: addendum mot PRD"
created: 2026-11-11
input: briefs/brief-Marin-2026-09-17/addendum.md (oppdatert 2026-10-29)
prd: prds/prd-Marin-2026-11-02/prd.md (oppdatert 2026-11-03, med A1/A2 avgjort 2026-11-11)
---

# Avstemming: addendum mot PRD

Gjennomgang av beslutninger, datafakta, begrensninger, åpne spørsmål og risikoer i addendumet som PRD-en dropper uten å si det, motsier eller lar stå uløst. Briefen er bare brukt for å slå opp regel-ID-er (R1–R6, T1–T10, SK1–SK5).

Alvorlighetsgrad: **høy** = kan gi feil krav, feil måling eller en påstand som ikke holder; **middels** = hull som bør lukkes før arkitektur/stories; **lav** = presisering eller sporbarhet.

## Oppsummering

| # | Gap | Alvor |
|---|---|---|
| G1 | Backtesttallene (35 % / 28–29 % / 14 %) er fra før A1 og gjelder ikke lenger uten videre | Høy |
| G2 | PRD-en sier at fasiten i T1–T10 er regnet for hånd, mens addendumet sier at T5, T6 og T8 fortsatt mangler håndregnet fasit | Høy |
| G3 | Kryssings-definisjonen i SK2 ser bort fra brudd etter en uke uten telling, og PRD-en sier ikke om «uka før» er ISO-uke eller forrige telte uke | Høy |
| G4 | Ingen plan for hva som skjer om appens backtest gir under 25 % | Middels |
| G5 | «Røde varsler som ikke ble fulgt av brudd» er ikke definert (unntak for «brudd nå», telleenhet) | Middels |
| G6 | Åpent spørsmål 1 (vurderingskriterier for leveransen) er ikke ført inn i PRD §12 | Middels |
| G7 | Åpenhetskravet om at X ble satt etter skissen, er borte fra PRD-en | Middels |
| G8 | «oppdretter»-prosjektet og posisjoneringen prediktiv vs. observasjon/aggregering er ikke nevnt i PRD-en | Middels |
| G9 | Lokaliteter uten tellinger og brakklagte anlegg (`Trolig uten fisk`, lange hull) er ikke håndtert i søk/detaljside | Middels |
| G10 | Backtestens nevner: kryssinger tidlig i 2025 kan ikke få treff (mangler historikk) | Lav |
| G11 | Kryssinger som skyldes at vårgrensen slår inn, rapporteres ikke separat | Lav |
| G12 | FR19 viser bare treffandel, ikke andelen falske alarmer | Lav/middels |
| G13 | `Over lusegrense uke` og «Har telt lakselus» er ikke brukt som fasit i tester | Lav |

---

## G1 Backtesttallene er fra før A1 — høy

- **Addendum:** «Grov backtest av R2–R4 som de står» (35 % tolkning A, 28 % tolkning B, 14 % av 4 774 røde varsler fulgt av brudd) og tabellen under «Beslutninger etter analysen» (27,9 / 28,4 / 28,8 % treff). Addendumet sier selv at skissen er «en grov skisse av R2–R4, ikke appens implementasjon».
- **PRD:** §11 «Treffsikkerhet» sier «omtrent 29 % treff» og «omtrent 14 %» som om tallene gjelder appen. M1 og SK2-målet (25 %) bygger på margin til disse tallene.
- **Hvorfor det betyr noe:** Skissen ble kjørt før A1 (2026-11-11) endret hva t er. Nå gir siste telling eldre enn uka før analyseuka grå «ingen ny telling». Det fjerner røde uker som skissen talte med, særlig ved telling annenhver uke under 4 °C (uke 6–13, rett før vårgrensen). Treffandelen kan dermed falle, og marginen til 25 % (ca. 4 prosentpoeng) er liten. 35 %-tallet (tolkning A) er i tillegg ikke den tolkningen SK2 bruker.
- **Forslag:** Skriv i §11 at tallene er fra skissen 2026-10-29, tolkning B, R2 med 3 av 5, *før* A1, og at de må regnes på nytt med FR27 før X vurderes. Nevn ikke 35 % som forventning. Legg til at A1 kan senke treffandelen.

## G2 Håndregnet fasit for T5, T6 og T8 — høy

- **Addendum:** Åpent spørsmål 7 «Delvis avklart»: inndata for T5, T6 og T8 er valgt med KI-støtte, og «fasiten for T5, T6 og T8 skal fortsatt regnes ut for hånd av gruppen».
- **PRD:** §11 «Kontroll på KI-ens arbeid»: «Fasiten i T1–T10 er regnet ut for hånd av gruppen og er kontrollen.» M2/NFR2 bygger på dette.
- **Hvorfor det betyr noe:** PRD-en påstår at kontrollen er på plass, mens kilden sier at den ikke er det for tre av testene (og T9/T10 kom til senere, ved R2-endringen og A1). Hvis fasiten er laget av samme KI som skriver regelkoden, er den ikke en uavhengig kontroll.
- **Forslag:** Bekreft at gruppen har regnet T5, T6, T8, T9 og T10 for hånd, og noter dato. Hvis ikke: flytt det til §12 som åpent punkt (f.eks. A4) og gjør §11 betinget («skal regnes ut for hånd før …»).

## G3 Kryssings-definisjonen og uker uten telling — høy

- **Addendum:** «Grensekryssinger»: «26 brudd kommer etter en uke uten telling og regnes ikke som kryssing med dagens definisjon.» «Telle-hyppighet»: telling hver 14. dag under 4 °C er lovlig.
- **PRD:** FR27 viser bare til «definisjonen i SK2». SK2 sier «uka før var under». PRD-en sier ikke om «uka før» betyr forrige ISO-uke (som da må ha telling) eller forrige uke med telling.
- **Hvorfor det betyr noe:** Med A1 er telling annenhver uke uttrykkelig en normal situasjon. Hvis «uka før» krever telling i ISO-uka rett før, faller brudd hos anlegg som teller annenhver uke systematisk ut av nevneren — akkurat i perioden før vårgrensen. To implementasjoner av FR27 kan gi ulike tall.
- **Forslag:** Presiser i FR27 (og helst SK2): «uka før» = forrige uke med telling, høyst én uke tidligere (samme logikk som A1), eller bevisst «forrige ISO-uke med telling». Rapporter antall brudd som ble utelatt av denne grunnen (jf. 26 i skissen).

## G4 Ingen plan om backtesten gir under 25 % — middels

- **Addendum:** «Lav treffsikkerhet er et legitimt funn å rapportere.» «Prognosemetode»: mer avansert tidsseriemodell er naturlig retning hvis treffsikkerheten ikke holder.
- **PRD:** §11 kaller lav treffsikkerhet et legitimt funn, men sier ikke hva som skjer om SK2 ikke nås (M1 feiler). SK2 i briefen sier at appens egen backtest avgjør.
- **Hvorfor det betyr noe:** Med liten margin og A1 (G1) er det reelt mulig at SK2 ikke nås. Uten avklaring blir det fristende å justere X eller definisjonen i etterkant.
- **Forslag:** Legg til i §11: hvis FR27 gir under 25 %, endres ikke X eller treffdefinisjonen; resultatet rapporteres i refleksjonsrapporten som funn, med mer avansert modell/R5 som neste steg.

## G5 Definisjon av «røde varsler som ikke ble fulgt av brudd» — middels

- **Addendum:** «Av 4 774 røde *prognosevarsler (ikke 'brudd nå')* ble 14 % fulgt av brudd innen 4 uker.»
- **PRD:** FR28: «andelen røde varsler som ikke ble fulgt av brudd innen 4 uker». Unntaket for rød «brudd nå» (R4) er ikke med, og det står ikke om enheten er anleggsuke med rød status eller sammenhengende rød periode.
- **Hvorfor det betyr noe:** Tar man med «brudd nå», blir tallet et annet og ikke sammenlignbart med skissen. Telles hver røde uke, blir en lang rød periode mange «falske alarmer».
- **Forslag:** Presiser i FR28: nevneren er anleggsuker med rød prognosestatus (ikke «brudd nå»); «brudd» = målt verdi ≥ grensen i en av de 4 neste ukene.

## G6 Åpent spørsmål 1 er ikke ført videre — middels

- **Addendum:** Spørsmål 1 «Delvis avklart»: refleksjonsrapport-mal finnes, men krav til omfang/vurderingskriterier for selve produktleveransen er ikke kartlagt.
- **PRD:** §12 har bare A1–A3. Spørsmålet er verken besvart eller ført inn.
- **Hvorfor det betyr noe:** Vurderingskriteriene for IBE160 kan påvirke omfang (§9), M4/SK5 og hva som må med i README og rapport.
- **Forslag:** Legg til A4 i §12: «Kartlegge vurderingskriterier for produktleveransen i IBE160», med eier og frist før epics.

## G7 Åpenhet om at X ble satt etter skissen — middels

- **Addendum:** Beslutning 3: «X er satt etter denne skissen, og det skal stå i refleksjonsrapporten.»
- **PRD:** M1 sier bare «minst 25 % treff». Ingen omtale av at X ble satt etter skissen, eller av at det skal stå i refleksjonsrapporten.
- **Hvorfor det betyr noe:** Det er en uttrykkelig forpliktelse som lett glemmes når PRD-en blir hoveddokumentet.
- **Forslag:** Legg til en setning i §11 «Treffsikkerhet» (eller som oppgave i §13): X = 25 % ble satt etter skissen 2026-10-29, og det skal stå i refleksjonsrapporten.

## G8 Posisjonering: prediktiv vs. observasjon/aggregering — middels

- **Addendum:** «Beslektet/eksisterende verktøy»: Dr-grimen/oppdretter er «et observasjons-/aggregeringsverktøy for nåværende status, ikke en prediktiv modell», og «bør ses nærmere på før PRD/arkitektur». «Prognosemetode» begrunner v1 med verdien av «et prediktivt varsel kontra observasjonsverktøyene».
- **PRD:** §1 sier «forvarsel», og FR19 sporer til «Hva gjør dette annerledes», men PRD-en nevner verken oppdretter, BarentsWatch som observasjonsverktøy eller om gjennomgangen av oppdretter er gjort.
- **Hvorfor det betyr noe:** PRD-ens hele mål (M1) er differensieringen «prognose, ikke øyeblikksbilde». Med ca. 14 % presisjon er den prediktive verdien svak, og PRD-en bør være ærlig om at fordelen er et retningsvalg, ikke en bevist styrke (som briefen sier). Ingen direkte motsigelse, men forutsetningen er stille droppet.
- **Forslag:** Legg til en kort setning i §1 eller §11 om at eksisterende verktøy (BarentsWatch, oppdretter) viser nåsituasjonen, og at Marins prognose er et retningsvalg med usikker treffsikkerhet. Bekreft om oppdretter er gjennomgått, eller før det som oppgave i arkitektursteget.

## G9 Lokaliteter uten tellinger og brakklagte anlegg — middels

- **Addendum:** «Innhold»: 1 092 lokaliteter, bare 927 med minst én telling; én rad per lokalitet per uke også uten rapport; kolonnen `Trolig uten fisk` (ingen rapport på 4+ uker). «Telle-hyppighet»: lange hull (6+ uker, 586 tilfeller) er i praksis brakklegging eller utslakting; telleplikten faller bort ved slakting innen 14 dager.
- **PRD:** FR4/FR5 søker i alle lokaliteter; §7 sier at øvrige kolonner ikke brukes. Ingen krav for de 165 lokalitetene som aldri har telling, eller for brakklagte anlegg.
- **Hvorfor det betyr noe:** Brukeren kan finne et anlegg som aldri har data, og får bare grå «ingen ny telling siden uke …» uten noen uke å vise. Brakklagte anlegg ser ut som manglende rapportering.
- **Forslag:** Bestem enten å utelate lokaliteter uten tellinger fra søket, eller vise «ingen tellinger i datagrunnlaget». Vurder å bruke `Trolig uten fisk` i forklaringsteksten for grå status (FR20), eller noter i §7 at den bevisst ikke brukes.

## G10 Backtestens nevner tidlig i datagrunnlaget — lav

- **Addendum:** 823 kryssinger (814 til og med 2026 uke 42), 616 av dem i 2025.
- **PRD:** FR27 «hele datagrunnlaget». Datagrunnlaget starter 2025 uke 1, så kryssinger i 2025 uke 1–6 har ikke nok historikk til rød status 2–4 uker før.
- **Hvorfor det betyr noe:** Disse kryssingene blir automatisk bom og trekker treffandelen ned, eller utelates av noen implementasjoner og ikke av andre.
- **Forslag:** Presiser i FR27 om kryssinger uten mulig historikk (før ca. 2025 uke 7) tas med i nevneren, og rapporter antallet.

## G11 Kryssinger når vårgrensen slår inn — lav

- **Addendum:** 113 kryssinger i vårperioden, 36 av dem akkurat i uka grensen faller fra 0,5 til 0,2.
- **PRD:** FR28 rapporterer ikke dette separat.
- **Hvorfor det betyr noe:** Disse kryssingene er der R3 (grense per uke, T6) gir verdi. Et eget tall viser om R3 fungerer i praksis, og er nyttig i refleksjonsrapporten.
- **Forslag:** Valgfritt i FR28: rapporter treffandel separat for vårperioden / uka grensen endres.

## G12 FR19 viser bare treffandel — lav/middels

- **Addendum:** De fleste røde varsler er falske alarmer (14 % fulgt av brudd).
- **PRD:** §11 sier at «FR19 sørger for at brukeren får vite det», men FR19 viser bare treffandelen, ikke andelen falske alarmer.
- **Hvorfor det betyr noe:** §11 lover mer enn FR19 leverer. For en driftsleder er «hvor ofte er rødt feil?» minst like viktig som treffandelen.
- **Forslag:** La FR19 også vise andelen røde varsler fulgt av brudd (fra FR28-fila), eller juster formuleringen i §11.

## G13 Ubrukte fasitkolonner — lav

- **Addendum:** BarentsWatch markerer de 49 radene med lusetall lik grensen som «Over lusegrense uke» = «Ja», som bekrefter «≥ grensen er brudd». «Har telt lakselus» = «Ja» samsvarer nøyaktig med at `Voksne hunnlus` har verdi.
- **PRD:** NFR3 bruker bare `Lusegrense uke`. FR2 bruker `Voksne hunnlus` (i samsvar), men ingen av kolonnene er brukt som kontroll.
- **Hvorfor det betyr noe:** Billige ekstra tester for brudd-sammenligningen (≥) og for FR2.
- **Forslag:** Utvid NFR3: test også ≥-regelen mot `Over lusegrense uke` og FR2 mot `Har telt lakselus`. Før kolonnene inn i §7 som «bare fasit i tester».

---

## Dekket uten avvik (kontrollert)

- Datakilde og lokal kopi uten API (FR1, NFR1, §9) — samsvarer med «Valgt for v1» og spørsmål 6.
- Utelatelse av 2026 uke 43–44 (FR1, FR7) — samsvarer med beslutning 2.
- R2 med minst 3 av 5 tellinger og regresjon bare på telte uker (FR11) — samsvarer med beslutning 1.
- Lineær regresjon, 5 uker, horisont 6 (FR11, FR12) — samsvarer med spørsmål 4 og «Prognosemetode».
- Web/dashboard, ikke SMS/e-post/push (§9) — samsvarer med spørsmål 2.
- Teknisk stack og arbeidsdeling (spørsmål 3) — ført videre som A3.
- R1 mot `Lusegrense uke` med 0 avvik (NFR3), og «ukjent område» for de 3 lokalitetene uten fylke (FR3).
- Temperatur og sesongjustering ute av v1 (§9, R5).
- Datakvalitet: fast utdrag lastet ned 27.10.2026 (§11).
