"""Indemnités familiales du secteur public : couverture de l'annexe 2.

Circulaire du Premier ministre n° 42 du 25 octobre 1996, annexe 2 (JORT n° 89 du
5 novembre 1996, p. 2537-2550 de l'édition arabe ; JORT n° 94 du 22 novembre 1996,
p. 2353-2362, traduction française). Les résultats de chaque cas sont dans
`tests/formulas/prestations/contributives/indemnites_familiales_secteur_public.yaml`.
"""

from openfisca_tunisia.variables.prestations.contributives.indemnites_familiales_secteur_public import (
    CAS_ANNEXE_2,
)


def test_la_table_porte_les_81_cas():
    codes = [ligne[0] for ligne in CAS_ANNEXE_2]
    assert sorted(codes) == list(range(1, 82))
