'''6. Revenus de valeurs mobilières et de capitaux mobiliers.'''


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class tspr(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Traitements, salaires, indemnités, pensions et rentes viagères'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        revenu_assimile_salaire_apres_abattements = foyer_fiscal(
            'revenu_assimile_salaire_apres_abattements', period = period)
        revenu_assimile_pension_apres_abattements = foyer_fiscal(
            'revenu_assimile_pension_apres_abattements', period = period)

        return revenu_assimile_salaire_apres_abattements + revenu_assimile_pension_apres_abattements


class revenu_assimile_salaire(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu assimilé à des salaires'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        salaire_imposable = foyer_fiscal.declarant_principal('salaire_imposable', period = period, options = [ADD])
        salaire_en_nature = foyer_fiscal.declarant_principal('salaire_en_nature', period = period, options = [ADD])
        return (salaire_imposable + salaire_en_nature)


class smig(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = 'Indicatrice de SMIG ou SMAG déduite du montant des salaires'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        salarie_declarant_percevoir_smig = foyer_fiscal.declarant_principal('salarie_declarant_percevoir_smig', period = period.first_month)
        smig_40h_mensuel = parameters(period.start).marche_travail.smig_40h_mensuel
        smig = (
            salarie_declarant_percevoir_smig
            + (revenu_assimile_salaire <= 12 * smig_40h_mensuel)
            )
        return smig


class revenu_assimile_salaire_apres_abattements(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu imposé comme des salaires net des abatements'
    definition_period = YEAR

    def formula_2011(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig = foyer_fiscal('smig', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        revenu_assimile_salaire_apres_abattements = max_(
            (
                revenu_assimile_salaire * (1 - tspr.abat_sal)
                - max_(
                    smig * tspr.abattement_pour_salaire_minimum,
                    (revenu_assimile_salaire <= tspr.smig_ext) * tspr.abattement_pour_salaire_minimum
                    )
                ),
            0
            )
        return revenu_assimile_salaire_apres_abattements

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_salaire = foyer_fiscal('revenu_assimile_salaire', period = period)
        smig = foyer_fiscal('smig', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        return max_(revenu_assimile_salaire * (1 - tspr.abat_sal) - smig * tspr.abattement_pour_salaire_minimum, 0)


class revenu_assimile_pension_apres_abattements(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenu assimilé à des pensions après abattements'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        revenu_assimile_pension = foyer_fiscal.declarant_principal('revenu_assimile_pension', period = period)
        avantages_nature_assimile_pension = foyer_fiscal.declarant_principal(
            'avantages_nature_assimile_pension', period = period)
        tspr = parameters(period.start).impot_revenu.tspr
        return (revenu_assimile_pension + avantages_nature_assimile_pension) * (1 - tspr.abat_pen)
