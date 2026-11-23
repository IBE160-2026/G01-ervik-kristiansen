"""Avrunding av lusetall (AD-6).

Alle lusetall og estimater avrundes til 2 desimaler med halvdeler opp (briefen R2).
Pythons innebygde avrunding brukes aldri på lusetall, fordi den runder halvdeler til
nærmeste partall og regner med binære flyttall.
"""

from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

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


def avrund_brok(verdi: Fraction) -> Decimal:
    """Avrunder en eksakt brøk til 2 desimaler med halvdeler opp, som `avrund`.

    Halvdeler rundes bort fra null, som ROUND_HALF_UP: 1/200 blir 0,01 og −1/200 blir
    −0,01. Brøken gjøres aldri om til Decimal før avrundingen, så et estimat som eksakt er
    x,xx5, kan ikke havne på x,xx4999… og rundes ned. Null har aldri minustegn.
    """
    if not isinstance(verdi, Fraction):
        raise TypeError(f"avrund_brok tar Fraction, ikke {type(verdi).__name__}")
    hundredeler = abs(verdi) * 100
    heltall, rest = divmod(hundredeler.numerator, hundredeler.denominator)
    if 2 * rest >= hundredeler.denominator:
        heltall += 1
    if verdi < 0:
        heltall = -heltall
    # Decimal fra tekst er eksakt og avhenger ikke av presisjonen i konteksten. Heltallet 0
    # har ikke fortegn, så resultatet blir aldri −0,00.
    return Decimal(f"{heltall}E-2")
