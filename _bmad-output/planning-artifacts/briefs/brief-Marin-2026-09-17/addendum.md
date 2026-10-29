---
title: "Addendum: Marin"
status: draft
created: 2026-09-17
updated: 2026-10-29
---

# Addendum: Marin

Supplerende materiale samlet under utarbeidelsen av brief.md — bakgrunn for videre arbeid (PRD, arkitektur), ikke ment å inngå i selve briefen.

## Regulatorisk grunnlag (research, 2026-09-17)

- **Lakselusforskriften** (FOR-2012-12-05-1140, Lovdata): standardgrense er i gjennomsnitt under 0,5 voksne hunnlus per fisk.
- Om våren gjelder en strengere grense på under 0,2 voksne hunnlus per fisk i snitt — for å skjerme utvandrende vill laksesmolt: uke 16 t.o.m. 21 fra og med Nord-Trøndelag og sørover, og uke 21 t.o.m. 26 i Nordland, Troms og Finnmark (§ 8). Forskriften bruker fortsatt «Nord-Trøndelag», selv om fylket ikke finnes lenger. Reglene appen bruker, står i R1 i brief.md.
- Mattilsynet kan gi dispensasjon for høyere grense for stamfisk siste halvår i sjø, men er ifølge iLaks «svært tilbakeholden» med dette.
- Kilde: [Lovdata — forskrift om bekjempelse av lakselus](https://lovdata.no/dokument/SF/forskrift/2012-12-05-1140), [Mattilsynet — lakselus](https://www.mattilsynet.no/fisk-og-akvakultur/fiskesykdommer/lakselus)

## Datakilder (research, 2026-09-17)

- Oppdrettere rapporterer ukentlige lusetall til Mattilsynet.
- **BarentsWatch Fiskehelse** aggregerer data fra Mattilsynet, Veterinærinstituttet og Fiskeridirektoratet, og viser ukentlig oversikt over lakselus, sykdom og tiltak per anlegg — med historikk tilbake til **2012**.
- Data er tilgjengelig via et **åpent API** (se [barentswatch.no/data](https://www.barentswatch.no/data/?lang=en), [Åpne data (API) via BarentsWatch](https://www.barentswatch.no/en/articles/open-data-via-barentswatch/)), i tillegg til nedlastbare Excel-uttrekk.
- **Valgt for v1 (2026-10-27):** et nedlastet utdrag av historiske lusetall fra BarentsWatch lagres i `data/barentswatch/` i repoet, slik at appen kan kjøres uten API-tilgang og nøkler (se Omfang i brief.md). API-et krever registrering og klientnøkler, og er derfor ute av v1.

## Dataanalyse av BarentsWatch-utdraget (research, 2026-10-29)

Analysen er gjort med KI-støtte (Claude Code) på begge filene i `data/barentswatch/`. Tallene er grunnlag for PRD-en, ikke fasit. Backtesten under er en grov skisse av R2–R4, ikke appens implementasjon.

### Innhold

- 2025 uke 1–52 og 2026 uke 1–44: 102 560 rader, 1 092 lokaliteter, 927 av dem med minst én telling. En rad per lokalitet per uke, også uker uten rapport.
- 54 482 rader har lusetall. «Har telt lakselus» = «Ja» samsvarer nøyaktig med at «Voksne hunnlus» har en verdi.
- Kolonner briefen ikke bruker ennå: `Lusegrense uke`, `Over lusegrense uke`, `Trolig uten fisk` (ingen rapport på 4+ uker), `Sjøtemperatur` (finnes på alle tellinger), `Produksjonsområde`, `Lat`/`Lon`.
- Bare 3 lokaliteter mangler fylke (grense «Ukjent»). R1-regelen om «ukjent område» gjelder altså nesten ingen anlegg.
- **2026 uke 43–44 er ufullstendige:** 436 og 13 tellinger, mot omtrent 600 i en vanlig uke. Utdraget ble lastet ned 27.10. De siste ukene må enten utelates eller håndteres eksplisitt.

### R1 mot BarentsWatch

- R1, regnet ut fra fylke og ISO-uke, gir **samme grense som `Lusegrense uke` i alle rader** (0 avvik). Kolonnen kan brukes som uavhengig fasit i tester av R1.
- I 49 rader er lusetallet nøyaktig lik grensen, og BarentsWatch markerer alle som «Over lusegrense uke» = «Ja». Det stemmer med «≥ grensen er brudd» i R1, selv om kolonnebeskrivelsen deres sier «flere enn».
- Lovdata (kontrollert 2026-10-29, sist endret 2023-12-14) bekrefter grensene og ukene i § 8.

### Telle-hyppighet og «for lite data» (R2)

- Lakselusforskriften § 6: lus skal telles minst hver 7. dag ved 4 °C eller mer, og **minst hver 14. dag under 4 °C**. Telleplikten faller bort om all fisk skal slaktes innen 14 dager.
- Dataene viser dette tydelig. Ved telling under 4 °C er neste telling 2 uker senere i 19 % av tilfellene, mot 0,6 % ved 4 °C eller mer. Temperatur under 4 °C forekommer mest i uke 6–13 (7–12 % av tellingene).
- Med R2 som i dag (alle 5 uker må ha telling) har 86,6 % av telleukene et komplett vindu. Under 4 °C er andelen 72 %. Krav om minst 3 av 5 uker ville gitt 94 %.
- Lange hull (6 uker eller mer, 586 tilfeller) er i praksis brakklegging eller utslakting.

### Grensekryssinger (grunnlag for backtesten)

- Med definisjonen i suksesskriterium 2 (≥ grensen nå, under grensen uka før) finnes det **823 kryssinger ved 428 lokaliteter**: 616 i 2025 og 207 i 2026, 591 i sør og 232 i nord.
- 113 kryssinger skjer i vårperioden (grense 0,2). 36 av dem skjer akkurat i uka grensen faller fra 0,5 til 0,2.
- 26 brudd kommer etter en uke uten telling og regnes ikke som kryssing med dagens definisjon.

### Grov backtest av R2–R4 som de står

- Treffandel avhenger av hvordan «første gang fikk rød status 2–4 uker før» tolkes:
  - rød status i minst én av ukene 2–4 før kryssingen: **35 %** (288 av 823)
  - første uke i den sammenhengende røde perioden før kryssingen ligger 2–4 uker før: **28 %** (230 av 823)
- Bom fordeler seg slik: ingen rød status i forkant (312), rød bare 1 uke før (158), og «for lite data» i ukene 2–4 før (65).
- Av 4 774 røde prognosevarsler (ikke «brudd nå») ble 14 % fulgt av brudd innen 4 uker. De fleste røde varsler er altså falske alarmer.
- Konsekvens for PRD-en: X i suksesskriterium 2 bør settes med disse tallene i bakhodet. Treff-definisjonen må presiseres. Lav treffsikkerhet er et legitimt funn å rapportere, siden briefen allerede kaller treffsikkerheten «en sentral usikkerhet».

### Beslutninger etter analysen (2026-10-29)

Skissen ble kjørt på nytt for hvert alternativ (treff etter tolkning B):

| Krav i R2 | Grå «for lite data» | Treff | Røde varsler fulgt av brudd |
|---|---|---|---|
| 5 av 5 | 13,3 % | 27,9 % | 14,4 % |
| 4 av 5 | 8,8 % | 28,4 % | 14,2 % |
| 3 av 5 | 5,5 % | 28,8 % | 14,1 % |

Å kutte datagrunnlaget ved 2026 uke 42 endrer nesten ingenting (814 i stedet for 823 kryssinger, samme treffandel).

Fredrik besluttet:

1. **R2:** vinduet på 5 uker må ha minst 3 tellinger, og regresjonen bruker bare ukene med telling. Begrunnelse: dekker telling annenhver uke under 4 °C (§ 6) og halverer andelen grå uker uten å endre treffsikkerheten. Nye testtilfeller T8 og T9 er lagt til i R6.
2. **Ufullstendige uker:** datagrunnlaget går til og med 2026 uke 42. Begrunnelse: gir et fast datagrunnlag, og demoen viser ikke nesten bare grå anlegg i de siste ukene.
3. **X = 25 %** med tolkning B, som briefen nå sier eksplisitt. Begrunnelse: realistisk for lineær regresjon, med litt margin til skissen (omtrent 29 %). **Åpenhet:** briefen sa at X skulle fastsettes før backtesten kjøres. X er satt etter denne skissen, og det skal stå i refleksjonsrapporten.

## Prognosemetode

- Metode for v1 er avklart (jf. åpne spørsmål nedenfor): **enkel trendekstrapolering** på historiske lusetall — ikke en mer avansert tidsseriemodell (f.eks. ARIMA, eksponentiell glatting, eller maskinlæringsbasert regresjon).
- Begrunnelse: holder kompleksiteten lav for en konseptuell prototype innenfor kursets (IBE160) tidsramme, og er tilstrekkelig til å demonstrere verdien av et prediktivt varsel kontra observasjonsverktøyene som finnes i dag (jf. «Hva gjør dette annerledes» i brief.md).
- **Avklart:** Implementasjonen er lineær regresjon over de 5 siste ukenes lusetall, med en horisont på 6 uker. Estimatet for hver kommende uke sammenlignes med grensen som gjelder i den uka (R2 og R3 i brief.md).
- Vanntemperatur og sesongjustering av trenden brukes ikke i v1, og er planlagt som neste trinn når v1 er testet (R5 i brief.md).
- Kobling til suksesskriteriene i brief.md: treffsikkerheten måles med en backtest der rød status (R4) 2–4 uker før faktisk grensekryssing regnes som treff.
- Dersom v1 viser at enkel trendekstrapolering ikke gir god nok treffsikkerhet mot suksesskriteriet, er en mer avansert tidsseriemodell en naturlig retning for en senere versjon (jf. Omfang i brief.md, der dette er bevisst holdt utenfor v1).

## Beslektet/eksisterende verktøy

- **Dr-grimen/oppdretter** (GitHub, åpen kildekode): «Varselsystem for norsk havbruk. Lakselus, sjukdom, soner og brønnbåtar frå opne norske kjelder.» Bygger på NLOD-lisensierte offentlige data.
  - Dette er et observasjons-/aggregeringsverktøy for **nåværende** status, ikke en prediktiv modell.
  - Relevant referansepunkt for «Hva gjør dette annerledes» — bør ses nærmere på før PRD/arkitektur, både som inspirasjon og for å unngå å bygge noe som allerede finnes i samme form.
  - Kilde: [github.com/Dr-grimen/oppdretter](https://github.com/Dr-grimen/oppdretter)

## Åpne spørsmål — status per 2026-10-27

1. **Delvis avklart.** Det finnes en refleksjonsrapport-mal for IBE160-leveransen. Konkrete krav til omfang/vurderingskriterier for selve produktleveransen er ikke kartlagt ennå.
2. **Avklart.** Web/dashboard — ikke SMS-/e-post-/push-varsling.
3. **Fortsatt åpent.** Teknisk stack og arbeidsdeling er ikke diskutert med Ella ennå.
4. **Avklart.** Prediksjonsmodellen i v1 er lineær regresjon over 5 uker med horisont 6 uker (R2), ikke en mer sofistikert tidsseriemodell.
5. **Avklart.** Ingen andre kjente konkurrenter/alternativer utover «oppdretter»-prosjektet.
6. **Avklart.** Datagrunnlaget er et nedlastet BarentsWatch-utdrag i `data/barentswatch/`: `lakselus_per_fisk_2025.xlsx` og `lakselus_per_fisk_2026.xlsx` (commit 51c6b85). Innholdet er analysert i seksjonen «Dataanalyse av BarentsWatch-utdraget».
7. **Delvis avklart.** X i backtesten er satt til 25 %, og datoen for kontroll mot Lovdata er fylt inn i R1 (2026-10-29). Inndata for T5, T6 og T8 er valgt med KI-støtte som rette linjer uten likhet mot grensen, slik at de er lette å regne for hånd. Fasiten for T5, T6 og T8 skal fortsatt regnes ut for hånd av gruppen.
