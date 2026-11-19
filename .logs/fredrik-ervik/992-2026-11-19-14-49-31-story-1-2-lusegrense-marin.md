# Story 1.2 lusegrense marin

## 2026-11-19 kl. 14:49 — Fredrik Ervik

### Oppgave
Fredrik ba om fire ting:
1. Flette PR #2 (Story 1.1).
2. Oppdatere `main`.
3. Sette Story 1.1 til `done`.
4. Starte Story 1.2 (lusegrense og område, R1) med `bmad-build` på egen gren.

Han ville diskutere valgene før koden ble skrevet.

### Plan
- Flettingen med `gh pr merge 2` ble stoppet av tillatelsene i Claude Code. Fredrik flettet selv med `! gh pr merge 2 --merge`.
- `main` ble oppdatert, og grenen `story/1-2-lusegrense-og-omrade-r1` ble laget fra den. Story 1.1 ble satt til `done` i sprint-status.
- Spec: [spec-1-2-lusegrense-og-omrade-r1.md](../../_bmad-output/implementation-artifacts/spec-1-2-lusegrense-og-omrade-r1.md).
  - En subagent gjennomgikk specen før godkjenning, og funnene ble tatt inn.
  - Fredrik valgte bare norske navneformer i fylkestabellen, uten samiske og kvenske, og godkjente specen.
- Implementering og review med tre subagenter (Blind Hunter, Edge Case Hunter, Verification Gap). Funnene er sortert i Review Triage Log i specen.

### Resultat
- PR #2 er flettet (`00ba959`). Story 1.1 ble satt til `done` i `57c4eb9` på grenen for 1.2.
- Story 1.2 er committet i `846b9fa` på `story/1-2-lusegrense-og-omrade-r1`. Den er ikke pushet. Den nye koden:
  - `backend/src/marin/kjerne/omrade.py`: `Omrade` (StrEnum `sor`/`nord`/`ukjent`), en lukket tabell med 26 fylkesnavn og `omrade_fra_fylke`. Oppslaget ignorerer store og små bokstaver og ekstra mellomrom, også hardt mellomrom.
  - `backend/src/marin/kjerne/lusegrense.py`: `grense(omrade, uke)` gir 0,2 i uke 16–21 i sør og uke 21–26 i nord, ellers 0,5, og `None` ved ukjent område. `er_brudd(verdi, grense)` krever `Decimal` og en verdi som er avrundet til 2 desimaler.
  - Testene `test_lusegrense.py` (T1–T4 navngitt etter fasiten) og `test_omrade.py`. Testen av kjernens importer kjenner de nye modulene.
- Review: 12 funn.
  - 4 rettet:
    - `er_brudd` avviser verdier som ikke er avrundet (0,495).
    - Docstringen for `Omrade` følger nå AD-13: `ukjent` blir `null` i API-et.
    - Hardt mellomrom står som ` ` i testen.
    - Typesjekken for uke testes også ved ukjent område.
  - 1 utsatt: `uv run pytest` på denne maskinen.
  - 7 avvist med begrunnelse.
- 210 tester består med `uv run python -m pytest` (113 før storyen). Sprint-status: Story 1.2 står på `review`.

### Åpne punkter
- `uv run pytest` feiler på denne maskinen fordi Windows Programkontroll blokkerer `backend/.venv/Scripts/pytest.exe`, mens `uv run python -m pytest` virker. Sjekk Smart App Control i Windows-sikkerhet, eller skriv alternativet i README (ført i deferred-work.md).
