"""Kjører backtesten: `uv run python -m marin.backtest` i backend/."""

import sys

from marin.backtest import kjor, resultatfil
from marin.forbered import datasettfil

sys.exit(kjor(datasettfil(), resultatfil()))
