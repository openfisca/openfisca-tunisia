from numpy import datetime64


from openfisca_tunisia.variables.base import *


class age(Variable):
    unit = "years"
    value_type = int
    default_value = AGE_INT_MINIMUM
    entity = Individu
    label = "Âge (en années) au premier jour du mois"
    definition_period = MONTH
    is_period_size_independent = True
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        date_naissance = individu("date_naissance", period)
        return (
            (datetime64(period.start) - date_naissance)
            .astype("timedelta64[Y]")
            .astype(int)
        )


class age_en_mois(Variable):
    value_type = int
    default_value = AGE_INT_MINIMUM
    unit = "months"
    entity = Individu
    label = "Âge (en mois)"
    is_period_size_independent = True
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        date_naissance = individu("date_naissance", period)
        return (
            (datetime64(period.start) - date_naissance)
            .astype("timedelta64[M]")
            .astype(int)
        )


class date_naissance(Variable):
    value_type = date
    default_value = date(1970, 1, 1)
    entity = Individu
    label = "Date de naissance"
    definition_period = ETERNITY


class male(Variable):
    value_type = bool
    entity = Individu
    label = "Mâle"
    definition_period = ETERNITY


class marie(Variable):
    value_type = bool
    entity = Individu
    label = "Marié(e)"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu("statut_marital", period=period)
        return statut_marital == 1


class celibataire(Variable):
    value_type = bool
    entity = Individu
    label = "Célibataire"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu("statut_marital", period=period)
        return statut_marital == 2


class divorce(Variable):
    value_type = bool
    entity = Individu
    label = "Divorcé(e)"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu("statut_marital", period=period)
        return statut_marital == 3


class veuf(Variable):
    value_type = bool
    entity = Individu
    label = "Veuf(ve)"
    definition_period = YEAR

    def formula(individu, period):
        statut_marital = individu("statut_marital", period=period)
        return statut_marital == 4


class statut_marital(Variable):
    value_type = int
    default_value = 2
    entity = Individu
    label = "Statut marital"
    definition_period = YEAR
