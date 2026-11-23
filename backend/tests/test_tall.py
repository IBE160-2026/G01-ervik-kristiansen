"""Tester for avrundingen i marin.kjerne.tall (AD-6)."""

from decimal import Decimal
from fractions import Fraction

import pytest

from marin.kjerne.formatering import format_lus
from marin.kjerne.tall import avrund, avrund_brok


@pytest.mark.parametrize("verdi", ["-0", "-0.00", "-0.004", "-0.0049"])
def test_null_far_aldri_minustegn(verdi):
    resultat = avrund(Decimal(verdi))
    assert str(resultat) == "0.00"
    assert format_lus(Decimal(verdi)) == "0,00"


def test_lite_negativt_estimat_kan_settes_til_null_med_max():
    # Story 1.4 setter negative estimater til 0. Uten normalisering ville max gitt −0,00.
    assert str(max(avrund(Decimal("-0.004")), Decimal("0.00"))) == "0.00"


def test_negative_tall_som_ikke_blir_null_beholder_fortegnet():
    assert avrund(Decimal("-0.005")) == Decimal("-0.01")


def test_avrund_tar_ikke_flyttall():
    with pytest.raises(TypeError):
        avrund(0.125)  # type: ignore[arg-type]


# avrund_brok (Story 1.4): eksakt avrunding av brøker fra regresjonen


def test_avrund_brok_gir_det_samme_som_avrund():
    # Alle tusendeler fra −1 til 1. Også samme skrivemåte: to desimaler og aldri −0,00.
    avvik = []
    for tusendeler in range(-1000, 1001):
        fra_brok = avrund_brok(Fraction(tusendeler, 1000))
        fra_decimal = avrund(Decimal(tusendeler).scaleb(-3))
        if fra_brok != fra_decimal or str(fra_brok) != str(fra_decimal):
            avvik.append((tusendeler, str(fra_brok), str(fra_decimal)))
    assert avvik == []


@pytest.mark.parametrize(
    ("brok", "svar"),
    [
        (Fraction(1, 3), "0.33"),
        (Fraction(2, 3), "0.67"),
        (Fraction(1, 200), "0.01"),
        (Fraction(-1, 200), "-0.01"),
        (Fraction(99, 200), "0.50"),  # 0,495 eksakt
        (Fraction(1, 2), "0.50"),
        (Fraction(0), "0.00"),
        (Fraction(-1, 300), "0.00"),
        (Fraction(7), "7.00"),
    ],
)
def test_avrund_brok_kjente_verdier(brok, svar):
    assert str(avrund_brok(brok)) == svar


def test_avrund_brok_runder_like_under_halv_ned():
    # En billiondel under 0,005 skal ned, selv om det er svært nær halvdelen.
    assert str(avrund_brok(Fraction(5, 1000) - Fraction(1, 10**12))) == "0.00"


@pytest.mark.parametrize("verdi", [0.125, Decimal("0.125"), 1])
def test_avrund_brok_tar_bare_brok(verdi):
    with pytest.raises(TypeError):
        avrund_brok(verdi)  # type: ignore[arg-type]
