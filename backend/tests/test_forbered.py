"""Tester for skriptet forbered (FR1, AD-10), mot en midlertidig mappe."""

import hashlib
import io
from decimal import Decimal

from hjelp_xlsx import lag_xlsx, rad

from marin.forbered import MAKS_FEIL, datasettfil, kildefiler, kildemappe, kjor
from marin.kilder.datasett import Datasett
from marin.kjerne.modeller import AnleggInfo, Uke


def skriv_filer(mappe, **filer):
    mappe.mkdir(exist_ok=True)
    for navn, rader in filer.items():
        (mappe / f"{navn}.xlsx").write_bytes(lag_xlsx(rader))


def kjor_i(tmp_path):
    ut, feilut = io.StringIO(), io.StringIO()
    utfil = tmp_path / "pakke" / "data" / "datasett.json"
    kode = kjor(tmp_path / "kilder", utfil, ut=ut, feilut=feilut)
    return kode, utfil, ut.getvalue(), feilut.getvalue()


def test_forbered_skriver_datasett_med_hasher_og_kutter_etter_siste_uke(tmp_path):
    skriv_filer(
        tmp_path / "kilder",
        aar_2025=[rad(nr=5, ar=2025, uke=52, lus=0.2, navn="Gammelt", fylke="Troms")],
        aar_2026=[
            rad(nr=5, ar=2026, uke=42, lus=None, navn="Nytt", fylke="Troms"),
            rad(nr=5, ar=2026, uke=43, lus=0.9, navn="Etter kuttet", fylke="Vestland"),
            rad(nr=6, ar=2026, uke=1, lus=0.1, fylke="Vestland"),
        ],
    )
    kode, utfil, ut, feilut = kjor_i(tmp_path)
    assert (kode, feilut) == (0, "")
    assert ut == "Skrev datasett.json: 2 anlegg, 2 uker med telling og 1 uker uten telling, til og med uke 42, 2026.\n"

    datasett = Datasett.fra_json(utfil.read_text(encoding="utf-8"))
    assert datasett.siste_uke == Uke(2026, 42)
    assert datasett.kilder == {
        f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in (tmp_path / "kilder").glob("*.xlsx")
    }
    (info5, serie5), (info6, _) = datasett.anlegg
    assert info5 == AnleggInfo(5, "Nytt", None, "Troms")
    assert [(t.uke, t.verdi) for t in serie5.tellinger] == [(Uke(2025, 52), Decimal("0.20")), (Uke(2026, 42), None)]
    assert info6 == AnleggInfo(6, None, None, "Vestland")


def test_info_fra_eldre_fil_brukes_naar_nyeste_fil_mangler_feltet(tmp_path):
    skriv_filer(
        tmp_path / "kilder",
        a=[rad(nr=1, ar=2025, uke=1, navn="Juvika", kommune="MOLDE", fylke="Møre og Romsdal")],
        b=[rad(nr=1, ar=2026, uke=1, kommune="HUSTADVIKA")],
    )
    kode, utfil, _, _ = kjor_i(tmp_path)
    assert kode == 0
    (info, _), = Datasett.fra_json(utfil.read_text(encoding="utf-8")).anlegg
    assert info == AnleggInfo(1, "Juvika", "HUSTADVIKA", "Møre og Romsdal")


def test_info_fra_nyeste_fil_selv_naar_filnavnene_ikke_er_i_tidsrekkefolge(tmp_path):
    skriv_filer(
        tmp_path / "kilder",
        a=[rad(nr=1, ar=2026, uke=1, navn="Nytt", fylke="Nordland")],
        b=[rad(nr=1, ar=2025, uke=1, navn="Gammelt", fylke="Trøndelag")],
    )
    kode, utfil, _, _ = kjor_i(tmp_path)
    assert kode == 0
    (info, _), = Datasett.fra_json(utfil.read_text(encoding="utf-8")).anlegg
    assert info == AnleggInfo(1, "Nytt", None, "Nordland")


def test_laasefiler_fra_excel_hoppes_over(tmp_path):
    skriv_filer(tmp_path / "kilder", a=[rad(nr=1, uke=1, lus=0.1)])
    (tmp_path / "kilder" / "~$a.xlsx").write_bytes(b"laasefil")
    assert [f.name for f in kildefiler(tmp_path / "kilder")] == ["a.xlsx"]
    kode, _, _, feilut = kjor_i(tmp_path)
    assert (kode, feilut) == (0, "")


def test_ny_kjoring_gir_samme_fil_byte_for_byte(tmp_path):
    skriv_filer(tmp_path / "kilder", a=[rad(nr=1, uke=1, lus=0.1, navn="Kårvik"), rad(nr=2, uke=1)])
    _, utfil, _, _ = kjor_i(tmp_path)
    forste = utfil.read_bytes()
    kjor_i(tmp_path)
    assert utfil.read_bytes() == forste
    assert b"\r\n" not in forste


def test_feil_i_fila_gir_kode_1_og_ingen_fil(tmp_path):
    skriv_filer(tmp_path / "kilder", a=[rad(uke=34, lus=0.1), rad(uke=34, lus=0.2)])
    kode, utfil, ut, feilut = kjor_i(tmp_path)
    assert kode == 1
    assert not utfil.exists()
    assert ut == ""
    assert feilut == (
        "a.xlsx: Rad 3: uke 34, 2026 finnes allerede i rad 2.\n"
        "1 feil. datasett.json er ikke skrevet.\n"
    )


def test_bare_de_forste_feilene_skrives_men_antallet_er_med(tmp_path):
    skriv_filer(tmp_path / "kilder", a=[rad(uke=u, lus="x") for u in range(1, 31)])
    kode, _, _, feilut = kjor_i(tmp_path)
    linjer = feilut.splitlines()
    assert kode == 1
    assert len(linjer) == MAKS_FEIL + 1
    assert linjer[-1] == "30 feil. datasett.json er ikke skrevet."


def test_samme_uke_i_to_filer_gir_feil(tmp_path):
    skriv_filer(tmp_path / "kilder", a=[rad(nr=7, uke=5, lus=0.1)], b=[rad(nr=7, uke=5, lus=0.2)])
    kode, utfil, _, feilut = kjor_i(tmp_path)
    assert kode == 1
    assert not utfil.exists()
    assert feilut.splitlines()[0] == (
        "Lokalitet 7 har samme uke i flere filer: uke 5, 2026 finnes mer enn én gang i serien."
    )


def test_ingen_xlsx_filer_gir_kode_1(tmp_path):
    (tmp_path / "kilder").mkdir()
    kode, utfil, _, feilut = kjor_i(tmp_path)
    assert kode == 1
    assert not utfil.exists()
    assert feilut.startswith("Fant ingen xlsx-filer i ")


def test_stiene_regnes_fra_pakken():
    assert kildemappe().parts[-2:] == ("data", "barentswatch")
    assert kildemappe().is_dir()
    assert datasettfil().parts[-4:] == ("src", "marin", "data", "datasett.json")
