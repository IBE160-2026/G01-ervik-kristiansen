"""Kjernens typer: uke, telling, serie og anleggsinfo (AD-11).

Område er aldri et felt i disse typene. Det sendes alltid som et eget argument, slik at
området bare finnes ett sted.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from marin.kjerne.tall import avrund


@dataclass(frozen=True, order=True, slots=True)
class Uke:
    """En ISO-uke. Uker sorteres kronologisk på (ar, uke).

    En ugyldig uke kan ikke lages: uke 0, uke 54 og uke 53 i et år uten uke 53 gir
    ValueError. Gyldigheten sjekkes med standardbibliotekets ISO-kalender. All
    ukearitmetikk ligger i marin.kjerne.uker.
    """

    ar: int
    uke: int

    def __post_init__(self) -> None:
        for navn in ("ar", "uke"):
            verdi = getattr(self, navn)
            if not isinstance(verdi, int) or isinstance(verdi, bool):
                raise TypeError(f"{navn} må være et heltall, ikke {type(verdi).__name__}")
        try:
            date.fromisocalendar(self.ar, self.uke, 1)
        except ValueError:
            raise ValueError(f"uke {self.uke}, {self.ar} finnes ikke i ISO-kalenderen") from None


@dataclass(frozen=True, slots=True)
class Telling:
    """Lusetallet (voksne hunnlus per fisk) for én uke.

    `verdi` er None for en uke uten telling. Ellers er den en Decimal som avrundes til
    2 desimaler med halvdeler opp når tellingen lages. Flyttall godtas ikke, fordi
    binære flyttall kan gi feil avrunding (0,145 kan bli 0,14). Kildene konverterer
    derfor via tekst, for eksempel Decimal(str(v)).
    """

    uke: Uke
    verdi: Decimal | None

    def __post_init__(self) -> None:
        if not isinstance(self.uke, Uke):
            raise TypeError(f"uke må være Uke, ikke {type(self.uke).__name__}")
        if self.verdi is None:
            return
        if not isinstance(self.verdi, Decimal):
            raise TypeError(f"lusetall må være Decimal eller None, ikke {type(self.verdi).__name__}")
        if not self.verdi.is_finite():
            raise ValueError(f"lusetall må være et endelig tall, ikke {self.verdi}")
        if self.verdi < 0:
            raise ValueError(f"lusetall kan ikke være negativt: {self.verdi}")
        object.__setattr__(self, "verdi", avrund(self.verdi))


@dataclass(frozen=True, slots=True)
class Serie:
    """Tellingene for ett anlegg, sortert stigende, med høyst én telling per uke.

    Serien inneholder bare ukene som finnes i kilden, med eller uten verdi. Den fyller
    aldri inn uker. To tellinger for samme uke gir ValueError.
    """

    tellinger: tuple[Telling, ...]

    def __init__(self, tellinger: Iterable[Telling]) -> None:
        sortert = tuple(sorted(tellinger, key=_ukenokkel))
        for forrige, denne in zip(sortert, sortert[1:]):
            if forrige.uke == denne.uke:
                raise ValueError(
                    f"uke {denne.uke.uke}, {denne.uke.ar} finnes mer enn én gang i serien"
                )
        object.__setattr__(self, "tellinger", sortert)


def _ukenokkel(telling: Telling) -> Uke:
    if not isinstance(telling, Telling):
        raise TypeError(f"en serie består av Telling, ikke {type(telling).__name__}")
    return telling.uke


@dataclass(frozen=True, slots=True)
class AnleggInfo:
    """Navn og sted for et anlegg. Alle feltene kan mangle, for eksempel ved CSV-opplasting."""

    lokalitetsnr: int | None = None
    navn: str | None = None
    kommune: str | None = None
    fylke: str | None = None
