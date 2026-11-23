"""Feil i en fil som leses inn (konvensjonen for opplastingsfeil i arkitekturen).

`rad` er radnummeret slik det står i regnearket, der overskriften er rad 1. `None`
betyr at feilen gjelder hele fila. `melding` er hele linja som vises til brukeren, med
«Rad N: » foran når raden er kjent.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Feil:
    """Én feil i en fil, med radnummer og ferdig melding."""

    rad: int | None
    melding: str

    @classmethod
    def i_rad(cls, rad: int, tekst: str) -> "Feil":
        """Feil i én rad. Meldingen får «Rad N: » foran teksten."""
        return cls(rad, f"Rad {rad}: {tekst}")
