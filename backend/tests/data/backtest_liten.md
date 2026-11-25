# Fasit for det lille backtest-datasettet (Story 1.6, NFR10)

`backtest_liten.json` er et lite, konstruert datasett i samme format som `datasett.json`. Tallene under er regnet ut for hånd etter SK2 og R4, med begrunnelse per anlegg. `test_treffsikkerhet.py` leser tabellen «Fasit» nederst og sjekker den mot `backtest` på datasettet.

KI laget datasettet og regnet ut tallene 2026-11-25. Gruppen kontrollerer tallene for hånd før PR-en flettes, som med A4.

Kontrollert for hånd av: ______________________ Dato: ____________

## Reglene som brukes

**Status for uke a (R4).** Status regnes for hver uke fra uke 1, 2025 til uke 42, 2026, med tellingene til og med a. Reglene prøves i denne rekkefølgen:

1. Ukjent område: «? Ukjent område» (grå).
2. Siste telling t er mer enn én uke eldre enn a: «Ingen ny telling» (grå).
3. Verdien i t er på eller over grensen i uke a: «✕ Brudd nå» (rød).
4. Færre enn 3 tellinger i uke t − 4 til t, eller ingen telling til og med a: «For lite data» (grå).
5. Trend: b = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)², og estimatet i uke a + k er ȳ + b · (x − x̄), avrundet til 2 desimaler med halvdeler opp. Første k fra 1 til 6 der estimatet er på eller over grensen i uke a + k, gir «✕ Varsel» (rød) når k er 1–3 og «! Følg med» (gul) når k er 4–6. Ingen slik k gir «✓ Ingen kryssing» (grønn).

En uke uten verdi er ikke en telling. Status kan bare være noe annet enn «For lite data» eller «Ingen ny telling» i uker med telling i a eller a − 1. Derfor står bare de ukene i tabellene. Alle andre uker er grå.

Alle tellingene for hvert anlegg ligger innenfor ett år. Da er løpende ukenummer lik ukenummeret pluss en konstant, og vi regner med ukenummeret som x.

**Grensen.** 0,2 i uke 16–21 i sør og uke 21–26 i nord, ellers 0,5. Alle ukene som brukes under (også de 4 ukene etter hvert varsel), har grensen 0,5.

**SK2.**

- Kryssing: uke w med telling på eller over grensen i uke w, der forrige telling, i w − 1 eller ellers w − 2, er under grensen i sin uke.
- Treff: den sammenhengende perioden med rød status som slutter i w − 1, begynte i w − 4, w − 3 eller w − 2.
- Varsel fulgt av brudd: minst én telling på eller over grensen i a + 1 til a + 4.
- Kryssinger før uke 9, 2025 og varsler etter uke 38, 2026 holdes utenfor og telles for seg.

## Anlegg A (lokalitet 1, Vestland, sør): treff

| Uke 2025 | Telling | Status | Begrunnelse |
| --- | --- | --- | --- |
| 30 | 0,10 | For lite data | 1 telling i vinduet |
| 31 | 0,20 | For lite data | 2 tellinger |
| 32 | 0,30 | ✕ Varsel, 2 uker | Tellinger 30–32, b = 0,10, x̄ = 31, ȳ = 0,20. Estimat uke 33 = 0,40, uke 34 = 0,50 ≥ 0,5, så k = 2 |
| 33 | 0,40 | ✕ Varsel, 1 uke | Tellinger 30–33, b = 0,10, x̄ = 31,5, ȳ = 0,25. Estimat uke 34 = 0,25 + 0,10 · 2,5 = 0,50, så k = 1 |
| 34 | 0,50 | ✕ Brudd nå | 0,50 ≥ 0,5 |
| 35 | – | ✕ Brudd nå | Siste telling er uke 34, én uke gammel, og 0,50 ≥ 0,5 |
| 36 og senere | – | Ingen ny telling | |

- Kryssing i uke 34: 0,50 ≥ 0,5, og forrige telling (uke 33) er 0,40 < 0,5. Uke 31–33 er under grensen og er ikke kryssinger.
- Rød i uke 32 og 33, grå i uke 31. Perioden begynte i uke 32 = w − 2, så kryssingen er et **treff**.
- Varsel i uke 32: uke 33–36 har brudd i uke 34, så det er **fulgt av brudd**.
- Varsel i uke 33: uke 34–37 har brudd i uke 34, så det er **fulgt av brudd**.

Bidrag: 1 kryssing, 1 treff, 2 varsler, 2 fulgt av brudd.

## Anlegg B (lokalitet 2, Nordland, nord): rød bare uka før

Vårgrensen i nord gjelder uke 21–26, så grensen er 0,5 i alle ukene her.

| Uke 2025 | Telling | Status | Begrunnelse |
| --- | --- | --- | --- |
| 40 | 0,10 | For lite data | 1 telling |
| 41 | 0,10 | For lite data | 2 tellinger |
| 42 | 0,10 | ✓ Ingen kryssing | Tellinger 40–42, b = 0, estimatet er 0,10 i uke 43–48 |
| 43 | 0,40 | ✕ Varsel, 3 uker | Se under |
| 44 | 0,60 | ✕ Brudd nå | 0,60 ≥ 0,5 |
| 45 | – | ✕ Brudd nå | Siste telling er uke 44, og 0,60 ≥ 0,5 |
| 46 og senere | – | Ingen ny telling | |

Uke 43: tellinger 40–43 er 0,10, 0,10, 0,10 og 0,40. x̄ = 41,5 og ȳ = 0,175. Σ(x − x̄)² = 2,25 + 0,25 + 0,25 + 2,25 = 5. Σ(x − x̄)(y − ȳ) = (−1,5)(−0,075) + (−0,5)(−0,075) + (0,5)(−0,075) + (1,5)(0,225) = 0,1125 + 0,0375 − 0,0375 + 0,3375 = 0,45. b = 0,45 / 5 = 0,09. Estimat uke 44 = 0,175 + 0,09 · 2,5 = 0,40, uke 45 = 0,49 og uke 46 = 0,58 ≥ 0,5, så k = 3.

- Kryssing i uke 44: 0,60 ≥ 0,5, og forrige telling (uke 43) er 0,40 < 0,5.
- Rød bare i uke 43, grønn i uke 42. Perioden begynte i w − 1, så kryssingen er **ikke treff**.
- Varsel i uke 43: uke 44–47 har brudd i uke 44, så det er **fulgt av brudd**.

Bidrag: 1 kryssing, 0 treff, 1 varsel, 1 fulgt av brudd.

## Anlegg C (lokalitet 3, Vestland, sør): rød fra 5 uker før

| Uke 2026 | Telling | Status | Begrunnelse |
| --- | --- | --- | --- |
| 23 | 0,20 | For lite data | 1 telling |
| 24 | 0,30 | For lite data | 2 tellinger |
| 25 | 0,40 | ✕ Varsel, 1 uke | Tellinger 23–25, b = 0,10, x̄ = 24, ȳ = 0,30. Estimat uke 26 = 0,30 + 0,10 · 2 = 0,50, så k = 1 |
| 26 | 0,42 | ✕ Varsel, 1 uke | Se under |
| 27 | 0,44 | ✕ Varsel, 1 uke | Se under |
| 28 | 0,46 | ✕ Varsel, 1 uke | Se under |
| 29 | 0,48 | ✕ Varsel, 1 uke | Tellinger 25–29, b = 0,02, x̄ = 27, ȳ = 0,44. Estimat uke 30 = 0,44 + 0,02 · 3 = 0,50, så k = 1 |
| 30 | 0,50 | ✕ Brudd nå | 0,50 ≥ 0,5 |
| 31 | – | ✕ Brudd nå | Siste telling er uke 30, og 0,50 ≥ 0,5 |
| 32 og senere | – | Ingen ny telling | |

Uke 26: tellinger 23–26 er 0,20, 0,30, 0,40 og 0,42. x̄ = 24,5 og ȳ = 1,32 / 4 = 0,33. Σ(x − x̄)² = 5. Σ(x − x̄)(y − ȳ) = (−1,5)(−0,13) + (−0,5)(−0,03) + (0,5)(0,07) + (1,5)(0,09) = 0,195 + 0,015 + 0,035 + 0,135 = 0,38. b = 0,076. Estimat uke 27 = 0,33 + 0,076 · 2,5 = 0,52, så k = 1.

Uke 27: tellinger 23–27 er 0,20, 0,30, 0,40, 0,42 og 0,44. x̄ = 25 og ȳ = 1,76 / 5 = 0,352. Σ(x − x̄)² = 10. Σ(x − x̄)(y − ȳ) = (−2)(−0,152) + (−1)(−0,052) + 0 + (1)(0,068) + (2)(0,088) = 0,304 + 0,052 + 0,068 + 0,176 = 0,60. b = 0,06. Estimat uke 28 = 0,352 + 0,06 · 3 = 0,532, avrundet 0,53, så k = 1.

Uke 28: tellinger 24–28 er 0,30, 0,40, 0,42, 0,44 og 0,46. x̄ = 26 og ȳ = 2,02 / 5 = 0,404. Σ(x − x̄)² = 10. Σ(x − x̄)(y − ȳ) = (−2)(−0,104) + (−1)(−0,004) + 0 + (1)(0,036) + (2)(0,056) = 0,208 + 0,004 + 0,036 + 0,112 = 0,36. b = 0,036. Estimat uke 29 = 0,404 + 0,036 · 3 = 0,512, avrundet 0,51, så k = 1.

- Kryssing i uke 30: 0,50 ≥ 0,5, og forrige telling (uke 29) er 0,48 < 0,5.
- Rød i uke 25–29, grå i uke 24. Perioden begynte i uke 25 = w − 5, så kryssingen er **ikke treff**.
- Varsel i uke 25: uke 26–29 har 0,42–0,48, alle under 0,5, så det er **ikke fulgt av brudd**.
- Varsel i uke 26, 27, 28 og 29: uke 30 ligger blant de 4 neste ukene, så alle fire er **fulgt av brudd**.

Bidrag: 1 kryssing, 0 treff, 5 varsler, 4 fulgt av brudd.

## Anlegg D (lokalitet 4, Troms, nord): brudd etter to uker uten telling

| Uke 2025 | Telling | Status | Begrunnelse |
| --- | --- | --- | --- |
| 44 | 0,40 | For lite data | 1 telling |
| 45 | tom | For lite data | Siste telling er uke 44, én uke gammel, og 0,40 < 0,5. Bare 1 telling i vinduet |
| 46 | tom | Ingen ny telling | Siste telling er uke 44, to uker gammel |
| 47 | 0,60 | ✕ Brudd nå | 0,60 ≥ 0,5 |
| 48 | – | ✕ Brudd nå | Siste telling er uke 47, og 0,60 ≥ 0,5 |
| 49 og senere | – | Ingen ny telling | |

- Uke 47 er på eller over grensen, men verken uke 46 eller uke 45 har telling, så uke 47 er **ikke en kryssing**.
- Ingen varsler.

Bidrag: ingenting.

## Anlegg E (lokalitet 5, Vestland, sør): kryssing før uke 9, 2025

| Uke 2025 | Telling | Status | Begrunnelse |
| --- | --- | --- | --- |
| 7 | 0,30 | For lite data | 1 telling |
| 8 | 0,60 | ✕ Brudd nå | 0,60 ≥ 0,5 |
| 9 | – | ✕ Brudd nå | Siste telling er uke 8, og 0,60 ≥ 0,5 |
| 10 og senere | – | Ingen ny telling | |

- Kryssing i uke 8: 0,60 ≥ 0,5, og forrige telling (uke 7) er 0,30 < 0,5. Uke 8, 2025 er før uke 9, 2025, så kryssingen **holdes utenfor**.
- Ingen varsler.

Bidrag: 1 utelatt kryssing.

## Anlegg F (lokalitet 6, Vestland, sør): varsel i uke 38 og 39, 2026

| Uke 2026 | Telling | Status | Begrunnelse |
| --- | --- | --- | --- |
| 36 | 0,30 | For lite data | 1 telling |
| 37 | 0,36 | For lite data | 2 tellinger |
| 38 | 0,42 | ✕ Varsel, 2 uker | Tellinger 36–38, b = 0,06, x̄ = 37, ȳ = 0,36. Estimat uke 39 = 0,48, uke 40 = 0,54 ≥ 0,5, så k = 2 |
| 39 | – | ✕ Varsel, 1 uke | Siste telling er uke 38, én uke gammel, og 0,42 < 0,5. Samme trend: estimat uke 40 = 0,54, så k = 1 |
| 40 og senere | – | Ingen ny telling | |

- Ingen kryssing, fordi ingen telling er på eller over 0,5.
- Varsel i uke 38: uke 39–42 har ingen tellinger, så det er **ikke fulgt av brudd**. Uke 38 er ikke etter uke 38, så varselet telles.
- Varsel i uke 39: etter uke 38, 2026, så det **holdes utenfor**.

Bidrag: 1 varsel, 0 fulgt av brudd, 1 utelatt varsel.

## Anlegg G (lokalitet 7, fylke mangler): ukjent område

Tellingene er de samme som for anlegg A. Uten fylke er området ukjent, og da finnes ingen grense. Alle ukene får «? Ukjent område», og det blir ingen kryssinger og ingen varsler. I sør ville anlegget gitt det samme som anlegg A.

Bidrag: ingenting.

## Sum per anlegg

| Anlegg | Område | Kryssinger | Treff | Varsler | Fulgt av brudd | Utelatte kryssinger | Utelatte varsler |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | sør | 1 | 1 | 2 | 2 | 0 | 0 |
| B | nord | 1 | 0 | 1 | 1 | 0 | 0 |
| C | sør | 1 | 0 | 5 | 4 | 0 | 0 |
| D | nord | 0 | 0 | 0 | 0 | 0 | 0 |
| E | sør | 0 | 0 | 0 | 0 | 1 | 0 |
| F | sør | 0 | 0 | 1 | 0 | 0 | 1 |
| G | ukjent | 0 | 0 | 0 | 0 | 0 | 0 |
| Sum | | 3 | 1 | 9 | 7 | 1 | 1 |

Treffandel = 1 / 3 = 0,33333…, avrundet til 4 desimaler 0,3333 (33,3 % i terminalen).
Presisjon = 7 / 9 = 0,77777…, avrundet til 4 desimaler 0,7778 (77,8 % i terminalen).

## Fasit

Verdiene står som i `backtest.json`, med desimalpunkt.

| Felt | Verdi |
| --- | --- |
| `antall_kryssinger` | 3 |
| `antall_treff` | 1 |
| `antall_varsler` | 9 |
| `antall_varsler_med_brudd` | 7 |
| `utelatt_kryssinger` | 1 |
| `utelatt_varsler` | 1 |
| `treffandel` | 0.3333 |
| `presisjon` | 0.7778 |
