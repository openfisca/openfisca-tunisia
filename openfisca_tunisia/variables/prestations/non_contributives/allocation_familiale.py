from openfisca_tunisia.variables.base import *


class amen_social_allocation_familiale(Variable):
    value_type = float
    entity = Menage
    label = 'Allocation familiale du programme Amen social'
    definition_period = MONTH

    def formula_2023_02(menage, period, parameters):
        # Extension aux amg2
        age = menage.members('age', period)
        # Les enfants sont considérés comme éligibles de 6 ans à 18 ans
        # eleve = menage.members('eleve', period.this_year)
        allocation_familiale = 30
        amen_social_eligible = individu('amen_social_eligible', period)
        pnafn = individu('pnafn_eligible', period)
        amg_1 = individu('amg_1', period)
        amg_2 = individu('amg_2', period)
        enfant_a_charge_0_5 = (age >= 0) * (age <= 5)
        enfant_a_charge_6_18 = (6 <= age) * (age >= 18)
        eligible_0_5 = amen_social_eligible
        eligible_6_18 = (pnafn + amg_1 + amg_2)
        enfants_eligibles = menage.sum(
            enfant_a_charge_0_5 * eligible_0_5 + enfant_a_charge_6_18 * eligible_6_18,
            role = Menage.ENFANT
            )
        return enfants_eligibles * allocation_familiale

    def formula_2022_07(menage, period, parameters):
        age = menage.members('age', period)
        # Les enfants sont considérés comme éligibles de 6 ans à 18 ans
        # eleve = menage.members('eleve', period.this_year)
        allocation_familiale = 30
        pnafn = individu('pnafn_eligible', period)
        amg_1 = individu('amg_1', period)
        amen_social_eligible = individu('amen_social_eligible', period)
        eligible_0_5 = amen_social_eligible
        enfant_a_charge_0_5 = (age >= 0) * (age <= 5)
        enfant_a_charge_6_18 = (6 <= age) * (age >= 18)
        eligible_6_18 = (pnafn + amg_1)
        enfants_eligibles = menage.sum(
            enfant_a_charge_0_5 * eligible_0_5 + enfant_a_charge_6_18 * eligible_6_18,
            role = Menage.ENFANT
            )
        return enfants_eligibles * allocation_familiale

    def formula_2022_01(menage, period, parameters):
        # Décret présidentiel numéro 2022-8
        # Allocation dans Amen social
        # Institutionalisation rien ne change ? TODO
        age = menage.members('age', period)
        # Les enfants sont considérés comme éligibles de 6 ans à 18 ans
        # eleve = menage.members('eleve', period.this_year)
        allocation_familiale = 30
        amen_social_eligible = individu('amen_social_eligible', period)
        eligible_0_5 = amen_social_eligible
        enfant_a_charge_0_5 = (age >= 0) * (age <= 5)
        enfants_eligibles = menage.sum(
            enfant_a_charge_0_5 * eligible_0_5,
            role = Menage.ENFANT
            )
        return enfants_eligibles * allocation_familiale

    def formula_2020_06(menage, period, parameters):
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
        age = menage.members('age', period)
        # Les enfants sont considérés comme éligibles de 6 ans à 18 ans
        # eleve = menage.members('eleve', period.this_year)
        allocation_familiale = 30
        amen_social_eligible = individu('amen_social_eligible', period)
        eligible_0_5 = amen_social_eligible
        enfant_a_charge_0_5 = (age >= 0) * (age <= 5)
        enfants_eligibles = menage.sum(
            enfant_a_charge_0_5 * eligible_0_5,
            role = Menage.ENFANT
            )
        return enfants_eligibles * allocation_familiale
