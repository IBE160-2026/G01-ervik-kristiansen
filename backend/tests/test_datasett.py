"""Tester for formatet til datasett.json (AD-10)."""

import json
from decimal import Decimal

from marin.kilder.datasett import Datasett
from marin.kjerne.modeller import AnleggInfo, Serie, Telling, Uke


def lag_datasett() -> Datasett:
    return Datasett(
        siste_uke=Uke(2026, 42),
        kilder={"b.xlsx": "bbb", "a.xlsx": "aaa"},
        anlegg=(
            (
                AnleggInfo(10560, "Kårvik", "TROMSØ", "Troms"),
                Serie([
                    Telling(Uke(2025, 52), Decimal("0.1")),
                    Telling(Uke(2026, 1), None),
                    Telling(Uke(2026, 2), Decimal("0")),
                    Telling(Uke(2026, 3), Decimal("8.3")),
                ]),
            ),
            (AnleggInfo(3877), Serie([Telling(Uke(2025, 52), Decimal("0.05"))])),
        ),
    )


def test_json_fram_og_tilbake_gir_samme_datasett():
    datasett = lag_datasett()
    assert Datasett.fra_json(datasett.til_json()) == datasett


def test_teksten_er_gyldig_json_med_ett_anlegg_per_linje():
    tekst = lag_datasett().til_json()
    data = json.loads(tekst)
    assert data["siste_uke"] == {"ar": 2026, "uke": 42}
    linjer = tekst.splitlines()
    assert len(linjer) == 4  # hode, to anlegg og slutten
    assert linjer[1].startswith('{"lokalitetsnr": 10560, "navn": "Kårvik"')
    assert linjer[2].startswith('{"lokalitetsnr": 3877, "navn": null')
    assert tekst.endswith("\n]}\n")


def test_lusetall_skrives_med_to_desimaler_og_uten_flyttall():
    tekst = lag_datasett().til_json()
    assert '"tellinger": [[2025,52,0.10],[2026,1,null],[2026,2,0.00],[2026,3,8.30]]' in tekst


def test_lusetall_leses_som_decimal():
    _, serie = Datasett.fra_json(lag_datasett().til_json()).anlegg[0]
    assert [t.verdi for t in serie.tellinger] == [Decimal("0.10"), None, Decimal("0.00"), Decimal("8.30")]
    assert all(isinstance(t.verdi, Decimal) for t in serie.tellinger if t.verdi is not None)


def test_aeoeaa_skrives_uten_escape():
    tekst = lag_datasett().til_json()
    assert "Kårvik" in tekst and "TROMSØ" in tekst
    assert "\\u" not in tekst


def test_kildene_sorteres_paa_filnavn():
    data = json.loads(lag_datasett().til_json())
    assert list(data["kilder"]) == ["a.xlsx", "b.xlsx"]


def test_samme_datasett_gir_samme_tekst():
    assert lag_datasett().til_json() == lag_datasett().til_json()


def test_tomt_datasett_er_gyldig_json():
    tomt = Datasett(Uke(2026, 42), {}, ())
    assert Datasett.fra_json(tomt.til_json()) == tomt
