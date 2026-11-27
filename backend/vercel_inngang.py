"""Inngangen for Vercel (AD-9). `vercel.json` peker hit med `vercel_inngang:app`.

Vercel slår opp `modul:app` som en fil regnet fra roten til tjenesten (`backend/`), så
`marin.api.app:app` blir `marin/api/app.py`, som ikke finnes. Koden ligger i `src/`.
Derfor legges `src/` først i importstien, slik at `marin` kan importeres enten Vercel
installerer pakken eller ikke. Lokalt brukes `marin.api.app:app` som før.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from marin.api.app import app

__all__ = ["app"]
