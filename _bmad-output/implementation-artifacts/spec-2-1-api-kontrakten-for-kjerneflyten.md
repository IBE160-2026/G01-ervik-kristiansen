---
title: 'Story 2.1: API-kontrakten for kjerneflyten'
type: 'feature'
created: '2026-11-25'
status: 'done'
route: 'dispatch'
review_loop_iteration: 0
baseline_commit: 'cc61fce9213d9ec37ffaa5cb73c64cfc6c61736d'
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
- [x] `backend/pyproject.toml` og `backend/uv.lock` -- legg til avhengighetene med `uv add` og `uv add --dev` etter Boundaries.
- [x] `backend/src/marin/api/__init__.py` og `modeller.py` -- modellene etter Boundaries.
- [x] `backend/src/marin/api/app.py` -- `app` med de tre rutene, CORS, lesing av datasettet ved oppstart og avhengigheten som gir datasettet.
- [x] `backend/src/marin/api/openapi.py` og `backend/openapi.json` -- kommandoen som skriver fila, og fila den skriver.
- [x] `backend/tests/test_api_modeller.py` -- radene om lusetall, ikke telt, fra kjernen og ukjent kode i matrisen.
- [x] `backend/tests/test_api_app.py` -- radene om ruter, CORS, skjema og oppstart i matrisen. Bruk TestClient.
- [x] `README.md` -- hvordan API-et startes med `uv run uvicorn marin.api.app:app --reload` (port 8000), og hvordan `openapi.json` lages på nytt.

**Acceptance Criteria:**
- Gitt `uv run pytest`, når testene kjører, så består alle, også de 492 fra før.
- Gitt `uv run uvicorn marin.api.app:app`, når appen startes, så starter den uten feil, og `/docs` viser de tre rutene.
- Gitt `git diff` mot baseline, når endringene leses, så er ingen filer under `marin/kjerne`, `marin/kilder`, `marin/forbered` eller `marin/backtest` endret.

## Implementation Notes

- Feltene som kan være `null`, har ingen standardverdi i modellene. Da står de under `required` i skjemaet, og frontend-typene blir `T | null` i stedet for valgfrie felt.
- Alle modellene har `from_attributes=True` (felles base `_Modell`), så `model_validate` tar kjernens dataclasser direkte, også nestet (`EstimertUke` med `Uke`).
- `kilde` er `Literal["innebygd", "opplastet"]` (aliaset `Kilde` i `modeller.py`).
- `q` er påkrevd. `?q=` (tom tekst) godtas, men uten `q` svarer FastAPI 422. Story 2.4 kan endre dette.
- CORS tillater bare `GET` (`allow_methods=["GET"]`), fordi bare GET-ruter finnes. Opplastingsrutene i Epic 3 må legge til `POST` og `Content-Type` i `allow_headers`.
- Datasettet lastes i `lifespan` og ligger i `app.state.datasett`. TestClient må brukes som kontekstbehandler (`with TestClient(app)`) for at oppstarten skal kjøre. Story 2.3 bør sjekke at Vercels Python-runtime kjører `lifespan`.
- `fastapi==0.163.1` har `opentelemetry-api` som vanlig avhengighet, så den står i `uv.lock` selv om `fastapi[standard]` ikke brukes.

## Spec Change Log

## Review Triage Log

| # | Kilde | Funn | Vurdering | Rute | Begrunnelse |
|---|---|---|---|---|---|
| 1 | Verification Gap | Ingen test sikrer at felt som kan være `null`, står under `required` i skjemaet. Med `= None` som i kjernen blir frontend-typene valgfrie, og testene består etter ny generering | low | patch | Bekreftet av revieweren med FastAPI 0.163.1. Regelen står i Implementation Notes og har ingen test. En test som sammenligner `required` med `properties` for modellene våre, er en direkte rettelse. |
| 2 | Verification Gap | Testen for lik tekst ved hver kjøring kan ikke feile, fordi `app.openapi()` er bufret i samme prosess | low | avvist | Bekreftet, men testen som sammenligner den committede fila med en ny kjøring, sammenligner allerede to prosesser. Skjemaet har ingen kilde til tilfeldig rekkefølge. Fiksen er en ny test med underprosesser. |
| 3 | Blind Hunter + Edge Case | 404 (og 501) står ikke i `openapi.json`, så frontend-typene ser ikke feilsvarene | low | avvist | Rutene gir aldri 404 i denne storyen. 404 bygges i Story 2.5 (AC i `epics.md`), som da må føre den opp. Story 2.7 trenger bare statuskoden («et nummer som ikke finnes (404), sender brukeren til forsiden»). Fiksen legger til en ny modell i kontrakten. Ført som åpent punkt for Story 2.5. |
| 4 | Blind Hunter | At `tabell` har 5 rader, at `analyseuker` er nyeste først og at standarduka er i lista, står bare i docstrings | low | avvist | Verdiene lages i Story 2.5, og ACene der tester nettopp dette (94 uker, nyeste først, standard 2026 uke 42). Fiksen legger til grenser og validering i kontrakten. |
| 5 | Blind Hunter + Edge Case | `ar` og `uke` i spørringen og API-ets `Uke` har ingen grenser, så uke 0 og 99 kan gi 500 i Story 2.5 | false | avvist | I denne storyen gir alle uker 501. AD-14 og ACene i Story 2.5 krever 422 for en uke utenfor lista, og det dekker uke 0 og 99. API-ets `Uke` fylles bare fra kjernens `Uke`, som sjekker ISO-kalenderen. |
| 6 | Blind Hunter + Edge Case | `Lusetall` godtar flyttall, mer enn 2 desimaler, negative tall og svært store tall | false | avvist | Svarmodellene fylles bare med verdier fra kjernen. Kjernen godtar ikke flyttall (`Telling`) og runder estimatene til 2 desimaler (`trend.py`). Et estimat kan med rette være negativt når trenden synker. |
| 7 | Blind Hunter | Docstringen til `modeller.py` sier at tallet i JSON har samme tekst som verdien, men `0.50` blir `0.5`. Testen har et tilfelle med 3 desimaler, og siste assert sammenligner bare kolonnene i tabellen | low | patch | Bekreftet. Tallverdien er den samme, men nuller på slutten faller bort. Docstringen og testen rettes direkte. |
| 8 | Blind Hunter | `summary` og `operationId` lages automatisk: «Sok Anlegg» uten ø, og `hent_prognose_api_anlegg__lokalitetsnr__prognose_get` | low | patch | Bekreftet i `openapi.json`. Utviklerne ser dette i `/docs` og i `schema.ts`. Det er billigst å rette før frontend genererer typene. |
| 9 | Blind Hunter + Edge Case | `openapifil()` virker bare når pakken er installert redigerbart | low | avvist | uv installerer prosjektet redigerbart som standard, og `test_openapi_json_ligger_i_backend` feiler hvis stien blir feil. Fiksen legger til en sjekk. |
| 10 | Blind Hunter | Ingen `.gitattributes` holder `openapi.json` på LF | false | avvist | Kommandoen skriver LF. Testen gjør CRLF om til LF, slik testene for `datasett.json` og `backtest.json` gjør. `openapi-typescript` leser JSON og bryr seg ikke om linjeskift. |
| 11 | Blind Hunter + Edge Case | `hent_datasett` gir 500 uten forklaring hvis oppstarten ikke har kjørt | false | avvist | Uvicorn kjører oppstarten som standard, og alle testene bruker `with TestClient`. Uten oppstart feiler appen tydelig, med `AttributeError` som nevner `datasett`. Vercel sjekkes i Story 2.3 (Implementation Notes). |
| 12 | Blind Hunter + Edge Case | `app.state.datasett` fjernes ikke etter nedstengning, så en senere test uten `with` kan bestå på gammel tilstand | low | avvist | Gjelder bare en tenkt test uten `with`. Fiksen legger til opprydding i koden. |
| 13 | Blind Hunter | Specen står som `in-review`, men sprint-status står som `in-progress` | false | avvist | bmad-build setter specen til `in-review` under review, og sprint-status til `review` når storyen presenteres. |
| 14 | Blind Hunter | Det som står i Implementation Notes, har ingen test: 422 uten `q`, `?q=` godtas og forhåndsforespørsel med POST avvises | low | avvist | Specen lar Story 2.4 bestemme hvordan `q` skal håndteres, så en test nå ville låse noe 2.4 skal avgjøre. AD-9 binder bare opphavet, og det er testet. |
| 15 | Blind Hunter + Edge Case | Treff i søket har `lokalitetsnr` som kan være `null`, selv om innebygde anlegg alltid har nummer | low | avvist | AD-3 og den låste delen av specen bestemmer `[AnleggInfo]`. Fiksen er å endre specen og arkitekturen. |
| 16 | Blind Hunter | README sier ikke at rutene svarer 501 | false | avvist | Meldingen i 501-svaret sier selv at ruten ikke er bygget ennå, og hvilken story som bygger den. |
| 17 | Blind Hunter | Docstringen til `sok_anlegg` sier FR4, FR5, men AD-3 knytter ruten til FR4–FR6 | low | patch | Bekreftet. FR6 er meldingen ved ingen treff. Henvisningen rettes direkte. |
| 18 | Edge Case | `010560`, `+42` og lignende skrivemåter gir samme anlegg | false | avvist | Det er ikke noe galt i at samme anlegg svarer. Frontend lager URL-en fra heltallet. |
| 19 | Edge Case | Et anlegg uten valgbare uker kan ikke gi et `Anleggsvar` | false | avvist | Etter AD-14 har alle innebygde anlegg ukene 2025 uke 1 til `SISTE_UKE`. Opplastede data bruker `OpplastetAnlegg` (Epic 3), ikke `Anleggsvar`. |
| 20 | Edge Case | CORS avviser `127.0.0.1:3000` og `localhost:3001` | false | avvist | AD-9 og matrisen i den låste delen av specen krever nettopp dette. |

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
