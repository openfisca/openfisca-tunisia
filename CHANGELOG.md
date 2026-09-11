# Changelog

## 0.81 - [#404](https://github.com/openfisca/openfisca-tunisia/pull/404)

* Évolution du système socio-fiscal.
* Périodes concernées : du 1989-08-01 au 1992-04-30, du 2014-05-01 au 2017-06-04, et à partir du 2020-10-01.
* Zones impactées : `parameters/marche_travail`.
* Détails :
  - **Sépare le SMIG de l'indemnité spéciale de 1989-1991.** Les quatre séries du SMIG portaient au 1er août 1989, au 1er janvier 1990 et au 1er août 1991 le SMIG augmenté de l'indemnité spéciale (123,016 D au lieu de 120,016 D en 1990, régime de 48 heures). Or l'indemnité n'est pas le SMIG : le décret n° 89-1551 l'institue « au profit des travailleurs payés au » SMIG, l'exclut de l'assiette des cotisations et des prestations de sécurité sociale (art. 5) et suspend à son titre les retenues d'impôt (art. 4) ; le décret n° 91-1316, qui la porte à 5 D, reprend les deux clauses (art. 4 et 5). Le SMIG légal est celui du décret n° 90-246 (JORT n° 13 du 16 février 1990, p. 252) : **120,016 D et 104,706 D par mois, 577 et 604 millimes l'heure**. Les valeurs du 1er août 1989 et du 1er août 1991, dates où seul le montant de l'indemnité change, sont supprimées. L'indemnité reste portée par `indemnite_speciale_smig`, jusqu'à son intégration au SMIG par l'article 3 du décret n° 92-1299 au 1er mai 1992.
  - Même correction pour le SMAG : **3,546 D** par jour au 1er janvier 1990 (décret n° 90-247, art. 1er) au lieu de 3,661 D, qui comptait l'indemnité spéciale agricole de 115 millimes (décret n° 89-1552) ; suppression des valeurs du 1er août 1989 et du 1er août 1991. Dans `indemnite_speciale_smag`, supprime la valeur du 1er janvier 1990, rattachée au décret n° 90-247, qui ne touche pas l'indemnité.
  - Tous les usages de ces paramètres visent le SMIG ou le SMAG légal : cotisations du régime des travailleurs à faible revenu et assiette de la retraite complémentaire (`cotisations_sociales`), prestations familiales et contribution aux frais de crèche, seuils de l'AMEN social, indicatrice `smig` et abattement de l'IRPP (`tspr`, `irpp`). Aucun ne doit compter une indemnité exclue des cotisations, des prestations et de la retenue d'impôt.
  - Conséquence pour la revalorisation des pensions indexées sur le SMIG : la hausse du 1er mai 1992 est de **+10,75 %** (120,016 → 132,912 D), dont les 5 D d'indemnité intégrée, et non de +6,32 %.
  - Ajoute le SMIG au **1er janvier 2026, 2027 et 2028** (décret n° 2026-67, JORT n° 44 du 30 avril 2026, pp. 838-839) : 554,736 / 582,400 / 611,520 D (48 heures, mensuel), 470,251 / 493,304 / 517,571 D (40 heures), 2,667 / 2,800 / 2,940 D et 2,713 / 2,846 / 2,986 D l'heure.
  - Ajoute le SMAG journalier manquant : **16,512 D** au 1er octobre 2020 (n° 2020-1070), **17,664 D** au 1er octobre 2022 (n° 2022-768), **18,904 D** au 1er mai 2024 et **20,320 D** au 1er janvier 2025 (n° 2024-420), **21,336 / 22,400 / 23,520 D** aux 1er janvier 2026, 2027 et 2028 (n° 2026-66).
  - Redate trois valeurs du SMAG qui portaient la date de signature du décret : 12,304 D au **1er mai 2014** (n° 2014-2908, art. 6), 13 D au **1er mai 2015** (n° 2015-1763, art. 6), 13,736 D au **1er août 2016** (n° 2017-669, art. 6). Toutes les dates de ce changement sont des dates d'effet énoncées par le texte.
  - Corrige l'intitulé du décret SMAG n° 2009-2258, daté du 14 juillet 2009 et non du 2 juin.
  - Chaque entrée touchée renvoie au fascicule du JORT sur pist.tn, éditions française et arabe, avec numéro, page, article et clause d'effet. Le fascicule n° 45 de 2017 n'est servi qu'en arabe : la référence du SMAG du 1er août 2016 pointe vers l'édition arabe, où le texte a été lu.

<!-- -->

## 0.80 - [#402](https://github.com/openfisca/openfisca-tunisia/pull/402)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/retraite`.
* Détails :
  - Supprime `parameters/retraite/` — trente fichiers que **rien ne lisait**. Aucun `.py`, `.yaml` ou `.ipynb` de ce paquet n'accède à `retraite.cnrps`, `retraite.rsna` ni `retraite.rsa` ; les variables de retraite d'ici sont toutes des variables d'entrée sans formule, de simples réceptacles pour l'IRPP et l'AMEN social, et elles restent.
  - Ces paramètres vivent, eux, dans `openfisca-tunisia-pension`, où ils sont lus par les formules de liquidation. Vingt-huit des trente fichiers y existaient à l'identique : c'était une seconde source de vérité pour les mêmes paramètres de droit, et elle avait déjà commencé à diverger dans ses métadonnées.
  - **La règle qui en découle** : un sous-arbre de paramètres a un propriétaire et un seul. `retraite/` appartient à `openfisca-tunisia-pension`, `marche_travail/` à ce paquet-ci. Le pendant de ce changement est la PR openfisca-tunisia-pension#23, qui greffe `marche_travail` depuis ici au lieu d'en garder une copie — laquelle avait figé le SMIG en 2019.
  - Les trois éléments que seule cette arborescence portait ont été récoltés avant suppression : l'URL du fascicule du JORT sur les âges légaux du cadre commun et des cadres actifs, le paragraphe sur l'option de report des enseignants du supérieur, et `rsna/plaf_taux_pension.yaml`.

<!-- -->

## 0.79 - [#398](https://github.com/openfisca/openfisca-tunisia/pull/398)

* Correction d'un bug.
* Périodes concernées : à partir du 1974-01-01.
* Zones impactées : `parameters/prelevements_sociaux/cotisations_sociales/secteur_prive`.
* Détails :
  - Date les **37 valeurs du secteur privé qui portaient le 1er janvier 1960** sans aucune référence. La structure qu'elles décrivent n'existe pas avant 1997 : le taux du régime général est la somme des 18 % répartis 13/5 de l'article 41 (nouveau) de la **loi n° 97-4** (publiée le 4 février 1997), du fonds spécial de l'État de l'article 57 de la **loi n° 74-101** (1er janvier 1975) et de la cotisation propre du régime de pensions de l'article 9 (nouveau) du **décret n° 97-555** — soit 23,75 %, dont les 16,00 % et 7,75 % que porte le modèle avant assurance maladie. La dernière pièce est le **décret n° 2003-1212**, qui porte la quote-part des pensions à 7,25/20e au 1er janvier 2003.
  - Date les autres régimes sur leurs textes : **1981-02-24** pour les salariés agricoles (loi n° 81-6, décret n° 81-224), **1989-10-01** pour le régime agricole amélioré (loi n° 89-73, art. 4 et 90), **1995-07-03** pour les travailleurs non salariés (décret n° 95-1166), **2002-12-31** pour les artistes (loi n° 2002-104), **1989-01-10** pour les Tunisiens à l'étranger (décret n° 89-107), **1995-04-01** pour le point transféré aux accidents du travail (décret n° 95-538), **1996-11-22** pour la protection sociale des travailleurs (loi n° 96-101) et **1974-01-01** pour la retraite complémentaire (arrêté du 18 novembre 1978).
  - Ajoute la valeur manquante de la **cotisation des étudiants** : la série commençait à 5 dinars, alors que le décret n° 92-631 la fixe d'abord à **2 dinars**.
  - Remplace **toutes** les références du secteur privé — dépôt GitLab personnel et, pour la perte d'emploi, un site commercial — par les fascicules du JORT sur pist.tn, avec numéro de fascicule, page et lien vers l'édition arabe. La référence de la perte d'emploi pointe vers l'édition arabe : l'édition française de ce fascicule répond 404, et c'est dans l'arabe que l'article 17 de la loi n° 2024-48 a été lu.
  - Consigne dans les notes trois défauts de structure qui appellent des correctifs distincts : le point d'accidents du travail n'est pas le tarif d'accidents du travail (patronal, de 0,50 % à 5 % selon dix-huit classes) ; le seuil de 0,66 du régime des bas revenus est une assiette forfaitaire et non un plafond, et ses quatre valeurs croisent deux répartitions que les textes ne croisent jamais ; l'assiette de la retraite complémentaire est la fraction de salaire excédant la limite de calcul des prestations, et son taux de 9 % n'a aucune source publiée.
  - **Aucune valeur de taux n'est modifiée** : les tableaux engendrés par le précis socio-fiscal sont identiques avant et après.

<!-- -->

## 0.78 - [#397](https://github.com/openfisca/openfisca-tunisia/pull/397)

* Correction d'un bug.
* Périodes concernées : à partir du 1959-02-01.
* Zones impactées : `parameters/prelevements_sociaux/cotisations_sociales/secteur_public`.
* Détails :
  - Supprime le palier salarié du **1er juin 2019** (8,7 %), que le texte contredit. L'article 4 de la loi n° 2019-37 (JORT n° 35, p. 1314) répartit les 3 points ainsi : « Au titre de l'employeur : 2 % à partir du premier jour du mois qui suit la date d'entrée en vigueur de la présente loi. Au titre de l'agent : 1 % à partir du premier janvier 2020. » La part salariale monte donc d'un point **en une seule fois** au 1er janvier 2020 ; la date de juin 2019 vaut pour la part patronale seule.
  - Redate la deuxième marche patronale de la loi n° 2007-43 au **1er janvier 2008** : le texte (p. 2198) donne 0,60 point au 1er janvier 2007, 2008 et 2009 côté employeur, contre 0,40 au 1er juillet côté salarié. Le fichier datait 2007 et 2009 en janvier et 2008 en juillet, se contredisant lui-même.
  - Fait commencer la **prévoyance sociale des pensionnés au 1er juillet 2007** au lieu de 1959. Le décret n° 2007-1406 (JORT n° 49, art. 2 p. 2156, art. 13 p. 2162) assied la cotisation sur le montant brut de la pension et échelonne le taux à 1, 2, 3 puis 4 %. Aucun texte antérieur établissant un prélèvement obligatoire sur la pension n'a pu être retrouvé.
  - Redate le millésime de **1985 au 12 septembre**, six mois après la publication du 12 mars comme l'article 75 de la loi n° 85-12 le prescrit. Le taux est inchangé de part et d'autre : ce millésime marque la refonte du régime, non un mouvement de taux.
  - Remplace **toutes** les références du secteur public — dépôt GitLab personnel et natlex — par les fascicules du JORT sur pist.tn, en éditions française et arabe, avec numéro de fascicule et page. Chaque URL a été vérifiée, et les deux éditions distinguées par la taille du fichier.
  - Référence les quatre paliers de 2003, 2004, 2008 et 2009, qui n'avaient aucun texte en regard : ils sont programmés par les échéanciers pluriannuels de l'article 85 de la loi de finances 2002 et de l'article premier de la loi n° 2007-43, et non par des textes distincts.
  - Corrige la date de création de la CNRPS dans les deux `index.yaml` : l'article 28 de la loi n° 75-83 du **30** décembre 1975 (et non du 31) « transforme en un établissement public à caractère financier » la CNR et la CPS.
  - Signale dans la note du paramètre que la date du **1er février 1959 n'a aucun appui textuel** : la loi n° 59-18 n'énonce pas d'effet pour son article 5, et sa seule date — le 1er avril 1959 — porte sur l'ouverture des droits à pension.

<!-- -->

## 0.77 - [#396](https://github.com/openfisca/openfisca-tunisia/pull/396)

* Correction d'un bug.
* Périodes concernées : à partir du 2020-05-20.
* Zones impactées : `parameters/prestations/non_contributives/amen_social/aides_ponctuelles`.
* Détails :
  - Date les cinq aides ponctuelles de l'AMEN social sur leur texte. Elles portaient le 1er janvier **2019**, qui n'est la date d'aucun texte : l'appui financier occasionnel est fixé par l'arrêté conjoint du **19 mai 2020**, publié au JORT n° 45 du 20 mai 2020, p. 1097. Les montants — 60 D pour le Ramadan, l'Aïd al-Fitr et l'Aïd al-Idha, 50 D par enfant à la rentrée scolaire, 120 D dans le supérieur — étaient exacts. Aucun des cinq ne portait de référence ; tous en ont désormais deux, l'arrêté du 8 décembre 2022 ayant abrogé celui de 2020 en reprenant les mêmes montants.
  - Ajoute l'**appui pour dépenses exceptionnelles** créé par l'arrêté du 8 décembre 2022, absent du modèle. Son montant n'est pas fixe : il est compris **entre 60 et 200 dinars** selon la situation financière de la famille, et servi **quatre fois par an au plus**. D'où trois paramètres — deux bornes et un compte — plutôt qu'une valeur unique qui aurait inventé un barème.
  - Documente ce qui n'est **pas** modélisé et pourquoi : la prise en charge des abonnements de transport scolaire et universitaire n'a pas de montant propre, le texte renvoyant aux tarifs des entreprises de transport public.

<!-- -->

## 0.76 - [#395](https://github.com/openfisca/openfisca-tunisia/pull/395)

* Correction d'un bug.
* Périodes concernées : à partir du 2020-05-20.
* Zones impactées : `parameters/prestations/non_contributives/amen_social`.
* Détails :
  - Ajoute `supplements/age_min_enfant`, borne basse d'âge du supplément par enfant du transfert monétaire permanent. Le modèle ne connaissait que la borne haute. Cette borne passe de 0 à **6 ans** le 1er février 2022, jour où l'allocation familiale non contributive de 30 dinars prend en charge les enfants de moins de six ans : c'est une **règle de non-cumul**, sans laquelle un enfant de moins de six ans ouvre droit aux deux prestations à la fois.
  - Corrige la date d'effet de l'allocation de base, portée du 1er au **20 mai 2020** : l'arrêté conjoint du 19 mai 2020 est publié au JORT n° 45 du 20 mai 2020, p. 1097, et aucun texte n'énonce le 1er mai.
  - Réaligne `metadata.official_journal_date` sur les dates de valeur, dont il avait divergé (clés 2022-04-01, 2023-04-01, 2024-03-01 pour des valeurs datées du 1er janvier), et ajoute la référence du palier 2025, qui n'en avait aucune.

<!-- -->

## 0.75 - [#393](https://github.com/openfisca/openfisca-tunisia/pull/393)

* Correction d'un bug.
* Périodes concernées : toutes.
* Zones impactées : `parameters/prestations/non_contributives`.
* Détails :
  - Corrige deux **références apocryphes** : le « décret n° 2019-318 » et l'« arrêté 931 du 20 mai 2020 » cités par les suppléments du programme AMEN social n'existent pas. La disposition figure à l'article 2 de l'arrêté conjoint du 19 mai 2020.
  - Corrige la limite d'âge de l'étudiant ouvrant droit au supplément : **25 ans** et non 21.
  - Redate l'allocation familiale non contributive à **avril 2022** et non juin 2020. Ce qui existait en 2020 est le supplément pour enfant à charge du transfert AMEN, dispositif distinct avec lequel elle ne se cumule pas.
  - Redate le droit annuel d'affiliation à l'AMG2 à **février 1998** (décret n° 98-409, art. 10) et non 2015.
  - Ajoute le palier de **260 dinars au 1er janvier 2025** de l'allocation de base du programme AMEN social.
  - Documente que les onze paliers de l'allocation du PNAFN **n'ont aucun texte**, ce qui est un résultat établi et non une lacune, et que les montants de 240 et 260 dinars des arrêtés de 2024 et 2025 sont des **plafonds sur un relèvement**, non des barèmes : les encoder comme valeurs serait une sur-interprétation.

<!-- -->

## 0.74 - [#392](https://github.com/openfisca/openfisca-tunisia/pull/392)

* Correction d'un bug.
* Périodes concernées : toutes.
* Zones impactées : `parameters/prestations/contributives/prestations_familiales`.
* Détails :
  - Corrige les treize valeurs des prestations familiales, toutes datées du 1er janvier 1960 alors qu'**aucune ne date de 1960**. Les taux de 18, 16 et 14 % viennent de la loi n° 75-82 (revenus 1976), le plafond de 122 dinars de la loi n° 86-75 (mai 1986) et non de la loi n° 88-38 qui était citée, la majoration pour salaire unique de la loi n° 80-36 (mai 1980), la contribution aux frais de crèche de la loi n° 94-88 et du décret n° 95-114 (octobre 1994).
  - Ajoute l'état d'origine du barème, absent : l'article 61 de la loi n° 60-30 ne connaît qu'un taux **unique de 15 %** appliqué à une **bande d'assiette de 52 à 500 dinars**, et non un plafond simple.
  - Crée trois paramètres sans lesquels la période 1960-1988 est inreprésentable : `af/plancher_trim` (borne basse de la bande, clôturée en 1976), `af/taux/enf4` (quatrième rang, clôturé en 1989) et `af/nb_enfants_max` (quatre enfants, ramené à trois par la loi n° 88-38).
  - Ajoute à chaque paramètre sa référence JORT avec URL pist.tn, page et date d'effet énoncée par le texte.

<!-- -->

## 0.73 - [#386](https://github.com/openfisca/openfisca-tunisia/pull/386)

* Correction d'un bug.
* Périodes concernées : toutes.
* Zones impactées : `parameters/impot_revenu/tspr`, `parameters/impot_revenu/minimum_impot`.
* Détails :
  - Complète l'abattement sur les pensions de source étrangère, qui ne connaissait que le régime de faveur de 80 %. Trois régimes successifs sont désormais encodés et sourcés : aucun abattement de 1990 à 1996, 25 % par renvoi à l'article 26 à partir des revenus 1997 (article 61 de la loi de finances 1998), 80 % à partir des pensions perçues en 2006. La borne 2001 sans support est supprimée.
  - Établit la date du minimum d'impôt au titre des avantages fiscaux : le taux de 60 % s'applique **à partir du 1er janvier 1999** en vertu de l'article 62 de la loi de finances pour 1998, et non de 2014 comme encodé jusqu'ici sans support.

<!-- -->

## 0.72 - [#385](https://github.com/openfisca/openfisca-tunisia/pull/385)

* Ajout de paramètres.
* Périodes concernées : toutes.
* Zones impactées : `parameters/impot_revenu/deductions`.
* Détails :
  - Date la déduction des intérêts de l'épargne de l'article 39 § II du code, dont les deux paramètres étaient figés à leur valeur de 1990. Plafond global : 1 000 D en 1990, 1 500 D en 1992, 5 000 D en 2016, 10 000 D en 2021. Sous-plafond des comptes spéciaux d'épargne : 1 000 D, puis 3 000 D en 2016 et 6 000 D en 2021. La valeur de 1990 du plafond global est corrigée de 1 500 à 1 000 D : le code d'origine ne connaît qu'un plafond unique, la structure à deux niveaux datant de la loi de finances 1992.
  - Corrige et complète les plafonds de déduction des primes d'assurance-vie. La valeur d'origine est de 200 dinars et non 800, la majoration pour conjoint de 100 dinars et non 400, celle par enfant de 50 dinars et non 200 : les valeurs encodées étaient celles de l'article 52 de la loi de finances 1998, rattachées à 1990. Ce palier de 1997 est ajouté, ce qui complète la série. Corrige également deux dates : 10 000 D aux revenus 2013 et non 2014, 100 000 D aux revenus 2020 et non 2021.

<!-- -->

## 0.71 - [#383](https://github.com/openfisca/openfisca-tunisia/pull/383)

* Correction d'un bug.
* Périodes concernées : jusqu'au 31/12/2010.
* Zones impactées : `variables/prelevements_obligatoires/impot_revenu/revenus_categoriels/tspr`.
* Détails :
  - Corrige `revenu_assimile_salaire_apres_abattements` : la formule applicable avant 2011 encadrait le résultat par `min_(..., 0)` au lieu de `max_(..., 0)`. Le revenu après abattements était donc systématiquement nul, et **l'IRPP de tous les salariés était nul pour les revenus antérieurs à 2011**. Un salaire imposable de 20 000 D en 2010 donne désormais 3 525 D d'impôt au lieu de 0.

<!-- -->

## 0.70 - [#382](https://github.com/openfisca/openfisca-tunisia/pull/382)

* Correction d'un bug.
* Périodes concernées : toutes.
* Zones impactées : `parameters/impot_revenu/tspr`, `parameters/impot_revenu/deductions/famille`, `parameters/impot_revenu/foncier`, `parameters/impot_revenu/bnc`, `parameters/impot_revenu/minimum_impot`.
* Détails :
  - Corrige le plafond de la déduction pour frais professionnels sur les salaires : il était encodé à 2 000 D dès 1990, alors que l'article 14 § 2 de la loi de finances 2017 le **crée**. De 1990 à 2016 inclus, la déduction de 10 % est sans limite. L'assiette salariale était surestimée pour tous les revenus supérieurs à 20 000 D sur 27 exercices.
  - Corrige l'abattement pour salaire minimum, qui restait appliqué alors qu'il est abrogé à compter des revenus 2014 par l'article 73 § 2 de la loi de finances 2014.
  - Corrige la déduction forfaitaire des revenus fonciers bâtis : 30 % dès 1990 et non 2007, bascule à 20 % aux revenus 2015 et non 2016, et ajout du relèvement à 25 % aux revenus 2024, absent.
  - Corrige les dates des déductions pour charges de famille (enfant infirme, enfant étudiant, parent à charge) et supprime une valeur d'enfant infirme de 2004 sans support. Corrige le numéro d'article cité pour le chef de famille et les enfants (article 54 et non 55 de la loi de finances 2018).
  - Corrige la date du minimum d'impôt au titre des avantages fiscaux : 45 % à partir du 1er avril 2017 et non de 2020.
  - Corrige la part forfaitaire des bénéfices non commerciaux (70 % dès 1990) et l'abattement sur pensions étrangères (80 % aux revenus 2006 et non 2007).
  - Ajoute à chaque paramètre corrigé ses références JORT et une documentation distinguant les dates attestées par note commune des dates dérivées de la règle de conversion en années de revenus.

<!-- -->

## 0.69 - [#381](https://github.com/openfisca/openfisca-tunisia/pull/381)

* Ajout de paramètres.
* Périodes concernées : du 01/01/1962 au 31/12/1989.
* Zones impactées : `parameters/impot_revenu/contribution_personnelle_etat`.
* Détails :
  - Ajoute le tarif de la contribution personnelle d'État, impôt progressif sur le revenu global institué par le décret du 31 mars 1932 et supprimé pour les revenus réalisés à compter du 1er janvier 1990. Cinq rédactions successives de l'article 8 : revenus 1962 (31 tranches, 80 % au-delà de 10 200 D), revenus 1965 (30 tranches, 88 % au-delà de 9 800 D), revenus 1980 (11 tranches, 80 % au-delà de 8 500 D), revenus 1983 (20 tranches, 80 % au-delà de 100 000 D) et revenus 1986 (18 tranches, 68 % au-delà de 80 000 D), avec leurs références JORT.
  - Ajoute le plafond de cotisation effective (40 % pour les revenus 1962, puis 45 %, 55 % et 60 % à partir des revenus 1983), qui n'a pas d'équivalent dans l'IRPP et qui tempère fortement des taux marginaux nominaux très élevés.
  - Aucune variable ne consomme ces paramètres : le modèle ne calcule pas l'avant-1990. Ils servent de référence datée et sourcée. Des tests vérifient que la colonne des taux d'imposition à la limite supérieure, imprimée dans les textes de loi, se déduit du tarif encodé.

<!-- -->

## 0.68 - [#380](https://github.com/openfisca/openfisca-tunisia/pull/380)

* Correction d'un bug.
* Périodes concernées : jusqu'au 31/12/2016.
* Zones impactées : `parameters/impot_revenu/bareme`, `parameters/impot_revenu/exoneration`.
* Détails :
  - Corrige le barème de l'IRPP applicable aux revenus de 1990 à 2016 : la tranche supérieure était absente. Le barème encodé s'arrêtait à « au-delà de 20 000 D : 30 % », alors que l'article 44 § I du code de l'IRPP et de l'IS institue une tranche de 20 000,001 à 50 000 D à 30 % puis une tranche à 35 % au-delà de 50 000 D. Les revenus nets imposables supérieurs à 50 000 D étaient sous-imposés.
  - Ajoute les références JORT (avec URL pist.tn) des trois millésimes du barème : code annexé à la loi n° 89-114 (JORT n° 1 du 2-5 janvier 1990, p. 9), article 14-1 de la loi n° 2016-78 (JORT n° 105 du 27 décembre 2016, p. 3831) et article 36 de la loi n° 2024-48 (JORT n° 149 du 10 décembre 2024, p. 6429).
  - Documente le seuil d'exonération de 2014 : il s'agit d'une exonération catégorielle des salariés et pensionnés, abrogée à compter des revenus de 2017, et non de l'ancêtre de la tranche à 0 % du barème.

<!-- -->

## 0.67 - [#369](https://github.com/openfisca/openfisca-tunisia/pull/369)

* Ajout de paramètres.
* Périodes concernées : toutes.
* Zones impactées : `parameters/fonction_publique`.
* Détails :
  - Injecte les indemnités spécifiques mensuelles reconstruites depuis les sources primaires pour 10 corps (campagne 2026-06) ; retire la note « valeurs 0 nominales » pour les corps concernés.
  - Ré-encode 4 grades d'`enseignants_lycees` de 16/20 à 25 échelons (concordance identité 2015-1165) et ajoute 2 grades de classe exceptionnelle (2015-1163).
  - Ajoute 5 corps nouveaux au format master : `cadres_techniques_administration`, `enseignement_secondaire_technique_professionnel`, `maitres_principaux_eps`, `personnel_institutions_formation_sante`, `surveillants_generaux_education`.

<!-- -->

## 0.66 - [#370](https://github.com/openfisca/openfisca-tunisia/pull/370)

* Amélioration technique.
* Périodes concernées : aucune.
* Détails :
  - Mise à jour des dépendances de sécurité : pillow, pygments, requests, tornado, werkzeug, mistune, nbconvert, cryptography, flask, fonttools.

<!-- -->

## 0.65 - [#369](https://github.com/openfisca/openfisca-tunisia/pull/369)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/fonction_publique`.
* Détails :
  - Ajoute des libellés courts aux paramètres de traitement de base et d'indemnité spécifique mensuelle.
  - Ajoute des libellés courts aux échelons, tout en conservant des descriptions autonomes.
  - Reformule les descriptions des corps, grades, paramètres et échelons avec des libellés lisibles.

<!-- -->

## 0.64 - [#369](https://github.com/openfisca/openfisca-tunisia/pull/369)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/fonction_publique`.
* Détails :
  - Ajoute l'ordre d'indexation des paramètres présents dans chaque grade de la fonction publique.
  - Déplace l'information de grille de catégorie dans la documentation des index de grade.

<!-- -->

## 0.63 - [#365](https://github.com/openfisca/openfisca-tunisia/pull/365)

* Changement mineur.
* Périodes concernées : à partir du 01/01/2025.
* Zones impactées : `parameters/impot_revenu/bareme`.
* Détails :
  - Remplace la référence secondaire du barème IRPP 2025 par une référence JORT précise : article 36 de la loi n° 2024-48 du 9 décembre 2024, JORT n° 149/2024, p. 6429.
  - Ne change aucune valeur ni aucun calcul.

<!-- -->

## 0.62 - [#354](https://github.com/openfisca/openfisca-tunisia/pull/354)

* Amélioration technique.
* Périodes concernées : toutes.
* Détails :
  - Fix units.


## 0.61 - [#351](https://github.com/openfisca/openfisca-tunisia/pull/351)

* Amélioration technique.
* Périodes concernées : aucune.
* Détails :
  - Bump version 0.61.

## 0.60 - [#349](https://github.com/openfisca/openfisca-tunisia/pull/349)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : CI, lint, outillage.
* Détails :
  - Suppression de flake8, flake8-print, flake8-quotes, flake8-pyproject et autopep8 ; utilisation exclusive de ruff (lint + format) et isort intégré à ruff.
  - Makefile et CI basés sur uv : `uv sync`, `uv run`, cache uv et venv dans le workflow GitHub Actions.
  - Scripts CI (.github) mis à jour pour appeler `uv run` (openfisca, python) ; twine ajouté aux dépendances dev pour le déploiement.
  - Reformattage du code avec `ruff format`.

## 0.59 - [#XXX](https://github.com/openfisca/openfisca-tunisia/pull/XXX)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : CI.
* Détails :
  - Corrige l'installation de la version minimale d'openfisca-core en CI (44.0.3 au lieu de 44, inexistante sur PyPI).

## 0.58 - [#346](https://github.com/openfisca/openfisca-tunisia/pull/346)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : CI, documentation.
* Détails :
  - Aligne les versions de Python sur openfisca-core v44 (3.10, 3.11, 3.12 ; retrait du support 3.9).
  - Met à jour le workflow CI et la documentation (README, CONTRIBUTING, .conda/meta.yaml).
  - Documente la mise à jour des required status checks dans CONTRIBUTING.

## 0.57 - [#340](https://github.com/openfisca/openfisca-tunisia/pull/340)

* Évolution du système socio-fiscal.
* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/fiscalite_indirecte`, `parameters/energie`, `parameters/units`.
* Détails :
  - Ajoute les paramètres de fiscalité indirecte (TVA avec taux normal, réduit et nul, accises sur alcool, tabac, boissons, café/thé, cosmétiques et autres produits).
  - Ajoute les paramètres pour l'énergie (électricité et gaz : tarifs par tranche, coûts fixes, réductions de puissance, taxes FTE).
  - Met à jour openfisca-core vers la version 44.
  - Ajoute de nouvelles unités de mesure.
  - Retire la dépendance directe à numpy (désormais fournie par openfisca-core).

## 0.56 - [#257](https://github.com/openfisca/openfisca-tunisia/pull/257)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `parameters/marche_travail`.
* Détails :
  - Complète l'historique du SMIG et du SMAG depuis 1961.
  - Ajoute les paramètres pour les indemnités spéciales (IS) et complémentaires (ICP).

## 0.55 - [#238](https://github.com/openfisca/openfisca-tunisia/pull/238)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes..
* Zones impactées : `cotisations/sociales/public/regimes_speciaux`.
* Détails :
  - Ajout des barèmes de membres du gouvernement, des députés et des gouverneurs.

### 0.54 - [#214](https://github.com/openfisca/openfisca-tunisia/pull/214)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters`.
* Détails :
  - Ajout / test href vers repo gitlab


### 0.53 - [#209](https://github.com/openfisca/openfisca-tunisia/pull/209)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `parameters`.
* Détails :
  - Ajoute référence pour le capital décès


### 0.52 - [#205](https://github.com/openfisca/openfisca-tunisia/pull/205)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `parameters`.
* Détails :
  - Corrige le smig pris en compte dans l'éligibilité Amen social
  - Ajoute des paramètres sur les produits alimentaires subventionnés et l'énergie

### 0.51 - [#204](https://github.com/openfisca/openfisca-tunisia/pull/204)

* Changement mineur.
* Zones impactées : `parameters/prelevements_sociaux/cotisations_sociales`.
* Détails :
  - Ajoute une référence législative pour les cotisations retraite

## 0.50 - [#198](https://github.com/openfisca/openfisca-tunisia/pull/198)

* Changement mineur.
* Zones impactées : `parameters/prelevements_sociaux/cotisations_sociales/salarie_cnrps`.
* Détails :
  - Ajoute une référence législative pour les cotisations retraite

## 0.49 - [#197](https://github.com/openfisca/openfisca-tunisia/pull/197)

* Évolution du système socio-fiscal. .
* Périodes concernées : toutes.
* Zones impactées : `parameters/prelevements_sociaux/cotisations_sociales/salarie_cnrps`.
* Détails :
  - Mise à jour des taux des cotisations retraite

## 0.48 - [#193](https://github.com/openfisca/openfisca-tunisia/pull/193)

* Évolution du système socio-fiscal. .
* Périodes concernées : toutes.
* Zones impactées : `variables/prestations/non_contributives/amen_social.py`.
* Détails :
  - Calcule `amen_social_presence_handicap_lourd`

## 0.47 - [#191](https://github.com/openfisca/openfisca-tunisia/pull/191)

* Évolution du système socio-fiscal. .
* Périodes concernées : toutes.
* Zones impactées : `variables/prestations/non_contributives/amen_social.py`.
* Détails :
  - Introduit `amen_social_revenu`

## 0.46 - [#191](https://github.com/openfisca/openfisca-tunisia/pull/191)

* Évolution du système socio-fiscal. .
* Périodes concernées : toutes.
* Zones impactées : `variables/caracteristiques_socio_demographiques/handicap.py`.
* Détails :
  - Introduit un niveau de handicap

## 0.45 - [#190](https://github.com/openfisca/openfisca-tunisia/pull/190)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `parameters/atmp`.
* Détails :
  - Corrige les unités

## 0.44 - [#188](https://github.com/openfisca/openfisca-tunisia/pull/188)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `parameters/prelevements_sociaux/atmp`.
* Détails :
  - Correction des labels

## 0.43 - [#187](https://github.com/openfisca/openfisca-tunisia/pull/187)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/atmp`.
* Détails :
  - Ajoute les paramètres ATMP


## 0.42 - [#186](https://github.com/openfisca/openfisca-tunisia/pull/186)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes. à partir du 2020.
* Zones impactées : `prestations/non_contributives/allocation_familiale`.
* Détails :
  - Corrige `allocation_familiale`

### 0.41.6 - [#183](https://github.com/openfisca/openfisca-tunisia/pull/183)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes. à partir du 2020.
* Zones impactées : `retraites`.
* Détails :
  - Mise à jour de l'âge légal

### 0.41.5 - [#184](https://github.com/openfisca/openfisca-tunisia/pull/184)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes. à partir du 2020.
* Zones impactées : `marche_travail/smig_*`.
* Détails :
  - Mise à jour des séries de Smig

### 0.41.4 - [#181](https://github.com/openfisca/openfisca-tunisia/pull/181)

* Évolution du système socio-fiscal.
* Périodes concernées : après 2025-01-01
* Zones impactées : `impot_revenu`, `cotisations_sociales`.
* Détails :
  - Nouveau barème de l'IR
  - Nouveau taux de CSS
  - Nouveau prélèvement (paramètres seulement dans RSNA) pour financer l'assurance perte d'emploi

### 0.41.3 - [#179](https://github.com/openfisca/openfisca-tunisia/pull/179)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/non_contributives/amen_social`.
* Détails :
  - Améliore Amen social (WIP)

### 0.41.2 - [#177](https://github.com/openfisca/openfisca-tunisia/pull/177)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `parameters/prestations/non_contributives/amen_social`.
* Détails :
  - Corrige et enrichit les références

### 0.41.1 - [#175](https://github.com/openfisca/openfisca-tunisia/pull/175)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/non_contributives`.
* Détails :
  - Corrige certains attributs des paramètres

## 0.41.0 - [#174](https://github.com/openfisca/openfisca-tunisia/pull/174)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/non_contributives`.
* Détails :
  - Amélioration Amen social.
  - Début des allocations familiales.

### 0.40.3 - [#169](https://github.com/openfisca/openfisca-tunisia/pull/169)

* Amélioration technique.
* Zones impactées : `parameters/retraite/cnrps`.
* Détails :
  - Complète l'historique des cotisations CNRPS

### 0.40.2 - [#167](https://github.com/openfisca/openfisca-tunisia/pull/167)

* Amélioration technique.
* Zones impactées : `parameters/retraite/cnrps`.
* Détails :
  - Corrige affichage barème annuité

### 0.40.1 - [#166](https://github.com/openfisca/openfisca-tunisia/pull/166)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `parameters/retraite`.
* Détails :
  - Synchro avec `openfsica-tunisia-pension`

## 0.40.0 - [#161](https://github.com/openfisca/openfisca-tunisia/pull/161)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `tests`.
* Détails :
  - Ajoute tests css.

## 0.39.0 - [#161](https://github.com/openfisca/openfisca-tunisia/pull/161)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `parameters/cotisations_sociales`.
* Détails :
  - Complète l'historique des cotisations retraite.

## 0.38.0 - [#160](https://github.com/openfisca/openfisca-tunisia/pull/160)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `variables/cotisations_sociales`.
* Détails :
  - Différencie cotisants et retraités.

## 0.37.O - [#153](https://github.com/openfisca/openfisca-tunisia/pull/153)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2019
* Zones impactées : `amen_social`.
* Détails :
  - Commence à coder les prestations du programme Amen social

## 0.36.O - [#151](https://github.com/openfisca/openfisca-tunisia/pull/151)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018
* Zones impactées : `contribution_sociale_solidarite`.
* Détails :
  - Implémenet la CSS
  - Nettoie le code et l'adapte aux plus récentes conventions

## 0.35.O - [#148](https://github.com/openfisca/openfisca-tunisia/pull/148)

* Changement mineur.
* Détails :
  - Régorganise les paramètres en créant marche_travail

## 0.34.O - [#147](https://github.com/openfisca/openfisca-tunisia/pull/147)

* Changement mineur.
* Détails :
  - Régorganise les paramètres en créant marche_travail

### 0.34.O - [#147](https://github.com/openfisca/openfisca-tunisia/pull/147)

* Changement mineur.
* Détails :
  - Migre vers pyproject.toml

### 0.33.4 - [#135](https://github.com/openfisca/openfisca-tunisia/pull/135)

* Changement mineur.
* Périodes concernées : aucune.
* Zones impactées : `README.md`.
* Détails :
  - Change les badges

### 0.33.3 - [#134](https://github.com/openfisca/openfisca-tunisia/pull/134)

* Amélioration technique.
* Détails :
  - Migration vers Github actions (retrait de CircleCi)

### 0.33.2 - [#126](https://github.com/openfisca/openfisca-tunisia/pull/126)

* Ajoute la validation des paramètres YAML ainsi que l'intégration à la CI tax-benefit.org.

### 0.33.1 - [#117](https://github.com/openfisca/openfisca-tunisia/pull/117)

* Mets à jour la dépendance à pytest

## 0.33.0 - [#119](https://github.com/openfisca/openfisca-tunisia/pull/119)

* Migre à `numpy` 1.18+ via `openfisca-core` v35
  * Sans impact sur le code qui ne contient pas de syntaxe numpy dépréciée

## 0.32.0 - [#115](https://github.com/openfisca/openfisca-tunisia/pull/115)

* Mets à jour les déductions pour charges de famille

### 0.31.2 - [#111](https://github.com/openfisca/openfisca-tunisia/pull/111)

* Nettoie certains tests

### 0.31.1 - [#108](https://github.com/openfisca/openfisca-tunisia/pull/108)

* Met à jour les dépendances de  pytest et openfisca-survey-manager

## 0.31.0 - [#109](https://github.com/openfisca/openfisca-tunisia/pull/109)

* Met à jour le montant de la déduction pour chef de famille suite à la Loi de Finances 2018 conformémément à l'[article 40 de l'IRPP en arabe](http://www.legislation.tn/affich-code-article/code-de-l%2526%2523039%3Bimpôt-sur-le-revenu-des-personnes-physiques-et-de-l%2526%2523039%3Bimpôt-sur-les-sociétés-article-40-__6169)

* Supprime une syntaxe obsolète de `cotisations_salarie`

## 0.30.0 - [#107](https://github.com/openfisca/openfisca-tunisia/pull/107)

* Migrate to `openfisca-core` v34
  * Migrate to v32, v33 and v34
* Update `openfisca-survey-manager` dependency to v0.32
* Remove the upper bound of children number for `Menage` entity

## 0.29.0 - [#105](https://github.com/openfisca/openfisca-tunisia/pull/105)

* Migrate tests library and syntax from `nose` to `pytest`
* Rename `tests/test_legislations.py` to `tests/test_parameters.py`
* Update tests information in `README` and set a `Debug` section
* Remove python 2 syntaxes in model and tests

### 0.28.2 - [#106](https://github.com/openfisca/openfisca-tunisia/pull/106)

* Remove python2 unicode mark

### 0.28.1 - [#102](https://github.com/openfisca/openfisca-tunisia/pull/102)

* Add 2018 + 2019 values and update metadata of `SMIG`
  * `cotisations_sociales/gen/smig_40h_horaire.yaml`
  * `cotisations_sociales/gen/smig_40h_mensuel.yaml`
  * `cotisations_sociales/gen/smig_48h_horaire.yaml`
  * `cotisations_sociales/gen/smig_48h_mensuel.yaml`
* Add 2018 + 2019 values and update metadata of `SMAG`
  * `cotisations_sociales/gen/smag_journalier.yaml`

## 0.28.0 - [#104](https://github.com/openfisca/openfisca-tunisia/pull/104)

* Migrate to `openfisca-core` v31
  * Remove the `base_function` of the variable `age_en_mois`

## 0.27.0 - [#101](https://github.com/openfisca/openfisca-tunisia/pull/101)

* Migrate to `openfisca-core` v30
  * Adapt `de_net_a_imposable` and `de_net_a_salaire_de_base` reforms

## 0.26.0 - [#90](https://github.com/openfisca/openfisca-tunisia/pull/90)

* Migrate to `openfisca-core` v29
* Clean up configuration (CI job names, old_tests residue)

## 0.25.0 - [#88](https://github.com/openfisca/openfisca-tunisia/pull/88)

* Migrate to `openfisca-core` v27 syntax

## 0.24.0 - [#87](https://github.com/openfisca/openfisca-tunisia/pull/87)

* Migrate to `openfisca-core` v26 syntax

### 0.23.1 - [#81](https://github.com/openfisca/openfisca-tunisia/pull/81)

* Update `openfisca-survey-manager` to `0.17.*` revision

## 0.23.0 - [#85](https://github.com/openfisca/openfisca-tunisia/pull/85)

* Improve `reforms/de_net_a_salaire_de_base.py`
  * Adapt with `ouvriere_2016_02.yaml` use case
* Add `reforms/de_net_a_salaire_de_base/ouvriere_2016_02.yaml` test

### 0.22.1 - [#78](https://github.com/openfisca/openfisca-tunisia/pull/78)

* Add some other missing units to `parameters`

## 0.22.0 - [#82](https://github.com/openfisca/openfisca-tunisia/pull/82)

* Migrate to openfisca-core v25 syntax
* Fix `KeyError` on `compute_cotisation`
* Rename parameters paths
  * Rename `cotisations_sociales/rsa/sal` to `cotisations_sociales/rsa/cotisations_salarie`
  * Rename `cotisations_sociales/rsaa/sal` to `cotisations_sociales/rsaa/cotisations_salarie`
* Fix `reforms` value in YAML tests

### 0.21.1 - [#75](https://github.com/openfisca/openfisca-tunisia/pull/75)

* Add missing units to `parameters`

## 0.21.0 - [#74](https://github.com/openfisca/openfisca-tunisia/pull/74)

* Migrate to openfisca-core v24 syntax

## 0.20.0 - [#71](https://github.com/openfisca/openfisca-tunisia/pull/71)

* Adapt to Python 3.6 and keep Python 2.7 compatibility
  * And delete outdated `scripts/`

## 0.19.0 - [#70](https://github.com/openfisca/openfisca-tunisia/pull/70)

* Migrate to openfisca-core v22 syntax
* Add `age_en_mois`

### 0.18.1 - [#68](https://github.com/openfisca/openfisca-tunisia/pull/68)

* Add 2017 references to `impot_revenu.bareme`

## 0.18.0 - [#67](https://github.com/openfisca/openfisca-tunisia/pull/67)

* Move tests outside `openfisca_tunisa` module
  * And delete `old_tests`
* Move PDF and Excel files from repository to public drive
* Update README with public drive link and API latest information
  * And delete old `api/` configuration

### 0.17.1 - [#66](https://github.com/openfisca/openfisca-tunisia/pull/66)

* Add continuous integration with CircleCI v2
* Add `CONTRIBUTING.md` information

## 0.17.0 - [#64](https://github.com/openfisca/openfisca-tunisia/pull/64)

* Update `smig` variable type
* Add parameters on `SMIG` _components_
  * `cotisations_sociales/gen/salaire_de_base_40h_horaire.yaml`
  * `cotisations_sociales/gen/salaire_de_base_40h_mensuel.yaml`
  * `cotisations_sociales/gen/salaire_de_base_48h_horaire.yaml`
  * `cotisations_sociales/gen/salaire_de_base_48h_mensuel.yaml`
  * `cotisations_sociales/gen/indemnite_complementaire_provisoire.yaml`
  * `cotisations_sociales/gen/majoration_smig_40h_mensuel.yaml`
  * `cotisations_sociales/gen/majoration_smig_48h_mensuel.yaml`
* Update parameters and references on `SMIG`
  * `cotisations_sociales/gen/smig_40h_horaire.yaml`
  * `cotisations_sociales/gen/smig_40h_mensuel.yaml`
  * `cotisations_sociales/gen/smig_48h_horaire.yaml`
  * `cotisations_sociales/gen/smig_48h_mensuel.yaml`
* Update parameters and references on `SMAG`
  * `cotisations_sociales/gen/smag_journalier.yaml`

### 0.16.2 - [#63](https://github.com/openfisca/openfisca-tunisia/pull/63)

* Add `notebooks/test_notebooks.py` script to execute .ipynb files
  * Add `Makefile` tag `nb` to test specified notebooks

### 0.16.1 - [#62](https://github.com/openfisca/openfisca-tunisia/pull/62)

* In `TypesRegimeSecuriteSociale` and `/parameters/cotisations_sociales`
  * Rename `cnrps_sal` to `salarie_cnrps`
  * Rename `cnrps_pen` to `pensionne_cnrps`

## 0.16.0 - [#61](https://github.com/openfisca/openfisca-tunisia/pull/61)

* Rename `categorie_salarie` to `regime_securite_sociale`

## 0.15.0 - [#58](https://github.com/openfisca/openfisca-tunisia/pull/58) [#59](https://github.com/openfisca/openfisca-tunisia/pull/59)

* Adapt to core v21.0.2 (Enum)
* Add `prestations_familiales_enfant_a_charge`
  * Update `af_nbenf`
  * Delete `smig75`
* Add `openfisca_tunisia/survey_scenario/`

### 0.14.1 - [#56](https://github.com/openfisca/openfisca-tunisia/pull/56)

* Add demo jupyter notebook and binder link

## 0.14.0 - [#55](https://github.com/openfisca/openfisca-tunisia/pull/55)

* Rename `de_net_a_brut` reform to `de_net_a_imposable`
* Create reform `de_net_a_salaire_de_base`

## 0.13.0 - [#53](https://github.com/openfisca/openfisca-tunisia/pull/53)

* Fix `de_net_a_brut` reform
* Remove python script for yaml testing

## 0.12.0 - [#50](https://github.com/openfisca/openfisca-tunisia/pull/50)

* Update barème impot sur le revenu
* Adopt long names for some parameters (far from completed)
* Update value of various déductions familiales

## 0.11.0 - [#44](https://github.com/openfisca/openfisca-tunisia/pull/44)

* Update to openfisca-core v20 syntax
* Rename `ir_brut` to `impot_revenu_brut`
* Rename `rni` to `revenu_net_imposable`

### 0.10.2 - [#39](https://github.com/openfisca/openfisca-tunisia/pull/39)

* Add installation instructions
* Translate revenus/activite/non_salarie.py labels to arabic

### 0.10.1 - [#38](https://github.com/openfisca/openfisca-tunisia/pull/38)

* Fix legislation tests

## 0.10.0

* Migrate to openfisca-core 14.0.1 syntax

## 0.9.0

* Migrate to openfisca-core 12.1.0 syntax

## 0.8.0

* Migrate to openfisca-core 10.0.2 syntax

## 0.7.0 - [#34](https://github.com/openfisca/openfisca-tunisia/pull/34)

* Rename `bic_forf_res` to `bic_forfaitaire_resultat`
* Rename `bic_sp` to `bic_societes_personnes`
* Rename `bic_sp_res` to `bic_societes_personnes_resultat`
* Rename `decl_inves` to `structure_declaration_investissement`
* Rename `fon_forf_bati_fra` to `foncier_forfaitaire_batis_frais`
* Rename `fon_forf_bati_rec` to `foncier_forfaitaire_batis_recettes`
* Rename `fon_forf_bati_rel` to `foncier_forfaitaire_batis_reliquat`
* Rename `fon_forf_bati_tax` to `foncier_forfaitaire_batis_taxe`
* Rename `fon_forf_nbat_dep` to `foncier_forfaitaire_non_batis_depenses`
* Rename `fon_forf_nbat_rec` to `foncier_forfaitaire_non_batis_recettes`
* Rename `fon_forf_nbat_tax` to `foncier_forfaitaire_non_batis_taxe`
* Rename `fon_reel_fisc` to `foncier_reel_resultat_fiscal`
* Rename `fon_sp` to `foncier_societes_personnes`

## 0.6.1

* Add cotisation `ugtt`
* Add a couple of payroll tests
