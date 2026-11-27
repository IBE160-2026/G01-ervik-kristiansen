"""Tester for frontend-bygget som FastAPI serverer ved lokal kjøring (AD-9, NFR1).

Testene gir `lag_app` en midlertidig mappe med `index.html`, `anlegg/index.html` og
`404.html` i stedet for det ekte bygget, så de virker også uten `npm run build`. Hver fil
har en egen tekst, så testene ser hvilken fil som ble servert.
"""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from starlette.routing import Mount

import marin.api.app as appmodul
from marin.api.app import lag_app
from marin.api.openapi import openapifil

FORSIDE = "<!DOCTYPE html><html lang=\"nb\"><body>forsiden</body></html>"
DETALJSIDE = "<!DOCTYPE html><html lang=\"nb\"><body>detaljsiden</body></html>"
IKKE_FUNNET = "<!DOCTYPE html><html lang=\"nb\"><body>Fant ikke siden.</body></html>"
SOK = "/api/anlegg?q=x"


@pytest.fixture(scope="module")
def bygg(tmp_path_factory) -> Path:
    """En midlertidig mappe med de tre filene fra `npm run build` som testene trenger."""
    mappe = tmp_path_factory.mktemp("out")
    (mappe / "index.html").write_text(FORSIDE, encoding="utf-8")
    (mappe / "anlegg").mkdir()
    (mappe / "anlegg" / "index.html").write_text(DETALJSIDE, encoding="utf-8")
    (mappe / "404.html").write_text(IKKE_FUNNET, encoding="utf-8")
    return mappe


@pytest.fixture(scope="module")
def montert(bygg):
    """Appen med den midlertidige mappa montert på `/`."""
    with TestClient(lag_app(bygg)) as klient:
        yield klient


@pytest.fixture(scope="module")
def uten_bygg(tmp_path_factory):
    """Appen når `frontend/out/` ikke finnes."""
    with TestClient(lag_app(tmp_path_factory.mktemp("tom") / "out")) as klient:
        yield klient


def er_html(svar) -> bool:
    return svar.headers["content-type"].startswith("text/html")


def er_json(svar) -> bool:
    return svar.headers["content-type"] == "application/json"


# Matrisen: lokal kjøring med mappa montert


def test_forsiden_gir_index_html(montert):
    svar = montert.get("/")
    assert svar.status_code == 200
    assert er_html(svar)
    assert svar.text == FORSIDE


def test_detaljsiden_kan_lastes_direkte(montert):
    svar = montert.get("/anlegg/?nr=1")
    assert svar.status_code == 200
    assert er_html(svar)
    assert svar.text == DETALJSIDE


def test_detaljsiden_uten_skrastrek_omdirigeres_med_sporringen(montert):
    svar = montert.get("/anlegg?nr=1", follow_redirects=False)
    assert svar.status_code == 307
    assert svar.headers["location"].endswith("/anlegg/?nr=1")
    fulgt = montert.get("/anlegg?nr=1")
    assert (fulgt.status_code, fulgt.text) == (200, DETALJSIDE)


def test_api_rutene_kommer_foran_bygget(montert, uten_bygg):
    svar = montert.get(SOK)
    assert svar.status_code == 501
    assert er_json(svar)
    assert svar.json() == uten_bygg.get(SOK).json()
    assert "Story 2.4" in svar.json()["detail"]


@pytest.mark.parametrize("sti", ["/api/finnes-ikke", "/api/", "/api/anlegg/10560/finnes-ikke", "/api/index.html"])
def test_ukjent_api_sti_gir_json_404_og_ikke_html(montert, uten_bygg, sti):
    svar = montert.get(sti)
    assert svar.status_code == 404
    assert er_json(svar)
    assert svar.json() == {"detail": "Not Found"}
    # Samme svar som når mappa ikke er montert.
    assert svar.json() == uten_bygg.get(sti).json()


def test_ukjent_api_sti_med_head_gir_404_uten_html(montert):
    svar = montert.head("/api/finnes-ikke")
    assert svar.status_code == 404
    assert er_json(svar)


def test_ukjent_side_gir_404_html(montert):
    svar = montert.get("/finnes-ikke")
    assert svar.status_code == 404
    assert er_html(svar)
    assert svar.text == IKKE_FUNNET


def test_feil_metode_pa_kjent_api_rute_gir_fortsatt_405(montert):
    # Den skjulte ruten gjelder bare GET og HEAD. Med alle metoder ville POST gitt 404.
    svar = montert.post(SOK)
    assert svar.status_code == 405
    assert er_json(svar)


def test_docs_virker_med_bygget_montert(montert):
    assert montert.get("/docs").status_code == 200


# Matrisen: uten bygg


def test_uten_bygg_virker_api_rutene(uten_bygg):
    svar = uten_bygg.get(SOK)
    assert svar.status_code == 501
    assert "Story 2.4" in svar.json()["detail"]


def test_uten_bygg_gir_forsiden_json_404(uten_bygg):
    svar = uten_bygg.get("/")
    assert svar.status_code == 404
    assert er_json(svar)
    assert svar.json() == {"detail": "Not Found"}


def test_uten_bygg_monteres_ingenting(tmp_path):
    for app in (lag_app(tmp_path / "out"), lag_app(None)):
        assert not any(isinstance(rute, Mount) for rute in app.routes)
        assert "/api/{sti:path}" not in {getattr(rute, "path", None) for rute in app.routes}


# Skjemaet og standardmappa


def test_skjemaet_er_uendret_med_bygget_montert(bygg):
    committet = json.loads(openapifil().read_text(encoding="utf-8"))
    assert lag_app(bygg).openapi() == committet
    assert lag_app(None).openapi() == committet


def test_standardmappa_er_frontend_out_i_repoet():
    rotmappe = Path(__file__).resolve().parents[2]
    assert appmodul.FRONTEND_BYGG == rotmappe / "frontend" / "out"


def test_appen_monterer_det_ekte_bygget_bare_nar_det_finnes():
    # Appen lages i testen, så et `npm run build` mens testene kjører ikke gir feil svar.
    finnes = appmodul.FRONTEND_BYGG.is_dir()
    app = lag_app()
    montert = [rute for rute in app.routes if isinstance(rute, Mount)]
    assert len(montert) == (1 if finnes else 0)
    if montert:
        # Monteringen står sist, etter alle /api-rutene.
        assert app.routes[-1] is montert[0]


@pytest.mark.skipif(
    not (appmodul.FRONTEND_BYGG / "index.html").is_file(), reason="krever `npm run build` i frontend/"
)
def test_det_ekte_bygget_gir_forsiden_detaljsiden_og_den_norske_404_siden():
    """Serverer frontend/out/ fra `npm run build`, så feil filstruktur i bygget eller den
    engelske 404-siden til Next blir oppdaget."""
    with TestClient(lag_app()) as klient:
        for sti in ("/", "/anlegg/?nr=1"):
            svar = klient.get(sti)
            assert svar.status_code == 200, sti
            assert er_html(svar), sti
        svar = klient.get("/finnes-ikke")
        assert svar.status_code == 404
        assert "Fant ikke siden." in svar.text
        assert 'lang="nb"' in svar.text


def test_vercel_inngangen_gir_den_samme_appen():
    """Vercel laster `vercel_inngang:app` fra backend/ (vercel.json), ikke `marin.api.app:app`."""
    import importlib.util

    fil = Path(__file__).resolve().parents[1] / "vercel_inngang.py"
    spesifikasjon = importlib.util.spec_from_file_location("vercel_inngang", fil)
    modul = importlib.util.module_from_spec(spesifikasjon)
    spesifikasjon.loader.exec_module(modul)
    assert modul.app is appmodul.app


def test_vercel_json_peker_pa_inngangen():
    rotmappe = Path(__file__).resolve().parents[2]
    oppsett = json.loads((rotmappe / "vercel.json").read_text(encoding="utf-8"))
    assert oppsett["services"]["backend"]["entrypoint"] == "vercel_inngang:app"
    assert (rotmappe / "backend" / "vercel_inngang.py").is_file()
