"""Område for lusegrensen (R1, FR3, AD-11).

Et anlegg er «nord» når det ligger i Nordland, Troms eller Finnmark, ellers «sør».
Området utledes av fylkesnavnet fra en lukket tabell over nåværende og tidligere fylker.
Mangler fylket, eller står det ikke i tabellen, er området ukjent, og da kan grensen ikke
bestemmes.
"""

from collections.abc import Mapping
from enum import StrEnum
from types import MappingProxyType
from typing import Final


class Omrade(StrEnum):
    """Område som avgjør hvilken vårgrense som gjelder.

    «sor» og «nord» er de samme kodene som i API-et. Ukjent område sendes ikke som kode:
    `omrade_utledet` er da null, og statusen får årsaken `ukjent_omrade` (AD-13).
    """

    SOR = "sor"
    NORD = "nord"
    UKJENT = "ukjent"


_NORD = ("Nordland", "Troms", "Finnmark", "Troms og Finnmark")
_SOR = (
    # Nåværende fylker (fra 2024)
    "Østfold",
    "Akershus",
    "Buskerud",
    "Oslo",
    "Innlandet",
    "Vestfold",
    "Telemark",
    "Agder",
    "Rogaland",
    "Vestland",
    "Møre og Romsdal",
    "Trøndelag",
    # Fylker 2020–2023
    "Viken",
    "Vestfold og Telemark",
    # Fylker før 2020
    "Hedmark",
    "Oppland",
    "Aust-Agder",
    "Vest-Agder",
    "Hordaland",
    "Sogn og Fjordane",
    "Sør-Trøndelag",
    "Nord-Trøndelag",
)

FYLKER: Final[Mapping[str, Omrade]] = MappingProxyType(
    {navn: Omrade.NORD for navn in _NORD} | {navn: Omrade.SOR for navn in _SOR}
)
"""Den lukkede tabellen over fylkesnavn, med de norske navneformene slik BarentsWatch
skriver dem. Samiske og kvenske parallellnavn er ikke med (avgjort 2026-11-19)."""


def _nokkel(tekst: str) -> str:
    # Slår sammen alle mellomrom, også hardt mellomrom, og ignorerer store og små bokstaver.
    return " ".join(tekst.split()).casefold()


_OPPSLAG: Final = MappingProxyType({_nokkel(navn): omrade for navn, omrade in FYLKER.items()})


def omrade_fra_fylke(fylke: str | None) -> Omrade:
    """Området for et fylke. Tomt fylke, None eller et ukjent navn gir Omrade.UKJENT."""
    if fylke is None:
        return Omrade.UKJENT
    if not isinstance(fylke, str):
        raise TypeError(f"fylke må være tekst eller None, ikke {type(fylke).__name__}")
    return _OPPSLAG.get(_nokkel(fylke), Omrade.UKJENT)
