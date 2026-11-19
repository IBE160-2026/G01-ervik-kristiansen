"""Tekstformat for lusetall, grenser og uker (AD-6, NFR5).

Lusetall skrives alltid med 2 desimaler og desimalkomma («0,50»). Grenser skrives med
1 desimal («0,5»), som i briefen og R4-tekstene. Uker skrives «uke 42, 2026».
Frontend får tilsvarende funksjoner i Story 2.2, testet mot de samme vektorene i
backend/tests/data/format.json.
"""

from decimal import ROUND_HALF_UP, Decimal

from marin.kjerne.modeller import Uke
from marin.kjerne.tall import avrund

_EN_DESIMAL = Decimal("0.1")


def format_lus(verdi: Decimal) -> str:
    """Lusetall med 2 desimaler og desimalkomma, for eksempel «0,06» og «0,50»."""
    return _med_komma(avrund(verdi))


def format_grense(grense: Decimal) -> str:
    """Lusegrense med 1 desimal og desimalkomma, for eksempel «0,5» og «0,2»."""
    if not isinstance(grense, Decimal):
        raise TypeError(f"format_grense tar Decimal, ikke {type(grense).__name__}")
    return _med_komma(grense.quantize(_EN_DESIMAL, rounding=ROUND_HALF_UP))


def format_uke(uke: Uke) -> str:
    """ISO-uke med år, for eksempel «uke 42, 2026»."""
    return f"uke {uke.uke}, {uke.ar}"


def _med_komma(verdi: Decimal) -> str:
    return f"{verdi:f}".replace(".", ",")
