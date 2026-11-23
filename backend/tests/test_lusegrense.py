"""Tester for lusegrensen etter R1 i marin.kjerne.lusegrense (FR10, T1–T4)."""

from decimal import Decimal

import pytest

from marin.kjerne.formatering import format_grense
from marin.kjerne.lusegrense import GRENSE_ELLERS, GRENSE_VAR, er_brudd, grense
from marin.kjerne.modeller import Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.uker import alle_uker

SOR, NORD, UKJENT = Omrade.SOR, Omrade.NORD, Omrade.UKJENT
D = Decimal


# Fasit fra briefen (R6)


def test_t1_sor_uke_21_gir_grense_0_2():
    assert grense(SOR, Uke(2026, 21)) == D("0.2")


def test_t2_sor_uke_22_gir_grense_0_5():
    assert grense(SOR, Uke(2026, 22)) == D("0.5")


def test_t3_nord_uke_21_gir_grense_0_2():
    assert grense(NORD, Uke(2026, 21)) == D("0.2")


def test_t4_nord_uke_20_gir_grense_0_5():
    assert grense(NORD, Uke(2026, 20)) == D("0.5")


# Kanter og hele året


@pytest.mark.parametrize(
    ("omrade", "uke", "svar"),
    [
        (SOR, 15, "0.5"),
        (SOR, 16, "0.2"),
        (SOR, 21, "0.2"),
        (SOR, 22, "0.5"),
        (NORD, 20, "0.5"),
        (NORD, 21, "0.2"),
        (NORD, 26, "0.2"),
        (NORD, 27, "0.5"),
    ],
)
def test_kantukene_for_vargrensen(omrade, uke, svar):
    assert grense(omrade, Uke(2026, uke)) == D(svar)


@pytest.mark.parametrize(
    ("omrade", "vaaruker"),
    [(SOR, [16, 17, 18, 19, 20, 21]), (NORD, [21, 22, 23, 24, 25, 26])],
)
def test_vargrensen_gjelder_bare_i_vaarukene(omrade, vaaruker):
    aret = alle_uker(Uke(2026, 1), Uke(2026, 53))
    assert [u.uke for u in aret if grense(omrade, u) == GRENSE_VAR] == vaaruker
    assert all(grense(omrade, u) == GRENSE_ELLERS for u in aret if u.uke not in vaaruker)


def test_aret_betyr_ikke_noe():
    assert grense(SOR, Uke(2025, 21)) == grense(SOR, Uke(2026, 21)) == D("0.2")
    assert grense(NORD, Uke(2026, 53)) == D("0.5")


@pytest.mark.parametrize("uke", [Uke(2026, 1), Uke(2026, 18), Uke(2026, 24), Uke(2026, 53)])
def test_ukjent_omrade_gir_ingen_grense(uke):
    assert grense(UKJENT, uke) is None


def test_grensene_skrives_med_en_desimal():
    assert format_grense(grense(SOR, Uke(2026, 16))) == "0,2"
    assert format_grense(grense(NORD, Uke(2026, 30))) == "0,5"


# Område som tekst og feil typer


@pytest.mark.parametrize(("kode", "svar"), [("sor", "0.2"), ("nord", "0.2")])
def test_omrade_kan_gis_som_kode(kode, svar):
    assert grense(kode, Uke(2026, 21)) == D(svar)


def test_ukjent_som_kode_gir_ingen_grense():
    assert grense("ukjent", Uke(2026, 21)) is None


@pytest.mark.parametrize("kode", ["sør", "xyz", "", "SOR"])
def test_ugyldig_omradekode_gir_valueerror(kode):
    with pytest.raises(ValueError):
        grense(kode, Uke(2026, 21))


@pytest.mark.parametrize("omrade", [SOR, NORD, UKJENT])
@pytest.mark.parametrize("uke", [21, (2026, 21), None])
def test_uke_ma_vaere_uke(omrade, uke):
    # Også ved ukjent område, der grense ellers gir None.
    with pytest.raises(TypeError):
        grense(omrade, uke)


# Brudd


@pytest.mark.parametrize(
    ("verdi", "grenseverdi", "svar"),
    [
        ("0.50", "0.5", True),
        ("0.49", "0.5", False),
        ("0.20", "0.2", True),
        ("0.19", "0.2", False),
        ("1.20", "0.5", True),
        ("0.00", "0.2", False),
    ],
)
def test_verdi_pa_eller_over_grensen_er_brudd(verdi, grenseverdi, svar):
    assert er_brudd(D(verdi), D(grenseverdi)) is svar


@pytest.mark.parametrize(
    ("verdi", "grenseverdi"),
    [
        (D("0.5"), None),
        (None, D("0.5")),
        (0.5, D("0.5")),
        (D("0.5"), 0.5),
    ],
)
def test_brudd_med_feil_type_gir_typeerror(verdi, grenseverdi):
    with pytest.raises(TypeError):
        er_brudd(verdi, grenseverdi)


@pytest.mark.parametrize("verdi", ["0.495", "0.4999", "0.199"])
def test_verdi_som_ikke_er_avrundet_gir_valueerror(verdi):
    # Avrundet ville 0,495 vært 0,50 og brudd. Den skal aldri bli «ikke brudd» i stillhet.
    with pytest.raises(ValueError):
        er_brudd(D(verdi), D("0.5"))


def test_ekstra_nuller_er_avrundet_nok():
    assert er_brudd(D("0.500"), D("0.5")) is True
