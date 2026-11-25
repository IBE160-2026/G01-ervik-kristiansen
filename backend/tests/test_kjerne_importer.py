"""Kontrakttest for kjernen (AD-1, AD-5, AD-6).

Kjernen skal bare importere standardbiblioteket og seg selv, aldri lese klokka og aldri
bruke round() (lusetall avrundes med Decimal). Testen leser kildekoden med ast, så
den fanger også bruk som ikke kjøres i andre tester.
"""

import ast
import sys
from pathlib import Path

import pytest

import marin.kjerne

KJERNE = Path(marin.kjerne.__file__).parent
KLOKKE = {"now", "today", "utcnow"}
RUND = {"round", "__round__"}


def finn_brudd(kilde: str) -> list[str]:
    """Alle brudd på reglene for kjernen i én kildefil."""
    brudd = []
    for node in ast.walk(ast.parse(kilde)):
        if isinstance(node, ast.Import):
            brudd += [f"import {a.name}" for a in node.names if not _lovlig(a.name)]
        elif isinstance(node, ast.ImportFrom):
            if node.level > 1 or (node.level == 0 and not _lovlig(node.module or "")):
                brudd.append(f"from {'.' * node.level}{node.module or ''} import …")
        elif isinstance(node, ast.Name) and node.id == "round":
            # Fanger både round(x), r = round og map(round, xs).
            brudd.append("round brukt")
        elif isinstance(node, ast.Attribute) and node.attr in RUND:
            brudd.append(f".{node.attr} brukt")
        elif isinstance(node, ast.Attribute) and node.attr in KLOKKE:
            brudd.append(f".{node.attr} leser klokka")
    return brudd


def _lovlig(modul: str) -> bool:
    topp = modul.split(".")[0]
    if topp == "marin":
        return modul == "marin.kjerne" or modul.startswith("marin.kjerne.")
    return topp in sys.stdlib_module_names and topp != "time"


def test_kjernen_har_moduler():
    assert {p.name for p in KJERNE.glob("*.py")} >= {
        "modeller.py",
        "uker.py",
        "tall.py",
        "formatering.py",
        "konstanter.py",
        "omrade.py",
        "lusegrense.py",
        "trend.py",
        "status.py",
    }


@pytest.mark.parametrize(
    "fil", sorted(KJERNE.rglob("*.py")), ids=lambda p: p.relative_to(KJERNE).as_posix()
)
def test_kjernen_bruker_bare_stdlib_og_leser_ikke_klokka(fil):
    assert finn_brudd(fil.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize(
    "kilde",
    [
        "import openpyxl",
        "import fastapi.responses",
        "from pydantic import BaseModel",
        "from marin.api import app",
        "from marin import kilder",
        "from .. import api",
        "import time",
        "from time import sleep",
        "from datetime import datetime\nx = datetime.now()",
        "from datetime import date\nx = date.today()",
        "x = round(y, 2)",
        "import builtins\nx = builtins.round(y, 2)",
        "r = round",
        "xs = list(map(round, ys))",
        "x = y.__round__(2)",
    ],
)
def test_sjekken_fanger_brudd(kilde):
    assert finn_brudd(kilde) != []


@pytest.mark.parametrize(
    "kilde",
    [
        "from decimal import Decimal",
        "import datetime",
        "from marin.kjerne.modeller import Uke",
        "from . import uker",
        "x = verdi.quantize(Decimal('0.01'))",
    ],
)
def test_sjekken_godtar_lovlig_kode(kilde):
    assert finn_brudd(kilde) == []
