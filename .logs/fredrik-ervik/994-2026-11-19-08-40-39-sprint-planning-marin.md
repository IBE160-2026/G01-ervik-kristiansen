# Sprint planning for Marin

## 2026-11-19 kl. 08:40 — Fredrik Ervik

### Oppgave
Starte neste fase i Marin etter epics og stories: sprint planning med readiness-sjekk, sporingsfil og eier per story (A3). Økten startet 18. november og ble avsluttet 19. november.

### Plan
- Kjøre `bmad-sprint-planning` med full flyt: readiness-sjekk mot PRD, arkitektur, UX og epics, og deretter `sprint_plan.py generate`.
- Avgjøre arbeidsdelingen (A3) og føre eier per story inn i sporingsfila.
- Bygger på forrige økt: [arkitektur-a4-epics-marin](995-2026-11-18-13-23-05-arkitektur-a4-epics-marin.md).

### Resultat
- **Readiness: PASS.** Epics og stories dekker FR1–FR29 og NFR1–NFR12, og beslutningene storyene bygger på, står i arkitekturen, i EXPERIENCE.md/DESIGN.md eller i selve storyene. Tre små avvik i ordlyd ble rettet (cad6648):
  - Story 1.5 og 1.7 sier nå «rød ved 0–3 uker», som FR27a og AD-1 (brudd nå er 0 uker). Dermed stemmer `parametere` i `backtest.json` med kjernen.
  - Story 1.5: `uke_tekst` er `null` når det ikke finnes noen uke, som i AD-2 (før stod det «tom»).
  - Arkitekturen binder nå `NFR1-NFR12` (før stod det `NFR1-NFR11`).
- **Sporingsfil:** `_bmad-output/implementation-artifacts/sprint-status.yaml` med 3 epics, 24 stories og 3 retrospektiver, alt i `backlog`/`optional`. Fila er validert med skriptet. Advarselen om «## Epic-liste» er godtatt, fordi det er oversiktsseksjonen og ikke en epic.
- **A3, arbeidsdeling:** Fredrik gjør alle storyene selv (avgjort 2026-11-19). Valget står i nøkkelen `eiere` i `sprint-status.yaml`. Nøkkelen bevares når sprint planning kjøres på nytt (kontrollert: `in_sync: true`, 24 eiere).
- Story-nøklene har æ, ø og å (for eksempel `1-7-første-backtestkjøring-og-rapport-a5`), fordi skriptet lager dem fra titlene. Det er godtatt.
- Neste steg: `bmad-build` på Story 1.1 (grunnmur for backend og kjerne).

### Åpne punkter
- Hvis Ella tar over stories, oppdater `eiere` i `sprint-status.yaml` (valgt «vent på Ella», men Fredrik gjør alt inntil videre).
