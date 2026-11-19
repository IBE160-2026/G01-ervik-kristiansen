# Epic 1 Context: Prognose som er testet og målt

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Gruppen får en prognosekjerne som følger reglene R1–R4 og består fasiten T1–T12, og et backtest-skript som måler treffandel og presisjon på hele BarentsWatch-utdraget (2025 uke 1 til 2026 uke 42). Tallene avgjør om suksesskriteriet M1 holder (treffandel minst 25 %, presisjon minst 20 %) før noe brukergrensesnitt bygges. Ingen stories i Epic 2 eller 3 starter før backtesten er kjørt og rapportert (Story 1.7).

## Stories

- Story 1.1: Grunnmur for backend og kjerne
- Story 1.2: Lusegrense og område (R1)
- Story 1.3: Datasett fra BarentsWatch-utdraget
- Story 1.4: Trend og uker til grensen (R2 og R3)
- Story 1.5: Status etter R4
- Story 1.6: Backtest etter SK2
- Story 1.7: Første backtestkjøring og rapport (A5)

## Requirements & Constraints

- Grense: 0,2 i uke 16–21 (sør) og uke 21–26 (nord), ellers 0,5. En verdi ≥ grensen er brudd. Område kommer fra fylket (Nordland, Troms, Finnmark og tidligere «Troms og Finnmark» er nord, alle andre sør). Mangler fylket, er området ukjent, og da finnes ingen grense.
- En uke med telling har en verdi i `Voksne hunnlus`. Uker uten verdi fylles aldri inn.
- Trend: lineær regresjon over vinduet t − 4 til t, der t er siste uke med telling til og med analyseuka (høyst én uke eldre, ellers «ingen ny telling»). Minst 3 tellinger, løpende ukenummer som x-verdi (årsskiftet er ett steg), estimatet avrundet til 2 desimaler med halvdeler opp, og negative estimater settes til 0. Horisont 6 uker regnet fra analyseuka, og hvert estimat sammenlignes med grensen i sin egen uke.
- Status i rekkefølgen ukjent område, ingen ny telling, brudd nå, for lite data, prognose. Rød er 0–3 uker (brudd nå er 0), gul 4–6, grønn ingen kryssing, grå ingen prognose. Statustekstene skal være tegn for tegn like briefen.
- Backtest (SK2): status for uke a regnes bare med data til og med a. Treff er en kryssing der en sammenhengende rød periode begynte 2–4 uker før. Presisjon er andelen «✕ Varsel»-uker med brudd i de 4 neste ukene. Kryssinger før 2025 uke 9 og varsler etter 2026 uke 38 holdes utenfor og telles opp.
- Parameterne (vindu 5, minst 3 tellinger, horisont 6, rød ved 0–3 uker) fryses før backtesten, og resultatet rapporteres uendret, også under tersklene.
- Ingen KI eller språkmodell i prognosen. Ingen hemmeligheter, nøkler eller miljøvariabler. Alt kjører lokalt uten nett, bortsett fra installasjon.
- `uv run pytest` kjører alle backendtester med én kommando, beskrevet i README. R1 testes også mot BarentsWatch-kolonnen `Lusegrense uke`, med 0 avvik.
- README oppgir datakilde (BarentsWatch, «Lakselus per fisk»), lisens (NLOD) og nedlastingsdato (27.10.2026).

## Technical Decisions

- Funksjonell kjerne og imperativt skall: `backend/src/marin/kjerne/` er rene funksjoner som bare importerer stdlib (ingen I/O, ingen klokke). En test sjekker importene. `kilder/`, `forbered/`, `backtest/` og senere `api/` er tynne skall.
- Én inngang: `vurder(serie, omrade, analyseuke)` tar hele serien og ser selv bort fra tellinger etter analyseuka. Appen og backtesten bruker den samme inngangen og kutter aldri serien selv.
- Typer i `marin.kjerne.modeller`: `Uke(ar, uke)`, `Telling(uke, verdi: Decimal | None)`, `Serie(tellinger)` (sortert, én telling per uke, `ValueError` ved duplikater eller ugyldige uker) og `AnleggInfo(lokalitetsnr, navn, kommune, fylke)`, der alle feltene kan mangle. Område er aldri et felt, men alltid et eget argument.
- `marin.kjerne.uker` er den eneste ISO-kalenderen (`neste`, `pluss`, `mellom`, `alle_uker`, `har_uke_53`). «Nå» er konstanten `SISTE_UKE = Uke(2026, 42)`, og kjernen leser aldri klokka.
- Tall er `Decimal` og avrundes med `ROUND_HALF_UP` til 2 desimaler, både inndata og estimater. `round()` brukes aldri på lusetall. Regresjonen bruker ikke flyttall.
- Status har koder: `farge ∈ {rod, gul, gronn, gra}`, `arsak ∈ {varsel, brudd_na, folg_med, ingen_kryssing, for_lite_data, ingen_ny_telling, ukjent_omrade}`, `symbol`, `tekst` (R4 uten symbol) og `uke_tekst` («(uke Y)» eller `null`). Uker skrives med år når de ligger i et annet år enn analyseuka.
- `format_lus`/`format_uke` gir desimalkomma og «uke 42, 2026», testet mot `backend/tests/data/format.json`, som frontend senere tester mot.
- `marin.kilder.barentswatch` er den eneste leseren for BarentsWatch-Excel (openpyxl): bytes inn, `[(AnleggInfo, Serie)]` + feil ut. Duplikatnøkkelen er `(lokalitetsnr, år, uke)`, og fylket hentes fra nyeste rad. Openpyxl gir lusetall som `float` eller `int`, med høyst 2 desimaler i utdraget.
- `uv run python -m marin.forbered` → `backend/src/marin/data/datasett.json` (kuttet etter `SISTE_UKE`, med sha256 for kildefilene). `uv run python -m marin.backtest` → `backend/src/marin/data/backtest.json` (`versjon`, `parametere`, `siste_uke`, antall og andeler 0–1). Begge committes og leses med `importlib.resources`.
- Stack: Python 3.14, uv ≥ 0.12, openpyxl 3.1.5 og pytest 9.2.0. Identifikatorer bruker norske fagord uten æ, ø og å, i `snake_case`.

## Cross-Story Dependencies

- 1.1 → 1.2 → (1.3 dataspor ∥ 1.4 regelspor) → 1.5 → 1.6 → 1.7. Story 1.3 trenger `omrade_fra_fylke` og `grense` fra 1.2 til NFR3-testen.
- Story 1.7 kan endre FR19-teksten og storyene i Epic 2. Epic 2 leser `datasett.json` og `backtest.json` fra denne epicen.
