'''7. revenus de source étrangère'''


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class revenus_source_etrangere(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Autres revenus (revenus de source étrangère n’ayant pas subi l’impôt dans le pays d'origine)"
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        salaire_etranger = foyer_fiscal.declarant_principal('salaire_etranger', period = period)
        pension_etranger_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_transferee', period = period)
        pension_etranger_non_transferee = foyer_fiscal.declarant_principal(
            'pension_etranger_non_transferee', period = period)
        autres_revenus_etranger = foyer_fiscal.declarant_principal(
            'autres_revenus_etranger', period = period)
        tspr = parameters(period.start).impot_revenu.tspr

        return (
            salaire_etranger * (1 - tspr.abat_sal)
            + pension_etranger_non_transferee * (1 - tspr.abat_pen)
            + pension_etranger_transferee * (1 - tspr.abat_pen_etr)
            + autres_revenus_etranger
            )
