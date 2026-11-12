---
title: "DESIGN: Marin"
status: final
created: 2026-11-11
updated: 2026-11-12
sources:
  - ../../prds/prd-Marin-2026-11-02/prd.md
  - ../../briefs/brief-Marin-2026-09-17/brief.md
name: Marin
description: Prognose for lakselus per anlegg. Rolig rapport på hvit flate, én dyp marineblå aksent, full statusfarge bare i den store statusboksen. Kun lys modus i v1.
colors:
  # Grunnpalett – tema 3 «Klar hvit». Flater skilles med kant, ikke tone.
  surface: '#FFFFFF'
  ink: '#111418'              # 18,5:1 mot surface
  ink-secondary: '#4A5059'    # 8,1:1 mot surface
  border: '#E3E6EA'           # skillelinjer og kort; dekorativ, ikke bærende
  border-strong: '#8A919A'    # 3,2:1 mot surface; stiplet grå status, analyseukelinje i graf
  accent: '#0B3D91'           # 10,0:1; eneste kulør utenom status
  on-accent: '#FFFFFF'
  accent-tint: '#E7EDF7'
  # Status – semantiske roller (R4). fill/on-fill brukes BARE i statusboksen.
  # symbol = farge på symbolet i nøytrale merker, graf og tabell (hvit bakgrunn).
  # Rød og grønn fill står bare i 1,06:1 mot hverandre (lik lyshet): status skilles på symbol og tekst.
  status-red-fill: '#B3261E'
  status-red-on-fill: '#FFFFFF'     # 6,5:1
  status-red-border: '#B3261E'
  status-red-symbol: '#B3261E'      # 6,5:1 mot hvit
  status-yellow-fill: '#F5B800'
  status-yellow-on-fill: '#1A1400'  # 10,3:1
  status-yellow-border: '#8A6A00'   # 5,1:1 mot hvit; gul flate mot hvit er bare 1,8:1 – kanten er påbudt
  status-yellow-symbol: '#1A1400'   # gul som tekst på hvit er uleselig; symbolet bruker mørk tone
  status-green-fill: '#1B6E4F'
  status-green-on-fill: '#FFFFFF'   # 6,2:1
  status-green-border: '#1B6E4F'
  status-green-symbol: '#1B6E4F'    # 6,2:1 mot hvit
  status-grey-fill: '#FFFFFF'
  status-grey-on-fill: '#3F4650'    # 9,5:1
  status-grey-border: '#8A919A'     # alltid stiplet
  status-grey-symbol: '#3F4650'
typography:
  # Systemfonter: ingen nedlasting, lett side på svak mobildekning.
  title:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 34px
    fontWeight: '600'
    letterSpacing: -0.01em
  title-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 28px
    fontWeight: '600'
    letterSpacing: -0.01em
  section-heading:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 20px
    fontWeight: '600'
  section-heading-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 18px
    fontWeight: '600'
  body:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.55'
  body-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.55'
  status-headline:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 26px
    fontWeight: '700'
    lineHeight: '1.25'
  status-headline-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 21px
    fontWeight: '700'
    lineHeight: '1.25'
  status-symbol:
    # Minst 32px på alle bredder; står i hvit sirkel (components.status-symbol-badge).
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 32px
    fontWeight: '800'
    lineHeight: '1'
  status-name:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 18px
    fontWeight: '700'
  meta:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '400'
  meta-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 14px
    fontWeight: '400'
  table-cell:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 17px
    fontWeight: '400'
  table-cell-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '400'
  caption:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 14px
    fontWeight: '400'
  chart-label:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 13px
    fontWeight: '400'
  pill:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1.2'
  pill-xs:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
  logo:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 20px
    fontWeight: '800'
    letterSpacing: 0.02em
  button:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 17px
    fontWeight: '600'
    lineHeight: '1.2'
  button-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '600'
    lineHeight: '1.2'
  field:
    # Søkefelt, analyseukevelger, filvelger. 16px på mobil hindrer automatisk zoom i iOS.
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 17px
    fontWeight: '400'
    lineHeight: '1.3'
  field-mobile:
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.3'
rounded:
  sm: 4px
  DEFAULT: 6px
  full: 9999px
spacing:
  content-max-width: 760px
  search-max-width: 420px
  page-x: 32px
  page-x-mobile: 16px
  page-top: 36px
  page-top-mobile: 20px
  page-bottom: 48px
  page-bottom-mobile: 32px
  topbar-y: 16px
  topbar-y-mobile: 12px
  topbar-gap: 20px
  section-gap: 40px
  section-gap-mobile: 28px
  heading-gap: 12px
  statusbox-y: 24px
  statusbox-x: 28px
  statusbox-mobile: 18px
  statusbox-line-gap: 10px
  table-cell-y: 14px
  table-cell-x: 8px
  table-cell-y-mobile: 11px
  table-cell-x-mobile: 6px
  uncertainty-top: 40px
  uncertainty-rule-gap: 20px
  pill-y: 3px
  pill-x: 10px
  status-marker: 10px               # liten statusmarkør i statusmerket
  status-symbol-badge-size: 52px    # hvit sirkel rundt statussymbolet i statusboksen
  status-symbol-badge-size-mobile: 46px
  target-min: 44px                  # minste høyde/bredde for trykkflater (mobil) og kontroller (alle bredder)
  target-min-inline: 24px           # minste mål for tekstlenker på desktop
  control-y: 10px                   # felt og nedtrekksliste, innvendig
  control-x: 12px
  button-y: 10px
  button-x: 20px
components:
  top-bar:
    background: '{colors.surface}'
    border-bottom: '{colors.border}'
    logo: '{typography.logo}'
    logo-color: '{colors.accent}'
    padding-x: '{spacing.page-x}'
    padding-y: '{spacing.topbar-y}'
    search: '{components.search-field}'
    search-button: '{components.button-secondary}'
  status-box-red:
    background: '{colors.status-red-fill}'
    foreground: '{colors.status-red-on-fill}'
    border: '2px solid {colors.status-red-border}'
    radius: '{rounded.DEFAULT}'
  status-box-yellow:
    background: '{colors.status-yellow-fill}'
    foreground: '{colors.status-yellow-on-fill}'
    border: '2px solid {colors.status-yellow-border}'
    radius: '{rounded.DEFAULT}'
  status-box-green:
    background: '{colors.status-green-fill}'
    foreground: '{colors.status-green-on-fill}'
    border: '2px solid {colors.status-green-border}'
    radius: '{rounded.DEFAULT}'
  status-box-grey:
    background: '{colors.status-grey-fill}'
    foreground: '{colors.status-grey-on-fill}'
    border: '2px dashed {colors.status-grey-border}'
    radius: '{rounded.DEFAULT}'
  status-symbol-badge:
    # Hvit sirkel med stort symbol i statusboksen; skiller status i gråtoner, sollys og ved fargesynsvikt.
    background: '{colors.surface}'
    radius: '{rounded.full}'
    size: '{spacing.status-symbol-badge-size}'
    size-mobile: '{spacing.status-symbol-badge-size-mobile}'
    typography: '{typography.status-symbol}'
    symbol-red: '{colors.status-red-symbol}'
    symbol-yellow: '{colors.status-yellow-symbol}'
    border-yellow: '2px solid {colors.status-yellow-border}'
    symbol-green: '{colors.status-green-symbol}'
    symbol-grey: '{colors.status-grey-symbol}'
    border-grey: '2px dashed {colors.status-grey-border}'
  status-loading:
    # Lastetilstand i statusboksens plass. Skal ikke ligne grå status: ingen stipling, intet symbol.
    background: '{colors.surface}'
    foreground: '{colors.ink-secondary}'
    border: '1px solid {colors.border}'
    radius: '{rounded.DEFAULT}'
    typography: '{typography.meta}'
  uploaded-data-line:
    # «Dine opplastede tall: <filnavn>» inne i statusboksen; farge arves fra statusboksens foreground.
    typography: '{typography.meta}'
    prefix-weight: '700'
  status-pill:
    background: '{colors.surface}'
    foreground: '{colors.ink}'
    border: '1px solid {colors.border}'
    radius: '{rounded.full}'
    typography: '{typography.pill}'
    padding-y: '{spacing.pill-y}'
    padding-x: '{spacing.pill-x}'
    marker-size: '{spacing.status-marker}'
    marker-radius: '{rounded.full}'
    marker-red: '{colors.status-red-fill}'
    marker-yellow: '{colors.status-yellow-fill}'
    marker-yellow-border: '1px solid {colors.status-yellow-border}'
    marker-green: '{colors.status-green-fill}'
    marker-grey: '{colors.surface}'
    marker-grey-border: '1px dashed {colors.status-grey-border}'
    symbol-red: '{colors.status-red-symbol}'
    symbol-yellow: '{colors.status-yellow-symbol}'
    border-yellow: '1px solid {colors.status-yellow-border}'
    symbol-green: '{colors.status-green-symbol}'
    symbol-grey: '{colors.status-grey-symbol}'
    border-grey: '1px dashed {colors.status-grey-border}'
  analysis-week-select:
    background: '{colors.surface}'
    foreground: '{colors.ink}'
    label: '{colors.ink-secondary}'
    border: '1px solid {colors.border-strong}'
    radius: '{rounded.DEFAULT}'
    typography: '{typography.field}'
    typography-mobile: '{typography.field-mobile}'
    padding-y: '{spacing.control-y}'
    padding-x: '{spacing.control-x}'
    min-height: '{spacing.target-min}'
  search-field:
    background: '{colors.surface}'
    foreground: '{colors.ink}'
    label: '{colors.ink-secondary}'
    border: '1px solid {colors.border-strong}'
    radius: '{rounded.DEFAULT}'
    max-width: '{spacing.search-max-width}'
    typography: '{typography.field}'
    typography-mobile: '{typography.field-mobile}'
    padding-y: '{spacing.control-y}'
    padding-x: '{spacing.control-x}'
    min-height: '{spacing.target-min}'
  hit-list-row:
    title: '{typography.body}'
    meta: '{typography.meta}'
    meta-color: '{colors.ink-secondary}'
    divider: '{colors.border}'
    active-background: '{colors.accent-tint}'
    min-height: '{spacing.target-min}'
  trend-graph:
    measured-point: '{colors.accent}'
    measured-line: '{colors.accent}'
    trend-history: '{colors.accent}'
    trend-forecast: '{colors.accent}'
    limit-line: '{colors.ink}'
    gridline: '{colors.border}'
    analysis-week-line: '{colors.border-strong}'
    not-counted-point: '{colors.border-strong}'
    axis-label: '{colors.ink-secondary}'
    label-typography: '{typography.chart-label}'   # gjengitt størrelse, minst 13 CSS-px ved alle bredder
    crossing-label-background: '{colors.surface}'
    crossing-label-radius: '{rounded.sm}'
    summary-typography: '{typography.meta}'        # synlig tekstoppsummering under grafen
    summary-color: '{colors.ink}'
  week-table:
    header-color: '{colors.ink-secondary}'
    divider: '{colors.border}'
    cell: '{typography.table-cell}'
    cell-padding-y: '{spacing.table-cell-y}'
    cell-padding-x: '{spacing.table-cell-x}'
  uncertainty-text:
    typography: '{typography.meta}'
    color: '{colors.ink-secondary}'
    rule: '{colors.border}'
  status-legend:
    item: '{components.status-pill}'
    description-color: '{colors.ink-secondary}'
  button-primary:
    background: '{colors.accent}'
    foreground: '{colors.on-accent}'
    border: '1px solid {colors.accent}'
    radius: '{rounded.DEFAULT}'
    typography: '{typography.button}'
    typography-mobile: '{typography.button-mobile}'
    padding-y: '{spacing.button-y}'
    padding-x: '{spacing.button-x}'
    min-height: '{spacing.target-min}'
    disabled-background: '{colors.surface}'
    disabled-foreground: '{colors.ink-secondary}'
    disabled-border: '1px solid {colors.border-strong}'
  button-secondary:
    background: '{colors.surface}'
    foreground: '{colors.accent}'
    border: '1px solid {colors.accent}'
    radius: '{rounded.DEFAULT}'
    typography: '{typography.button}'
    typography-mobile: '{typography.button-mobile}'
    padding-y: '{spacing.button-y}'
    padding-x: '{spacing.button-x}'
    min-height: '{spacing.target-min}'
    disabled-background: '{colors.surface}'
    disabled-foreground: '{colors.ink-secondary}'
    disabled-border: '1px solid {colors.border-strong}'
  upload-form:
    field-border: '1px solid {colors.border-strong}'
    field-border-invalid: '2px solid {colors.ink}'
    field-typography: '{typography.field}'
    field-typography-mobile: '{typography.field-mobile}'
    field-padding-y: '{spacing.control-y}'
    field-padding-x: '{spacing.control-x}'
    label: '{colors.ink}'
    help: '{colors.ink-secondary}'
    field-error: '{colors.ink}'
    radio-row-min-height: '{spacing.target-min}'
    radius: '{rounded.DEFAULT}'
  error-message:
    background: '{colors.surface}'
    foreground: '{colors.ink}'
    border: '2px solid {colors.ink}'
    radius: '{rounded.DEFAULT}'
  link:
    color: '{colors.accent}'
  focus-ring:
    outline: '2px solid {colors.accent}'
    offset: 2px
---

## Brand & Style

Marin er en rolig rapport, ikke et kontrollpanel. Driftslederen åpner den på en fast onsdagsrutine og vil ha ett svar: hvor lenge har jeg før grensen nås? Siden leses fra topp til bunn i én kolonne, med stor og lett type og god luft mellom delene. Den skal ikke se uryddig ut, og den skal ikke rope.

Grunnlaget er tema 3 «Klar hvit»: hvit flate, skarp mørk tekst og én dyp marineblå aksent. Temaet ble valgt fordi det leses best i sterkt sollys ute på anlegget. Temaet er i utgangspunktet høylytt, så regelen om *status nøytral* demper det: den eneste store fargeflaten på siden er statusboksen. Øyet lander der først, og boksen kan skjermdumpes alene og sendes videre. Alt annet er hvitt.

Kun lys modus i v1. Mørk modus er utenfor v1.

Visuelle referanser: nøkkelskissene `mockups/key-detaljside.html` (statusboks med statussymbol, graf med tekstoppsummering, ukestabell), `mockups/key-forside.html` (forside med fargeforklaring og trefliste), `mockups/key-opplasting.html` (opplastingsskjema og feilmelding) og `mockups/key-oversikt-skisse.html` (ikke del av v1). Beslutningshistorikk: `.working/color-themes-1.html` (tema 3) og `.working/directions-1.html` (retning A «Rolig rapport»). Ved konflikt mellom skissene og spesifikasjonen gjelder DESIGN.md og EXPERIENCE.md.

## Colors

**Grunnpalett.**

- **Hvit (`{colors.surface}` #FFFFFF)** er både bakgrunn og flate. Flater skilles med kant, ikke med tone.
- **Blekk (`{colors.ink}` #111418, 18,5:1)** er all primærtekst og grenselinja i grafen.
- **Sekundærtekst (`{colors.ink-secondary}` #4A5059, 8,1:1)** brukes til metadata (lokalitetsnr., kommune og fylke), etiketter, aksetekst, tabelloverskrifter og usikkerhetsteksten.
- **Kant (`{colors.border}` #E3E6EA)** er skillelinjer, tabellrader og toppfeltets underkant. Den er for svak til å bære mening alene.
- **Sterk kant (`{colors.border-strong}` #8A919A, 3,2:1)** er den stiplede kanten på grå status, analyseukelinja i grafen og markøren for «ikke telt». Den brukes også som kant på skjemafelt (søk, analyseuke, filvelger), fordi `{colors.border}` ikke gir 3:1 mot hvitt.
- **Aksent (`{colors.accent}` #0B3D91, 10,0:1)** er den eneste kuløren utenom status. Den brukes på lenker, primærknapp, logo, målte punkter og trendlinja i grafen, men aldri som statusfarge.
- **Aksent-tone (`{colors.accent-tint}` #E7EDF7)** markerer aktiv rad i treflisten ved tastaturnavigering. Den brukes ellers ikke i retning A.

**Status (R4).** Fire faste roller. Fargen står aldri alene: alltid farge, symbol og tekst sammen (NFR4).

| Status | Symbol | Full flate (bare statusboks) | Kant | Symbol på hvit (merker, graf, tabell) |
|---|---|---|---|---|
| Rød – brudd nå / varsel | ✕ | `{colors.status-red-on-fill}` på `{colors.status-red-fill}`, 6,5:1 | `{colors.status-red-border}` | `{colors.status-red-symbol}`, 6,5:1 |
| Gul – følg med | ! | `{colors.status-yellow-on-fill}` på `{colors.status-yellow-fill}`, 10,3:1 | `{colors.status-yellow-border}` (påbudt) | `{colors.status-yellow-symbol}` med kant `{colors.status-yellow-border}` |
| Grønn – ingen kryssing | ✓ | `{colors.status-green-on-fill}` på `{colors.status-green-fill}`, 6,2:1 | `{colors.status-green-border}` | `{colors.status-green-symbol}`, 6,2:1 |
| Grå – ingen prognose | – / ? | `{colors.status-grey-on-fill}` på hvit, 9,5:1 | `{colors.status-grey-border}`, stiplet | `{colors.status-grey-symbol}` med stiplet kant |

**Kjent begrensning: rød og grønn har samme lyshet.** Rød (#B3261E) og grønn (#1B6E4F) står bare i 1,06:1 mot hverandre og skilles kun på kulør. Ved rød-grønn fargesynsvikt, i sterkt sollys og i et skjermbilde i gråtoner blir de to flatene nesten like. Paletten beholdes. Derfor er det symbolet og teksten som skiller statusene, ikke fargen:

- I statusboksen står symbolet stort, minst 32px (`{typography.status-symbol}`), i en hvit sirkel (`{components.status-symbol-badge}`) med symbolet i statusens `*-symbol`-farge. ✕, !, ✓ og – / ? skiller da statusene på avstand, i gråtoner og ved fargesynsvikt.
- README-sjekklista (NFR10) får et punkt: statusboksene for rød, gul, grønn og grå kontrolleres i gråtoner og med deuteranopi-simulering.

Gul flate mot hvitt gir bare 1,8:1, så gul har alltid mørk kant (`{colors.status-yellow-border}`, 5,1:1 mot hvitt). Gul brukes aldri som tekst- eller symbolfarge på hvitt.

**Status nøytral.** Full statusfarge (`*-fill`) brukes bare i den store statusboksen. Små statusmerker, grafmarkøren og tabellen er hvite, og bare symbolet (og for gul og grå: kanten) bærer statusfargen. Unntaket er en liten rund statusmarkør (`{spacing.status-marker}`, 10px) i statusmerket, i statusens `*-fill` (gul med `{colors.status-yellow-border}`-kant, grå hvit med stiplet kant). Markøren gjør at gul faktisk ser gul ut i fargeforklaringen, slik at merket kan kobles til den gule statusboksen. Merket selv er fortsatt hvitt.

## Typography

Systemfonter (`system-ui`-stabelen). Ingen fontnedlasting, slik at siden er lett på svak mobildekning.

| Rolle | Desktop | Mobil | Brukes til |
|---|---|---|---|
| `title` | 34px / 600 | `title-mobile` 28px | Anleggsnavn øverst på detaljsiden |
| `section-heading` | 20px / 600 | `section-heading-mobile` 18px | «Lusetall og trend», «De siste 5 ukene» |
| `body` | 18px / 400 / 1,55 | `body-mobile` 16px | Brødtekst, forsideintro, trefliste |
| `status-headline` | 26px / 700 / 1,25 | `status-headline-mobile` 21px | R4-teksten i statusboksen |
| `status-symbol` | 32px / 800 | samme (32px er gulvet) | Statussymbolet i den hvite sirkelen i statusboksen |
| `status-name` | 18px / 700 | samme | Anleggsnavn inne i statusboksen |
| `meta` | 16px | `meta-mobile` 14px | Sted og analyseuke i statusboksen, forklarende setning, analyseukevelger, usikkerhetstekst |
| `table-cell` | 17px | `table-cell-mobile` 16px | Ukestabell. Tall med tabulære sifre (`font-variant-numeric: tabular-nums`), høyrejustert |
| `caption` | 14px | samme | «Sist viste anlegg» over tittelen |
| `chart-label` | 13px | samme (13px er gulvet også på mobil, selv om retning A brukte 11px) | Aksetekst, grafetiketter, tegnforklaring |
| `pill` / `pill-xs` | 13px / 12px, 600 | samme | Statusmerker |
| `logo` | 20px / 800 | samme | «Marin» i toppfeltet |
| `button` | 17px / 600 | `button-mobile` 16px | Knapper («Søk», «Velg fil», «Vis prognose») |
| `field` | 17px / 400 | `field-mobile` 16px | Tekst i søkefelt, analyseukevelger og filvelger |

**Grafetiketter skaleres ikke ned.** Gulvet på 13px gjelder *gjengitt* størrelse: aksetekst, grafetiketter og tegnforklaring er minst 13 CSS-px ved alle skjermbredder (også rett over bruddpunktet og ved 320px) og blir større når brukeren øker tekststørrelsen (tekstzoom). Tekst i en SVG som skaleres med `viewBox`, krymper med grafen og følger ikke tekstzoom; arkitekturen velger hvordan kravet oppfylles. Sjekklista (NFR10) kontrollerer 320px, 600px og 200 % tekstzoom.

Ingen versaler i grensesnittet utenom vanlig setningsstart. Tall skrives med desimalkomma (0,41).

## Layout & Spacing

Én kolonne, sentrert, maks `{spacing.content-max-width}` (760px) på alle skjermbredder. Rekkefølgen er fast: tittel med sted, analyseukevelger, statusboks, graf med tegnforklaring, ukestabell, usikkerhetstekst.

| Token | Desktop | Mobil |
|---|---|---|
| Sidemarg | `{spacing.page-x}` 32px | `{spacing.page-x-mobile}` 16px |
| Topp / bunn i innhold | `{spacing.page-top}` 36px / `{spacing.page-bottom}` 48px | `{spacing.page-top-mobile}` 20px / `{spacing.page-bottom-mobile}` 32px |
| Toppfelt | `{spacing.topbar-y}` 16px vertikalt | `{spacing.topbar-y-mobile}` 12px |
| Mellom seksjoner (over hver seksjonsoverskrift, under statusboksen) | `{spacing.section-gap}` 40px | `{spacing.section-gap-mobile}` 28px |
| Overskrift til innhold | `{spacing.heading-gap}` 12px | samme |
| Statusboks innvendig | `{spacing.statusbox-y}` 24px / `{spacing.statusbox-x}` 28px | `{spacing.statusbox-mobile}` 18px |
| Tabellcelle | `{spacing.table-cell-y}` 14px / `{spacing.table-cell-x}` 8px | `{spacing.table-cell-y-mobile}` 11px / `{spacing.table-cell-x-mobile}` 6px |
| Usikkerhetstekst | `{spacing.uncertainty-top}` 40px over, strek, `{spacing.uncertainty-rule-gap}` 20px | samme |
| Felt og nedtrekksliste innvendig | `{spacing.control-y}` 10px / `{spacing.control-x}` 12px | samme |
| Knapp innvendig | `{spacing.button-y}` 10px / `{spacing.button-x}` 20px | samme |
| Trykkflater og kontroller | Felt, nedtrekksliste og knapper minst `{spacing.target-min}` 44px høye; tekstlenker minst `{spacing.target-min-inline}` 24 × 24px | Alle interaktive mål minst `{spacing.target-min}` 44 × 44px |

Bruddpunkt mellom desktop- og mobilverdier: 600px viewport-bredde. Retning A er skissert bare på 1080px og 375px.

**Reflow.** Siden fungerer ved 320 CSS-px bredde og 400 % zoom uten vannrett rulling, og med økt tekstavstand (WCAG 1.4.12) uten at innhold går tapt. Toppfeltet bryter til to linjer ved behov. Statusmerker bruker minstebredde, ikke fast bredde, og teksten i dem kan bryte linje.

## Elevation & Depth

Ingen skygger og ingen tonelag. Hierarkiet kommer fra rekkefølge, typestørrelse og den ene fargeflaten (statusboksen). Flater og rader skilles med 1px `{colors.border}`.

## Shapes

`{rounded.DEFAULT}` (6px) på statusboks, knapper, skjemafelt og feilmelding. `{rounded.full}` bare på statusmerker (piller), statusmarkøren og den hvite symbolsirkelen i statusboksen. `{rounded.sm}` (4px) på etikettboksen for grensekryssing i grafen. Ingen kort med store radier.

## Components

- **Toppfelt** (`top-bar`) – hvit med `{colors.border}` underkant. «Marin» i `{typography.logo}` og `{colors.accent}` til venstre. Desktop: søkeskjema (maks `{spacing.search-max-width}`) og lenken «Bytt anlegg» til høyre. Søkeskjemaet har etiketten «Søk anlegg» (visuelt skjult, men koblet til feltet og lik starten på plassholderen), søkefeltet og en synlig knapp «Søk» (`{components.button-secondary}`) rett etter feltet. Mobil: bare lenken «Søk / bytt» til høyre. Lenken «Last opp egne tall» står i toppfeltet på begge bredder. På forsiden skjules søkeskjemaet og «Bytt anlegg» / «Søk / bytt», fordi siden har sitt eget søk. Der står bare logoen og «Last opp egne tall», og lenken gjentas ikke på selve siden. Lenkene i toppfeltet har trykkflate på minst `{spacing.target-min}` på mobil. Ved smal skjerm eller stor zoom bryter toppfeltet til to linjer i stedet for å gi vannrett rulling.
- **Statusboks** (`status-box-red|yellow|green|grey`) – den eneste fulle fargeflaten. Innhold ovenfra: anleggsnavn i `{typography.status-name}` med lokalitetsnr., kommune og fylke på egen linje i `{typography.meta}`; «Prognose regnet fra uke 42, 2026» i `{typography.meta}`; symbolsirkel og R4-tekst i `{typography.status-headline}` på samme linje; én forklarende setning i `{typography.meta}` vekt 400. Rød og grønn: hvit tekst på full flate. Gul: mørk tekst på gul med 2px `{colors.status-yellow-border}`. Grå: hvit flate, `{colors.status-grey-on-fill}` tekst, 2px stiplet `{colors.status-grey-border}`.
  - **Symbolsirkel** (`status-symbol-badge`): hvit sirkel, `{spacing.status-symbol-badge-size}` (mobil `{spacing.status-symbol-badge-size-mobile}`), med symbolet i `{typography.status-symbol}` (minst 32px) i statusens `*-symbol`-farge: rød ✕, gul ! (mørk, sirkelen har 2px `{colors.status-yellow-border}`), grønn ✓, grå – eller ? (sirkelen har 2px stiplet `{colors.status-grey-border}`, fordi den står på hvit flate). Symbolet bærer statusen når fargen ikke gjør det (se Colors).
  - **Opplastede data** (`uploaded-data-line`): når boksen viser tall fra en opplastet fil, står linja «Dine opplastede tall: lusetall_langholmen.csv» inne i boksen, rett under anleggsnavnet og stedet, i `{typography.meta}` med «Dine opplastede tall:» i vekt 700 og samme tekstfarge som resten av boksen. Linja står i selve boksen, så den følger med i et skjermbilde.
- **Lastetilstand** (`status-loading`) – står i statusboksens plass mens prognosen regnes ut: hvit flate, 1px heltrukken `{colors.border}`, teksten «Regner ut prognose …» i `{typography.meta}` `{colors.ink-secondary}`. Ingen statusfarge, ingen stipling og ingen symbolsirkel, slik at den ikke kan forveksles med grå status, heller ikke i et skjermbilde.
- **Statusmerke** (`status-pill`) – liten pille: hvit bakgrunn, `{colors.border}` kant, `{colors.ink}` tekst, innvendig `{spacing.pill-y}` / `{spacing.pill-x}`. Foran symbolet står en rund statusmarkør på `{spacing.status-marker}` i statusens `*-fill` (gul med 1px `{colors.status-yellow-border}`, grå hvit med 1px stiplet `{colors.status-grey-border}`); symbolet står i statusens `*-symbol`-farge. Gul får kant `{colors.status-yellow-border}`, grå får stiplet kant `{colors.status-grey-border}`. Størrelse `pill` (13px) eller `pill-xs` (12px, i tabellen). Brukes i ukestabellen («– Ikke telt») og i fargeforklaringen. Merket er ikke interaktivt; blir det interaktivt senere, må kanten ha minst 3:1.
- **Analyseukevelger** (`analysis-week-select`) – etikett «Analyseuke» i `{colors.ink-secondary}`, nedtrekksliste med verdier som «uke 42, 2026». Hvit, `{rounded.DEFAULT}`, tekst i `{typography.field}`, innvendig `{spacing.control-y}` / `{spacing.control-x}`, minst `{spacing.target-min}` høy på alle bredder.
- **Søkefelt** (`search-field`) – hvitt felt med `{rounded.DEFAULT}`, tekst i `{typography.field}`, innvendig `{spacing.control-y}` / `{spacing.control-x}`, minst `{spacing.target-min}` høyt. Plassholder «Søk anlegg – navn eller lokalitetsnr.» på desktop og «Søk navn eller nr.» på mobil. Feltet har alltid en etikett («Søk anlegg»): synlig på forsiden, visuelt skjult i toppfeltet. Plassholderen er aldri eneste etikett. Feltet står alltid sammen med knappen «Søk».
- **Trefliste** (`hit-list-row`) – én rad per anlegg: lokalitetsnavn i `{typography.body}` vekt 600, under det «Lokalitetsnr. 12345 · Hitra, Trøndelag» i `{typography.meta}` `{colors.ink-secondary}`. Rader skilles med `{colors.border}`. Hver rad er minst `{spacing.target-min}` høy. Ingen statusfarge i treflisten. Skisse: `mockups/key-forside.html`.
- **Graf** (`trend-graph`) – SVG-linjediagram med lusetall på y-aksen (0,0; 0,2; 0,4 …) og ISO-uke på x-aksen, fra første uke i vinduet til analyseuke + 6.
  - Rutenett: horisontale linjer i `{colors.border}`.
  - Målte lusetall: punkter i `{colors.accent}` med hvit kant, tynn linje mellom påfølgende tellinger.
  - Uke uten telling: hult punkt med stiplet `{colors.border-strong}` på x-aksen og etiketten «ikke telt».
  - Trend: heltrukken `{colors.accent}` med redusert styrke gjennom vinduet, stiplet `{colors.accent}` fram i tid.
  - Grense: heltrukken 2px `{colors.ink}` som trapp når vårgrensen slår inn, med etiketten «Grense 0,5».
  - Analyseuka: vertikal prikket linje i `{colors.border-strong}` med «Prognose →», ukenummeret i fet `{colors.ink}`.
  - Kryssing (rød og gul): vertikal linje og punkt i statusens kantfarge der trend møter grense, og en hvit etikett (`{rounded.sm}`) med statussymbolet i statusfarge, statusordet og uka i `{colors.ink}`: «✕ Varsel uke 44» eller «! Følg med uke 46». For gul brukes `{colors.status-yellow-border}` på linje og punkt, siden gul mot hvitt er 1,8:1. Statusordet trengs fordi rød og gul kant er nesten like ved deuteranopi.
  - Tegnforklaring under grafen i `{typography.chart-label}`: «Målt lusetall», «Trend (stiplet = prognose)», «Grense per uke». Uten prognose faller trendoppføringen bort.
  - All tekst i grafen (akser, etiketter, tegnforklaring) er minst 13 CSS-px slik den vises, ved alle bredder, og følger tekstzoom (se Typography).
  - Tekstoppsummering: under tegnforklaringen står en synlig oppsummering i `{typography.meta}` `{colors.ink}` (figurtekst til grafen). Den gir målte verdier, prognoseverdier per uke, grensen per uke med vårtrappen og kryssingsuka. Malene står i EXPERIENCE.md (Voice and Tone).
- **Ukestabell** (`week-table`) – kolonnene «Uke», «Voksne hunnlus» (høyrejustert, tabulære sifre) og «Merknad». Overskrifter i `{colors.ink-secondary}` vekt 600. Radlinjer i `{colors.border}`. Uke uten telling: «–» i `{colors.ink-secondary}` og statusmerket «– Ikke telt» (`pill-xs`, grå). Siste telling får merknaden «Siste telling» i `{colors.ink-secondary}`.
- **Usikkerhetstekst** (`uncertainty-text`) – `{typography.meta}` i `{colors.ink-secondary}`, med 1px `{colors.border}` strek over.
- **Fargeforklaring** (`status-legend`) – på forsiden ved første besøk. Fire statusmerker (rød, gul, grønn, grå), hvert med én kort forklarende linje i `{colors.ink-secondary}`. Følger regelen *status nøytral*: ingen fulle flater; statusmarkøren i merket viser fargen. Skisse: `mockups/key-forside.html`.
- **Knapp** (`button-primary`, `button-secondary`) – primær: `{colors.accent}` fylt, `{colors.on-accent}` tekst i `{typography.button}`, `{rounded.DEFAULT}`. Sekundær: hvit med `{colors.accent}` kant og tekst. Innvendig `{spacing.button-y}` / `{spacing.button-x}`, minst `{spacing.target-min}` høy på alle bredder. Brukes på opplastingssiden og som søkeknapp. **Deaktivert** (bare mens fila leses, se EXPERIENCE.md): hvit flate, 1px `{colors.border-strong}` kant og tekst i `{colors.ink-secondary}`, for begge knappetyper. Deaktivert knapp skal se tydelig annerledes ut enn aktiv primærknapp, og teksten holder fortsatt 8,1:1.
- **Opplastingsskjema** (`upload-form`) – skisse: `mockups/key-opplasting.html`. Filvelger, områdevalg som radioknapper, anleggsvalg med standard radioknapper ved Excel med flere anlegg, og primærknapp. Felt med `{colors.border-strong}` kant og `{rounded.DEFAULT}`, tekst i `{typography.field}`; hjelpetekst i `{colors.ink-secondary}`. Hver radioknapp har klikkbar etikett over hele raden, og raden er minst `{spacing.target-min}` høy. Felt eller gruppe med feil får 2px `{colors.ink}` kant (`field-border-invalid`) og feilteksten rett under etiketten i `{colors.ink}`, uten statusrødt. Utledet område vises som vanlig tekst, med fylket først: «Område: Trøndelag – grense som for sør». Når fila har feil, vises bare feilmeldingen og filvelgeren; områdevalg og «Vis prognose» skjules.
- **Feilmelding** (`error-message`) – hvit boks med 2px `{colors.ink}` kant og fet overskrift. Bruker ikke statusrød, fordi rød betyr «brudd» i Marin. Skisse: `mockups/key-opplasting.html`.
- **Lenke** (`link`) – `{colors.accent}`, understreket.
- **Fokusmarkering** (`focus-ring`) – 2px `{colors.accent}` omriss med 2px avstand på alle interaktive elementer.

## Do's and Don'ts

| Do | Don't |
|---|---|
| Full statusfarge bare i den store statusboksen | Fylte statuspiller, fargede tabellrader eller fargede grafflater |
| Alltid farge + symbol + tekst for status | Farge alene, eller symbol uten tekst |
| Mørk kant `{colors.status-yellow-border}` på alt gult | Gul flate eller gul tekst rett på hvitt |
| Én kolonne, maks 760px, fast rekkefølge | To kolonner eller kontrollpanel-oppsett |
| `{colors.accent}` til lenker, knapper og målte data | Aksent som statusfarge, eller flere kulører |
| Skill flater med `{colors.border}` | Skygger, gråtonede bakgrunner, gradienter |
| Systemfonter og SVG-graf | Nedlastede fonter eller tunge bilder |
| Desimalkomma og «uke 42, 2026» | Desimalpunktum eller «2026-W42» |
| Lys modus | Mørk modus i v1 |
