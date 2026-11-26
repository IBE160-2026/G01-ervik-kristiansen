"""FastAPI-appen med rutene i kjerneflyten (AD-3, AD-9, AD-10).

Startes med `uv run uvicorn marin.api.app:app` i backend/ (port 8000), med `--reload` i
utvikling. Rutene svarer HTTP 501 til de bygges: søket i Story 2.4 og anlegget og
prognosen i Story 2.5. Svarmodellene står likevel i skjemaet, slik at frontend kan bygges
mot kontrakten.

Ved oppstart leses datasett.json én gang og holdes i minnet. Rutene får det gjennom
avhengigheten `hent_datasett`, så 2.4 og 2.5 kan bruke det uavhengig av hverandre.

Finnes frontend-bygget (`frontend/out/` etter `npm run build`), serverer appen det på `/`
etter alle `/api`-rutene, så Marin kan kjøres lokalt som én prosess (NFR1). På Vercel er
roten til backend `backend/`, så mappa finnes ikke der, og Vercel sender bare `/api/…` hit.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Final

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from marin.api.modeller import AnleggInfo, Anleggsvar, Detaljsvar
from marin.kilder.datasett import Datasett, last

UTVIKLINGSOPPHAV: Final = "http://localhost:3000"
"""Next.js i utvikling (`npm run dev`). Det eneste opphavet CORS tillater (AD-9)."""


def _frontend_bygg() -> Path | None:
    """`frontend/out/` i repoet, regnet ut fra plasseringen til denne fila.

    Fila ligger i backend/src/marin/api/, så rotmappa i repoet er fire nivåer opp. Er
    pakken installert et annet sted, peker stien på en mappe som ikke finnes, og da
    monteres ingenting.
    """
    foreldre = Path(__file__).resolve().parents
    return foreldre[4] / "frontend" / "out" if len(foreldre) > 4 else None


FRONTEND_BYGG: Final = _frontend_bygg()
"""Det statiske bygget fra `npm run build` i frontend/. Monteres bare når mappa finnes."""


@asynccontextmanager
async def levetid(app: FastAPI) -> AsyncIterator[None]:
    """Leser datasett.json én gang ved oppstart og holder det i minnet (AD-10)."""
    app.state.datasett = last()
    yield


def hent_datasett(request: Request) -> Datasett:
    """Avhengigheten som gir rutene datasettet som ble lest ved oppstart."""
    return request.app.state.datasett


DatasettAvhengighet = Annotated[Datasett, Depends(hent_datasett)]

ruter = APIRouter()
"""API-rutene. `lag_app` tar dem med før frontend-bygget, så de alltid kommer først."""


def _ikke_bygget(detail: str) -> HTTPException:
    # 501 Not Implemented til ruten bygges. Meldingen nevner storyen som bygger den.
    return HTTPException(status_code=501, detail=detail)


@ruter.get("/api/anlegg", summary="Søk etter anlegg")
def sok_anlegg(q: str, datasett: DatasettAvhengighet) -> list[AnleggInfo]:
    """Anleggene som passer søket, sortert alfabetisk på navn (FR4–FR6)."""
    raise _ikke_bygget("Søket er ikke bygget ennå. Det kommer i Story 2.4.")


@ruter.get("/api/anlegg/{lokalitetsnr}", summary="Hent anlegget")
def hent_anlegg(lokalitetsnr: int, datasett: DatasettAvhengighet) -> Anleggsvar:
    """Anlegget med de valgbare analyseukene og standarduka (FR6b, FR7)."""
    raise _ikke_bygget("Ruten for anlegget er ikke bygget ennå. Den kommer i Story 2.5.")


@ruter.get("/api/anlegg/{lokalitetsnr}/prognose", summary="Hent prognosen")
def hent_prognose(lokalitetsnr: int, ar: int, uke: int, datasett: DatasettAvhengighet) -> Detaljsvar:
    """Prognosen for anlegget med analyseuka `ar` og `uke` (FR7–FR20a)."""
    raise _ikke_bygget("Prognosen er ikke bygget ennå. Den kommer i Story 2.5.")


def _ukjent_api_sti(sti: str) -> None:
    """Gir FastAPIs JSON 404 for en ukjent sti under /api/, ikke 404.html fra bygget."""
    raise HTTPException(status_code=404)


def lag_app(frontend_bygg: Path | None = FRONTEND_BYGG) -> FastAPI:
    """Lager appen. Testene kan gi en midlertidig mappe i stedet for det ekte bygget.

    Finnes `frontend_bygg`, monteres den på `/` etter alle `/api`-rutene. `html=True` gir
    `index.html` for mapper, omdirigerer `/anlegg` til `/anlegg/` med spørringen og gir
    `404.html` med status 404 for filer som ikke finnes. Uten mappa starter appen som før.
    """
    # operationId i skjemaet er navnet på rutefunksjonen, ikke et navn FastAPI lager fra stien.
    app = FastAPI(title="Marin", lifespan=levetid, generate_unique_id_function=lambda rute: rute.name)

    # Lokalt og på Vercel kommer frontenden fra samme opphav, så regelen brukes bare i
    # utvikling. Uten miljøvariabler kan appen ikke vite hvor den kjører, så den er alltid
    # på. Bare GET finnes ennå. Opplastingsrutene (Epic 3) trenger også POST.
    app.add_middleware(CORSMiddleware, allow_origins=[UTVIKLINGSOPPHAV], allow_methods=["GET"])

    app.include_router(ruter)

    if frontend_bygg is not None and frontend_bygg.is_dir():
        # Monteringen på `/` ville også tatt ukjente stier under /api/. Den skjulte ruten
        # kommer etter API-rutene og før monteringen. Den gjelder bare GET og HEAD, så andre
        # metoder på en kjent rute, som POST /api/anlegg, fortsatt gir 405. HEAD på en kjent
        # GET-rute, som HEAD /api/anlegg, gir derimot 404 når bygget er montert.
        app.add_api_route("/api/{sti:path}", _ukjent_api_sti, methods=["GET", "HEAD"], include_in_schema=False)
        app.mount("/", StaticFiles(directory=frontend_bygg, html=True), name="frontend")

    return app


app = lag_app()
