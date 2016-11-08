# -*- coding: utf-8 -*-


from openfisca_tunisia.model.base import *


CAT = Enum(['rsna', 'rsa', 'rsaa', 'rtns', 'rtte', 're', 'rtfr', 'raic', 'cnrps_sal', 'cnrps_pen'])


# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type


class idmen(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    # 600001, 600002,


class idfoy(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    # idmen + noi du déclarant


class quimen(Variable):
    column = EnumCol(QUIMEN, is_permanent = True)
    entity_class = Individus


class quifoy(Variable):
    column = EnumCol(QUIFOY, is_permanent = True)
    entity_class = Individus


class date_naissance(Variable):
    column = DateCol(is_permanent = True)
    entity_class = Individus
    label = u"Année de naissance"


class categorie_salarie(Variable):
    column = EnumCol(CAT, default = 0)
    entity_class = Individus


class inv(Variable):
    column = BoolCol
    label = u'invalide'
    entity_class = Individus


class jour_xyz(Variable):
    column = PeriodSizeIndependentIntCol(default = 360)
    entity_class = Individus


class loyer(Variable):
    column = IntCol
    entity_class = Menages
    # Loyer mensuel


class activite(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Individus


class boursier(Variable):
    column = BoolCol()
    entity_class = Individus


class code_postal(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Menages


class so(Variable):
    column = PeriodSizeIndependentIntCol
    entity_class = Menages


class statut_marital(Variable):
    column = PeriodSizeIndependentIntCol(default = 2)
    entity_class = Individus


class chef(Variable):
    column = BoolCol()
    entity_class = Individus

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
    entity_class = Individus


# Les personnes soumises au régime forfaitaire qui ont cédé le fond de commerce peuvent déclarer l’impôt
# annuel sur le revenu au titre des bénéfices industriels et commerciaux
# sur la base de la différence entre les recettes et les dépenses .
# régime des sociétés de personnes


class bic_sp(Variable):
    column = BoolCol()
    entity_class = Individus


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
    entity_class = Individus


class bic_reel_res(Variable):
    column = IntCol
    entity_class = Individus


class bic_forf_res(Variable):
    column = IntCol
    entity_class = Individus


class bic_sp_res(Variable):
    column = IntCol
    entity_class = Individus


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
    entity_class = Individus


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
    entity_class = Individus
    label = u"Résultat fiscal (BIC)"


# Case réserve aux personnes soumises au régime forfaitaire ayant cédé le fond de commerce


class bic_ca_revente(Variable):
    column = IntCol
    entity_class = Individus
    label = u"Chiffre d’affaires global au titre des activités d’achat en vue de la revente " \
        u"et les activités de transformation"


class bic_ca_autre(Variable):
    column = IntCol
    entity_class = Individus
    label = u"Chiffre d’affaires global au titre d’autres activités"


class bic_depenses(Variable):
    column = IntCol
    label = u"Total des dépenses (BIC cession de fond de commerce)"
    entity_class = Individus


class bic_pv_cession(Variable):
    column = IntCol
    entity_class = Individus
    label = u"Plue-value de cession du fond de commerce"


# B/ Part dans le bénéfice ou dans la perte des sociétés de personnes
# et assimilées exerçant dans le secteur industriel et commercial


class bic_part_benef_sp(Variable):
    column = IntCol
    label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant " \
        u"dans le secteur industriel et commercial"
    entity_class = Individus


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
    entity_class = Individus
    label = u"Résultat fiscal (BNC)"


# B/ Détermination du bénéfice sur la base d’une assiette forfaitaire
# - Recettes au titre des services locaux
# - Recettes au titre des services exportés (3) Pour les entreprises totalement exportatrices
# dans le cadre du CII ou exerçant dans les parcs d’activités économiques.
# - Recettes globales brutes TTC


class bnc_forf_rec_brut(Variable):
    column = IntCol
    label = u"Recettes globales brutes TTC (BNC)"
    entity_class = Individus


# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation
# ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions
# du fonds national de l’emploi

# C/ Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent
# des bénéfices non commerciaux


class bnc_part_benef_sp(Variable):
    column = IntCol
    entity_class = Individus
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
    entity_class = Individus


# B/ Détermination du bénéfice sur la base du reliquat positif entre les
# recettes et les dépenses
# - Recettes brutes …………………………..
# - Stocks …………………………..


class beap_reliq_rec(Variable):
    column = IntCol
    label = u"Recettes (BEAP bénéfice comme reliquat entre recette et dépenses"
    entity_class = Individus


class beap_reliq_stock(Variable):
    column = IntCol
    label = u"Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)"
    entity_class = Individus


# TOTAL …………………………..
# - Déduction des dépenses d’exploitation justifiées …………………………..


class beap_reliq_dep_ex(Variable):
    column = IntCol
    label = u"Dépenses d’exploitation (BEAP bénéfice comme reliquat entre recette et dépenses)"
    entity_class = Individus


# - Montant des primes (1) …………………………..
# - Résultat B = bénéfice P = perte …………………………..
# - Bénéfice fiscal (4) …………………………..


class beap_reliq_benef_fiscal(Variable):
    column = IntCol
    label = u"Bénéfice fiscal (BEAP)"
    entity_class = Individus


# C/ Détermination du bénéfice sur la base de monographies sectorielles (5)
# - Bénéfice fiscal …………………………..


class beap_monogr(Variable):
    column = IntCol
    label = u"Détermination du bénéfice sur la base de monographies sectorielles (BEAP)"
    entity_class = Individus

# D/ Part dans le bénéfice ou dans la perte des sociétés de personnes et
# assimilées exerçant dans le secteur agricole et de pêche


class beap_part_benef_sp(Variable):
    column = IntCol
    label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées " \
        u"exerçant dans le secteur agricole et de pêche"
    entity_class = Individus


# revenus_fonciers Revenus fonciers
#  régime réel


class fon_reel_fisc(Variable):
    column = IntCol
    entity_class = Individus


#  régime forfaitaire bâti


class fon_forf_bati_rec(Variable):
    column = IntCol
    entity_class = Individus


class fon_forf_bati_rel(Variable):
    column = IntCol
    entity_class = Individus


class fon_forf_bati_fra(Variable):
    column = IntCol
    entity_class = Individus


class fon_forf_bati_tax(Variable):
    column = IntCol
    entity_class = Individus

# régime forfaitaire non bâti


class fon_forf_nbat_rec(Variable):
    column = IntCol
    entity_class = Individus


class fon_forf_nbat_dep(Variable):
    column = IntCol
    entity_class = Individus


class fon_forf_nbat_tax(Variable):
    column = IntCol
    entity_class = Individus

#  part dans les bénéfices ou els pertes de sociétés de personnes et assimilées qui réalisent des revenus fonciers


class fon_sp(Variable):
    column = IntCol
    entity_class = Individus

# Salaires et pensions


class salaire_imposable(Variable):
    column = IntCol
    label = u"Salaires imposables"
    entity_class = Individus


class sal_nat(Variable):
    column = IntCol
    label = u"Avantages en nature assimilables à des salaires"
    entity_class = Individus


class smig_dec(Variable):
    column = BoolCol
    label = u"Salarié déclarant percevoir le SMIG ou le SMAG"
    entity_class = Individus


class revenu_assimile_pension(Variable):
    column = IntCol
    label = u"Reenu assimilé à des pensions (pensions et rentes viagères)"
    entity_class = Individus


class avantages_nature_assimile_pension(Variable):
    column = IntCol
    label = u"Avantages en nature assimilables à des pensions"
    entity_class = Individus

# rvcm Revenus de valeurs mobilières et de capitaux mobiliers
# A Revenus des valeurs mobilières et de capitaux mobiliers


class valm_nreg(Variable):
    column = IntCol
    label = u"Revenus des valeurs mobilières autres que ceux régulièrement distribués"
    entity_class = Individus


class valm_jpres(Variable):
    column = IntCol
    label = u"Jetons de présence"
    entity_class = Individus


class valm_aut(Variable):
    column = IntCol
    label = u"Autres rémunérations assimilées"
    entity_class = Individus


# B Revenus de capitaux mobiliers


class capm_banq(Variable):
    column = IntCol
    label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès des banques"
    entity_class = Individus


class capm_cent(Variable):
    column = IntCol
    label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès de la CENT"
    entity_class = Individus


class capm_caut(Variable):
    column = IntCol
    label = u"Intérêts des créances et intérêts et rémunérations des cautionnements"
    entity_class = Individus


class capm_part(Variable):
    column = IntCol
    label = u"Intérêts des titres de participation"
    entity_class = Individus


class capm_oblig(Variable):
    column = IntCol
    label = u"Intérêts des emprunts obligataires"
    entity_class = Individus


class capm_caisse(Variable):
    column = IntCol
    label = u"Intérêts des bons de caisse"
    entity_class = Individus


class capm_plfcc(Variable):
    column = IntCol
    label = u"Revenus des parts et de liquidation du fonds commun des créances"
    entity_class = Individus


class capm_epinv(Variable):
    column = IntCol
    label = u"Intérêts des comptes épargne pour l'investissement"
    entity_class = Individus


class capm_aut(Variable):
    column = IntCol
    label = u"Autres intérêts"
    entity_class = Individus

# AUtres revenus


class etr_sal(Variable):
    column = IntCol
    label = u"Salaires perçus à l'étranger"
    entity_class = Individus


class etr_pen(Variable):
    column = IntCol
    label = u"Pensions perçues à l'étranger (non transférées)"
    entity_class = Individus


class etr_trans(Variable):
    column = IntCol
    label = u"Pensions perçues à l'étranger (transférées en Tunisie)"
    entity_class = Individus


class etr_aut(Variable):
    column = IntCol
    label = u"Autres revenus perçus à l'étranger"
    entity_class = Individus

# Revnus exonérés
# Revenus non imposables

# deficit antérieurs non déduits


class def_ante(Variable):
    column = IntCol
    label = u"Déficits des années antérieures non déduits"
    entity_class = Individus


# déductions

# 1/ Au titre de l'activité
#
#    Droit commun
# - Déduction de la plus value provenant de l’apport d’actions et de parts sociales au capital de la société mère ou de la société holding 6811
# - Déduction de la plus value provenant de la cession des entreprises en difficultés économiques dans le cadre de la transmission des entreprises 6881
# - Déduction de la plus value provenant de la cession des entreprises suite à l’atteinte du propriétaire de l’âge de la retraite ou à l’incapacité de poursuivre la gestion de l’entreprise dans le cadre de la transmission des entreprises. 6891
# - Déduction de la plus value provenant de l'intégration des éléments d'actifs. 6851
# - Déduction de la plus value provenant de la cession des actions cotées en bourse 6841
# - Bénéfices provenant des opérations de courtage international 1141
# - Exportation 1191
# - Location d’immeubles au profit des étudiants 1211 1212 1213
# - Bénéfices provenant des services de restauration au profit des étudiants, des élèves et des apprenants dans les centres de formation professionnelle de base. 1221 1222 1223
# - Bénéfices provenant de la location des constructions verticales destinées à l’habitat collectif social ou économique. 1251
# - Bénéfices provenant de l’exploitation des bureaux d’encadrement et d’assistance fiscale 1311
# - Bénéfices réinvestis dans le capital des sociétés qui commercialisent exclusivement des marchandises ou services tunisiens 1132
# - Bénéfices réinvestis dans les SICAR ou placés auprès d'elles dans des fonds de capital à risque ou dans des fonds de placement à risque qui se conforment aux exigences de l'article 21 de la loi n°: 88-92 relative au sociétés d'investissement. 6872
# - Bénéfices réinvestis dans les SICAR ou placés auprès d'elles dans des fonds de capital à risque ou dans des fonds de placement à risque qui utilisent 75% au moins de leur capital libéré et des montants mis à sa disposition et de leurs actifs dans le financement des projets implantés dans les zones de développement.
# 6842
# - Revenus et bénéfices placés dans les fonds d’amorçage
# 1432
# - Montants déposés dans les comptes épargne pour l’investissement dans la limite de 20000 D
# 1412
# - Montants déposés dans les comptes épargne en actions dans la limite de 20000 D
# 1422
# - Bénéfices réinvestis pour l’acquisition d’entreprises ou de titres cédés suite à l’atteinte du propriétaire de l’âge de la retraite ou à son incapacité de poursuivre la gestion de l’entreprise
# 1512
# - Bénéfices réinvestis pour l’acquisition d’entreprises cédées dans le cadre de cession d’entreprises en difficultés économiques dans le cadre de la loi n° 34 de l'année 1995.
# 1522

#     2/ Autres déductions


class deduc_banq(Variable):
    column = IntCol
    label = u"Intérêts des comptes spéciaux d’épargne ouverts auprès des banques"
    entity_class = Individus


class deduc_cent(Variable):
    column = IntCol
    label = u"Intérêts des comptes spéciaux d’épargne ouverts auprès de la CENT dans la limite"
    entity_class = Individus


class deduc_obli(Variable):
    column = IntCol
    label = u"Intérêts des emprunts obligataires"
    entity_class = Individus


class deduc_epinv(Variable):
    column = IntCol
    label = u"Intérêts des comptes épargne pour l'investissement"
    entity_class = Individus


class rente(Variable):
    column = IntCol
    label = u"Rentes payées obligatoirement et à titre gratuit"
    entity_class = Individus


class prime_ass_vie(Variable):
    column = IntCol
    label = u"Prime d’assurance-vie"
    entity_class = Individus


class dons(Variable):
    column = IntCol
    label = u"Dons au profit du fonds national de solidarité 26-26 et du Fonds National de l’Emploi 21-21"
    entity_class = Individus


class pret_univ(Variable):
    column = IntCol
    label = u"Remboursement des prêts universitaires en principal et intérêts"
    entity_class = Individus


class cotis_nonaf(Variable):
    column = IntCol
    label = u"Les cotisations payées par les travailleurs non salariés affiliés à l’un des régimes légaux " \
        u"de la sécurité sociale"
    entity_class = Individus


class deduc_logt(Variable):
    column = IntCol
    label = u"Les intérêts payés au titre des prêts relatifs à l’acquisition ou à la construction d’un logement social"
    entity_class = Individus


# Code d’incitation aux investissements
# Incitations Communes 3::3
# Bénéfices réinvestis dans l'acquisition des éléments d'actif d'une société ou dans l'acquisition ou la souscription d'actions ou de parts permettant de posséder 50% au moins du capital d'une société 2982
# Déduction de 20% des revenus et bénéfices soumis à l'impôt sur le revenu de la part des entreprises dont le chiffre d’affaires annuel ne dépasse pas 150 milles dinars pour les activités de services et 300 milles dinars pour les autres activités sans dépasser un chiffre d’affaires annuel de 300 milles dinars qui confient la tenue de leurs comptes et la préparation de leurs déclarations fiscales aux centres de gestion intégrés. (1) 2971
# Exportation totale (pendant la période de la déduction totale). 3222 3223
# Investissement au capital des sociétés de commerce international totalement exportateur. 2172
# Déduction des bénéfices provenant de la gestion d'une zone portuaire destinée au tourisme de croisière (pendant les dix premières années à partir de la date d'entrée en activité effective) 2151
# Déduction des bénéfices provenant de la gestion d'une zone portuaire destinée au tourisme de croisière (à partir de la onzième année de la date d'entrée en activité effective) 2161
# Déduction des bénéfices réinvestis dans l'acquisition des éléments d'actif d'une société totalement exportatrice ou dans l'acquisition d'actions ou de parts permettant de posséder 50% au moins du capital d'une société totalement exportatrice dans le cadre de la loi n° 34 de l'année 1995. 2142
# Exportation partielle. 3232
# Développement régional: le premier groupe 3461 3463
# Développement régional: le deuxième groupe 2371 2372
# Développement régional prioritaire pendant les dix premières années à partir de la date d'entrée en activité effective ( 2) 2391 2392
# Développement régional prioritaire pendant les dix années qui suivent des dix premières années à partir de la date d'entrée en activité effective ( 2) 2381 2382
# Déduction des bénéfices réinvestis dans l'acquisition des éléments d'actif des sociétés exerçant dans les zones d'encouragement au développement régional ou dans l'acquisition ou la souscription d'actions ou de parts permettant de posséder 50% au moins du capital de ces sociétés dans le cadre de la loi n° 34 de l'année 1995. 2352
# Travaux publics et promotion immobilière dans la zone de développement régional . 3422
# Développement agricole 35:2 35:3
# Investissements agricoles réalisés dans les régions à climat difficile ainsi que les investissements de pêche dans les zones insuffisamment exploitées 3523
# Lutte contre la pollution 38:2 38:3
# Activités de soutien 33:2 33:3
# Bénéfices provenant de projets réalisés par les promoteurs immobiliers concernant les programmes de logements sociaux et de réaménagement des zones d’activités agricoles, touristiques, industrielles et les bâtiments pour les activités industrielles.
# 36:2
# Sociétés implantées dans les parcs des activités économiques
# 4262 4263
# Bénéfices et revenus réinvestis dans le cadre de la mise à niveau des entreprises publiques.
#


# TODO Remove Me


class rstbrut(Variable):
    column = IntCol
    entity_class = Individus


class alr(Variable):
    column = IntCol
    entity_class = Individus


class alv(Variable):
    column = IntCol
    entity_class = Individus


class rto(Variable):
    column = IntCol
    entity_class = Individus


class psoc(Variable):
    column = IntCol
    entity_class = Individus


class uc(Variable):
    column = IntCol
    entity_class = Individus
