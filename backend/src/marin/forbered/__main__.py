"""Kjører forbered: `uv run python -m marin.forbered` i backend/."""

import sys

from marin.forbered import datasettfil, kildemappe, kjor

sys.exit(kjor(kildemappe(), datasettfil()))
