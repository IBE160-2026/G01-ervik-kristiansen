"""Lusegrensen etter R1 (FR10).

Grensen er 0,2 voksne hunnlus per fisk i uke 16–21 i sør og uke 21–26 i nord, ellers 0,5
(lakselusforskriften § 8). Grensen avhenger bare av ukenummeret, ikke av året. En verdi
på eller over grensen er brudd. Ved ukjent område finnes ingen grense, og alle som kaller
`grense`, må håndtere None.
"""

from collections.abc import Mapping
from decimal import Decimal
from types import MappingProxyType
from typing import Final

from marin.kjerne.modeller import Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.tall import avrund

GRENSE_VAR: Final = Decimal("0.2")
GRENSE_ELLERS: Final = Decimal("0.5")

VARUKER: Final[Mapping[Omrade, range]] = MappingProxyType(
    {Omrade.SOR: range(16, 22), Omrade.NORD: range(21, 27)}
)
"""ISO-ukene med vårgrense: uke 16–21 i sør og uke 21–26 i nord, begge ender med."""


def grense(omrade: Omrade | str, uke: Uke) -> Decimal | None:
    """Lusegrensen for et område i en ISO-uke, eller None når området er ukjent.

    `omrade` kan være en Omrade eller koden som tekst («sor», «nord», «ukjent»). En annen
    kode gir ValueError.
    """
    omrade = Omrade(omrade)
    if not isinstance(uke, Uke):
        raise TypeError(f"uke må være Uke, ikke {type(uke).__name__}")
    if omrade is Omrade.UKJENT:
        return None
    return GRENSE_VAR if uke.uke in VARUKER[omrade] else GRENSE_ELLERS


def er_brudd(verdi: Decimal, grense: Decimal) -> bool:
    """Sann når verdien er på eller over grensen (R1: grensen er «færre enn»).

    Begge må være Decimal. Funksjonen avrunder ikke: den som kaller, må avrunde estimatet
    til 2 desimaler først (R2, AD-6). En verdi som ikke er avrundet, gir ValueError, så
    0,495 aldri blir «ikke brudd» når den avrundede verdien 0,50 er brudd.
    """
    for navn, tall in (("verdi", verdi), ("grense", grense)):
        if not isinstance(tall, Decimal):
            raise TypeError(f"{navn} må være Decimal, ikke {type(tall).__name__}")
    if verdi != avrund(verdi):
        raise ValueError(f"verdi må være avrundet til 2 desimaler først (R2), ikke {verdi}")
    return verdi >= grense
