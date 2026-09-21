# Changelog

### 7.3.0

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 02/05/2019.
* Zones impactées : `parameters/retraite/cnrps/age_legal/militaire`, `parameters/retraite/cnrps/bonifications/cadre_actif`.
* Détails :
  - **Verse les âges militaires issus de la loi n° 2019-37**, relue sur pièce. Son article premier réécrit l'article 61 : cinquante-deux ans pour les hommes de troupe, cinquante-sept pour les sous-officiers, soixante pour les officiers subalternes, soixante-deux pour les officiers supérieurs et les officiers généraux. Son article 5 les atteint en deux temps : un an de plus au 1er juillet 2019, deux ans au 1er janvier 2020.
  - **Le second palier retombe exactement sur l'article 61 nouveau, pour chacun des cinq grades.** C'est ce qui permet d'attribuer les quatre âges du texte aux cinq grades sans ambiguïté, les officiers supérieurs et généraux partageant le même.
  - **Verse le terme de la période bonifiable de l'article 32** : soixante ans, porté à soixante-deux par l'article 2 de la loi. Le nom du fichier, `age_terme_article_32`, désigne l'article pour qu'on n'y lise pas les articles 33 et 67, qui portent aussi un terme de soixante-deux ans mais par une autre voie.
  - **Ce terme saute d'un coup, quand l'âge de départ des mêmes agents monte en deux temps.** L'article 5, qui échelonne le relèvement, énumère les articles auxquels il déroge — 24, 27, 28, 29 et 61 — et l'article 32 n'en est pas. L'énumération a été lue deux fois : l'extraction mise en page avait perdu un numéro, l'extraction brute l'a rendu.
  - **La date d'entrée en vigueur est déduite, et corroborée.** La loi n'a pas de clause propre et se clôt sur la formule ordinaire : elle devient exécutoire un jour franc après sa publication du 30 avril, le 2 mai 2019. Son article 4 fait courir la hausse des cotisations « à partir du premier jour du mois qui suit la date d'entrée en vigueur », et openfisca-tunisia la date au 1er juin 2019 : l'entrée en vigueur tombe donc bien en mai, et non le jour de la publication.
  - Aucune valeur antérieure n'est modifiée. La bonification militaire, calculée comme un forfait de cinq ans que le texte ne fonde pas, fait l'objet de l'issue #53.

### 7.2.0

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/1974.
* Zones impactées : `parameters/retraite/rsna/survivants`, `parameters/retraite/rsna/depart_anticipe`, `parameters/retraite/cnrps/age_legal/militaire`.
* Détails :
  - **Verse trois jeux de paramètres que l'arbre ne portait pas** : les droits des survivants du régime des salariés non agricoles, les durées et le taux des départs anticipés du même régime, et les âges de mise à la retraite des militaires par grade. Dix-huit fichiers, aucune valeur existante modifiée, aucun résultat changé.
  - **Les survivants du régime non agricole.** Réversion du conjoint survivant à la moitié de la pension de l'assuré depuis 1974 ; pension d'orphelin au cinquième, portée à trois dixièmes en 1981 ; âges limites de service, seize ans sans condition, vingt et un ans en cas d'études, vingt-cinq ans pour les études supérieures sans bourse à compter du 1er mai 1997.
  - **Deux taux sont dédoublés plutôt que mis en série, parce qu'une série serait fausse.** La majoration de l'article 31, qui porte la réversion jusqu'aux trois quarts, est un plafond sous conditions et non un taux : elle est versée à part, faute de quoi le modèle affirmerait que tout conjoint survivant touche les trois quarts depuis 1981. De même, le taux d'orphelin de père et de mère vaut trois dixièmes sur toute la période : la réforme de 1981 ne le relève pas, elle aligne sur lui le taux de l'orphelin ordinaire et fait disparaître la distinction.
  - **Les départs anticipés du régime non agricole.** Stage de 360 mois pour la convenance personnelle et de 180 mois pour les mères de trois enfants vivants au moins, depuis 1982 ; décote d'un demi pour cent par trimestre restant à courir ; jouissance à cinquante-cinq ans pour l'article 15 ter à compter de 2007. Les textes comptent en mois, et les paramètres aussi.
  - **Le décret n° 2007-2148 ne repousse pas l'âge des départs anticipés**, contrairement à ce qu'une lecture rapide suggérerait : il sort la convenance personnelle de l'article 15 bis pour la porter à un article 15 ter où la jouissance est différée à cinquante-cinq ans. Les trois autres cas restent à cinquante ans.
  - **Les âges militaires.** Cinquante ans pour les hommes de troupe, cinquante-cinq pour les sous-officiers, cinquante-huit pour les officiers subalternes, soixante pour les officiers supérieurs, soixante-deux pour les officiers généraux — ce dernier abaissé à soixante par la loi n° 88-71, au 1er janvier 1989. Les quatre autres sont reconduits sans changement, et portent une référence de 1989 sans valeur nouvelle pour que la relecture du texte ne conclue pas à une lacune.
  - **Deux gardes sont ajoutées**, portées depuis openfisca-tunisia, dans `tests/test_parametres_lisibles.py` : la prose d'un paramètre ne nomme ni variable, ni formule, ni entité, et n'use pas de l'emphase par capitales. Elles ont trouvé sept fichiers de ce dépôt qui décrivaient le modèle, désormais corrigés sans qu'aucune valeur bouge.
  - **Ce qui n'est pas versé, et pourquoi.** Trois règles de la section des survivants n'ont pas de valeur : le sort de la réversion en cas de remariage, le plafond de cumul de l'article 38, qui borne un total par un autre montant, et l'interdiction de cumuler invalidité et survivant, levée en 1997. Du côté de l'article 32 de la loi n° 85-12, seul le repère d'âge — soixante ans, porté à soixante-deux par la loi n° 2019-37 — serait versable, mais la date d'effet de l'article 2 de cette loi n'est pas établie : le fait reste documenté dans `bonifications/cadre_actif/service_35.yaml` plutôt que daté à tort.

### 7.1.0

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/1994.
* Zones impactées : `parameters/retraite/rsna/salaire_reference`.
* Détails :
  - **Verse la fenêtre du salaire moyen de référence** du régime des salariés non agricoles, que le modèle ne portait pas : soixante mois à partir du 1er juillet 1994, quatre-vingt-quatre à partir du 1er juillet 1995, cent vingt à partir du 1er juillet 1996.
  - **Les trois dates sont écrites dans un seul texte.** La montée de cinq à dix ans n'est pas l'œuvre de trois décrets successifs : le décret n° 94-1429 porte les trois échéances dans son article 18 nouveau. Chercher un modificatif pour 1995 ou 1996 serait peine perdue.
  - **LA SÉRIE NE COMMENCE QU'EN 1994, ET CE N'EST PAS UNE LACUNE.** Ni l'état de 1974 ni celui de 1990 ne se laissent écrire en un nombre, et la documentation du paramètre dit pourquoi. En 1974, le décret n° 74-499 retient les salaires des trois OU cinq dernières années, « selon que l'une ou l'autre de ces périodes de référence est plus avantageuse » pour l'assuré : deux valeurs et une règle de choix, dont un paramètre scalaire ne retiendrait qu'une.
  - **En 1990, le texte se contredit lui-même.** Le décret n° 90-1455 porte la fenêtre à dix ans en réécrivant le seul article 18 et LAISSE L'ARTICLE 19 INCHANGÉ, lequel continue de diviser par trente-six ou soixante mois. La contradiction dure près de quatre ans, et aucun texte publié au Journal officiel entre septembre 1990 et juin 1994 ne dit lequel des deux articles l'a emporté en pratique. Verser cent vingt mois pour cette période trancherait une question que les textes laissent ouverte.
  - Le décret n° 94-1429 abroge et remplace ENSEMBLE les articles 18 et 19, et fait suivre à la moyenne la durée de la fenêtre : la contradiction disparaît, et la valeur devient représentable.
  - Aucun résultat existant ne change : les 47 tests passent à l'identique. Ce que l'arbre doit au modèle, et ce que le modèle lui doit, relève du CHANGELOG et des issues — un fichier de paramètre porte une valeur du droit, et doit pouvoir se lire avec le texte seul.

### 7.0.1

* Amélioration technique.
* Zones impactées : `parameters/retraite/cnrps/bonifications`, `parameters/retraite/cnrps/depart_anticipe/meres_3_enfants`.
* Détails :
  - **Six paramètres cessent de se documenter par le modèle** (issue #46). Un paramètre porte une valeur du droit : il doit pouvoir se lire avec le texte seul, sans connaître le nom des formules qui l'emploient. Aucune valeur, aucune date d'effet et aucune référence ne sont modifiées.
  - **Cinq de ces mentions étaient devenues fausses.** Les quatre paliers de `bonifications.cadre_actif` et `bonifications.militaire.bonus` affirmaient : « La formule `cnrps_bonifications` n'utilise pas ce paramètre : le barème y est écrit en dur. » C'était exact à leur rédaction, mais la 5.6.0 (PR #42, issue #29) a précisément branché la formule sur ces paramètres. La phrase désinformait donc le lecteur sur l'état du modèle, en plus de l'y renvoyer.
  - **Un motif de conception rejoint le CHANGELOG, où il a sa place.** `depart_anticipe.meres_3_enfants.age_minimum` expliquait conserver une valeur non sourcée pour 1985-1988 parce que « `cnrps_age_requis` évalue toutes les branches de son `select` pour tous les individus » : la retirer rendrait tout calcul CNRPS impossible sur ces trois années. Le fait est vrai et utile, mais il décrit le modèle, non le droit. Le paramètre conserve le fait juridique — aucun texte lu n'appuie les 50 ans, et l'article 41 nouveau de 1988 range les mères dans un cas distinct de la demande ordinaire, ce qui invite à en douter.
  - Aucun test n'est modifié : `make test` passe à l'identique.

<!-- -->

# 7.0.0

* Changement non rétrocompatible.
* Zones impactées : `parameters/retraite/cnrps/age_legal/civil`, `parameters/retraite/cnrps/depart_anticipe/sur_demande`, `variables/cnrps`, `regimes/cnrps`.
* Détails :
  - **Les deux conditions de l'article 28 sont réunies sous un seul nœud** (issue #37). L'article 28 de la loi n° 85-12 pose deux conditions cumulatives pour les agents exerçant des fonctions astreignantes : un âge et une durée de services. Elles étaient portées par deux jeux de paramètres distincts, l'un décrivant à tort un départ anticipé « sur demande ». `age_legal.civil.fonctions_astreignantes` devient un nœud portant `age` et `duree_services`.
  - **Chemins supprimés** : `retraite.cnrps.depart_anticipe.sur_demande.astreignants.age_minimum` et `.duree_minimum`. **Chemin transformé** : `retraite.cnrps.age_legal.civil.fonctions_astreignantes`, qui était une valeur scalaire, devient un nœud — les appels qui le lisaient comme un âge doivent viser `fonctions_astreignantes.age`.
  - **Le nom disait le contraire du texte.** L'article 28 ne décrit pas un départ à l'initiative de l'agent : il fixe l'âge et la durée au terme desquels les agents « sont mis à la retraite », avec maintien possible en activité jusqu'à 60 ans. Les ranger sous `depart_anticipe.sur_demande` présentait comme une faculté ce que la loi écrit comme une mise à la retraite.
  - **Un doublon disparaît.** Les deux jeux portaient les mêmes valeurs — 55 ans au 12 septembre 1985, 56 au 1er juillet 2019, 57 au 1er janvier 2020 — et la même source, mais un seul des deux était lu par les formules, et seul l'autre portait la durée de 35 ans. Les notes conservées sont les plus complètes des deux : elles citent l'article 28 *in extenso*, dans sa rédaction de 1985 puis dans celle de la loi n° 2019-37.
  - **Aucun résultat ne change.** Les valeurs, les dates d'effet et les références sont identiques ; seuls les chemins changent. `cnrps_age_requis` et `cnrps_duree_requise_annees`, dans `variables/cnrps` comme dans `regimes/cnrps`, lisent désormais le nœud fusionné. Les quatre tests de `tests/formulas/test_astreignants.py` passent sans modification de leurs valeurs attendues. `make test` : 144 tests.
  - Rapport d'audit régénéré : le dépôt compte **52 paramètres porteurs de valeurs au lieu de 53**, et 49 avec référence au lieu de 50. La baisse est exactement le doublon supprimé — trois paramètres disparaissent (`fonctions_astreignantes` comme valeur scalaire, `astreignants.age_minimum`, `astreignants.duree_minimum`), deux les remplacent (`fonctions_astreignantes.age`, `fonctions_astreignantes.duree_services`). Les paramètres multi-dates passent de 21 à 20, deux d'entre eux ayant porté les mêmes trois dates jusqu'ici. Aucune valeur, aucune date d'effet et aucune référence ne sont modifiées : seule la structure change, et les trois paramètres sans source restent les mêmes (`bonifications.militaire.bonus`, `rsa.pension_min`, `rsa.periode_remplacement_base`).
  - _Dépendance à connaître : le précis socio-fiscal lit `age_legal/civil/fonctions_astreignantes.yaml` comme une feuille scalaire pour engendrer son tableau des âges. Sa mise à jour doit suivre la publication de cette version, et non la précéder._

<!-- -->

## 6.1.0

* Évolution du système socio-fiscal.
* Périodes concernées : jusqu'au 30/04/1981 (indemnité de revenu unique).
* Zones impactées : `variables/accessoires_formulas`.
* Détails :
  - **`cnrps_indemnite_revenu_unique` reçoit une formule datée** (issue #47). Elle portait une formule non datée, alors que ses trois paramètres de montant ne commencent qu'au 1er mai 1981. Elle devient `formula_1981_05_01`. La date est celle de l'**effet** énoncé par l'article 5 de la loi n° 81-70 du 1er août 1981 — « L'article 4 de la présente loi prend effet à compter du 1er mai 1981 » (JORT n° 51 du 7 août 1981, p. 1790) — et non celle de sa signature ni de sa publication. C'est l'article 4 qui ouvre le droit aux retraités, en ajoutant un paragraphe V à l'article 22 de la loi n° 59-18.
  - **Un zéro silencieux est supprimé, et c'était le vrai défaut.** La formule lisait ses paramètres par `getattr(params_iru, "1_enfant", 0)`. Or `ParameterNotFoundError` **dérive de `AttributeError`** — MRO : `['ParameterNotFoundError', 'AttributeError', 'Exception', ...]` —, de sorte que la valeur par défaut avalait l'erreur. Avant mai 1981, la variable rendait bien zéro, mais par accident. Le même filet aurait transformé, **à n'importe quelle date**, un paramètre mal orthographié, supprimé ou renommé en un zéro silencieux qu'aucun test n'aurait vu : le renommage `rang_4_et_plus` → `rang_4` de la 6.0.0 aurait pu passer inaperçu ici. Les trois valeurs par défaut sont retirées ; un paramètre manquant échoue désormais bruyamment. Le `getattr` lui-même est conservé, « 1_enfant » n'étant pas un identifiant Python valide.
  - **Aucun résultat ne change à partir du 1er mai 1981.** Avant cette date, la variable vaut toujours zéro, mais parce que la formule n'existe pas encore — résultat voulu, et non produit d'une erreur masquée.
  - Tests : `tests/formulas/test_indemnite_revenu_unique.yaml`, **neuf cas** en YAML — l'entrée en vigueur au mois près (décembre 1980 et avril 1981 à zéro, mai 1981 à 3,125), les trois montants selon le nombre d'enfants, le taux de trois enfants appliqué au-delà, la condition de revenu unique dans ses deux formes, et l'absence d'enfant. Les deux tests existants de `test_accessoires.yaml` passent **sans modification**. `make test` : 144 tests passent.
  - _Ce que la formule ne fait toujours pas : les montants ne sont établis par aucun texte du Journal officiel — ils viennent du manuel de liquidation de la caisse, qui ne cite pas leur source. Les paramètres le déclarent._

<!-- -->

# 6.0.0 - [#44](https://github.com/openfisca/openfisca-tunisia-pension/pull/44)

* Évolution du système socio-fiscal.
* **Changement non rétrocompatible** : le paramètre `retraite.cnrps.accessoires.indemnites_familiales.rang_4_et_plus` est renommé **`rang_4`**. Son ancien nom affirmait un « et plus » que les textes ne portent pas — le barème du décret n° 86-611 s'arrête au quatrième rang. Tout code ou test appelant l'ancien chemin doit être mis à jour ; le contenu du paramètre, ses valeurs, ses dates et ses références sont inchangés.
* Périodes concernées : à partir du 01/01/1989 (indemnités familiales au-delà du troisième enfant).
* Zones impactées : `parameters/retraite/cnrps/accessoires/indemnites_familiales`, `variables/accessoires_formulas`, `variables/accessoires_inputs`.
* Détails :
  - **L'indemnité familiale est limitée aux trois premiers enfants depuis le 1er janvier 1989** (issue #30). `cnrps_indemnites_familiales` appliquait le taux du 4e rang à **chaque** enfant au-delà du troisième, quelle que soit la période. La loi n° 88-39 du 6 mai 1988 (JORT n° 33 du 13 mai 1988, p. 735, article unique) accorde l'indemnité « dans la limite des trois premiers enfants » à compter du 1er janvier 1989. La formule surestimait donc l'indemnité de tout pensionné de quatre enfants ou plus, sur trente-sept ans.
  - **Deux exceptions, que la loi réserve et que la formule porte désormais.** Les **droits acquis antérieurement au 1er janvier 1989**, que l'article unique excepte expressément et dont le décret n° 96-1906 (article 2) fixe encore le taux en 1996 au titre du « quatrième enfant ayant acquis ce droit antérieurement au 1er janvier 1989 » ; et l'**enfant handicapé** venant après le troisième rang, qui ouvre droit quel que soit son rang (loi n° 81-46 du 29 mai 1981, article 18 ; décret n° 96-1906, article 3).
  - **Deux formules datées, et aucun paramètre nouveau.** Le changement de régime est porté par le code, non par les données : `cnrps_indemnites_familiales` reçoit deux formules datées, `formula_1986_05_01` et `formula_1989_01_01`. La première vaut du 1er mai 1986 au 31 décembre 1988 et applique le taux du quatrième rang au quatrième enfant, et à lui seul : le décret n° 86-611 fixe quatre taux et s'arrête là, sans rien publier pour un cinquième enfant, qui n'ouvre donc aucun droit. Sa date est celle qu'énonce l'article 3 du décret, et c'est aussi la première date portée par les quatre paramètres de rang : **auparavant, la variable levait une `ParameterNotFoundError`** — « the parameter `retraite.cnrps.accessoires.indemnites_familiales[rang_1]` was not found in the 1985-12-01 tax and benefit system » — au lieu de rendre zéro faute de taux publié. Dater la formule corrige ce défaut, jamais couvert par un test jusqu'ici. La formule du 1er janvier 1989 réserve ce taux aux enfants que la loi n° 88-39 excepte. Chacune est documentée par son texte dans sa *docstring*. Un paramètre est une **valeur** du droit — un taux, un montant, un âge ; une bascule de régime n'en est pas une, et l'écrire en booléen aurait obligé la formule à interroger les données pour choisir son propre comportement.
  - **Deux variables d'entrée, nulles par défaut** : `nombre_enfants_indemnite_familiale_droit_acquis` et `nombre_enfants_handicapes_au_dela_du_troisieme_rang`. Le défaut de 0 ne change **rien** aux cas courants — trois enfants ou moins, l'écrasante majorité — et applique la limitation à qui ne déclare rien, ce qui est l'état du droit commun depuis 1989. La formule borne par ailleurs le nombre d'enfants ouvrant droit au nombre d'enfants effectivement présents au-delà du troisième : on ne peut pas déclarer plus de droits acquis qu'on n'a d'enfants.
  - **Résultats modifiés, dans les deux régimes.** Depuis le 1er janvier 1989, pour les pensionnés de quatre enfants ou plus qui ne déclarent ni droit acquis ni enfant handicapé : en 2024, quatre enfants donnaient 24,400 dinars par mois, et donnent 19,520. Avec un droit acquis ou un enfant handicapé déclaré, le montant est inchangé. **Avant le 1er janvier 1989, les foyers de cinq enfants et plus sont également touchés** : le taux du quatrième rang ne s'applique plus qu'une fois, de sorte que cinq enfants en 1987 donnaient 29,100 dinars et donnent 24,400 — le barème du décret n° 86-611 ne publie aucun taux au-delà du quatrième rang. Quatre enfants ou moins : aucun changement avant 1989.
  - **Le droit acquis ne vaut que pour un enfant, le handicap pour autant qu'il y en a.** Le décret n° 96-1906 vise « le quatrième enfant ayant acquis ce droit antérieurement au 1er janvier 1989 », au singulier : déclarer deux droits acquis n'en fait retenir qu'un. L'enfant handicapé relève d'une autre logique — l'article 18 de la loi n° 81-46 lui ouvre droit « quels que soient leur âge et leur rang », et l'article 3 du décret de 1996 vise « l'enfant handicapé venant après le 3e rang » : deux enfants handicapés au-delà du troisième comptent tous les deux, la limite du barème ne leur étant pas opposable.
  - Tests : `tests/formulas/test_indemnites_familiales_droits_acquis.yaml` porte **dix-neuf cas** en YAML — l'entrée en vigueur au mois près (décembre 1985 et avril 1986 à zéro, mai 1986 à 24,400), la bascule de 1989 au mois près (décembre 1988 contre janvier 1989, sur le même foyer de quatre enfants : 24,400 puis 19,700), les deux situations qui y échappent (droit acquis, enfant handicapé), l'arrêt du barème au quatrième rang avant 1989 (cinq puis huit enfants, 24,400 dans les deux cas), le droit acquis borné à un enfant quand deux sont déclarés, deux enfants handicapés comptés tous les deux, le régime actuel en 1990 et 2024, le cas courant de trois enfants, et la borne qui empêche de déclarer plus d'enfants qu'il n'y en a. Les quatre tests existants de `test_accessoires.yaml` passent **sans modification** : ils portent sur un et trois enfants, que la limitation ne touche pas. `make test` : 135 tests passent, contre 116 sur `master`.
  - Rapport d'audit régénéré : **identique à celui de `master`**, au caractère près. Aucun paramètre n'est ajouté, retiré, redaté ni resourcé — le dépôt compte toujours 53 paramètres porteurs de valeurs, dont 50 avec référence et trois sans source (`bonifications.militaire.bonus`, `rsa.pension_min`, `rsa.periode_remplacement_base`). C'est la contrepartie attendue du choix de porter la bascule par une formule plutôt que par une donnée : l'arbre des paramètres ne bouge pas, seul le code change.
  - _Ce que la formule ne fait toujours pas : l'âge limite des enfants — 16 ans, reculé à 18 en apprentissage et à 21 pour les études —, qui relève de la doctrine de la caisse et non d'un texte lu, reste à la charge de l'utilisateur dans `nombre_enfants_charge`._

<!-- -->

## 5.7.0 - [#43](https://github.com/openfisca/openfisca-tunisia-pension/pull/43)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/1989 (âge requis des mères de trois enfants, et leur éligibilité) ; du 05/03/1985 au 11/09/1985 (date de départ du paramètre).
* Zones impactées : `parameters/retraite/cnrps/depart_anticipe/meres_3_enfants`.
* Détails :
  - **Depuis le 1er janvier 1989, la jouissance de la pension des mères de trois enfants est immédiate** (issue #27). `cnrps.depart_anticipe.meres_3_enfants.age_minimum` valait 50 ans pour toute période, sans qu'aucun texte lu ne fixe cet âge — la version 5.4.0 en avait retiré la référence à l'article 5, qui ne le contient pas. L'**article 41 nouveau**, issu de la loi n° 88-71 du 27 juin 1988 (JORT n° 45 du 1er juillet 1988, pp. 967-968 ; effet au 1er janvier 1989 par son article 4), range « la mise à la retraite sur la demande des mères » parmi les cas de **jouissance immédiate**, aux côtés de l'atteinte de l'âge légal, de l'invalidité, du licenciement pour suppression d'emplois et de la mise à la retraite d'office. Le paramètre prend donc la valeur **0** au 1er janvier 1989, avec sa référence : aucune condition d'âge n'est plus opposable.
  - **Résultat modifié.** À partir du 1er janvier 1989, `cnrps_age_requis` rend 0 au lieu de 50 pour les mères de trois enfants, et `cnrps_eligible` devient vrai pour celles qui remplissent la condition de durée — quinze ans de services, inchangée — sans avoir atteint 50 ans. Une mère de 45 ans totalisant seize ans de services n'ouvrait pas droit ; elle ouvre droit désormais. Les mères de 50 ans et plus, seules que les tests couvraient jusqu'ici, sont inchangées.
  - **La formule n'est pas modifiée**, et c'est délibéré : `cnrps_age_requis` lit déjà le paramètre dans la branche des mères de trois enfants. Corriger la valeur datée corrige la formule là où elle se trompait, sans toucher à un `select` que les questions ouvertes de #37 destinent à un remaniement. Une valeur de 0 s'y compose correctement, la condition `age >= age_requis` étant alors toujours vraie.
  - **L'état antérieur à 1989 n'est pas établi par les textes lus, et le paramètre le dit.** L'article 5, 2° e) de la loi n° 85-12 ouvre le départ des mères sans fixer d'âge ; l'article 41, dans sa rédaction de 1985, diffère la jouissance jusqu'à 50 ans pour les agents mis à la retraite « sur leur demande », sans nommer les mères. Qu'elles relèvent de cette catégorie est une lecture possible — vraisemblablement celle dont la valeur procède — mais elle n'est écrite nulle part, et la réécriture de 1988, qui range les mères dans un cas **distinct** de la demande ordinaire, invite plutôt à en douter. La valeur de 50 ans est néanmoins **conservée** pour 1985-1988, en étant déclarée non sourcée : la retirer rendrait tout calcul CNRPS impossible du 12 septembre 1985 au 31 décembre 1988, `cnrps_age_requis` évaluant toutes les branches de son `select` pour tous les individus. Conserver une valeur non sourcée en la déclarant telle a paru préférable à fermer trois ans de calculs ; le choix est réversible.
  - **Date de départ corrigée** : du 5 mars 1985, date de **signature** de la loi n° 85-12 que la convention du dépôt rejette, au 12 septembre 1985, date de son **effet** (article 75) — comme les autres paramètres du même bloc depuis la version 5.4.0. Aucun calcul n'aboutissait de toute façon avant cette date.
  - Tests : `tests/formulas/test_meres_trois_enfants.yaml`, écrit en YAML comme le reste des tests de formules du dépôt, porte **douze cas** — l'âge requis avant 1989 (50 ans, en 1986 et en 1988) et après (0, en 1989, 1990 et 2024), l'éligibilité de la mère de 45 ans de part et d'autre de la bascule, la stabilité du cas de 52 ans que couvraient déjà `test_anticipe.py` et `test_depart_anticipe.yaml`, et l'invariance de la durée requise de quinze ans, pour établir que seule la condition d'âge bouge. Les cas d'éligibilité prennent `cnrps_salaire_de_reference` en entrée plutôt que `cnrps_salaire_de_base`, ce qui dit la même chose sans traverser l'agrégation sur quarante ans. Aucun test existant n'est modifié. `make test` : 116 tests passent, contre 104 sur la branche de base.
  - _Un seul cas n'est pas repris en YAML : celui du 12 septembre 1985, premier jour d'application, qui demande une période annuelle commençant en cours d'année — le lanceur de tests YAML y résout bien les paramètres, mais n'y fait pas atterrir les variables d'entrée. Il était redondant avec 1986, qui lit la même valeur du paramètre et qui est couvert._
  - Rapport d'audit régénéré : 50 paramètres sur 53 ont une référence, contre 49 ; il n'en reste que trois sans source — `bonifications.militaire.bonus`, `rsa.pension_min` et `rsa.periode_remplacement_base`, tous trois documentés comme tels. Les paramètres multi-dates passent de 20 à 21, et la loi n° 88-71 est citée par deux paramètres au lieu d'un.

<!-- -->

## 5.6.0 - [#42](https://github.com/openfisca/openfisca-tunisia-pension/pull/42)

* Évolution du système socio-fiscal.
* Périodes concernées : jusqu'au 11/09/1985 (bonifications CNRPS, qui n'aboutissent plus) ; à partir du 12/09/1985, résultats inchangés.
* Zones impactées : `regimes/cnrps`, `variables/cnrps`.
* Détails :
  - **Les bonifications CNRPS lisent enfin leurs paramètres** (issue #29). `cnrps_bonifications` calculait le barème en dur, sous un commentaire — « Hardcoding the rules as the YAML parameter mapping seems to be failing » — qui datait d'un temps où la lecture des paramètres échouait. Les paramètres `retraite.cnrps.bonifications.**`, datés du 12 septembre 1985 et sourcés sur l'article 32 de la loi n° 85-12, n'étaient lus par aucune formule. Ils le sont désormais : `cadre_actif.service_35`, `service_25`, `service_20` et `service_15` remplacent les constantes 5, 4, 3 et 2, et `militaire.bonus` remplace la constante 5. La correction porte sur les **deux** fichiers, `regimes/cnrps.py` et `variables/cnrps.py` — ce dernier est engendré à partir du premier par `scripts_ast/script_ast.py`, et une correction portée au seul fichier engendré serait défaite à la prochaine régénération.
  - **Les résultats sont inchangés, et les tests écrivent en clair ce que le droit commande.** `tests/formulas/test_bonifications_parametrees.yaml` suit la convention du dépôt et porte **vingt cas** : les quatre seuils de l'article 32 encadrés des deux côtés (0 et 14 ans, sans bonification ; 15 et 19 ; 20 et 24 ; 25 et 34 ; 35 et 40, où le barème plafonne), le seuil de 20 ans des militaires encadré de même (19, 20, 30), le cumul des deux bonifications, la stabilité des valeurs en 1986, 2019 et 2020, et la durée d'assurance en bout de chaîne. Les valeurs attendues sont écrites sous la forme `2 * 4`, `(2 + 5) * 4`, qui laisse voir l'année de bonification et sa conversion en trimestres. Les **dates de 2019 ne jouent pas** sur ce calcul — la loi n° 2019-37 ne déplace que le repère d'âge de l'article 32, que la formule ne modélise pas —, et deux cas le constatent plutôt que de le supposer.
  - _Deux cas n'ont pas pu s'exprimer en YAML, et ne sont pas maintenus ailleurs en silence. Le **premier jour d'application, le 12 septembre 1985** : l'éprouver suppose une période annuelle commençant en cours d'année (`year:1985-09-12`), pour laquelle le lanceur de tests YAML résout bien les paramètres, mais **ne fait pas atterrir les variables d'entrée** — `duree_service_cadre_actif: 35` y est lu comme 0, et le cas passerait en testant un agent sans services. Un tel cas serait vert sans rien prouver. Le premier exercice entier sous la loi, 1986, est couvert. Et **l'erreur explicite avant cette date** : les tests YAML ne savent pas affirmer qu'un calcul lève une exception. Ce comportement reste couvert, pour les variables voisines, par `tests/formulas/test_astreignants.py`._
  - **Conséquence assumée : les bonifications ne se calculent plus avant le 12 septembre 1985.** Comme tout paramètre de ce dépôt depuis la version 5.4.0, `bonifications.cadre_actif.**` commence à la date d'effet de la loi n° 85-12, et la formule lève désormais une erreur explicite avant cette date, là où l'arithmétique en dur rendait un nombre. `cnrps_bonifications` et `cnrps_duree_assurance` sont directement calculables — les tests existants les appellent sans passer par `cnrps_age_requis` —, la période est donc réellement atteignable, et le changement réel. Il aligne les bonifications sur `cnrps_age_requis`, `cnrps_duree_requise_annees` et `cnrps_taux_de_liquidation`, qui n'aboutissent pas non plus avant cette date. Mieux vaut une erreur explicite qu'une valeur que nul texte lu n'appuie.
  - _Effet de bord à signaler : `bonifications.militaire.bonus` porte la date du 5 mars 1985 — une date de signature, que la convention du dépôt rejette, conservée faute de texte qui fixe cette valeur. La formule lisant dans le même souffle les paramètres du cadre actif, qui commencent le 12 septembre 1985, cette date antérieure est désormais **inatteignable par le calcul**, comme l'est depuis la version 5.4.0 le barème d'annuités CNRPS du 1er février 1959._
  - **Ce que la formule ne fait toujours pas, et que l'article 32 dit.** La parenthèse mérite d'être ouverte, car brancher les paramètres ne corrige pas la règle. L'article 32 vise **trois** catégories, et ne leur applique pas la même règle : pour les **ouvriers accomplissant des travaux pénibles et insalubres**, le barème 5 / 4 / 3 / 2 est la bonification elle-même ; pour les **agents exerçant des fonctions astreignantes** et pour les **cadres actifs**, la bonification est « la période restant à courir jusqu'à 60 ans » — 62 ans depuis la loi n° 2019-37 (article 2) —, que le barème vient seulement **plafonner**. La formule applique le barème comme valeur pour tout le monde, ne connaît qu'une seule durée d'entrée (`duree_service_cadre_actif`, dont le libellé réunit « cadre actif ou travaux pénibles »), et ne porte aucun paramètre de repère d'âge. Le calcul conservé n'est donc pas celui du texte pour deux des trois catégories : il surestime la bonification de l'agent proche du repère d'âge, et la sous-estime pour celui qui en est loin. La question de savoir lequel des deux calculs suit le texte n'a qu'une réponse honnête : ni l'un ni l'autre pour ces deux catégories, l'ancien comme le nouveau. Ce qui change ici, c'est que les valeurs sont lues là où elles sont datées et sourcées ; la structure de l'article 32 reste à modéliser, et elle demande des paramètres et une variable d'entrée que le dépôt n'a pas.
  - **Régimes spéciaux et article 67 non traités**, faute de paramètres : l'article 67 accorde aux militaires mis à la retraite d'office ou ayant atteint la limite d'âge de leur grade la période restant à courir jusqu'à 60 ans, puis 62 ans depuis 2019 — et non un forfait de cinq ans. Le seuil de 20 ans de services militaires que porte la formule n'est lui non plus appuyé par aucun texte lu, et n'a pas de paramètre. Ces points sont posés en questions ouvertes, non tranchés.
  - `make test` : 104 tests passent, contre 84 sur `master` ; aucun test existant n'est modifié.
  - Rapport d'audit régénéré : il change d'une seule ligne, celle des paramètres de retraite accédés par `variables/cnrps.py`, qui gagne `retraite.cnrps.bonifications`. Aucun paramètre n'est ajouté, retiré, redaté ni resourcé.

<!-- -->

### 5.5.1 - [#41](https://github.com/openfisca/openfisca-tunisia-pension/pull/41)

* Changement mineur.
* Périodes concernées : aucune.
* Zones impactées : aucune — notes de référence et documentation seules.
* Détails :
  - **Citation de l'article 5 de la loi n° 2019-37 reprise sur le fascicule** (issue #40). Les notes de `cnrps.age_legal.civil.fonctions_astreignantes` et `cnrps.age_legal.civil.ouvriers_travaux_penibles` résumaient le calendrier transitoire en écrivant « contrairement aux dispositions des articles 24, 27, 28, 29 et 61 (nouveaux) ». Le texte publié fait suivre **chaque** numéro de sa propre mention : « contrairement aux dispositions des articles 24 (nouveau), 27 (nouveau), 28 (nouveau), 29 (nouveau) et 61 (nouveau) ». La citation est désormais donnée in extenso, comme celle que porte déjà `depart_anticipe.sur_demande.astreignants.age_minimum`, et la mention « La loi ne comporte pas de clause d'entrée en vigueur » cède la place à « Dates d'effet énoncées par le texte » : l'article 5 énonce bien le 1er juillet 2019 et le 1er janvier 2020. Source : JORT n° 35 du 30 avril 2019, p. 1314.
  - **`retraite.rsa.periode_remplacement_base` : dix ans que nul texte lu n'appuie** (issue #32, second point). Le paramètre reçoit une `documentation` qui le constate. L'article 50 de la loi n° 81-6 retient les **trois ou cinq dernières années**, la plus avantageuse des deux ; aucune fenêtre de dix ans n'y figure, ni ailleurs dans les articles lus du régime des salariés agricoles. Aucune source n'est inventée : la valeur est conservée, son origine déclarée non établie, et sa date du 1er janvier 1981 explicitée comme celle du bloc RSA — l'entrée en vigueur de la loi n° 81-6 énoncée par son article 88 — et non comme celle d'un texte qui fixerait dix ans. La documentation renvoie à l'issue #24, qui porte le même sujet : les textes disent les **dernières** années là où les formules retiennent les **meilleures**.
  - _Le premier point de l'issue #32 — la documentation de `cnrps.age_legal.civil.cadres_actifs`, qui décrivait encore les ouvriers des travaux pénibles — a été traité par la version 5.5.0._
  - Valeurs, dates et formules inchangées. Les tests passent sans modification.

<!-- -->

## 5.5.0 - [#35](https://github.com/openfisca/openfisca-tunisia-pension/pull/35)

* Évolution du système socio-fiscal.
* Périodes concernées : du 12/09/1985 au 23/09/1985 (calculs CNRPS, qui échouaient) ; à partir du 01/07/2019 (âge requis des agents exerçant des fonctions astreignantes) ; ailleurs, dates, références et documentation seules.
* Zones impactées : `parameters/retraite/cnrps/depart_anticipe/sur_demande/astreignants`, `parameters/retraite/cnrps/age_legal/civil`.
* Détails :
  - **Aucun calcul CNRPS n'aboutissait avant le 24 septembre 1985.** `cnrps_age_requis` et `cnrps_duree_requise_annees` lisent, pour tous les individus, `depart_anticipe.sur_demande.astreignants.age_minimum` et `duree_minimum`, qui ne commençaient qu'à cette date ; `cnrps_taux_de_liquidation`, `cnrps_eligible` et `cnrps_pension` levaient `ParameterNotFoundError`. Ils se calculent désormais à partir du **12 septembre 1985**, date d'effet de la loi n° 85-12 : avec 80 trimestres, le taux de liquidation vaut 50 % (article 38). Avant cette date, ils lèvent toujours `ParameterNotFoundError`, et c'est voulu : aucune condition d'ouverture du droit n'est portée avant l'effet de la loi, faute de texte lu pour la période de la loi n° 59-18 (voir 5.4.0). Le barème d'annuités CNRPS du 1er février 1959 reste encodé et sourcé, mais aucun calcul ne peut l'atteindre.
  - **Source et date d'effet.** Les deux paramètres citaient le décret n° 85-1178 du 24 septembre 1985 et prenaient sa date de signature. Les 55 ans et 35 ans de services sont fixés par l'article 28 de la loi n° 85-12 (JORT n° 20 du 12 mars 1985, p. 361), qui entre en vigueur le 12 septembre 1985 (article 75). Le décret n° 85-1178 ne fait que dresser la liste des fonctions astreignantes, et prend effet le 1er juillet 1986 (article 2) ; il est cité dans la documentation. Aucune valeur n'est portée avant le 12 septembre 1985 : la valeur antérieure, identique et sans source, serait la même valeur mal datée, comme celles que la version 5.4.0 a retirées des paramètres `cadre_commun`, `meres_3_enfants` et `duree_de_service_minimale` que la même formule lit dans le même `select`.
  - **Relèvement de 2019.** `astreignants.age_minimum` passe à 56 ans au 1er juillet 2019 et à 57 ans au 1er janvier 2020 (loi n° 2019-37 du 30 avril 2019, article premier, article 28 nouveau, et article 5), comme `age_legal.civil.fonctions_astreignantes`. Il restait à 55 ans. La durée de 35 ans est inchangée.
  - Les paramètres gardent leur nom : l'article 28 fixe les conditions d'une mise à la retraite, non d'un départ anticipé sur demande. La documentation le dit, et renvoie à `age_legal.civil.fonctions_astreignantes`, qui porte le même âge en données.
  - `age_legal.civil.cadres_actifs` ne documente plus les ouvriers accomplissant des tâches pénibles et insalubres, portés par `age_legal.civil.ouvriers_travaux_penibles` ; sa référence ne rattache plus les cadres actifs au décret n° 85-1177, qui fixe la liste de ces ouvriers. Valeurs inchangées.
  - Les calculs restent impossibles avant le 12 septembre 1985 : toutes les branches de `cnrps_age_requis` et de `cnrps_duree_requise_annees` commencent à cette date.
  - Tests : `tests/formulas/test_astreignants.py` vérifie le taux de liquidation au 12 et au 24 septembre 1985, l'âge et la durée requis des astreignants au 12 septembre 1985, en 2019 et en 2020, et constate l'erreur explicite attendue au 1er juin et au 11 septembre 1985, en disant pourquoi elle vaut mieux qu'une valeur inventée. Aucun test existant ne change.
  - Rapport d'audit régénéré : le décret n° 85-1178 n'est plus cité comme source de valeurs ; la loi n° 85-12 l'est par 25 paramètres, la loi n° 2019-37 par 5 ; les paramètres multi-dates passent de 19 à 20.

<!-- -->

### 5.4.1 - [#34](https://github.com/openfisca/openfisca-tunisia-pension/pull/34)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : `scripts/generate_pension_source_audit.py`.
* Détails :
  - Le rapport d'audit des sources rattachait quatre textes au mauvais fascicule du JORT : le décret n° 74-499 au n° 39 de 1974, le décret n° 82-1030 au n° 66 de 1982 et la loi n° 81-6 au n° 26 de 1981, qui publient leurs rectificatifs ; la loi n° 2009-20 au n° 100 de 2009, qui publie une circulaire de même numéro. Ils sont désormais rattachés aux n° 30 de 1974, 51 de 1982, 9 de 1981 et 30 de 2009.
  - _Le cache `jort_cache.db` range le rectificatif sous le type, le numéro et la date de signature du texte qu'il corrige, avec un identifiant plus petit ; la circulaire n'a pas de date de signature. Trié par date puis par identifiant, le mauvais enregistrement venait en tête, et seuls six textes pivots faisaient l'objet d'un contrôle de type._
  - Le choix du fascicule lit maintenant la référence : le type cité (« Décret n° », « Loi n° ») doit concorder avec celui de l'enregistrement ; un rectificatif passe toujours après le texte principal ; à égalité, le fascicule désigné par le lien pist.tn de la référence, puis l'année de signature, départagent les candidats.
  - Dans `parameters_candidates/retraite_source_candidates.yml`, les correspondances sont classées, rectificatifs en dernier, et la circulaire n° 2009-20 n'y figure plus.

<!-- -->

## 5.4.0 - [#25](https://github.com/openfisca/openfisca-tunisia-pension/pull/25)

* Évolution du système socio-fiscal.
* Périodes concernées : du 01/01/1985 au 11/09/1985 (barème d'annuités CNRPS) ; du 01/05/1986 au 31/10/1996 (indemnités familiales) ; du 25/06/2007 au 30/06/2007 (départ anticipé sur demande) ; jusqu'au 11/09/1985 (calculs CNRPS, qui n'aboutissent plus) ; jusqu'au 21/07/1982 et jusqu'au 31/12/1973 (calculs RSNA, qui n'aboutissent plus) ; ailleurs, dates et références seules.
* Zones impactées : `parameters/retraite/cnrps`, `parameters/retraite/rsna`, `parameters/retraite/rsa`.
* Détails :
  - Date et référence des paramètres de retraite, à partir d'un dépouillement du *Journal officiel* dont chaque article cité a été lu. Chaque valeur est datée de l'**effet** du texte qui la fixe, et chaque référence prend la forme structurée `title` + `href` pist.tn + `note` (fascicule, page, article, clause d'entrée en vigueur). Une date d'effet énoncée par le texte est reprise telle quelle. Quand un texte n'en énonce pas, la date retenue est celle à laquelle il devient exécutoire selon la règle générale : « un jour franc après la publication » avant 1993 (article 3 nouveau du décret du 27 janvier 1883, rédaction du 13 septembre 1956), « cinq jours après le dépôt du journal officiel » au siège du gouvernorat de Tunis depuis la loi n° 93-64 du 5 juillet 1993 (article 2) ; la note donne le calcul. Ni la signature ni la publication ne servent de date d'effet.
  - **Loi n° 85-12 : effet au 12 septembre 1985.** Son article 75 la fait entrer en vigueur six mois après sa publication, faite le 12 mars 1985. Les paramètres qui la dataient du 5 mars 1985 (signature), et le barème d'annuités qui la datait du 1er janvier 1985, passent au 12 septembre 1985 — la date qu'`openfisca-tunisia` retient déjà pour les cotisations.
  - **Aucune valeur sans source.** Quand une date recule et que l'état antérieur est établi, il est encodé avec sa référence : le taux de réversion de 75 %, la pension minimale des deux tiers du SMIG et le plafond de 80 % valent dès le 1er mai 1981 (loi n° 81-70, article 4, qui remplace les articles 22 et 31 de la loi n° 59-18). Sinon, **la valeur antérieure est retirée**. Elle était identique à la valeur sourcée qui la suit et portait une date conventionnelle du modèle — 5 mars 1985 (signature de la loi n° 85-12), 1er janvier 1974, 1er février 1959, 1er janvier 1960 — sans qu'aucun texte ne l'appuie : ce n'est pas un état du droit antérieur, c'est la même valeur mal datée. Dix-huit paramètres commencent désormais à la date du texte lu : les quatre bonifications des cadres actifs, l'âge des enfants et la durée des mères de trois enfants, l'âge et la durée du départ sur demande du cadre commun, la durée de service minimale, l'allocation de vieillesse et sa durée, le minimum garanti, les trois paramètres des survivants (12 septembre 1985) ; l'âge de départ anticipé et le plancher de la moitié du SMIG du RSNA (22 juillet 1982) ; le barème d'annuités du RSNA (1er janvier 1974).
  - **Conséquence assumée : des calculs qui n'aboutissent plus.** `cnrps_age_requis` et `cnrps_duree_requise_annees` évaluent toutes les branches de leur `select` : aucun calcul CNRPS n'aboutit avant le 12 septembre 1985, faute de texte lu pour la période de la loi n° 59-18 — le barème d'annuités CNRPS du 1er février 1959, correctement sourcé, devient de ce fait inatteignable par le calcul. De même, `rsna_taux_de_liquidation` ne se calcule pas avant le 1er janvier 1974, et le départ anticipé et le plancher de la moitié du SMIG du RSNA pas avant le 22 juillet 1982. Mieux vaut une erreur explicite qu'une valeur inventée : une valeur reconduite en arrière sans texte se présente comme du droit, et se propage dans les résultats sans qu'on puisse la distinguer d'un état sourcé.
  - **Résultats modifiés.**
    - `retraite.cnrps.bareme_annuite`, du 1er janvier au 11 septembre 1985 : le barème de la loi n° 59-18 (0,5 % par trimestre) s'applique au lieu de celui de la loi n° 85-12 (2 %, 3 %, 2 % par année), qui n'était pas en vigueur. En pratique, `cnrps_taux_de_liquidation` ne se calcule pas pour 1985, avant comme après : les paramètres `depart_anticipe.sur_demande.astreignants`, qu'il lit par `cnrps_duree_requise_annees`, ne commencent que le 24 septembre 1985, et les autres branches de la même formule — cadre commun, mères de trois enfants, `duree_de_service_minimale` — que le 12 septembre 1985.
    - `cnrps_indemnites_familiales`, du 1er mai 1986 au 31 octobre 1996 : 7,600 / 6,500 / 5,600 / 4,700 dinars au lieu de 7,320 / 6,507 / 5,693 / 4,880. Les valeurs portées étaient exactes, mais ce sont celles du décret n° 96-1906, effet 1er novembre 1996 ; elles étaient rattachées à un « décret n° 85-611 du 3 juin 1986 » qui n'existe pas. La série devient : décret n° 86-611 au 1er mai 1986, décret n° 88-1136 au 1er janvier 1989 (trois rangs), décret n° 96-1906 au 1er novembre 1996. Le quatrième rang garde 4,700 dinars de 1989 à 1996 : la loi n° 88-39 limite le droit aux trois premiers enfants à compter de 1989 mais « ne s'applique pas aux droits acquis antérieurement au 1er janvier 1989 », et le décret n° 88-1136 n'abroge pas le décret de 1986, abrogé seulement en 1996. La formule ne teste pas le droit acquis.
    - Départ anticipé sur demande du cadre commun : la loi n° 2007-43, sans clause d'entrée en vigueur, publiée le 26 juin 2007, est datée du 1er juillet 2007, date à laquelle elle devient exécutoire (loi n° 93-64, article 2), et non plus de sa signature, le 25 juin.
  - **RSNA** : le barème d'annuités, rattaché à tort à la loi n° 60-33 et daté de 1960, est celui de l'article 17 du décret n° 74-499 (effet 1er janvier 1974), reformulé à l'identique par l'article 4 du décret n° 82-1030. L'âge de départ anticipé (article 15 bis) et le plancher de la moitié du SMIG (article 45 nouveau) sont créés par le décret n° 82-1030, publié au JORT daté des 20-23 juillet 1982 et obligatoire le 22 juillet 1982 selon la règle du jour franc. Âge légal, stage, plafond de 80 %, plancher des deux tiers et stage de 60 mois sont sourcés sur le décret n° 74-499.
  - **RSA** : les cinq paramètres fixés par la loi n° 81-6 (articles 48 et 49) passent du 24 février 1981 — date qui correspond à la signature du décret n° 81-224, relatif aux cotisations — au 1er janvier 1981, date d'entrée en vigueur énoncée par l'article 88.
  - **CNRPS** : professeurs de l'enseignement supérieur à 65 ans au 19 avril 2009 (loi n° 2009-20, article 29 bis), au lieu du 1er avril 2019 ; âge des enfants des mères de trois enfants porté à 20 ans au 1er janvier 1989 (loi n° 88-71, dont l'article 4 fixe l'effet six mois après la publication du 1er juillet 1988), au lieu du 27 juin 1988 ; conditions d'âge des orphelins rattachées à la loi n° 97-59 (effet 1er mai 1997) puis à la loi n° 2007-43, et non plus à la loi n° 85-12.
  - **Trois paramètres ajoutés, en données seulement** — aucune formule ne les lit : `cnrps.plaf_taux_pension` (80 % au 1er mai 1981, 90 % au 12 septembre 1985, article 38 de la loi n° 85-12) ; `cnrps.age_legal.civil.ouvriers_travaux_penibles` et `cnrps.age_legal.civil.fonctions_astreignantes` (articles 27 et 28 : 55 ans, puis 56 et 57 ans selon le calendrier de la loi n° 2019-37).
  - **Références retirées, faute de texte.** `cnrps.bonifications.militaire.bonus` (5 ans) était rattaché à l'article 32 de la loi n° 85-12, qui ne vise pas les militaires ; l'article 67 leur accorde la période restant à courir jusqu'à 60 ans, puis 62. `cnrps.depart_anticipe.meres_3_enfants.age_minimum` (50 ans) était rattaché à l'article 5, qui ne fixe pas d'âge ; depuis 1989, l'article 41 nouveau rend la jouissance immédiate. Les deux valeurs sont conservées et documentées.
  - **Sans texte, documentés** : `rsa.pension_min` (0,4 SMAG), qu'aucun article de la loi n° 81-6 n'appuie ; les montants de l'indemnité de revenu unique, dont la seule source est le *Manuel de liquidation* de la CNRPS (2013, p. 94), document non normatif — la loi n° 81-70 ouvre le droit au 1er mai 1981 sans fixer de montant.
  - Les tests passent sans modification : aucun ne porte sur les périodes dont le résultat change.
  - Rapport d'audit régénéré : 49 paramètres sur 53 ont une référence, contre 31 sur 50. Les paramètres multi-dates tombent de 32 à 19, le retrait des valeurs antérieures non sourcées ayant supprimé treize dates qui ne correspondaient à aucun texte. Le texte fantôme « 2024-9 », lu dans une date « 24-09-1985 » d'un titre, disparaît.

<!-- -->

### 5.3.1 - [#19](https://github.com/openfisca/openfisca-tunisia-pension/pull/19)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : aucune — outillage seul.
* Détails :
  - Ajoute `scripts/generate_pension_source_audit.py`, qui dresse la carte de ce qui est sourcé et de ce qui ne l'est pas : couverture par régime, textes cités, paramètres sans référence, paramètres multi-dates, et rapprochement avec le corpus JORT local quand il est disponible. Sortie dans `reports/openfisca/pension_source_audit.md` et `parameters_candidates/retraite_source_candidates.yml`.
  - **Ce que l'audit établit aujourd'hui** : 50 paramètres portent une valeur ou un barème, **31 ont une référence et 19 n'en ont aucune**. Les sept paramètres du régime des salariés agricoles n'en ont pas une seule, et portent tous la même date conventionnelle du 24 février 1981.
  - Il isole aussi un texte impossible : le décret cité « n° 85-611 du 3 juin 1986 », dont le millésime et l'année ne peuvent pas être justes tous les deux. Le rapport le classe « à résoudre ».
  - **Correction au passage** : l'extraction des numéros de texte lisait aussi le champ `note`, dont les plages de pages — « pp. 1312-1315 » — ont exactement la forme d'un numéro de loi. Le rapport annonçait un « texte 1312-1315 » à résoudre. Elle ne lit plus que `title` et `href`.

<!-- -->

## 5.3.0 - [#21](https://github.com/openfisca/openfisca-tunisia-pension/pull/21)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 1985-03-05.
* Zones impactées : `parameters/retraite/cnrps/survivants`, `parameters/retraite/cnrps/capital_deces`, `variables/survivants.py`.
* Détails :
  - **Survivants — loi n° 85-12 du 5 mars 1985.** Les taux de réversion étaient des constantes écrites dans `variables/survivants.py`. Ils deviennent des paramètres datés et référencés : `taux_conjoint` (0,75 — article 43), `taux_orphelin` (0,10 — article 45), `plafond_cumul` (1,0 — article 45) et `taux_partage_5_orphelins` (0,50 — article 45).
  - **Capital-décès — décret n° 93-308 du 1er février 1993.** Même traitement : `majoration_par_enfant` (0,10), `multiplicateur_deces_accidentel` (2,0), `plafond_anciennete_mois` (18) et le barème `taux_retraite_selon_age`, dégressif de 100 % avant 60 ans à 10 % à partir de 85 ans (article 6).
  - Le remaniement **préserve les résultats** : les six tests de `test_survivants` et les trois de `test_capital_deces` passent à l'identique.
  - **Localisations JORT** ajoutées aux références qui n'en avaient pas — lois n° 59-18, 60-33, 85-12, 88-71, 2007-43 —, et **vingt-trois références converties de la chaîne libre à la forme structurée** `title` + `href` + `note`, avec l'URL du fascicule sur pist.tn. Une référence en texte libre ne se vérifie pas ; une URL, si.
  - Neuf références restent en texte libre, faute d'URL vérifiée : les indemnités du décret « n° 85-611 du 3 juin 1986 » — dont le millésime et l'année se contredisent —, la loi n° 81-70 des indemnités de revenu unique, et le décret n° 85-1178 des départs anticipés astreignants.

<!-- -->

## 5.2.0 - [#23](https://github.com/openfisca/openfisca-tunisia-pension/pull/23)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 2020-01-01.
* Zones impactées : `parameters/marche_travail`, pensions minimales de tous les régimes.
* Détails :
  - Ce paquet lit désormais les sous-arbres de paramètres dont `openfisca-tunisia` est propriétaire **chez lui**, greffés au chargement, au lieu d'en garder une copie. La copie locale de `marche_travail` est supprimée.
  - **Le SMIG était figé depuis 2019.** Les deux paquets portaient chacun leur `marche_travail`, et les copies avaient divergé sans que rien ne le signale : la série s'arrêtait ici au 1er mai 2019 avec 36 références, quand celle d'`openfisca-tunisia` court jusqu'au 1er janvier 2025 avec 110. Le SMIG 40 h lu passe de **343,892 dinars** gelés à **448,238** en 2025.
  - **Conséquence sur les calculs** : les pensions minimales — `minimum_garanti` et `allocation_vieillesse` du CNRPS, `inf` et `sup` du RSNA — sont indexées sur le SMIG. Elles étaient donc **fausses de 2020 à 2026**, d'une valeur périmée et non d'une valeur manquante : rien ne le signalait.
  - La règle qui en découle : un sous-arbre de paramètres a un propriétaire et un seul. `retraite/` appartient à ce paquet, `marche_travail/` à `openfisca-tunisia`, dont la PR #402 a retiré sa copie morte de `retraite/`. `tests/test_parametres_partages.py` interdit le retour de la duplication.
  - Trois éléments que seul l'autre paquet portait sont récoltés au passage : l'URL du fascicule du JORT sur les âges légaux du cadre commun et des cadres actifs — dont les références en texte libre deviennent structurées et gagnent leur page —, le paragraphe sur l'option de report des enseignants du supérieur introduite par la loi n° 2019-37, et `rsna/plaf_taux_pension.yaml`.
  - Le plancher d'`openfisca-core` monte à **44.0.3**, puisque c'est ce qu'`openfisca-tunisia` exige. Le patch compte : `.github/get_minimal_version.py` épingle le plancher **à l'exact** pour la matrice « minimal », et `44.0.0` n'a jamais été publiée — la série 44 commence à 44.0.3. Un plancher qui n'existe pas rend la résolution minimale insatisfiable.

<!-- -->

### 5.1.1 - [#22](https://github.com/openfisca/openfisca-tunisia-pension/pull/22)

* Amélioration technique.
* Périodes concernées : aucune.
* Zones impactées : aucune.
* Détails :
  - Élargit les bornes de dépendance à `openfisca-core >=43.0.0, <45.0.0` et `numpy >=1.24.3, <3`, et rafraîchit `uv.lock`, qui restait sur core 43.5.0.
  - **Les deux bornes devaient bouger ensemble.** Élargir la seule borne d'`openfisca-core` ne suffit pas : sur Python 3.13, core 44 exige `numpy >=2.1.0`, que le plafond `numpy <2` interdisait. Le résolveur retombait alors silencieusement sur core 43, y compris en résolution `maximal` — de sorte que la CI validait une compatibilité avec core 44 qu'elle ne testait pas.
  - Le verrou est rafraîchi **par mise à jour ciblée** (`uv lock --upgrade-package openfisca-core --upgrade-package numpy`) et non globale : trois paquets sur cent dix-huit bougent. Une mise à jour globale emportait aussi `ruff` de 0.15.5 à 0.16.6, dont les règles nouvelles font échouer le lint sur les variables engendrées par `script_ast` — une remontée d'outil n'a pas sa place dans un correctif de dépendance.
  - Compatibilité vérifiée localement, dépendances effectivement installées : `openfisca-core 44.7.1`, `numpy 2.4.6`, `ruff` inchangé, lint propre et les 53 tests passent.
  - Ce changement ne modifie aucun calcul. Il lève le seul obstacle technique à ce que ce paquet dépende d'`openfisca-tunisia`, dont les bornes sont `openfisca-core >=44, <45` — préalable à la fin de la duplication des paramètres partagés entre les deux dépôts, au premier rang desquels le SMIG, arrêté ici au 1er mai 2019 et courant jusqu'au 1er janvier 2025 dans l'autre.

<!-- -->

# 5.1.0

* Amélioration technique.
* Périodes concernées : toutes.
* Détails :
  - Alignement CI et outillage sur openfisca-tunisia : Ubuntu 24.04, Python 3.10–3.12, uv (sync, cache), Node.js 24
  - Lint : passage à ruff uniquement (remplacement de flake8), per-file-ignores pour les variables générées (script_ast)
  - Makefile : même structure que openfisca-tunisia (format-style, check-style, uv run)
  - Tests YAML : clé `individu` remplacée par `input` (API openfisca_core) ; tests taux_de_liquidation en 1986 avec attendus ajustés ; correction salaire_de_reference attendu
  - CI : suppression du job test-api ; dépendance tomli pour get_minimal_version (Python 3.10)
  - Documentation des règles ruff dans pyproject.toml

# 5.0.0 [#15](https://github.com/openfisca/openfisca-tunisia-pension/pull/15)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `variables/regimes/cnrps`.
* Détails :
  - Introduit le régime de la CNRPS


# 4.0.0 [#14](https://github.com/openfisca/openfisca-tunisia-pension/pull/14)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `variables/regimes`.
* Détails :
  - Sépare les régimes dans différents répertoires

# 3.0.0 [#13](https://github.com/openfisca/openfisca-tunisia-pension/pull/13)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `parameters/pension`, `parameters/retraite`.
* Détails :
  - Renomme `parameters/pension` en  `parameters/retraite`

### 2.0.1 [#11](https://github.com/openfisca/openfisca-tunisia-pension/pull/11)

* Amélioration technique.
* Détails :
  - Utilise variables au lieu de model.
  - Utilise github actions et pyproject.toml.

### 2.0.0

* Migrate to openfisca-core v24 syntax
* Update `regime_securite_social` variable periodicity
* Details:
    * Move parameters from xml format to yaml files tree

### 1.0.0
* Renomme `nb_trim_val` en `duree_assurance`
* Utilisation de noms longs pour différent paramètres

## 0.9.2
* Migrate old-syntax formula

## 0.9.1
* Fix legislation tests

## 0.9.0
* Migrate to openfisca-core 14.0.1 syntax
* Use bottleneck.partition instead of deprecated bottleneck.partsort

## 0.8.0
* Migrate to openfisca-core 12.0.3 syntax
