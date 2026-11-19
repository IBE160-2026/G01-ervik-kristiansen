# G01 — Marin
https://g01-ervik-kristiansen.vercel.app/ 
Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Backend og tester

Backend ligger i `backend/` og er et [uv](https://docs.astral.sh/uv/)-prosjekt med Python 3.14. Du trenger uv 0.12 eller nyere. uv henter Python 3.14 selv hvis den mangler.

```sh
cd backend
uv sync        # installerer avhengighetene (trenger nett første gang)
uv run pytest  # kjører alle backendtestene
```

## Medlemmer

- Fredrik Ervik
- Ella Vågø Kristiansen
