# Audit des sources des paramètres d'OpenFisca-Tunisia

Généré le 2026-09-12 par `scripts/generate_source_audit.py`, en 7.2 s.

Ce rapport mesure, par sous-arbre, ce que les paramètres disent de leur fondement juridique : combien portent une valeur, combien une référence, de quelle qualité est cette référence, et si le texte cité se retrouve dans le corpus du JORT.

## Ce que compte ce rapport

Un *fichier* de paramètres porte souvent plusieurs *paramètres* : `fonction_publique/.../traitement_de_base.yaml` n'a pas de valeur à sa racine, mais un `echelon_N` par échelon, chacun avec ses valeurs et sa référence. Les deux unités sont donc comptées séparément, et les colonnes le disent. Les `index.yaml`, qui ne portent que l'ordre d'affichage, sont exclus : c'est l'écart avec un `grep` naïf sur l'arborescence, qui en compte trois portant un champ `reference` et un lien `pist.tn`.

## Fichiers non chargés ou mal nommés

Ces fichiers sont dans l'arborescence mais **hors de l'arbre chargé** : OpenFisca ne lit que les `.yaml` et `.yml`.

| Fichier | Lignes | Motif | `.yaml` voisin ? |
| --- | ---: | --- | --- |
| `prelevements_sociaux/cotisations_sociales/secteur_public/regimes_speciaux/gouvernement_deputes_gouverneurs/cotisations_employeur/retraite` | 129 | sans extension `.yaml` : OpenFisca ne le lit pas | **non** |
| `prelevements_sociaux/cotisations_sociales/secteur_public/regimes_speciaux/gouvernement_deputes_gouverneurs/cotisations_salarie/retraite` | 112 | sans extension `.yaml` : OpenFisca ne le lit pas | **non** |

Ces fichiers sont chargés, mais leur nom contient un caractère que l'accès pointé ne sait pas franchir : le paramètre existe et reste inatteignable par `parameters(period).<chemin>`.

| Fichier | Paramètre | Caractères impropres | Portée |
| --- | --- | --- | --- |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/installation_de menuiserie_bois_métallique_et_serrurerie.yaml` | `prelevements_sociaux.atmp.activites_annexes_du_btp.installation_de menuiserie_bois_métallique_et_serrurerie` | ` `, `é` | **inatteignable** en accès pointé |
| `prelevements_sociaux/atmp/construction_et_reparation navale.yaml` | `prelevements_sociaux.atmp.construction_et_reparation navale` | ` ` | **inatteignable** en accès pointé |
| `prelevements_sociaux/atmp/industries_chimiques/fabrication_produits_minéraux_divers.yaml` | `prelevements_sociaux.atmp.industries_chimiques.fabrication_produits_minéraux_divers` | `é` | identifiant non ASCII |
| `prelevements_sociaux/atmp/location_de_la main_d_oeuvre_pour_les_services_administratifs.yaml` | `prelevements_sociaux.atmp.location_de_la main_d_oeuvre_pour_les_services_administratifs` | ` ` | **inatteignable** en accès pointé |

## Synthèse par sous-arbre

| Sous-arbre | Fichiers | Paramètres avec valeur | dont référencés | dont URL JORT | dont sans rien |
| --- | ---: | ---: | ---: | ---: | ---: |
| `energie` | 9 | 9 | 2 | 0 | 7 |
| `fiscalite_indirecte` | 30 | 30 | 0 | 0 | 30 |
| `fonction_publique` | 1258 | 28744 | 23294 | 0 | 5450 |
| `impot_revenu` | 44 | 44 | 30 | 16 | 14 |
| `marche_travail` | 14 | 14 | 14 | 14 | 0 |
| `prelevements_sociaux` | 151 | 151 | 68 | 57 | 83 |
| `prestations` | 41 | 41 | 41 | 26 | 0 |
| `produits_subventionnes` | 10 | 10 | 0 | 0 | 10 |
| `**Ensemble**` | 1557 | 29043 | 23449 | 113 | 5594 |

La colonne « URL JORT » ne compte que les liens vers `www.pist.tn`, le fascicule officiel. Un paramètre est dit référencé s'il porte une référence propre ou s'il en hérite d'un nœud de son fichier.

## Niveaux de référence

| Niveau | Fichiers | Paramètres avec valeur |
| --- | ---: | ---: |
| Porte un champ `reference` | 1177 | 23449 |
| Référence **structurée** (dictionnaire, non chaîne libre) | – | 23447 |
| … dont **titre et lien** | – | 127 |
| … dont **titre seul, sans lien** | – | 23320 |
| Référence en **chaîne libre** | – | 2 |
| Référence **datée** (indexée par date de valeur) | – | 23444 |
| Référence **globale** (non datée) | – | 5 |
| Lien **pist.tn** | 113 | 113 |
| Lien **gitlab.com** (non probant) | 12 | 12 |

Autres hôtes cités : `jibaya.tn` (3), `www.finances.gov.tn` (2), `www.ijtimaia.tn` (1), `www.legislation.tn` (3).

La datation n'est presque jamais discriminante : la convention du dépôt indexe la référence par date de valeur. Le contrôle instructif est l'inverse — les dates de valeur **qu'aucune référence ne couvre** ; il est en section « Anomalies ».

## Paramètres sans aucune référence

5594 paramètres portent une valeur sans qu'aucune référence, propre ou héritée, ne la fonde. Regroupés par fichier, le plus fourni en tête, vingt fichiers par sous-arbre au plus.

### `fonction_publique` — 5450 paramètres dans 237 fichiers

| Fichier | Paramètres sans référence |
| --- | ---: |
| `fonction_publique/agents_affaires_economiques/agent_constatation_affaires_economiques/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_affaires_economiques/attache_inspection_affaires_economiques/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_affaires_economiques/controleur_affaires_economiques/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_affaires_economiques/inspecteur_affaires_economiques/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_affaires_economiques/inspecteur_central_affaires_economiques/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_affaires_economiques/prepose_affaires_economiques/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_services_douaniers/caporal_adjoint_des_douanes/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_services_douaniers/lieutenant_des_douanes/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_services_douaniers/lieutenant_major_des_douanes/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_services_douaniers/sergent_des_douanes_echelle_1/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_services_douaniers/sergent_major_des_douanes_echelle_1/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/agents_services_douaniers/sous_lieutenant_des_douanes/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/animateurs_des_jardins_d_enfants/animateur_hors_classe_des_jardins_d_enfants/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/animateurs_des_jardins_d_enfants/animateur_principal_des_jardins_d_enfants/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/animateurs_des_jardins_d_enfants/animateur_principal_emerite_des_jardins_d_enfants/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/animateurs_des_jardins_d_enfants/animateur_principal_hors_classe_des_jardins_d_enfants/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/cadres_communs_de_laboratoire/chef_de_laboratoire/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/cadres_communs_de_laboratoire/chef_des_travaux_adjoint_de_laboratoire/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/cadres_communs_de_laboratoire/chef_des_travaux_de_laboratoire/indemnite_specifique_mensuelle.yaml` | 25 |
| `fonction_publique/cadres_des_metiers_du_sport/manager_conseiller_en_sport/indemnite_specifique_mensuelle.yaml` | 25 |
| _…et 217 autres fichiers_ | 4950 |

### `prelevements_sociaux` — 83 paramètres dans 83 fichiers

| Fichier | Paramètres sans référence |
| --- | ---: |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/autres_travaux_installation_et_finition.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/installation_de menuiserie_bois_métallique_et_serrurerie.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/installation_electrique.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/plomberie_et_installation_equipements_thermiques_et_climatisation.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/realisation_charpentes_et_couvertures.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_annexes_du_btp/travaux_peinture_et_vitrerie.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_liees_aux_constructions_et_reparations_navales.yaml` | 1 |
| `prelevements_sociaux/atmp/activites_sportives.yaml` | 1 |
| `prelevements_sociaux/atmp/agence_de_voyage/categorie_a.yaml` | 1 |
| `prelevements_sociaux/atmp/agence_de_voyage/categorie_b.yaml` | 1 |
| `prelevements_sociaux/atmp/agriculture_et_peche.yaml` | 1 |
| `prelevements_sociaux/atmp/auto_ecole.yaml` | 1 |
| `prelevements_sociaux/atmp/autres_industries_manufacturieres.yaml` | 1 |
| `prelevements_sociaux/atmp/autres_services.yaml` | 1 |
| `prelevements_sociaux/atmp/batiment_et_travaux_publics.yaml` | 1 |
| `prelevements_sociaux/atmp/commerce/commerce_de_detail.yaml` | 1 |
| `prelevements_sociaux/atmp/commerce/commerce_de_gros.yaml` | 1 |
| `prelevements_sociaux/atmp/concessionnaires_automobiles/avec_atelier_de_reparation.yaml` | 1 |
| `prelevements_sociaux/atmp/concessionnaires_automobiles/sans_atelier_de_reparation.yaml` | 1 |
| `prelevements_sociaux/atmp/construction_et_reparation navale.yaml` | 1 |
| _…et 63 autres fichiers_ | 63 |

### `fiscalite_indirecte` — 30 paramètres dans 30 fichiers

| Fichier | Paramètres sans référence |
| --- | ---: |
| `fiscalite_indirecte/accises/alcool/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/alcool/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_100pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_100pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_10pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_10pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_135pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_135pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_25pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_25pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_2pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_2pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_7pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/autres/taux_7pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/boissons/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/boissons/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/cafe_the/taux_10pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/cafe_the/taux_10pct/taux.yaml` | 1 |
| `fiscalite_indirecte/accises/cafe_the/taux_25pct/produits.yaml` | 1 |
| `fiscalite_indirecte/accises/cafe_the/taux_25pct/taux.yaml` | 1 |
| _…et 10 autres fichiers_ | 10 |

### `impot_revenu` — 14 paramètres dans 14 fichiers

| Fichier | Paramètres sans référence |
| --- | ---: |
| `impot_revenu/bic/forf/acc.yaml` | 1 |
| `impot_revenu/bic/forf/bareme.yaml` | 1 |
| `impot_revenu/bic/forf/forfait.yaml` | 1 |
| `impot_revenu/bic/reel/forfait.yaml` | 1 |
| `impot_revenu/bic/simpl/forfait.yaml` | 1 |
| `impot_revenu/contribution_budget_etat.yaml` | 1 |
| `impot_revenu/deductions/cea_cei/cei.yaml` | 1 |
| `impot_revenu/deductions/famille/age.yaml` | 1 |
| `impot_revenu/deductions/famille/age_sup.yaml` | 1 |
| `impot_revenu/deductions/famille/parent_taux.yaml` | 1 |
| `impot_revenu/deductions/interets_comptes_epargne_investissement/plaf.yaml` | 1 |
| `impot_revenu/deductions/interets_comptes_speciaux_epargne_cent/plaf.yaml` | 1 |
| `impot_revenu/tspr/abat_sal.yaml` | 1 |
| `impot_revenu/tspr/smig_ext.yaml` | 1 |

### `produits_subventionnes` — 10 paramètres dans 10 fichiers

| Fichier | Paramètres sans référence |
| --- | ---: |
| `produits_subventionnes/baguette.yaml` | 1 |
| `produits_subventionnes/couscous.yaml` | 1 |
| `produits_subventionnes/farine.yaml` | 1 |
| `produits_subventionnes/gros_pain.yaml` | 1 |
| `produits_subventionnes/huile.yaml` | 1 |
| `produits_subventionnes/lait_demi_ecreme_bouteille.yaml` | 1 |
| `produits_subventionnes/lait_demi_ecreme_uht.yaml` | 1 |
| `produits_subventionnes/pate.yaml` | 1 |
| `produits_subventionnes/semoule.yaml` | 1 |
| `produits_subventionnes/sucre.yaml` | 1 |

### `energie` — 7 paramètres dans 7 fichiers

| Fichier | Paramètres sans référence |
| --- | ---: |
| `energie/electricite/cout_fixe.yaml` | 1 |
| `energie/electricite/reduction_puissance.yaml` | 1 |
| `energie/electricite/taxe_fte.yaml` | 1 |
| `energie/gaz/cout_fixe.yaml` | 1 |
| `energie/gaz/prix.yaml` | 1 |
| `energie/gaz/reduction_puissance.yaml` | 1 |
| `energie/gaz/taxe_fte.yaml` | 1 |

## Textes cités et leur résolution dans le corpus JORT

| Texte cité | Type cité | Occurrences | Résolution |
| --- | --- | ---: | --- |
| `1959-18` | loi | 2 | JORT 1959/8 du 1959-02-03 (Loi du 1959-02-05) |
| `1960-30` | loi | 20 | JORT 1960/57 du 1960-12-13 (Loi du 1960-12-14) |
| `1961-145` | decret | 4 | JORT 1961/12 du 1961-03-28 (Decret du 1961-03-30) |
| `1962-73` | loi | 2 | JORT 1962/64 du 1962-12-28 (Loi du 1962-12-31) |
| `1965-46` | loi | 2 | JORT 1965/66 du 1965-12-31 (Loi du 1965-12-31) |
| `1965-561` | decret | 4 | JORT 1965/66 du 1965-12-31 (Decret du 1965-12-31) |
| `1968-113` | decret | 1 | JORT 1968/18 du 1968-04-30 (Decret du 1968-04-30) |
| `1968-97` | decret | 4 | JORT 1968/16 du 1968-04-16 (Decret du 1968-04-15) |
| `1969-344` | decret | 1 | JORT 1969/38 du 1969-09-26 (Decret du 1969-09-27) |
| `1971-163` | decret | 1 | JORT 1971/20 du 1971-04-30 (Decret du 1971-05-03) |
| `1971-164` | decret | 4 | JORT 1971/20 du 1971-04-30 (Decret du 1971-05-03) |
| `1973-91` | decret | 1 | JORT 1973/10 du 1973-03-09 (Decret du 1973-03-12) |
| `1974-101` | loi | 3 | JORT 1974/80 du 1974-12-31 (Loi du 1974-12-25) |
| `1974-499` | decret | 4 | JORT 1974/30 du 1974-04-30 (Decret du 1974-04-27) |
| `1974-571` | decret | 1 | JORT 1974/36 du 1974-05-24 (Decret du 1974-05-22) |
| `1974-572` | decret | 2 | JORT 1974/36 du 1974-05-24 (Decret du 1974-05-22) |
| `1974-63` | decret | 4 | JORT 1974/10 du 1974-02-08 (Decret du 1974-01-31) |
| `1975-357` | decret | 4 | JORT 1975/38 du 1975-06-03 (Decret du 1975-06-03) |
| `1975-358` | decret | 1 | JORT 1975/38 du 1975-06-03 (Decret du 1975-06-03) |
| `1975-82` | loi | 6 | JORT 1975/87 du 1975-12-30 (Loi du 1975-12-30) |
| `1977-115` | decret | 4 | JORT 1977/9 du 1977-02-01 (Decret du 1977-02-02) |
| `1977-116` | decret | 1 | JORT 1977/9 du 1977-02-01 (Decret du 1977-02-02) |
| `1978-441` | decret | 4 | JORT 1978/33 du 1978-04-28 (Decret du 1978-04-26) |
| `1978-442` | decret | 1 | JORT 1978/33 du 1978-04-28 (Decret du 1978-04-26) |
| `1979-2022` | decret loi | 2 | **introuvable** |
| `1979-473` | decret | 4 | JORT 1979/34 du 1979-05-22 (Decret du 1979-05-21) |
| `1979-474` | decret | 1 | JORT 1979/34 du 1979-05-22 (Decret du 1979-05-21) |
| `1979-66` | loi | 2 | JORT 1979/76 du 1979-12-28 (Loi du 1979-12-31) |
| `1980-36` | loi | 3 | JORT 1980/32 du 1980-05-27 (Loi du 1980-05-28) |
| `1980-609` | decret | 4 | JORT 1980/31 du 1980-05-23 (Decret du 1980-05-19) |
| `1980-610` | decret | 1 | JORT 1980/31 du 1980-05-23 (Decret du 1980-05-19) |
| `1980-75` | decret | 4 | JORT 1980/5 du 1980-01-25 (Decret du 1980-01-21) |
| `1980-76` | decret | 1 | JORT 1980/5 du 1980-01-25 (Decret du 1980-01-21) |
| `1981-224` | decret | 8 | JORT 1981/13 du 1981-02-27 (Decret du 1981-02-24) |
| `1981-437` | decret | 5 | JORT 1981/25 du 1981-04-14 (Decret du 1981-04-07) |
| `1981-438` | decret | 1 | JORT 1981/25 du 1981-04-14 (Decret du 1981-04-07) |
| `1981-6` | loi | 18 | JORT 1981/9 du 1981-02-13 (Loi du 1981-02-12) |
| `1982-501` | decret | 7 | JORT 1982/19 du 1982-03-19 (Decret du 1982-03-16) |
| `1982-502` | decret | 1 | JORT 1982/19 du 1982-03-19 (Decret du 1982-03-16) |
| `1982-91` | loi | 2 | JORT 1982/84 du 1982-12-31 (Loi du 1982-12-31) |
| `1983-1217` | decret | 198 | JORT 1983/85 du 1983-12-27 (Decret du 1983-12-21) |
| `1983-509` | decret | 4 | JORT 1983/42 du 1983-06-07 (Decret du 1983-06-04) |
| `1983-510` | decret | 1 | JORT 1983/42 du 1983-06-07 (Decret du 1983-06-04) |
| `1985-109` | loi | 1 | JORT 1985/91 du 1985-12-31 (Loi du 1985-12-31) |
| `1985-12` | loi | 3 | JORT 1985/20 du 1985-03-12 (Loi du 1985-03-05) |
| `1986-689` | decret | 4 | JORT 1986/41 du 1986-07-18 (Decret du 1986-07-20) |
| `1986-690` | decret | 1 | JORT 1986/41 du 1986-07-18 (Decret du 1986-07-20) |
| `1986-75` | loi | 1 | JORT 1986/43 du 1986-08-01 (Loi du 1986-07-28) |
| `1987-1277` | decret | 4 | JORT 1987/78 du 1987-11-06 (Decret du 1987-11-05) |
| `1987-1278` | decret | 1 | JORT 1987/78 du 1987-11-06 (Decret du 1987-11-05) |
| `1988-38` | loi | 2 | JORT 1988/33 du 1988-05-13 (Loi du 1988-05-06) |
| `1988-889` | decret | 4 | JORT 1988/31 du 1988-05-06 (Decret du 1988-06-05) |
| `1988-890` | decret | 1 | JORT 1988/31 du 1988-05-06 (Decret du 1988-05-05) |
| `1989-107` | decret | 4 | JORT 1989/4 du 1989-01-17 (Decret du 1989-01-10) |
| `1989-114` | loi | 14 | JORT 1989/1 du 1990-01-02 (Loi du 1989-12-30) |
| `1989-1551` | decret | 1 | JORT 1989/69 du 1989-10-17 (Decret du 1989-10-06) |
| `1989-1552` | decret | 1 | JORT 1989/69 du 1989-10-17 (Decret du 1989-10-06) |
| `1989-73` | loi | 10 | JORT 1989/60 du 1989-09-05 (Loi du 1989-09-02) |
| `1990-246` | decret | 4 | JORT 1990/13 du 1990-02-16 (Decret du 1990-02-05) |
| `1990-247` | decret | 1 | JORT 1990/13 du 1990-02-16 (Decret du 1990-02-05) |
| `1991-1128` | decret | 161 | JORT 1991/57 du 1991-08-16 (Decret du 1991-07-29) |
| `1991-1316` | decret | 1 | JORT 1991/63 du 1991-09-17 (Decret du 1991-09-02) |
| `1991-1317` | decret | 1 | JORT 1991/63 du 1991-09-17 (Decret du 1991-09-02) |
| `1991-241` | decret | 266 | JORT 1991/14 du 1991-02-19 (Decret du 1991-02-04) |
| `1991-98` | loi | 2 | JORT 1991/90 du 1991-12-31 (Loi du 1991-12-31) |
| `1992-1299` | decret | 5 | JORT 1992/49 du 1992-07-28 (Decret du 1992-07-13) |
| `1992-1300` | decret | 2 | JORT 1992/49 du 1992-07-28 (Decret du 1992-07-13) |
| `1992-1630` | decret | 4 | JORT 1992/63 du 1992-09-22 (Decret du 1992-09-07) |
| `1992-1631` | decret | 1 | JORT 1992/63 du 1992-09-22 (Decret du 1992-09-07) |
| `1992-631` | decret | 2 | JORT 1992/21 du 1992-04-03 (Decret du 1992-03-23) |
| `1993-1256` | decret | 4 | JORT 1993/44 du 1993-06-15 (Decret du 1993-06-07) |
| `1993-1257` | decret | 1 | JORT 1993/44 du 1993-06-15 (Decret du 1993-06-07) |
| `1993-1838` | decret | 4 | JORT 1993/69 du 1993-09-14 (Decret du 1993-09-06) |
| `1993-1840` | decret | 1 | JORT 1993/69 du 1993-09-14 (Decret du 1993-09-06) |
| `1993-2309` | decret | 184 | JORT 1993/89 du 1993-11-23 (Decret du 1993-11-10) |
| `1993-308` | decret | 2 | JORT 1993/13 du 1993-02-16 (Decret du 1993-02-01) |
| `1994-1103` | decret | 84 | JORT 1994/41 du 1994-05-27 (Decret du 1994-05-14) |
| `1994-1105` | decret | 84 | JORT 1994/41 du 1994-05-27 (Decret du 1994-05-14) |
| `1994-1110` | decret | 84 | JORT 1994/41 du 1994-05-27 (Decret du 1994-05-14) |
| `1994-1804` | decret | 4 | JORT 1994/71 du 1994-09-09 (Decret du 1994-08-29) |
| `1994-1865` | decret | 1 | JORT 1994/72 du 1994-09-13 (Decret du 1994-09-05) |
| `1994-71` | loi | 2 | JORT 1994/50 du 1994-06-28 (Loi du 1994-06-27) |
| `1994-88` | loi | 5 | JORT 1994/60 du 1994-08-02 (Loi du 1994-07-26) |
| `1995-114` | decret | 5 | JORT 1995/8 du 1995-01-27 (Decret du 1995-01-16) |
| `1995-1166` | decret | 4 | JORT 1995/55 du 1995-07-11 (Decret du 1995-07-03) |
| `1995-538` | decret | 2 | JORT 1995/30 du 1995-04-14 (Decret du 1995-04-01) |
| `1995-900` | decret | 4 | JORT 1995/40 du 1995-05-19 (Decret du 1995-05-15) |
| `1995-901` | decret | 1 | JORT 1995/40 du 1995-05-19 (Decret du 1995-05-15) |
| `1996-101` | loi | 2 | JORT 1996/94 du 1996-11-22 (Loi du 1996-11-18) |
| `1996-1013` | decret | 4 | JORT 1996/45 du 1996-06-04 (Decret du 1996-05-27) |
| `1996-1014` | decret | 1 | JORT 1996/45 du 1996-06-04 (Decret du 1996-05-27) |
| `1996-1547` | decret | 4 | JORT 1996/74 du 1996-09-13 (Decret du 1996-09-10) |
| `1996-1548` | decret | 1 | JORT 1996/74 du 1996-09-13 (Decret du 1996-09-10) |
| `1996-1908` | decret | 300 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1909` | decret | 300 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1910` | decret | 174 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1911` | decret | 49 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1912` | decret | 300 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1913` | decret | 75 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1916` | decret | 74 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1921` | decret | 63 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1923` | decret | 111 | JORT 1996/85 du 1996-10-22 (Decret du 1996-10-16) |
| `1996-1990` | decret | 86 | JORT 1996/88 du 1996-11-01 (Decret du 1996-10-23) |
| `1996-1994` | decret | 66 | JORT 1996/88 du 1996-11-01 (Decret du 1996-10-23) |
| `1996-2000` | decret | 61 | JORT 1996/88 du 1996-11-01 (Decret du 1996-10-23) |
| `1996-2007` | decret | 195 | JORT 1996/88 du 1996-11-01 (Decret du 1996-10-23) |
| `1996-2388` | decret | 84 | JORT 1996/102 du 1996-12-20 (Decret du 1996-12-09) |
| `1996-2410` | decret | 186 | JORT 1996/103 du 1996-12-24 (Decret du 1996-12-11) |
| `1996-2438` | decret | 106 | JORT 1996/104 du 1996-12-27 (Decret du 1996-12-18) |
| `1997-1521` | decret | 4 | JORT 1997/63 du 1997-08-08 (Decret du 1997-08-04) |
| `1997-1522` | decret | 1 | JORT 1997/63 du 1997-08-08 (Decret du 1997-08-04) |
| `1997-1832` | decret | 8557 | JORT 1997/76 du 1997-09-23 (Decret du 1997-09-16) |
| `1997-2148` | decret | 4 | JORT 1997/93 du 1997-11-21 (Decret du 1997-11-12) |
| `1997-2149` | decret | 1 | JORT 1997/93 du 1997-11-21 (Decret du 1997-11-12) |
| `1997-228` | decret | 103 | JORT 1997/11 du 1997-02-07 (Decret du 1997-01-27) |
| `1997-4` | loi | 10 | JORT 1997/10 du 1997-02-04 (Loi du 1997-02-03) |
| `1997-88` | loi | 5 | JORT 1997/104 du 1997-12-31 (Loi du 1997-12-29) |
| `1998-1523` | decret | 106 | JORT 1998/62 du 1998-08-04 (Decret du 1998-07-20) |
| `1998-1674` | decret | 4 | JORT 1998/71 du 1998-09-04 (Decret du 1998-08-26) |
| `1998-1675` | decret | 1 | JORT 1998/71 du 1998-09-04 (Decret du 1998-08-26) |
| `1998-409` | decret | 1 | JORT 1998/17 du 1998-02-27 (Decret du 1998-02-18) |
| `1999-1866` | decret | 4 | JORT 1999/74 du 1999-09-14 (Decret du 1999-08-31) |
| `1999-1867` | decret | 1 | JORT 1999/74 du 1999-09-14 (Decret du 1999-08-31) |
| `1999-2016` | decret | 136 | JORT 1999/77 du 1999-09-24 (Decret du 1999-09-13) |
| `1999-205` | decret | 86 | JORT 1999/11 du 1999-02-05 (Decret du 1999-01-25) |
| `1999-2116` | decret | 106 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2117` | decret | 106 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2119` | decret | 86 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2121` | decret | 174 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2127` | decret | 66 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2132` | decret | 84 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2137` | decret | 111 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2141` | decret | 63 | JORT 1999/80 du 1999-10-05 (Decret du 1999-09-27) |
| `1999-2183` | decret | 86 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2184` | decret | 49 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2186` | decret | 75 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2189` | decret | 100 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2193` | decret | 186 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2194` | decret | 103 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2198` | decret | 114 | JORT 1999/82 du 1999-10-12 (Decret du 1999-10-04) |
| `1999-2432` | decret | 61 | JORT 1999/91 du 1999-11-12 (Decret du 1999-11-01) |
| `1999-2498` | decret | 195 | JORT 1999/93 du 1999-11-19 (Decret du 1999-11-08) |
| `1999-366` | decret | 136 | JORT 1999/16 du 1999-02-23 (Decret du 1999-02-15) |
| `1999-994` | decret | 4 | JORT 1999/38 du 1999-05-11 (Decret du 1999-05-10) |
| `1999-995` | decret | 1 | JORT 1999/38 du 1999-05-11 (Decret du 1999-05-10) |
| `2000-1070` | decret | 100 | JORT 2000/42 du 2000-05-26 (Decret du 2000-05-15) |
| `2000-1440` | decret | 131 | JORT 2000/54 du 2000-07-07 (Decret du 2000-06-27) |
| `2000-2063` | decret | 131 | JORT 2000/78 du 2000-09-29 (Decret du 2000-09-18) |
| `2000-2452` | decret | 372 | JORT 2000/86 du 2000-10-27 (Decret du 2000-10-17) |
| `2000-2491` | decret | 114 | JORT 2000/90 du 2000-11-10 (Decret du 2000-10-31) |
| `2000-949` | decret | 4 | JORT 2000/38 du 2000-05-12 (Decret du 2000-05-11) |
| `2000-950` | decret | 1 | JORT 2000/38 du 2000-05-12 (Decret du 2000-05-11) |
| `2001-1002` | decret | 114 | JORT 2001/39 du 2001-05-15 (Decret du 2001-05-08) |
| `2001-1159` | decret | 100 | JORT 2001/43 du 2001-05-29 (Decret du 2001-05-22) |
| `2001-123` | loi | 8 | JORT 2001/104 du 2001-12-28 (Loi du 2001-12-28) |
| `2001-1746` | decret | 4 | JORT 2001/63 du 2001-08-07 (Decret du 2001-08-01) |
| `2001-1747` | decret | 1 | JORT 2001/63 du 2001-08-07 (Decret du 2001-08-01) |
| `2001-1763` | decret | 63 | JORT 2001/64 du 2001-08-10 (Decret du 2001-08-01) |
| `2001-2591` | decret | 73 | JORT 2001/92 du 2001-11-16 (Decret du 2001-11-09) |
| `2002-104` | loi | 4 | JORT 2002/106 du 2002-12-31 (Loi du 2002-12-30) |
| `2002-1790` | decret | 4 | JORT 2002/67 du 2002-08-16 (Decret du 2002-08-12) |
| `2002-1791` | decret | 1 | JORT 2002/67 du 2002-08-16 (Decret du 2002-08-12) |
| `2002-2232` | decret | 131 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2233` | decret | 106 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2234` | decret | 106 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2235` | decret | 86 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2236` | decret | 136 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2237` | decret | 86 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2239` | decret | 174 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2240` | decret | 49 | JORT 2002/85 du 2002-10-18 (Decret du 2002-10-14) |
| `2002-2824` | decret | 558 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2827` | decret | 114 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2837` | decret | 100 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2840` | decret | 195 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2841` | decret | 73 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2851` | decret | 100 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2852` | decret | 63 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2856` | decret | 84 | JORT 2002/90 du 2002-11-05 (Decret du 2002-10-29) |
| `2002-2939` | decret | 61 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-2941` | decret | 61 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-2943` | decret | 66 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-2951` | decret | 103 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-2952` | decret | 186 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-2954` | decret | 111 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-2957` | decret | 63 | JORT 2002/94 du 2002-11-19 (Decret du 2002-11-11) |
| `2002-3023` | decret | 558 | JORT 2002/98 du 2002-12-03 (Decret du 2002-11-19) |
| `2002-32` | loi | 8 | JORT 2002/22 du 2002-03-15 (Loi du 2002-03-12) |
| `2002-916` | decret | 4 | JORT 2002/35 du 2002-04-30 (Decret du 2002-04-22) |
| `2003-1212` | decret | 4 | JORT 2003/46 du 2003-06-10 (Decret du 2003-06-02) |
| `2003-1235` | decret | 100 | JORT 2003/46 du 2003-06-10 (Decret du 2003-06-02) |
| `2003-1544` | decret | 1 | JORT 2003/55 du 2003-07-11 (Decret du 2003-07-02) |
| `2003-1691` | decret | 4 | JORT 2003/67 du 2003-08-22 (Decret du 2003-08-18) |
| `2003-1692` | decret | 1 | JORT 2003/67 du 2003-08-22 (Decret du 2003-08-18) |
| `2004-1349` | decret | 100 | JORT 2004/48 du 2004-06-15 (Decret du 2004-06-07) |
| `2004-1803` | decret | 4 | JORT 2004/63 du 2004-08-06 (Decret du 2004-08-02) |
| `2004-1804` | decret | 1 | JORT 2004/63 du 2004-08-06 (Decret du 2004-08-02) |
| `2004-90` | loi | 2 | JORT 2004/105 du 2004-12-31 (Loi du 2004-12-31) |
| `2005-2320` | decret | 4 | JORT 2005/68 du 2005-08-26 (Decret du 2005-08-22) |
| `2005-2321` | decret | 1 | JORT 2005/68 du 2005-08-26 (Decret du 2005-08-22) |
| `2005-3127` | decret | 86 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3130` | decret | 131 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3131` | decret | 106 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3132` | decret | 106 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3133` | decret | 136 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3134` | decret | 86 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3135` | decret | 174 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3138` | decret | 49 | JORT 2005/99 du 2005-12-13 (Decret du 2005-12-06) |
| `2005-3164` | decret | 558 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3165` | decret | 100 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3169` | decret | 558 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3172` | decret | 66 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3185` | decret | 84 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3187` | decret | 103 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3188` | decret | 186 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3198` | decret | 111 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3201` | decret | 63 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3210` | decret | 61 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3213` | decret | 63 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3214` | decret | 100 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3219` | decret | 195 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3220` | decret | 73 | JORT 2005/100 du 2005-12-16 (Decret du 2005-12-12) |
| `2005-3292` | decret | 114 | JORT 2005/102 du 2005-12-23 (Decret du 2005-12-19) |
| `2006-1794` | decret | 100 | JORT 2006/52 du 2006-06-30 (Decret du 2006-06-26) |
| `2006-2098` | decret | 4 | JORT 2006/62 du 2006-08-04 (Decret du 2006-07-24) |
| `2006-2099` | decret | 1 | JORT 2006/62 du 2006-08-04 (Decret du 2006-07-24) |
| `2006-2429` | decret | 86 | JORT 2006/73 du 2006-09-12 (Decret du 2006-09-05) |
| `2006-85` | loi | 1 | JORT 2006/103 du 2006-12-26 (Loi du 2006-12-25) |
| `2007-1034` | decret | 100 | JORT 2007/36 du 2007-05-04 (Decret du 2007-04-24) |
| `2007-1406` | decret | 9 | JORT 2007/49 du 2007-06-19 (Decret du 2007-06-18) |
| `2007-2079` | decret | 4 | JORT 2007/67 du 2007-08-21 (Decret du 2007-08-14) |
| `2007-2080` | decret | 1 | JORT 2007/67 du 2007-08-21 (Decret du 2007-08-14) |
| `2007-268` | decret | 14372 | JORT 2007/14 du 2007-02-16 (Decret du 2007-02-12) |
| `2007-43` | loi | 7 | JORT 2007/51 du 2007-06-26 (Loi du 2007-06-25) |
| `2007-62` | decret | 86 | JORT 2007/5 du 2007-01-16 (Decret du 2007-01-10) |
| `2007-70` | loi | 3 | JORT 2007/104 du 2007-12-28 (Loi du 2007-12-27) |
| `2008-2072` | decret | 8 | JORT 2008/46 du 2008-06-06 (Decret du 2008-06-02) |
| `2008-2073` | decret | 1 | JORT 2008/46 du 2008-06-06 (Decret du 2008-06-02) |
| `2008-4048` | decret | 175 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4051` | decret | 86 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4053` | decret | 136 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4054` | decret | 106 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4055` | decret | 131 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4056` | decret | 106 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4058` | decret | 86 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4059` | decret | 49 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4062` | decret | 558 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4064` | decret | 558 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4066` | decret | 100 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4069` | decret | 61 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4074` | decret | 63 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4076` | decret | 111 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4085` | decret | 558 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4086` | decret | 66 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4088` | decret | 84 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4089` | decret | 103 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4090` | decret | 186 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4093` | decret | 73 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4094` | decret | 195 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4096` | decret | 86 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4100` | decret | 100 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4102` | decret | 63 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2008-4105` | decret | 114 | JORT 2008/3 du 2009-01-09 (Decret du 2008-12-30) |
| `2009-1508` | decret | 100 | JORT 2009/41 du 2009-05-22 (Decret du 2009-05-18) |
| `2009-2155` | decret | 63 | JORT 2009/58 du 2009-07-21 (Decret du 2009-07-14) |
| `2009-2257` | decret | 8 | JORT 2009/62 du 2009-08-04 (Decret du 2009-07-14) |
| `2009-2258` | decret | 1 | JORT 2009/62 du 2009-08-04 (Decret du 2009-07-14) |
| `2009-2972` | decret | 342 | JORT 2009/82 du 2009-10-13 (Decret du 2009-10-05) |
| `2009-71` | loi | 3 | JORT 2009/102 du 2009-12-22 (Loi du 2009-12-21) |
| `2009-900` | decret | 111 | JORT 2009/29 du 2009-04-10 (Decret du 2009-04-04) |
| `2010-1746` | decret | 8 | JORT 2010/58 du 2010-07-20 (Decret du 2010-07-17) |
| `2010-1747` | decret | 1 | JORT 2010/58 du 2010-07-20 (Decret du 2010-07-17) |
| `2010-2743` | decret | 161 | JORT 2010/87 du 2010-10-29 (Decret du 2010-10-25) |
| `2010-527` | decret | 100 | JORT 2010/25 du 2010-03-26 (Decret du 2010-03-22) |
| `2011-1093` | decret | 38 | JORT 2011/59 du 2011-08-09 (Decret du 2011-08-03) |
| `2011-1262` | decret | 100 | JORT 2011/68 du 2011-09-09 (Decret du 2011-09-05) |
| `2011-2286` | decret | 136 | JORT 2011/73 du 2011-09-27 (Decret du 2011-09-21) |
| `2011-48` | decret loi | 1 | JORT 2011/41 du 2011-06-07 (Decret-Loi du 2011-06-04) |
| `2011-4836` | decret | 342 | JORT 2011/1 du 2012-01-03 (Decret du 2011-12-10) |
| `2011-679` | decret | 8 | JORT 2011/42 du 2011-06-10 (Decret du 2011-06-09) |
| `2011-681` | decret | 1 | JORT 2011/42 du 2011-06-10 (Decret du 2011-06-09) |
| `2012-1684` | decret | 184 | JORT 2012/72 du 2012-09-11 (Decret du 2012-08-22) |
| `2012-1981` | decret | 8 | JORT 2012/77 du 2012-09-28 (Decret du 2012-09-20) |
| `2012-1982` | decret | 2 | JORT 2012/77 du 2012-09-28 (Decret du 2012-09-20) |
| `2012-2949` | decret | 84 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2952` | decret | 106 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2953` | decret | 86 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2954` | decret | 131 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2955` | decret | 106 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2956` | decret | 86 | JORT 2012/97 du 2012-11-29 (Decret du 2012-11-29) |
| `2012-2957` | decret | 175 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2960` | decret | 558 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2961` | decret | 558 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2962` | decret | 136 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2963` | decret | 49 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2964` | decret | 558 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2967` | decret | 297 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2969` | decret | 82 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2970` | decret | 84 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2972` | decret | 63 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2973` | decret | 225 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2980` | decret | 86 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2981` | decret | 84 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2982` | decret | 84 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2983` | decret | 103 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2012-2984` | decret | 186 | JORT 2012/97 du 2012-12-07 (Decret du 2012-11-29) |
| `2013-1403` | decret | 64 | JORT 2013/34 du 2013-04-26 (Decret du 2013-04-22) |
| `2013-1405` | decret | 64 | JORT 2013/34 du 2013-04-26 (Decret du 2013-04-22) |
| `2013-1406` | decret | 66 | JORT 2013/34 du 2013-04-26 (Decret du 2013-04-22) |
| `2013-1407` | decret | 66 | JORT 2013/34 du 2013-04-26 (Decret du 2013-04-22) |
| `2013-1408` | decret | 66 | JORT 2013/34 du 2013-04-26 (Decret du 2013-04-22) |
| `2013-1409` | decret | 66 | JORT 2013/34 du 2013-04-26 (Decret du 2013-04-22) |
| `2013-2227` | decret | 255 | JORT 2013/46 du 2013-06-07 (Decret du 2013-06-03) |
| `2013-2527` | decret | 167 | JORT 2013/51 du 2013-06-25 (Decret du 2013-06-10) |
| `2013-3114` | decret | 136 | JORT 2013/61 du 2013-07-30 (Decret du 2013-07-22) |
| `2013-3801` | decret | 111 | JORT 2013/79 du 2013-10-01 (Decret du 2013-09-25) |
| `2013-5095` | decret | 84 | JORT 2013/100 du 2013-12-17 (Decret du 2013-11-22) |
| `2013-5098` | decret | 84 | JORT 2013/100 du 2013-12-17 (Decret du 2013-11-22) |
| `2013-54` | loi | 8 | JORT 2013/105 du 2013-12-31 (Loi du 2013-12-30) |
| `2013-667` | decret | 150 | JORT 2013/11 du 2013-02-05 (Decret du 2013-01-29) |
| `2013-719` | decret | 184 | JORT 2013/13 du 2013-02-12 (Decret du 2013-01-29) |
| `2014-1463` | decret | 145 | JORT 2014/36 du 2014-05-06 (Decret du 2014-04-22) |
| `2014-1715` | decret | 558 | JORT 2014/41 du 2014-05-23 (Decret du 2014-05-19) |
| `2014-1796` | decret | 63 | JORT 2014/42 du 2014-05-27 (Decret du 2014-05-19) |
| `2014-1798` | decret | 130 | JORT 2014/42 du 2014-05-27 (Decret du 2014-05-19) |
| `2014-1799` | decret | 266 | JORT 2014/42 du 2014-05-27 (Decret du 2014-05-19) |
| `2014-1800` | decret | 133 | JORT 2014/42 du 2014-05-27 (Decret du 2014-05-19) |
| `2014-2597` | decret | 558 | JORT 2014/58 du 2014-07-22 (Decret du 2014-07-15) |
| `2014-2598` | decret | 558 | JORT 2014/58 du 2014-07-22 (Decret du 2014-07-15) |
| `2014-2907` | decret | 8 | JORT 2014/66 du 2014-08-15 (Decret du 2014-08-11) |
| `2014-2908` | decret | 1 | JORT 2014/66 du 2014-08-15 (Decret du 2014-08-11) |
| `2014-3943` | decret | 161 | JORT 2014/88 du 2014-10-31 (Decret du 2014-10-17) |
| `2014-4216` | decret | 137 | JORT 2014/95 du 2014-11-25 (Decret du 2014-10-30) |
| `2014-45` | decret | 266 | JORT 2014/6 du 2014-01-21 (Decret du 2014-01-10) |
| `2014-50` | decret | 84 | JORT 2014/6 du 2014-01-21 (Decret du 2014-01-10) |
| `2014-57` | decret | 179 | JORT 2014/6 du 2014-01-21 (Decret du 2014-01-10) |
| `2014-61` | decret | 24 | JORT 2014/7 du 2014-01-24 (Decret du 2014-01-17) |
| `2015-1164` | decret | 50 | JORT 2015/71 du 2015-09-04 (Decret du 2015-09-04) |
| `2015-1762` | decret | 4 | JORT 2015/91 du 2015-11-13 (Decret du 2015-11-09) |
| `2015-1763` | decret gouvernemental | 1 | **introuvable** |
| `2015-53` | loi | 1 | JORT 2015/104 du 2015-12-29 (Loi du 2015-12-25) |
| `2015-60` | decret | 256 | JORT 2015/34 du 2015-04-28 (Decret du 2015-04-27) |
| `2016-114` | decret | 100 | JORT 2016/15 du 2016-02-19 (Decret gouvernemental du 2016-01-11) |
| `2016-153` | decret | 139 | JORT 2016/8 du 2016-01-26 (Decret gouvernemental du 2016-01-25) |
| `2016-78` | loi | 4 | JORT 2016/105 du 2016-12-27 (Loi du 2016-12-17) |
| `2017-347` | decret | 110 | JORT 2017/20 du 2017-03-10 (Decret gouvernemental du 2017-03-03) |
| `2017-349` | decret | 110 | JORT 2017/20 du 2017-03-10 (Decret gouvernemental du 2017-03-03) |
| `2017-66` | loi | 11 | JORT 2017/101 du 2017-12-19 (Loi du 2017-12-18) |
| `2017-668` | decret | 4 | JORT 2017/45 du 2017-06-06 (Decret gouvernemental du 2017-06-05) |
| `2017-69` | decret | 115 | JORT 2017/5 du 2017-01-17 (Decret gouvernemental du 2017-01-06) |
| `2017-8` | loi | 1 | JORT 2017/15 du 2017-02-21 (Loi du 2017-02-14) |
| `2017-990` | decret | 125 | JORT 2017/73 du 2017-09-12 (Decret gouvernemental du 2017-08-17) |
| `2018-672` | decret gouvernemental | 4 | JORT 2018/64 du 2018-08-10 (Decret gouvernemental du 2018-08-07) |
| `2018-782` | decret | 79 | JORT 2018/77 du 2018-09-25 (Decret gouvernemental du 2018-09-21) |
| `2018-786` | decret | 179 | JORT 2018/77 du 2018-09-25 (Decret gouvernemental du 2018-09-21) |
| `2019-10` | loi organique | 2 | JORT 2019/11 du 2019-02-05 (Loi organique du 2019-01-30) |
| `2019-1133` | decret | 2460 | JORT 2019/100 du 2019-12-13 (Décret gouvernemental du 2019-12-12) |
| `2019-1241` | decret | 161 | JORT 2020/3 du 2020-01-10 (Décret gouvernemental du 2019-12-26) |
| `2019-209` | decret | 2133 | JORT 2019/20 du 2019-03-08 (Decret gouvernemental du 2019-03-05) |
| `2019-37` | loi | 2 | JORT 2019/35 du 2019-04-30 (Loi du 2019-04-30) |
| `2019-433` | decret | 372 | JORT 2019/41 du 2019-05-21 (Decret gouvernemental du 2019-05-10) |
| `2019-436` | decret | 186 | JORT 2019/41 du 2019-05-21 (Decret gouvernemental du 2019-05-10) |
| `2019-454` | decret gouvernemental | 4 | **introuvable** |
| `2019-455` | decret gouvernemental | 1 | **introuvable** |
| `2019-78` | loi | 2 | JORT 2019/104 du 2019-12-27 (Loi du 2019-12-23) |
| `2019-922` | decret | 126 | JORT 2019/85 du 2019-10-22 (Décret gouvernemental du 2019-09-26) |
| `2020-100` | decret | 86 | JORT 2020/16 du 2020-02-25 (Décret gouvernemental du 2020-02-14) |
| `2020-1069` | decret gouvernemental | 4 | JORT 2021/1 du 2021-01-05 (Décret gouvernemental du 2020-12-30) |
| `2020-1070` | decret gouvernemental | 1 | JORT 2021/1 du 2021-01-05 (Décret gouvernemental du 2020-12-31) |
| `2020-122` | decret | 74 | JORT 2020/17 du 2020-02-28 (Décret gouvernemental du 2020-02-25) |
| `2020-127` | decret | 84 | JORT 2020/18 du 2020-03-03 (Décret gouvernemental du 2020-02-25) |
| `2020-128` | decret | 84 | JORT 2020/18 du 2020-03-03 (Décret gouvernemental du 2020-02-25) |
| `2020-129` | decret | 184 | JORT 2020/18 du 2020-03-03 (Décret gouvernemental du 2020-02-25) |
| `2020-130` | decret | 84 | JORT 2020/18 du 2020-03-03 (Décret gouvernemental du 2020-02-25) |
| `2020-141` | decret | 84 | JORT 2020/18 du 2020-03-03 (Décret gouvernemental du 2020-02-25) |
| `2020-142` | decret | 292 | JORT 2020/19 du 2020-03-06 (Décret gouvernemental du 2020-02-25) |
| `2020-143` | decret | 73 | JORT 2020/19 du 2020-03-06 (Décret gouvernemental du 2020-02-25) |
| `2020-317` | decret, decret gouvernemental | 12 | JORT 2020/45 du 2020-05-20 (Décret gouvernemental du 2020-05-19) |
| `2020-46` | loi | 2 | JORT 2020/128 du 2020-12-25 (Loi du 2020-12-23) |
| `2020-635` | decret | 168 | JORT 2020/88 du 2020-08-25 (Décret gouvernemental du 2020-08-14) |
| `2020-73` | decret | 86 | JORT 2020/14 du 2020-02-18 (Décret gouvernemental du 2020-02-14) |
| `2020-767` | decret | 2322 | JORT 2020/94 du 2020-09-18 (Décret gouvernemental du 2020-09-18) |
| `2020-80` | decret | 64 | JORT 2020/14 du 2020-02-18 (Décret gouvernemental du 2020-02-14) |
| `2020-81` | decret | 66 | JORT 2020/14 du 2020-02-18 (Décret gouvernemental du 2020-02-14) |
| `2020-82` | decret | 66 | JORT 2020/14 du 2020-02-18 (Décret gouvernemental du 2020-02-14) |
| `2020-83` | decret | 130 | JORT 2020/14 du 2020-02-18 (Décret gouvernemental du 2020-02-14) |
| `2021-105` | decret | 74 | JORT 2021/14 du 2021-02-09 (Décret gouvernemental du 2021-02-08) |
| `2021-21` | decret loi | 2 | JORT 2021/119 du 2021-12-28 (Decret-Loi du 2021-12-28) |
| `2021-481` | decret | 93 | JORT 2021/55 du 2021-06-29 (Décret gouvernemental du 2021-06-28) |
| `2021-492` | decret | 45 | JORT 2021/57 du 2021-07-06 (Décret gouvernemental du 2021-07-05) |
| `2021-59` | decret | 16 | JORT 2021/8 du 2021-01-22 (Décret gouvernemental du 2021-01-21) |
| `2022-768` | decret | 1 | JORT 2022/114 du 2022-10-21 (Décret du 2022-10-19) |
| `2022-769` | decret gouvernemental | 4 | **introuvable** |
| `2022-79` | decret loi | 1 | **introuvable** |
| `2022-797` | decret | 7686 | JORT 2022/120 du 2022-11-08 (Décret du 2022-11-08) |
| `2022-8` | decret loi | 1 | JORT 2022/13 du 2022-02-02 (Decret-Loi du 2022-01-31) |
| `2024-419` | decret | 8 | JORT 2024/85 du 2024-07-09 (Décret du 2024-07-09) |
| `2024-420` | decret | 2 | JORT 2024/85 du 2024-07-09 (Décret du 2024-07-09) |
| `2024-48` | loi | 5 | **introuvable** |
| `2025-17` | loi | 1 | JORT 2025/148 du 2025-12-12 (Loi du 2025-12-12) |
| `2026-66` | decret | 3 | **introuvable** |
| `2026-67` | decret | 12 | **introuvable** |

## Anomalies

### Référence en chaîne libre — 2 paramètres

| Paramètre | Référence |
| --- | --- |
| `energie.electricite.tarifs_par_tranche` | Tarification progressive de l'électricité en Tunisie |
| `energie.gaz.tarifs_par_tranche` | Tarification progressive du gaz naturel en Tunisie |

### Lien gitlab.com — 12 paramètres

Un dépôt personnel n'est pas une source officielle : ces liens doivent céder la place au fascicule du JORT sur `pist.tn`.

- `marche_travail/smag_journalier.yaml`
- `marche_travail/smig_40h_horaire.yaml`
- `marche_travail/smig_40h_mensuel.yaml`
- `marche_travail/smig_48h_horaire.yaml`
- `marche_travail/smig_48h_mensuel.yaml`
- `prelevements_sociaux/contribution_sociale_solidarite/entreprise/taux_is_10_pc/bareme.yaml`
- `prelevements_sociaux/contribution_sociale_solidarite/entreprise/taux_is_10_pc/montant_minimum.yaml`
- `prelevements_sociaux/contribution_sociale_solidarite/salarie.yaml`
- `prelevements_sociaux/cotisations_sociales/secteur_public/pensionne_cnrps/deces.yaml`
- `prelevements_sociaux/cotisations_sociales/secteur_public/salarie_cnrps/cotisations_employeur/maladie.yaml`
- `prelevements_sociaux/cotisations_sociales/secteur_public/salarie_cnrps/cotisations_salarie/deces.yaml`
- `prelevements_sociaux/cotisations_sociales/secteur_public/salarie_cnrps/cotisations_salarie/maladie.yaml`

### Textes cités introuvables dans le corpus — 9

| Texte | Type cité | Occurrences |
| --- | --- | ---: |
| `1979-2022` | decret loi | 2 |
| `2015-1763` | decret gouvernemental | 1 |
| `2019-454` | decret gouvernemental | 4 |
| `2019-455` | decret gouvernemental | 1 |
| `2022-769` | decret gouvernemental | 4 |
| `2022-79` | decret loi | 1 |
| `2024-48` | loi | 5 |
| `2026-66` | decret | 3 |
| `2026-67` | decret | 12 |

### Textes cités par leur seule date — 13 paramètres

Ces citations sont réelles mais insolubles contre un corpus indexé par numéro : « arrêté conjoint … du 19 mai 2020 ». Elles ne sont pas des références fautives, elles demandent un numéro.

| Paramètre | Citation |
| --- | --- |
| `marche_travail.smag_journalier` | Arrêté des Secrétaires d'Etat à l'Agriculture et à la Santé Publique et aux Affaires Sociales du 24 décembre 1963 modifiant l'arrêté du 30 a |
| `prelevements_sociaux.cotisations_sociales.secteur_prive.rsna.cotisations_employeur.retraite_complementaire` | Arrêté du ministre des affaires sociales du 18 novembre 1978 portant publication du règlement du régime complémentaire de pension de vieille |
| `prelevements_sociaux.cotisations_sociales.secteur_prive.rsna.cotisations_salarie.retraite_complementaire` | Arrêté du ministre des affaires sociales du 18 novembre 1978 portant publication du règlement du régime complémentaire de pension de vieille |
| `prelevements_sociaux.cotisations_sociales.secteur_public.pensionne_cnrps.deces` | Circulaire du premier ministre n°12  du 15 février 1993 |
| `prelevements_sociaux.cotisations_sociales.secteur_public.salarie_cnrps.cotisations_salarie.deces` | Circulaire du premier ministre n°12 du 15 février 1993 |
| `prestations.non_contributives.amen_social.aides_ponctuelles.fetes_religieuses.aid_al_adha` | Article 4 de l'arrêté conjoint du 8 décembre 2022, JORT n° 136 du 9 décembre 2022, p. 3446-3447 ; son article 5 abroge l'arrêté du 19 mai 20 |
| `prestations.non_contributives.amen_social.aides_ponctuelles.fetes_religieuses.aid_al_fitr` | Article 4 de l'arrêté conjoint du 8 décembre 2022, JORT n° 136 du 9 décembre 2022, p. 3446-3447 ; son article 5 abroge l'arrêté du 19 mai 20 |
| `prestations.non_contributives.amen_social.aides_ponctuelles.fetes_religieuses.ramadan` | Article 4 de l'arrêté conjoint du 8 décembre 2022, JORT n° 136 du 9 décembre 2022, p. 3446-3447 ; son article 5 abroge l'arrêté du 19 mai 20 |
| `prestations.non_contributives.amen_social.aides_ponctuelles.scolarite.rentree_scolaire` | Article 4 de l'arrêté conjoint du 8 décembre 2022, JORT n° 136 du 9 décembre 2022, p. 3446-3447 ; son article 5 abroge l'arrêté du 19 mai 20 |
| `prestations.non_contributives.amen_social.aides_ponctuelles.scolarite.rentree_universitaire` | Article 4 de l'arrêté conjoint du 8 décembre 2022, JORT n° 136 du 9 décembre 2022, p. 3446-3447 ; son article 5 abroge l'arrêté du 19 mai 20 |
| `prestations.non_contributives.amen_social.decile` | Circulaire N°12 du 12 mai 2022 |
| `prestations.non_contributives.amen_social.supplements.age_min_enfant` | Article premier de l'arrêté conjoint du 1er avril 2022 modifiant l'arrêté du 19 mai 2020, JORT n° 38 du 8 avril 2022, p. 972 ; effet au 1er  |
| `prestations.non_contributives.amen_social.supplements.handicap` | Dernier alinéa de l'article 2 de l'arrêté conjoint du 19 mai 2020 |

### Date de valeur antérieure au texte qui la fonde — 7887 paramètres, 143 couples distincts

Une valeur qui prend effet **avant la signature** du texte cité. Ce n'est pas une erreur en soi : les décrets de rémunération tunisiens sont couramment rétroactifs, et le dépôt date délibérément ses valeurs à la date d'effet énoncée par le texte, non à sa signature. C'est donc une **file de revue**, pas une liste de fautes — mais c'est dans cette file que se trouvent les dates fausses et les textes cités à tort, et les écarts les plus larges sont les plus suspects. Le contrôle porte sur la signature et non sur la publication, qui ajouterait un bruit certain.

| Texte cité | Signé le | Date de valeur | Écart | Paramètres | Fichiers | Exemple |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `2020-767` (Décret gouvernemental) | 2020-09-18 | 2020-08-01 | 48 j | 2136 | 91 | `fonction_publique.cadres_techniques_administration.adjoint_technique.indemnite_specifique_mensuelle.echelon_1` |
| `2019-209` (Decret gouvernemental) | 2019-03-05 | 2019-03-01 | 4 j | 1253 | 53 | `fonction_publique.conseillers_educatifs.conseiller_educatif.indemnite_specifique_mensuelle.echelon_1` |
| `1997-1832` (Decret) | 1997-09-16 | 1996-12-10 | 280 j | 538 | 25 | `fonction_publique.agents_services_douaniers.adjudant_chef_des_douanes_echelle_1.traitement_de_base.echelon_1` |
| `2011-4836` (Decret) | 2011-12-10 | 2011-05-01 | 223 j | 342 | 15 | `fonction_publique.cadres_des_metiers_du_sport.animateur_d_application_en_sport_pour_tous.indemnite_specifique_mensuelle.echelon_1` |
| `2019-1133` (Décret gouvernemental) | 2019-12-12 | 2019-07-01 | 164 j | 315 | 15 | `fonction_publique.conseillers_en_information_et_en_orientation_scolaire_et_universitaire.conseiller_en_information_et_en_orientation_scolaire_et_universitaire.indemnite_specifique_mensuelle.echelon_1` |
| `2014-45` (Decret) | 2014-01-10 | 2013-01-01 | 374 j | 266 | 12 | `fonction_publique.medecins_dentistes_hospitalo_sanitaires.medecin_dentiste_de_la_sante_publique.indemnite_specifique_mensuelle.echelon_1` |
| `2013-719` (Decret) | 2013-01-29 | 2013-01-01 | 28 j | 184 | 8 | `fonction_publique.controle_depenses_publiques.attache_controle_depenses_publiques.indemnite_specifique_mensuelle.echelon_1` |
| `2015-60` (Decret) | 2015-04-27 | 2015-01-01 | 116 j | 175 | 7 | `fonction_publique.infirmiers_de_la_sante_publique.auxiliaire_de_la_sante_publique.indemnite_specifique_mensuelle.echelon_1` |
| `2010-2743` (Decret) | 2010-10-25 | 2010-07-01 | 116 j | 161 | 7 | `fonction_publique.service_social_administrations_publiques.administrateur_conseiller_du_service_social.indemnite_specifique_mensuelle.echelon_1` |
| `2018-786` (Decret gouvernemental) | 2018-09-21 | 2014-01-21 | 1704 j | 137 | 6 | `fonction_publique.conseillers_praticiens_en_education_relevant.conseiller_praticien_adjoint_en_education.indemnite_specifique_mensuelle.echelon_1` |
| `2011-2286` (Decret) | 2011-09-21 | 2011-07-01 | 82 j | 136 | 6 | `fonction_publique.analystes_techniciens_informatique.analyste.indemnite_specifique_mensuelle.echelon_1` |
| `2019-922` (Décret gouvernemental) | 2019-09-26 | 2019-03-01 | 209 j | 126 | 6 | `fonction_publique.inspection_pedagogique_jeunesse_sports.inspecteur_ep_sports.indemnite_specifique_mensuelle.echelon_1` |
| `2001-1002` (Decret) | 2001-05-08 | 2001-05-01 | 7 j | 114 | 5 | `fonction_publique.enseignants_education_physique.professeur_education_physique.indemnite_specifique_mensuelle.echelon_1` |
| `2011-1262` (Decret) | 2011-09-05 | 2011-02-01 | 216 j | 100 | 4 | `fonction_publique.controleurs_reglements_municipaux.attache_inspection_reglements_municipaux.indemnite_specifique_mensuelle.echelon_1` |
| `1999-2189` (Decret) | 1999-10-04 | 1999-08-06 | 59 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2001-1159` (Decret) | 2001-05-22 | 2001-05-01 | 21 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2002-2851` (Decret) | 2002-10-29 | 2002-05-01 | 181 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2003-1235` (Decret) | 2003-06-02 | 2003-05-01 | 32 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2004-1349` (Decret) | 2004-06-07 | 2004-05-01 | 37 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2005-3214` (Decret) | 2005-12-12 | 2005-05-01 | 225 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2006-1794` (Decret) | 2006-06-26 | 2006-05-01 | 56 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2008-4100` (Decret) | 2008-12-30 | 2008-05-01 | 243 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2009-1508` (Decret) | 2009-05-18 | 2009-05-01 | 17 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2012-2973` (Decret) | 2012-11-29 | 2012-05-01 | 212 j | 100 | 4 | `fonction_publique.maitres_auxiliaires_education.maitre_auxiliaire_de_la_categorie_a.indemnite_specifique_mensuelle.echelon_1` |
| `2017-990` (Decret gouvernemental) | 2017-08-17 | 2016-01-26 | 569 j | 75 | 3 | `fonction_publique.enseignants_de_langue_anglaise_et_d_informatique.professeur_principal_emerite.indemnite_specifique_mensuelle.echelon_1` |
| `2001-2591` (Decret) | 2001-11-09 | 2001-11-01 | 8 j | 73 | 3 | `fonction_publique.enseignants_technologues.maitre_technologue.indemnite_specifique_mensuelle.echelon_1` |
| `2013-1406` (Decret) | 2013-04-22 | 2013-01-01 | 111 j | 66 | 3 | `fonction_publique.medecins_dentistes_hospitalo_universitaires.assistant_hospitalo_universitaire_en_medecine_dentaire.indemnite_specifique_mensuelle.echelon_1` |
| `2013-1407` (Decret) | 2013-04-22 | 2013-01-01 | 111 j | 66 | 3 | `fonction_publique.medecins_dentistes_hospitalo_universitaires.assistant_hospitalo_universitaire_en_medecine_dentaire.indemnite_specifique_mensuelle.echelon_1` |
| `2013-1408` (Decret) | 2013-04-22 | 2013-01-01 | 111 j | 66 | 3 | `fonction_publique.pharmaciens_hospitalo_universitaires.assistant_hospitalo_universitaire_en_pharmacie.indemnite_specifique_mensuelle.echelon_1` |
| `2013-1409` (Decret) | 2013-04-22 | 2013-01-01 | 111 j | 66 | 3 | `fonction_publique.pharmaciens_hospitalo_universitaires.assistant_hospitalo_universitaire_en_pharmacie.indemnite_specifique_mensuelle.echelon_1` |
| `2013-1403` (Decret) | 2013-04-22 | 2013-01-01 | 111 j | 64 | 3 | `fonction_publique.medecins_hospitalo_universitaires.assistant_hospitalo_universitaire_en_medecine.indemnite_specifique_mensuelle.echelon_1` |
| `2013-1405` (Decret) | 2013-04-22 | 2013-01-01 | 111 j | 64 | 3 | `fonction_publique.medecins_hospitalo_universitaires.assistant_hospitalo_universitaire_en_medecine.indemnite_specifique_mensuelle.echelon_1` |
| `2017-990` (Decret gouvernemental) | 2017-08-17 | 2015-09-04 | 713 j | 50 | 2 | `fonction_publique.enseignants_de_langue_anglaise_et_d_informatique.professeur.indemnite_specifique_mensuelle.echelon_1` |
| `2021-59` (Décret gouvernemental) | 2021-01-21 | 2020-02-28 | 328 j | 16 | 1 | `fonction_publique.corps_administratif_commun.administrateur_general_classe_superieure.indemnite_specifique_mensuelle.echelon_1` |
| `2010-1746` (Decret) | 2010-07-17 | 2010-07-01 | 16 j | 8 | 8 | `marche_travail.salaire_de_base_40h_horaire` |
| `2011-679` (Decret) | 2011-06-09 | 2011-05-01 | 39 j | 8 | 8 | `marche_travail.salaire_de_base_40h_horaire` |
| `2012-1981` (Decret) | 2012-09-20 | 2012-07-01 | 81 j | 8 | 8 | `marche_travail.salaire_de_base_40h_horaire` |
| `2014-2907` (Decret) | 2014-08-11 | 2014-05-01 | 102 j | 8 | 8 | `marche_travail.salaire_de_base_40h_horaire` |
| `2020-317` (Décret gouvernemental) | 2020-05-19 | 2020-01-01 | 139 j | 8 | 8 | `prestations.non_contributives.amen_social.eligibilite.deux_membres` |
| `1960-30` (Loi) | 1960-12-14 | 1960-01-01 | 348 j | 7 | 7 | `prestations.contributives.prestations_familiales.af.nb_enfants_max` |
| _…et 103 autres couples_ | | | | | | |

Les dix écarts les plus larges, à regarder en premier :

| Texte cité | Signé le | Date de valeur | Écart | Paramètres |
| --- | --- | --- | ---: | ---: |
| `1993-308` (Decret) | 1993-02-01 | 1974-06-01 | 6820 j | 1 |
| `2018-786` (Decret gouvernemental) | 2018-09-21 | 2014-01-21 | 1704 j | 137 |
| `2017-990` (Decret gouvernemental) | 2017-08-17 | 2015-09-04 | 713 j | 50 |
| `2017-990` (Decret gouvernemental) | 2017-08-17 | 2016-01-26 | 569 j | 75 |
| `2014-45` (Decret) | 2014-01-10 | 2013-01-01 | 374 j | 266 |
| `2004-90` (Loi) | 2004-12-31 | 2004-01-01 | 365 j | 2 |
| `1962-73` (Loi) | 1962-12-31 | 1962-01-01 | 364 j | 2 |
| `1965-46` (Loi) | 1965-12-31 | 1965-01-01 | 364 j | 2 |
| `2013-54` (Loi) | 2013-12-30 | 2013-01-01 | 363 j | 6 |
| `1997-88` (Loi) | 1997-12-29 | 1997-01-01 | 362 j | 4 |

### Dates de valeur qu'aucune référence ne couvre — 3058 paramètres dans 158 fichiers, dont **361 à valeur non nulle**

Le paramètre porte une référence datée, mais l'une de ses dates de valeur n'y figure pas : cette valeur-là n'est fondée par rien.

La distinction compte. Une date non couverte portant une valeur **nulle** — 2697 des 3058 — marque d'ordinaire la création d'un grade, et son absence de source ne prête pas à conséquence. Les autres sont des **montants non sourcés**, et c'est là la lacune indiscutable. Le tableau est classé sur cette colonne.

| Fichier | Dates non couvertes | Paramètres | dont valeur non nulle |
| --- | --- | ---: | ---: |
| `fonction_publique/enseignants_ecoles_primaires/maitre/traitement_de_base.yaml` | 2013-06-07 | 25 | 25 |
| `fonction_publique/enseignants_ecoles_primaires/maitre_de_l_education_manuelle_et_technique/traitement_de_base.yaml` | 2013-06-07 | 25 | 25 |
| `fonction_publique/maitres_auxiliaires_education/maitre_auxiliaire_de_la_categorie_a/indemnite_specifique_mensuelle.yaml` | 2013-01-01 | 25 | 25 |
| `fonction_publique/maitres_auxiliaires_education/maitre_auxiliaire_de_la_categorie_b/indemnite_specifique_mensuelle.yaml` | 2013-01-01 | 25 | 25 |
| `fonction_publique/maitres_auxiliaires_education/maitre_auxiliaire_de_la_categorie_c/indemnite_specifique_mensuelle.yaml` | 2013-01-01 | 25 | 25 |
| `fonction_publique/maitres_auxiliaires_education/maitre_auxiliaire_de_la_categorie_d/indemnite_specifique_mensuelle.yaml` | 2013-01-01 | 25 | 25 |
| `fonction_publique/enseignants_ecoles_primaires/maitre_dapplication/traitement_de_base.yaml` | 2013-06-07 | 24 | 24 |
| `fonction_publique/enseignants_ecoles_primaires/maitre_dapplication_de_l_education_manuelle_et_technique/traitement_de_base.yaml` | 2013-06-07 | 24 | 24 |
| `fonction_publique/infirmiers_de_la_sante_publique/infirmier_principal_de_la_sante_publique/traitement_de_base.yaml` | 2011-07-12 | 24 | 24 |
| `fonction_publique/enseignants_lycees/professeur_de_l_enseignement_hors_classe/traitement_de_base.yaml` | 2015-09-04 | 20 | 20 |
| `fonction_publique/enseignants_lycees/professeur_de_l_enseignement_principal_hors_classe/traitement_de_base.yaml` | 2015-09-04 | 20 | 20 |
| `fonction_publique/enseignants_lycees/professeur_de_l_enseignement_secondaire_emerite/traitement_de_base.yaml` | 2015-09-04 | 20 | 20 |
| `fonction_publique/surveillants_generaux_education/surveillant_general_en_chef/traitement_de_base.yaml` | 2014-05-06 | 20 | 20 |
| `fonction_publique/surveillants_generaux_education/surveillant_general_en_chef_hors_classe/traitement_de_base.yaml` | 2014-05-06 | 20 | 20 |
| `fonction_publique/enseignants_lycees/professeur_principal_emerite/traitement_de_base.yaml` | 2015-09-04 | 16 | 16 |
| `impot_revenu/deductions/cea_cei/cea.yaml` | 1990-01-01, 2001-01-01 | 1 | 1 |
| `impot_revenu/deductions/famille/chef_de_famille.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/deductions/famille/enf1.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/deductions/famille/enf2.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/deductions/famille/enf3.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/deductions/famille/enf4.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/deductions/investissements/taux_plafond_partiel.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/regimes_speciaux/forfaitaire/taux_imposition.yaml` | 2014-01-01 | 1 | 1 |
| `impot_revenu/regimes_speciaux/retenue_liberatoire/taux.yaml` | 1990-01-01 | 1 | 1 |
| `impot_revenu/tspr/abat_pen.yaml` | 1990-01-01, 2028-01-01, 2029-01-01 | 1 | 1 |
| `prelevements_sociaux/contribution_sociale_solidarite/entreprise/taux_is_15_20_25_pc/montant_minimum.yaml` | 2018-01-01 | 1 | 1 |
| `prelevements_sociaux/contribution_sociale_solidarite/entreprise/taux_is_35_pc/montant_minimum.yaml` | 2018-01-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/raci/cotisations_salarie/assurances_sociales/maladie.yaml` | 2007-07-01, 2008-07-01, 2009-07-01, 2010-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rsa/cotisations_employeur/assurances_sociales/maladie.yaml` | 2007-07-01, 2008-07-01, 2009-07-01, 2010-07-01, 2011-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rsa/cotisations_salarie/assurances_sociales/maladie.yaml` | 2007-07-01, 2008-07-01, 2009-07-01, 2010-07-01, 2011-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rsaa/cotisations_employeur/assurances_sociales/maladie.yaml` | 2007-07-01, 2008-07-01, 2009-07-01, 2010-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rsaa/cotisations_salarie/assurances_sociales/maladie.yaml` | 2008-07-01, 2009-07-01, 2010-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rsna/cotisations_employeur/assurances_sociales/maladie.yaml` | 2007-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rsna/cotisations_salarie/assurances_sociales/maladie.yaml` | 2008-07-01, 2009-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rtns/cotisations_salarie/assurances_sociales/maladie.yaml` | 2007-07-01, 2008-07-01, 2009-07-01, 2010-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_prive/rtte/cotisations_salarie/assurances_sociales/maladie.yaml` | 2007-07-01, 2008-07-01, 2009-07-01 | 1 | 1 |
| `prelevements_sociaux/cotisations_sociales/secteur_public/salarie_cnrps/cotisations_employeur/maladie.yaml` | 1959-02-01 | 1 | 1 |
| `prestations/non_contributives/pnafn/allocation.yaml` | 1987-01-01, 2000-01-01, 2009-01-01, 2009-07-01, 2010-07-01, 2011-07-01, 2012-04-01, 2013-07-01, 2014-07-01, 2015-01-01 | 1 | 1 |
| `fonction_publique/agents_affaires_culturelles/administrateur_adjoint_services_culturels/indemnite_specifique_mensuelle.yaml` | 2019-05-21 | 25 | 0 |
| `fonction_publique/agents_affaires_culturelles/administrateur_conseiller_services_culturels/indemnite_specifique_mensuelle.yaml` | 2019-05-21 | 25 | 0 |
| _…et 118 autres_ | | | |

