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

To av testene leser hele BarentsWatch-utdraget, så testene tar omtrent 35 sekunder.

## Data

Lusetallene kommer fra BarentsWatch, datasettet «Lakselus per fisk», som bygger på anleggenes ukentlige rapportering. De ble lastet ned 27.10.2026 fra BarentsWatch Fiskehelse som Excel-uttrekk, ett per år (2025 og 2026), for alle lokaliteter. Dataene er lisensiert under Norsk lisens for offentlige data (NLOD) 2.0.

Appen bruker data fra 2025 uke 1 til og med 2026 uke 42. Uke 43 og 44 i 2026 var ikke ferdig rapportert da utdraget ble lastet ned, og leses ikke inn.

| Hva | Hvor |
| --- | --- |
| Kildedataene (Excel fra BarentsWatch) | `data/barentswatch/` |
| Den forhåndsbehandlede datafila som appen leser | `backend/src/marin/data/datasett.json` |
| Testdata | `backend/tests/data/` og i testene selv |

`datasett.json` lages av kildedataene og committes. Endres Excel-filene, lages den på nytt slik:

```sh
cd backend
uv run python -m marin.forbered
```

Skriptet stopper med en feilmelding hvis en fil har feil. Testene sjekker at sha256-hashene i `datasett.json` stemmer med Excel-filene, og at `datasett.json` er lik en ny kjøring av skriptet.

Datasettet er knyttet til dette utdraget. Byttes utdraget ut, må også `SISTE_UKE` i `backend/src/marin/kjerne/konstanter.py` og tallene som testene sjekker mot utdraget (antall anlegg og rader i `test_datasett_fil.py` og `test_nfr3.py`), oppdateres.

## Medlemmer

- Fredrik Ervik
- Ella Vågø Kristiansen
