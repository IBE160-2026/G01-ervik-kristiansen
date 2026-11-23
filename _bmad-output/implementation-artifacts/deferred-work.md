- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-grunnmur-for-backend-og-kjerne.md`
  summary: Story 2.1 må sørge for at Pydantic sender lusetall (Decimal) som JSON-tall og ikke som tekst, slik AD-6 krever.
  evidence: Blind Hunter i review av Story 1.1 påpekte at Pydantic v2 serialiserer Decimal som streng i JSON som standard. Ikke kontrollert ennå. Avklares ved å sjekke `model_dump_json()` på en modell med et Decimal-felt i Story 2.1, og at frontend får `0.5` og ikke `"0.50"`.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-2-lusegrense-og-omrade-r1.md`
  summary: `uv run pytest` (kommandoen i README og NFR2) feiler på Fredriks Windows-maskin fordi Windows Programkontroll blokkerer `backend/.venv/Scripts/pytest.exe`; `uv run python -m pytest` virker.
  evidence: Kontrollert to ganger 2026-11-19 under Story 1.2 (os error 4551, «En programkontrollpolicy har blokkert denne filen»). Under Story 1.1 virket `uv run pytest` i samme `.venv`. Avklares ved å sjekke Smart App Control eller WDAC i Windows-sikkerhet, eller ved å skrive `uv run python -m pytest` som alternativ i README.
