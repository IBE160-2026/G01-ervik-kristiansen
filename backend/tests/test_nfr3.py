"""NFR3: R1 testes mot BarentsWatch-kolonnen «Lusegrense uke» som uavhengig fasit.

Testen leser xlsx-filene direkte med openpyxl, ikke gjennom leseren, så en feil i
leseren ikke kan skjule et avvik. «Lusegrense uke» brukes aldri som grense i appen,
bare her. Å lese filene tar omtrent 15 sekunder, og det skjer én gang for modulen.
"""

from decimal import Decimal

import openpyxl
import pytest

from marin.forbered import kildefiler, kildemappe
from marin.kjerne.lusegrense import grense
from marin.kjerne.modeller import Uke
from marin.kjerne.omrade import Omrade, omrade_fra_fylke


@pytest.fixture(scope="module")
def rader() -> list[tuple[str, int, int, str | None, str]]:
    """(fil, år, uke, fylke, Lusegrense uke) for hver rad i utdraget."""
    resultat = []
    for fil in kildefiler(kildemappe()):
        bok = openpyxl.load_workbook(fil, read_only=True, data_only=True)
        try:
            radene = bok["Lakselus per fisk"].iter_rows(values_only=True)
            kolonne = {navn: i for i, navn in enumerate(next(radene))}
            for r in radene:
                resultat.append(
                    (fil.name, r[kolonne["År"]], r[kolonne["Uke"]], r[kolonne["Fylke"]], r[kolonne["Lusegrense uke"]])
                )
        finally:
            bok.close()
    assert len(resultat) == 102_560
    return resultat


def test_nfr3_r1_gir_samme_grense_som_barentswatch_i_alle_rader(rader):
    avvik = []
    for fil, ar, uke, fylke, fasit in rader:
        forventet = None if fasit == "Ukjent" else Decimal(fasit)
        if grense(omrade_fra_fylke(fylke), Uke(ar, uke)) != forventet:
            avvik.append((fil, ar, uke, fylke, fasit))
    assert avvik == []


def test_nfr3_rader_med_ukjent_grense_gir_ukjent_omrade(rader):
    ukjente = [fylke for _, _, _, fylke, fasit in rader if fasit == "Ukjent"]
    assert len(ukjente) == 7
    assert {omrade_fra_fylke(fylke) for fylke in ukjente} == {Omrade.UKJENT}


def test_nfr3_alle_utfylte_fylker_gir_sor_eller_nord(rader):
    fylker = {fylke for _, _, _, fylke, _ in rader if fylke}
    assert {fylke: omrade_fra_fylke(fylke) for fylke in fylker if omrade_fra_fylke(fylke) == Omrade.UKJENT} == {}
    assert fylker  # utdraget har fylker
