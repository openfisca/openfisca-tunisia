# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Revenus fonciers


# Régime réel

class foncier_reel_resultat_fiscal(Variable):
    column = IntCol
    entity = Individu
    label = u"Résultat fiscal (revenus fonciers, régime réel)"
    definition_period = YEAR


# Régime forfaitaire bâti

class foncier_forfaitaire_batis_recettes(Variable):
    column = IntCol
    entity = Individu
    label = u"Recettes brutes réalisées TTC (revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_batis_reliquat(Variable):
    column = IntCol
    entity = Individu
    label = u"Reliquat (revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_batis_frais(Variable):
    column = IntCol
    entity = Individu
    label = u"Frais d’entretien et de réparation justifiés à déduire " \
        u"(revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_batis_taxe(Variable):
    column = IntCol
    entity = Individu
    label = u"Taxe effectivement payée à déduire (revenus fonciers, base forfaitaire, immeubles bâtis)"
    definition_period = YEAR


# Régime forfaitaire non bâti

class foncier_forfaitaire_non_batis_recettes(Variable):
    column = IntCol
    entity = Individu
    label = u"Recettes brutes réalisées TTC (revenus fonciers, base forfaitaire, terrains non bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_non_batis_depenses(Variable):
    column = IntCol
    entity = Individu
    label = u"Dépenses justifiées à déduire (revenus fonciers, base forfaitaire, terrains non bâtis)"
    definition_period = YEAR


class foncier_forfaitaire_non_batis_taxe(Variable):
    column = IntCol
    entity = Individu
    label = u"Taxe effectivement payée à déduire (revenus fonciers, base forfaitaire, terrains non bâtis)"
    definition_period = YEAR


class foncier_societes_personnes(Variable):
    column = IntCol
    entity = Individu
    label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent des revenus fonciers"
    definition_period = YEAR
