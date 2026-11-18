---
title: "A4: kontroll av fasit (T5, T6, T8, T10, T11, T12)"
status: bekreftet
created: 2026-11-18
regnet_av: "Claude (KI), med eksakte brøker, 2026-11-18"
kontrollert_av: "Fredrik Ervik"
dato_kontrollert: 2026-11-18
---

# A4: kontroll av fasit

**Slik ble kontrollen gjort.** Briefen (R6) sier at fasiten skal regnes ut av gruppen for hånd. Gruppen valgte 2026-11-18 i stedet at Claude regner med alle mellomregninger vist, og at gruppen kontrollerer hvert steg med kalkulator. Claude regnet med eksakte brøker, ikke flyttall, for å unngå avrundingsfeil. Kontrollen er dermed ikke helt uavhengig av KI. Det er gruppens kontroll av mellomregningene som gjør den til en kontroll. Fyll inn navn og dato i `kontrollert_av` og `dato_kontrollert` når dere har gått gjennom alle steg.

## Fremgangsmåte (fra R1–R4 i briefen)

Stegene gås gjennom i denne rekkefølgen. Det første steget som slår til, gir status (R4).

1. **Område og grense (R1).** Sør: 0,2 i uke 16–21, ellers 0,5. En verdi ≥ grensen er brudd.
2. **t (R2).** Siste uke med telling til og med analyseuka a. Er t eldre enn a − 1, blir status «– Ingen ny telling siden uke t».
3. **Brudd nå (R2).** Er verdien i uke t ≥ grensen i analyseuka, blir status «✕ Brudd nå».
4. **Vinduet (R2).** Uke t − 4 til og med t. Færre enn 3 tellinger gir «– For lite data».
5. **Trendlinje (R2).** x er løpende ukenummer. b = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)². Estimat ŷ = ȳ + b · (x − x̄), avrundet til 2 desimaler, halvdeler opp.
6. **Uker til grensen (R2, R3).** Den første k (1–6) der estimatet i uke a + k er ≥ grensen *i den uka*.
7. **Status (R4).** 1–3 uker gir rød, 4–6 uker gul, og ingen kryssing gir grønn.

## T5

**Inndata:** sør, analyseuke 34. Uke 30–34: 0,06 / 0,12 / 0,18 / 0,24 / 0,30.

| Steg | Mellomregning | Resultat |
|---|---|---|
| Grense i uke 34 | sør, uke 34 er utenfor 16–21 | 0,5 |
| t | siste telling ≤ 34 | 34 |
| Ingen ny telling? | 34 ≥ 33 | nei |
| Brudd nå? | 0,30 < 0,5 | nei |
| Tellinger i vinduet (30–34) | 5 | ≥ 3, ok |
| x̄, ȳ | (30+31+32+33+34)/5 · (0,06+0,12+0,18+0,24+0,30)/5 | 32 · 0,18 |
| Σ(x − x̄)² | 4 + 1 + 0 + 1 + 4 | 10 |
| Σ(x − x̄)(y − ȳ) | (−2)(−0,12) + (−1)(−0,06) + 0 + (1)(0,06) + (2)(0,12) | 0,60 |
| b | 0,60 / 10 | 0,06 |

| k | Uke | Estimat 0,18 + 0,06 · (uke − 32) | Grense | ≥ grensen? |
|---|---|---|---|---|
| 1 | 35 | 0,36 | 0,5 | nei |
| 2 | 36 | 0,42 | 0,5 | nei |
| 3 | 37 | 0,48 | 0,5 | nei |
| 4 | 38 | 0,54 | 0,5 | **ja** |

**Resultat:** grensen nås om 4 uker (uke 38). Status gul: «! Følg med: grensen kan nås om 4 uker».

## T6

**Inndata:** sør, analyseuke 14. Uke 10–14: 0,10 / 0,12 / 0,14 / 0,16 / 0,18.

| Steg | Mellomregning | Resultat |
|---|---|---|
| Grense i uke 14 | sør, uke 14 er utenfor 16–21 | 0,5 |
| t, ingen ny telling, brudd nå | t = 14, 0,18 < 0,5 | nei, nei |
| Tellinger i vinduet (10–14) | 5 | ok |
| x̄, ȳ | 12 · 0,14 | |
| Σ(x − x̄)² · Σ(x − x̄)(y − ȳ) | 10 · (−2)(−0,04) + (−1)(−0,02) + 0 + 0,02 + 0,08 = 0,20 | |
| b | 0,20 / 10 | 0,02 |

| k | Uke | Estimat 0,14 + 0,02 · (uke − 12) | Grense i uka | ≥ grensen? |
|---|---|---|---|---|
| 1 | 15 | 0,20 | 0,5 | nei |
| 2 | 16 | 0,22 | **0,2** (vårperiode) | **ja** |

**Resultat:** grensen nås om 2 uker (uke 16). Status rød: «✕ Varsel: grensen nås om 2 uker».

**Ekstra:** med 0,5 i alle ukene blir høyeste estimat 0,30 i uke 20, som er under 0,5. Status ville da feilaktig blitt grønn.

## T8

**Inndata:** sør, analyseuke 40. Telling i uke 36 (0,20), 38 (0,28) og 40 (0,36). Ikke telt i uke 37 og 39.

| Steg | Mellomregning | Resultat |
|---|---|---|
| Grense i uke 40 | sør | 0,5 |
| t, ingen ny telling, brudd nå | t = 40, 0,36 < 0,5 | nei, nei |
| Tellinger i vinduet (36–40) | uke 36, 38, 40 | 3, ok |
| x̄, ȳ | (36+38+40)/3 · (0,20+0,28+0,36)/3 | 38 · 0,28 |
| Σ(x − x̄)² | 4 + 0 + 4 | 8 |
| Σ(x − x̄)(y − ȳ) | (−2)(−0,08) + 0 + (2)(0,08) | 0,32 |
| b | 0,32 / 8 | 0,04 per uke |

| k | Uke | Estimat 0,28 + 0,04 · (uke − 38) | Grense | ≥ grensen? |
|---|---|---|---|---|
| 1 | 41 | 0,40 | 0,5 | nei |
| 2 | 42 | 0,44 | 0,5 | nei |
| 3 | 43 | 0,48 | 0,5 | nei |
| 4 | 44 | 0,52 | 0,5 | **ja** |

**Resultat:** grensen nås om 4 uker (uke 44). Status gul: «! Følg med: grensen kan nås om 4 uker».

**Ekstra:** med tellingsnummer 1, 2, 3 som x blir b = 0,08. Brukes det som stigning per uke, gir 0,36 + 0,08 · 2 = 0,52 i uke 42. Status ville da feilaktig blitt rød (2 uker).

## T10

**Inndata:** samme tellinger som i T8, ingen telling i uke 41–42.

**T10a, analyseuke 42:** t = 40. Siden 40 < 42 − 1 = 41, er siste telling mer enn én uke eldre enn analyseuka. Status grå: «– Ingen ny telling siden uke 40». Ingen prognose.

**T10b, analyseuke 41:** t = 40, og 40 ≥ 41 − 1, så det blir prognose. Vinduet og linja er de samme som i T8 (b = 0,04), men k telles fra uke 41.

| k | Uke | Estimat | Grense | ≥ grensen? |
|---|---|---|---|---|
| 1 | 42 | 0,44 | 0,5 | nei |
| 2 | 43 | 0,48 | 0,5 | nei |
| 3 | 44 | 0,52 | 0,5 | **ja** |

**Resultat:** grensen nås om 3 uker (uke 44). Status rød: «✕ Varsel: grensen nås om 3 uker».

## T11

**Inndata:** sør, analyseuke 30. Telling bare i uke 29 (0,30) og 30 (0,60).

| Steg | Mellomregning | Resultat |
|---|---|---|
| Grense i uke 30 | sør | 0,5 |
| t, ingen ny telling | t = 30 | nei |
| Brudd nå? | 0,60 ≥ 0,5 | **ja**, slår til her |
| (Tellinger i vinduet) | 2, som ville gitt «for lite data» | sjekkes ikke, siden brudd nå kommer først |

**Resultat:** status rød: «✕ Brudd nå», ikke «For lite data».

## T12

**Inndata:** sør, analyseuke 2026 uke 2. 2025 har 52 ISO-uker. Tellinger: 0,30 / 0,34 / 0,38 / 0,42 / 0,46.

| Uke | 2025 u50 | 2025 u51 | 2025 u52 | 2026 u1 | 2026 u2 |
|---|---|---|---|---|---|
| Løpende x (startuke 2025 u50 = 1) | 1 | 2 | 3 | 4 | 5 |

| Steg | Mellomregning | Resultat |
|---|---|---|
| Grense i 2026 uke 2 | sør | 0,5 |
| t, ingen ny telling, brudd nå | t = x 5, 0,46 < 0,5 | nei, nei |
| Tellinger i vinduet | 5 | ok |
| x̄, ȳ | 3 · 0,38 | |
| Σ(x − x̄)² · Σ(x − x̄)(y − ȳ) | 10 · (−2)(−0,08) + (−1)(−0,04) + 0 + 0,04 + 0,16 = 0,40 | |
| b | 0,40 / 10 | 0,04 |

| k | Uke | x | Estimat uavrundet (brøk) | Avrundet | Grense | ≥ grensen? |
|---|---|---|---|---|---|---|
| 1 | 2026 u3 | 6 | 0,38 + 0,04 · 3 = 1/2 = 0,50 nøyaktig | 0,50 | 0,5 | **ja** |

**Resultat:** grensen nås om 1 uke (2026 uke 3). Status rød: «✕ Varsel: grensen nås om 1 uke».

**Ekstra:** med ISO-uka direkte som x (50, 51, 52, 1, 2) blir b ≈ −0,002, altså svakt fallende, og status ville feilaktig blitt grønn. Estimatet i uke 3 er nøyaktig 0,50 bare i eksakt regning. Med flyttall kan regresjonen gi 0,4999…, som uten avrunding er under grensen. Derfor kreves `Decimal` og avrunding med halvdeler opp (arkitektur AD-6).

## Sammenligning med briefen

| Test | Regnet her | Briefen (R6) | Stemmer? |
|---|---|---|---|
| T5 | b 0,06 · 0,48 i u37, 0,54 i u38 · 4 uker · gul | samme | ja |
| T6 | b 0,02 · 0,20 i u15, 0,22 i u16 mot 0,2 · 2 uker · rød · grønn ved feil grense | samme | ja |
| T8 | b 0,04 · 0,48 i u43, 0,52 i u44 · 4 uker · gul · rød ved tellingsnummer | samme | ja |
| T10 | a = 42: ingen ny telling siden uke 40 · a = 41: 3 uker, rød | samme | ja |
| T11 | brudd nå går foran for lite data · rød «✕ Brudd nå» | samme | ja |
| T12 | b 0,04 · 0,50 i 2026 u3 · 1 uke · rød · grønn ved ISO-uke direkte | samme | ja |

Når gruppen har bekreftet mellomregningene, fjernes merkingen «[FASIT MÅ KONTROLLERES FOR HÅND AV GRUPPEN]» i briefen. PRD A4 og kap. 11 oppdateres slik at de beskriver hvordan kontrollen faktisk ble gjort.
