# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from .base import *  # reference_input_variable, QUIFOY, QUIMEN


CAT = Enum(['rsna', 'rsa', 'rsaa', 'rtns', 'rtte', 're', 'rtfr', 'raic', 'cnrps_sal', 'cnrps_pen'])


# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type
reference_input_variable(
    name = 'idmen',
    column = IntCol(is_permanent = True),
    entity_class = Individus,
    )  # 600001, 600002,
reference_input_variable(
    name = 'idfoy',
    column = IntCol(is_permanent = True),
    entity_class = Individus,
    )  # idmen + noi du déclarant
reference_input_variable(
    name = 'quimen',
    column = EnumCol(QUIMEN, is_permanent = True),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'quifoy',
    column = EnumCol(QUIFOY, is_permanent = True),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'birth',
    column = DateCol(is_permanent = True),
    entity_class = Individus,
    label = u"Année de naissance"
    )
reference_input_variable(
    name = 'type_sal',
    column = EnumCol(CAT, default = 0),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'inv',
    column = BoolCol(label = u'invalide'),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'jour_xyz',
    column = PeriodSizeIndependentIntCol(default = 360),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'loyer',
    column = IntCol(),
    entity_class = Menages,
    )  # Loyer mensuel
reference_input_variable(
    name = 'activite',
    column = PeriodSizeIndependentIntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'boursier',
    column = BoolCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'code_postal',
    column = PeriodSizeIndependentIntCol(),
    entity_class = Menages,
    )
reference_input_variable(
    name = 'so',
    column = PeriodSizeIndependentIntCol(),
    entity_class = Menages,
    )
reference_input_variable(
    name = 'statmarit',
    column = PeriodSizeIndependentIntCol(default = 2),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'chef',
    column = BoolCol(),
    entity_class = Individus,
    )
# BIC Bénéfices industriels et commerciaux
# régime réel
reference_input_variable(
    name = 'bic_reel',
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
        ),
    entity_class = Individus,
    )
# Les personnes soumises au régime forfaitaire qui ont cédé le fond de commerce peuvent déclarer l’impôt
# annuel sur le revenu au titre des bénéfices industriels et commerciaux
# sur la base de la différence entre les recettes et les dépenses .
# régime des sociétés de personnes
reference_input_variable(
    name = 'bic_sp',
    column = BoolCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'cadre_legal',
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
            start = 1)
        ),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'bic_reel_res',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'bic_forf_res',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'bic_sp_res',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'decl_inves',
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
        ),
    entity_class = Individus,
    )
# A/ Régime réel
# Valeur du stock au début de l’exercice
# Valeur du stock à la fin de l’exercice
# Valeur des achats au cours de l’exercice
# Chiffre d’affaires local HT.
# Chiffre d’affaires à l’exportation
# Chiffre d’affaires global TTC.
# Chiffre d’affaires provenant des activités de services.
# Montant des primes (5) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi.
# Résultat comptable
# Résultat fiscal (6) Joindre à la déclaration l’état de détermination du résultat fiscal.
reference_input_variable(
    name = 'bic_res_fiscal',
    column = IntCol(label = u"Résultat fiscal (BIC)"),
    entity_class = Individus,
    )
# Case réserve aux personnes soumises au régime forfaitaire ayant cédé le fond de commerce
reference_input_variable(
    name = 'bic_ca_revente',
    column = IntCol(
        label = u"Chiffre d’affaires global au titre des activités d’achat en vue de la revente et les activités de transformation"
        ),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'bic_ca_autre',
    column = IntCol(label = u"Chiffre d’affaires global au titre d’autres activités"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'bic_depenses',
    column = IntCol(label = u"Total des dépenses (BIC cession de fond de commerce)"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'bic_pv_cession',
    column = IntCol(label = u"Plue-value de cession du fond de commerce"),
    entity_class = Individus,
    )
# B/ Part dans le bénéfice ou dans la perte des sociétés de personnes
# et assimilées exerçant dans le secteur industriel et commercial
reference_input_variable(
    name = 'bic_part_benef_sp',
    column = IntCol(
        label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant dans le secteur industriel et commercial"
        ),
    entity_class = Individus,
    )
# BNC Bénéfices des professions non commerciales
# A/ Régime réel
# - Chiffre d’affaires local HT.
# - Chiffre d’affaires à l’exportation
# - Chiffre d’affaires global TTC.
# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi
# - Résultat comptable
# - Résultat fiscal (2) Joindre à la déclaration l'état de détermination du résultat fiscal
reference_input_variable(
    name = 'bnc_reel_res_fiscal',
    column = IntCol(label = u"Résultat fiscal (BNC)"),
    entity_class = Individus,
    )
# B/ Détermination du bénéfice sur la base d’une assiette forfaitaire
# - Recettes au titre des services locaux
# - Recettes au titre des services exportés (3) Pour les entreprises totalement exportatrices dans le cadre du CII ou exerçant dans les parcs d’activités économiques.
# - Recettes globales brutes TTC
reference_input_variable(
    name = 'bnc_forf_rec_brut',
    column = IntCol(label = u"Recettes globales brutes TTC (BNC)"),
    entity_class = Individus,
    )
# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi

# C/ Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent des bénéfices non commerciaux
reference_input_variable(
    name = 'bnc_part_benef_sp',
    column = IntCol(
        label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes qui réalisent des bénéfices non commerciaux"
        ),
    entity_class = Individus,
    ),
# beap Bénéfices de l'exploitation agricole et de pêche
# A/ Régime réel
# - Chiffre d’affaires local
# - Chiffre d’affaires à l’exportation
# - Chiffre d’affaires global
# - Montant des primes  Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi.
# - Résultat comptable B = bénéfice P = perte
# - Résultat fiscal  B = bénéfice P = perte
reference_input_variable(
    name = 'beap_reel_res_fiscal',
    column = IntCol(label = u"Résultat fiscal (BEAP, régime réel)"),
    entity_class = Individus,
    )
# B/ Détermination du bénéfice sur la base du reliquat positif entre les
# recettes et les dépenses
# - Recettes brutes …………………………..
# - Stocks …………………………..
reference_input_variable(
    name = 'beap_reliq_rec',
    column = IntCol(label = u"Recettes (BEAP, bénéfice comme reliquat entre recette et dépenses"),
    entity_class = Individus,
    ),
reference_input_variable(
    name = 'beap_reliq_stock',
    column = IntCol(),
    label = u"Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)",
    entity_class = Individus,
    ),
# TOTAL …………………………..
# - Déduction des dépenses d’exploitation justifiées …………………………..
reference_input_variable(
    name = 'beap_reliq_dep_ex',
    column = IntCol(label = u"Dépenses d’exploitation (BEAP, bénéfice comme reliquat entre recette et dépenses)"),
    entity_class = Individus,
    )
# - Montant des primes (1) …………………………..
# - Résultat B = bénéfice P = perte …………………………..
# - Bénéfice fiscal (4) …………………………..
reference_input_variable(
    name = 'beap_reliq_benef_fiscal',
    column = IntCol(label = u"Bénéfice fiscal (BEAP)"),
    entity_class = Individus,
    ),
# C/ Détermination du bénéfice sur la base de monographies sectorielles (5)
# - Bénéfice fiscal …………………………..
reference_input_variable(
    name = 'beap_monogr',
    column = IntCol(label = u"Détermination du bénéfice sur la base de monographies sectorielles (BEAP)"),
    entity_class = Individus,
    )
# D/ Part dans le bénéfice ou dans la perte des sociétés de personnes et
# assimilées exerçant dans le secteur agricole et de pêche
reference_input_variable(
    name = 'beap_part_benef_sp',
    column = IntCol(label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant dans le secteur agricole et de pêche"),
    entity_class = Individus,
    )
# rfon Revenus fonciers
#  régime réel
reference_input_variable(
    name = 'fon_reel_fisc',
    column = IntCol(),
    entity_class = Individus,
    )
#  régime forfaitaire bâti
reference_input_variable(
    name = 'fon_forf_bati_rec',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'fon_forf_bati_rel',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'fon_forf_bati_fra',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'fon_forf_bati_tax',
    column = IntCol(),
    entity_class = Individus,
    )
# régime forfaitaire non bâti
reference_input_variable(
    name = 'fon_forf_nbat_rec',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'fon_forf_nbat_dep',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'fon_forf_nbat_tax',
    column = IntCol(),
    entity_class = Individus,
    )
#  part dans les bénéfices ou els pertes de sociétés de personnes et assimilées qui réalisent des revenus fonciers
reference_input_variable(
    name = 'fon_sp',
    column = IntCol(),
    entity_class = Individus,
    )
# Salaires et pensions

reference_input_variable(
    name = 'sali',
    column = IntCol(label = u"Salaires imposables", default = 0),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'sal_nat',
    column = IntCol(label = u"Avantages en nature assimilables à des salaires", default = 0),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'smig_dec',
    column = BoolCol(label = u"Salarié déclarant percevoir le SMIG ou le SMAG"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'pen',
    column = IntCol(label = u"Pensions et rentes viagères"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'pen_nat',
    column = IntCol(label = u"Avantages en nature assimilables à des pensions"),
    entity_class = Individus,
    )
# rvcm Revenus de valeurs mobilières et de capitaux mobiliers
# A Revenus des valeurs mobilières et de capitaux mobiliers
reference_input_variable(
    name = 'valm_nreg',
    column = IntCol(label = u"Revenus des valeurs mobilières autres que ceux régulièrement distribués"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'valm_jpres',
    column = IntCol(label = u"Jetons de présence"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'valm_aut',
    column = IntCol(label = u"Autres rémunérations assimilées"),
    entity_class = Individus,
    )
# B Revenus de capitaux mobiliers
reference_input_variable(
    name = 'capm_banq',
    column = IntCol(label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès des banques"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_cent',
    column = IntCol(label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès de la CENT"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_caut',
    column = IntCol(label = u"Intérêts des créances et intérêts et rémunérations des cautionnements"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_part',
    column = IntCol(label = u"Intérêts des titres de participation"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_oblig',
    column = IntCol(label = u"Intérêts des emprunts obligataires"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_caisse',
    column = IntCol(label = u"Intérêts des bons de caisse"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_plfcc',
    column = IntCol(label = u"Revenus des parts et de liquidation du fonds commun des créances"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_epinv',
    column = IntCol(label = u"Intérêts des comptes épargne pour l'investissement"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'capm_aut',
    column = IntCol(label = u"Autres intérêts"),
    entity_class = Individus,
    )
# AUtres revenus
reference_input_variable(
    name = 'etr_sal',
    column = IntCol(label = u"Salaires perçus à l'étranger"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'etr_pen',
    column = IntCol(label = u"Pensions perçues à l'étranger (non transférées)"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'etr_trans',
    column = IntCol(label = u"Pensions perçues à l'étranger (transférées en Tunisie)"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'etr_aut',
    column = IntCol(label = u"Autres revenus perçus à l'étranger"),
    entity_class = Individus,
    )
# Revnus exonérés
# Revenus non imposables

# deficit antérieurs non déduits
reference_input_variable(
    name = 'def_ante',
    column = IntCol(label = u"Déficits des années antérieures non déduits"),
    entity_class = Individus,
    )

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

reference_input_variable(
    name = 'deduc_banq',
    column = IntCol(label = u"Intérêts des comptes spéciaux d’épargne ouverts auprès des banques"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'deduc_cent',
    column = IntCol(label = u"Intérêts des comptes spéciaux d’épargne ouverts auprès de la CENT dans la limite"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'deduc_obli',
    column = IntCol(label = u"Intérêts des emprunts obligataires"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'deduc_epinv',
    column = IntCol(label = u"Intérêts des comptes épargne pour l'investissement"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'rente',
    column = IntCol(label = u"Rentes payées obligatoirement et à titre gratuit"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'prime_ass_vie',
    column = IntCol(label = u"Prime d’assurance-vie"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'dons',
    column = IntCol(label = u"Dons au profit du fonds national de solidarité 26-26 et du Fonds National de l’Emploi 21-21"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'pret_univ',
    column = IntCol(label = u"Remboursement des prêts universitaires en principal et intérêts"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'cotis_nonaf',
    column = IntCol(label = u"Les cotisations payées par les travailleurs non salariés affiliés à l’un des régimes légaux de la sécurité sociale"),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'deduc_logt',
    column = IntCol(label = u"Les intérêts payés au titre des prêts relatifs à l’acquisition ou à la construction d’un logement social"),
    entity_class = Individus,
    )


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
reference_input_variable(
    name = 'rstbrut',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'alr',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'alv',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'rto',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'psoc',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'af',
    column = IntCol(),
    entity_class = Individus,
    )
reference_input_variable(
    name = 'uc',
    column = IntCol(),
    entity_class = Individus,
    )
