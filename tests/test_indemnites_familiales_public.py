"""Indemnités familiales du secteur public : les cas de l'annexe 2 que le tableau ne tranche pas.

Circulaire du Premier ministre n° 42 du 25 octobre 1996, annexe 2 (JORT n° 94 du
22 novembre 1996, p. 2353-2362). Les soixante-dix-huit autres cas sont dans
`tests/formulas/prestations/contributives/indemnites_familiales_secteur_public.yaml`.
"""

import pytest
from openfisca_core.simulation_builder import SimulationBuilder

from openfisca_tunisia import TunisiaTaxBenefitSystem
from openfisca_tunisia.variables.prestations.contributives.indemnites_familiales_secteur_public import (
    CAS_ANNEXE_2,
)

tax_benefit_system = TunisiaTaxBenefitSystem()

PERIODE = "2000-01"

# Cas du tableau que le code ne tranche pas : situation d'entrée, raison.
CAS_AMBIGUS = {
    34: (
        dict(
            pf_public_situation_parents="pere_decede",
            pf_public_statut_pere="agent_public",
            pf_public_statut_mere="agent_public_reversion_et_indemnites_familiales",
            pf_public_filiation="communs",
        ),
        "II-A : l'indemnité familiale est « servie par la caisse de retraite » sans que le "
        "bénéficiaire soit nommé",
    ),
    42: (
        dict(
            pf_public_situation_parents="mere_decedee",
            pf_public_statut_pere="agent_public",
            pf_public_filiation="communs",
        ),
        "III-A : même description que le cas 43 (III-B), mère « décédée » sans autre précision, "
        "et pour résultat une indemnité pour salaire unique servie au père au lieu de non servie",
    ),
    43: (
        dict(
            pf_public_situation_parents="mere_decedee",
            pf_public_statut_pere="agent_public",
            pf_public_filiation="communs",
        ),
        "III-B : même description que le cas 42 (III-A), mais indemnité pour salaire unique non "
        "servie",
    ),
}


def resultat(variable, **entrees):
    entrees = {nom: {PERIODE: valeur} for nom, valeur in entrees.items()}
    simulation = SimulationBuilder().build_from_dict(
        tax_benefit_system,
        {"individus": {"enfant": entrees}, "menage": {"enfants": ["enfant"]}},
    )
    return simulation.calculate(variable, PERIODE).decode_to_str()[0]


def test_la_table_porte_les_81_cas_sauf_les_trois_ambigus():
    codes = {ligne[0] for ligne in CAS_ANNEXE_2}
    assert codes | set(CAS_AMBIGUS) == set(range(1, 82))
    assert not codes & set(CAS_AMBIGUS)
    assert len(codes) == len(CAS_ANNEXE_2)


@pytest.mark.parametrize("code", sorted(CAS_AMBIGUS))
def test_cas_ambigu_hors_annexe(code):
    """Faute de lecture sûre du tableau, le modèle ne tranche pas."""
    entrees, _raison = CAS_AMBIGUS[code]
    assert resultat("indemnite_familiale_public_beneficiaire", **entrees) == "hors_annexe"
    assert resultat("indemnite_salaire_unique_public_beneficiaire", **entrees) == "hors_annexe"


@pytest.mark.skip(reason=CAS_AMBIGUS[34][1])
def test_cas_34_beneficiaire_non_nomme():
    pass


@pytest.mark.skip(reason=CAS_AMBIGUS[42][1])
def test_cas_42_salaire_unique_servi_au_pere():
    pass


@pytest.mark.skip(reason=CAS_AMBIGUS[43][1])
def test_cas_43_salaire_unique_non_servi():
    pass
