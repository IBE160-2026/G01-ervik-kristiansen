"""Leser for BarentsWatch-uttrekket «Lakselus per fisk» (FR1–FR3, AD-11, AD-12).

Dette er den eneste modulen som kjenner arknavnet, kolonnenavnene og typene i
BarentsWatch-formatet. `forbered` bruker den til det innebygde datasettet, og
opplastingen (Story 3.2) bruker den til brukerens egne filer, slik at samme fil gir samme
serie begge veier.

Leseren sjekker bare det som trengs for å lage kjernens typer. Reglene som bare gjelder
opplasting (årsgrensen, filstørrelsen og teksten for ukjent format), kommer i Story 3.2.
"""

import io
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Final

import openpyxl

from marin.kilder.feil import Feil
from marin.kjerne.formatering import format_uke
from marin.kjerne.modeller import AnleggInfo, Serie, Telling, Uke

ARK: Final = "Lakselus per fisk"

LOKALITETSNR: Final = "Lokalitetsnummer"
AR: Final = "År"
UKE: Final = "Uke"
VOKSNE_HUNNLUS: Final = "Voksne hunnlus"
NAVN: Final = "Lokalitetsnavn"
KOMMUNE: Final = "Kommune"
FYLKE: Final = "Fylke"

PAKREVDE: Final = (LOKALITETSNR, AR, UKE, VOKSNE_HUNNLUS)
"""Kolonnene som må finnes. Navn, kommune og fylke kan mangle (FR23a)."""

FEIL_FORMAT: Final = f"Fila er ikke et Excel-uttrekk fra BarentsWatch med arket «{ARK}»."

# Feltene i AnleggInfo og kolonnene de hentes fra.
_INFO: Final = (("navn", NAVN), ("kommune", KOMMUNE), ("fylke", FYLKE))

type Anlegg = tuple[AnleggInfo, Serie]


def les(innhold: bytes, til_og_med: Uke | None = None) -> tuple[list[Anlegg], list[Feil]]:
    """Leser et Excel-uttrekk og gir anleggene sortert på lokalitetsnummer, og feilene.

    Rader etter `til_og_med` hoppes over før anleggene lages (FR1). En rad med feil kommer
    ikke med, og ved duplikat beholdes den første raden. Navn, kommune og fylke hentes
    felt for felt fra den nyeste raden der feltet har verdi (AD-11, avgjort 2026-11-23).
    """
    if not isinstance(innhold, bytes):
        raise TypeError(f"innhold må være bytes, ikke {type(innhold).__name__}")
    if til_og_med is not None and not isinstance(til_og_med, Uke):
        raise TypeError(f"til_og_med må være Uke eller None, ikke {type(til_og_med).__name__}")
    try:
        bok = openpyxl.load_workbook(io.BytesIO(innhold), read_only=True, data_only=True)
    except Exception:
        # openpyxl gir mange ulike unntak for filer som ikke er xlsx (zip, XML, nøkler).
        # Alle betyr det samme for brukeren: fila er ikke et uttrekk Marin kan lese.
        return [], [Feil(None, FEIL_FORMAT)]
    try:
        if ARK not in bok.sheetnames:
            return [], [Feil(None, FEIL_FORMAT)]
        ark = bok[ARK]
        # I read_only-modus stoler openpyxl på <dimension> i fila. Er den feil, kan
        # rader og kolonner forsvinne uten feil, så den regnes ut på nytt mens vi leser.
        ark.reset_dimensions()
        return _les_rader(_rader(ark), til_og_med)
    except _Formatfeil:
        return [], [Feil(None, FEIL_FORMAT)]
    finally:
        bok.close()


class _Formatfeil(Exception):
    """openpyxl klarte ikke å lese radene i arket, for eksempel fordi XML-en er ødelagt."""


def _rader(ark):
    # read_only-modus leser XML-en først når radene hentes. Feil derfra gjelder fila,
    # ikke leseren, og blir formatfeil. Feil i leserens egen kode slipper gjennom.
    try:
        yield from ark.iter_rows(values_only=True)
    except Exception as feil:
        raise _Formatfeil from feil


@dataclass(slots=True)
class _Samling:
    """Det leseren har funnet om ett anlegg så langt."""

    tellinger: list[Telling] = field(default_factory=list)
    # Felt i AnleggInfo → (uka verdien ble funnet i, verdien).
    info: dict[str, tuple[Uke, str]] = field(default_factory=dict)


class _Radfeil(Exception):
    """En feil i én celle. Teksten er meldingen uten «Rad N: »."""


def _les_rader(rader, til_og_med: Uke | None) -> tuple[list[Anlegg], list[Feil]]:
    overskrift = next(rader, None) or ()
    kolonner: dict[str, int] = {}
    for indeks, navn in enumerate(overskrift):
        if isinstance(navn, str):
            kolonner.setdefault(navn.strip(), indeks)
    manglende = [navn for navn in PAKREVDE if navn not in kolonner]
    if manglende:
        return [], [Feil(None, f"Fila mangler kolonnen «{navn}».") for navn in manglende]

    samlinger: dict[int, _Samling] = {}
    forste_rad: dict[tuple[int, Uke], int] = {}
    feil: list[Feil] = []

    # Overskriften er rad 1. read_only-modus gir også tomme rader, så nummeret stemmer.
    for radnr, rad in enumerate(rader, start=2):
        if all(_er_tom(verdi) for verdi in rad):
            continue

        def celle(kolonne: str) -> object:
            indeks = kolonner.get(kolonne)
            return rad[indeks] if indeks is not None and indeks < len(rad) else None

        radfeil: list[str] = []
        nr = _fang(radfeil, _heltall, celle(LOKALITETSNR), LOKALITETSNR)
        ar = _fang(radfeil, _heltall, celle(AR), AR)
        ukenr = _fang(radfeil, _heltall, celle(UKE), UKE)
        uke = _fang(radfeil, _uke, ar, ukenr) if ar is not None and ukenr is not None else None
        if uke is not None and til_og_med is not None and uke > til_og_med:
            continue
        verdi = _fang(radfeil, _lusetall, celle(VOKSNE_HUNNLUS))

        if nr is not None and uke is not None:
            forste = forste_rad.setdefault((nr, uke), radnr)
            if forste != radnr:
                radfeil.append(f"{format_uke(uke)} finnes allerede i rad {forste}.")
        if radfeil:
            feil += [Feil.i_rad(radnr, tekst) for tekst in radfeil]
            continue

        samling = samlinger.setdefault(nr, _Samling())
        samling.tellinger.append(Telling(uke, verdi))
        for felt, kolonne in _INFO:
            tekst = _tekst(celle(kolonne))
            if tekst is not None and (felt not in samling.info or uke > samling.info[felt][0]):
                samling.info[felt] = (uke, tekst)

    anlegg = [
        (
            AnleggInfo(nr, **{felt: verdi for felt, (_, verdi) in samling.info.items()}),
            Serie(samling.tellinger),
        )
        for nr, samling in sorted(samlinger.items())
    ]
    return anlegg, feil


def _fang(radfeil: list[str], funksjon, *argumenter):
    """Kaller funksjonen. Gir den _Radfeil, legges teksten i radfeil og svaret blir None."""
    try:
        return funksjon(*argumenter)
    except _Radfeil as feil:
        radfeil.append(str(feil))
        return None


def _er_tom(verdi: object) -> bool:
    return verdi is None or (isinstance(verdi, str) and not verdi.strip())


def _vis(verdi: object) -> str:
    # Tall vises med desimalkomma, slik brukeren ser dem i norsk Excel.
    if isinstance(verdi, (int, float)) and not isinstance(verdi, bool):
        return str(verdi).replace(".", ",")
    return str(verdi).strip()


def _heltall(verdi: object, kolonne: str) -> int:
    if _er_tom(verdi):
        raise _Radfeil(f"«{kolonne}» mangler.")
    if isinstance(verdi, int) and not isinstance(verdi, bool):
        return verdi
    # Excel lagrer alle tall som flyttall, så 2025.0 er et heltall.
    if isinstance(verdi, float) and verdi.is_integer():
        return int(verdi)
    raise _Radfeil(f"«{kolonne}» må være et heltall, ikke «{_vis(verdi)}».")


def _uke(ar: int, ukenr: int) -> Uke:
    if not 1 <= ukenr <= 53:
        raise _Radfeil(f"uke {ukenr} finnes ikke. Uke må være 1–53.")
    try:
        return Uke(ar, ukenr)
    except ValueError:
        # For år som finnes i kalenderen, kan bare uke 53 være ugyldig.
        if 1 <= ar <= 9999:
            raise _Radfeil(f"{ar} har ikke uke 53.") from None
        raise _Radfeil(f"året {ar} finnes ikke i kalenderen.") from None


def _lusetall(verdi: object) -> Decimal | None:
    if _er_tom(verdi):
        return None
    if isinstance(verdi, bool) or not isinstance(verdi, (int, float)):
        raise _Radfeil(f"lusetallet «{_vis(verdi)}» er ikke et tall.")
    try:
        # Via tekst, så 0,145 blir 0,145 og ikke flyttallet like under (Telling avrunder).
        tall = Decimal(str(verdi))
    except InvalidOperation:
        raise _Radfeil(f"lusetallet «{_vis(verdi)}» er ikke et tall.") from None
    if not tall.is_finite():
        raise _Radfeil(f"lusetallet «{_vis(verdi)}» er ikke et tall.")
    if tall < 0:
        raise _Radfeil(f"lusetallet «{_vis(verdi)}» er negativt.")
    if tall.adjusted() >= 20:
        # Så store tall kan ikke avrundes til 2 desimaler med Decimal sin standardpresisjon.
        raise _Radfeil(f"lusetallet «{_vis(verdi)}» er for stort.")
    return tall


def _tekst(verdi: object) -> str | None:
    if _er_tom(verdi):
        return None
    return verdi.strip() if isinstance(verdi, str) else str(verdi)
