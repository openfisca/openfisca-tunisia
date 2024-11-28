from openfisca_tunisia.variables.base import *  # noqa analysis:ignore
from openfisca_tunisia.variables.prelevements_obligatoires.impot_revenu.irpp import calcule_base_imposable


class contribution_sociale_solidarite(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Contribution sociale de solidarité'
    definition_period = YEAR

    def formula_2020_01_01(foyer_fiscal, period, parameters):
        impot_revenu_brut = bareme.calc(revenu_net_imposable)
        revenu_net_imposable = foyer_fiscal('revenu_net_imposable', period = period)
        bareme_irpp = parameters(period.start).impot_revenu.bareme.copy()
        bareme_css = parameters(period.start).prelevements_sociaux.contribution_sociale_solidarite.salarie
        bareme_irpp.add_tax_scale(bareme_css)
        non_exonere_css = (
            revenu_net_imposable
            > parameters(period.start).impot_revenu.exoneration.seuil
            )
        return non_exonere_css * (
            non_exonere_irpp * bareme_irpp.calc(revenu_net_imposable)
            - impot_revenu_brut
            )

    def formula_2018_01_01(foyer_fiscal, period, parameters):
        revenu_net_imposable = foyer_fiscal('revenu_net_imposable', period = period)
        bareme_irpp = parameters(period.start).impot_revenu.bareme.copy()
        impot_revenu_brut = bareme_irpp.calc(revenu_net_imposable)
        non_exonere_irpp = revenu_net_imposable >= 0
        bareme_css = parameters(period.start).prelevements_sociaux.contribution_sociale_solidarite.salarie
        bareme_irpp.add_tax_scale(bareme_css)
        contribution_sociale_solidarite = (
            non_exonere_irpp * bareme_irpp.calc(revenu_net_imposable)
            - impot_revenu_brut
            )
        return contribution_sociale_solidarite


class contribution_sociale_solidarite_nette_a_payer(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Contribution sociale de solidarité nette des prélèvements à la source'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        return (
            foyer_fiscal('contribution_sociale_solidarite', period)
            - foyer_fiscal.sum(foyer_fiscal.members('contribution_sociale_solidarite_prelevee_a_la_source', period, options = [ADD]))
            )


class contribution_sociale_solidarite_prelevee_a_la_source(Variable):
    value_type = float
    entity = Individu
    label = 'Contribution sociale de solidarité'
    definition_period = MONTH

    def formula_2020_01_01(individu, period, parameters):
        salaire_imposable = individu('salaire_imposable', period = period)
        deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)
        irpp_salarie_preleve_a_la_source = individu('irpp_salarie_preleve_a_la_source', period = period)
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

    def formula_2018_01_01(individu, period, parameters):
        '''
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
        '''
        salaire_imposable = individu('salaire_imposable', period = period)
        deduction_famille_annuelle = individu.foyer_fiscal('deduction_famille', period = period.this_year)
        irpp_salarie_preleve_a_la_source = individu('irpp_salarie_preleve_a_la_source', period = period)

        non_exonere_irpp, revenu_assimile_salaire_apres_abattement = calcule_base_imposable(
            salaire_imposable, deduction_famille_annuelle, period, parameters)
        bareme_irpp = parameters(period.start).impot_revenu.bareme.copy()
        bareme_css = parameters(period.start).prelevements_sociaux.contribution_sociale_solidarite.salarie
        bareme_irpp.add_tax_scale(bareme_css)
        contribution_sociale_solidarite = (
            non_exonere_irpp * bareme_irpp.calc(
                (12 * revenu_assimile_salaire_apres_abattement - deduction_famille_annuelle)
                ) / 12
            - irpp_salarie_preleve_a_la_source
            )
        return contribution_sociale_solidarite
