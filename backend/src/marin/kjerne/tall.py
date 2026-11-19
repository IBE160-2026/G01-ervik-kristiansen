"""Avrunding av lusetall (AD-6).

Alle lusetall og estimater avrundes til 2 desimaler med halvdeler opp (briefen R2).
Pythons innebygde avrunding brukes aldri på lusetall, fordi den runder halvdeler til
nærmeste partall og regner med binære flyttall.
"""

from decimal import ROUND_HALF_UP, Decimal

_TO_DESIMALER = Decimal("0.01")


def avrund(verdi: Decimal) -> Decimal:
    """Avrunder til 2 desimaler med halvdeler opp, for eksempel 0,125 til 0,13.

    Null har aldri minustegn: −0,004 blir 0,00, ikke −0,00. Ellers ville et lite negativt
    estimat sluppet forbi en sjekk på `< 0` og blitt vist som «−0,00».
    """
    if not isinstance(verdi, Decimal):
        raise TypeError(f"avrund tar Decimal, ikke {type(verdi).__name__}")
    resultat = verdi.quantize(_TO_DESIMALER, rounding=ROUND_HALF_UP)
    return resultat.copy_abs() if resultat.is_zero() else resultat
