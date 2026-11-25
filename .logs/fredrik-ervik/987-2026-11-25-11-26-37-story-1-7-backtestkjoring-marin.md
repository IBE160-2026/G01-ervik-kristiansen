# Story 1.7 backtestkjøring marin

## 2026-11-25 kl. 11:26 — Fredrik Ervik

### Oppgave
Fredrik flettet PR #7 for Story 1.6 og ba meg planlegge Story 1.7, første backtestkjøring og rapport (A5), med `bmad-build`. Han godkjente specen og valgte «Godkjenn og fortsett».

### Plan
- Laget grenen `story/1-7-forste-backtestkjoring-og-rapport-a5` fra `main` etter flettingen (`011d762`). Satte Story 1.6 til `done` og rettet matriseraden i spec-1-6 (`b2a17eb`).
- `bmad-build` steg 1–2:
  - `epic-1-context.md` var gyldig. Fortsatte fra spec-1-6.
  - Leste PRD kap. 1, 2, FR19, kap. 11–13, SK2 i briefen, EXPERIENCE.md linje 111 og Story 2.6 i `epics.md`.
- Fredriks beslutninger før kjøringen:
  - M1-C-tekstene for FR19 og PRD kap. 1 er låst før tallet er kjent.
  - Treffandel under 25 % rapporteres bare og endrer ingen tekster i appen.
  - Gruppen kontrollerer og signerer fasiten i `backtest_liten.md` før kjøringen.
  - Specen beholdes hel (omtrent 2 500 tokens).
- Mine valg i specen:
  - Tersklene sjekkes eksakt med antallene.
  - En ny test sjekker at den committede `backtest.json` er lik en ny kjøring (omtrent 13 sekunder).
  - Hvis M1-C slår inn, legges M1-C-teksten til ved siden av den vanlige FR19-teksten, fordi Story 2.6 velger etter presisjonen i fila.
  - PRD-en settes til `final`.
- Spec: [spec-1-7-forste-backtestkjoring-og-rapport-a5.md](../../_bmad-output/implementation-artifacts/spec-1-7-forste-backtestkjoring-og-rapport-a5.md).

### Resultat
- Specen er committet som `ready-for-dev` (`2111aea`).
- Implementeringen er ikke startet. Signaturlinja i `backend/tests/data/backtest_liten.md` er tom, og specen krever at den er fylt ut og committet før kjøringen.
- Backtesten er ikke kjørt, og grenen er ikke pushet.

### Åpne punkter
- Gruppen kontrollerer fasiten i `backend/tests/data/backtest_liten.md` og signerer. Deretter fortsetter `bmad-build` med spec-1-7 fra steg 3 (allerede ført i `issues.md` fra Story 1.6).
