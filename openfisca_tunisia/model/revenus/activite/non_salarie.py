# -*- coding: utf-8 -*-

from openfisca_tunisia.model.base import *


# BIC Bénéfices industriels et commerciaux
# régime réel


class TypesActivite(Enum):
    neant = "Néant"
    commercant = "Commerçant"
    industriel = "Industriel"
    prestataire_de_services = "Prestataire de services"
    artisan = "Artisan"
    multi_activites = "Plus d'une activité"


class TypesCadreLegalActiviteEntreprise(Enum):
    exportation_totale = "Exportation totale dans le cadre du Code d'Incitations aux Investissements (CII)"
    developpement_regional = "Développement régional"
    developpement_agricole = "Développement agricole"
    parcs_activites_economiques = "Parcs des activités économiques"
    exportation_droit_commun = "Exportation dans le cadre du droit commun"
    autres = "Autres (à préciser)"


class TypesStructureDeclarationInvestissement(Enum):
    api = "Agence de Promotion de l'Industrie et de l'Innovation"
    apia = "Agence de Promotion des Investissements Agricoles"
    commissariat_regional_developpement_agricole = "Commissariat régional du développement agricole"
    ont = "ONT"
    autres = "Autre structure (à préciser)"


class bic_reel(Variable):
    value_type = Enum
    possible_values = TypesActivite
    default_value = TypesActivite.neant
    entity = Individu
    label = "Type d’activité (BIC)"
    definition_period = YEAR


# Les personnes soumises au régime forfaitaire qui ont cédé le fond de commerce peuvent déclarer l’impôt
# annuel sur le revenu au titre des bénéfices industriels et commerciaux
# sur la base de la différence entre les recettes et les dépenses .
# régime des sociétés de personnes


class bic_societes_personnes(Variable):
    value_type = bool
    entity = Individu
    label = "Indicatrice des sociétés de personnes et assimilées (BIC)"
    definition_period = YEAR


class cadre_legal(Variable):
    value_type = Enum
    default_value = TypesCadreLegalActiviteEntreprise.developpement_regional  # Développement régional
    possible_values = TypesCadreLegalActiviteEntreprise
    entity = Individu
    label = "Cadre légal de l’activité de l’entreprise"
    definition_period = YEAR


class bic_reel_res(Variable):
    value_type = int
    entity = Individu
    label = "Résultat comptable (BIC, régime réel)"
    definition_period = YEAR


class bic_forfaitaire_resultat(Variable):
    value_type = int
    entity = Individu
    label = "Résultat (BIC, régime forfaitaire, cession de fonds de commerce)"
    definition_period = YEAR


class bic_societes_personnes_resultat(Variable):
    value_type = int
    entity = Individu
    label = "Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées " \
        "exerçant dans le secteur industriel et commercial (BIC)"
    definition_period = YEAR


class structure_declaration_investissement(Variable):
    value_type = Enum
    possible_values = TypesStructureDeclarationInvestissement
    default_value = TypesStructureDeclarationInvestissement.api
    entity = Individu
    label = "Structure auprès de laquelle la déclaration d’investissement a été déposée"
    definition_period = YEAR


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
    value_type = int
    entity = Individu
    label = "Résultat fiscal (BIC, régime réel)"
    definition_period = YEAR


# Case réserve aux personnes soumises au régime forfaitaire ayant cédé le fond de commerce


class bic_ca_revente(Variable):
    value_type = int
    entity = Individu
    label = "Chiffre d’affaires global au titre des activités d’achat en vue de la revente " \
        "et les activités de transformation (BIC, régime forfaitaire, cession de fonds de commerce)"
    definition_period = YEAR


class bic_ca_autre(Variable):
    value_type = int
    entity = Individu
    label = "Chiffre d’affaires global au titre d’autres activités (BIC, régime forfaitaire, cession de fonds de commerce)"
    definition_period = YEAR


class bic_depenses(Variable):
    value_type = int
    label = "Total des dépenses (BIC, cession de fonds de commerce)"
    entity = Individu
    definition_period = YEAR


class bic_pv_cession(Variable):
    value_type = int
    entity = Individu
    label = "Plue-value de cession du fond de commerce (BIC, régime forfaitaire, cession de fonds de commerce)"
    definition_period = YEAR


# B/ Part dans le bénéfice ou dans la perte des sociétés de personnes
# et assimilées exerçant dans le secteur industriel et commercial


class bic_part_benef_sp(Variable):
    value_type = int
    label = "Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant " \
        "dans le secteur industriel et commercial"
    entity = Individu
    definition_period = YEAR


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
    value_type = int
    entity = Individu
    label = "Résultat fiscal (BNC, régime réel)"
    definition_period = YEAR


# B/ Détermination du bénéfice sur la base d’une assiette forfaitaire
# - Recettes au titre des services locaux
# - Recettes au titre des services exportés (3) Pour les entreprises totalement exportatrices
# dans le cadre du CII ou exerçant dans les parcs d’activités économiques.
# - Recettes globales brutes TTC


class bnc_forfaitaire_recettes_brutes(Variable):
    value_type = int
    label = "Recettes globales brutes TTC (BNC, assiette forfaitaire)"
    entity = Individu
    definition_period = YEAR


# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation
# ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions
# du fonds national de l’emploi

# C/ Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent
# des bénéfices non commerciaux


class bnc_part_benef_sp(Variable):
    value_type = int
    entity = Individu
    label = "Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées" \
        "qui réalisent des bénéfices non commerciaux (BNC)"
    definition_period = YEAR


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
    value_type = int
    label = "Résultat fiscal (BEAP, régime réel)"
    entity = Individu
    definition_period = YEAR

# B/ Détermination du bénéfice sur la base du reliquat positif entre les
# recettes et les dépenses
# - Recettes brutes …………………………..
# - Stocks …………………………..


class beap_reliq_rec(Variable):
    value_type = int
    label = "Recettes brutes (BEAP, bénéfice comme reliquat positif entre recette et dépenses)"
    entity = Individu
    definition_period = YEAR

class beap_reliq_stock(Variable):
    value_type = int
    label = "Stocks (BEAP, bénéfice comme reliquat positif entre recette et dépenses)"
    entity = Individu
    definition_period = YEAR

# TOTAL …………………………..
# - Déduction des dépenses d’exploitation justifiées …………………………..


class beap_reliq_dep_ex(Variable):
    value_type = int
    label = "Dépenses d’exploitation (BEAP, bénéfice comme reliquat positif entre recette et dépenses)"
    entity = Individu
    definition_period = YEAR

# - Montant des primes (1) …………………………..
# - Résultat B = bénéfice P = perte …………………………..
# - Bénéfice fiscal (4) …………………………..


class beap_reliq_benef_fiscal(Variable):
    value_type = int
    label = "Bénéfice fiscal (BEAP, bénéfice comme reliquat positif entre recette et dépenses)"
    entity = Individu
    definition_period = YEAR

# C/ Détermination du bénéfice sur la base de monographies sectorielles (5)
# - Bénéfice fiscal …………………………..


class beap_monogr(Variable):
    value_type = int
    label = "Bénéfice sur la base de monographies sectorielles (BEAP)"
    entity = Individu
    definition_period = YEAR
# D/ Part dans le bénéfice ou dans la perte des sociétés de personnes et
# assimilées exerçant dans le secteur agricole et de pêche


class beap_part_benef_sp(Variable):
    value_type = int
    label = "Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées " \
        "exerçant dans le secteur agricole et de pêche (BEAP)"
    entity = Individu
    definition_period = YEAR
