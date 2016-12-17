# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *



# BIC Bénéfices industriels et commerciaux
# régime réel


class bic_reel(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Néant",
                u"Commerçant",
                u"Industriel",
                u"Prestataire de services",
                u"Artisan",
                u"Plus d'une activité",
                ]
            )
        )
    entity = Individu


# Les personnes soumises au régime forfaitaire qui ont cédé le fond de commerce peuvent déclarer l’impôt
# annuel sur le revenu au titre des bénéfices industriels et commerciaux
# sur la base de la différence entre les recettes et les dépenses .
# régime des sociétés de personnes


class bic_sp(Variable):
    column = BoolCol()
    entity = Individu


class cadre_legal(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Exportation totale dans le cadre du CII",
                u"Développement régional",
                u"Développement agricole",
                u"Parcs des activités économiques",
                u"Exportation dans le cadre du droit commun",
                u"Autres (à préciser)",
                ],
            start = 1,
            )
        )
    entity = Individu


class bic_reel_res(Variable):
    column = IntCol
    entity = Individu


class bic_forf_res(Variable):
    column = IntCol
    entity = Individu


class bic_sp_res(Variable):
    column = IntCol
    entity = Individu


class decl_inves(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"API",
                u"APIA",
                u"Commissariat régional du développement agricole",
                u"ONT",
                u"Autre structure ( à préciser)"
                ],
            start = 1,
            )
        )
    entity = Individu


# A/ Régime réel
# Valeur du stock au début de l’exercice
# Valeur du stock à la fin de l’exercice
# Valeur des achats au cours de l’exercice
# Chiffre d’affaires local HT.
# Chiffre d’affaires à l’exportation
# Chiffre d’affaires global TTC.
# Chiffre d’affaires provenant des activités de services.
# Montant des primes (5) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'Exportation
# ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions
# du fonds national de l’emploi.
# Résultat comptable
# Résultat fiscal (6) Joindre à la déclaration l’état de détermination du résultat fiscal.


class bic_res_fiscal(Variable):
    column = IntCol
    entity = Individu
    label = u"Résultat fiscal (BIC)"


# Case réserve aux personnes soumises au régime forfaitaire ayant cédé le fond de commerce


class bic_ca_revente(Variable):
    column = IntCol
    entity = Individu
    label = u"Chiffre d’affaires global au titre des activités d’achat en vue de la revente " \
        u"et les activités de transformation"


class bic_ca_autre(Variable):
    column = IntCol
    entity = Individu
    label = u"Chiffre d’affaires global au titre d’autres activités"


class bic_depenses(Variable):
    column = IntCol
    label = u"Total des dépenses (BIC cession de fond de commerce)"
    entity = Individu


class bic_pv_cession(Variable):
    column = IntCol
    entity = Individu
    label = u"Plue-value de cession du fond de commerce"


# B/ Part dans le bénéfice ou dans la perte des sociétés de personnes
# et assimilées exerçant dans le secteur industriel et commercial


class bic_part_benef_sp(Variable):
    column = IntCol
    label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant " \
        u"dans le secteur industriel et commercial"
    entity = Individu


# BNC Bénéfices des professions non commerciales
# A/ Régime réel
# - Chiffre d’affaires local HT.
# - Chiffre d’affaires à l’exportation
# - Chiffre d’affaires global TTC.
# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation
# ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions
# du fonds national de l’emploi
# - Résultat comptable
# - Résultat fiscal (2) Joindre à la déclaration l'état de détermination du résultat fiscal


class bnc_reel_res_fiscal(Variable):
    column = IntCol
    entity = Individu
    label = u"Résultat fiscal (BNC)"


# B/ Détermination du bénéfice sur la base d’une assiette forfaitaire
# - Recettes au titre des services locaux
# - Recettes au titre des services exportés (3) Pour les entreprises totalement exportatrices
# dans le cadre du CII ou exerçant dans les parcs d’activités économiques.
# - Recettes globales brutes TTC


class bnc_forf_rec_brut(Variable):
    column = IntCol
    label = u"Recettes globales brutes TTC (BNC)"
    entity = Individu


# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation
# ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions
# du fonds national de l’emploi

# C/ Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent
# des bénéfices non commerciaux


class bnc_part_benef_sp(Variable):
    column = IntCol
    entity = Individu
    label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes " \
        u"qui réalisent des bénéfices non commerciaux"


# beap Bénéfices de l'exploitation agricole et de pêche
# A/ Régime réel
# - Chiffre d’affaires local
# - Chiffre d’affaires à l’exportation
# - Chiffre d’affaires global
# - Montant des primes  Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation
# ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions
# du fonds national de l’emploi.
# - Résultat comptable B = bénéfice P = perte
# - Résultat fiscal  B = bénéfice P = perte


class beap_reel_res_fiscal(Variable):
    column = IntCol
    label = u"Résultat fiscal (BEAP régime réel)"
    entity = Individu


# B/ Détermination du bénéfice sur la base du reliquat positif entre les
# recettes et les dépenses
# - Recettes brutes …………………………..
# - Stocks …………………………..


class beap_reliq_rec(Variable):
    column = IntCol
    label = u"Recettes (BEAP bénéfice comme reliquat entre recette et dépenses"
    entity = Individu


class beap_reliq_stock(Variable):
    column = IntCol
    label = u"Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)"
    entity = Individu


# TOTAL …………………………..
# - Déduction des dépenses d’exploitation justifiées …………………………..


class beap_reliq_dep_ex(Variable):
    column = IntCol
    label = u"Dépenses d’exploitation (BEAP bénéfice comme reliquat entre recette et dépenses)"
    entity = Individu


# - Montant des primes (1) …………………………..
# - Résultat B = bénéfice P = perte …………………………..
# - Bénéfice fiscal (4) …………………………..


class beap_reliq_benef_fiscal(Variable):
    column = IntCol
    label = u"Bénéfice fiscal (BEAP)"
    entity = Individu


# C/ Détermination du bénéfice sur la base de monographies sectorielles (5)
# - Bénéfice fiscal …………………………..


class beap_monogr(Variable):
    column = IntCol
    label = u"Détermination du bénéfice sur la base de monographies sectorielles (BEAP)"
    entity = Individu

# D/ Part dans le bénéfice ou dans la perte des sociétés de personnes et
# assimilées exerçant dans le secteur agricole et de pêche


class beap_part_benef_sp(Variable):
    column = IntCol
    label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées " \
        u"exerçant dans le secteur agricole et de pêche"
    entity = Individu


# revenus_fonciers Revenus fonciers
#  régime réel


class fon_reel_fisc(Variable):
    column = IntCol
    entity = Individu


#  régime forfaitaire bâti


class fon_forf_bati_rec(Variable):
    column = IntCol
    entity = Individu


class fon_forf_bati_rel(Variable):
    column = IntCol
    entity = Individu


class fon_forf_bati_fra(Variable):
    column = IntCol
    entity = Individu


class fon_forf_bati_tax(Variable):
    column = IntCol
    entity = Individu

# régime forfaitaire non bâti


class fon_forf_nbat_rec(Variable):
    column = IntCol
    entity = Individu


class fon_forf_nbat_dep(Variable):
    column = IntCol
    entity = Individu


class fon_forf_nbat_tax(Variable):
    column = IntCol
    entity = Individu

#  part dans les bénéfices ou les pertes de sociétés de personnes et assimilées qui réalisent des revenus fonciers


class fon_sp(Variable):
    column = IntCol
    entity = Individu


# Salaires et pensions

class salaire_de_base(Variable):
    column = FloatCol
    label = u"Salaire de base"
    entity = Individu


class primes(Variable):
    column = FloatCol
    label = u"Primes"
    entity = Individu


class salaire_en_nature(Variable):
    column = IntCol
    label = u"Avantages en nature assimilables à des salaires"
    entity = Individu


class smig_dec(Variable):
    column = BoolCol
    label = u"Salarié déclarant percevoir le SMIG ou le SMAG"
    entity = Individu


class revenu_assimile_pension(Variable):
    column = IntCol
    label = u"Reenu assimilé à des pensions (pensions et rentes viagères)"
    entity = Individu


class avantages_nature_assimile_pension(Variable):
    column = IntCol
    label = u"Avantages en nature assimilables à des pensions"
    entity = Individu

# rvcm Revenus de valeurs mobilières et de capitaux mobiliers
# A Revenus des valeurs mobilières et de capitaux mobiliers


class valm_nreg(Variable):
    column = IntCol
    label = u"Revenus des valeurs mobilières autres que ceux régulièrement distribués"
    entity = Individu


class valm_jpres(Variable):
    column = IntCol
    label = u"Jetons de présence"
    entity = Individu


class valm_aut(Variable):
    column = IntCol
    label = u"Autres rémunérations assimilées"
    entity = Individu


# B Revenus de capitaux mobiliers


class capm_banq(Variable):
    column = IntCol
    label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès des banques"
    entity = Individu


class capm_cent(Variable):
    column = IntCol
    label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès de la CENT"
    entity = Individu


class capm_caut(Variable):
    column = IntCol
    label = u"Intérêts des créances et intérêts et rémunérations des cautionnements"
    entity = Individu


class capm_part(Variable):
    column = IntCol
    label = u"Intérêts des titres de participation"
    entity = Individu


class capm_oblig(Variable):
    column = IntCol
    label = u"Intérêts des emprunts obligataires"
    entity = Individu


class capm_caisse(Variable):
    column = IntCol
    label = u"Intérêts des bons de caisse"
    entity = Individu


class capm_plfcc(Variable):
    column = IntCol
    label = u"Revenus des parts et de liquidation du fonds commun des créances"
    entity = Individu


class capm_epinv(Variable):
    column = IntCol
    label = u"Intérêts des comptes épargne pour l'investissement"
    entity = Individu


class capm_aut(Variable):
    column = IntCol
    label = u"Autres intérêts"
    entity = Individu

# AUtres revenus


class salaire_etranger(Variable):
    column = IntCol
    label = u"Salaires perçus à l'étranger"
    entity = Individu


class pension_etranger_non_transferee(Variable):
    column = IntCol
    label = u"Pensions perçues à l'étranger (non transférées)"
    entity = Individu


class pension_etranger_transferee(Variable):
    column = IntCol
    label = u"Pensions perçues à l'étranger (transférées en Tunisie)"
    entity = Individu


class autres_revenus_etranger(Variable):
    column = IntCol
    label = u"Autres revenus perçus à l'étranger"
    entity = Individu

# Revnus exonérés
# Revenus non imposables

# deficit antérieurs non déduits


class deficits_anterieurs_non_deduits(Variable):
    column = IntCol
    label = u"Déficits des années antérieures non déduits"
    entity = Individu
