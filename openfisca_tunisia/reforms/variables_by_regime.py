from openfisca_core.model_api import *  # noqa F401
from openfisca_core.reforms import Reform


from openfisca_tunisia.entities import Individu

from openfisca_tunisia.variables.prelevements_obligatoires.cotisations_sociales import TypesRegimeSecuriteSocialeCotisant
from openfisca_tunisia.variables.prelevements_obligatoires.impot_revenu.irpp import calcule_impot_revenu_brut, calcule_base_imposable


# from openfisca_tunisia.variables.prelevements_obligatoires.cotisations_sociales import compute_cotisation_regime


def compute_cotisation_regime(individu, period, parameters = None, regime = None, cotisation_type = None):
    assert cotisation_type in ['employeur', 'salarie']
    assert regime in TypesRegimeSecuriteSocialeCotisant._member_names_ and regime != 'neant'

    assiette_cotisations_sociales = (
        individu(f'{regime}_salaire_de_base', period)
        + individu('primes', period)
        )

    baremes_by_regime = parameters(period.start).prelevements_sociaux.cotisations_sociales
    cotisation = individu.empty_array()

    if f'cotisations_{cotisation_type}' not in baremes_by_regime[regime]._children:
        return cotisation

    baremes_by_name = getattr(
        baremes_by_regime[regime],
        f'cotisations_{cotisation_type}',
        )
    baremes = [
        baremes_by_name._children[bareme_name]
        for bareme_name in baremes_by_name._children.keys()
        if bareme_name != 'assurances_sociales'
        ]

    if 'assurances_sociales' in baremes_by_name._children:
        baremes_assurances_sociales = getattr(baremes_by_name, 'assurances_sociales')
        baremes_additionnels = baremes_assurances_sociales._children.values()
        baremes += baremes_additionnels

    for bareme in baremes:
        cotisation += bareme.calc(assiette_cotisations_sociales)

    return cotisation


class openfisca_variable_by_regime_extension(Reform):
    def apply(self):
        for regime in TypesRegimeSecuriteSocialeCotisant._member_names_:
            if regime == 'neant':
                continue

            if regime in ['pensionne_cnrps', 'raci', 're', 'rtns']:
                continue

            # Add regime_cotisations_salarie and regime_cotisations_employeur
            for cotisation_type in ['salarie', 'employeur']:
                class_name = f'{regime}_cotisations_{cotisation_type}'
                label = f'Cotisations {cotisation_type} pour le régime {regime}'

                def formula_creator(regime, cotisation_type):
                    def formula(individu, period, parameters):
                        return compute_cotisation_regime(
                            individu,
                            period,
                            parameters,
                            regime = regime,
                            cotisation_type = cotisation_type
                            )

                    formula.__name__ = 'formula'
                    return formula

                variable_instance = type(
                    class_name,
                    (Variable,),
                    dict(
                        value_type = float,
                        entity = Individu,
                        label = label,
                        definition_period = MONTH,
                        formula = formula_creator(regime, cotisation_type),
                        ),
                    )
                self.add_variable(variable_instance)
                del variable_instance

            # Add regime_salaire_de_base
            class_name = f'{regime}_salaire_de_base'
            label = f'Salaire de base pour le régime {regime}'

            variable_instance = type(
                class_name,
                (Variable,),
                dict(
                    value_type = float,
                    entity = Individu,
                    label = label,
                    definition_period = MONTH,
                    ),
                )
            self.add_variable(variable_instance)
            del variable_instance

            # Add regime salaire_imposable
            class_name = f'{regime}_salaire_imposable'
            label = f'Salaire imposable pour le régime {regime}'

            def salaire_imposable_formula_creator(regime):
                def formula(individu, period):
                    return (
                        individu(f'{regime}_salaire_de_base', period)
                        + individu('primes', period)
                        - individu(f'{regime}_cotisations_salarie', period)
                        )

                formula.__name__ = 'formula'
                return formula

            variable_instance = type(
                class_name,
                (Variable,),
                dict(
                    value_type = float,
                    entity = Individu,
                    label = label,
                    definition_period = MONTH,
                    set_input = set_input_divide_by_period,
                    formula = salaire_imposable_formula_creator(regime),
                    ),
                )
            self.add_variable(variable_instance)
            del variable_instance

            # Add regime salaire_net_a_payer
            class_name = f'{regime}_salaire_net_a_payer'
            label = f'Salaire net à payer pour le régime {regime}'

            def salaire_net_a_payer_formula_creator(regime):
                def formula(individu, period):
                    return (
                        individu(f'{regime}_salaire_imposable', period)
                        - individu(f'{regime}_irpp_salarie_preleve_a_la_source', period)
                        - individu(f'{regime}_contribution_sociale_solidarite_prelevee_a_la_source', period)
                        )

                formula.__name__ = 'formula'
                return formula

            variable_instance = type(
                class_name,
                (Variable,),
                dict(
                    value_type = float,
                    entity = Individu,
                    label = label,
                    definition_period = MONTH,
                    set_input = set_input_divide_by_period,
                    formula = salaire_net_a_payer_formula_creator(regime),
                    ),
                )
            self.add_variable(variable_instance)
            del variable_instance

            # Add regime irpp_salarie_preleve_a_la_source
            class_name = f'{regime}_irpp_salarie_preleve_a_la_source'
            label = 'Impôt sur le revenu des personnes physiques prélevé à la source pour les salariés du régime {regime}'

            def irpp_salarie_preleve_a_la_source_formula_creator(regime):
                def formula(individu, period, parameters):
                    salaire_imposable = individu(f'{regime}_salaire_imposable', period = period)
                    deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)
                    return calcule_impot_revenu_brut(
                        salaire_imposable, deduction_famille_annuelle, period, parameters,
                        )

                formula.__name__ = 'formula'
                return formula

            variable_instance = type(
                class_name,
                (Variable,),
                dict(
                    value_type = float,
                    entity = Individu,
                    label = label,
                    definition_period = MONTH,
                    set_input = set_input_divide_by_period,
                    formula = irpp_salarie_preleve_a_la_source_formula_creator(regime),
                    ),
                )
            self.add_variable(variable_instance)
            del variable_instance

            # Add regime contribution_sociale_solidarite_prelevee_a_la_source
            class_name = f'{regime}_contribution_sociale_solidarite_prelevee_a_la_source'
            label = 'Contribution sociale de solidarité pour les salariés du régime {regime}'

            def contribution_sociale_solidarite_prelevee_a_la_source_formula_creator(regime):
                def formula(individu, period, parameters):
                    salaire_imposable = individu(f'{regime}_salaire_imposable', period = period)
                    deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)
                    irpp_salarie_preleve_a_la_source = individu(f'{regime}_irpp_salarie_preleve_a_la_source', period = period)
                    non_exonere_irpp, revenu_assimile_salaire_apres_abattement = calcule_base_imposable(
                        salaire_imposable, deduction_famille_annuelle, period, parameters)
                    bareme_irpp = parameters(period.start).impot_revenu.bareme.copy()
                    bareme_css = parameters(period.start).prelevements_sociaux.contribution_sociale_solidarite.salarie
                    bareme_irpp.add_tax_scale(bareme_css)
                    non_exonere_css = (
                        (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
                        > parameters(period.start).impot_revenu.exoneration.seuil
                        )
                    return non_exonere_css * (
                        non_exonere_irpp * bareme_irpp.calc(
                            (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
                            ) / 12
                        - irpp_salarie_preleve_a_la_source
                        )

                formula.__name__ = 'formula'
                return formula

            variable_instance = type(
                class_name,
                (Variable,),
                dict(
                    value_type = float,
                    entity = Individu,
                    label = label,
                    definition_period = MONTH,
                    set_input = set_input_divide_by_period,
                    formula = contribution_sociale_solidarite_prelevee_a_la_source_formula_creator(regime),
                    ),
                )
            self.add_variable(variable_instance)
            del variable_instance


# TODO:
# - Lister les Variables à retirer ou à corriger
