"""Tester for FastAPI-appen i marin.api.app og den committede openapi.json (AD-3, AD-9, AD-10).

Appen startes én gang for hele modulen med TestClient, som kjører oppstarten. Testen av
openapi.json feiler når en modell eller rute er endret uten at
`uv run python -m marin.api.openapi` er kjørt på nytt.
"""

import io
import json

import pytest
from fastapi import Request
from fastapi.testclient import TestClient

import marin.api.app as appmodul
from marin.api.app import app, hent_datasett
from marin.api.openapi import kjor, openapifil
from marin.kilder.datasett import last

TILLATT = "http://localhost:3000"
SOK = "/api/anlegg?q=hitra"
ANLEGG = "/api/anlegg/10560"
PROGNOSE = "/api/anlegg/10560/prognose?ar=2026&uke=42"


@pytest.fixture(scope="module")
def oppstart():
    """Starter appen én gang og teller hvor mange ganger datasett.json leses."""
    lesinger = []

    def tellende_last():
        lesinger.append(last())
        return lesinger[-1]

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(appmodul, "last", tellende_last)
        with TestClient(app) as klient:
            yield klient, lesinger


@pytest.fixture
def klient(oppstart):
    return oppstart[0]


# Rutene


@pytest.mark.parametrize(("sti", "story"), [(SOK, "Story 2.4"), (ANLEGG, "Story 2.5"), (PROGNOSE, "Story 2.5")])
def test_rutene_svarer_501_til_de_bygges(klient, sti, story):
    svar = klient.get(sti)
    assert svar.status_code == 501
    assert list(svar.json()) == ["detail"]
    assert story in svar.json()["detail"]
    assert "ikke bygget ennå" in svar.json()["detail"]


@pytest.mark.parametrize(
    "sti",
    [
        "/api/anlegg/abc",
        "/api/anlegg/10560.5",
        "/api/anlegg/abc/prognose?ar=2026&uke=42",
        "/api/anlegg/10560/prognose?uke=42",
        "/api/anlegg/10560/prognose?ar=2026",
        "/api/anlegg/10560/prognose?ar=2026&uke=uke42",
    ],
)
def test_ugyldig_parameter_gir_422(klient, sti):
    assert klient.get(sti).status_code == 422


# CORS (AD-9)


def forhandsforesporsel(klient, opphav):
    return klient.options(PROGNOSE, headers={"Origin": opphav, "Access-Control-Request-Method": "GET"})


def test_cors_tillater_localhost_3000(klient):
    for sti in (SOK, ANLEGG, PROGNOSE):
        assert klient.get(sti, headers={"Origin": TILLATT}).headers["access-control-allow-origin"] == TILLATT
    svar = forhandsforesporsel(klient, TILLATT)
    assert svar.status_code == 200
    assert svar.headers["access-control-allow-origin"] == TILLATT


@pytest.mark.parametrize(
    "opphav", ["http://127.0.0.1:3000", "http://localhost:3001", "https://localhost:3000", "http://localhost"]
)
def test_cors_tillater_ikke_andre_opphav(klient, opphav):
    assert "access-control-allow-origin" not in klient.get(ANLEGG, headers={"Origin": opphav}).headers
    assert "access-control-allow-origin" not in forhandsforesporsel(klient, opphav).headers


# Skjemaet (AD-3)


def test_openapi_json_er_lik_skjemaet_appen_lager(tmp_path):
    utfil = tmp_path / "openapi.json"
    assert kjor(utfil, ut=io.StringIO()) == 0
    # Kommandoen skriver LF. CRLF gjøres om til LF i den committede fila, så testen tåler
    # core.autocrlf på Windows.
    committet = openapifil().read_bytes().replace(b"\r\n", b"\n")
    assert utfil.read_bytes() == committet, "openapi.json er utdatert: kjør uv run python -m marin.api.openapi i backend/"


def test_kommandoen_skriver_samme_utf8_med_lf_og_innrykk_2_hver_gang(tmp_path):
    forste, andre = tmp_path / "forste.json", tmp_path / "andre.json"
    kjor(forste, ut=io.StringIO())
    kjor(andre, ut=io.StringIO())
    data = forste.read_bytes()
    assert data == andre.read_bytes()
    assert b"\r" not in data
    tekst = data.decode("utf-8")
    assert tekst == json.dumps(json.loads(tekst), ensure_ascii=False, indent=2) + "\n"
    assert "\\u00" not in tekst, "æ, ø og å skal stå som tegn"


def test_openapi_json_ligger_i_backend():
    assert openapifil().name == "openapi.json"
    assert (openapifil().parent / "pyproject.toml").is_file()


def test_skjemaet_har_de_tre_rutene_med_parametere_og_svarmodell():
    stier = app.openapi()["paths"]
    assert set(stier) == {"/api/anlegg", "/api/anlegg/{lokalitetsnr}", "/api/anlegg/{lokalitetsnr}/prognose"}

    def parametere(sti):
        return {p["name"]: (p["in"], p["required"], p["schema"]["type"]) for p in stier[sti]["get"]["parameters"]}

    def svarmodell(sti):
        return stier[sti]["get"]["responses"]["200"]["content"]["application/json"]["schema"]

    assert parametere("/api/anlegg") == {"q": ("query", True, "string")}
    assert parametere("/api/anlegg/{lokalitetsnr}") == {"lokalitetsnr": ("path", True, "integer")}
    assert parametere("/api/anlegg/{lokalitetsnr}/prognose") == {
        "lokalitetsnr": ("path", True, "integer"),
        "ar": ("query", True, "integer"),
        "uke": ("query", True, "integer"),
    }
    sok = svarmodell("/api/anlegg")
    assert (sok["type"], sok["items"]) == ("array", {"$ref": "#/components/schemas/AnleggInfo"})
    assert svarmodell("/api/anlegg/{lokalitetsnr}") == {"$ref": "#/components/schemas/Anleggsvar"}
    assert svarmodell("/api/anlegg/{lokalitetsnr}/prognose") == {"$ref": "#/components/schemas/Detaljsvar"}


def test_lusetall_er_number_i_skjemaet_til_appen():
    skjemaer = app.openapi()["components"]["schemas"]
    for modell, felt in [("Tabellrad", "verdi"), ("Grafpunkt", "malt"), ("Grafpunkt", "trend"), ("Grafpunkt", "grense")]:
        assert skjemaer[modell]["properties"][felt]["anyOf"] == [{"type": "number"}, {"type": "null"}]


def test_alle_feltene_er_paakrevd_ogsaa_de_som_kan_vaere_null():
    # Et felt med standardverdi (= None) ville blitt valgfritt i frontend-typene.
    skjemaer = app.openapi()["components"]["schemas"]
    utenom = {"HTTPValidationError", "ValidationError", "Farge", "Arsak"}
    for navn, skjema in skjemaer.items():
        if navn not in utenom:
            assert set(skjema["required"]) == set(skjema["properties"]), navn


def test_docs_og_skjemaet_vises_av_appen(klient):
    assert klient.get("/docs").status_code == 200
    assert klient.get("/openapi.json").json() == app.openapi()


# Oppstart (AD-10)


def test_datasettet_leses_en_gang_ved_oppstart(oppstart):
    klient, lesinger = oppstart
    for _ in range(3):
        for sti in (SOK, ANLEGG, PROGNOSE):
            klient.get(sti)
    assert len(lesinger) == 1
    assert len(lesinger[0].anlegg) == 1092
    assert app.state.datasett is lesinger[0]


def test_rutene_far_datasettet_fra_avhengigheten(oppstart):
    klient, lesinger = oppstart
    gitt = []

    def registrer(request: Request):
        gitt.append(hent_datasett(request))
        return gitt[-1]

    app.dependency_overrides[hent_datasett] = registrer
    try:
        for sti in (SOK, ANLEGG, PROGNOSE):
            klient.get(sti)
    finally:
        app.dependency_overrides.pop(hent_datasett)
    assert len(gitt) == 3
    assert all(datasett is lesinger[0] for datasett in gitt)
