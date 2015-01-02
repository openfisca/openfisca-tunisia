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


from openfisca_core.columns import BoolCol, DateCol, EnumCol, IntCol, PeriodSizeIndependentIntCol, StrCol
from openfisca_core.enumerations import Enum

from .. import entities
from .base import build_column, QUIFOY, QUIMEN


CAT = Enum(['rsna', 'rsa', 'rsaa', 'rtns', 'rtte', 're', 'rtfr', 'raic', 'cnrps_sal', 'cnrps_pen'])


# Socio-economic data
# Donnée d'entrée de la simulation à fournir à partir d'une enquète ou
# à générer avec un générateur de cas type
build_column('idmen', IntCol(is_permanent = True))  # 600001, 600002,
build_column('idfoy', IntCol(is_permanent = True))  # idmen + noi du déclarant

build_column('quimen', EnumCol(QUIMEN, is_permanent = True))
build_column('quifoy', EnumCol(QUIFOY, is_permanent = True))

build_column(entities.FoyersFiscaux.name_key, StrCol(entity = 'foy', is_permanent = True,
    label = u"Nom"))
build_column(entities.Individus.name_key, StrCol(is_permanent = True, label = u"Prénom"))
build_column(entities.Menages.name_key, StrCol(entity = 'men', is_permanent = True, label = u"Nom"))

build_column('birth', DateCol(is_permanent = True, label = u"Année de naissance"))
# build_column('age', AgesCol(label = u"âge"))
# build_column('agem', AgesCol(label = u"âge (en mois)"))

build_column('type_sal', EnumCol(CAT, default = 0))

build_column('inv', BoolCol(label = u'invalide'))

build_column('jour_xyz', PeriodSizeIndependentIntCol(default = 360))

build_column('loyer', IntCol(entity = 'men'))  # Loyer mensuel
build_column('activite', PeriodSizeIndependentIntCol())
build_column('boursier', BoolCol())
build_column('code_postal', PeriodSizeIndependentIntCol(entity = 'men'))
build_column('so', PeriodSizeIndependentIntCol())

build_column('statmarit', PeriodSizeIndependentIntCol(default = 2))
build_column('chef', BoolCol())

# BIC Bénéfices industriels et commerciaux
# régime réel
build_column(
    'bic_reel',
    EnumCol(
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
    ),
# Les personnes soumises au régime forfaitaire qui ont cédé le fond de commerce peuvent déclarer l’impôt
# annuel sur le revenu au titre des bénéfices industriels et commerciaux
# sur la base de la différence entre les recettes et les dépenses .
# régime des sociétés de personnes
build_column('bic_sp', BoolCol())

build_column(
    'cadre_legal',
    EnumCol(
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
        )
    ),
build_column('bic_reel_res', IntCol())
build_column('bic_forf_res', IntCol())
build_column('bic_sp_res', IntCol())

build_column(
    'decl_inves',
    EnumCol(
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
    ),

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
build_column('bic_res_fiscal', IntCol(label = u"Résultat fiscal (BIC)"))

# Case réserve aux personnes soumises au régime forfaitaire ayant cédé le fond de commerce
build_column(
    'bic_ca_revente',
    IntCol(
        label = u"Chiffre d’affaires global au titre des activités d’achat en vue de la revente et les activités de transformation"
        )
    ),
build_column('bic_ca_autre', IntCol(label = u"Chiffre d’affaires global au titre d’autres activités"))
build_column('bic_depenses', IntCol(label = u"Total des dépenses (BIC cession de fond de commerce)"))
build_column('bic_pv_cession', IntCol(label = u"Plue-value de cession du fond de commerce"))

# B/ Part dans le bénéfice ou dans la perte des sociétés de personnes
# et assimilées exerçant dans le secteur industriel et commercial
build_column(
    'bic_part_benef_sp',
    IntCol(
        label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant dans le secteur industriel et commercial"
        )
    ),

# BNC Bénéfices des professions non commerciales
# A/ Régime réel
# - Chiffre d’affaires local HT.
# - Chiffre d’affaires à l’exportation
# - Chiffre d’affaires global TTC.
# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi
# - Résultat comptable
# - Résultat fiscal (2) Joindre à la déclaration l'état de détermination du résultat fiscal
build_column('bnc_reel_res_fiscal', IntCol(label = u"Résultat fiscal (BNC)"))

# B/ Détermination du bénéfice sur la base d’une assiette forfaitaire
# - Recettes au titre des services locaux
# - Recettes au titre des services exportés (3) Pour les entreprises totalement exportatrices dans le cadre du CII ou exerçant dans les parcs d’activités économiques.
# - Recettes globales brutes TTC
build_column('bnc_forf_rec_brut', IntCol(label = u"Recettes globales brutes TTC (BNC)"))
# - Montant des primes (1) Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi

# C/ Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées qui réalisent des bénéfices non commerciaux
build_column(
    'bnc_part_benef_sp',
    IntCol(
        label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes qui réalisent des bénéfices non commerciaux"
        )
    ),

# beap Bénéfices de l'exploitation agricole et de pêche
# A/ Régime réel
# - Chiffre d’affaires local
# - Chiffre d’affaires à l’exportation
# - Chiffre d’affaires global
# - Montant des primes  Primes octroyées dans le cadre du CII ou dans le cadre d'encouragement de l'exportation ou dans le cadre d'un programme de mise à niveau approuvé ou dans le cadre des interventions du fonds national de l’emploi.
# - Résultat comptable B = bénéfice P = perte
# - Résultat fiscal  B = bénéfice P = perte
build_column('beap_reel_res_fiscal', IntCol(label = u"Résultat fiscal (BEAP, régime réel)"))

# B/ Détermination du bénéfice sur la base du reliquat positif entre les
# recettes et les dépenses
# - Recettes brutes …………………………..
# - Stocks …………………………..
build_column(
    'beap_reliq_rec',
    IntCol(label = u"Recettes (BEAP, bénéfice comme reliquat entre recette et dépenses")
    ),
build_column(
    'beap_reliq_stock',
    IntCol(label = u"Stocks (BEAP, bénéfice comme reliquat entre recette et dépenses)")
    ),
# TOTAL …………………………..
# - Déduction des dépenses d’exploitation justifiées …………………………..
build_column(
    'beap_reliq_dep_ex',
    IntCol(label = u"Dépenses d’exploitation (BEAP, bénéfice comme reliquat entre recette et dépenses)"))
# - Montant des primes (1) …………………………..
# - Résultat B = bénéfice P = perte …………………………..
# - Bénéfice fiscal (4) …………………………..
build_column(
    'beap_reliq_benef_fiscal',
    IntCol(label = u"Bénéfice fiscal (BEAP)")
    ),
# C/ Détermination du bénéfice sur la base de monographies sectorielles (5)
# - Bénéfice fiscal …………………………..
build_column('beap_monogr', IntCol(label = u"Détermination du bénéfice sur la base de monographies sectorielles (BEAP)"))

# D/ Part dans le bénéfice ou dans la perte des sociétés de personnes et
# assimilées exerçant dans le secteur agricole et de pêche
build_column('beap_part_benef_sp', IntCol(label = u"Part dans le bénéfice ou dans la perte des sociétés de personnes et assimilées exerçant dans le secteur agricole et de pêche"))


# rfon Revenus fonciers
#  régime réel
build_column('fon_reel_fisc', IntCol())

#  régime forfaitaire bâti
build_column('fon_forf_bati_rec', IntCol())
build_column('fon_forf_bati_rel', IntCol())
build_column('fon_forf_bati_fra', IntCol())
build_column('fon_forf_bati_tax', IntCol())

# régime forfaitaire non bâti
build_column('fon_forf_nbat_rec', IntCol())
build_column('fon_forf_nbat_dep', IntCol())
build_column('fon_forf_nbat_tax', IntCol())

#  part dans les bénéfices ou els pertes de sociétés de personnes et assimilées qui réalisent des revenus fonciers
build_column('fon_sp', IntCol())

# Salaires et pensions

build_column('sali', IntCol(label = u"Salaires imposables", default = 0))
build_column('sal_nat', IntCol(label = u"Avantages en nature assimilables à des salaires", default = 0))
build_column('smig_dec', BoolCol(label = u"Salarié déclarant percevoir le SMIG ou le SMAG"))
build_column('pen', IntCol(label = u"Pensions et rentes viagères"))
build_column('pen_nat', IntCol(label = u"Avantages en nature assimilables à des pensions"))


# rvcm Revenus de valeurs mobilières et de capitaux mobiliers
# A Revenus des valeurs mobilières et de capitaux mobiliers
build_column('valm_nreg', IntCol(label = u"Revenus des valeurs mobilières autres que ceux régulièrement distribués"))
build_column('valm_jpres', IntCol(label = u"Jetons de présence"))
build_column('valm_aut', IntCol(label = u"Autres rémunérations assimilées"))

# B Revenus de capitaux mobiliers
build_column('capm_banq', IntCol(label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès des banques"))
build_column('capm_cent', IntCol(label = u"Intérêts bruts des comptes spéciaux d’épargne ouverts auprès de la CENT"))
build_column('capm_caut', IntCol(label = u"Intérêts des créances et intérêts et rémunérations des cautionnements"))
build_column('capm_part', IntCol(label = u"Intérêts des titres de participation"))
build_column('capm_oblig', IntCol(label = u"Intérêts des emprunts obligataires"))
build_column('capm_caisse', IntCol(label = u"Intérêts des bons de caisse"))
build_column('capm_plfcc', IntCol(label = u"Revenus des parts et de liquidation du fonds commun des créances"))
build_column('capm_epinv', IntCol(label = u"Intérêts des comptes épargne pour l'investissement"))
build_column('capm_aut', IntCol(label = u"Autres intérêts"))


# AUtres revenus
build_column('etr_sal', IntCol(label = u"Salaires perçus à l'étranger"))
build_column('etr_pen', IntCol(label = u"Pensions perçues à l'étranger (non transférées)"))
build_column('etr_trans', IntCol(label = u"Pensions perçues à l'étranger (transférées en Tunisie)"))
build_column('etr_aut', IntCol(label = u"Autres revenus perçus à l'étranger"))
# Revnus exonérés
# Revenus non imposables

# deficit antérieurs non déduits
build_column('def_ante', IntCol(label = u"Déficits des années antérieures non déduits"))

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

build_column('deduc_banq', IntCol(label = u"Intérêts des comptes spéciaux d’épargne ouverts auprès des banques"))
build_column('deduc_cent', IntCol(label = u"Intérêts des comptes spéciaux d’épargne ouverts auprès de la CENT dans la limite"))
build_column('deduc_obli', IntCol(label = u"Intérêts des emprunts obligataires"))
build_column('deduc_epinv', IntCol(label = u"Intérêts des comptes épargne pour l'investissement"))
build_column('rente', IntCol(label = u"Rentes payées obligatoirement et à titre gratuit"))
build_column('prime_ass_vie', IntCol(label = u"Prime d’assurance-vie"))
build_column('dons', IntCol(label = u"Dons au profit du fonds national de solidarité 26-26 et du Fonds National de l’Emploi 21-21"))
build_column('pret_univ', IntCol(label = u"Remboursement des prêts universitaires en principal et intérêts"))
build_column('cotis_nonaf', IntCol(label = u"Les cotisations payées par les travailleurs non salariés affiliés à l’un des régimes légaux de la sécurité sociale"))
build_column('deduc_logt', IntCol(label = u"Les intérêts payés au titre des prêts relatifs à l’acquisition ou à la construction d’un logement social"))


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
build_column('rstbrut', IntCol())
build_column('alr', IntCol())
build_column('alv', IntCol())
build_column('rto', IntCol())
build_column('psoc', IntCol())
build_column('af', IntCol())
build_column('uc', IntCol())
