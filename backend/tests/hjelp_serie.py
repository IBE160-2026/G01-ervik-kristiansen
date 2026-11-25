"""Hjelp til testene: serier av lusetall og tellingene i fasiten T5, T6, T8 og T12.

Tellingene er hentet fra den kontrollerte håndregningen i
_bmad-output/planning-artifacts/briefs/brief-Marin-2026-09-17/a4-handkontroll.md. Både
test_trend.py og test_status.py bruker dem, så fasiten står ett sted.
"""

from decimal import Decimal

from marin.kjerne.modeller import Serie, Telling, Uke
from marin.kjerne.uker import pluss


def lag_serie(par: list[tuple[Uke, str | None]]) -> Serie:
    """En serie av (uke, verdi), der verdien er tekst eller None for en uke uten telling."""
    return Serie(Telling(uke, None if verdi is None else Decimal(verdi)) for uke, verdi in par)


def fortlopende(start: Uke, *verdier: str | None) -> list[tuple[Uke, str | None]]:
    """Verdiene i påfølgende uker fra og med `start`."""
    return [(pluss(start, i), verdi) for i, verdi in enumerate(verdier)]


T5 = fortlopende(Uke(2026, 30), "0.06", "0.12", "0.18", "0.24", "0.30")
T6 = fortlopende(Uke(2026, 10), "0.10", "0.12", "0.14", "0.16", "0.18")
T8 = [(Uke(2026, 36), "0.20"), (Uke(2026, 38), "0.28"), (Uke(2026, 40), "0.36")]
T12 = fortlopende(Uke(2025, 50), "0.30", "0.34", "0.38", "0.42", "0.46")
