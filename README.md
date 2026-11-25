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

To av testene leser hele BarentsWatch-utdraget, og én kjører backtesten på hele datasettet, så testene tar omtrent 55 sekunder.

## Data

Lusetallene kommer fra datasettet «Lakselus per fisk» i [BarentsWatch Fiskehelse](https://www.barentswatch.no/fiskehelse/). Det er anleggenes ukentlige rapportering av lakselus til Mattilsynet. Tallene ble lastet ned 27.10.2026 som Excel-uttrekk, ett per år (2025 og 2026). Uttrekkene har alle lokaliteter for laks, ørret og regnbueørret i akvakulturregisteret, unntatt dem på land. Arket «Om datasettet» i hver fil beskriver kolonnene.

Dataene er lisensiert under [Norsk lisens for offentlige data (NLOD)](https://data.norge.no/nlod), se også [vilkårene til BarentsWatch](https://www.barentswatch.no/en/articles/api-terms-and-conditions). Data levert av BarentsWatch. Opplysninger om lakselus er hentet fra Mattilsynet.

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

Backtesten etter SK2 leser `datasett.json`, regner treffandel og presisjon og skriver `backend/src/marin/data/backtest.json` og et sammendrag i terminalen:

```sh
cd backend
uv run python -m marin.backtest
```

`backtest.json` er committet, og tallene står under [Treffsikkerhet](#treffsikkerhet).

Datasettet er knyttet til dette utdraget. Byttes utdraget ut, må også `FORSTE_UKE` og `SISTE_UKE` i `backend/src/marin/kjerne/konstanter.py`, `FORSTE_KRYSSING` og `SISTE_VARSEL` i `backend/src/marin/kjerne/treffsikkerhet.py` og tallene som testene sjekker mot utdraget (antall anlegg og rader i `test_datasett_fil.py` og `test_nfr3.py`), oppdateres.

## Treffsikkerhet

Backtesten etter SK2 ble kjørt én gang på hele datasettet 25.11.2026 (A5 i PRD-en). Parameterne ble fryst før kjøringen og er de samme som i kjernen: vindu 5 uker, minst 3 tellinger, horisont 6 uker og rød ved 0–3 uker. Tallene står i `backend/src/marin/data/backtest.json` og er rapportert slik skriptet ga dem, også når de er under tersklene (FR27a).

| | Antall | Holdt utenfor | Andel |
| --- | --- | --- | --- |
| Kryssinger | 778 | 44 før uke 9, 2025 | |
| Treff (rød status begynte 2–4 uker før kryssingen) | 127 | | Treffandel 16,3 % |
| Varsler («✕ Varsel …») | 5161 | 281 etter uke 38, 2026 | |
| Varsler fulgt av brudd innen 4 uker | 687 | | Presisjon 13,3 % |

- **M1 holder ikke.** Treffandelen er 16,3 %, under kravet på minst 25 %, så SK2 og M1 er ikke oppfylt. Det endrer ingen tekster i appen.
- **M1-C slår inn.** Presisjonen er 13,3 %, under 20 %. Etter reaksjonen på M1-C, som ble bestemt før kjøringen, presenteres Marin som en tidlig indikator: rød status betyr at brukeren bør følge ekstra med, ikke at grensen helt sikkert brytes. Kravteksten for usikkerhetsteksten (FR19 i PRD-en, `EXPERIENCE.md` og Story 2.6) og beskrivelsen av Marin i PRD-en er endret med tekstene som ble låst før kjøringen. Appen viser teksten fra Story 2.6.

Testene sjekker at `backtest.json` er lik en ny kjøring av skriptet, og at parameterne i fila er kjernens. Endres kjernen eller datasettet, feiler testen til backtesten er kjørt på nytt. Da må de nye tallene rapporteres for hånd her og i PRD kap. 11.

## Medlemmer

- Fredrik Ervik
- Ella Vågø Kristiansen
