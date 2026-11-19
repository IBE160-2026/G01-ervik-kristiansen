"""ISO-kalenderen i Marin (AD-14). All ukearitmetikk ligger her.

Løpende ukenummer er antall uker fra en fast startuke (ISO-uka som begynner 1. januar
år 1). Da er årsskiftet, fra uke 52 eller 53 til uke 1, alltid ett steg på +1
(briefen R2, T12).
"""

from datetime import date

from marin.kjerne.modeller import Uke


def har_uke_53(ar: int) -> bool:
    """Sann når ISO-året har 53 uker. 28. desember ligger alltid i årets siste ISO-uke."""
    return date(ar, 12, 28).isocalendar().week == 53


def lopende(uke: Uke) -> int:
    """Løpende ukenummer for uka. Påfølgende uker gir påfølgende heltall."""
    mandag = date.fromisocalendar(uke.ar, uke.uke, 1)
    # Alle mandager har ordinal 1, 8, 15, … (1. januar år 1 var en mandag).
    return (mandag.toordinal() - 1) // 7


def fra_lopende(nummer: int) -> Uke:
    """Uka med dette løpende ukenummeret. Omvendt av lopende."""
    iso = date.fromordinal(nummer * 7 + 1).isocalendar()
    return Uke(iso.year, iso.week)


def pluss(uke: Uke, antall: int) -> Uke:
    """Uka `antall` uker etter `uke`. Negativt antall går bakover."""
    return fra_lopende(lopende(uke) + antall)


def neste(uke: Uke) -> Uke:
    """Uka etter `uke`."""
    return pluss(uke, 1)


def mellom(fra: Uke, til: Uke) -> int:
    """Antall uker fra `fra` til `til`. Negativt når `til` ligger før `fra`."""
    return lopende(til) - lopende(fra)


def alle_uker(fra: Uke, til: Uke) -> list[Uke]:
    """Alle uker fra og med `fra` til og med `til`, stigende."""
    if til < fra:
        raise ValueError(
            f"uke {fra.uke}, {fra.ar} ligger etter uke {til.uke}, {til.ar}"
        )
    return [fra_lopende(nummer) for nummer in range(lopende(fra), lopende(til) + 1)]
