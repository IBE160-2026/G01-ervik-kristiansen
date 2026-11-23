"""Tester for leseren av BarentsWatch-uttrekket (FR1–FR3, AD-11, AD-12).

Hver rad i I/O-matrisen i spec-1-3 har minst én test her. Filene lages i minnet med
hjelp_xlsx, så radnumrene i testene er radnumrene i regnearket (overskriften er rad 1).
"""

import io
import re
import zipfile
from decimal import Decimal

import pytest
from hjelp_xlsx import KOLONNER, lag_xlsx, rad

from marin.kilder.barentswatch import FEIL_FORMAT, les
from marin.kilder.feil import Feil
from marin.kjerne.modeller import AnleggInfo, Telling, Uke


def verdier(serie) -> list[tuple[int, int, Decimal | None]]:
    return [(t.uke.ar, t.uke.uke, t.verdi) for t in serie.tellinger]


def endre_ark(innhold: bytes, endring) -> bytes:
    """Ny xlsx der XML-en for arket er endret med `endring` (bytes inn, bytes ut)."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(innhold)) as inn, zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as ut:
        for info in inn.infolist():
            data = inn.read(info.filename)
            ut.writestr(info, endring(data) if info.filename == "xl/worksheets/sheet1.xml" else data)
    return buffer.getvalue()


def les_ett_bytes(innhold, **kwargs):
    """Leser en fil som skal gi ett anlegg og ingen feil."""
    anlegg, feil = les(innhold, **kwargs)
    assert feil == []
    assert len(anlegg) == 1
    return anlegg[0]


def les_ett(rader, **kwargs):
    return les_ett_bytes(lag_xlsx(rader), **kwargs)


# Gyldig fil


def test_gyldig_fil_gir_anlegg_sortert_paa_nummer_og_tom_verdi_som_none():
    rader = [
        rad(nr=20, uke=1, lus=0.5, navn="B", kommune="HITRA", fylke="Trøndelag"),
        rad(nr=10, uke=1, lus=0.12, navn="A", kommune="LOPPA", fylke="Finnmark"),
        rad(nr=20, uke=2, lus=None, navn="B", kommune="HITRA", fylke="Trøndelag"),
        rad(nr=10, uke=2, lus=0, navn="A", kommune="LOPPA", fylke="Finnmark"),
        rad(nr=20, uke=3, lus=1.25, navn="B", kommune="HITRA", fylke="Trøndelag"),
        rad(nr=10, uke=3, lus=None, navn="A", kommune="LOPPA", fylke="Finnmark"),
    ]
    anlegg, feil = les(lag_xlsx(rader))
    assert feil == []
    assert [info for info, _ in anlegg] == [
        AnleggInfo(10, "A", "LOPPA", "Finnmark"),
        AnleggInfo(20, "B", "HITRA", "Trøndelag"),
    ]
    assert verdier(anlegg[0][1]) == [
        (2026, 1, Decimal("0.12")),
        (2026, 2, Decimal("0.00")),
        (2026, 3, None),
    ]
    assert verdier(anlegg[1][1]) == [
        (2026, 1, Decimal("0.50")),
        (2026, 2, None),
        (2026, 3, Decimal("1.25")),
    ]


def test_lusetall_gaar_via_tekst_saa_0_145_blir_0_15():
    # Flyttallet 0.145 ligger like under 0,145. Via tekst avrundes det riktig til 0,15.
    _, serie = les_ett([rad(lus=0.145)])
    assert serie.tellinger == (Telling(Uke(2026, 1), Decimal("0.15")),)


def test_lokalitetsnummer_er_int():
    info, _ = les_ett([rad(nr=12260.0, ar=2026.0, uke=3.0, lus=0.1)])
    assert info.lokalitetsnr == 12260
    assert type(info.lokalitetsnr) is int


def test_tom_rad_hoppes_over_og_radnumrene_stemmer():
    rader = [rad(uke=1, lus=0.1), None, rad(**{"Uke": None, "År": None, "Lokalitetsnummer": None}), rad(uke=1, lus=0.2)]
    anlegg, feil = les(lag_xlsx(rader))
    # Rad 3 og 4 er tomme, så duplikatet står i rad 5.
    assert feil == [Feil(5, "Rad 5: uke 1, 2026 finnes allerede i rad 2.")]
    assert verdier(anlegg[0][1]) == [(2026, 1, Decimal("0.10"))]


def test_tekst_med_bare_mellomrom_er_tom():
    info, serie = les_ett([rad(lus="  ", navn=" ", kommune="", fylke=" ")])
    assert info == AnleggInfo(1, None, None, None)
    assert verdier(serie) == [(2026, 1, None)]


def test_kolonnene_finnes_etter_navn_og_andre_kolonner_ignoreres():
    kolonner = ("Lusegrense uke", "Fylke", "Voksne hunnlus", " Uke ", "Lokalitetsnummer", "År", "Sjøtemperatur")
    rader = [rad(uke=5, lus=0.3, fylke="Nordland", **{" Uke ": 5, "Lusegrense uke": "0.2"})]
    anlegg, feil = les(lag_xlsx(rader, kolonner=kolonner))
    assert feil == []
    assert anlegg[0][0] == AnleggInfo(1, None, None, "Nordland")
    assert verdier(anlegg[0][1]) == [(2026, 5, Decimal("0.30"))]


def test_navn_kommune_og_fylke_kan_mangle_som_kolonner():
    kolonner = ("Uke", "År", "Lokalitetsnummer", "Voksne hunnlus")
    anlegg, feil = les(lag_xlsx([rad(lus=0.1)], kolonner=kolonner))
    assert feil == []
    assert anlegg[0][0] == AnleggInfo(1, None, None, None)


# Kutt (FR1)


def test_kutt_tar_bare_med_uker_til_og_med():
    rader = [rad(uke=42, lus=0.1), rad(uke=43, lus=0.2), rad(ar=2027, uke=1, lus=0.3)]
    _, serie = les_ett(rader, til_og_med=Uke(2026, 42))
    assert verdier(serie) == [(2026, 42, Decimal("0.10"))]


def test_uten_kutt_er_alle_ukene_med():
    _, serie = les_ett([rad(uke=42, lus=0.1), rad(uke=43, lus=0.2)])
    assert [t.uke for t in serie.tellinger] == [Uke(2026, 42), Uke(2026, 43)]


def test_kutt_gjelder_ogsaa_navn_og_fylke():
    rader = [rad(uke=42, lus=0.1, navn="Før", fylke="Vestland"), rad(uke=43, lus=0.2, navn="Etter", fylke="Troms")]
    info, _ = les_ett(rader, til_og_med=Uke(2026, 42))
    assert info == AnleggInfo(1, "Før", None, "Vestland")


def test_rader_etter_kuttet_kontrolleres_ikke():
    # Ugyldig lusetall, duplikat og ugyldig nummer etter kuttet gir ingen feil.
    rader = [rad(uke=42, lus=0.1), rad(uke=43, lus="abc"), rad(uke=43, lus=0.2), rad(nr="x", uke=44)]
    _, serie = les_ett(rader, til_og_med=Uke(2026, 42))
    assert verdier(serie) == [(2026, 42, Decimal("0.10"))]


def test_anlegg_med_bare_rader_etter_kuttet_er_ikke_med():
    anlegg, feil = les(lag_xlsx([rad(nr=1, uke=42, lus=0.1), rad(nr=2, uke=43, lus=0.1)]), til_og_med=Uke(2026, 42))
    assert feil == []
    assert [info.lokalitetsnr for info, _ in anlegg] == [1]


# Navn, kommune og fylke (AD-11, avgjort 2026-11-23)


def test_ulikt_fylke_gir_fylket_fra_nyeste_rad_selv_naar_radene_staar_baklengs():
    info, _ = les_ett([rad(uke=2, fylke="Nordland"), rad(uke=1, fylke="Trøndelag")])
    assert info.fylke == "Nordland"


def test_nyeste_rad_uten_info_gir_info_fra_nyeste_rad_med_verdi():
    felles = {"navn": "Juvika", "kommune": "MOLDE", "fylke": "Møre og Romsdal"}
    rader = [rad(nr=12260, uke=1, **felles), rad(nr=12260, uke=2, **felles), rad(nr=12260, uke=3)]
    info, serie = les_ett(rader)
    assert info == AnleggInfo(12260, "Juvika", "MOLDE", "Møre og Romsdal")
    assert [t.uke.uke for t in serie.tellinger] == [1, 2, 3]


def test_ulikt_navn_gir_navnet_fra_nyeste_rad():
    info, _ = les_ett([rad(uke=1, navn="Sloppegrunn"), rad(uke=2, navn="Geitelva")])
    assert info.navn == "Geitelva"


def test_feltene_hentes_hver_for_seg():
    info, _ = les_ett([rad(uke=1, navn="Gammel", kommune="SØMNA"), rad(uke=2, kommune="BRØNNØY")])
    assert info == AnleggInfo(1, "Gammel", "BRØNNØY", None)


def test_anlegg_uten_info_i_noen_rad():
    info, _ = les_ett([rad(nr=3877, ar=2025, uke=52, lus=0.05)])
    assert info == AnleggInfo(3877, None, None, None)


def test_info_fra_rad_med_feil_brukes_ikke():
    anlegg, feil = les(lag_xlsx([rad(uke=1, navn="God"), rad(uke=2, lus="abc", navn="Feil")]))
    assert len(feil) == 1
    assert anlegg[0][0].navn == "God"


# Duplikater (AD-12)


def test_duplikat_gir_feil_og_beholder_forste_rad():
    rader = [rad(nr=n, uke=1) for n in range(100, 104)]  # rad 2–5
    rader += [rad(nr=7, uke=34, lus=0.1)]  # rad 6
    rader += [rad(nr=n, uke=2) for n in range(100, 102)]  # rad 7–8
    rader += [rad(nr=7, uke=34, lus=0.9)]  # rad 9
    anlegg, feil = les(lag_xlsx(rader))
    assert feil == [Feil(9, "Rad 9: uke 34, 2026 finnes allerede i rad 6.")]
    sju = dict(anlegg)[AnleggInfo(7)]
    assert verdier(sju) == [(2026, 34, Decimal("0.10"))]


def test_duplikat_av_en_rad_med_feil_meldes_ogsaa():
    # Fila har uke 3 to ganger, så brukeren får vite begge deler med én gang.
    anlegg, feil = les(lag_xlsx([rad(uke=3, lus="abc"), rad(uke=3, lus=0.2)]))
    assert anlegg == []
    assert feil == [
        Feil(2, "Rad 2: lusetallet «abc» er ikke et tall."),
        Feil(3, "Rad 3: uke 3, 2026 finnes allerede i rad 2."),
    ]


def test_samme_uke_for_ulike_anlegg_er_ikke_duplikat():
    anlegg, feil = les(lag_xlsx([rad(nr=1, uke=34), rad(nr=2, uke=34)]))
    assert feil == []
    assert len(anlegg) == 2


def test_samme_uke_i_ulike_aar_er_ikke_duplikat():
    _, serie = les_ett([rad(ar=2025, uke=34), rad(ar=2026, uke=34)])
    assert [t.uke for t in serie.tellinger] == [Uke(2025, 34), Uke(2026, 34)]


# Ugyldige uker


@pytest.mark.parametrize(
    ("ar", "uke", "melding"),
    [
        (2026, 54, "Rad 2: uke 54 finnes ikke. Uke må være 1–53."),
        (2026, 0, "Rad 2: uke 0 finnes ikke. Uke må være 1–53."),
        (2025, 53, "Rad 2: 2025 har ikke uke 53."),
        (0, 1, "Rad 2: året 0 finnes ikke i kalenderen."),
    ],
)
def test_ugyldig_uke_gir_feil(ar, uke, melding):
    anlegg, feil = les(lag_xlsx([rad(ar=ar, uke=uke, lus=0.1)]))
    assert anlegg == []
    assert feil == [Feil(2, melding)]


def test_uke_53_i_aar_med_uke_53_er_gyldig():
    _, serie = les_ett([rad(ar=2026, uke=53, lus=0.1)])
    assert serie.tellinger[0].uke == Uke(2026, 53)


# Ugyldige lusetall


@pytest.mark.parametrize(
    ("lus", "melding"),
    [
        ("abc", "Rad 2: lusetallet «abc» er ikke et tall."),
        ("0,5", "Rad 2: lusetallet «0,5» er ikke et tall."),
        (True, "Rad 2: lusetallet «True» er ikke et tall."),
        (-0.2, "Rad 2: lusetallet «-0,2» er negativt."),
        (-1, "Rad 2: lusetallet «-1» er negativt."),
        (1e30, "Rad 2: lusetallet «1e+30» er for stort."),
    ],
)
def test_ugyldig_lusetall_gir_feil(lus, melding):
    anlegg, feil = les(lag_xlsx([rad(lus=lus)]))
    assert anlegg == []
    assert feil == [Feil(2, melding)]


# Heltall i Lokalitetsnummer, År og Uke


@pytest.mark.parametrize(
    ("kolonne", "verdi", "melding"),
    [
        ("År", None, "Rad 2: «År» mangler."),
        ("Uke", "x", "Rad 2: «Uke» må være et heltall, ikke «x»."),
        ("Lokalitetsnummer", 12.5, "Rad 2: «Lokalitetsnummer» må være et heltall, ikke «12,5»."),
        ("Lokalitetsnummer", "  ", "Rad 2: «Lokalitetsnummer» mangler."),
        ("Uke", True, "Rad 2: «Uke» må være et heltall, ikke «True»."),
    ],
)
def test_ikke_heltall_gir_feil(kolonne, verdi, melding):
    anlegg, feil = les(lag_xlsx([rad(lus=0.1, **{kolonne: verdi})]))
    assert anlegg == []
    assert feil == [Feil(2, melding)]


def test_alle_feil_i_en_rad_meldes():
    anlegg, feil = les(lag_xlsx([rad(nr="x", uke=54, lus=-1)]))
    assert anlegg == []
    assert feil == [
        Feil(2, "Rad 2: «Lokalitetsnummer» må være et heltall, ikke «x»."),
        Feil(2, "Rad 2: uke 54 finnes ikke. Uke må være 1–53."),
        Feil(2, "Rad 2: lusetallet «-1» er negativt."),
    ]


def test_gyldige_rader_kommer_med_selv_om_andre_rader_har_feil():
    anlegg, feil = les(lag_xlsx([rad(uke=1, lus=0.1), rad(uke=2, lus="abc"), rad(uke=3, lus=0.3)]))
    assert feil == [Feil(3, "Rad 3: lusetallet «abc» er ikke et tall.")]
    assert [t.uke.uke for t in anlegg[0][1].tellinger] == [1, 3]


# Feil i hele fila


@pytest.mark.parametrize("kolonne", ["Voksne hunnlus", "Lokalitetsnummer", "År", "Uke"])
def test_manglende_kolonne_gir_feil_uten_rad(kolonne):
    kolonner = [k for k in KOLONNER if k != kolonne]
    anlegg, feil = les(lag_xlsx([rad(lus=0.1)], kolonner=kolonner))
    assert anlegg == []
    assert feil == [Feil(None, f"Fila mangler kolonnen «{kolonne}».")]


def test_tomt_ark_gir_feil_for_alle_paakrevde_kolonner():
    anlegg, feil = les(lag_xlsx([], kolonner=[]))
    assert anlegg == []
    assert [f.melding for f in feil] == [
        "Fila mangler kolonnen «Lokalitetsnummer».",
        "Fila mangler kolonnen «År».",
        "Fila mangler kolonnen «Uke».",
        "Fila mangler kolonnen «Voksne hunnlus».",
    ]


@pytest.mark.parametrize("innhold", [b"", b"ikke en xlsx-fil", b"PK\x03\x04 odelagt zip"])
def test_fil_som_ikke_er_xlsx_gir_formatfeil(innhold):
    assert les(innhold) == ([], [Feil(None, FEIL_FORMAT)])


def test_odelagt_xml_i_arket_gir_formatfeil():
    rader = [rad(uke=u, lus=0.1, navn="Et langt navn som fyller XML-en") for u in range(1, 30)]
    innhold = endre_ark(lag_xlsx(rader), lambda xml: xml[: len(xml) // 2])
    assert les(innhold) == ([], [Feil(None, FEIL_FORMAT)])


def test_feil_dimension_i_fila_mister_ingen_rader_eller_kolonner():
    # Andre verktøy kan skrive en <dimension> som ikke stemmer. Leseren skal ikke stole på den.
    innhold = endre_ark(
        lag_xlsx([rad(uke=u, lus=0.1, fylke="Troms") for u in range(1, 6)]),
        lambda xml: re.sub(rb'<dimension ref="[^"]*"\s*/>', b'<dimension ref="A1:A1"/>', xml),
    )
    _, serie = les_ett_bytes(innhold)
    assert [t.uke.uke for t in serie.tellinger] == [1, 2, 3, 4, 5]


def test_feil_arknavn_gir_formatfeil():
    assert les(lag_xlsx([rad(lus=0.1)], ark="Ark1")) == ([], [Feil(None, FEIL_FORMAT)])


def test_formatfeilen_har_ordlyden_fra_specen():
    assert FEIL_FORMAT == "Fila er ikke et Excel-uttrekk fra BarentsWatch med arket «Lakselus per fisk»."


# Typer


@pytest.mark.parametrize("innhold", ["tekst", bytearray(b"x"), None])
def test_innhold_maa_vaere_bytes(innhold):
    with pytest.raises(TypeError):
        les(innhold)


def test_til_og_med_maa_vaere_uke():
    with pytest.raises(TypeError):
        les(lag_xlsx([]), til_og_med=(2026, 42))
