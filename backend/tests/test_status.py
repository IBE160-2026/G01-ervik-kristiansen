"""Tester for status etter R4 i marin.kjerne.status (Story 1.5, T5–T12).

Fasiten sjekker `f"{symbol} {tekst}"` tegn for tegn mot R4 og T5–T12 i briefen. Hver rad
i I/O-matrisen i spec-1-5 har minst én test her. Alle tilfellene er i sør med analyseuka
lik siste uke, hvis ikke annet står.
"""

import dataclasses
import inspect
from decimal import Decimal

import pytest
from hjelp_serie import T5, T6, T8, T12, fortlopende, lag_serie

from marin.kjerne.modeller import Telling, Uke
from marin.kjerne.omrade import Omrade
from marin.kjerne.status import Arsak, EstimertUke, Farge, Vurdering, vurder
from marin.kjerne.trend import siste_telling, trendlinje, uker_til_grensen, vindu

SOR, NORD, UKJENT = Omrade.SOR, Omrade.NORD, Omrade.UKJENT
D = Decimal

T9 = [(Uke(2026, 38), "0.20"), (Uke(2026, 40), "0.30")]
T11 = [(Uke(2026, 29), "0.30"), (Uke(2026, 30), "0.60")]
FLAT = fortlopende(Uke(2026, 36), "0.10", "0.10", "0.10", "0.10", "0.10")


def vist(vurdering: Vurdering) -> str:
    """Statusen slik den vises: symbol, mellomrom og tekst (R4)."""
    return f"{vurdering.symbol} {vurdering.tekst}"


def uten_prognose(vurdering: Vurdering) -> bool:
    """Sann når vurderingen verken har uke_tekst, estimert_uke eller trend."""
    return (vurdering.uke_tekst, vurdering.estimert_uke, vurdering.trend) == (None, None, None)


# Fasit fra briefen (R6), kontrollert i A4


def test_t5_folg_med_grensen_kan_nas_om_4_uker():
    v = vurder(lag_serie(T5), SOR, Uke(2026, 34))
    assert (v.farge, v.arsak) == (Farge.GUL, Arsak.FOLG_MED)
    assert vist(v) == "! Følg med: grensen kan nås om 4 uker"
    assert (v.uke_tekst, v.estimert_uke) == ("(uke 38)", EstimertUke(Uke(2026, 38), 4))


def test_t6_vargrensen_gir_varsel_om_2_uker():
    v = vurder(lag_serie(T6), SOR, Uke(2026, 14))
    assert (v.farge, v.arsak) == (Farge.ROD, Arsak.VARSEL)
    assert vist(v) == "✕ Varsel: grensen nås om 2 uker"
    assert (v.uke_tekst, v.estimert_uke) == ("(uke 16)", EstimertUke(Uke(2026, 16), 2))


@pytest.mark.parametrize("omrade", [UKJENT, "ukjent"])
def test_t7_ukjent_omrade_gir_gra_uten_prognose(omrade):
    a = Uke(2026, 34)
    v = vurder(lag_serie(T5), omrade, a)
    assert (v.farge, v.arsak) == (Farge.GRA, Arsak.UKJENT_OMRADE)
    assert vist(v) == "? Ukjent område: grensen kan ikke bestemmes"
    assert uten_prognose(v)
    assert v.siste_telling == Telling(a, D("0.30"))


def test_t8_folg_med_om_4_uker_i_uke_44():
    v = vurder(lag_serie(T8), SOR, Uke(2026, 40))
    assert (v.farge, v.arsak) == (Farge.GUL, Arsak.FOLG_MED)
    assert vist(v) == "! Følg med: grensen kan nås om 4 uker"
    assert (v.uke_tekst, v.estimert_uke) == ("(uke 44)", EstimertUke(Uke(2026, 44), 4))


def test_t9_to_tellinger_gir_for_lite_data():
    v = vurder(lag_serie(T9), SOR, Uke(2026, 40))
    assert (v.farge, v.arsak) == (Farge.GRA, Arsak.FOR_LITE_DATA)
    assert vist(v) == "– For lite data"
    assert uten_prognose(v)


def test_t10_analyseuke_42_gir_ingen_ny_telling_siden_uke_40():
    v = vurder(lag_serie(T8), SOR, Uke(2026, 42))
    assert (v.farge, v.arsak) == (Farge.GRA, Arsak.INGEN_NY_TELLING)
    assert vist(v) == "– Ingen ny telling siden uke 40"
    assert uten_prognose(v)
    assert v.siste_telling == Telling(Uke(2026, 40), D("0.36"))


def test_t10_analyseuke_41_gir_varsel_om_3_uker():
    v = vurder(lag_serie(T8), SOR, Uke(2026, 41))
    assert (v.farge, v.arsak) == (Farge.ROD, Arsak.VARSEL)
    assert vist(v) == "✕ Varsel: grensen nås om 3 uker"
    assert (v.uke_tekst, v.estimert_uke) == ("(uke 44)", EstimertUke(Uke(2026, 44), 3))


def test_t11_brudd_na_gar_foran_for_lite_data():
    v = vurder(lag_serie(T11), SOR, Uke(2026, 30))
    assert (v.farge, v.arsak) == (Farge.ROD, Arsak.BRUDD_NA)
    assert vist(v) == "✕ Brudd nå"
    assert v.estimert_uke is None
    assert uten_prognose(v)


def test_t12_arsskiftet_gir_varsel_om_1_uke():
    v = vurder(lag_serie(T12), SOR, Uke(2026, 2))
    assert (v.farge, v.arsak) == (Farge.ROD, Arsak.VARSEL)
    assert vist(v) == "✕ Varsel: grensen nås om 1 uke"
    assert (v.uke_tekst, v.estimert_uke) == ("(uke 3)", EstimertUke(Uke(2026, 3), 1))


# Resten av I/O-matrisen


def test_flat_linje_gir_gronn_ingen_kryssing():
    a = Uke(2026, 40)
    v = vurder(lag_serie(FLAT), SOR, a)
    assert (v.farge, v.arsak) == (Farge.GRONN, Arsak.INGEN_KRYSSING)
    assert vist(v) == "✓ Ingen kryssing ventet innen 6 uker"
    assert (v.uke_tekst, v.estimert_uke) == (None, None)
    assert v.trend == trendlinje(vindu(lag_serie(FLAT), a))


@pytest.mark.parametrize(
    ("verdier", "arsak", "tekst", "uke_tekst"),
    [
        (("0.43", "0.44", "0.45"), Arsak.FOLG_MED, "! Følg med: grensen kan nås om 5 uker", "(uke 37)"),
        (("0.42", "0.43", "0.44"), Arsak.FOLG_MED, "! Følg med: grensen kan nås om 6 uker", "(uke 38)"),
        (("0.41", "0.42", "0.43"), Arsak.INGEN_KRYSSING, "✓ Ingen kryssing ventet innen 6 uker", None),
    ],
    ids=["5 uker", "6 uker", "7 uker er utenfor horisonten"],
)
def test_gul_gjelder_til_og_med_6_uker_og_sa_gronn(verdier, arsak, tekst, uke_tekst):
    v = vurder(lag_serie(fortlopende(Uke(2026, 30), *verdier)), SOR, Uke(2026, 32))
    assert v.arsak is arsak
    assert vist(v) == tekst
    assert v.uke_tekst == uke_tekst


@pytest.mark.parametrize(
    "par",
    [[(Uke(2026, 15), "0.30")], [(Uke(2026, 15), "0.30"), (Uke(2026, 16), None)]],
    ids=["uke 16 mangler", "uke 16 uten verdi"],
)
def test_brudd_na_bruker_grensen_i_analyseuka(par):
    # 0,30 er under grensen 0,5 i uke 15, men over grensen 0,2 i uke 16.
    v = vurder(lag_serie(par), SOR, Uke(2026, 16))
    assert (v.farge, v.arsak) == (Farge.ROD, Arsak.BRUDD_NA)
    assert vist(v) == "✕ Brudd nå"
    assert v.siste_telling == Telling(Uke(2026, 15), D("0.30"))


def test_tellinger_etter_analyseuka_brukes_ikke_fr8():
    uten = lag_serie(T5)
    med = lag_serie([*T5, (Uke(2026, 36), "0.90")])
    v = vurder(med, SOR, Uke(2026, 34))
    assert v == vurder(uten, SOR, Uke(2026, 34))
    assert vist(v) == "! Følg med: grensen kan nås om 4 uker"
    assert vist(vurder(med, SOR, Uke(2026, 36))) == "✕ Brudd nå"


def test_tellinger_for_t_minus_4_brukes_ikke():
    a = Uke(2026, 34)
    # Bare uke 33 og 34 ligger i vinduet uke 30–34. Uke 20–22 teller ikke med.
    gamle = [(Uke(2026, uke), "0.10") for uke in (20, 21, 22)]
    v = vurder(lag_serie([*gamle, (Uke(2026, 33), "0.30"), (a, "0.30")]), SOR, a)
    assert v.arsak is Arsak.FOR_LITE_DATA
    assert vist(v) == "– For lite data"
    # 5,00 i uke 29 ligger fem uker før t og endrer verken tekst, trend eller estimert uke.
    assert vurder(lag_serie([(Uke(2026, 29), "5.00"), *T5]), SOR, a) == vurder(
        lag_serie(T5), SOR, a
    )


def test_siste_telling_i_et_annet_ar_far_ar_i_teksten():
    v = vurder(lag_serie([(Uke(2025, 50), "0.30")]), SOR, Uke(2026, 1))
    assert v.arsak is Arsak.INGEN_NY_TELLING
    assert vist(v) == "– Ingen ny telling siden uke 50, 2025"


def test_estimert_uke_i_neste_ar_far_ar_over_uke_53():
    # 2026 har uke 53 (estimat 0,46), og 2027 uke 1 gir 0,50, to uker etter analyseuka.
    serie = lag_serie(fortlopende(Uke(2026, 48), "0.26", "0.30", "0.34", "0.38", "0.42"))
    v = vurder(serie, SOR, Uke(2026, 52))
    assert (v.farge, v.arsak) == (Farge.ROD, Arsak.VARSEL)
    assert vist(v) == "✕ Varsel: grensen nås om 2 uker"
    assert (v.uke_tekst, v.estimert_uke) == ("(uke 1, 2027)", EstimertUke(Uke(2027, 1), 2))


@pytest.mark.parametrize(
    "par",
    [
        [],
        [(Uke(2026, 30), None), (Uke(2026, 31), None)],
        [(Uke(2026, 33), None), (Uke(2026, 35), "0.90")],
    ],
    ids=["tom serie", "bare tomme uker", "telling bare etter a"],
)
def test_ingen_telling_til_og_med_a_gir_for_lite_data(par):
    # 0 av de 5 siste ukene har telling (R2). Ingen egen tekst (avgjort 2026-11-23).
    v = vurder(lag_serie(par), SOR, Uke(2026, 34))
    assert (v.farge, v.arsak) == (Farge.GRA, Arsak.FOR_LITE_DATA)
    assert vist(v) == "– For lite data"
    assert v.siste_telling is None
    assert uten_prognose(v)


def test_ukjent_omradekode_gir_valueerror():
    with pytest.raises(ValueError, match="vest"):
        vurder(lag_serie(T5), "vest", Uke(2026, 34))


_SERIE = lag_serie(T5)
_A = Uke(2026, 34)


@pytest.mark.parametrize(
    "kall",
    [
        lambda: vurder(list(_SERIE.tellinger), SOR, _A),
        lambda: vurder(None, SOR, _A),
        lambda: vurder(_SERIE, 1, _A),
        lambda: vurder(_SERIE, None, _A),
        lambda: vurder(_SERIE, SOR, (2026, 34)),
        lambda: vurder(_SERIE, SOR, "2026-34"),
        lambda: vurder([], UKJENT, _A),
        lambda: vurder(_SERIE, UKJENT, 34),
        lambda: vurder(_SERIE, "vest", "2026-34"),
        lambda: EstimertUke((2026, 38), 4),
        lambda: EstimertUke(Uke(2026, 38), 4.0),
        lambda: EstimertUke(Uke(2026, 38), True),
    ],
    ids=[
        "serie som liste av tellinger",
        "serie som None",
        "område som heltall",
        "område som None",
        "analyseuke som tuppel",
        "analyseuke som tekst",
        "feil serie sjekkes før ukjent område",
        "feil analyseuke sjekkes før ukjent område",
        "feil analyseuke går foran ukjent områdekode",
        "EstimertUke med tuppel som uke",
        "EstimertUke med flyttall som uker_til",
        "EstimertUke med bool som uker_til",
    ],
)
def test_feil_type_gir_typeerror(kall):
    with pytest.raises(TypeError):
        kall()


# Rekkefølgen i R4: den første regelen som slår til, gjelder


@pytest.mark.parametrize(
    ("par", "omrade", "a", "arsak"),
    [
        # Ukjent område går foran alt, også når det ikke finnes noen telling.
        ([], UKJENT, Uke(2026, 34), Arsak.UKJENT_OMRADE),
        ([(Uke(2026, 30), "0.90")], UKJENT, Uke(2026, 34), Arsak.UKJENT_OMRADE),
        # Ingen ny telling går foran brudd nå: 0,90 i uke 30 er for gammel med a = 34.
        ([(Uke(2026, 30), "0.90")], SOR, Uke(2026, 34), Arsak.INGEN_NY_TELLING),
        # Én uke gammel telling er ny nok og gir brudd nå.
        ([(Uke(2026, 33), "0.90")], SOR, Uke(2026, 34), Arsak.BRUDD_NA),
        # Brudd nå går foran prognosen, også når linja er flat.
        (fortlopende(Uke(2026, 30), "0.50", "0.50", "0.50"), SOR, Uke(2026, 32), Arsak.BRUDD_NA),
        # Like under grensen er ikke brudd, og linja når grensen neste uke.
        (fortlopende(Uke(2026, 30), "0.45", "0.47", "0.49"), SOR, Uke(2026, 32), Arsak.VARSEL),
    ],
    ids=[
        "ukjent område uten tellinger",
        "ukjent område med gammel telling over grensen",
        "gammel telling over grensen",
        "telling i uka før over grensen",
        "brudd nå med flat linje",
        "0,49 er ikke brudd",
    ],
)
def test_forste_regel_som_slar_til_gjelder(par, omrade, a, arsak):
    assert vurder(lag_serie(par), omrade, a).arsak is arsak


# De 7 årsakene: farge, symbol og hvilke felt som finnes


# Symbolene står som tegnkoder, så et tegn som bare ligner (× i stedet for ✕, - i stedet
# for –) ikke slipper gjennom: ✕ U+2715, ! U+0021, ✓ U+2713, – U+2013 og ? U+003F.
ARSAKER = [
    (Arsak.VARSEL, T6, SOR, Uke(2026, 14), Farge.ROD, "\u2715", True, True),
    (Arsak.BRUDD_NA, T11, SOR, Uke(2026, 30), Farge.ROD, "\u2715", False, False),
    (Arsak.FOLG_MED, T5, SOR, Uke(2026, 34), Farge.GUL, "\u0021", True, True),
    (Arsak.INGEN_KRYSSING, FLAT, SOR, Uke(2026, 40), Farge.GRONN, "\u2713", False, True),
    (Arsak.FOR_LITE_DATA, T9, SOR, Uke(2026, 40), Farge.GRA, "\u2013", False, False),
    (Arsak.INGEN_NY_TELLING, T8, SOR, Uke(2026, 42), Farge.GRA, "\u2013", False, False),
    (Arsak.UKJENT_OMRADE, T5, UKJENT, Uke(2026, 34), Farge.GRA, "\u003f", False, False),
]


@pytest.mark.parametrize(
    ("arsak", "par", "omrade", "a", "farge", "symbol", "har_estimat", "har_trend"),
    ARSAKER,
    ids=[rad[0].value for rad in ARSAKER],
)
def test_hver_arsak_har_riktig_farge_symbol_og_felt(
    arsak, par, omrade, a, farge, symbol, har_estimat, har_trend
):
    serie = lag_serie(par)
    v = vurder(serie, omrade, a)
    assert (v.arsak, v.farge, v.symbol) == (arsak, farge, symbol)
    assert not v.tekst.startswith(v.symbol)
    assert v.siste_telling == siste_telling(serie, a)
    # estimert_uke og uke_tekst bare ved varsel og følg med (FR18).
    assert (v.estimert_uke is not None, v.uke_tekst is not None) == (har_estimat, har_estimat)
    # trend bare ved varsel, følg med og ingen kryssing.
    assert (v.trend is not None) == har_trend
    if har_trend:
        assert v.trend == trendlinje(vindu(serie, a))
    if har_estimat:
        assert v.estimert_uke.uker_til == uker_til_grensen(v.trend, omrade, a)


def test_tabellen_over_dekker_alle_arsakene():
    assert sorted(rad[0] for rad in ARSAKER) == sorted(Arsak)


def test_kodene_er_de_samme_som_i_ad_7():
    assert [f.value for f in Farge] == ["rod", "gul", "gronn", "gra"]
    assert {a.value for a in Arsak} == {
        "varsel",
        "brudd_na",
        "folg_med",
        "ingen_kryssing",
        "for_lite_data",
        "ingen_ny_telling",
        "ukjent_omrade",
    }
    assert Farge.ROD == "rod" and Arsak.BRUDD_NA == "brudd_na"


# Inngangen


def test_vurder_tar_bare_serie_omrade_og_analyseuke_fr27a():
    assert list(inspect.signature(vurder).parameters) == ["serie", "omrade", "analyseuke"]


@pytest.mark.parametrize("kode", ["sor", "nord", "ukjent"])
def test_omradekode_som_tekst_gir_samme_vurdering_som_omrade(kode):
    a = Uke(2026, 14)
    assert vurder(lag_serie(T6), kode, a) == vurder(lag_serie(T6), Omrade(kode), a)


def test_nord_har_vargrensen_i_uke_21_26():
    # T6 i nord: grensen er 0,5 i uke 15–20, så linja når den ikke innen 6 uker.
    v = vurder(lag_serie(T6), NORD, Uke(2026, 14))
    assert vist(v) == "✓ Ingen kryssing ventet innen 6 uker"
    # 0,30 i uke 20 er brudd med grensen 0,2 i uke 21, men ikke med 0,5 i uke 20.
    serie = lag_serie([(Uke(2026, 20), "0.30")])
    assert vist(vurder(serie, NORD, Uke(2026, 21))) == "✕ Brudd nå"
    assert vist(vurder(serie, NORD, Uke(2026, 20))) == "– For lite data"


def test_vurderingen_er_frossen():
    v = vurder(lag_serie(T5), SOR, Uke(2026, 34))
    with pytest.raises(dataclasses.FrozenInstanceError):
        v.farge = Farge.ROD
