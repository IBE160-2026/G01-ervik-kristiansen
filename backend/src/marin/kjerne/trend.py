"""Trend og uker til grensen etter R2 og R3 (FR8, FR11–FR13).

Fire byggeklosser som Story 1.5 (status), backtesten og detaljsiden bruker:

- `siste_telling` finner t, siste uke med telling til og med analyseuka a.
- `vindu` gir tellingene i uke t − 4 til og med t.
- `trendlinje` regner minste kvadraters metode med løpende ukenummer som x, og gir en
  `Trend` med `stigning` per uke og `estimat` for en uke.
- `uker_til_grensen` finner første uke a + k (k = 1–6) der estimatet når grensen i den uka.

Regresjonen regnes eksakt med brøker (Fraction), aldri med flyttall eller Decimal-divisjon.
Bare estimatet blir Decimal, avrundet til 2 desimaler med halvdeler opp (AD-6). Den som
kaller, trenger aldri å kutte serien: funksjonene ser selv bort fra tellinger etter a
(FR8). Status kommer i Story 1.5.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction

from marin.kjerne.konstanter import HORISONT, MINSTE_TELLINGER, VINDU
from marin.kjerne.lusegrense import er_brudd, grense
from marin.kjerne.modeller import Serie, Telling, Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.tall import avrund_brok
from marin.kjerne.uker import lopende, pluss


def siste_telling(serie: Serie, analyseuke: Uke) -> Telling | None:
    """Siste telling med verdi til og med analyseuka, eller None når det ikke finnes noen.

    Uka til denne tellingen er t i R2. Tellinger etter analyseuka og uker uten verdi brukes
    ikke (FR8). Om t er for gammel, sjekkes ikke her, men i statusen (Story 1.5).
    """
    _sjekk_serie_og_uke(serie, analyseuke)
    for telling in reversed(serie.tellinger):
        if telling.uke <= analyseuke and telling.verdi is not None:
            return telling
    return None


def vindu(serie: Serie, analyseuke: Uke) -> tuple[Telling, ...]:
    """Tellingene med verdi i uke t − 4 til og med t, stigende (R2).

    t er uka til `siste_telling`. Tom når det ikke finnes noen telling til og med
    analyseuka. Uker uten telling fylles aldri inn, så vinduet kan ha færre enn 5 tellinger.
    """
    siste = siste_telling(serie, analyseuke)
    if siste is None:
        return ()
    t = siste.uke
    fra = pluss(t, -(VINDU - 1))
    return tuple(
        telling
        for telling in serie.tellinger
        if fra <= telling.uke <= t and telling.verdi is not None
    )


@dataclass(frozen=True, slots=True)
class Trend:
    """Trendlinja fra minste kvadraters metode, regnet eksakt med brøker.

    Linja går gjennom snittpunktet (x̄, ȳ), der x er løpende ukenummer
    (`marin.kjerne.uker.lopende`) og y er lusetallet. `stigning` er endringen i lusetall
    per uke. Lages med `trendlinje`.
    """

    stigning: Fraction
    x_snitt: Fraction
    y_snitt: Fraction

    def __post_init__(self) -> None:
        for navn in ("stigning", "x_snitt", "y_snitt"):
            verdi = getattr(self, navn)
            if not isinstance(verdi, Fraction):
                raise TypeError(f"{navn} må være Fraction, ikke {type(verdi).__name__}")

    def estimat(self, uke: Uke) -> Decimal:
        """Estimatet på linja i uka, avrundet til 2 desimaler med halvdeler opp (R2).

        Estimatet er ȳ + b · (x − x̄), regnet eksakt. Et estimat under 0 blir 0,00 (FR13).
        """
        if not isinstance(uke, Uke):
            raise TypeError(f"uke må være Uke, ikke {type(uke).__name__}")
        eksakt = self.y_snitt + self.stigning * (lopende(uke) - self.x_snitt)
        return avrund_brok(max(eksakt, Fraction(0)))


def trendlinje(tellinger: Iterable[Telling]) -> Trend:
    """Trendlinja for tellingene med minste kvadraters metode (R2, FR11).

    x er løpende ukenummer, så årsskiftet er ett steg, og uker uten telling teller med
    i avstanden (T8, T12). b = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)². Krever minst
    MINSTE_TELLINGER tellinger, alle med verdi og i ulike uker, ellers ValueError.
    Tellingene skal komme fra `vindu(serie, analyseuke)`. Funksjonen sjekker ikke selv at
    de ligger i ett vindu eller ikke er etter analyseuka.
    """
    tellinger = tuple(tellinger)
    for telling in tellinger:
        if not isinstance(telling, Telling):
            raise TypeError(f"trendlinje tar Telling, ikke {type(telling).__name__}")
        if telling.verdi is None:
            raise ValueError(
                f"uke {telling.uke.uke}, {telling.uke.ar} har ingen verdi og kan ikke være med"
            )
    if len({telling.uke for telling in tellinger}) != len(tellinger):
        raise ValueError("tellingene må være i ulike uker")
    if len(tellinger) < MINSTE_TELLINGER:
        raise ValueError(
            f"trendlinja trenger minst {MINSTE_TELLINGER} tellinger, ikke {len(tellinger)}"
        )

    xs = [Fraction(lopende(telling.uke)) for telling in tellinger]
    ys = [Fraction(telling.verdi) for telling in tellinger]
    x_snitt = sum(xs, Fraction(0)) / len(xs)
    y_snitt = sum(ys, Fraction(0)) / len(ys)
    sxx = sum(((x - x_snitt) ** 2 for x in xs), Fraction(0))
    sxy = sum(((x - x_snitt) * (y - y_snitt) for x, y in zip(xs, ys)), Fraction(0))
    # sxx er større enn 0, fordi det er minst to ulike uker.
    return Trend(stigning=sxy / sxx, x_snitt=x_snitt, y_snitt=y_snitt)


def uker_til_grensen(trend: Trend, omrade: Omrade | str, analyseuke: Uke) -> int | None:
    """Antall uker fra analyseuka til estimatet første gang når grensen (R2, R3, FR12).

    Svaret er første k fra 1 til HORISONT der det avrundede estimatet i uke a + k er på
    eller over grensen i uke a + k. Grensen hentes for hver uke, så vårgrensen slår inn
    midt i horisonten (R3, T6). k telles fra analyseuka, ikke fra t (T10). None betyr
    «ingen kryssing innen 6 uker». Ukjent område gir ValueError, fordi det ikke finnes
    noen grense å regne mot.
    """
    if not isinstance(trend, Trend):
        raise TypeError(f"trend må være Trend, ikke {type(trend).__name__}")
    if not isinstance(omrade, str):
        raise TypeError(f"omrade må være Omrade eller tekst, ikke {type(omrade).__name__}")
    if not isinstance(analyseuke, Uke):
        raise TypeError(f"analyseuke må være Uke, ikke {type(analyseuke).__name__}")
    omrade = Omrade(omrade)
    if omrade is Omrade.UKJENT:
        raise ValueError("uker til grensen kan ikke regnes ut når området er ukjent")
    for k in range(1, HORISONT + 1):
        uke = pluss(analyseuke, k)
        if er_brudd(trend.estimat(uke), grense(omrade, uke)):
            return k
    return None


def _sjekk_serie_og_uke(serie: Serie, analyseuke: Uke) -> None:
    if not isinstance(serie, Serie):
        raise TypeError(f"serie må være Serie, ikke {type(serie).__name__}")
    if not isinstance(analyseuke, Uke):
        raise TypeError(f"analyseuke må være Uke, ikke {type(analyseuke).__name__}")
