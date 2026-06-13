# Évolution Historique des Taux de Cotisation CNSS (Secteur Privé - RSNA)

Ce document retrace les recherches effectuées concernant l'évolution des taux de cotisations de la Caisse Nationale de Sécurité Sociale (CNSS) en Tunisie, afin de guider les futures implémentations historiques dans OpenFisca-Tunisia.

## 1. Évolution du Taux Global (Employeur + Salarié)
Les textes et rapports (notamment de l'ITCEQ) montrent que le taux global de cotisation a connu des augmentations successives majeures pour financer les équilibres des caisses :
- **1985** : 12.00% (5% salarial / 7% patronal)
- **1995** : 14.20%
- **2011** : 20.70%
- **2021** : 23.70%
- **2024** : 25.75% (9.18% salarial / 16.57% patronal)
- **2025** : 26.75% (+0.5% salarial / +0.5% patronal pour le Fonds de Perte d'Emploi)

## 2. Le défi de la répartition par branche (Problème OpenFisca)
Dans `openfisca_tunisia`, le taux global n'est pas utilisé directement. Le système calcule la cotisation par "branches" :
- Maladie
- Maternité
- Accidents du travail
- Allocations familiales
- **Vieillesse, invalidité, survivants (Retraite)**
- etc.

Actuellement, le taux de la branche Retraite est fixé à **12.5%** (4.74% salarial / 7.76% patronal).

**Problématique :** Sur internet, les documents vulgarisés ou les résumés de lois de finances annoncent généralement la hausse du *Taux Global*. Il est très difficile de trouver comment ce taux de 12.5% a évolué au cours du temps (était-il de 8% en 1985 ? de 10% en 1995 ?). L'information publique actuelle (depuis 2011/2023) confirme que les 12.5% n'ont pas bougé récemment, mais pour coder un historique juste sur 40 ans, il faudra sourcer la ventilation exacte.

## 3. Pistes recommandées pour la suite
Pour modéliser parfaitement la CNSS il faudrait :
1. Consulter les archives du **JORT (Journal Officiel de la République Tunisienne)** des années 1985, 1995 et 2011.
2. Rechercher les décrets spécifiques d'application qui fixaient la répartition interne du taux de sécurité sociale à chaque fois que le taux global a été modifié par une loi de finances.
3. Alternativement : demander à un expert comptable ou à la CNSS un tableau récapitulatif de la ventilation historique des taux (ce type de document n'est pas indexé publiquement sur le web).
