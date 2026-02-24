from numpy import datetime64, timedelta64


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
        has_birth = individu.get_holder("date_naissance").get_known_periods()
        if not has_birth:
            has_age_en_mois = bool(
                individu.get_holder("age_en_mois").get_known_periods()
            )
            if has_age_en_mois:
                return individu("age_en_mois", period) // 12

            # If age is known at the same day of another year, compute the new age from it.
            holder = individu.get_holder("age")
            start = period.start
            known_periods = holder.get_known_periods()
            if known_periods:
                for last_period in sorted(known_periods, reverse=True):
                    last_start = last_period.start
                    if last_start.day == start.day:
                        last_array = holder.get_array(last_period)
                        return last_array + int(
                            start.year
                            - last_start.year
                            + (start.month - last_start.month) / 12
                        )

        date_naissance = individu("date_naissance", period)
        epsilon = timedelta64(1)
        return (datetime64(period.start) - date_naissance + epsilon).astype(
            "timedelta64[Y]"
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
        # If age_en_mois is known at the same day of another month, compute the new age_en_mois from it.
        holder = individu.get_holder("age_en_mois")
        start = period.start
        known_periods = holder.get_known_periods()

        for last_period in sorted(known_periods, reverse=True):
            last_start = last_period.start
            if last_start.day == start.day:
                last_array = holder.get_array(last_period)
                return last_array + (
                    (start.year - last_start.year) * 12
                    + (start.month - last_start.month)
                )

        has_birth = individu.get_holder("date_naissance").get_known_periods()
        if not has_birth:
            has_age = bool(individu.get_holder("age").get_known_periods())
            if has_age:
                return individu("age", period) * 12
        date_naissance = individu("date_naissance", period)
        epsilon = timedelta64(1)
        return (datetime64(period.start) - date_naissance + epsilon).astype(
            "timedelta64[M]"
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
