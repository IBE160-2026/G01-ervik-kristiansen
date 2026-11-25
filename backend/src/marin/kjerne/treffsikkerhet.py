"""Backtest etter SK2: kryssinger, treff, varsler og presisjon (FR27–FR29, AD-1, AD-10).

Backtesten måler hvor godt statusen varsler brudd. Status for uke a er
`vurder(hele serien, område, a)` for hver a fra FORSTE_UKE til og med SISTE_UKE. `vurder`
ser selv bort fra tellinger etter a, så ingen her kutter serien (AD-1).

- Kryssing: en uke w med telling der verdien er på eller over grensen i uke w, og der
  forrige telling, i w − 1 eller ellers w − 2, er under grensen i sin uke.
- Treff: en kryssing der den sammenhengende perioden med rød status som slutter i w − 1,
  begynte i w − 4, w − 3 eller w − 2. Rød er både «✕ Varsel» og «✕ Brudd nå».
- Varsel fulgt av brudd: en uke a med årsak varsel, der minst én telling i a + 1 til
  a + 4 er på eller over grensen i sin uke.
- Treffandel er treff / kryssinger, og presisjon er varsler fulgt av brudd / varsler.

En uke uten verdi er ikke en telling. Ukjent område gir ingen kryssinger og ingen varsler.
Kryssinger før FORSTE_KRYSSING og varsler etter SISTE_VARSEL holdes utenfor og telles for
seg. Parameterne i R2 og R4 kan ikke overstyres (FR27a).
"""

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, fields
from decimal import Decimal
from types import MappingProxyType
from typing import Final

from marin.kjerne.formatering import format_uke
from marin.kjerne.konstanter import (
    FORSTE_UKE,
    HORISONT,
    MAKS_UKER_ROD,
    MINSTE_TELLINGER,
    SISTE_UKE,
    VINDU,
)
from marin.kjerne.lusegrense import er_brudd, grense
from marin.kjerne.modeller import Serie, Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.status import Arsak, Farge, vurder
from marin.kjerne.uker import alle_uker, pluss

FORSTE_KRYSSING: Final = Uke(2025, 9)
"""Første kryssing som telles. Tidligere kryssinger har for kort historikk før seg til at en
rød periode kan ha begynt 2–4 uker før, og telles i `utelatt_kryssinger`."""

SISTE_VARSEL: Final = Uke(2026, 38)
"""Siste varsel som telles. For senere varsler finnes ikke alle de 4 neste ukene i dataene,
og de telles i `utelatt_varsler`."""

VERSJON: Final = 1
"""Versjonen av formatet i backtest.json."""

PARAMETERE: Final[Mapping[str, int]] = MappingProxyType(
    {
        "vindu": VINDU,
        "minste_tellinger": MINSTE_TELLINGER,
        "horisont": HORISONT,
        "maks_uker_rod": MAKS_UKER_ROD,
    }
)
"""Regelparameterne som backtesten er kjørt med, i rekkefølgen i backtest.json."""

_UKER_ETTER_VARSEL: Final = 4
"""Et varsel er fulgt av brudd når bruddet kommer i en av de 4 neste ukene (SK2)."""

_TREFF_LENGDER: Final = range(2, 5)
"""Antall røde uker rett før kryssingen ved treff: perioden begynte i w − 2, w − 3 eller w − 4."""

_ANTALL: Final = (
    "antall_kryssinger",
    "antall_treff",
    "antall_varsler",
    "antall_varsler_med_brudd",
    "utelatt_kryssinger",
    "utelatt_varsler",
)


def kryssinger(serie: Serie, omrade: Omrade | str) -> tuple[Uke, ...]:
    """Ukene der serien krysser grensen, stigende (SK2).

    Uke w er en kryssing når verdien i w er på eller over grensen i uke w, og forrige
    telling, i w − 1 eller ellers w − 2, er under grensen i sin uke. Har verken w − 1 eller
    w − 2 en telling, er w ikke en kryssing. Ukjent område gir ingen kryssinger. Hele
    serien brukes, og ingen kryssinger holdes utenfor her.
    """
    omrade = _sjekk_serie_og_omrade(serie, omrade)
    if omrade is Omrade.UKJENT:
        return ()
    verdier = _verdier(serie)
    funnet = []
    for uke, verdi in verdier.items():
        if not er_brudd(verdi, grense(omrade, uke)):
            continue
        forrige = next((u for u in (pluss(uke, -1), pluss(uke, -2)) if u in verdier), None)
        if forrige is not None and not er_brudd(verdier[forrige], grense(omrade, forrige)):
            funnet.append(uke)
    return tuple(funnet)


def er_treff(kryssing: Uke, rode_uker: Iterable[Uke]) -> bool:
    """Sann når den røde perioden før kryssingen begynte 2–4 uker før (SK2).

    `rode_uker` er ukene med rød status (`Farge.ROD`). Perioden er de sammenhengende røde
    ukene som slutter i w − 1. Den må ha begynt i w − 4, w − 3 eller w − 2, altså være 2,
    3 eller 4 uker lang. En uke med en annen farge, eller uten status, bryter perioden.
    """
    if not isinstance(kryssing, Uke):
        raise TypeError(f"kryssing må være Uke, ikke {type(kryssing).__name__}")
    rode = set(rode_uker)
    # Teller røde uker bakover fra w − 1, men stopper én uke forbi den lengste perioden
    # som gir treff. Da er lengden 5 for alle perioder som begynte i w − 5 eller før.
    lengde = 0
    while lengde <= _TREFF_LENGDER[-1] and pluss(kryssing, -(lengde + 1)) in rode:
        lengde += 1
    return lengde in _TREFF_LENGDER


def fulgt_av_brudd(serie: Serie, omrade: Omrade | str, varsel: Uke) -> bool:
    """Sann når minst én telling i uke a + 1 til a + 4 er på eller over grensen i sin uke.

    a er `varsel`. Funksjonen sjekker ikke at uka har status varsel, det gjør `backtest`.
    Ukjent område gir aldri varsel og har ingen grense, så svaret er da alltid False.
    """
    omrade = _sjekk_serie_og_omrade(serie, omrade)
    if not isinstance(varsel, Uke):
        raise TypeError(f"varsel må være Uke, ikke {type(varsel).__name__}")
    if omrade is Omrade.UKJENT:
        return False
    verdier = _verdier(serie)
    for k in range(1, _UKER_ETTER_VARSEL + 1):
        uke = pluss(varsel, k)
        if uke in verdier and er_brudd(verdier[uke], grense(omrade, uke)):
            return True
    return False


@dataclass(frozen=True, slots=True, kw_only=True)
class Backtestresultat:
    """Resultatet av backtesten, slik det står i backtest.json (AD-10).

    Bare de seks antallene gis inn. `versjon`, `parametere` og `siste_uke` kommer fra
    kjernens konstanter og kan ikke overstyres (FR27a). `treffandel` og `presisjon` regnes
    eksakt fra antallene og avrundes til 4 desimaler med halvdeler opp. Er nevneren 0, gir
    det ValueError. Rekkefølgen på feltene er rekkefølgen i fila.
    """

    versjon: int = field(default=VERSJON, init=False)
    parametere: Mapping[str, int] = field(default=PARAMETERE, init=False, hash=False)
    siste_uke: Uke = field(default=SISTE_UKE, init=False)
    antall_kryssinger: int
    antall_treff: int
    antall_varsler: int
    antall_varsler_med_brudd: int
    utelatt_kryssinger: int
    utelatt_varsler: int
    treffandel: Decimal = field(init=False)
    presisjon: Decimal = field(init=False)

    def __post_init__(self) -> None:
        for navn in _ANTALL:
            verdi = getattr(self, navn)
            if not isinstance(verdi, int) or isinstance(verdi, bool):
                raise TypeError(f"{navn} må være et heltall, ikke {type(verdi).__name__}")
            if verdi < 0:
                raise ValueError(f"{navn} kan ikke være negativt: {verdi}")
        if self.antall_treff > self.antall_kryssinger:
            raise ValueError("det kan ikke være flere treff enn kryssinger")
        if self.antall_varsler_med_brudd > self.antall_varsler:
            raise ValueError("det kan ikke være flere varsler fulgt av brudd enn varsler")
        if self.antall_kryssinger == 0:
            raise ValueError("treffandelen kan ikke regnes ut når det ikke er noen kryssinger")
        if self.antall_varsler == 0:
            raise ValueError("presisjonen kan ikke regnes ut når det ikke er noen varsler")
        treffandel = _avrund(self.antall_treff, self.antall_kryssinger, 4)
        presisjon = _avrund(self.antall_varsler_med_brudd, self.antall_varsler, 4)
        object.__setattr__(self, "treffandel", treffandel)
        object.__setattr__(self, "presisjon", presisjon)

    def til_json(self) -> str:
        """Teksten i backtest.json, ett felt per linje. Samme resultat gir alltid samme tekst.

        Alle tall er JSON-tall, og andelene skrives direkte fra Decimal uten flyttall, så
        `json.loads(tekst, parse_float=Decimal)` gir de samme verdiene tilbake.
        """
        linjer = [f"  {json.dumps(f.name)}: {_json_verdi(getattr(self, f.name))}" for f in fields(self)]
        return "{\n" + ",\n".join(linjer) + "\n}\n"

    def sammendrag(self, filnavn: str) -> str:
        """De fire linjene som skallet skriver til terminalen etter at `filnavn` er skrevet.

        Prosentene har én desimal med halvdeler opp og desimalkomma, og regnes fra
        antallene, ikke fra de avrundede andelene. Ukene og parameterne kommer fra
        konstantene.
        """
        treffandel = _prosent(self.antall_treff, self.antall_kryssinger)
        presisjon = _prosent(self.antall_varsler_med_brudd, self.antall_varsler)
        return "\n".join(
            [
                f"Skrev {filnavn} for {format_uke(FORSTE_UKE)} til {format_uke(self.siste_uke)}.",
                f"Kryssinger: {self.antall_kryssinger} ({self.utelatt_kryssinger} før "
                f"{format_uke(FORSTE_KRYSSING)} er holdt utenfor). Treff: {self.antall_treff}. "
                f"Treffandel: {treffandel} %.",
                f"Varsler: {self.antall_varsler} ({self.utelatt_varsler} etter "
                f"{format_uke(SISTE_VARSEL)} er holdt utenfor). Fulgt av brudd: "
                f"{self.antall_varsler_med_brudd}. Presisjon: {presisjon} %.",
                f"Parametere: vindu {VINDU} uker, minst {MINSTE_TELLINGER} tellinger, "
                f"horisont {HORISONT} uker, rød ved 0–{MAKS_UKER_ROD} uker.",
            ]
        )


def backtest(anlegg: Iterable[tuple[Serie, Omrade | str]]) -> Backtestresultat:
    """Backtesten etter SK2 for anleggene, gitt som (serie, område) (FR27, FR28).

    For hvert anlegg regnes status med `vurder(serien, området, a)` for hver uke a fra
    FORSTE_UKE til og med SISTE_UKE, én gang. Ukene med rød status avgjør om kryssingene er
    treff, og ukene med årsak varsel er varslene. Serien kuttes aldri (AD-1). Dataene skal
    ende i SISTE_UKE, slik datasett.json gjør, fordi kryssinger etter SISTE_UKE ikke holdes
    utenfor. Gir ValueError når det ikke er noen kryssinger eller ingen varsler som telles.
    """
    analyseuker = alle_uker(FORSTE_UKE, SISTE_UKE)
    antall = dict.fromkeys(_ANTALL, 0)
    for serie, omrade in anlegg:
        status = {a: vurder(serie, omrade, a) for a in analyseuker}
        rode = {a for a, vurdering in status.items() if vurdering.farge is Farge.ROD}
        for kryssing in kryssinger(serie, omrade):
            if kryssing < FORSTE_KRYSSING:
                antall["utelatt_kryssinger"] += 1
                continue
            antall["antall_kryssinger"] += 1
            if er_treff(kryssing, rode):
                antall["antall_treff"] += 1
        for a, vurdering in status.items():
            if vurdering.arsak is not Arsak.VARSEL:
                continue
            if a > SISTE_VARSEL:
                antall["utelatt_varsler"] += 1
                continue
            antall["antall_varsler"] += 1
            if fulgt_av_brudd(serie, omrade, a):
                antall["antall_varsler_med_brudd"] += 1
    return Backtestresultat(**antall)


def _sjekk_serie_og_omrade(serie: Serie, omrade: Omrade | str) -> Omrade:
    if not isinstance(serie, Serie):
        raise TypeError(f"serie må være Serie, ikke {type(serie).__name__}")
    if not isinstance(omrade, str):
        raise TypeError(f"omrade må være Omrade eller tekst, ikke {type(omrade).__name__}")
    return Omrade(omrade)


def _verdier(serie: Serie) -> dict[Uke, Decimal]:
    # Serie har ikke oppslag fra uke til verdi. Uker uten verdi er ikke tellinger.
    return {telling.uke: telling.verdi for telling in serie.tellinger if telling.verdi is not None}


def _avrund(teller: int, nevner: int, desimaler: int) -> Decimal:
    # teller / nevner med halvdeler opp (ROUND_HALF_UP), regnet eksakt med heltall som
    # avrund_brok. Teller og nevner er aldri negative, og nevneren er større enn 0.
    heltall, rest = divmod(teller * 10**desimaler, nevner)
    if 2 * rest >= nevner:
        heltall += 1
    # Decimal fra tekst er eksakt og avhenger ikke av presisjonen i konteksten.
    return Decimal(f"{heltall}E-{desimaler}")


def _prosent(teller: int, nevner: int) -> str:
    # Prosent med én desimal og desimalkomma, for eksempel «28,3».
    return f"{_avrund(100 * teller, nevner, 1):f}".replace(".", ",")


def _json_verdi(verdi: object) -> str:
    if isinstance(verdi, Decimal):
        return f"{verdi:f}"
    if isinstance(verdi, Uke):
        return json.dumps({"ar": verdi.ar, "uke": verdi.uke})
    if isinstance(verdi, Mapping):
        return json.dumps(dict(verdi))
    return json.dumps(verdi)
