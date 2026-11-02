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


def test_salaire_unique_servi_a_l_allocataire_de_l_indemnite_familiale():
    """Quand l'indemnité pour salaire unique est servie (colonne 8), elle l'est à la même
    personne et par le même organisme que l'indemnité familiale (colonne 7) : une seule variable
    d'allocataire et de payeur suffit aux deux prestations."""
    for ligne in CAS_ANNEXE_2:
        (alloc, payeur), (alloc_su, payeur_su) = ligne[7], ligne[8]
        if alloc_su != "N":
            assert (alloc_su, payeur_su) == (alloc, payeur), ligne[0]
