"""Kjører backtesten etter SK2 på det innebygde datasettet (FR27–FR29, AD-10).

Kjøres med `uv run python -m marin.backtest` i backend/. Skriptet er et tynt skall: det
leser datasett.json, lar kjernen (`marin.kjerne.treffsikkerhet.backtest`) regne alt, og
skriver backend/src/marin/data/backtest.json og et sammendrag i terminalen. Området for
hvert anlegg kommer fra fylket. Den første kjøringen på de ekte dataene er Story 1.7.
"""

import sys
from importlib.resources import files
from pathlib import Path
from typing import TextIO

from marin.kilder.datasett import Datasett
from marin.kjerne.omrade import omrade_fra_fylke
from marin.kjerne.treffsikkerhet import backtest


def resultatfil() -> Path:
    """backend/src/marin/data/backtest.json, regnet fra pakken."""
    return Path(str(files("marin").joinpath("data", "backtest.json")))


def kjor(datasett: Path, utfil: Path, ut: TextIO | None = None) -> int:
    """Leser datasettet i `datasett`, kjører backtesten og skriver resultatet til `utfil`. Gir 0."""
    ut = ut or sys.stdout
    data = Datasett.fra_json(datasett.read_text(encoding="utf-8"))
    resultat = backtest((serie, omrade_fra_fylke(info.fylke)) for info, serie in data.anlegg)
    utfil.parent.mkdir(parents=True, exist_ok=True)
    utfil.write_text(resultat.til_json(), encoding="utf-8", newline="\n")
    print(resultat.sammendrag(utfil.name), file=ut)
    return 0
