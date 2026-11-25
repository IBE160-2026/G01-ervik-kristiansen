"""Tester for backtesten etter SK2 i marin.kjerne.treffsikkerhet (Story 1.6).

Hver rad i I/O-matrisen i spec-1-6 har minst én test her, merket med radens navn. Alle
tilfellene er i sør i 2026, hvis ikke annet står. Det lille datasettet sjekkes mot
fasiten i tests/data/backtest_liten.md, som er regnet ut for hånd.
"""

import dataclasses
import inspect
import json
import re
from decimal import Decimal
from pathlib import Path

import pytest
from hjelp_serie import T6, fortlopende, lag_serie

from marin.kilder.datasett import Datasett
from marin.kjerne import treffsikkerhet
from marin.kjerne.konstanter import FORSTE_UKE, HORISONT, MAKS_UKER_ROD, MINSTE_TELLINGER, SISTE_UKE, VINDU
from marin.kjerne.modeller import Uke
from marin.kjerne.omrade import Omrade, omrade_fra_fylke
from marin.kjerne.status import Arsak, vurder
from marin.kjerne.treffsikkerhet import (
    FORSTE_KRYSSING,
    SISTE_VARSEL,
    Backtestresultat,
    backtest,
    er_treff,
    fulgt_av_brudd,
    kryssinger,
)
from marin.kjerne.uker import alle_uker, pluss

SOR, NORD, UKJENT = Omrade.SOR, Omrade.NORD, Omrade.UKJENT
DATA = Path(__file__).parent / "data"


def u(uke: int, ar: int = 2026) -> Uke:
    return Uke(ar, uke)


def uker(*nummer: int, ar: int = 2026) -> set[Uke]:
    return {u(n, ar) for n in nummer}


def varselsuker(serie, omrade) -> list[Uke]:
    """Ukene fra FORSTE_UKE til SISTE_UKE der statusen har årsak varsel."""
    return [a for a in alle_uker(FORSTE_UKE, SISTE_UKE) if vurder(serie, omrade, a).arsak is Arsak.VARSEL]


def resultat(**antall) -> Backtestresultat:
    """Et resultat med 1 av 1 kryssing og varsel, der `antall` overstyrer."""
    felt = dict(
        antall_kryssinger=1,
        antall_treff=1,
        antall_varsler=1,
        antall_varsler_med_brudd=1,
        utelatt_kryssinger=0,
        utelatt_varsler=0,
    )
    return Backtestresultat(**(felt | antall))


KRYSSING_UKA_FOR = [(u(30), "0.40"), (u(31), "0.50")]
# Tellinger som gir ett varsel i uke 38 og ett i uke 39, 2026, og ingen kryssing.
VARSEL_38_OG_39 = fortlopende(u(36), "0.30", "0.36", "0.42")


# Kryssinger


def test_kryssing_uka_for():
    assert kryssinger(lag_serie(KRYSSING_UKA_FOR), SOR) == (u(31),)


@pytest.mark.parametrize(
    "tellinger",
    [
        [(u(30), "0.40"), (u(31), None), (u(32), "0.55")],
        [(u(30), "0.40"), (u(32), "0.55")],
    ],
    ids=["tom uke uten verdi", "uke som mangler"],
)
def test_kryssing_w_minus_2(tellinger):
    assert kryssinger(lag_serie(tellinger), SOR) == (u(32),)


def test_to_tomme_uker_gir_ingen_kryssing():
    serie = lag_serie([(u(29), "0.40"), (u(30), None), (u(31), None), (u(32), "0.60")])
    assert kryssinger(serie, SOR) == ()


def test_allerede_over_gir_ingen_kryssing():
    assert kryssinger(lag_serie([(u(30), "0.50"), (u(31), "0.60")]), SOR) == ()


def test_grense_i_sin_uke():
    # 0,30 er under 0,5 i uke 15 og over 0,2 i uke 16.
    assert kryssinger(lag_serie([(u(15), "0.30"), (u(16), "0.30")]), SOR) == (u(16),)
    # 0,30 er over 0,2 i uke 21 (uten telling før) og under 0,5 i uke 22.
    assert kryssinger(lag_serie([(u(21), "0.30"), (u(22), "0.30")]), SOR) == ()


def test_grense_i_sin_uke_i_nord():
    # Vårgrensen i nord er uke 21–26, så uke 16 har grensen 0,5 i nord.
    serie = lag_serie([(u(15), "0.30"), (u(16), "0.30"), (u(20), "0.30"), (u(21), "0.30")])
    assert kryssinger(serie, NORD) == (u(21),)
    assert kryssinger(serie, "nord") == (u(21),)


def test_kryssingene_er_stigende_og_teller_alle_i_serien():
    serie = lag_serie([(u(1, 2024), "0.10"), (u(2, 2024), "0.60"), (u(30), "0.40"), (u(31), "0.50"), (u(32), "0.20"), (u(33), "0.70")])
    assert kryssinger(serie, SOR) == (u(2, 2024), u(31), u(33))


@pytest.mark.parametrize("omrade", [UKJENT, "ukjent"])
def test_ukjent_omrade_gir_ingen_kryssinger_og_ingen_varsler(omrade):
    serie = lag_serie(KRYSSING_UKA_FOR + T6)
    assert kryssinger(serie, omrade) == ()
    assert varselsuker(serie, omrade) == []
    assert not fulgt_av_brudd(serie, omrade, u(30))
    # I sør gir tellingene én kryssing (uke 31). T6 gir varsel i uke 14, som i fasiten, og
    # også i uke 13 og 15, når vårgrensen i uke 16 er innen 3 uker.
    assert kryssinger(serie, SOR) == (u(31),)
    assert varselsuker(serie, SOR) == [u(13), u(14), u(15)]
    # Det ukjente anlegget legger ingenting til i backtesten.
    assert backtest([(serie, SOR), (serie, omrade)]) == backtest([(serie, SOR)])


# Treff


@pytest.mark.parametrize("rode", [uker(27, 28, 29, 30), uker(28, 29, 30), uker(29, 30)], ids=["w-4", "w-3", "w-2"])
def test_treff(rode):
    assert er_treff(u(31), rode)


@pytest.mark.parametrize(
    "rode",
    [uker(30), uker(26, 27, 28, 29, 30), set(), uker(27, 28, 29), uker(25, 26, 27, 28, 29, 30)],
    ids=["bare w-1", "w-5", "ingen rod", "ingen rod i w-1", "w-6"],
)
def test_ikke_treff(rode):
    assert not er_treff(u(31), rode)


def test_brutt_periode():
    # Uke 27 er ikke rød, så perioden som slutter i uke 30, begynte i uke 28.
    assert er_treff(u(31), uker(26, 28, 29, 30))


def test_over_arsskiftet():
    # 2025 har 52 uker. Perioden 2025 uke 51 til 2026 uke 1 begynte i w − 3.
    rode = {u(51, 2025), u(52, 2025), u(1)}
    assert er_treff(u(2), rode)
    assert not er_treff(u(2), rode | {u(50, 2025), u(49, 2025)})


def test_eksemplene_i_spec():
    assert er_treff(u(31), uker(28, 29, 30))
    assert not er_treff(u(31), uker(26, 27, 28, 29, 30))


def test_brudd_na_i_perioden_teller_som_rod():
    # Uke 31 er grå, uke 32 er brudd nå og uke 33 er varsel. Kryssingen i uke 34 er et
    # treff, fordi den røde perioden begynte i uke 32 = w − 2. Kryssingen i uke 32 er ikke.
    r = backtest([(lag_serie(fortlopende(u(30), "0.30", "0.40", "0.55", "0.45", "0.60")), SOR)])
    assert (r.antall_kryssinger, r.antall_treff, r.antall_varsler) == (2, 1, 1)


def test_er_treff_tar_ukene_som_liste_og_sjekker_typen():
    assert er_treff(u(31), [u(29), u(30)])
    with pytest.raises(TypeError):
        er_treff((2026, 31), uker(29, 30))  # type: ignore[arg-type]


# Varsler fulgt av brudd


def test_brudd_etter_varsel():
    assert fulgt_av_brudd(lag_serie([(u(30), "0.40"), (u(34), "0.50")]), SOR, u(30))
    assert not fulgt_av_brudd(lag_serie([(u(30), "0.40"), (u(35), "0.50")]), SOR, u(30))


def test_brudd_i_varselsuka_eller_uka_etter_den_fjerde_teller_ikke():
    serie = lag_serie([(u(30), "0.60"), (u(31), "0.10"), (u(34), "0.49"), (u(35), "0.90")])
    assert not fulgt_av_brudd(serie, SOR, u(30))


def test_uker_uten_verdi_er_ikke_brudd():
    serie = lag_serie([(u(31), None), (u(32), None), (u(33), "0.49")])
    assert not fulgt_av_brudd(serie, SOR, u(30))


def test_vargrense_etter_varsel():
    serie = lag_serie([(u(12), "0.15"), (u(16), "0.25")])
    assert fulgt_av_brudd(serie, SOR, u(12))
    # I nord er grensen i uke 16 0,5.
    assert not fulgt_av_brudd(serie, NORD, u(12))


# Utelatte


def test_grensene_for_utelatte():
    assert (FORSTE_KRYSSING, SISTE_VARSEL) == (u(9, 2025), u(38))
    # Et varsel trenger de 4 neste ukene i dataene, så SISTE_VARSEL følger SISTE_UKE.
    assert pluss(SISTE_VARSEL, 4) == SISTE_UKE


def test_utelatte():
    anlegg = [
        (lag_serie([(u(7, 2025), "0.30"), (u(8, 2025), "0.60")]), SOR),  # kryssing i uke 8, 2025
        (lag_serie([(u(8, 2025), "0.30"), (u(9, 2025), "0.60")]), SOR),  # kryssing i uke 9, 2025
        (lag_serie(VARSEL_38_OG_39), SOR),  # varsel i uke 38 og 39, 2026
    ]
    assert [kryssinger(serie, omrade) for serie, omrade in anlegg[:2]] == [(u(8, 2025),), (u(9, 2025),)]
    assert varselsuker(*anlegg[2]) == [u(38), u(39)]

    r = backtest(anlegg)
    assert (r.antall_kryssinger, r.utelatt_kryssinger) == (1, 1)
    assert (r.antall_varsler, r.utelatt_varsler) == (1, 1)


# Det lille datasettet


def fasit() -> dict[str, Decimal]:
    """Tabellen «Fasit» i backtest_liten.md, som er regnet ut for hånd."""
    tekst = (DATA / "backtest_liten.md").read_text(encoding="utf-8")
    seksjon = tekst.split("## Fasit", 1)[1]
    rader = re.findall(r"^\| `(\w+)` \| ([0-9.]+) \|$", seksjon, flags=re.MULTILINE)
    return {navn: Decimal(verdi) for navn, verdi in rader}


def test_lite_datasett_gir_tallene_regnet_ut_for_hand():
    datasett = Datasett.fra_json((DATA / "backtest_liten.json").read_text(encoding="utf-8"))
    r = backtest((serie, omrade_fra_fylke(info.fylke)) for info, serie in datasett.anlegg)
    forventet = fasit()
    assert list(forventet) == [f.name for f in dataclasses.fields(r)][3:]
    assert {navn: getattr(r, navn) for navn in forventet} == forventet


def test_lite_datasett_har_ett_anlegg_per_omrade_som_trengs():
    datasett = Datasett.fra_json((DATA / "backtest_liten.json").read_text(encoding="utf-8"))
    omrader = {omrade_fra_fylke(info.fylke) for info, _ in datasett.anlegg}
    assert omrader == {SOR, NORD, UKJENT}


# Tom nevner


def test_tom_nevner_gir_valueerror():
    with pytest.raises(ValueError, match="kryssinger"):
        backtest([(lag_serie(VARSEL_38_OG_39), SOR)])  # varsler, men ingen kryssinger
    with pytest.raises(ValueError, match="varsler"):
        backtest([(lag_serie(KRYSSING_UKA_FOR), SOR)])  # kryssing, men ingen varsler
    with pytest.raises(ValueError):
        backtest([])


# Backtestresultat


def test_feltene_og_konstantene():
    r = resultat(antall_kryssinger=4, antall_treff=1, antall_varsler=8, antall_varsler_med_brudd=2)
    assert [f.name for f in dataclasses.fields(r)] == [
        "versjon",
        "parametere",
        "siste_uke",
        "antall_kryssinger",
        "antall_treff",
        "antall_varsler",
        "antall_varsler_med_brudd",
        "utelatt_kryssinger",
        "utelatt_varsler",
        "treffandel",
        "presisjon",
    ]
    assert (r.versjon, r.siste_uke) == (1, SISTE_UKE)
    assert dict(r.parametere) == {
        "vindu": VINDU,
        "minste_tellinger": MINSTE_TELLINGER,
        "horisont": HORISONT,
        "maks_uker_rod": MAKS_UKER_ROD,
    }
    assert (r.treffandel, r.presisjon) == (Decimal("0.2500"), Decimal("0.2500"))


@pytest.mark.parametrize(
    ("teller", "nevner", "andel"),
    [
        (1, 3, "0.3333"),
        (2, 3, "0.6667"),
        (1, 32, "0.0313"),  # 0,03125 eksakt: halvdelen rundes opp
        (1, 64, "0.0156"),  # 0,015625: over halvdelen
        (3, 64, "0.0469"),  # 0,046875
        (7, 9, "0.7778"),
        (0, 5, "0.0000"),
        (5, 5, "1.0000"),
    ],
)
def test_andelene_avrundes_til_4_desimaler_med_halvdeler_opp(teller, nevner, andel):
    r = resultat(antall_kryssinger=nevner, antall_treff=teller, antall_varsler=nevner, antall_varsler_med_brudd=teller)
    assert str(r.treffandel) == andel
    assert str(r.presisjon) == andel


def test_parameterne_kan_ikke_overstyres():
    for navn in ("versjon", "parametere", "siste_uke", "treffandel", "presisjon"):
        with pytest.raises(TypeError):
            resultat(**{navn: 2})
    r = resultat()
    with pytest.raises(TypeError):
        r.parametere["vindu"] = 4  # type: ignore[index]
    with pytest.raises(dataclasses.FrozenInstanceError):
        r.antall_treff = 0  # type: ignore[misc]
    assert list(inspect.signature(backtest).parameters) == ["anlegg"]


@pytest.mark.parametrize(
    ("antall", "feil"),
    [
        ({"antall_kryssinger": 0, "antall_treff": 0}, ValueError),
        ({"antall_varsler": 0, "antall_varsler_med_brudd": 0}, ValueError),
        ({"antall_treff": 2}, ValueError),
        ({"antall_varsler_med_brudd": 2}, ValueError),
        ({"utelatt_varsler": -1}, ValueError),
        ({"antall_treff": True}, TypeError),
        ({"antall_kryssinger": 1.0}, TypeError),
    ],
)
def test_ugyldige_antall(antall, feil):
    with pytest.raises(feil):
        resultat(**antall)


def test_til_json_har_feltene_i_rekkefolge_uten_flyttall():
    r = resultat(antall_kryssinger=3, antall_treff=1, antall_varsler=9, antall_varsler_med_brudd=7, utelatt_kryssinger=1, utelatt_varsler=2)
    tekst = r.til_json()
    assert tekst == (
        "{\n"
        '  "versjon": 1,\n'
        '  "parametere": {"vindu": 5, "minste_tellinger": 3, "horisont": 6, "maks_uker_rod": 3},\n'
        '  "siste_uke": {"ar": 2026, "uke": 42},\n'
        '  "antall_kryssinger": 3,\n'
        '  "antall_treff": 1,\n'
        '  "antall_varsler": 9,\n'
        '  "antall_varsler_med_brudd": 7,\n'
        '  "utelatt_kryssinger": 1,\n'
        '  "utelatt_varsler": 2,\n'
        '  "treffandel": 0.3333,\n'
        '  "presisjon": 0.7778\n'
        "}\n"
    )
    data = json.loads(tekst, parse_float=Decimal)
    assert list(data) == [f.name for f in dataclasses.fields(r)]
    assert data["treffandel"] == r.treffandel and data["presisjon"] == r.presisjon
    assert data["siste_uke"] == {"ar": 2026, "uke": 42}
    assert data["parametere"] == dict(r.parametere)
    assert resultat(antall_kryssinger=3, antall_treff=1, antall_varsler=9, antall_varsler_med_brudd=7, utelatt_kryssinger=1, utelatt_varsler=2).til_json() == tekst


def test_til_json_skriver_hele_og_null_med_4_desimaler():
    data = json.loads(resultat(antall_treff=0).til_json(), parse_float=Decimal)
    assert (str(data["treffandel"]), str(data["presisjon"])) == ("0.0000", "1.0000")


def test_sammendrag():
    r = resultat(antall_kryssinger=3, antall_treff=1, antall_varsler=9, antall_varsler_med_brudd=7, utelatt_kryssinger=1, utelatt_varsler=2)
    assert r.sammendrag("backtest.json") == (
        "Skrev backtest.json for uke 1, 2025 til uke 42, 2026.\n"
        "Kryssinger: 3 (1 før uke 9, 2025 er holdt utenfor). Treff: 1. Treffandel: 33,3 %.\n"
        "Varsler: 9 (2 etter uke 38, 2026 er holdt utenfor). Fulgt av brudd: 7. Presisjon: 77,8 %.\n"
        "Parametere: vindu 5 uker, minst 3 tellinger, horisont 6 uker, rød ved 0–3 uker."
    )


@pytest.mark.parametrize(
    ("teller", "nevner", "prosent"),
    [(1, 16, "6,3"), (1, 3, "33,3"), (2, 3, "66,7"), (17, 60, "28,3"), (0, 7, "0,0"), (7, 7, "100,0")],
)
def test_prosent_i_sammendraget_regnes_fra_antallene(teller, nevner, prosent):
    # 1/16 er 6,25 % eksakt og rundes opp, selv om andelen 0,0625 allerede er avrundet.
    r = resultat(antall_kryssinger=nevner, antall_treff=teller, antall_varsler=nevner, antall_varsler_med_brudd=teller)
    linjer = r.sammendrag("x.json").splitlines()
    assert linjer[1].endswith(f"Treffandel: {prosent} %.")
    assert linjer[2].endswith(f"Presisjon: {prosent} %.")


# Backtesten bruker vurder med hele serien (AD-1)


def test_backtest_kaller_vurder_med_hele_serien_for_hver_uke(monkeypatch):
    kall = []

    def opptak(serie, omrade, analyseuke):
        kall.append((serie, omrade, analyseuke))
        return vurder(serie, omrade, analyseuke)

    monkeypatch.setattr(treffsikkerhet, "vurder", opptak)
    serie = lag_serie(KRYSSING_UKA_FOR + T6)
    backtest([(serie, SOR)])
    assert all(s is serie and o is SOR for s, o, _ in kall)
    assert [a for _, _, a in kall] == alle_uker(FORSTE_UKE, SISTE_UKE)


def test_analyseukene_er_94():
    assert FORSTE_UKE == u(1, 2025)
    assert len(alle_uker(FORSTE_UKE, SISTE_UKE)) == 94


def test_feil_type_gir_typeerror():
    serie = lag_serie(KRYSSING_UKA_FOR)
    with pytest.raises(TypeError):
        kryssinger(KRYSSING_UKA_FOR, SOR)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        kryssinger(serie, None)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        kryssinger(serie, "vest")
    with pytest.raises(TypeError):
        fulgt_av_brudd(serie, SOR, (2026, 30))  # type: ignore[arg-type]
