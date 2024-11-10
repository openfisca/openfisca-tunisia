from openfisca_tunisia.variables.base import *


class amen_social_eligible(Variable):
    value_type = bool
    entity = Menage
    label = 'Ménage éligible au programme Amen social'
    definition_period = MONTH


class amen_social_enfants_a_charge(Variable):
    value_type = int
    entity = Menage
    label = 'Enfant considéré à charge au sens de la prestation Amen social'
    definition_period = MONTH

    def formula(menage, period, parameters):
        age = menage.members('age', period)
        eleve = menage.members('eleve', period.this_year)
        etudiant = menage.members('etudiant', period.this_year)
        invalide = menage.members('invalide', period.this_year)
        amen_social = parameters(period).prestations.amen_social.supplements
        condition_enfant = (age <= amen_social.limite_age_enfant) * eleve
        condition_jeune_etudiant = (age <= amen_social.limite_age_etudiant) * etudiant
        enfant_a_charge = condition_enfant + condition_jeune_etudiant + invalide
        return menage.sum(enfant_a_charge, role = Menage.ENFANT)


class amen_social_allocation(Variable):
    value_type = float
    entity = Menage
    label = 'Allocation mensuelle Amen social'
    definition_period = MONTH

    def formula(menage, period, parameters):
        amen_social = parameters(period).prestations.amen_social
        eligible = menage('amen_social_eligible', period)

        allocation = eligible * (
            amen_social.allocation_base
            + amen_social_enfant_a_charge)

        return allocation
