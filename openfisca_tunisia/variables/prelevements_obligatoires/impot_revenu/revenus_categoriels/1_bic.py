'''1. Bénéfices industriels et commerciaux.'''


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class bic(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Bénéfices industriels et commerciaux (BIC)'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bic_reel_res = foyer_fiscal('bic_reel_res', period = period)
        # TODO:
        #    return bic_reel + bic_simpl + bic_forf
        return bic_reel_res

# régime réel
# régime réel simplifié
# régime forfaitaire

class bic_ca_global(Variable):
    value_type = float
    entity = Individu
    label = 'Chiffre d’affaires global (BIC, cession de fond de commerce'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        '''
        Chiffre d’affaires global
        des personnes soumises au régime forfaitaire ayant cédé le fond de commerce
        '''
        bic_ca_revente = foyer_fiscal('bic_ca_revente', period = period)
        bic_ca_autre = foyer_fiscal('bic_ca_autre', period = period)

        return bic_ca_revente + bic_ca_autre


class bic_res_cession(Variable):
    value_type = float
    entity = Individu
    label = 'Résultat (BIC, cession de fond de commerce)'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bic_ca_global = foyer_fiscal('bic_ca_global', period = period)
        bic_depenses = foyer_fiscal('bic_depenses', period = period)

        return max_(bic_ca_global - bic_depenses, 0)


class bic_benef_fiscal_cession(Variable):
    value_type = float
    entity = Individu
    label = 'Bénéfice fiscal (BIC, cession de fond de commerce)'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        bic_res_cession = foyer_fiscal('bic_res_cession', period = period)
        bic_pv_cession = foyer_fiscal('bic_pv_cession', period = period)
        return bic_res_cession + bic_pv_cession


def _bic_res_net(bic_benef_fiscal_cession, bic_part_benef_sp):
    '''
    Résultat net BIC TODO: il manque le régime réel
    '''
    return bic_benef_fiscal_cession + bic_part_benef_sp
