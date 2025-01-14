from openfisca_tunisia.variables.base import *


class allocation_familiale_non_contributive(Variable):
    value_type = float
    entity = Menage
    label = 'Allocation familiale pour les ménages non affiliés à un régime de sécurité sociale'
    definition_period = MONTH

    def formula(menage, period, parameters):
        return (
            menage('allocation_familiale_non_contributive_0_5', period)
            + menage('allocation_familiale_non_contributive_6_18', period)
            )


class allocation_familiale_non_contributive_0_5(Variable):
    value_type = float
    entity = Menage
    label = 'Allocation familiale pour les enfants entre 0  et 5 ans pour les ménages non affiliés à un régime de sécurité sociale'
    definition_period = MONTH

    def formula_2020_06(menage, period, parameters):
        age = menage.members('age', period)
        eligible = menage('eligible_allocation_familiale_non_contributive_0_5', period)
        enfant_a_charge_0_5 = (age >= 0) * (age <= 5)
        enfants_eligibles = eligible * menage.sum(enfant_a_charge_0_5, role = Menage.ENFANT)
        allocation_familiale = parameters(period).prestations.non_contributives.allocation_familiale
        return enfants_eligibles * allocation_familiale


class allocation_familiale_non_contributive_6_18(Variable):
    value_type = float
    entity = Menage
    label = 'Allocation familiale pour les enfants entre 6 et 18 ans pour les ménages non affiliés à un régime de sécurité sociale'
    definition_period = MONTH

    def formula_2022_07(menage, period, parameters):
        age = menage.members('age', period)
        eligible = menage('eligible_allocation_familiale_non_contributive_6_18', period)
        enfant_a_charge_6_18 = (6 <= age) * (age >= 18)
        enfants_eligibles = eligible * menage.sum(enfant_a_charge_6_18, role = Menage.ENFANT)
        allocation_familiale = parameters(period).prestations.non_contributives.allocation_familiale
        return enfants_eligibles * allocation_familiale


class eligible_allocation_familiale_non_contributive_0_5(Variable):
    value_type = bool
    entity = Menage
    label = "Eligibilité à l'allocation familiale non contributive pour les enfants de 0 à 5 ans"
    definition_period = MONTH

    def formula_2020_06(menage, period, parameters):
        # TODO quand est-ce que cela débute ?
        # https://www.unicef.org/mena/media/24061/file
        # Mai 2020: décret abolissant
        # la limite du nombre d’enfants
        # éligibles par ménage (aupar-
        # avant limité à 3 enfants par
        # ménage) et supprimant le
        # seuil d’âge (l’âge minimum
        # pour
        # bénéficier d’une allocation
        # familiale était de plus de 5
        # ans

        return (
            menage('pnafn_eligible', period)
            + menage('amg_1', period)
            + menage('amg_2', period)
            + menage('amen_social_eligible', period)
            )


class eligible_allocation_familiale_non_contributive_6_18(Variable):
    value_type = bool
    entity = Menage
    label = "Eligibilité à l'allocation familiale non contributive pour les enfants de 6 à 18 ans"
    definition_period = MONTH

    def formula_2023_02(menage, period, parameters):
        return (
            menage('pnafn_eligible', period)
            + menage('amg_1', period)
            + menage('amg_2', period)
            )

    def formula_2022_07(menage, period, parameters):
        return (
            menage('pnafn_eligible', period)
            + menage('amg_1', period)
            )
