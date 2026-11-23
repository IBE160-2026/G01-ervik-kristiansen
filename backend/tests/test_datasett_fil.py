"""Kontrakttester for den committede datasett.json (AD-10, AD-12, FR1).

Hashtesten feiler hvis xlsx-filene i data/barentswatch/ er endret, lagt til eller
fjernet uten at `uv run python -m marin.forbered` er kjørt på nytt. Testen av en ny
kjøring feiler hvis leseren eller formatet er endret uten at fila er laget på nytt. Den
leser hele utdraget og tar omtrent 15 sekunder.
"""

import hashlib
import io

import pytest

from marin.forbered import datasettfil, kildefiler, kildemappe, kjor
from marin.kilder.datasett import last
from marin.kjerne.konstanter import SISTE_UKE
from marin.kjerne.modeller import Uke


@pytest.fixture(scope="module")
def datasett():
    return last()


def test_hashene_stemmer_med_xlsx_filene(datasett):
    filer = kildefiler(kildemappe())
    assert filer, "fant ingen xlsx-filer i data/barentswatch/"
    assert datasett.kilder == {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in filer}


def test_datasett_json_er_lik_en_ny_kjoring_av_forbered(tmp_path):
    utfil = tmp_path / "datasett.json"
    feilut = io.StringIO()
    assert kjor(kildemappe(), utfil, ut=io.StringIO(), feilut=feilut) == 0, feilut.getvalue()
    # read_text gjør CRLF om til LF, så testen tåler core.autocrlf på Windows.
    ny = utfil.read_text(encoding="utf-8")
    assert ny == datasettfil().read_text(encoding="utf-8"), "kjør uv run python -m marin.forbered"


def test_datasettet_gaar_fra_2025_uke_1_til_og_med_siste_uke(datasett):
    uker = [t.uke for _, serie in datasett.anlegg for t in serie.tellinger]
    assert datasett.siste_uke == SISTE_UKE
    assert min(uker) == Uke(2025, 1)
    assert max(uker) == SISTE_UKE


def test_datasettet_har_alle_anleggene_sortert(datasett):
    numre = [info.lokalitetsnr for info, _ in datasett.anlegg]
    assert len(numre) == 1092
    assert numre == sorted(set(numre))


def test_anlegg_som_ble_tatt_ut_av_registeret_beholder_navn_og_fylke(datasett):
    # Den siste raden til disse fire mangler navn, kommune og fylke (avgjort 2026-11-23).
    info = {i.lokalitetsnr: i for i, _ in datasett.anlegg}
    assert (info[12260].navn, info[12260].fylke) == ("Juvika", "Møre og Romsdal")
    assert (info[12371].navn, info[12371].fylke) == ("Kalvøya", "Trøndelag")
    assert (info[10560].navn, info[10560].fylke) == ("Kårvik", "Troms")
    assert (info[13550].navn, info[13550].fylke) == ("Marøy Nø", "Vestland")
