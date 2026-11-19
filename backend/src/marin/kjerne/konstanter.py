"""Faste verdier i kjernen.

Regelparameterne fra R2 og R4 (vindu, minste antall tellinger, horisont og grensen for
rød status) samles også her når de lages i Story 1.4 og 1.5, slik at backtesten kan
skrive dem ut som de er.
"""

from typing import Final

from marin.kjerne.modeller import Uke

SISTE_UKE: Final = Uke(2026, 42)
"""Siste uke i det innebygde datagrunnlaget, og «nå» for innebygde data (AD-5).

Kjernen leser aldri klokka. Gjelder ikke opplastede data.
"""
