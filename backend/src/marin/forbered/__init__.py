"""Lager datasett.json fra BarentsWatch-utdraget (FR1, AD-10).

Kjøres med `uv run python -m marin.forbered` i backend/. Skriptet leser alle xlsx-filene i
data/barentswatch/ med samme leser som opplastingen, tar bare med uker til og med
SISTE_UKE og skriver backend/src/marin/data/datasett.json med sha256 for hver kildefil.
Finner leseren feil, skrives ingen fil.
"""

import hashlib
import sys
from collections import defaultdict
from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path
from typing import Final, TextIO

from marin.kilder import barentswatch
from marin.kilder.barentswatch import Anlegg
from marin.kilder.datasett import Datasett
from marin.kjerne.formatering import format_uke
from marin.kjerne.konstanter import SISTE_UKE
from marin.kjerne.modeller import AnleggInfo, Serie

MAKS_FEIL: Final = 20
"""Så mange feil skrives til terminalen. Antallet skrives alltid."""


def kildemappe() -> Path:
    """data/barentswatch/ i repoet, regnet fra pakken (backend/src/marin er tre nivåer ned)."""
    return Path(str(files("marin"))).parents[2] / "data" / "barentswatch"


def datasettfil() -> Path:
    """backend/src/marin/data/datasett.json, regnet fra pakken."""
    return Path(str(files("marin").joinpath("data", "datasett.json")))


def kildefiler(mappe: Path) -> list[Path]:
    """xlsx-filene i mappa, sortert på navn. Låsefilene Excel lager (~$navn.xlsx) er ikke med."""
    return sorted(fil for fil in mappe.glob("*.xlsx") if not fil.name.startswith("~$"))


def kjor(kilder: Path, utfil: Path, ut: TextIO | None = None, feilut: TextIO | None = None) -> int:
    """Leser xlsx-filene i `kilder` og skriver datasettet til `utfil`. Gir 0, eller 1 ved feil."""
    ut = ut or sys.stdout
    feilut = feilut or sys.stderr
    filer = kildefiler(kilder)
    if not filer:
        print(f"Fant ingen xlsx-filer i {kilder}.", file=feilut)
        return 1

    hasher: dict[str, str] = {}
    lesinger: list[list[Anlegg]] = []
    feil: list[str] = []
    for fil in filer:
        innhold = fil.read_bytes()
        hasher[fil.name] = hashlib.sha256(innhold).hexdigest()
        anlegg, filfeil = barentswatch.les(innhold, til_og_med=SISTE_UKE)
        lesinger.append(anlegg)
        feil += [f"{fil.name}: {f.melding}" for f in filfeil]

    anlegg, samlefeil = slaa_sammen(lesinger)
    feil += samlefeil
    if feil:
        for linje in feil[:MAKS_FEIL]:
            print(linje, file=feilut)
        print(f"{len(feil)} feil. {utfil.name} er ikke skrevet.", file=feilut)
        return 1

    datasett = Datasett(SISTE_UKE, hasher, tuple(anlegg))
    utfil.parent.mkdir(parents=True, exist_ok=True)
    utfil.write_text(datasett.til_json(), encoding="utf-8", newline="\n")

    tellinger = [t for _, serie in anlegg for t in serie.tellinger]
    med = sum(t.verdi is not None for t in tellinger)
    print(
        f"Skrev {utfil.name}: {len(anlegg)} anlegg, {med} uker med telling og "
        f"{len(tellinger) - med} uker uten telling, til og med {format_uke(SISTE_UKE)}.",
        file=ut,
    )
    return 0


def slaa_sammen(lesinger: Iterable[list[Anlegg]]) -> tuple[list[Anlegg], list[str]]:
    """Slår sammen anlegg som finnes i flere filer, for eksempel én fil per år.

    Tellingene samles i én serie, og samme uke i to filer er en feil. Navn, kommune og
    fylke tas felt for felt fra den nyeste delen som har verdi, der delene sorteres på
    siste uke. Det gir samme regel som i leseren så lenge filene ikke overlapper i tid.
    """
    deler: dict[int, list[Anlegg]] = defaultdict(list)
    for anlegg in lesinger:
        for info, serie in anlegg:
            deler[info.lokalitetsnr].append((info, serie))

    resultat: list[Anlegg] = []
    feil: list[str] = []
    for nr in sorted(deler):
        biter = sorted(deler[nr], key=lambda bit: bit[1].tellinger[-1].uke)
        try:
            serie = Serie(t for _, s in biter for t in s.tellinger)
        except ValueError as unntak:
            feil.append(f"Lokalitet {nr} har samme uke i flere filer: {unntak}.")
            continue
        felt = {
            navn: next((getattr(i, navn) for i, _ in reversed(biter) if getattr(i, navn) is not None), None)
            for navn in ("navn", "kommune", "fylke")
        }
        resultat.append((AnleggInfo(nr, **felt), serie))
    return resultat, feil
