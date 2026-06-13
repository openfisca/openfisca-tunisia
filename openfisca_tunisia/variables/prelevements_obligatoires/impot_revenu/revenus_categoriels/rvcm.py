"""6. Revenus de valeurs mobilières et de capitaux mobiliers"""

from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class rvcm(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Revenus de valeurs mobilières et de capitaux mobiliers"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        capm_banq = foyer_fiscal.declarant_principal("capm_banq", period=period)
        capm_cent = foyer_fiscal.declarant_principal("capm_cent", period=period)
        capm_caut = foyer_fiscal.declarant_principal("capm_caut", period=period)
        capm_part = foyer_fiscal.declarant_principal("capm_part", period=period)
        capm_oblig = foyer_fiscal.declarant_principal("capm_oblig", period=period)
        capm_caisse = foyer_fiscal.declarant_principal("capm_caisse", period=period)
        capm_plfcc = foyer_fiscal.declarant_principal("capm_plfcc", period=period)
        capm_epinv = foyer_fiscal.declarant_principal("capm_epinv", period=period)
        capm_aut = foyer_fiscal.declarant_principal("capm_aut", period=period)

        return (
            capm_banq
            + capm_cent
            + capm_caut
            + capm_part
            + capm_oblig
            + capm_caisse
            + capm_plfcc
            + capm_epinv
            + capm_aut
        )
