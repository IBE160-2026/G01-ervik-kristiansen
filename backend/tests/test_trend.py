"""Tester for trend og uker til grensen etter R2 og R3 i marin.kjerne.trend (Story 1.4).

Fasiten T5, T6, T8, T10 og T12 er hentet fra den kontrollerte håndregningen i
_bmad-output/planning-artifacts/briefs/brief-Marin-2026-09-17/a4-handkontroll.md. Alle
tilfellene er i sør med analyseuka lik siste uke, hvis ikke annet står.
"""

import ast
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest
from hjelp_serie import T5, T6, T8, T12, fortlopende, lag_serie

import marin.kjerne.trend as trendmodul
from marin.kjerne.konstanter import HORISONT, MAKS_UKER_ROD, MINSTE_TELLINGER, VINDU
from marin.kjerne.modeller import Telling, Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.trend import (
    Trend,
    siste_telling,
    trendlinje,
    uker_til_grensen,
    vindu,
)
from marin.kjerne.uker import alle_uker, lopende, pluss

SOR, NORD, UKJENT = Omrade.SOR, Omrade.NORD, Omrade.UKJENT
D = Decimal


def estimater(trend: Trend, analyseuke: Uke, antall: int) -> list[str]:
    """Estimatene i uke a + 1 til a + antall, som tekst."""
    return [str(trend.estimat(pluss(analyseuke, k))) for k in range(1, antall + 1)]


def eksakt(trend: Trend, uke: Uke) -> Fraction:
    """Verdien på linja i uka før avrunding, for å sjekke regnestykket i fasiten."""
    return trend.y_snitt + trend.stigning * (lopende(uke) - trend.x_snitt)


# Fasit fra briefen (R6), kontrollert i A4


def test_t5_stigning_0_06_og_grensen_nas_om_4_uker():
    a = Uke(2026, 34)
    serie = lag_serie(T5)
    assert siste_telling(serie, a) == Telling(a, D("0.30"))
    assert [t.uke.uke for t in vindu(serie, a)] == [30, 31, 32, 33, 34]
    trend = trendlinje(vindu(serie, a))
    assert trend.stigning == Fraction("0.06")
    assert trend.estimat(Uke(2026, 37)) == D("0.48")
    assert trend.estimat(Uke(2026, 38)) == D("0.54")
    assert estimater(trend, a, 4) == ["0.36", "0.42", "0.48", "0.54"]
    assert uker_til_grensen(trend, SOR, a) == 4


def test_t6_vargrensen_i_uke_16_gir_2_uker():
    a = Uke(2026, 14)
    trend = trendlinje(vindu(lag_serie(T6), a))
    assert trend.stigning == Fraction("0.02")
    assert trend.estimat(Uke(2026, 15)) == D("0.20")
    assert trend.estimat(Uke(2026, 16)) == D("0.22")
    assert uker_til_grensen(trend, SOR, a) == 2


def test_t6_med_grensen_0_5_i_alle_ukene_gir_ingen_kryssing():
    # R3: i nord er grensen 0,5 i uke 15–20. Det samme ville sør fått om grensen i
    # analyseuka ble brukt for hele horisonten. Høyeste estimat er 0,30 i uke 20.
    a = Uke(2026, 14)
    trend = trendlinje(vindu(lag_serie(T6), a))
    assert estimater(trend, a, HORISONT) == ["0.20", "0.22", "0.24", "0.26", "0.28", "0.30"]
    assert uker_til_grensen(trend, NORD, a) is None


def test_slutten_pa_vargrensen_i_sor_gir_ingen_kryssing():
    # R3: 0,19 i uke 21 er under 0,2, og 0,21 i uke 22 er under 0,5.
    a = Uke(2026, 18)
    serie = lag_serie(fortlopende(Uke(2026, 14), "0.05", "0.07", "0.09", "0.11", "0.13"))
    trend = trendlinje(vindu(serie, a))
    assert trend.estimat(Uke(2026, 21)) == D("0.19")
    assert trend.estimat(Uke(2026, 22)) == D("0.21")
    assert uker_til_grensen(trend, SOR, a) is None


def test_vargrensen_i_nord_gjelder_i_uke_21_26():
    # R3: 0,20 i uke 25 er brudd i nord (0,2), men ikke i sør (0,5 fra uke 22).
    a = Uke(2026, 19)
    serie = lag_serie(fortlopende(Uke(2026, 15), "0.10", "0.11", "0.12", "0.13", "0.14"))
    trend = trendlinje(vindu(serie, a))
    assert uker_til_grensen(trend, NORD, a) == 6
    assert uker_til_grensen(trend, SOR, a) is None


@pytest.mark.parametrize(("kode", "svar"), [("sor", 2), ("nord", None)])
def test_omradekode_som_tekst_gir_samme_svar_som_omrade(kode, svar):
    a = Uke(2026, 14)
    trend = trendlinje(vindu(lag_serie(T6), a))
    assert uker_til_grensen(trend, kode, a) == uker_til_grensen(trend, Omrade(kode), a) == svar


def test_ukjent_omradekode_gir_valueerror():
    trend = trendlinje(vindu(lag_serie(T6), Uke(2026, 14)))
    with pytest.raises(ValueError, match="vest"):
        uker_til_grensen(trend, "vest", Uke(2026, 14))


def test_t8_stigning_per_uke_er_0_04_og_ikke_0_08():
    a = Uke(2026, 40)
    serie = lag_serie(T8)
    assert [t.uke.uke for t in vindu(serie, a)] == [36, 38, 40]
    trend = trendlinje(vindu(serie, a))
    assert trend.stigning == Fraction("0.04")
    assert trend.stigning != Fraction("0.08")
    assert trend.estimat(Uke(2026, 43)) == D("0.48")
    assert trend.estimat(Uke(2026, 44)) == D("0.52")
    assert uker_til_grensen(trend, SOR, a) == 4


def test_t10_analyseuke_41_teller_fra_a_og_gir_3_uker():
    a = Uke(2026, 41)
    serie = lag_serie(T8)
    assert siste_telling(serie, a).uke == Uke(2026, 40)
    assert vindu(serie, a) == vindu(serie, Uke(2026, 40))
    trend = trendlinje(vindu(serie, a))
    assert trend == trendlinje(vindu(serie, Uke(2026, 40)))
    assert estimater(trend, a, 3) == ["0.44", "0.48", "0.52"]
    assert uker_til_grensen(trend, SOR, a) == 3


def test_t10_vindu_sjekker_ikke_om_t_er_for_gammel():
    # Med analyseuke 42 er t = 40 for gammel. Det avgjør statusen i Story 1.5, ikke vindu.
    serie = lag_serie(T8)
    assert siste_telling(serie, Uke(2026, 42)).uke == Uke(2026, 40)
    assert vindu(serie, Uke(2026, 42)) == vindu(serie, Uke(2026, 40))


def test_t12_arsskiftet_er_ett_steg_og_gir_noyaktig_0_50():
    a = Uke(2026, 2)
    serie = lag_serie(T12)
    assert len(vindu(serie, a)) == 5
    trend = trendlinje(vindu(serie, a))
    assert trend.stigning == Fraction("0.04")
    assert eksakt(trend, Uke(2026, 3)) == Fraction(1, 2)
    assert trend.estimat(Uke(2026, 3)) == D("0.50")
    assert uker_til_grensen(trend, SOR, a) == 1


# Spesialtilfeller i matrisen


def test_negativt_estimat_blir_0_00_fr13():
    a = Uke(2026, 34)
    serie = lag_serie(fortlopende(Uke(2026, 30), "0.40", "0.30", "0.20", "0.10", "0.00"))
    trend = trendlinje(vindu(serie, a))
    assert trend.stigning == Fraction("-0.10")
    assert eksakt(trend, Uke(2026, 35)) == Fraction("-0.10")
    assert str(trend.estimat(Uke(2026, 35))) == "0.00"
    assert all(e == "0.00" for e in estimater(trend, a, HORISONT))
    assert uker_til_grensen(trend, SOR, a) is None


def test_eksakt_0_495_avrundes_opp_til_0_50_og_gir_1_uke():
    a = Uke(2026, 34)
    serie = lag_serie(fortlopende(Uke(2026, 30), "0", "0", "0", "0.35", "0.40"))
    trend = trendlinje(vindu(serie, a))
    assert eksakt(trend, Uke(2026, 35)) == Fraction("0.495")
    assert str(trend.estimat(Uke(2026, 35))) == "0.50"
    assert uker_til_grensen(trend, SOR, a) == 1


def test_eksakt_0_495_med_tredjedeler_gir_0_50_og_2_uker():
    # Tre tellinger gir ȳ = 0,34/3, som ikke kan skrives som et endelig desimaltall. Med
    # Decimal-divisjon blir estimatet i uke 36 litt under 0,495, altså 0,49 og 3 uker.
    a = Uke(2026, 34)
    serie = lag_serie(
        [(Uke(2026, 30), "0.00"), (Uke(2026, 31), "0.01"), (Uke(2026, 34), "0.33")]
    )
    trend = trendlinje(vindu(serie, a))
    assert eksakt(trend, Uke(2026, 36)) == Fraction(99, 200)
    assert str(trend.estimat(Uke(2026, 36))) == "0.50"
    assert uker_til_grensen(trend, SOR, a) == 2


def test_tellinger_etter_analyseuka_brukes_ikke_fr8():
    a = Uke(2026, 34)
    uten = lag_serie(T5)
    med = lag_serie([*T5, (Uke(2026, 35), "9.99")])
    assert siste_telling(med, a) == siste_telling(uten, a)
    assert vindu(med, a) == vindu(uten, a)
    trend = trendlinje(vindu(med, a))
    assert trend == trendlinje(vindu(uten, a))
    assert uker_til_grensen(trend, SOR, a) == 4


def test_tom_analyseuke_gir_t_lik_uka_for():
    a = Uke(2026, 34)
    serie = lag_serie(
        fortlopende(Uke(2026, 28), "0.10", "0.11", "0.12", "0.13", "0.14", "0.15", None)
    )
    assert siste_telling(serie, a) == Telling(Uke(2026, 33), D("0.15"))
    # Vinduet er a − 5 til a − 1. Tellingen i uke 28 er utenfor.
    assert [t.uke.uke for t in vindu(serie, a)] == [29, 30, 31, 32, 33]


@pytest.mark.parametrize(
    "par",
    [
        [],
        [(Uke(2026, 30), None), (Uke(2026, 31), None)],
        [(Uke(2026, 33), None), (Uke(2026, 35), "0.20")],
    ],
    ids=["tom serie", "bare tomme uker", "telling bare etter a"],
)
def test_ingen_telling_til_og_med_a(par):
    serie = lag_serie(par)
    assert siste_telling(serie, Uke(2026, 34)) is None
    assert vindu(serie, Uke(2026, 34)) == ()


def test_horisonten_over_uke_53_er_ett_steg_per_uke():
    a = Uke(2026, 52)
    serie = lag_serie(fortlopende(Uke(2026, 48), "0.26", "0.30", "0.34", "0.38", "0.42"))
    trend = trendlinje(vindu(serie, a))
    assert trend.estimat(Uke(2026, 53)) == D("0.46")
    assert trend.estimat(Uke(2027, 1)) == D("0.50")
    assert uker_til_grensen(trend, SOR, a) == 2


def test_vinduet_over_uke_53():
    a = Uke(2027, 1)
    serie = lag_serie(fortlopende(Uke(2026, 49), "0.20", "0.30", "0.34", "0.38", "0.42", "0.46"))
    assert [t.uke for t in vindu(serie, a)] == alle_uker(Uke(2026, 50), Uke(2027, 1))
    trend = trendlinje(vindu(serie, a))
    assert trend.stigning == Fraction("0.04")
    assert trend.estimat(Uke(2027, 2)) == D("0.50")
    assert uker_til_grensen(trend, SOR, a) == 1


def test_t9_to_tellinger_er_for_fa():
    # T9: telling bare i uke t − 2 og t.
    a = Uke(2026, 40)
    serie = lag_serie([(Uke(2026, 38), "0.20"), (Uke(2026, 40), "0.30")])
    assert len(vindu(serie, a)) == 2
    with pytest.raises(ValueError, match="minst"):
        trendlinje(vindu(serie, a))


def test_tomt_vindu_gir_valueerror():
    with pytest.raises(ValueError, match="minst"):
        trendlinje(())


@pytest.mark.parametrize("omrade", [UKJENT, "ukjent"])
def test_ukjent_omrade_gir_valueerror(omrade):
    trend = trendlinje(vindu(lag_serie(T5), Uke(2026, 34)))
    with pytest.raises(ValueError, match="ukjent"):
        uker_til_grensen(trend, omrade, Uke(2026, 34))


# Manglende rader og rader med None er det samme


@pytest.mark.parametrize(
    ("par", "a", "svar"),
    [
        (T5, Uke(2026, 34), 4),
        (T8, Uke(2026, 40), 4),
        (T8, Uke(2026, 41), 3),
        (T12, Uke(2026, 2), 1),
        # Hull i uke 31 og ingen telling i analyseuka. Linja når nøyaktig 0,50 i uke 40.
        (
            [(Uke(2026, 30), "0.30"), (Uke(2026, 32), "0.34"), (Uke(2026, 33), "0.36")],
            Uke(2026, 34),
            6,
        ),
    ],
    ids=["T5", "T8", "T10b", "T12", "hull og tom analyseuke"],
)
def test_manglende_rader_og_rader_med_none_gir_samme_svar(par, a, svar):
    # Alle uker uten telling fra a − 9 til a + 2 får en rad med None.
    uten_hull = lag_serie(par)
    kjente = {uke for uke, _ in par}
    tomme = [uke for uke in alle_uker(pluss(a, -9), pluss(a, 2)) if uke not in kjente]
    med_none = lag_serie([*par, *((uke, None) for uke in tomme)])
    assert len(med_none.tellinger) > len(uten_hull.tellinger)
    assert siste_telling(med_none, a) == siste_telling(uten_hull, a)
    assert vindu(med_none, a) == vindu(uten_hull, a)
    trend = trendlinje(vindu(med_none, a))
    assert trend == trendlinje(vindu(uten_hull, a))
    assert uker_til_grensen(trend, SOR, a) == svar


# Horisont, parametre og trendlinja


def test_kryssing_i_uke_a_pluss_6_er_med_og_a_pluss_7_er_utenfor():
    a = Uke(2026, 34)
    i_horisonten = lag_serie(fortlopende(Uke(2026, 30), "0.30", "0.32", "0.34", "0.36", "0.38"))
    utenfor = lag_serie(fortlopende(Uke(2026, 30), "0.28", "0.30", "0.32", "0.34", "0.36"))
    assert uker_til_grensen(trendlinje(vindu(i_horisonten, a)), SOR, a) == 6
    trend = trendlinje(vindu(utenfor, a))
    assert trend.estimat(pluss(a, 7)) == D("0.50")
    assert uker_til_grensen(trend, SOR, a) is None


def test_parameterne_er_fryst_etter_fr27a():
    assert (VINDU, MINSTE_TELLINGER, HORISONT) == (5, 3, 6)
    assert MAKS_UKER_ROD == 3


def test_tellinger_utenfor_vinduet_brukes_ikke():
    # Uke 29 ligger fem uker før t og er utenfor vinduet t − 4 til t.
    a = Uke(2026, 34)
    serie = lag_serie([(Uke(2026, 29), "5.00"), *T5])
    assert vindu(serie, a) == vindu(lag_serie(T5), a)


def test_rekkefolgen_pa_tellingene_betyr_ikke_noe():
    tellinger = vindu(lag_serie(T8), Uke(2026, 40))
    assert trendlinje(reversed(tellinger)) == trendlinje(tellinger)


def test_flat_linje_gir_stigning_0():
    a = Uke(2026, 34)
    trend = trendlinje(vindu(lag_serie(fortlopende(Uke(2026, 32), "0.25", "0.25", "0.25")), a))
    assert trend.stigning == 0
    assert estimater(trend, a, HORISONT) == ["0.25"] * HORISONT
    assert uker_til_grensen(trend, SOR, a) is None


def test_trendlinje_krever_verdi_i_alle_tellingene():
    tellinger = [Telling(Uke(2026, 30), D("0.1")), Telling(Uke(2026, 31), None)]
    tellinger.append(Telling(Uke(2026, 32), D("0.2")))
    tellinger.append(Telling(Uke(2026, 33), D("0.3")))
    with pytest.raises(ValueError, match="ingen verdi"):
        trendlinje(tellinger)


def test_trendlinje_krever_ulike_uker():
    tellinger = [Telling(Uke(2026, 30), D("0.1"))] * 2 + [Telling(Uke(2026, 31), D("0.2"))]
    with pytest.raises(ValueError, match="ulike uker"):
        trendlinje(tellinger)


# Feil type inn gir TypeError, som i resten av kjernen

_SERIE = lag_serie(T5)
_A = Uke(2026, 34)
_TREND = trendlinje(vindu(_SERIE, _A))


@pytest.mark.parametrize(
    "kall",
    [
        lambda: siste_telling(list(_SERIE.tellinger), _A),
        lambda: siste_telling(_SERIE, (2026, 34)),
        lambda: vindu(_SERIE, 34),
        lambda: trendlinje([(Uke(2026, 30), D("0.1"))] * 3),
        lambda: trendlinje(_SERIE),
        lambda: _TREND.estimat(35),
        lambda: uker_til_grensen("trend", SOR, _A),
        lambda: uker_til_grensen(_TREND, 1, _A),
        lambda: uker_til_grensen(_TREND, SOR, "2026-34"),
        lambda: uker_til_grensen(_TREND, "vest", "2026-34"),
        lambda: Trend(0.06, Fraction(32), Fraction("0.18")),
        lambda: Trend(Fraction("0.06"), Fraction(32), D("0.18")),
    ],
    ids=[
        "siste_telling med liste i stedet for serie",
        "siste_telling med tuppel som uke",
        "vindu med heltall som uke",
        "trendlinje med tupler i stedet for tellinger",
        "trendlinje tar ikke en Serie, bare tellingene",
        "estimat med heltall som uke",
        "uker_til_grensen med tekst som trend",
        "uker_til_grensen med heltall som område",
        "uker_til_grensen med tekst som analyseuke",
        "feil analyseuke går foran ukjent områdekode",
        "Trend med flyttall som stigning",
        "Trend med Decimal som snitt",
    ],
)
def test_feil_type_gir_typeerror(kall):
    with pytest.raises(TypeError):
        kall()


# Regresjonen er eksakt (AD-6)


def test_regresjonen_bruker_ikke_flyttall_eller_decimal_regning():
    tre = ast.parse(Path(trendmodul.__file__).read_text(encoding="utf-8"))
    navn = {node.id for node in ast.walk(tre) if isinstance(node, ast.Name)}
    assert "float" not in navn
    assert not [
        node for node in ast.walk(tre)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    # Sjekken finner bare kall til Decimal(...), ikke regning med Decimal-verdiene fra
    # tellingene. At regnestykket er eksakt, viser testen med tredjedeler
    # (test_eksakt_0_495_med_tredjedeler_gir_0_50_og_2_uker).
    assert not [
        node for node in ast.walk(tre)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Decimal"
    ]


def test_estimatet_er_decimal_med_to_desimaler():
    trend = trendlinje(vindu(lag_serie(T8), Uke(2026, 40)))
    # Stigning 0,04 og ȳ 0,28 gir eksakte hundredeler. Ujevne uker gir brøker med
    # tredjedeler, og de avrundes også til to desimaler.
    ujevn = trendlinje(
        [
            Telling(Uke(2026, 36), D("0.20")),
            Telling(Uke(2026, 37), D("0.21")),
            Telling(Uke(2026, 40), D("0.36")),
        ]
    )
    for estimat in (trend.estimat(Uke(2026, 41)), ujevn.estimat(Uke(2026, 41))):
        assert isinstance(estimat, Decimal)
        assert estimat.as_tuple().exponent == -2
