# -*- coding: utf-8 -*-


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore
from openfisca_tunisia.variables.prelevements_obligatoires.impot_revenu.irpp import calcule_base_imposable


class contribution_sociale_solidarite(Variable):
    value_type = float
    entity = Individu
    label = "Contribution sociale de solidarité"
    definition_period = MONTH
    reference = "http://www.legislation.tn/fr/detailtexte/Loi-num-2017-66-du----jort-2017-101__2017101000661"

    def formula_2018_01_01(individu, period, parameters):
        """
        Art. 53
        Pour les personnes physiques, la différence entre l’impôt sur le revenu déterminé
        sur la base du barème de l’impôt sur le revenu prévu à l’article 44 du code
        de l’impôt sur le revenu des personnes physiques et de l’impôt sur les sociétés,
        en majorant de un point les taux d’imposition applicables aux tranches de revenu
        prévues par ledit barème et l’impôt sur le revenu déterminé sur la base
        dudit barème d’impôt sans la majoration d'un point des taux d’imposition,

        Art. 39 de la loi de finance 2020
        La contribution sociale de solidarité ne s'applique pas aux personnes physiques qui réalisent exclusivement
        les revenus prévus à l'article 25 du code de l'impôt sur le revenu des personnes physiques
        et de l'impôt sur les sociétés et dont le revenu annuel net ne dépasse pas 5000 dinars
        après déduction des abattements au titre de la situation et charges de famille
        prévus à l'article 40 dudit code uniquement.

        """
        salaire_imposable = individu('salaire_imposable', period = period)
        deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)
        irpp_mensuel_salarie = individu('irpp_mensuel_salarie', period = period)

        non_exonere_irpp, revenu_assimile_salaire_apres_abattement = calcule_base_imposable(
            salaire_imposable, deduction_famille_annuelle, period, parameters)
        bareme_irpp = parameters(period.start).impot_revenu.bareme.copy()
        bareme_css = parameters(period.start).prelevements_sociaux.contribution_sociale_solidarite.salarie
        bareme_irpp.add_tax_scale(bareme_css)

        if period.year >= 2020:
            non_exonere_css = (
                (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
                > parameters(period.start).impot_revenu.exoneration.seuil
                )
            return non_exonere_css * (
                - irpp_mensuel_salarie - non_exonere_irpp * bareme_irpp.calc(
                    (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
                    ) / 12
                )
        else:
            return (
                - irpp_mensuel_salarie - non_exonere_irpp * bareme_irpp.calc(
                    (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
                    ) / 12
                )
