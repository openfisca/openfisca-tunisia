# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# Autres revenus


class salaire_etranger(Variable):
    column = IntCol
    label = u"Salaires perçus à l'étranger"
    entity = Individu


class pension_etranger_non_transferee(Variable):
    column = IntCol
    label = u"Pensions perçues à l'étranger (non transférées)"
    entity = Individu


class pension_etranger_transferee(Variable):
    column = IntCol
    label = u"Pensions perçues à l'étranger (transférées en Tunisie)"
    entity = Individu


class autres_revenus_etranger(Variable):
    column = IntCol
    label = u"Autres revenus perçus à l'étranger"
    entity = Individu

# Revenus exonérés
# Revenus non imposables

# deficit antérieurs non déduits


class deficits_anterieurs_non_deduits(Variable):
    column = IntCol
    label = u"Déficits des années antérieures non déduits"
    entity = Individu
