# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# rvcm Revenus de valeurs mobilières et de capitaux mobiliers
# A Revenus des valeurs mobilières et de capitaux mobiliers


class valm_nreg(Variable):
    column = IntCol
    label = u"Revenus des valeurs mobilières autres que ceux régulièrement distribués"
    entity = Individu
    definition_period = YEAR


class valm_jpres(Variable):
    column = IntCol
    label = u"Jetons de présence"
    entity = Individu
    definition_period = YEAR


class valm_aut(Variable):
    column = IntCol
    label = u"Autres rémunérations assimilées"
    entity = Individu
    definition_period = YEAR


# B Revenus de capitaux mobiliers


class capm_banq(Variable):
    column = IntCol
    label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès des banques"
    entity = Individu
    definition_period = YEAR


class capm_cent(Variable):
    column = IntCol
    label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès de la CENT"
    entity = Individu
    definition_period = YEAR


class capm_caut(Variable):
    column = IntCol
    label = u"Intérêts des créances et intérêts et rémunérations des cautionnements"
    entity = Individu
    definition_period = YEAR


class capm_part(Variable):
    column = IntCol
    label = u"Intérêts des titres de participation"
    entity = Individu
    definition_period = YEAR


class capm_oblig(Variable):
    column = IntCol
    label = u"Intérêts des emprunts obligataires"
    entity = Individu
    definition_period = YEAR


class capm_caisse(Variable):
    column = IntCol
    label = u"Intérêts des bons de caisse"
    entity = Individu
    definition_period = YEAR


class capm_plfcc(Variable):
    column = IntCol
    label = u"Revenus des parts et de liquidation du fonds commun des créances"
    entity = Individu
    definition_period = YEAR


class capm_epinv(Variable):
    column = IntCol
    label = u"Intérêts des comptes épargne pour l'investissement"
    entity = Individu
    definition_period = YEAR


class capm_aut(Variable):
    column = IntCol
    label = u"Autres intérêts"
    entity = Individu
    definition_period = YEAR
