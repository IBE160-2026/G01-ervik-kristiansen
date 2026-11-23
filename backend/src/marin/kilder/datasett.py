"""Formatet til datasett.json, den forhåndsbehandlede datafila i pakken (AD-10).

`forbered` skriver fila, og backtesten (Story 1.6) og API-et (Epic 2) leser den med
`last()`. Formatet står bare her. Fila har ett anlegg per linje, så endringer gir
lesbare differ:

    {"siste_uke": {"ar": 2026, "uke": 42}, "kilder": {"fil.xlsx": "sha256"}, "anlegg": [
    {"lokalitetsnr": 10560, "navn": "Kårvik", ..., "tellinger": [[2025,1,null],[2025,2,0.12]]},
    ...
    ]}

Lusetall skrives som JSON-tall med 2 desimaler direkte fra Decimal, uten flyttall, og
leses tilbake som Decimal. En uke uten telling er null.
"""

import json
from dataclasses import dataclass
from decimal import Decimal
from importlib.resources import files

from marin.kjerne.modeller import AnleggInfo, Serie, Telling, Uke


@dataclass(frozen=True, slots=True)
class Datasett:
    """De innebygde dataene: anleggene, siste uke som er med, og sha256 per kildefil."""

    siste_uke: Uke
    kilder: dict[str, str]
    anlegg: tuple[tuple[AnleggInfo, Serie], ...]

    def til_json(self) -> str:
        """Teksten i datasett.json. Samme datasett gir alltid samme tekst."""
        hode = {
            "siste_uke": {"ar": self.siste_uke.ar, "uke": self.siste_uke.uke},
            "kilder": dict(sorted(self.kilder.items())),
        }
        linjer = [_anlegg_til_json(info, serie) for info, serie in self.anlegg]
        return json.dumps(hode, ensure_ascii=False)[:-1] + ', "anlegg": [\n' + ",\n".join(linjer) + "\n]}\n"

    @classmethod
    def fra_json(cls, tekst: str) -> "Datasett":
        """Leser teksten fra datasett.json."""
        data = json.loads(tekst, parse_float=Decimal)
        anlegg = tuple(
            (
                AnleggInfo(a["lokalitetsnr"], a["navn"], a["kommune"], a["fylke"]),
                Serie(Telling(Uke(ar, uke), verdi) for ar, uke, verdi in a["tellinger"]),
            )
            for a in data["anlegg"]
        )
        siste = data["siste_uke"]
        return cls(Uke(siste["ar"], siste["uke"]), dict(data["kilder"]), anlegg)


def last() -> Datasett:
    """Leser datasett.json fra pakken (backend/src/marin/data/), aldri fra arbeidsmappa."""
    return Datasett.fra_json(files("marin").joinpath("data", "datasett.json").read_text(encoding="utf-8"))


def _anlegg_til_json(info: AnleggInfo, serie: Serie) -> str:
    felt = {"lokalitetsnr": info.lokalitetsnr, "navn": info.navn, "kommune": info.kommune, "fylke": info.fylke}
    tellinger = ",".join(_telling_til_json(telling) for telling in serie.tellinger)
    return json.dumps(felt, ensure_ascii=False)[:-1] + f', "tellinger": [{tellinger}]}}'


def _telling_til_json(telling: Telling) -> str:
    # Telling har alltid avrundet verdien til 2 desimaler, så f-formatet gir for eksempel 0.10.
    verdi = "null" if telling.verdi is None else f"{telling.verdi:f}"
    return f"[{telling.uke.ar},{telling.uke.uke},{verdi}]"
