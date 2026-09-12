# Audit sources retraite OpenFisca Tunisia Pension

Généré le 2026-09-12 par `scripts/generate_pension_source_audit.py`.

## Synthèse

- Fichiers paramètres retraite: 66
- Paramètres avec valeurs ou barèmes: 53
- Paramètres avec référence: 49 / 53
- Paramètres sans référence: 4 / 53
- Paramètres multi-dates: 19
- Textes JORT locaux: 1

## Couverture par régime

| Régime | Paramètres avec valeurs |
| --- | ---: |
| `cnrps` | 38 |
| `rsa` | 7 |
| `rsna` | 8 |

## Textes cités dans les références

| Texte | Occurrences paramètres | Statut |
| --- | ---: | --- |
| `1959-18` - Loi n° 59-18 du 5 février 1959, pensions civiles et militaires | 9 | JORT 1959/8, texte pivot |
| `1974-499` - Texte cité par les paramètres | 8 | JORT 1974/39 |
| `1981-6` - Loi n° 81-6 du 12 février 1981, sécurité sociale secteur agricole | 5 | JORT 1981/26, texte pivot |
| `1981-70` - Texte cité par les paramètres | 6 | JORT 1981/51 |
| `1982-1030` - Texte cité par les paramètres | 6 | JORT 1982/66 |
| `1985-1178` - Texte cité par les paramètres | 2 | JORT 1985/68 |
| `1985-12` - Loi n° 85-12 du 5 mars 1985, pensions civiles et militaires secteur public | 23 | JORT 1985/20, texte pivot |
| `1986-611` - Texte cité par les paramètres | 4 | JORT 1986/34 |
| `1988-1136` - Texte cité par les paramètres | 3 | JORT 1988/43 |
| `1988-39` - Texte cité par les paramètres | 1 | JORT 1988/33 |
| `1988-71` - Texte cité par les paramètres | 1 | JORT 1988/45 |
| `1993-308` - Texte cité par les paramètres | 4 | JORT 1993/13 |
| `1996-1906` - Texte cité par les paramètres | 4 | JORT 1996/85 |
| `2007-43` - Loi n° 2007-43 du 25 juin 2007, pensions public/privé/régimes spéciaux | 2 | texte local, JORT 2007/51, texte pivot |
| `2009-20` - Texte cité par les paramètres | 1 | JORT 2009/100 |
| `2019-37` - Loi n° 2019-37 du 30 avril 2019, relèvement âge retraite | 4 | JORT 2019/35, texte pivot |

## Textes JORT locaux

| Fichier | Lois détectées | Articles détectés |
| --- | --- | --- |
| `tmp/JORTs/Loi-n°-2007-43-du-25-Juin-2007-Fr.txt` | `2007-43`; cite `1983-31`, `1985-12`, `1985-16`, `1988-16` | premier, 2, 30 (nouveau), 37 (nouveau), 46 (nouveau), 47 (nouveau), 3, 4, 5 |

## Paramètres sans référence

| Paramètre | Description | Dates |
| --- | --- | --- |
| `retraite.cnrps.bonifications.militaire.bonus` | Bonification maximum pour militaires | 1985-03-05 |
| `retraite.cnrps.depart_anticipe.meres_3_enfants.age_minimum` | Âge minimum de jouissance de la pension pour les mères de 3 enfants | 1985-03-05 |
| `retraite.rsa.pension_min` | Pension minimale (en part de SMAG) | 1981-01-01 |
| `retraite.rsa.periode_remplacement_base` | Période de remplacement de base | 1981-01-01 |

## Paramètres multi-dates à relier finement

| Paramètre | Dates | Lois citées |
| --- | --- | --- |
| `retraite.cnrps.accessoires.indemnites_familiales.rang_1` | 1986-05-01, 1989-01-01, 1996-11-01 | `1986-611`, `1988-1136`, `1996-1906` |
| `retraite.cnrps.accessoires.indemnites_familiales.rang_2` | 1986-05-01, 1989-01-01, 1996-11-01 | `1986-611`, `1988-1136`, `1996-1906` |
| `retraite.cnrps.accessoires.indemnites_familiales.rang_3` | 1986-05-01, 1989-01-01, 1996-11-01 | `1986-611`, `1988-1136`, `1996-1906` |
| `retraite.cnrps.accessoires.indemnites_familiales.rang_4_et_plus` | 1986-05-01, 1989-01-01, 1996-11-01 | `1986-611`, `1988-39`, `1996-1906` |
| `retraite.cnrps.age_legal.civil.cadre_commun` | 1959-02-01, 2019-07-01, 2020-01-01 | `1959-18`, `1985-12`, `2019-37` |
| `retraite.cnrps.age_legal.civil.cadres_actifs` | 1959-02-01, 2019-07-01, 2020-01-01 | `1959-18`, `1985-12`, `2019-37` |
| `retraite.cnrps.age_legal.civil.fonctions_astreignantes` | 1985-09-12, 2019-07-01, 2020-01-01 | `1985-12`, `2019-37` |
| `retraite.cnrps.age_legal.civil.ouvriers_travaux_penibles` | 1985-09-12, 2019-07-01, 2020-01-01 | `1985-12`, `2019-37` |
| `retraite.cnrps.bareme_annuite` | 1959-02-01, 1985-09-12 | `1959-18`, `1985-12` |
| `retraite.cnrps.depart_anticipe.meres_3_enfants.age_maximum_enfant` | 1985-09-12, 1989-01-01 | `1985-12`, `1988-71` |
| `retraite.cnrps.depart_anticipe.sur_demande.cadre_commun.age_minimum` | 1985-09-12, 2007-07-01 | `1985-12`, `2007-43` |
| `retraite.cnrps.depart_anticipe.sur_demande.cadre_commun.duree_minimum` | 1985-09-12, 2007-07-01 | `1985-12`, `2007-43` |
| `retraite.cnrps.pension_minimale.minimum_garanti` | 1981-05-01, 1985-09-12 | `1959-18`, `1981-70`, `1985-12` |
| `retraite.cnrps.plaf_taux_pension` | 1981-05-01, 1985-09-12 | `1959-18`, `1981-70`, `1985-12` |
| `retraite.cnrps.survivants.taux_conjoint` | 1981-05-01, 1985-09-12 | `1959-18`, `1981-70`, `1985-12` |
| `retraite.rsna.bareme_annuite` | 1974-01-01, 1982-07-22 | `1974-499`, `1982-1030` |
| `retraite.rsna.pension_minimale.sup` | 1974-01-01, 1982-07-22 | `1974-499`, `1982-1030` |
| `retraite.rsna.plaf_taux_pension` | 1974-01-01, 1982-07-22 | `1974-499`, `1982-1030` |
| `retraite.rsna.stage_derog` | 1974-01-01, 1982-07-22 | `1974-499`, `1982-1030` |

## Accès aux paramètres depuis les variables

| Fichier | Paramètres retraite accédés |
| --- | --- |
| `accessoires_formulas.py` | `retraite.cnrps.accessoires.indemnites_familiales` |
| `cnrps.py` | `retraite.cnrps`, `retraite.cnrps.bareme_annuite` |
| `rsa.py` | `retraite.rsa`, `retraite.rsa.bareme_annuite` |
| `rsna.py` | `retraite.rsna`, `retraite.rsna.bareme_annuite` |
| `survivants.py` | `retraite.cnrps.capital_deces`, `retraite.cnrps.survivants` |

## Recommandations

- Ajouter des références aux paramètres RSA et aux accessoires/pensions minimales avant toute correction de valeur.
- Promouvoir le texte `2007-43` depuis `tmp/JORTs` vers un emplacement de sources documenté si le dépôt doit conserver les textes pivots.
- Résoudre prioritairement les textes `1959-18`, `1960-33`, `1981-6`, `1985-12` et `2019-37` dans le cache JORT ou dans le corpus législatif externe.
- Traiter les paramètres multi-dates avec une référence par date d'effet, car les dates OpenFisca ne coïncident pas toujours avec la date de signature du texte.
