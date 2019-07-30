# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Revenus fonciers


# Régime réel

class foncier_reel_resultat_fiscal(Variable):
    value_type = int
    entity = Individu
    label = "Résultat fiscal (revenus fonciers, régime réel)"
    definition_period = YEAR


# Régime forfaitaire bâti

class foncier_forfaitaire_batis_recettes(Variable):
    value_type = int
    entity = Individu
    label = "Recettes brutes réalisées TTC (revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_batis_reliquat(Variable):
    value_type = int
    entity = Individu
    label = "Reliquat (revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_batis_frais(Variable):
    value_type = int
    entity = Individu
    label = "Frais d’entretien et de réparation justifiés à déduire " \
        "(revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_batis_taxe(Variable):
    value_type = int
    entity = Individu
    label = "Taxe effectivement payée à déduire (revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


# Régime forfaitaire non bâti

class foncier_forfaitaire_non_batis_recettes(Variable):
    value_type = int
    entity = Individu
    label = "Recettes brutes réalisées TTC (revenus fonciers, base forfaitaire, terrains non bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_non_batis_depenses(Variable):
    value_type = int
    entity = Individu
    label = "Dépenses justifiées à déduire (revenus fonciers, base forfaitaire, terrains non bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_non_batis_taxe(Variable):
    value_type = int
    entity = Individu
    label = "Taxe effectivement payée à déduire (revenus fonciers, base forfaitaire, terrains non bâtis)"
    definition_period = YEAR


class foncier_societes_personnes(Variable):
    value_type = int
    entity = Individu
    label = "Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent des revenus fonciers"
    definition_period = YEAR
