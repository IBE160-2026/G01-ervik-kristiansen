"""Tester for område fra fylke i marin.kjerne.omrade (FR3, R1, AD-11)."""

import pytest

from marin.kjerne.omrade import FYLKER, Omrade, omrade_fra_fylke

SOR, NORD, UKJENT = Omrade.SOR, Omrade.NORD, Omrade.UKJENT

# Testens egen fasit, skrevet ut for hånd. Tabellen i koden skal ha nøyaktig disse navnene.
FORVENTET = {
    # Nord
    "Nordland": NORD,
    "Troms": NORD,
    "Finnmark": NORD,
    "Troms og Finnmark": NORD,
    # Sør, nåværende fylker
    "Østfold": SOR,
    "Akershus": SOR,
    "Buskerud": SOR,
    "Oslo": SOR,
    "Innlandet": SOR,
    "Vestfold": SOR,
    "Telemark": SOR,
    "Agder": SOR,
    "Rogaland": SOR,
    "Vestland": SOR,
    "Møre og Romsdal": SOR,
    "Trøndelag": SOR,
    # Sør, 2020–2023
    "Viken": SOR,
    "Vestfold og Telemark": SOR,
    # Sør, før 2020
    "Hedmark": SOR,
    "Oppland": SOR,
    "Aust-Agder": SOR,
    "Vest-Agder": SOR,
    "Hordaland": SOR,
    "Sogn og Fjordane": SOR,
    "Sør-Trøndelag": SOR,
    "Nord-Trøndelag": SOR,
}


def test_tabellen_har_noyaktig_de_26_navnene():
    assert len(FORVENTET) == 26
    assert dict(FYLKER) == FORVENTET


def test_bare_de_fire_nordfylkene_gir_nord():
    nord = {navn for navn in FORVENTET if omrade_fra_fylke(navn) is NORD}
    assert nord == {"Nordland", "Troms", "Finnmark", "Troms og Finnmark"}


@pytest.mark.parametrize(("fylke", "omrade"), FORVENTET.items())
def test_hvert_fylke_gir_riktig_omrade(fylke, omrade):
    assert omrade_fra_fylke(fylke) is omrade


@pytest.mark.parametrize(
    "fylke",
    [None, "", "  ", "Svalbard", "Ukjent", "Troms – Romsa – Tromssa", "Nord", "Sør"],
)
def test_tomt_eller_ukjent_fylke_gir_ukjent(fylke):
    assert omrade_fra_fylke(fylke) is UKJENT


@pytest.mark.parametrize(
    ("fylke", "omrade"),
    [
        (" Nordland ", NORD),
        ("TRØNDELAG", SOR),
        ("troms  og\u00a0finnmark", NORD),
        ("Nordland\u00a0", NORD),
        ("møre og romsdal", SOR),
        ("\tSør-Trøndelag\n", SOR),
    ],
)
def test_skrivematen_spiller_ingen_rolle(fylke, omrade):
    assert omrade_fra_fylke(fylke) is omrade


def test_omradekodene_er_sor_nord_og_ukjent():
    # «sor» og «nord» er også kodene i API-et. Ukjent blir null der (AD-13).
    assert [o.value for o in Omrade] == ["sor", "nord", "ukjent"]
    assert Omrade.SOR == "sor"


def test_fylke_ma_vaere_tekst_eller_none():
    with pytest.raises(TypeError):
        omrade_fra_fylke(18)  # type: ignore[arg-type]


def test_tabellen_kan_ikke_endres():
    with pytest.raises(TypeError):
        FYLKER["Svalbard"] = NORD  # type: ignore[index]
