# Arkitektur, fasitkontroll og epics for Marin

## 2026-11-18 kl. 13:23 — Fredrik Ervik

### Oppgave
Fortsette Marin fra UX-steget: føre UX-tilleggene inn i PRD-en, lage arkitekturen, følge opp PRD-en, kontrollere fasiten i briefen (A4) og lage epics og stories. Arbeidet gikk fra 16. til 18. november.

### Plan
- Bekrefte tre PRD-tolkninger og føre UX-1 til UX-7 inn som FR i PRD-en.
- Lage arkitekturen med `bmad-architecture` (coaching), med Ella til stede ved de første valgene.
- Følge opp PRD-en etter arkitekturen og definere presisjon i backtesten (A6).
- Kontrollere fasiten for T5, T6, T8 og T10–T12 (A4) og endre rekkefølgen slik at backtesten (A5) kjøres etter første epic.
- Lage epics og stories med `bmad-create-epics-and-stories`.

### Resultat
- **PRD og UX (16.11):** FR6a, FR6b, FR15a, FR15b og FR25a lagt til fra UX-1 til UX-7, og EXPERIENCE.md avstemt (0c429b1).
- **Arkitektur (16.11, oppdatert 18.11):** funksjonell kjerne og imperativt skall, Python/FastAPI og Next.js med statisk eksport, publisert med Vercel Services. AD-1 til AD-15 i `architecture/architecture-Marin-2026-11-16/ARCHITECTURE-SPINE.md` (c54850d).
- **PRD-oppfølging (18.11):** presisjon og kanttilfeller i SK2 (A6, fa12838), NFR12 for Vercel, 4 MB-grense for opplasting og valgbare uker for opplastede data (184eb41).
- **A4 (18.11):** Claude regnet T5, T6, T8 og T10–T12 med eksakte brøker, og Fredrik kontrollerte hvert steg. Alle seks stemte med briefen. Merkingen er fjernet fra briefen, og avviket fra planen (ikke regnet for hånd) er beskrevet i PRD kap. 11 og `a4-handkontroll.md` (633ca2f, 672e2db).
- **Epics og stories (18.11):** `_bmad-output/planning-artifacts/epics.md` med 3 epics og 24 stories (1abc139):
  - Epic 1: prognose og backtest (7 stories, A5 i Story 1.7)
  - Epic 2: J1 og J2 i appen (11 stories)
  - Epic 3: opplasting (6 stories, 3.6 kan kuttes)
- **Beslutninger under epics:**
  - Arbeidsdelingen (A3) settes per story ved sprint planning.
  - Treff i backtesten teller all rød status.
  - Statusteksten får år når uka er i et annet år enn analyseuka.
  - FR19 bruker ordlyden fra EXPERIENCE.md.
  - CSV godtas i UTF-8 og Windows-1252.
  - Nettleseren sjekker 4 MB før opplasting, fordi Vercel stopper større forespørsler (AD-4 utvidet).

### Åpne punkter
- Kjør sprint planning (`bmad-sprint-planning`) i ny økt, helst med Ella, og sett eier per story (A3).
- Kjør A5 (Story 1.7) før noen stories i Epic 2 eller 3 starter, og sett PRD-en til `final` etterpå.
- Bekreft eller endre teksten «Fila er større enn 4 MB. Last ned bare ditt eget anlegg fra BarentsWatch og prøv igjen.» (Story 3.2 og 3.3, ikke i EXPERIENCE.md).
- Vercel Services er i beta. Reserveplanen er to Vercel-prosjekter (Story 2.3).
- Skriv i refleksjonsrapporten at fasiten (A4) ble regnet av KI og kontrollert av gruppen, ikke regnet for hånd.
