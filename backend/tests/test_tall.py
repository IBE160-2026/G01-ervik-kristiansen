"""Tester for avrundingen i marin.kjerne.tall (AD-6)."""

from decimal import Decimal

import pytest

from marin.kjerne.formatering import format_lus
from marin.kjerne.tall import avrund


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
