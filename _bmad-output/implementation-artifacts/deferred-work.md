- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-grunnmur-for-backend-og-kjerne.md`
  summary: Story 2.1 må sørge for at Pydantic sender lusetall (Decimal) som JSON-tall og ikke som tekst, slik AD-6 krever.
  evidence: Blind Hunter i review av Story 1.1 påpekte at Pydantic v2 serialiserer Decimal som streng i JSON som standard. Ikke kontrollert ennå. Avklares ved å sjekke `model_dump_json()` på en modell med et Decimal-felt i Story 2.1, og at frontend får `0.5` og ikke `"0.50"`.
