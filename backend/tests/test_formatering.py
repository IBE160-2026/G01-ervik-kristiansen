"""Tester for formateringen i marin.kjerne.formatering mot de felles vektorene (AD-6)."""

import json
from decimal import Decimal
from pathlib import Path

import pytest

from marin.kjerne.formatering import format_grense, format_lus, format_uke
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
