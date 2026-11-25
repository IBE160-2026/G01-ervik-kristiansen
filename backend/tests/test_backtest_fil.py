"""Kontrakttester for den committede backtest.json (A5, FR27a, AD-10).

Tallene i fila er rapportert i README og PRD kap. 11 (Story 1.7). Testen av en ny kjøring
feiler hvis kjernen, datasettet eller formatet er endret uten at backtesten er kjørt på
nytt. Da skal `uv run python -m marin.backtest` kjøres, og de nye tallene rapporteres på
nytt, i stedet for at de gamle blir stående. Testen kjører backtesten på hele datasettet.
"""

import io
import json

from marin.backtest import kjor, resultatfil
from marin.forbered import datasettfil
from marin.kjerne.konstanter import SISTE_UKE
from marin.kjerne.treffsikkerhet import PARAMETERE


def test_backtest_json_er_lik_en_ny_kjoring_av_backtest(tmp_path):
    utfil = tmp_path / "backtest.json"
    assert kjor(datasettfil(), utfil, ut=io.StringIO()) == 0
    # Skriptet skriver LF. CRLF gjøres om til LF i den committede fila, så testen tåler
    # core.autocrlf på Windows.
    committet = resultatfil().read_bytes().replace(b"\r\n", b"\n")
    assert utfil.read_bytes() == committet, "kjør uv run python -m marin.backtest og rapporter tallene på nytt"


def test_parameterne_og_siste_uke_i_fila_er_kjernens_konstanter():
    data = json.loads(resultatfil().read_text(encoding="utf-8"))
    assert data["parametere"] == dict(PARAMETERE)
    assert data["siste_uke"] == {"ar": SISTE_UKE.ar, "uke": SISTE_UKE.uke}
