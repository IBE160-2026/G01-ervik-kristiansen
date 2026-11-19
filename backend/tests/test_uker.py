"""Tester for ISO-kalenderen i marin.kjerne.uker (AD-14) og SISTE_UKE (AD-5)."""

import pytest

from marin.kjerne.konstanter import SISTE_UKE
from marin.kjerne.modeller import Uke
from marin.kjerne.uker import (
    alle_uker,
    fra_lopende,
    har_uke_53,
    lopende,
    mellom,
    neste,
    pluss,
)


@pytest.mark.parametrize(
    ("ar", "svar"),
    [(2025, False), (2026, True), (2024, False), (2020, True), (2015, True), (2027, False)],
)
def test_har_uke_53(ar, svar):
    assert har_uke_53(ar) is svar


@pytest.mark.parametrize(
    ("uke", "svar"),
    [
        (Uke(2025, 52), Uke(2026, 1)),  # 2025 har ikke uke 53
        (Uke(2026, 52), Uke(2026, 53)),  # 2026 har uke 53
        (Uke(2026, 53), Uke(2027, 1)),
        (Uke(2026, 41), Uke(2026, 42)),
    ],
)
def test_neste(uke, svar):
    assert neste(uke) == svar


@pytest.mark.parametrize(
    ("uke", "antall", "svar"),
    [
        (Uke(2025, 50), 3, Uke(2026, 1)),
        (Uke(2026, 1), -4, Uke(2025, 49)),  # vinduet t − 4 over årsskiftet
        (Uke(2026, 42), 6, Uke(2026, 48)),
        (Uke(2026, 50), 6, Uke(2027, 3)),  # over uke 53
        (Uke(2026, 30), 0, Uke(2026, 30)),
    ],
)
def test_pluss(uke, antall, svar):
    assert pluss(uke, antall) == svar


def test_lopende_ukenummer_er_sammenhengende_over_arsskiftet_t12():
    uker = [Uke(2025, 50), Uke(2025, 51), Uke(2025, 52), Uke(2026, 1), Uke(2026, 2)]
    nummer = [lopende(u) for u in uker]
    assert nummer == list(range(nummer[0], nummer[0] + 5))


def test_lopende_ukenummer_er_sammenhengende_over_uke_53():
    uker = [Uke(2026, 52), Uke(2026, 53), Uke(2027, 1)]
    nummer = [lopende(u) for u in uker]
    assert nummer == list(range(nummer[0], nummer[0] + 3))


def test_fra_lopende_er_omvendt_av_lopende():
    for uke in alle_uker(Uke(2024, 1), Uke(2028, 52)):
        assert fra_lopende(lopende(uke)) == uke


@pytest.mark.parametrize(
    ("fra", "til", "svar"),
    [
        (Uke(2025, 50), Uke(2026, 2), 4),
        (Uke(2026, 2), Uke(2025, 50), -4),
        (Uke(2026, 30), Uke(2026, 30), 0),
        (Uke(2026, 52), Uke(2027, 1), 2),
    ],
)
def test_mellom(fra, til, svar):
    assert mellom(fra, til) == svar


def test_alle_uker_i_det_innebygde_datagrunnlaget():
    uker = alle_uker(Uke(2025, 1), SISTE_UKE)
    assert len(uker) == 94
    assert uker[0] == Uke(2025, 1)
    assert uker[-1] == Uke(2026, 42)
    assert uker == sorted(uker)
    assert Uke(2025, 52) in uker
    assert len(set(uker)) == 94


def test_alle_uker_med_bare_en_uke():
    assert alle_uker(Uke(2026, 30), Uke(2026, 30)) == [Uke(2026, 30)]


def test_alle_uker_baklengs_gir_valueerror():
    with pytest.raises(ValueError):
        alle_uker(Uke(2026, 30), Uke(2026, 29))


def test_siste_uke_er_2026_uke_42():
    assert SISTE_UKE == Uke(2026, 42)
