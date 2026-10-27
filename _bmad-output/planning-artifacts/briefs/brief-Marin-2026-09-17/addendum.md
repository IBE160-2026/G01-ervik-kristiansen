---
title: "Addendum: Marin"
status: draft
created: 2026-09-17
updated: 2026-10-27
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
6. **Avklart.** Datagrunnlaget er et nedlastet BarentsWatch-utdrag i `data/barentswatch/`. Fila er ikke lastet ned ennå.
7. **Fortsatt åpent.** Plassholdere i brief.md: dato for kontroll mot Lovdata (R1), inndata og fasit for T5 og T6 (R6), og prosentkravet X i backtesten.
