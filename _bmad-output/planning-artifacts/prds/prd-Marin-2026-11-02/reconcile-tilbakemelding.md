# Avstemming: tilbakemelding på product brief mot PRD

| | |
|---|---|
| **Kilde** | `briefs/brief-Marin-2026-09-17/tilbakemelding-product-brief.md` (faglærer IBE160, 2026-10-06) |
| **PRD** | `prds/prd-Marin-2026-11-02/prd.md` (status draft, `updated: 2026-11-03`) |
| **Også lest** | `briefs/brief-Marin-2026-09-17/brief.md` (R1–R6, T1–T10, SK1–SK5), fordi PRD-en viser til reglene i stedet for å gjenta dem |
| **Dato for avstemming** | 2026-11-11 |

Status: **dekket** = PRD (eller briefen den viser til) svarer fullt ut, **delvis** = noe mangler eller er bare implisitt, **mangler** = ikke behandlet. **Motstrid** markeres der PRD-en går mot tilbakemeldingen eller mot seg selv.

## Sammendrag

De tre viktigste endringene faglærer ba om (sjekkbare suksesskriterier, presise regler, avklart datagrunnlag) er godt fulgt opp. Briefen er oppdatert med R1–R6, T1–T10 og SK1–SK5, og PRD-en sporer til dem (kap. 10). Hullene ligger i de kvalitative forventningene som FR-strukturen lett mister:

1. **Ærlighet om falske alarmer (motstrid):** kap. 11 sier at FR19 sørger for at brukeren får vite at mange røde varsler er falske alarmer. FR19 krever bare at treffandelen vises.
2. **Testbarhet utover reglene:** NFR2 dekker bare T1–T10. Søk, opplasting/validering (FR21–FR26), analyseuke (FR7–FR9) og backtest-skriptet (FR27–FR28) har ingen testkrav eller akseptansekriterier.
3. **README og dataopphav:** faglærer ba om at README beskriver hvor dataene kommer fra og hvordan de er hentet. Ingen FR/NFR krever det.
4. **Kjerneflyt først:** faglærer ba om at kjerneflyten blir ferdig og stabil før mer legges til. PRD-en har ingen prioritering eller rekkefølge, og opplasting (FR21–FR26) står likt med kjerneflyten.
5. **KI-styring i prosessen (30 % av del 1):** PRD-en beskriver kontroll av regelkoden (kap. 11), men ikke hvordan gruppen styrer og etterprøver Claude Codes arbeid ellers, eller sporing fra krav til test og kode.

## Gjennomgang per tilbakemeldingspunkt

### A. De viktigste endringene

| # | Tilbakemelding | Status | PRD-plassering | Foreslått tiltak | Alvor |
|---|---|---|---|---|---|
| A1 | Suksesskriteriene må bli testbare (eks. «gitt testdatasett X varsler appen i uke 14 når grensen krysses i uke 16») | Dekket | Kap. 2 (M1–M4 → SK1–SK5), kap. 10, NFR2; T6 i briefen er nøyaktig eksempelet faglærer ga | Ingen for reglene. Se C3 for testbarhet av resten av appen. | Lav |
| A2 | Reglene må skrives ut presist (grense per område og uke, antall uker historikk, terskler for grønn/gul/rød) | Dekket | Briefen R1–R4; PRD FR10–FR14 og kap. 1 viser til dem | PRD-en gjentar ikke reglene, bevisst. Det er greit så lenge briefen er eneste kilde. Legg inn en setning om at endringer i R1–R6 skal føres i briefen, og at PRD/tester følger etter. | Lav |
| A3 | Avklar datagrunnlaget (utdrag eller syntetisk), plassering i repoet, lukk [ANTAGELSE] | Dekket | FR1, kap. 7, NFR1, NFR9; ingen [ANTAGELSE] igjen i briefen | — | Lav |

### B. Vanskelighetsgrad og gjennomførbarhet

| # | Tilbakemelding | Status | PRD-plassering | Foreslått tiltak | Alvor |
|---|---|---|---|---|---|
| B1 | Temperatur og sesong er nevnt som datakilde uten at bruken er beskrevet | Dekket | R5, kap. 7 (temperatur brukes ikke), kap. 9 | — | Lav |
| B2 | «Prediksjon» er statistikk, ikke KI. Vær bevisst på ordbruken | Dekket | NFR7; PRD bruker konsekvent «prognose» og «trendberegning» | Briefen bruker fortsatt «prediksjon/prediktivt» noen steder (Hva gjør dette annerledes, Omfang). Vurder å samkjøre ordbruken. | Lav |
| B3 | Filhåndtering: avklar format og om brukeren skal kunne laste opp egne data | Dekket | FR21–FR26, kap. 7 (CSV-eksempel), J3 | — | Lav |
| B4 | Få kjerneflyten (velg anlegg → trend → prognose → status) ferdig og stabil med kjente testdata før mer legges til | Delvis | J1, FR4–FR20 beskriver kjerneflyten, men ingen prioritet eller rekkefølge | Merk FR-ene med prioritet (f.eks. «kjerne»: FR1–FR20, NFR1–NFR5; «utvidelse»: FR21–FR26) og si i kap. 13 at epics bygges i den rekkefølgen. | Middels |
| B5 | Kontroll på KI-ens arbeid: lag små eksempler med fasit som gruppen regner ut selv | Dekket | Kap. 11 (Kontroll på KI-ens arbeid), R6 («regnes ut av gruppen for hånd, ikke av KI»), NFR3 (uavhengig fasit mot `Lusegrense uke`) | — | Lav |
| B6 | Testbarhet: grenser og terskler egner seg for tester når de er skrevet som regler | Dekket | NFR2, NFR3, T1–T10 | — | Lav |
| B7 | Kjørbar for sensor: «Sørg for at dette står i PRD og README» | Dekket | NFR1, M4, SK5 | — | Lav |
| B8 | Avhengigheter og kostnader: ingen betalte tjenester | Dekket | NFR1 (ingen API-nøkler, betalte kontoer eller nettilgang) | — | Lav |
| B9 | Kom raskt i gang med PRD | Dekket | PRD finnes (2026-11-03) | — | Lav |
| B10 | Forslag 1: del prognosen i to trinn, temperatur/sesong som neste trinn | Dekket | R5, kap. 9 | — | Lav |
| B11 | Forslag 2a: backtest «som egen funksjon» som gjør treffsikkerhet målbar og løfter verdien av appen | Delvis (bevisst avvik) | FR27–FR29: backtest bare som skript, ikke side i appen (beslutning 2026-11-03). J2/FR7–FR9 lar brukeren se historiske varsler for ett anlegg. | Avviket er forsvarlig, men begrunnelsen står ikke i PRD-en. Skriv én setning i kap. 9 om hvorfor (omfang) og at J2 + FR19 gir brukeren innsyn i treffsikkerheten. | Lav |
| B12 | Forslag 2b: side der brukeren kan legge inn eller laste opp egne lusetall | Dekket | FR21–FR26, J3, skjermbilde 3 | — | Lav |

### C. Gjennomgang av briefens deler og kriteriene for del 1

| # | Tilbakemelding | Status | PRD-plassering | Foreslått tiltak | Alvor |
|---|---|---|---|---|---|
| C1 | The Solution: beskriv kjerneflyten i 3–5 steg | Dekket | Kap. 4 J1 (4 steg), J2, J3 | — | Lav |
| C2 | Who This Serves: ett eller flere anlegg? | Dekket | Kap. 3 (ett anlegg; regionledere ute av v1) | — | Lav |
| C3 | Kvalitetssikring og testing (15 %): funksjoner konkrete nok til å bli testtilfeller | Delvis | NFR2 og NFR3 dekker bare reglene (T1–T10, R1). FR4–FR9, FR15–FR28 har ingen testkrav eller akseptansekriterier. | Legg til en NFR om at hver FR får minst ett automatisk test- eller akseptansekriterium, og konkretiser de mest feilutsatte: FR24 (en ugyldig fil per feiltype, med forventet melding og radnummer), FR8 (data etter analyseuka påvirker ikke prognosen), FR28 (backtest-skriptet på et lite kjent datasett gir kjent treffandel). | Høy |
| C4 | What Makes This Different: ærlig om at treffsikkerheten ikke er validert | Delvis, **motstrid** | FR19 (fast tekst + treffandel), kap. 11 (29 % treff, bare ca. 14 % av røde varsler fulgt av brudd) | Kap. 11 lover at FR19 forteller brukeren at mange røde varsler er falske alarmer, men FR19 krever bare treffandelen. Utvid FR19 til også å vise andelen røde varsler som ikke ble fulgt av brudd (tallet FR28 allerede rapporterer), og angi teksten eller minst innholdet i den. | Høy |
| C5 | Scope: ett område eller hele kysten? | Delvis (implisitt) | FR1 (hele utdraget), FR3/R1 (sør/nord) | Skriv eksplisitt i kap. 9 at v1 dekker alle lokaliteter langs hele kysten i utdraget. | Lav |
| C6 | Prosess og KI-styring (30 %): krav skal kunne spores fra brief til kode | Delvis | Kap. 10 sporer brief → FR/NFR; kap. 13 sier at stories viser til FR/NFR-ID-er; kap. 11 om fasit i T1–T10 | PRD-en sier ikke hvordan gruppen styrer og etterprøver Claude Code utover regelkoden (gjennomgang av kode, krav-ID i commit/story, sesjonslogg). Legg til et kort avsnitt eller NFR om sporing FR → story → test → commit, og om at KI-generert kode gjennomgås av gruppen. | Middels |
| C7 | Funksjonalitet og omfang (20 %): ren visning kan bli tynn; backtest og egen dataregistrering gir mer å vise | Dekket | J2/FR7–FR9 (historisk analyseuke), FR21–FR26 (opplasting), FR27–FR28 (backtest-skript) | — | Lav |
| C8 | Design (10 %): skisser oversikt over anlegg og detaljsiden | Delvis, **avvik** | Kap. 8 lister tre skjermbilder; skisser er utsatt til arkitektur/UX. Samlet oversikt over anlegg er tatt ut (kap. 3, kap. 9), mens briefens Omfang fortsatt har «Dashboard som viser status ... per anlegg». | Bekreft at søk + detaljside erstatter oversikten, og oppdater briefens Omfang slik at brief og PRD er enige. Lag skissene før stories skrives. | Middels |
| C9 | Statusfarger må forstås uten fargesyn | Dekket | NFR4, FR15, R4 | — | Lav |
| C10 | Brukeren har ikke datafaglig bakgrunn (nivå på tekst og forklaringer) | Delvis | M3, NFR5, FR20 (forklaring ved grå status) | Kvalitativ forventning som ikke er testbar slik den står. Legg inn et sjekkbart kriterium, f.eks. at alle statustekster og feilmeldinger (FR24) er på norsk uten fagtermer som «regresjon» eller «stigningstall», eller en enkel brukertest med én person utenfor gruppen. | Lav |
| C11 | Kodekvalitet og arkitektur (10 %): velg en enkel stakk og begrunn den | Delvis (utsatt) | Kap. 12 A3, kap. 13 punkt 2 | Riktig å utsette til arkitektursteget. Ingen endring i PRD-en nødvendig. | Lav |
| C12 | README og kjørbarhet (10 %): beskriv i README hvor dataene kommer fra og hvordan de er hentet | Delvis | NFR1 (kjøres etter README), NFR2 (testkommando i README); nedlastingsdato bare i kap. 11 | Legg til en NFR: README beskriver datakilden (BarentsWatch, lisens NLOD), nedlastingsdato 27.10.2026, hvilke filer og uker som brukes, og hvordan utdraget ble hentet. | Middels |
| C13 | Ryddighet i repoet (5 %): fast mappe for datasett og testdata, API-nøkler ute av repoet | Delvis | NFR9 (`data/`, «egen testmappe», ingen hemmeligheter) | Navngi testmappen, og angi hvor resultatfila fra backtesten skal ligge (FR28 sier bare «en fil i repoet»). Siden FR19 leser denne fila: si om den er committet, og hva detaljsiden viser hvis den mangler. | Lav |
| C14 | Sikkerhet og personvern: lusetall er offentlige data, ingen personopplysninger | Dekket | NFR6, FR26 (opplastede data lagres ikke) | — | Lav |

### D. Neste steg fra faglærer

| # | Tilbakemelding | Status | PRD-plassering | Foreslått tiltak | Alvor |
|---|---|---|---|---|---|
| D1 | 4–6 sjekkbare suksesskriterier, blant annet treffsikkerhet mot historiske data | Dekket | SK1–SK5 (5 stk.), SK2 = backtest med 25 % terskel | Terskelen er satt etter en foreløpig backtest (29 %). Briefen sier det åpent, og det bør stå i kap. 11 i PRD-en også, så det ikke ser ut som et mål valgt for å bli nådd. | Lav |
| D2 | Skriv ut reglene, og lag 2–3 små eksempler med fasit | Dekket | R1–R6, T1–T10 (10 eksempler) | — | Lav |
| D3 | Bestem datagrunnlaget, legg det i repoet, gå videre til PRD | Dekket | FR1, kap. 7 | — | Lav |
| D4 | Oppdater briefen i repoet så historikken viser hvordan planen utviklet seg | Dekket (utenfor PRD) | Briefen er oppdatert med R1–R6, T1–T10, SK1–SK5 | PRD-en har selv utdatert metadata: `updated: 2026-11-03` selv om A1/A2 ble avgjort 2026-11-11, og kap. 13 punkt 1 («Lukke A1 og A2») står fortsatt selv om begge er lukket. Oppdater frontmatter og kap. 13. | Lav |

## Kvalitative forventninger som FR-strukturen kan miste

| Forventning | Hvor det står i tilbakemeldingen | Hvordan PRD-en fanger det | Risiko |
|---|---|---|---|
| Ærlighet om usikkerhet og falske alarmer | «What Makes This Different – ærlig» | FR19 + kap. 11, men FR19 dekker ikke falske alarmer (C4) | Høy: kan forsvinne i implementeringen fordi bare treffandelen er krav |
| Testbarhet for hele appen, ikke bare reglene | Kriterium 3 (15 %) | NFR2/NFR3 bare for regler (C3) | Høy |
| KI-styring og sporbarhet fra plan til kode | Kriterium 1 (30 %), «Kontroll på KI-ens arbeid» | Kap. 10–11, kap. 13 (C6) | Middels |
| Kjerneflyt ferdig og stabil før utvidelser | «Hva vanskelighetsgraden betyr» | Ikke prioritert (B4) | Middels |
| README med dataopphav | Kriterium 6 | Ikke krav (C12) | Middels |
| Ordbruk: statistikk, ikke KI | KI-funksjonalitet i appen | NFR7 (B2) | Lav |
| Språknivå for bruker uten datafaglig bakgrunn | Kriterium 4 | M3, NFR5, FR20, men ikke sjekkbart (C10) | Lav |
| Personvern | Sikkerhet og personvern | NFR6, FR26 | Lav |
| Repo-hygiene | Kriterium 7 | NFR9, men testmappe og backtest-fil er ikke navngitt (C13) | Lav |

## Motstrid og avvik

1. **Kap. 11 mot FR19 (høy):** kap. 11 sier at FR19 sørger for at brukeren får vite at mange røde varsler er falske alarmer. FR19 krever bare treffandelen.
2. **Samlet oversikt over anlegg (middels):** faglærer ba om skisse av «oversikt over anlegg», og briefens Omfang har «Dashboard som viser status ... per anlegg». PRD-en tar oversikten ut av v1 (kap. 3, kap. 9). Avviket er bevisst, men briefen er ikke oppdatert tilsvarende.
3. **Backtest som funksjon i appen (lav):** faglærer foreslo backtest som egen funksjon. PRD-en har den bare som skript (FR29). Avviket er bevisst, men begrunnelsen står ikke.
4. **Utdatert status i PRD-en (lav):** frontmatter `updated: 2026-11-03` og kap. 13 punkt 1 «Lukke A1 og A2» står fortsatt, selv om kap. 12 viser at begge ble avgjort 2026-11-11.
