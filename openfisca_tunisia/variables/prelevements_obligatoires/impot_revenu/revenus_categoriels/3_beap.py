"""3. Bénéfices de l'exploitation agricole et de pêche."""


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class beap(Variable):
    value_type = float
    entity = FoyerFiscal
    label = "Bénéfices de l'exploitation agricole et de pêche (BEAP)"
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        beap_reel_res_fiscal = foyer_fiscal('beap_reel_res_fiscal', period = period)
        beap_reliq_benef_fiscal = foyer_fiscal('beap_reliq_benef_fiscal', period = period)
        beap_monogr = foyer_fiscal('beap_monogr', period = period)
        beap_part_benef_sp = foyer_fiscal('beap_part_benef_sp', period = period)

        return beap_reel_res_fiscal + beap_reliq_benef_fiscal + beap_monogr + beap_part_benef_sp
