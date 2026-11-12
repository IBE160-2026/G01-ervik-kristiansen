# Tilbakemelding på PRD

| | |
|---|---|
| **Gruppe** | G01 – G01-ervik-kristiansen |
| **PRD vurdert** | `_bmad-output/planning-artifacts/prds/prd-Marin-2026-11-02/prd.md` (status: final, sist endret 2026-11-11, commit 536e09f) |
| **Dato** | 2026-11-12 |
| **Type** | Formativ tilbakemelding, ikke karakter |

## 1. Samlet inntrykk

Dette er en sterk PRD med tydelig tese (forvarsel før lusegrensen brytes), sporing fra brief til krav og uvanlig ærlig omtale av risiko. Hovedrisikoen er at kravene er lette å lese men vanskelige å teste ferdig: reglene og fasiten bor i briefen, og detaljsiden, som er det brukeren faktisk ser, har ingen testbare konsekvenser ennå.

## 2. Dette fungerer godt

- **Sporing og ID-er.** Hver FR/NFR har en «Sporing»-kolonne, og § 10 viser hvilke krav som dekker R1–R5, T1–T12 og SK1–SK5. Epics, stories og tester kan vise direkte til kravene.
- **Ærlighet om det som kan gå galt.** § 11: «Mange røde varsler er altså falske alarmer. Det er et legitimt funn, og FR19 sørger for at brukeren får vite det.» FR27a: «Parameterne justeres ikke for å nå terskelen.» Det er en egen beslutning, ikke pynt.
- **Kontroll på KI-arbeidet.** NFR3 (uavhengig fasit fra kolonnen `Lusegrense uke`, 0 avvik), NFR7 (ingen KI i appen), NFR10 (konkret liste over hva som testes automatisk) og § 11 (fasit regnes for hånd før regelkoden skrives). FR24 er et godt eksempel på et krav som kan bli testtilfeller direkte: én feiltype per rad.

## 3. Oversikt per dimensjon

| Dimensjon | Vurdering | Kort begrunnelse |
|---|---|---|
| Beslutningsklarhet – er valg og avveininger synlige? | sterk | Datert avgjorte punkter (A1, A2), bevisste tillegg utenfor briefen og valget om ingen terskel for falske alarmer er skrevet ut. |
| Substans – er innholdet fortjent, eller «pynt»? | sterk | Krav og NFR-er har produktspesifikke tall (vindu 5 uker, horisont 6 uker, 2 sekunder). Ingen pynte-personas. |
| Strategisk sammenheng – har PRD-en en tese som funksjonene tjener? | god | Tesen er klar, men suksessmålet måler bare treffandel, mens det som kan velte tesen (falske alarmer) ikke har noe mål. |
| Testbarhet – vet man når hvert FR er ferdig? | god | Beregningen er godt dekket av T1–T12 og NFR10. FR-ene for detaljsiden og analyseuke-visning mangler testbare konsekvenser. |
| Scope og avgrensning – er utelatelser eksplisitte? | god | Tydelig «Ute av v1» og prioritert rekkefølge. Kuttlinjen for opplasting er uklar, og FR21 er mer omfattende enn det trengs. |
| Brukbarhet for neste fase – kan UX, arkitektur og stories hente fra den? | god | Rene ID-er, men reglene må hentes fra briefen, og noen sentrale begreper mangler i ordlista. |
| Formtilpasning – passer PRD-formen produktet? | sterk | Tabeller med FR/NFR passer et lite verktøy med én brukertype. Brukerreisene er korte og nyttige. |

## 4. Viktigste forbedringer

### 4.1 Detaljsidens krav har ingen testbare konsekvenser
- **Alvorlighet:** høy
- **Hvor:** § 5.3 og § 5.5, f.eks. FR9 «Detaljsiden viser tydelig hvilken uke prognosen er regnet fra», FR15–FR17; NFR10: «Detaljsiden (FR15–FR20a) kontrolleres manuelt etter en sjekkliste i README.»
- **Problem og hvorfor det betyr noe:** Beregningen er godt sikret, men det brukeren ser (status, graf, tabell, tekster) hviler på ord som «tydelig» og på en sjekkliste som ikke finnes ennå. Da kan en story bli «ferdig» uten at noen kan si hva ferdig er, og Claude Code får ikke noe å bygge mot.
- **Forslag:** Gi hvert FR to–tre konsekvenser med konkrete verdier, og la sjekklisten i README bli en kopi av dem. Eksempel:
  > **FR9** Detaljsiden viser teksten «Prognose regnet fra uke {uke}, {år}» over statusboksen. Konsekvenser: (1) Velges 2026 uke 30, står «uke 30, 2026». (2) Byttes analyseuke til uke 25, endres teksten, grafen og tabellen (FR17) samtidig. (3) Teksten vises også ved grå status.

  Tilsvarende for FR8: «Gitt et anlegg med tellinger i uke 14–18 og en ekstra telling i uke 25: prognosen med analyseuke 20 er identisk med prognosen når uke 25-tellingen fjernes.» Det er også en ferdig testidé for NFR10.

### 4.2 PRD-en er ikke selvstendig: reglene og fasiten bor i briefen
- **Alvorlighet:** medium
- **Hvor:** § 1 «PRD-en gjentar ikke reglene. Den viser til dem med ID»; FR10–FR14 viser bare til «R1», «R2», «R4».
- **Problem og hvorfor det betyr noe:** UX, arkitektur og stories må åpne to dokumenter for å forstå ett krav. Briefen er allerede endret etter at PRD-en startet (§ 12: «Ført inn i R2, R4 og T10 i briefen»), så det er uklart hvilken versjon som gjelder. FR27a gjengir dessuten «rød ved 0–3 uker», mens FR14 bare viser til R4. Det gir to steder å holde i takt.
- **Forslag:** Legg inn én setning i § 1: «Briefen i commit {hash} er normativ for R1–R5 og T1–T12; endres den, oppdateres PRD-en samme dag.» Gjerne også en kort tabell (fem–seks linjer) med grense, vindu, horisont og fargeterskler, slik at FR-ene kan leses alene.

### 4.3 Suksessmålet måler bare treff, ikke falske alarmer
- **Alvorlighet:** medium
- **Hvor:** § 2 M1 «SK2 (backtest, minst 25 % treff)»; § 11 «bare omtrent 14 % av de røde varslene ble fulgt av brudd. … V1 har bevisst ingen terskel for andelen falske alarmer».
- **Problem og hvorfor det betyr noe:** Tesen er at brukeren får et nyttig forvarsel. Hvis åtte av ni røde varsler er falske, er produktet dårlig som varsel selv om M1 oppfylles. Valget om ingen terskel er forsvarlig, men det står ingen plan for hva dere gjør med resultatet.
- **Forslag:** Legg til et motmål, f.eks.: «M1-C: Andel røde varsler fulgt av brudd innen 4 uker rapporteres ved siden av treffandelen og vises i FR19. Er den under {X} % i den endelige backtesten, omformuleres FR19 og § 1 slik at Marin presenteres som en tidlig indikator, ikke som et pålitelig varsel.» Da er reaksjonen bestemt før tallet er kjent.

### 4.4 Uklar kuttlinje og tung FR21
- **Alvorlighet:** medium
- **Hvor:** § 9 «Med i v1: alt i kap. 5 og 6» mot «Opplasting … Kuttes først ved tidsnød»; FR21 (to CSV-formater, to tegnkoder, norsk og engelsk desimaltegn).
- **Problem og hvorfor det betyr noe:** Er opplasting «med i v1» eller ikke? Uten svar blir det en diskusjon midt i et sprint, og J3 med 6 FR-er har mest uvante detaljer for nybegynnere.
- **Forslag:** Definer minimum: «V1 er ferdig når prioritet 1 og 2 er ferdig og testet. Opplasting er et tillegg.» Del FR21 slik at ett format (f.eks. Excel fra BarentsWatch, FR22) kommer først, og at semikolon/Windows-1252-støtte er et eget krav «FR21b» som kan kuttes alene.

### 4.5 Ordlista og brukerreisene mangler noen ledd
- **Alvorlighet:** lav
- **Hvor:** § 1 Ordliste; § 4.
- **Problem og hvorfor det betyr noe:** Begrepene «område», «brudd nå», «treffandel», «detaljside» og «estimat» brukes i FR-ene, men er ikke i ordlista. «Varsel» (FR19) og «status» (FR14) brukes om nær det samme. J1–J3 har bare «brukeren», og J1 henvises ikke til fra noe FR.
- **Forslag:** Legg til fire–fem linjer i ordlista og velg ett av «varsel» og «status». Gi J1–J3 en kort kontekst («Driftsleder ved et anlegg i Vestland, mandag morgen …») og knytt J1 til FR4–FR6 og FR15–FR18.

## 5. Mekaniske funn

- FR1–FR29 er sammenhengende (med FR20a, FR23a og FR27a), M1–M4 og J1–J3 er unike. Ingen brutte krysshenvisninger i FR-tabellene.
- FR29 og «Beslutning 2026-11-03» i sporingskolonnen har ingen kilde i PRD-en. «Tilbakemelding» (FR26, NFR6, NFR9, NFR10) bør si hvilken, og «Hva gjør dette annerledes» (FR19) er en brief-seksjon som ikke finnes i PRD-en.
- A1–A4 deler nummerering med briefen uten at det står. Det gjør «A4» tvetydig i § 11 og § 12.
- Ingen `[ASSUMPTION]`-tagger; antakelser står i § 11 og § 12. Det fungerer, men § 11 og § 12 bør oppgi hvem som eier hver antakelse.
- `status: final` stemmer dårlig med at A4 og backtest-tallene i § 11 fortsatt er åpne. `draft` eller «final med åpne punkter» er mer ærlig.

## 6. Før dere går videre

**Må avklares før epics (og helst før UX):**
- A4: håndkontroll av fasit for T5, T6, T8 og T10–T12. Dette er hele kontrollen mot KI-feil i regelkoden.
- Kjør backtesten (FR27) tidlig, ikke som siste steg i § 13. Tallene avgjør om M1 og FR19 holder, og dermed hva story-ene skal bygge.
- Bestem kuttlinjen for opplasting (4.4) og skriv testbare konsekvenser for detaljsiden (4.1), slik at UX-skissene har noe å måles mot.

**Kan vente:** valg av stack og arbeidsdeling (A3, arkitektursteget), skisser av skjermbildene, samlet oversikt som neste versjon.

**Oppfølging av briefen:** ja. Suksesskriteriene er gjort sjekkbare (SK1–SK5, T1–T12, 25 % backtest), reglene er skrevet ut, datagrunnlaget ligger i repoet (FR1, NFR11), backtest og opplasting er tatt inn, temperatur er utsatt (R5), og håndkontroll av fasit er planlagt.

## 7. Refleksjonsspørsmål

1. Dere skriver at bare omtrent 14 % av røde varsler ble fulgt av brudd. Hvem ville stolt på et slikt varsel, og hva ville dere endre i selve produktet (ikke bare i FR19-teksten) hvis den endelige backtesten gir samme tall?
2. Hvordan kontrollerte dere at PRD-utkastet fra KI faktisk gjengir reglene i briefen riktig, og hvilke krav endret dere etter at dere regnet fasiten for hånd?

_Vurdert mot kvalitetsrubrikken i bmad-prd. Dette er veiledning, ikke sensur._
