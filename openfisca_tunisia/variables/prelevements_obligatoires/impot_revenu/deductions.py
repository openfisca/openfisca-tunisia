from openfisca_tunisia.variables.base import *

# déductions

# 1/ Au titre de l'activité
#
#    Droit commun
# - Déduction de la plus value provenant de l’apport d’actions et de parts sociales au capital de la société mère ou de
#   la société holding 6811
# - Déduction de la plus value provenant de la cession des entreprises en difficultés économiques dans le cadre de la
#   transmission des entreprises 6881
# - Déduction de la plus value provenant de la cession des entreprises suite à l’atteinte du propriétaire de l’âge de la
#   retraite ou à l’incapacité de poursuivre la gestion de l’entreprise dans le cadre de la transmission des
#   entreprises. 6891
# - Déduction de la plus value provenant de l'intégration des éléments d'actifs. 6851
# - Déduction de la plus value provenant de la cession des actions cotées en bourse 6841
# - Bénéfices provenant des opérations de courtage international 1141
# - Exportation 1191
# - Location d’immeubles au profit des étudiants 1211 1212 1213
# - Bénéfices provenant des services de restauration au profit des étudiants, des élèves et des apprenants dans les
#   centres de formation professionnelle de base. 1221 1222 1223
# - Bénéfices provenant de la location des constructions verticales destinées à l’habitat collectif social ou
#   économique. 1251
# - Bénéfices provenant de l’exploitation des bureaux d’encadrement et d’assistance fiscale 1311
# - Bénéfices réinvestis dans le capital des sociétés qui commercialisent exclusivement des marchandises ou services
#   tunisiens 1132
# - Bénéfices réinvestis dans les SICAR ou placés auprès d'elles dans des fonds de capital à risque ou dans des fonds
#   de placement à risque qui se conforment aux exigences de l'article 21 de la loi n°: 88-92 relative au sociétés
#   d'investissement. 6872
# - Bénéfices réinvestis dans les SICAR ou placés auprès d'elles dans des fonds de capital à risque ou dans des fonds
#   de placement à risque qui utilisent 75% au moins de leur capital libéré et des montants mis à sa disposition et de
#   leurs actifs dans le financement des projets implantés dans les zones de développement.
# 6842
# - Revenus et bénéfices placés dans les fonds d’amorçage
# 1432
# - Montants déposés dans les comptes épargne pour l’investissement dans la limite de 20000 D
# 1412
# - Montants déposés dans les comptes épargne en actions dans la limite de 20000 D
# 1422
# - Bénéfices réinvestis pour l’acquisition d’entreprises ou de titres cédés suite à l’atteinte du propriétaire de l’âge
#   de la retraite ou à son incapacité de poursuivre la gestion de l’entreprise
# 1512
# - Bénéfices réinvestis pour l’acquisition d’entreprises cédées dans le cadre de cession d’entreprises en difficultés
#   économiques dans le cadre de la loi n° 34 de l'année 1995.
# 1522

#     2/ Autres déductions


class compte_special_epargne_banque(Variable):
    value_type = int
    label = "Intérêts des comptes spéciaux d'épargne ouverts auprès des banques"
    entity = Individu
    definition_period = YEAR


class compte_special_epargne_cent(Variable):
    value_type = int
    label = "Intérêts des comptes spéciaux d'épargne ouverts auprès de la CENT dans la limite"
    entity = Individu
    definition_period = YEAR


class emprunt_obligataire(Variable):
    value_type = int
    label = 'Intérêts des emprunts obligataires'
    entity = Individu
    definition_period = YEAR


class compte_epargne_investissement(Variable):
    value_type = int
    label = "Intérêts des comptes épargne pour l'investissement"
    entity = Individu
    definition_period = YEAR


class rente(Variable):
    value_type = int
    label = 'Rentes payées obligatoirement et à titre gratuit'
    entity = Individu
    definition_period = YEAR


class prime_assurance_vie(Variable):
    value_type = int
    label = 'Prime d’assurance-vie'
    entity = Individu
    definition_period = YEAR


class dons(Variable):
    value_type = int
    label = 'Dons au profit du fonds national de solidarité 26-26 et du Fonds National de l’Emploi 21-21'
    entity = Individu
    definition_period = YEAR


class pret_universitaire(Variable):
    value_type = int
    label = 'Remboursement des prêts universitaires en principal et intérêts'
    entity = Individu
    definition_period = YEAR


class cotisations_non_affilie(Variable):
    value_type = int
    label = "Cotisations payées par les travailleurs non salariés affiliés à l'un des régimes légaux de la sécurité sociale"
    entity = Individu
    definition_period = YEAR


class interet_acquisition_logement(Variable):
    value_type = int
    label = "Intérêts payés au titre des prêts relatifs à l'acquisition ou à la construction d’un logement social"
    entity = Individu
    definition_period = YEAR


# Code d’incitation aux investissements
# Incitations Communes 3::3
# Bénéfices réinvestis dans l'acquisition des éléments d'actif d'une société ou dans l'acquisition ou la souscription
# d'actions ou de parts permettant de posséder 50% au moins du capital d'une société 2982
# Déduction de 20% des revenus et bénéfices soumis à l'impôt sur le revenu de la part des entreprises dont le chiffre
# d’affaires annuel ne dépasse pas 150 milles dinars pour les activités de services et 300 milles dinars pour les autres
# activités sans dépasser un chiffre d’affaires annuel de 300 milles dinars qui confient la tenue de leurs comptes et la
# préparation de leurs déclarations fiscales aux centres de
# gestion intégrés. (1) 2971
# Exportation totale (pendant la période de la déduction totale). 3222 3223
# Investissement au capital des sociétés de commerce international totalement exportateur. 2172
# Déduction des bénéfices provenant de la gestion d'une zone portuaire destinée au tourisme de croisière (pendant les
# dix premières années à partir de la date d'entrée en activité effective) 2151
# Déduction des bénéfices provenant de la gestion d'une zone portuaire destinée au tourisme de croisière (à partir de
# la onzième année de la date d'entrée en activité effective) 2161
# Déduction des bénéfices réinvestis dans l'acquisition des éléments d'actif d'une société totalement exportatrice ou
# dans l'acquisition d'actions ou de parts permettant de posséder 50% au moins du capital d'une société totalement
# exportatrice dans le cadre de la loi n° 34 de l'année 1995. 2142
# Exportation partielle. 3232
# Développement régional: le premier groupe 3461 3463
# Développement régional: le deuxième groupe 2371 2372
# Développement régional prioritaire pendant les dix premières années à partir de la date d'entrée en activité effective
#  ( 2) 2391 2392
# Développement régional prioritaire pendant les dix années qui suivent des dix premières années à partir de la date
# d'entrée en activité effective ( 2) 2381 2382
# Déduction des bénéfices réinvestis dans l'acquisition des éléments d'actif des sociétés exerçant dans les zones
# d'encouragement au développement régional ou dans l'acquisition ou la souscription d'actions ou de parts permettant
# de posséder 50% au moins du capital de ces sociétés dans le cadre de la loi n° 34 de l'année 1995. 2352
# Travaux publics et promotion immobilière dans la zone de développement régional . 3422
# Développement agricole 35:2 35:3
# Investissements agricoles réalisés dans les régions à climat difficile ainsi que les investissements de pêche dans
# les zones insuffisamment exploitées 3523
# Lutte contre la pollution 38:2 38:3
# Activités de soutien 33:2 33:3
# Bénéfices provenant de projets réalisés par les promoteurs immobiliers concernant les programmes de logements sociaux
# et de réaménagement des zones d’activités agricoles, touristiques, industrielles et les bâtiments pour les activités
# industrielles.
# 36:2
# Sociétés implantées dans les parcs des activités économiques
# 4262 4263
# Bénéfices et revenus réinvestis dans le cadre de la mise à niveau des entreprises publiques.
#
