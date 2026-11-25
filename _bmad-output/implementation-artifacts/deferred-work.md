- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-grunnmur-for-backend-og-kjerne.md`
  summary: Story 2.1 må sørge for at Pydantic sender lusetall (Decimal) som JSON-tall og ikke som tekst, slik AD-6 krever.
  evidence: Blind Hunter i review av Story 1.1 påpekte at Pydantic v2 serialiserer Decimal som streng i JSON som standard. Ikke kontrollert ennå. Avklares ved å sjekke `model_dump_json()` på en modell med et Decimal-felt i Story 2.1, og at frontend får `0.5` og ikke `"0.50"`.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-lusegrense-og-omrade-r1.md`
  summary: `uv run pytest` (kommandoen i README og NFR2) feiler på Fredriks Windows-maskin fordi Windows Programkontroll blokkerer `backend/.venv/Scripts/pytest.exe`; `uv run python -m pytest` virker.
  evidence: Kontrollert to ganger 2026-11-19 under Story 1.2 (os error 4551, «En programkontrollpolicy har blokkert denne filen»). Under Story 1.1 virket `uv run pytest` i samme `.venv`. Avklares ved å sjekke Smart App Control eller WDAC i Windows-sikkerhet, eller ved å skrive `uv run python -m pytest` som alternativ i README.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-5-status-etter-r4.md`
  summary: Modul-docstringen i `backend/src/marin/kjerne/trend.py` (linje 14) sier fortsatt «Status kommer i Story 1.5.», selv om statusen nå finnes i `status.py`.
  evidence: Blind Hunter i review av Story 1.5, bekreftet. Specen for 1.5 forbyr endringer i `trend.py` (Never), så linja må rettes i en senere story som får lov til å røre `trend.py`.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-5-status-etter-r4.md`
  summary: Story 2.6 trenger antall tellinger i vinduet («Bare 2 av de siste 5 ukene …»), men `Vurdering` har det ikke. `vurder` regner det ut og kaster det.
  evidence: Blind Hunter i review av Story 1.5, bekreftet mot T9 og forklaringsmalene. Feltene i `Vurdering` er låst i intensjonen for 1.5. I 2.6 må forklaringsfunksjonen enten få et nytt felt i `Vurdering` eller kalle `vindu(serie, analyseuke)` på nytt. Grensen og analyseuka har API-et selv.
