"""4. Revenus fonciers."""


from openfisca_tunisia.variables.base import *  # noqa analysis:ignore


class revenus_fonciers(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus fonciers'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        foncier_reel_resultat_fiscal = foyer_fiscal.declarant_principal('foncier_reel_resultat_fiscal', period = period)
        fon_forf_bati = foyer_fiscal('fon_forf_bati', period = period)
        fon_forf_nbat = foyer_fiscal('fon_forf_nbat', period = period)
        foncier_societes_personnes = foyer_fiscal.declarant_principal('foncier_societes_personnes', period = period)

        return foncier_reel_resultat_fiscal + fon_forf_bati + fon_forf_nbat + foncier_societes_personnes


class fon_forf_bati(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus fonciers net des immeubles bâtis'
    definition_period = YEAR

    def formula(foyer_fiscal, period, parameters):
        foncier_forfaitaire_batis_recettes = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_recettes', period = period)
        # foncier_forfaitaire_batis_reliquat = foyer_fiscal.declarant_principal(
        #     'foncier_forfaitaire_batis_reliquat', period = period)
        foncier_forfaitaire_batis_frais = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_frais', period = period)
        foncier_forfaitaire_batis_taxe = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_batis_taxe', period = period)
        taux_deduction_frais = parameters(period.start).impot_revenu.foncier.bati.deduction_frais
        return max_(
            0,
            foncier_forfaitaire_batis_recettes * (1 - taux_deduction_frais)
            - foncier_forfaitaire_batis_frais
            - foncier_forfaitaire_batis_taxe
            )


class fon_forf_nbat(Variable):
    value_type = float
    entity = FoyerFiscal
    label = 'Revenus fonciers net des terrains non bâtis'
    definition_period = YEAR

    def formula(foyer_fiscal, period):
        foncier_forfaitaire_non_batis_recettes = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_non_batis_recettes', period = period)
        foncier_forfaitaire_non_batis_depenses = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_non_batis_depenses', period = period)
        foncier_forfaitaire_non_batis_taxe = foyer_fiscal.declarant_principal(
            'foncier_forfaitaire_non_batis_taxe', period = period)
        return max_(
            foncier_forfaitaire_non_batis_recettes - foncier_forfaitaire_non_batis_depenses - foncier_forfaitaire_non_batis_taxe,
            0
            )
