---
title: 'Story 2.1: API-kontrakten for kjerneflyten'
type: 'feature'
created: '2026-11-25'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-2-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Det finnes ikke noe API ennå. Backend (2.4–2.6) og frontend (2.2, 2.3 og 2.7–2.10) kan ikke bygges parallelt før formen på svarene er bestemt i kode (AD-3, AD-7).

**Approach:** `marin.api` får Pydantic-modellene som speiler kjernens typer, og en FastAPI-app med de tre rutene i kjerneflyten. Rutene svarer 501 til de bygges. `backend/openapi.json` committes og holdes lik appen med en test. Appen leser `datasett.json` én gang ved oppstart.

## Boundaries & Constraints

**Always:**
- Avhengighetene er de som står under Stack i arkitekturen: `fastapi==0.163.1`, `pydantic==2.14.3` og `uvicorn==0.54.0`, med `httpx2==2.16.2` som dev-avhengighet for TestClient. Ingen `fastapi[standard]`.
- `marin.api.modeller` har disse modellene, med feltene fra minsteformen i AD-3:
  - `Uke` (`ar`, `uke`)
  - `AnleggInfo` (`lokalitetsnr`, `navn`, `kommune`, `fylke`, alle kan være `null`)
  - `Status` (`farge`, `arsak`, `symbol`, `tekst`, `uke_tekst`, `forklaring`)
  - `EstimertUke` (`uke`, `uker_til`)
  - `Tabellrad` (`uke`, `verdi`, `siste_telling`)
  - `Grafpunkt` (`uke`, `malt`, `trend`, `grense`)
  - `Kryssing` (`uke`, `tekst`)
  - `Graf` (`punkter`, `kryssing`)
  - `Detaljsvar` (`kilde`, `anlegg`, `analyseuke`, `status`, `estimert_uke`, `tabell`, `graf`, `tekstoppsummering`, `usikkerhetstekst`)
  - `Anleggsvar` (`anlegg`, `analyseuker`, `standard_analyseuke`)
  
  `kilde` er `innebygd` eller `opplastet`.
- `farge` og `arsak` har typene `Farge` og `Arsak` fra `marin.kjerne.status`, så kodene finnes bare ett sted (AD-7).
- `Uke`, `AnleggInfo` og `EstimertUke` har de samme feltene som kjernens typer og kan lages direkte fra et kjerneobjekt.
- Lusetall (`verdi`, `malt`, `trend` og `grense`) er `Decimal` i modellen. De blir JSON-tall i svaret og `number` i skjemaet, aldri tekst (AD-6). `null` betyr ikke telt eller mangler.
- Rutene er:
  - `GET /api/anlegg?q=`, som gir `list[AnleggInfo]`
  - `GET /api/anlegg/{lokalitetsnr}`, som gir `Anleggsvar`
  - `GET /api/anlegg/{lokalitetsnr}/prognose?ar=&uke=`, som gir `Detaljsvar`

  `lokalitetsnr`, `ar` og `uke` er heltall, og `q` er tekst. Svarmodellen står i skjemaet. Hver rute svarer HTTP 501 med `{"detail": …}` på norsk og nevner storyen som bygger den (2.4 eller 2.5).
- CORS tillater bare opphavet `http://localhost:3000` (AD-9).
- Ved oppstart leser appen `datasett.json` én gang med `marin.kilder.datasett.last()` og holder det i minnet. En avhengighet gir rutene datasettet, slik at 2.4 og 2.5 kan bruke det uavhengig av hverandre (AD-10).
- `uv run python -m marin.api.openapi` skriver `backend/openapi.json` fra `app.openapi()`. Fila er UTF-8 med `\n`, har innrykk på 2 og samme tekst ved hver kjøring.

**Never:**
- Ingen søk, prognose, `bygg_detaljsvar` eller lesing av `backtest.json` (Story 2.4–2.6). Ingen modeller eller ruter for opplasting (Epic 3). Ingen montering av `frontend/out/` (Story 2.3).
- Ingen endring i `marin.kjerne`, `marin.kilder`, `marin.forbered` eller `marin.backtest`. Kjernen importerer aldri `marin.api`.
- Ingen miljøvariabler eller hemmeligheter. Ingen flyttall i kjernen.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Lusetall | `Tabellrad` med `verdi=Decimal("0.28")` | JSON-teksten har `"verdi": 0.28` som tall, og skjemaet sier `number` | N/A |
| Ikke telt | `verdi=None` | `"verdi": null` | N/A |
| Fra kjernen | kjernens `Uke(2026, 42)`, `AnleggInfo(10560, …)` og `EstimertUke(Uke(2026, 46), 4)` | API-modellene får de samme verdiene, og feltnavnene er like kjernens | N/A |
| Ukjent kode | `Status` med `farge="lilla"` eller `arsak="annet"` | — | ValidationError |
| Tom rute | `GET /api/anlegg?q=hitra`, `/api/anlegg/10560` og `/api/anlegg/10560/prognose?ar=2026&uke=42` | HTTP 501 og `{"detail": "…"}` | N/A |
| Ugyldig parameter | `/api/anlegg/abc` eller prognose uten `ar` | HTTP 422 fra FastAPI | N/A |
| CORS tillatt | `Origin: http://localhost:3000`, også forhåndsforespørsel | `access-control-allow-origin: http://localhost:3000` | N/A |
| CORS ikke tillatt | `Origin: http://127.0.0.1:3000` eller `http://localhost:3001` | ingen `access-control-allow-origin` | N/A |
| Utdatert skjema | `backend/openapi.json` avviker fra `app.openapi()` | — | testen feiler, og meldingen gir kommandoen |
| Oppstart | appen startes og får flere forespørsler | `datasett.json` er lest én gang og har 1 092 anlegg | N/A |

</frozen-after-approval>

## Code Map

- `backend/src/marin/kjerne/modeller.py` -- `Uke(ar, uke)` og `AnleggInfo(lokalitetsnr, navn, kommune, fylke)`, med alle felt valgfrie. Endres ikke.
- `backend/src/marin/kjerne/status.py` -- `Farge` og `Arsak` (`StrEnum`) og `EstimertUke(uke, uker_til)`. `Vurdering` har `symbol`, `tekst` og `uke_tekst`. Endres ikke.
- `backend/src/marin/kilder/datasett.py` -- `last() -> Datasett(siste_uke, kilder, anlegg)`. Leser fra pakken med `importlib.resources` og importerer bare kjernen, ikke openpyxl.
- `backend/tests/test_kjerne_importer.py` -- skal fortsatt bestå. Kjernen importerer bare stdlib og seg selv.
- `backend/tests/test_datasett_fil.py:49` -- 1 092 anlegg.
- `backend/pyproject.toml` og `uv.lock` -- avhengigheter er pinnet med `==`, som `openpyxl==3.1.5`.
- `_bmad-output/planning-artifacts/architecture/architecture-Marin-2026-11-16/ARCHITECTURE-SPINE.md:61-88` -- AD-3 med rutene og minsteformen. Linje 190–201 har Stack.
- `.../reviews/review-versions.md:64` -- `httpx2` er det Starlette 1.10.0 sin TestClient importerer.
- `README.md` -- seksjonen «Backend og tester» (linje 7). Kommandoene for API-et legges her.

## Tasks & Acceptance

**Execution:**
- [ ] `backend/pyproject.toml` og `backend/uv.lock` -- legg til avhengighetene med `uv add` og `uv add --dev` etter Boundaries.
- [ ] `backend/src/marin/api/__init__.py` og `modeller.py` -- modellene etter Boundaries.
- [ ] `backend/src/marin/api/app.py` -- `app` med de tre rutene, CORS, lesing av datasettet ved oppstart og avhengigheten som gir datasettet.
- [ ] `backend/src/marin/api/openapi.py` og `backend/openapi.json` -- kommandoen som skriver fila, og fila den skriver.
- [ ] `backend/tests/test_api_modeller.py` -- radene om lusetall, ikke telt, fra kjernen og ukjent kode i matrisen.
- [ ] `backend/tests/test_api_app.py` -- radene om ruter, CORS, skjema og oppstart i matrisen. Bruk TestClient.
- [ ] `README.md` -- hvordan API-et startes med `uv run uvicorn marin.api.app:app --reload` (port 8000), og hvordan `openapi.json` lages på nytt.

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 492 fra før.
- Gitt `uv run uvicorn marin.api.app:app`, når appen startes, så starter den uten feil, og `/docs` viser de tre rutene.
- Gitt `git diff` mot baseline, når endringene leses, så er ingen filer under `marin/kjerne`, `marin/kilder`, `marin/forbered` eller `marin/backtest` endret.

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

Pydantic v2 gjør `Decimal` om til tekst i JSON som standard. Lusetallene har høyst 2 desimaler, så en serialisering som gir JSON-tall, gir samme tekst som verdien (`0.28` blir `0.28`). Den må bare gjelde JSON og ikke endre verdien i Python. Et eksempel:

```python
Lusetall = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]
```

`Anleggsvar` har `AnleggInfo` under `anlegg`, slik `Detaljsvar` har. Et flatt svar med alle feltene i `AnleggInfo` ville ikke speilet en kjernetype.

CORS er alltid på for `http://localhost:3000`. Uten miljøvariabler kan appen ikke vite om den kjører i utvikling. Lokalt og på Vercel kommer frontenden fra samme opphav, så regelen brukes bare i utvikling.

## Verification

**Commands (i `backend/`):**
- `uv run pytest` -- expected: alle testene består
- `uv run python -m marin.api.openapi` og deretter `git diff --exit-code openapi.json` -- expected: ingen endring
