"""Hjelp til testene: Excel-filer i BarentsWatch-formatet, laget i minnet.

Testdataene står dermed i testene og ikke i binærfiler. Kolonnenavnene her er testens
egen kopi av formatet, så en endring i leseren ikke kan endre fasiten.
"""

import io
from collections.abc import Iterable, Mapping

import openpyxl

KOLONNER = ("Uke", "År", "Lokalitetsnummer", "Lokalitetsnavn", "Voksne hunnlus", "Kommune", "Fylke")


def rad(nr=1, ar=2026, uke=1, lus=None, navn=None, kommune=None, fylke=None, **andre) -> dict:
    """Én rad. Kolonner kan overstyres med navn, for eksempel rad(**{"Uke": "x"})."""
    return {
        "Lokalitetsnummer": nr,
        "År": ar,
        "Uke": uke,
        "Voksne hunnlus": lus,
        "Lokalitetsnavn": navn,
        "Kommune": kommune,
        "Fylke": fylke,
    } | andre


def lag_xlsx(
    rader: Iterable[Mapping[str, object] | None],
    kolonner: Iterable[str] = KOLONNER,
    ark: str = "Lakselus per fisk",
) -> bytes:
    """Lager xlsx-bytes. Overskriften er rad 1, og `None` i stedet for en rad gir en tom rad."""
    kolonner = list(kolonner)
    bok = openpyxl.Workbook()
    side = bok.active
    side.title = ark
    side.append(kolonner)
    for radnr, celler in enumerate(rader, start=2):
        if celler is None:
            continue
        for kolonnenr, kolonne in enumerate(kolonner, start=1):
            side.cell(row=radnr, column=kolonnenr, value=celler.get(kolonne))
    buffer = io.BytesIO()
    bok.save(buffer)
    return buffer.getvalue()
