"""Revenus de valeurs mobilières et de capitaux mobiliers."""

from openfisca_tunisia.variables.base import *


# A Revenus des valeurs mobilières et de capitaux mobiliers


class valm_nreg(Variable):
    value_type = int
    label = "Revenus des valeurs mobilières autres que ceux régulièrement distribués"
    entity = Individu
    definition_period = YEAR


class valm_jpres(Variable):
    value_type = int
    label = "Jetons de présence"
    entity = Individu
    definition_period = YEAR


class valm_aut(Variable):
    value_type = int
    label = "Autres rémunérations assimilées"
    entity = Individu
    definition_period = YEAR


# B Revenus de capitaux mobiliers


class capm_banq(Variable):
    value_type = int
    label = "Intérêts bruts des comptes spéciaux d'épargne ouverts auprès des banques"
    entity = Individu
    definition_period = YEAR


class capm_cent(Variable):
    value_type = int
    label = "Intérêts bruts des comptes spéciaux d'épargne ouverts auprès de la CENT"
    entity = Individu
    definition_period = YEAR


class capm_caut(Variable):
    value_type = int
    label = "Intérêts des créances et intérêts et rémunérations des cautionnements"
    entity = Individu
    definition_period = YEAR


class capm_part(Variable):
    value_type = int
    label = "Intérêts des titres de participation"
    entity = Individu
    definition_period = YEAR


class capm_oblig(Variable):
    value_type = int
    label = "Intérêts des emprunts obligataires"
    entity = Individu
    definition_period = YEAR


class capm_caisse(Variable):
    value_type = int
    label = "Intérêts des bons de caisse"
    entity = Individu
    definition_period = YEAR


class capm_plfcc(Variable):
    value_type = int
    label = "Revenus des parts et de liquidation du fonds commun des créances"
    entity = Individu
    definition_period = YEAR


class capm_epinv(Variable):
    value_type = int
    label = "Intérêts des comptes épargne pour l'investissement"
    entity = Individu
    definition_period = YEAR


class capm_aut(Variable):
    value_type = int
    label = "Autres intérêts"
    entity = Individu
    definition_period = YEAR
