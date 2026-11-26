"""Skriver backend/openapi.json fra appen (AD-3).

Kjøres med `uv run python -m marin.api.openapi` i backend/. Fila committes, og
frontend-typene genereres fra den. En test feiler når fila ikke er lik `app.openapi()`,
så kommandoen må kjøres hver gang en modell eller rute endres. Fila er UTF-8 med LF og
innrykk på 2, og samme app gir alltid samme tekst.
"""

import json
import sys
from importlib.resources import files
from pathlib import Path
from typing import TextIO

from marin.api.app import app


def openapifil() -> Path:
    """backend/openapi.json, regnet fra pakken (backend/src/marin er to nivåer ned)."""
    return Path(str(files("marin"))).parents[1] / "openapi.json"


def skjema_som_tekst() -> str:
    """Teksten i openapi.json: skjemaet appen lager, med innrykk på 2 og linjeskift til slutt."""
    return json.dumps(app.openapi(), ensure_ascii=False, indent=2) + "\n"


def kjor(utfil: Path, ut: TextIO | None = None) -> int:
    """Skriver skjemaet til `utfil`. Gir 0."""
    ut = ut or sys.stdout
    utfil.write_text(skjema_som_tekst(), encoding="utf-8", newline="\n")
    print(f"Skrev {utfil}.", file=ut)
    return 0


if __name__ == "__main__":
    sys.exit(kjor(openapifil()))
