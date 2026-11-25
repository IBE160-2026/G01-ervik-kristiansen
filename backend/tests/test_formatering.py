"""Tester for formateringen i marin.kjerne.formatering mot de felles vektorene (AD-6)."""

import json
from decimal import Decimal
from pathlib import Path

import pytest

from marin.kjerne.formatering import format_grense, format_lus, format_uke, format_uke_i_tekst
from marin.kjerne.modeller import Uke

# Flyttall i JSON leses som Decimal, så vektorene aldri går via binære flyttall.
VEKTORER = json.loads(
    (Path(__file__).parent / "data" / "format.json").read_text(encoding="utf-8"),
    parse_float=Decimal,
)


@pytest.mark.parametrize("vektor", VEKTORER["lus"], ids=lambda v: v["tekst"])
def test_format_lus(vektor):
    assert format_lus(vektor["verdi"]) == vektor["tekst"]


@pytest.mark.parametrize("vektor", VEKTORER["grense"], ids=lambda v: v["tekst"])
def test_format_grense(vektor):
    assert format_grense(vektor["verdi"]) == vektor["tekst"]


@pytest.mark.parametrize("vektor", VEKTORER["uke"], ids=lambda v: v["tekst"])
def test_format_uke(vektor):
    assert format_uke(Uke(vektor["ar"], vektor["uke"])) == vektor["tekst"]


def test_vektorene_dekker_eksemplene_i_story_1_1():
    lus = {v["tekst"] for v in VEKTORER["lus"]}
    grense = {v["tekst"] for v in VEKTORER["grense"]}
    uker = {v["tekst"] for v in VEKTORER["uke"]}
    assert {"0,06", "0,50"} <= lus
    assert {"0,5", "0,2"} <= grense
    assert "uke 42, 2026" in uker


def test_lusetall_rundes_halvdel_opp_ved_formatering():
    assert format_lus(Decimal("0.125")) == "0,13"


@pytest.mark.parametrize("funksjon", [format_lus, format_grense])
def test_formatering_tar_ikke_flyttall(funksjon):
    with pytest.raises(TypeError):
        funksjon(0.5)


# Uker i statustekstene (bare i backend, så ingen vektorer i format.json)


@pytest.mark.parametrize(
    ("uke", "analyseuke", "tekst"),
    [
        (Uke(2026, 44), Uke(2026, 40), "uke 44"),
        (Uke(2026, 40), Uke(2026, 42), "uke 40"),
        (Uke(2026, 53), Uke(2026, 52), "uke 53"),
        (Uke(2027, 1), Uke(2026, 52), "uke 1, 2027"),
        (Uke(2025, 50), Uke(2026, 1), "uke 50, 2025"),
    ],
    ids=["senere i samme år", "tidligere i samme år", "uke 53 i samme år", "neste år", "året før"],
)
def test_format_uke_i_tekst_har_ar_bare_i_et_annet_ar(uke, analyseuke, tekst):
    assert format_uke_i_tekst(uke, analyseuke) == tekst


@pytest.mark.parametrize(
    ("uke", "analyseuke"),
    [((2026, 44), Uke(2026, 40)), (Uke(2026, 44), "2026-40")],
    ids=["uke som tuppel", "analyseuke som tekst"],
)
def test_format_uke_i_tekst_tar_bare_uker(uke, analyseuke):
    with pytest.raises(TypeError):
        format_uke_i_tekst(uke, analyseuke)
