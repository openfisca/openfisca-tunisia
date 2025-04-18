import os

from openfisca_core.parameters import ParameterNode
from openfisca_tunisia.tunisia_taxbenefitsystem import COUNTRY_DIR

from openfisca_core.periods.helpers import period
from openfisca_tunisia.variables.prelevements_obligatoires.cotisations_sociales import TypesRegimeSecuriteSocialeCotisant

period = period(2024)

parameters = ParameterNode("", directory_path=os.path.join(COUNTRY_DIR, 'parameters'))


baremes_by_regime = parameters(period.start).prelevements_sociaux.cotisations_sociales


baremes_by_cotisation_type_by_regime = dict()
for regime in TypesRegimeSecuriteSocialeCotisant._member_names_:
    if regime == 'neant':
        continue

    baremes_by_cotisation_type = dict()
    for cotisation_type in ['salarie', 'employeur']:
        if f'cotisations_{cotisation_type}' not in baremes_by_regime[regime]._children:
            continue
        else:
            print(regime)
            baremes_of_cotisation_type = getattr(baremes_by_regime[regime], f'cotisations_{cotisation_type}')
            baremes = list(baremes_of_cotisation_type._children.keys())
            if 'assurances_sociales' in baremes:
                baremes_assurances_sociales = getattr(baremes_of_cotisation_type, 'assurances_sociales')
                baremes_assurances_sociales_names = list(baremes_assurances_sociales._children.keys())
                baremes.remove('assurances_sociales')
                baremes += baremes_assurances_sociales_names

            baremes_by_cotisation_type[cotisation_type] = baremes
            baremes_by_cotisation_type_by_regime[regime] = baremes_by_cotisation_type


# https://git.leximpact.dev/leximpact/simulateur-socio-fiscal/budget/leximpact-survey-scenario/-/blob/master/leximpact_survey_scenario/leximpact_tax_and_benefit_system.py?ref_type=heads#L603

# TODO:
# - write a variable that computes cotisations salarie and employeur of a regime
# - test it
# - generalise


