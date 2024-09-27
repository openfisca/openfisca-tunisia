import os
from openfisca_tunisia import CountryTaxBenefitSystem as TunisiaTaxBenefitSystem
from openfisca_tunisia.tunisia_taxbenefitsystem import TunisiaTaxBenefitSystem

from openfisca_survey_manager.scenarios import AbstractSurveyScenario

survey_variables_filepath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data.py'
    )


class TunisiaSurveyScenario(AbstractSurveyScenario):
    id_variable_by_entity_key = dict(
        foyer_fiscal = 'id_foyer_fiscal',
        menage = 'id_menage',
        )
    role_variable_by_entity_key = dict(
        foyer_fiscal = 'role_foyer_fiscal',
        menage = 'role_menage',
        )

    weight_column_name_by_entity = dict(
        individu = 'poids',
        foyer_fiscal = 'poids_foyer_fiscal',
        menage = 'poids_menage',
        )

    def __init__(self, input_data_frame = None, tax_benefit_system = None,
            baseline_tax_benefit_system = None, year = None):
        super(TunisiaSurveyScenario, self).__init__()
        assert input_data_frame is not None
        assert year is not None
        self.year = year
        if tax_benefit_system is None:
            tax_benefit_system = TunisiaTaxBenefitSystem()

        tax_benefit_system.add_variables_from_file(survey_variables_filepath)
        if baseline_tax_benefit_system:
            baseline_tax_benefit_system.add_variables_from_file(survey_variables_filepath)

        self.set_tax_benefit_systems(
            tax_benefit_system = tax_benefit_system,
            baseline_tax_benefit_system = baseline_tax_benefit_system
            )

        self.used_as_input_variables = list(
            set(list(tax_benefit_system.variables.keys())).intersection(
                set(input_data_frame.columns)
                ))
        self.init_from_data_frame(input_data_frame = input_data_frame)
        self.new_simulation()
        if baseline_tax_benefit_system is not None:
            self.new_simulation(use_baseline = True)
