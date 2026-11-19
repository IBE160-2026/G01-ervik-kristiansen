"""Tester for kjernens typer i marin.kjerne.modeller (AD-11)."""

from dataclasses import fields
from decimal import Decimal

import pytest

from marin.kjerne.modeller import AnleggInfo, Serie, Telling, Uke

U = Uke(2026, 30)


# Uke


def test_uker_sorteres_kronologisk_over_arsskiftet():
    assert Uke(2025, 52) < Uke(2026, 1) < Uke(2026, 2)
    assert sorted([Uke(2026, 1), Uke(2025, 52), Uke(2025, 3)]) == [
        Uke(2025, 3),
        Uke(2025, 52),
        Uke(2026, 1),
    ]


@pytest.mark.parametrize(("ar", "uke"), [(2025, 0), (2025, 54), (2025, 53), (2026, -1)])
def test_ugyldig_uke_gir_valueerror(ar, uke):
    with pytest.raises(ValueError):
        Uke(ar, uke)


def test_uke_53_finnes_i_2026():
    assert Uke(2026, 53).uke == 53


@pytest.mark.parametrize(("ar", "uke"), [(2025.0, 1), (2025, "1"), (True, 1), (2025, None)])
def test_uke_krever_heltall(ar, uke):
    with pytest.raises(TypeError):
        Uke(ar, uke)


def test_uke_kan_ikke_endres():
    with pytest.raises(AttributeError):
        U.uke = 31  # type: ignore[misc]


# Telling


@pytest.mark.parametrize(
    ("inn", "ut"),
    [
        ("0.125", "0.13"),  # halvdel opp, eksempelet i Story 1.1
        ("0.135", "0.14"),
        ("0.145", "0.15"),  # avrunding til partall ville gitt 0,14
        ("0.124", "0.12"),
        ("0.5", "0.50"),
        ("1", "1.00"),
    ],
)
def test_telling_avrundes_til_2_desimaler_med_halvdeler_opp(inn, ut):
    verdi = Telling(U, Decimal(inn)).verdi
    assert verdi == Decimal(ut)
    assert str(verdi) == ut


def test_telling_uten_verdi_er_uke_uten_telling():
    assert Telling(U, None).verdi is None


@pytest.mark.parametrize("verdi", [0.1, 1, "0.1", True])
def test_telling_godtar_bare_decimal_eller_none(verdi):
    with pytest.raises(TypeError):
        Telling(U, verdi)


@pytest.mark.parametrize("verdi", ["-0.01", "-1"])
def test_negativt_lusetall_gir_valueerror(verdi):
    with pytest.raises(ValueError):
        Telling(U, Decimal(verdi))


@pytest.mark.parametrize("verdi", ["NaN", "Infinity", "-Infinity"])
def test_lusetall_som_ikke_er_endelig_gir_valueerror(verdi):
    with pytest.raises(ValueError):
        Telling(U, Decimal(verdi))


def test_negativ_null_blir_null():
    assert str(Telling(U, Decimal("-0")).verdi) == "0.00"


def test_telling_krever_uke():
    with pytest.raises(TypeError):
        Telling((2026, 30), Decimal("0.1"))  # type: ignore[arg-type]


# Serie


def test_serie_sorteres_stigende_uten_nye_uker():
    tellinger = [
        Telling(Uke(2026, 2), Decimal("0.46")),
        Telling(Uke(2025, 50), Decimal("0.30")),
        Telling(Uke(2026, 1), None),
        Telling(Uke(2025, 52), Decimal("0.38")),
    ]
    serie = Serie(tellinger)
    assert [t.uke for t in serie.tellinger] == [
        Uke(2025, 50),
        Uke(2025, 52),
        Uke(2026, 1),
        Uke(2026, 2),
    ]
    assert set(serie.tellinger) == set(tellinger)


def test_serie_er_en_tuple_og_kan_ikke_endres():
    serie = Serie([Telling(U, Decimal("0.1"))])
    assert isinstance(serie.tellinger, tuple)
    with pytest.raises(AttributeError):
        serie.tellinger = ()  # type: ignore[misc]


@pytest.mark.parametrize(
    "andre",
    [Telling(Uke(2026, 30), Decimal("0.2")), Telling(Uke(2026, 30), None)],
)
def test_to_tellinger_for_samme_uke_gir_valueerror(andre):
    with pytest.raises(ValueError):
        Serie([Telling(Uke(2026, 30), Decimal("0.1")), Telling(Uke(2026, 31), None), andre])


def test_tom_serie_er_lov():
    assert Serie([]).tellinger == ()


def test_serie_godtar_bare_tellinger():
    with pytest.raises(TypeError):
        Serie([(Uke(2026, 30), Decimal("0.1"))])  # type: ignore[list-item]


def test_like_serier_er_like():
    a = Serie([Telling(Uke(2026, 2), Decimal("0.1")), Telling(Uke(2026, 1), None)])
    b = Serie([Telling(Uke(2026, 1), None), Telling(Uke(2026, 2), Decimal("0.10"))])
    assert a == b


# AnleggInfo og område


def test_alle_feltene_i_anlegginfo_kan_mangle():
    info = AnleggInfo()
    assert (info.lokalitetsnr, info.navn, info.kommune, info.fylke) == (None, None, None, None)


def test_omrade_er_ikke_et_felt_i_serie_eller_anlegginfo():
    for klasse in (Serie, AnleggInfo, Telling, Uke):
        assert "omrade" not in {felt.name for felt in fields(klasse)}
