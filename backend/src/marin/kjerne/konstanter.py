"""Faste verdier i kjernen.

Første og siste uke i det innebygde datagrunnlaget, regelparameterne fra R2 (vindu, minste
antall tellinger og horisont) og grensen for rød status i R4 ligger her, slik at
backtesten kan skrive dem ut som de er.
"""

from typing import Final

from marin.kjerne.modeller import Uke

FORSTE_UKE: Final = Uke(2025, 1)
"""Første analyseuke for de innebygde dataene (FR27).

Backtesten regner status for hver uke fra og med FORSTE_UKE til og med SISTE_UKE.
"""

SISTE_UKE: Final = Uke(2026, 42)
"""Siste uke i det innebygde datagrunnlaget, og «nå» for innebygde data (AD-5).

Kjernen leser aldri klokka. Gjelder ikke opplastede data.
"""

VINDU: Final = 5
"""Antall uker i vinduet for trendlinja: uke t − 4 til og med t (R2).

Parameterne i R2 og R4 er fryst før backtesten (FR27a). De kan ikke overstyres av den som
kaller kjernen, og de justeres ikke for å nå tersklene i M1.
"""

MINSTE_TELLINGER: Final = 3
"""Minste antall tellinger i vinduet for å lage en trendlinje (R2). Fryst etter FR27a."""

HORISONT: Final = 6
"""Antall uker etter analyseuka som prognosen ser fremover (R2). Fryst etter FR27a."""

MAKS_UKER_ROD: Final = 3
"""Flest uker til grensen som gir rød status (R4). Fryst etter FR27a.

Grensen nås om 1–3 uker gir rød «✕ Varsel», 4–6 uker gir gul «! Følg med». Brudd nå
(0 uker) er også rødt, men avgjøres før prognosen.
"""
