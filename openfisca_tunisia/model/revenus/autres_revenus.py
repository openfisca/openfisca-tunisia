from openfisca_tunisia.model.base import *


# Autres revenus


class salaire_etranger(Variable):
    value_type = int
    label = "Salaires perçus à l'étranger"
    entity = Individu
    definition_period = YEAR


class pension_etranger_non_transferee(Variable):
    value_type = int
    label = "Pensions perçues à l'étranger (non transférées)"
    entity = Individu
    definition_period = YEAR


class pension_etranger_transferee(Variable):
    value_type = int
    label = "Pensions perçues à l'étranger (transférées en Tunisie)"
    entity = Individu
    definition_period = YEAR


class autres_revenus_etranger(Variable):
    value_type = int
    label = "Autres revenus perçus à l'étranger"
    entity = Individu
    definition_period = YEAR

# Revenus exonérés
# Revenus non imposables

# deficit antérieurs non déduits


class deficits_anterieurs_non_deduits(Variable):
    value_type = int
    label = "Déficits des années antérieures non déduits"
    entity = Individu
    definition_period = YEAR
