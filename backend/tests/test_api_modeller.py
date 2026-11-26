"""Tester for Pydantic-modellene i marin.api.modeller (AD-3, AD-6, AD-7)."""

import json
from dataclasses import fields
from decimal import Decimal

import pytest
from pydantic import ValidationError

from marin.api.modeller import (
    AnleggInfo,
    Anleggsvar,
    Detaljsvar,
    EstimertUke,
    Graf,
    Grafpunkt,
    Kryssing,
    Status,
    Tabellrad,
    Uke,
)
from marin.kjerne import modeller as kjerne
from marin.kjerne import status as kjernestatus
from marin.kjerne.status import Arsak, Farge

U42 = Uke(ar=2026, uke=42)
U44 = Uke(ar=2026, uke=44)
KARVIK = AnleggInfo(lokalitetsnr=10560, navn="Kårvik", kommune="TROMSØ", fylke="Troms")


def status(**felt):
    verdier = {
        "farge": "rod",
        "arsak": "varsel",
        "symbol": "✕",
        "tekst": "Varsel: grensen nås om 2 uker",
        "uke_tekst": "(uke 44)",
        "forklaring": "",
    }
    return Status(**(verdier | felt))


def detaljsvar(**felt):
    verdier = {
        "kilde": "innebygd",
        "anlegg": KARVIK,
        "analyseuke": U42,
        "status": status(),
        "estimert_uke": EstimertUke(uke=U44, uker_til=2),
        "tabell": [Tabellrad(uke=Uke(ar=2026, uke=u), verdi=None, siste_telling=False) for u in range(38, 43)],
        "graf": Graf(
            punkter=[Grafpunkt(uke=U42, malt=Decimal("0.36"), trend=Decimal("0.38"), grense=Decimal("0.50"))],
            kryssing=Kryssing(uke=U44, tekst="✕ Varsel uke 44"),
        ),
        "tekstoppsummering": "",
        "usikkerhetstekst": "",
    }
    return Detaljsvar(**(verdier | felt))


# Lusetall (AD-6)


def test_lusetall_er_tall_i_json_og_decimal_i_python():
    rad = Tabellrad(uke=U42, verdi=Decimal("0.28"), siste_telling=True)
    tekst = rad.model_dump_json()
    assert '"verdi":0.28' in tekst
    assert json.loads(tekst, parse_float=Decimal)["verdi"] == Decimal("0.28")
    # Serialiseringen gjelder bare JSON. I Python er verdien fortsatt den samme Decimal.
    assert rad.verdi == Decimal("0.28")
    assert rad.model_dump()["verdi"] == Decimal("0.28")


@pytest.mark.parametrize(
    ("verdi", "i_json"),
    [("0.28", "0.28"), ("0.5", "0.5"), ("0.50", "0.5"), ("0.10", "0.1"), ("12.34", "12.34"), ("0", "0.0")],
)
def test_lusetall_gir_samme_tall_i_json_som_verdien(verdi, i_json):
    punkt = Grafpunkt(uke=U42, malt=Decimal(verdi), trend=Decimal(verdi), grense=Decimal(verdi))
    tekst = punkt.model_dump_json()
    assert tekst == f'{{"uke":{{"ar":2026,"uke":42}},"malt":{i_json},"trend":{i_json},"grense":{i_json}}}'
    data = json.loads(tekst, parse_float=Decimal)
    assert (data["malt"], data["trend"], data["grense"]) == (Decimal(verdi),) * 3


@pytest.mark.parametrize(("modell", "feltene"), [(Tabellrad, ["verdi"]), (Grafpunkt, ["malt", "trend", "grense"])])
def test_lusetall_er_number_i_skjemaet(modell, feltene):
    egenskaper = modell.model_json_schema(mode="serialization")["properties"]
    for felt in feltene:
        assert egenskaper[felt]["anyOf"] == [{"type": "number"}, {"type": "null"}]


def test_ikke_telt_er_null():
    tekst = Tabellrad(uke=U42, verdi=None, siste_telling=False).model_dump_json()
    assert '"verdi":null' in tekst
    assert json.loads(tekst)["verdi"] is None
    punkt = json.loads(Grafpunkt(uke=U42, malt=None, trend=None, grense=None).model_dump_json())
    assert (punkt["malt"], punkt["trend"], punkt["grense"]) == (None, None, None)


# Fra kjernen (AD-3, AD-11)


@pytest.mark.parametrize(
    ("modell", "kjernetype"),
    [(Uke, kjerne.Uke), (AnleggInfo, kjerne.AnleggInfo), (EstimertUke, kjernestatus.EstimertUke)],
)
def test_feltnavnene_er_like_kjernens(modell, kjernetype):
    assert list(modell.model_fields) == [f.name for f in fields(kjernetype)]


def test_modellene_lages_direkte_fra_kjernens_typer():
    assert Uke.model_validate(kjerne.Uke(2026, 42)) == Uke(ar=2026, uke=42)
    info = kjerne.AnleggInfo(10560, "Kårvik", "TROMSØ", "Troms")
    assert AnleggInfo.model_validate(info) == KARVIK
    estimert = kjernestatus.EstimertUke(kjerne.Uke(2026, 46), 4)
    assert EstimertUke.model_validate(estimert) == EstimertUke(uke=Uke(ar=2026, uke=46), uker_til=4)


def test_anleggsinfo_uten_felt_gir_null_i_alle_feltene():
    tekst = AnleggInfo.model_validate(kjerne.AnleggInfo()).model_dump_json()
    assert json.loads(tekst) == {"lokalitetsnr": None, "navn": None, "kommune": None, "fylke": None}


# Statuskoder (AD-7)


def test_status_bruker_kjernens_koder():
    s = status(farge="gul", arsak="folg_med")
    assert (s.farge, s.arsak) == (Farge.GUL, Arsak.FOLG_MED)
    data = json.loads(s.model_dump_json())
    assert (data["farge"], data["arsak"]) == ("gul", "folg_med")


def test_skjemaet_har_akkurat_kjernens_koder():
    defs = Status.model_json_schema()["$defs"]
    assert defs["Farge"]["enum"] == [f.value for f in Farge]
    assert defs["Arsak"]["enum"] == [a.value for a in Arsak]


@pytest.mark.parametrize("felt", [{"farge": "lilla"}, {"arsak": "annet"}, {"farge": "Rod"}, {"farge": "rød"}])
def test_ukjent_kode_gir_valideringsfeil(felt):
    with pytest.raises(ValidationError) as feil:
        status(**felt)
    assert [e["loc"] for e in feil.value.errors()] == [tuple(felt)]


# Hele svarene


def test_detaljsvar_har_minsteformen_i_ad_3():
    data = json.loads(detaljsvar().model_dump_json())
    assert list(data) == [
        "kilde",
        "anlegg",
        "analyseuke",
        "status",
        "estimert_uke",
        "tabell",
        "graf",
        "tekstoppsummering",
        "usikkerhetstekst",
    ]
    assert data["anlegg"] == {"lokalitetsnr": 10560, "navn": "Kårvik", "kommune": "TROMSØ", "fylke": "Troms"}
    assert data["analyseuke"] == {"ar": 2026, "uke": 42}
    assert list(data["status"]) == ["farge", "arsak", "symbol", "tekst", "uke_tekst", "forklaring"]
    assert data["estimert_uke"] == {"uke": {"ar": 2026, "uke": 44}, "uker_til": 2}
    assert data["tabell"][0] == {"uke": {"ar": 2026, "uke": 38}, "verdi": None, "siste_telling": False}
    assert data["graf"]["punkter"] == [{"uke": {"ar": 2026, "uke": 42}, "malt": 0.36, "trend": 0.38, "grense": 0.5}]
    assert data["graf"]["kryssing"] == {"uke": {"ar": 2026, "uke": 44}, "tekst": "✕ Varsel uke 44"}


def test_detaljsvar_uten_estimert_uke_og_kryssing_gir_null():
    svar = detaljsvar(estimert_uke=None, graf=Graf(punkter=[], kryssing=None))
    data = json.loads(svar.model_dump_json())
    assert data["estimert_uke"] is None
    assert data["graf"] == {"punkter": [], "kryssing": None}


def test_kilde_er_innebygd_eller_opplastet():
    assert Detaljsvar.model_json_schema()["properties"]["kilde"]["enum"] == ["innebygd", "opplastet"]
    assert detaljsvar(kilde="opplastet").kilde == "opplastet"
    with pytest.raises(ValidationError):
        detaljsvar(kilde="annet")


def test_anleggsvar_har_anlegget_under_anlegg():
    svar = Anleggsvar(anlegg=KARVIK, analyseuker=[U42, Uke(ar=2026, uke=41)], standard_analyseuke=U42)
    assert json.loads(svar.model_dump_json()) == {
        "anlegg": {"lokalitetsnr": 10560, "navn": "Kårvik", "kommune": "TROMSØ", "fylke": "Troms"},
        "analyseuker": [{"ar": 2026, "uke": 42}, {"ar": 2026, "uke": 41}],
        "standard_analyseuke": {"ar": 2026, "uke": 42},
    }
