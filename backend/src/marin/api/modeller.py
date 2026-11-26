"""Pydantic-modellene for svarene fra API-et (AD-3, AD-6, AD-7).

Modellene er fasiten for kontrakten med frontend. backend/openapi.json lages fra dem, og
frontend-typene genereres fra den fila. Modellene speiler kjernens typer: `Uke`,
`AnleggInfo` og `EstimertUke` har de samme feltene som i kjernen og kan lages direkte fra
et kjerneobjekt med `model_validate`. `farge` og `arsak` har kjernens typer `Farge` og
`Arsak`, så kodene finnes bare ett sted (AD-7).

Lusetall er Decimal i Python og JSON-tall i svaret, aldri tekst (AD-6). Pydantic v2 gjør
Decimal om til tekst i JSON som standard, så `Lusetall` overstyrer det, men bare for
JSON. Lusetallene har høyst 2 desimaler, så tallet i JSON har samme tallverdi som
verdien, men nuller til slutt faller bort (0.28 blir 0.28, 0.50 blir 0.5 og 0 blir 0.0).
Frontend formaterer derfor tallet selv. `None` (`null` i JSON) betyr ikke telt eller mangler.
"""

from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, PlainSerializer

from marin.kjerne.status import Arsak, Farge

Lusetall = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]
"""Voksne hunnlus per fisk: Decimal i Python, tall i JSON og `number` i skjemaet."""

Kilde = Literal["innebygd", "opplastet"]
"""Hvor tallene kommer fra: de innebygde dataene eller en opplastet fil (Epic 3)."""


class _Modell(BaseModel):
    # from_attributes lar modellene lages fra kjernens dataclasser, også nestet
    # (EstimertUke med en Uke inni).
    model_config = ConfigDict(from_attributes=True)


class Uke(_Modell):
    """En ISO-uke (AD-6)."""

    ar: int
    uke: int


class AnleggInfo(_Modell):
    """Navn og sted for et anlegg. Alle feltene kan være null, for eksempel ved CSV-opplasting."""

    lokalitetsnr: int | None
    navn: str | None
    kommune: str | None
    fylke: str | None


class Status(_Modell):
    """Statusen etter R4 (AD-2, AD-7).

    `farge` og `arsak` er de faste kodene. `symbol` og `tekst` er R4-teksten delt i to,
    og `uke_tekst` («(uke 44)») finnes bare ved varsel og følg med. `forklaring` er den
    forklarende setningen under statusteksten.
    """

    farge: Farge
    arsak: Arsak
    symbol: str
    tekst: str
    uke_tekst: str | None
    forklaring: str


class EstimertUke(_Modell):
    """Uka der estimatet først når grensen, og antall uker dit fra analyseuka (R2)."""

    uke: Uke
    uker_til: int


class Tabellrad(_Modell):
    """En uke i ukestabellen. `verdi` er null når uka ikke er telt."""

    uke: Uke
    verdi: Lusetall | None
    siste_telling: bool


class Grafpunkt(_Modell):
    """Én uke i grafen: målt verdi, trend og grense. null betyr at verdien ikke finnes for uka."""

    uke: Uke
    malt: Lusetall | None
    trend: Lusetall | None
    grense: Lusetall | None


class Kryssing(_Modell):
    """Uka der trenden når grensen, med etiketten i grafen, for eksempel «✕ Varsel uke 44»."""

    uke: Uke
    tekst: str


class Graf(_Modell):
    """Alt grafen tegner. `kryssing` er null når trenden ikke når grensen."""

    punkter: list[Grafpunkt]
    kryssing: Kryssing | None


class Detaljsvar(_Modell):
    """Hele detaljsiden for ett anlegg og én analyseuke (AD-3).

    `estimert_uke` er null utenom varsel og følg med. `tabell` har 5 uker, eldste først.
    """

    kilde: Kilde
    anlegg: AnleggInfo
    analyseuke: Uke
    status: Status
    estimert_uke: EstimertUke | None
    tabell: list[Tabellrad]
    graf: Graf
    tekstoppsummering: str
    usikkerhetstekst: str


class Anleggsvar(_Modell):
    """Et anlegg med de valgbare analyseukene, nyeste først, og standarduka (AD-14)."""

    anlegg: AnleggInfo
    analyseuker: list[Uke]
    standard_analyseuke: Uke
