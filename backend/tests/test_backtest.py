"""Tester for skriptet backtest (FR27–FR29, AD-10), med det lille datasettet.

Testene skriver bare til en midlertidig mappe. Ingen av dem kjører backtesten på de ekte
dataene eller skriver backend/src/marin/data/backtest.json. Den committede fila testes i
test_backtest_fil.py.
"""

import io
import json
from decimal import Decimal
from pathlib import Path

from marin.backtest import kjor, resultatfil

LITEN = Path(__file__).parent / "data" / "backtest_liten.json"


def kjor_i(tmp_path):
    ut = io.StringIO()
    utfil = tmp_path / "pakke" / "data" / "backtest.json"
    kode = kjor(LITEN, utfil, ut=ut)
    return kode, utfil, ut.getvalue()


def test_backtest_skriver_fila_med_feltene_og_verdiene(tmp_path):
    kode, utfil, _ = kjor_i(tmp_path)
    assert kode == 0
    data = json.loads(utfil.read_text(encoding="utf-8"), parse_float=Decimal)
    assert list(data.items()) == [
        ("versjon", 1),
        ("parametere", {"vindu": 5, "minste_tellinger": 3, "horisont": 6, "maks_uker_rod": 3}),
        ("siste_uke", {"ar": 2026, "uke": 42}),
        ("antall_kryssinger", 3),
        ("antall_treff", 1),
        ("antall_varsler", 9),
        ("antall_varsler_med_brudd", 7),
        ("utelatt_kryssinger", 1),
        ("utelatt_varsler", 1),
        ("treffandel", Decimal("0.3333")),
        ("presisjon", Decimal("0.7778")),
    ]


def test_backtest_skriver_sammendraget(tmp_path):
    _, _, ut = kjor_i(tmp_path)
    assert ut == (
        "Skrev backtest.json for uke 1, 2025 til uke 42, 2026.\n"
        "Kryssinger: 3 (1 før uke 9, 2025 er holdt utenfor). Treff: 1. Treffandel: 33,3 %.\n"
        "Varsler: 9 (1 etter uke 38, 2026 er holdt utenfor). Fulgt av brudd: 7. Presisjon: 77,8 %.\n"
        "Parametere: vindu 5 uker, minst 3 tellinger, horisont 6 uker, rød ved 0–3 uker.\n"
    )


def test_ny_kjoring_gir_samme_fil_byte_for_byte(tmp_path):
    _, utfil, _ = kjor_i(tmp_path)
    forste = utfil.read_bytes()
    kjor_i(tmp_path)
    assert utfil.read_bytes() == forste
    assert b"\r\n" not in forste
    assert forste.decode("utf-8").endswith("}\n")


def test_stien_regnes_fra_pakken():
    assert resultatfil().parts[-4:] == ("src", "marin", "data", "backtest.json")
