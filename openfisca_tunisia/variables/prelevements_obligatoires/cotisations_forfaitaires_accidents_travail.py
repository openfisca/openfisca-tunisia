"""Cotisations forfaitaires d'accidents du travail et de maladies professionnelles.

Le décret n° 95-538 du 1er avril 1995 (articles 4 à 7) assoit la cotisation d'accidents du
travail et de maladies professionnelles sur un salaire forfaitaire pour des catégories dont le
salaire effectif est difficile à établir. Les paramètres de ces forfaits vivent sous
``prelevements_sociaux/atmp_forfaits`` et la modulation sous ``prelevements_sociaux/atmp_modulation``.

Seul le forfait des employés de maison (article 6) est entièrement déterminé par le droit — taux
propres à l'article et assiette fixe (SMAG rapporté à 300 jours) — et donc calculé ici. Les autres
forfaits (agricole et pêche de l'article 4, dont l'assiette dépend des surfaces et des effectifs ;
chauffeurs et masseurs de l'article 5 ; temporaires de l'article 7, dont le taux de branche n'est
pas désigné) sont versés en paramètres mais leur arborescence de variables reste à arbitrer : voir
``docs/notes/atmp-forfaits-95-538.md`` et l'issue openfisca-tunisia#471.
"""

from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class TypesEmployeMaisonAccidentTravail(Enum):
    __order__ = "non_concerne aide_de_menage autre_employe conducteur"
    non_concerne = "Non concerné"
    aide_de_menage = "Aide de ménage"
    autre_employe = "Autre employé de maison, sauf chauffeur"
    conducteur = "Conducteur de voiture"


class employe_maison_accident_travail_categorie(Variable):
    value_type = Enum
    possible_values = TypesEmployeMaisonAccidentTravail
    default_value = TypesEmployeMaisonAccidentTravail.non_concerne
    entity = Individu
    label = "Catégorie d'employé de maison pour la cotisation forfaitaire d'accidents du travail (décret n° 95-538, art. 6)"
    definition_period = YEAR
    set_input = set_input_dispatch_by_period


class cotisation_accident_travail_forfaitaire_employe_maison(Variable):
    value_type = float
    entity = Individu
    label = "Cotisation annuelle forfaitaire d'accidents du travail des employés de maison (décret n° 95-538, art. 6)"
    definition_period = YEAR
    reference = "https://www.pist.tn/jort/1995/1995F/Jo03095.pdf"

    def formula_1995_01_01(individu, period, parameters):
        categorie = individu("employe_maison_accident_travail_categorie", period)
        valeurs = categorie.possible_values
        smag_journalier = parameters(period.start).marche_travail.smag_journalier
        forfaits = parameters(
            period.start
        ).prelevements_sociaux.atmp_forfaits.employes_maison
        base = smag_journalier * forfaits.base_jours
        taux = (
            (categorie == valeurs.aide_de_menage) * forfaits.taux_aides_menage
            + (categorie == valeurs.autre_employe) * forfaits.taux_autres
            + (categorie == valeurs.conducteur) * forfaits.taux_conducteurs
        )
        coefficient = where(
            categorie == valeurs.conducteur, forfaits.coefficient_conducteurs, 1
        )
        return taux * base * coefficient
