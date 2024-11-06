'''2. Bénéfices des professions non commerciales'''


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class bnc(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Bénéfices des professions non commerciales (BNC)'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bnc_reel_res_fiscal = foyer_fiscal.sum(
            foyer_fiscal.members('bnc_reel_res_fiscal', period = period)
            )
        bnc_forf_benef_fiscal = foyer_fiscal.sum(
            foyer_fiscal.members('bnc_forf_benef_fiscal', period = period)
            )
        bnc_part_benef_sp = foyer_fiscal.sum(
            foyer_fiscal.members('bnc_part_benef_sp', period = period)
            )
        return bnc_reel_res_fiscal + bnc_forf_benef_fiscal + bnc_part_benef_sp


class bnc_forf_benef_fiscal(Variable):
    value_type = float
    entity = Individu
    label = 'Bénéfice fiscal (régime forfaitaire en % des recettes brutes TTC)'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        '''
        Bénéfice fiscal (régime forfaitaire, en % des recettes brutes TTC)
        '''
        bnc_forfaitaire_recettes_brutes = foyer_fiscal('bnc_forfaitaire_recettes_brutes', period = period)
        part = parameters(period.start).impot_revenu.bnc.forf.part_forf
        return bnc_forfaitaire_recettes_brutes * part
