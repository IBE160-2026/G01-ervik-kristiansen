"""FastAPI-appen med rutene i kjerneflyten (AD-3, AD-9, AD-10).

Startes med `uv run uvicorn marin.api.app:app --reload` i backend/ (port 8000). Rutene
svarer HTTP 501 til de bygges: søket i Story 2.4 og anlegget og prognosen i Story 2.5.
Svarmodellene står likevel i skjemaet, slik at frontend kan bygges mot kontrakten.

Ved oppstart leses datasett.json én gang og holdes i minnet. Rutene får det gjennom
avhengigheten `hent_datasett`, så 2.4 og 2.5 kan bruke det uavhengig av hverandre.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Annotated, Final

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from marin.api.modeller import AnleggInfo, Anleggsvar, Detaljsvar
from marin.kilder.datasett import Datasett, last

UTVIKLINGSOPPHAV: Final = "http://localhost:3000"
"""Next.js i utvikling (`npm run dev`). Det eneste opphavet CORS tillater (AD-9)."""


@asynccontextmanager
async def levetid(app: FastAPI) -> AsyncIterator[None]:
    """Leser datasett.json én gang ved oppstart og holder det i minnet (AD-10)."""
    app.state.datasett = last()
    yield


def hent_datasett(request: Request) -> Datasett:
    """Avhengigheten som gir rutene datasettet som ble lest ved oppstart."""
    return request.app.state.datasett


DatasettAvhengighet = Annotated[Datasett, Depends(hent_datasett)]

# operationId i skjemaet er navnet på rutefunksjonen, ikke et navn FastAPI lager fra stien.
app = FastAPI(title="Marin", lifespan=levetid, generate_unique_id_function=lambda rute: rute.name)

# Lokalt og på Vercel kommer frontenden fra samme opphav, så regelen brukes bare i
# utvikling. Uten miljøvariabler kan appen ikke vite hvor den kjører, så den er alltid
# på. Bare GET finnes ennå. Opplastingsrutene (Epic 3) trenger også POST.
app.add_middleware(CORSMiddleware, allow_origins=[UTVIKLINGSOPPHAV], allow_methods=["GET"])


def _ikke_bygget(detail: str) -> HTTPException:
    # 501 Not Implemented til ruten bygges. Meldingen nevner storyen som bygger den.
    return HTTPException(status_code=501, detail=detail)


@app.get("/api/anlegg", summary="Søk etter anlegg")
def sok_anlegg(q: str, datasett: DatasettAvhengighet) -> list[AnleggInfo]:
    """Anleggene som passer søket, sortert alfabetisk på navn (FR4–FR6)."""
    raise _ikke_bygget("Søket er ikke bygget ennå. Det kommer i Story 2.4.")


@app.get("/api/anlegg/{lokalitetsnr}", summary="Hent anlegget")
def hent_anlegg(lokalitetsnr: int, datasett: DatasettAvhengighet) -> Anleggsvar:
    """Anlegget med de valgbare analyseukene og standarduka (FR6b, FR7)."""
    raise _ikke_bygget("Ruten for anlegget er ikke bygget ennå. Den kommer i Story 2.5.")


@app.get("/api/anlegg/{lokalitetsnr}/prognose", summary="Hent prognosen")
def hent_prognose(lokalitetsnr: int, ar: int, uke: int, datasett: DatasettAvhengighet) -> Detaljsvar:
    """Prognosen for anlegget med analyseuka `ar` og `uke` (FR7–FR20a)."""
    raise _ikke_bygget("Prognosen er ikke bygget ennå. Den kommer i Story 2.5.")
