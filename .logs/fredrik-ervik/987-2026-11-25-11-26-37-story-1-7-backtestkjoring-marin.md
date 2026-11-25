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
- Fredrik kontrollerte fasiten i `backtest_liten.md` for hånd og signerte 25.11.2026 (`609f383`, baseline for storyen). SK2-testene besto før signaturen ble committet.
- En implementeringsagent som bare hadde specen, kjørte backtesten én gang (exit 0, omtrent 19 sekunder) og skrev rapporten:
  - Kryssinger: 778, med 44 holdt utenfor. Treff: 127. Treffandel 16,3 % (0.1632).
  - Varsler: 5161, med 281 holdt utenfor. Fulgt av brudd: 687. Presisjon 13,3 % (0.1331).
  - **M1 holder ikke** (127 × 4 = 508 < 778), og **reaksjonen på M1-C slo inn** (687 × 5 = 3435 < 5161). Skissen ga omtrent 29 % og 14 %.
- Jeg kontrollerte selv:
  - Ingen kode under `backend/src/` er endret. Den eneste nye fila der er `backtest.json`.
  - Tallene er de samme i `backtest.json`, terminalteksten, README, PRD kap. 11 og `issues.md`.
  - De låste M1-C-tekstene står ordrett i PRD-en, EXPERIENCE.md og Story 2.6.
  - Den låste blokken i specen er uendret.
- Review med Blind Hunter, Edge Case Hunter og Verification Gap: 17 funn, ført i Review Triage Log i specen. 5 ble rettet, 1 ble utsatt og 11 ble avvist. De fire rettelsene implementeringsagenten gjorde:
  - README sier at en ny kjøring må rapporteres for hånd.
  - README sier at bare kravene er endret, ikke appen.
  - Story 2.6 og FR19 velger M1-C-teksten med antallene, ikke den avrundede andelen.
  - Testdocstringen oppgir ikke lenger sekunder.

  Den femte rettelsen var å lukke punktene i `issues.md` under. Det utsatte funnet er den eldre ordlyden i det vanlige FR19-eksempelet i PRD-en, ført i `deferred-work.md`.
- Commit `c6e7f29`:
  - `backtest.json`
  - `test_backtest_fil.py`, med 2 tester
  - seksjonen Treffsikkerhet i README
  - PRD-en, som nå er `final`, med kap. 1, FR19, kap. 2, 11, 12 og 13 oppdatert
  - EXPERIENCE.md og Story 2.6
- `uv run pytest` ga 492 bestått (490 fra før og 2 nye) på 53–64 sekunder.
- Specen står som `done`, og Story 1.7 står som `review` i sprint-status. Grenen er ikke pushet.
- Lukket i `issues.md`:
  - ny kjøring med FR27 og oppdatering av PRD kap. 11
  - PRD-en til `final`
  - testtiden i README
  - signaturen for fasiten
  - kjøring med PYTHONIOENCODING

### Åpne punkter
- Refleksjonsrapporten skal ha forskjellen fra skissen og at SK2 og M1 ikke er oppfylt (ført i `issues.md` av implementeringen).
- Refleksjonsrapporten skal også si at KI regnet fasiten for `backtest_liten.md`, og at Fredrik kontrollerte den 25.11.2026 før kjøringen.
- Før eller i Story 2.6: det vanlige FR19-eksempelet i PRD-en må få samme ordlyd som Story 2.6 og EXPERIENCE.md (`deferred-work.md`).
- Story 2.6: skal reserveteksten, som vises når `backtest.json` mangler, også ha forbeholdet om tidlig indikator? I dag er den bare «Prognosen er en enkel trendberegning, ikke en garanti.».
