"""Status etter R4 (FR8, FR13, FR14, AD-1, AD-2, AD-7).

`vurder(serie, omrade, analyseuke)` er den eneste inngangen til status. Appen og
backtesten bruker den samme funksjonen og kutter aldri serien selv: tellinger etter
analyseuka brukes ikke (FR8). Reglene prøves i fast rekkefølge, og den første som slår
til, gjelder (R4):

1. Ukjent område: grensen kan ikke bestemmes.
2. Ingen ny telling: siste telling t er mer enn én uke eldre enn analyseuka a.
3. Brudd nå: verdien i t er på eller over grensen i analyseuka.
4. For lite data: færre enn MINSTE_TELLINGER tellinger i vinduet t − 4 til t. Finnes det
   ingen telling til og med a, er vinduet tomt, og statusen blir også «For lite data».
5. Prognose: rød når grensen nås om 1 til MAKS_UKER_ROD uker, gul når den nås senere i
   horisonten, og grønn når den ikke nås innen HORISONT uker.

`tekst` er R4-teksten uten symbol, slik at `f"{symbol} {tekst}"` er tegn for tegn lik
briefen. Forklaringssetningene (FR15a, FR20) kommer i Story 2.6.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Final

from marin.kjerne.formatering import format_uke_i_tekst
from marin.kjerne.konstanter import HORISONT, MAKS_UKER_ROD, MINSTE_TELLINGER
from marin.kjerne.lusegrense import er_brudd, grense
from marin.kjerne.modeller import Serie, Telling, Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.trend import Trend, siste_telling, trendlinje, uker_til_grensen, vindu
from marin.kjerne.uker import mellom, pluss


class Farge(StrEnum):
    """Statusfargen (AD-7). Frontend velger farge og stil bare fra denne koden."""

    ROD = "rod"
    GUL = "gul"
    GRONN = "gronn"
    GRA = "gra"


class Arsak(StrEnum):
    """Regelen i R4 som avgjorde statusen (AD-7)."""

    VARSEL = "varsel"
    BRUDD_NA = "brudd_na"
    FOLG_MED = "folg_med"
    INGEN_KRYSSING = "ingen_kryssing"
    FOR_LITE_DATA = "for_lite_data"
    INGEN_NY_TELLING = "ingen_ny_telling"
    UKJENT_OMRADE = "ukjent_omrade"


_FARGE_OG_SYMBOL: Final[Mapping[Arsak, tuple[Farge, str]]] = MappingProxyType(
    {
        Arsak.BRUDD_NA: (Farge.ROD, "✕"),
        Arsak.VARSEL: (Farge.ROD, "✕"),
        Arsak.FOLG_MED: (Farge.GUL, "!"),
        Arsak.INGEN_KRYSSING: (Farge.GRONN, "✓"),
        Arsak.FOR_LITE_DATA: (Farge.GRA, "–"),
        Arsak.INGEN_NY_TELLING: (Farge.GRA, "–"),
        Arsak.UKJENT_OMRADE: (Farge.GRA, "?"),
    }
)
"""Fargen og symbolet for hver årsak. Symbolene er ✕ U+2715, ! U+0021, ✓ U+2713,
– U+2013 (tankestrek) og ? U+003F. Symbolet kommer bare fra backend (AD-2)."""


@dataclass(frozen=True, slots=True)
class EstimertUke:
    """Uka der estimatet først når grensen, og antall uker dit fra analyseuka (R2).

    Samme form som `estimert_uke` i `Detaljsvar` (AD-3).
    """

    uke: Uke
    uker_til: int

    def __post_init__(self) -> None:
        if not isinstance(self.uke, Uke):
            raise TypeError(f"uke må være Uke, ikke {type(self.uke).__name__}")
        if not isinstance(self.uker_til, int) or isinstance(self.uker_til, bool):
            raise TypeError(f"uker_til må være et heltall, ikke {type(self.uker_til).__name__}")


@dataclass(frozen=True, slots=True)
class Vurdering:
    """Statusen for en serie, et område og en analyseuke. Lages med `vurder`.

    - `farge` og `arsak` er kodene fra AD-7. Backtesten trenger bare dem.
    - `symbol` og `tekst` er R4-teksten delt i to, så `f"{symbol} {tekst}"` er briefens tekst.
    - `uke_tekst` («(uke Y)») og `estimert_uke` finnes bare ved varsel og følg med (FR18).
    - `trend` finnes bare ved varsel, følg med og ingen kryssing.
    - `siste_telling` er siste telling til og med analyseuka for alle statuser, eller None.

    `siste_telling` og `trend` er med, slik at tabellen, grafen og forklaringen (Story 2.5
    og 2.6) bruker den samme linja og ikke regner den ut på nytt.
    """

    farge: Farge
    arsak: Arsak
    symbol: str
    tekst: str
    uke_tekst: str | None
    estimert_uke: EstimertUke | None
    siste_telling: Telling | None
    trend: Trend | None


def vurder(serie: Serie, omrade: Omrade | str, analyseuke: Uke) -> Vurdering:
    """Status etter R4 for serien i området med analyseuka (FR13, FR14).

    Tar hele serien og ser selv bort fra tellinger etter analyseuka (FR8). `omrade` kan
    være en Omrade eller koden som tekst («sor», «nord», «ukjent»). Alle tre argumentene
    sjekkes før reglene: feil type gir TypeError, også et område som ikke er tekst, og en
    ukjent områdekode gir ValueError. Parameterne i R2 og R4 kan ikke overstyres (FR27a).
    """
    if not isinstance(serie, Serie):
        raise TypeError(f"serie må være Serie, ikke {type(serie).__name__}")
    if not isinstance(omrade, str):
        raise TypeError(f"omrade må være Omrade eller tekst, ikke {type(omrade).__name__}")
    if not isinstance(analyseuke, Uke):
        raise TypeError(f"analyseuke må være Uke, ikke {type(analyseuke).__name__}")
    omrade = Omrade(omrade)

    siste = siste_telling(serie, analyseuke)

    # 1) Ukjent område
    if omrade is Omrade.UKJENT:
        return _vurdering(Arsak.UKJENT_OMRADE, "Ukjent område: grensen kan ikke bestemmes", siste)

    # 2) Ingen ny telling: t er eldre enn uka før analyseuka
    if siste is not None and mellom(siste.uke, analyseuke) > 1:
        tekst = f"Ingen ny telling siden {format_uke_i_tekst(siste.uke, analyseuke)}"
        return _vurdering(Arsak.INGEN_NY_TELLING, tekst, siste)

    # 3) Brudd nå: verdien i t mot grensen i analyseuka, ikke i uke t
    if siste is not None and er_brudd(siste.verdi, grense(omrade, analyseuke)):
        return _vurdering(Arsak.BRUDD_NA, "Brudd nå", siste)

    # 4) For lite data, også når det ikke finnes noen telling til og med analyseuka
    tellinger = vindu(serie, analyseuke)
    if len(tellinger) < MINSTE_TELLINGER:
        return _vurdering(Arsak.FOR_LITE_DATA, "For lite data", siste)

    # 5) Prognose
    trend = trendlinje(tellinger)
    uker_til = uker_til_grensen(trend, omrade, analyseuke)
    if uker_til is None:
        tekst = f"Ingen kryssing ventet innen {_uker(HORISONT)}"
        return _vurdering(Arsak.INGEN_KRYSSING, tekst, siste, trend=trend)
    if uker_til <= MAKS_UKER_ROD:
        arsak, tekst = Arsak.VARSEL, f"Varsel: grensen nås om {_uker(uker_til)}"
    else:
        arsak, tekst = Arsak.FOLG_MED, f"Følg med: grensen kan nås om {_uker(uker_til)}"
    estimert = EstimertUke(pluss(analyseuke, uker_til), uker_til)
    return _vurdering(
        arsak,
        tekst,
        siste,
        trend=trend,
        estimert_uke=estimert,
        uke_tekst=f"({format_uke_i_tekst(estimert.uke, analyseuke)})",
    )


def _vurdering(
    arsak: Arsak,
    tekst: str,
    siste: Telling | None,
    *,
    trend: Trend | None = None,
    estimert_uke: EstimertUke | None = None,
    uke_tekst: str | None = None,
) -> Vurdering:
    farge, symbol = _FARGE_OG_SYMBOL[arsak]
    return Vurdering(
        farge=farge,
        arsak=arsak,
        symbol=symbol,
        tekst=tekst,
        uke_tekst=uke_tekst,
        estimert_uke=estimert_uke,
        siste_telling=siste,
        trend=trend,
    )


def _uker(antall: int) -> str:
    # «1 uke», men «2 uker» (T12).
    return "1 uke" if antall == 1 else f"{antall} uker"
