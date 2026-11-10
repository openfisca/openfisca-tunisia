# Corps de PR — sujet 1 (branche `fix/atmp-salaires-forfaitaires`)

> À relire par le propriétaire avant ouverture. Ne pas fusionner, attendre la CI.
> Numéro de PR à fixer à l'ouverture (placeholder `#523` dans le CHANGELOG).

## Titre

AT/MP : salaires forfaitaires (décret n° 95-538, art. 4 à 7 ; décrets n° 99-1010 et 2000-1439) et modulation (art. 10 à 27)

## Corps

Verse en paramètres les salaires forfaitaires d'accidents du travail et de maladies
professionnelles et la modulation des taux, jusqu'ici absents du modèle.

**Textes lus** (corpus `PDFs-legislation-tunisie`, édition arabe lue à l'image quand elle fait
foi) — voir le dossier `docs/notes/atmp-forfaits-95-538.md` :

- **Décret n° 95-538 du 1er avril 1995**, art. 4 à 7 (forfaits) et 10 à 27 (modulation) — JORT
  n° 30 du 14 avril 1995, éd. arabe pp. 691-692, **qui fait foi** ;
- **Décret n° 99-1010 du 10 mai 1999**, art. 1er (art. 4 §2 nouveau) — JORT n° 40, p. 734 ;
- **Décret n° 2000-1439 du 27 juin 2000**, art. 1er à 4 — JORT n° 52, p. 1541.

**Paramètres** (`prelevements_sociaux/atmp_forfaits/`, `prelevements_sociaux/atmp_modulation/`) :
forfait agricole et pêche (art. 4 : taux 1 % puis 0,80 % au 1er avril 1999, coefficient 1,5,
tableau des journées 1995/1999, base des réparations SMAG × 300 × coefficient 1/1,5/2) ;
chauffeurs de louage et taxis et masseurs des bains maures (art. 5) ; employés de maison (art. 6) ;
temporaires auprès des particuliers (art. 7) ; cotisation supplémentaire et réduction (art. 17, 18, 24).
Tous datés à l'entrée en vigueur (95-538 : 1er janvier 1995, art. 28 ; 99-1010 : 1er avril 1999 ;
2000-1439 : 1er juillet 2000), avec la date de publication relevée et la référence pist.tn dans
l'édition de la langue.

**Variable** : `cotisation_accident_travail_forfaitaire_employe_maison` calcule le seul forfait
entièrement déterminé par le droit (art. 6 : taux propres et assiette SMAG × 300). Test YAML en
valeurs claires tirées du droit (`tests/formulas/cotisations/`).

**Test Python aux bornes** (`tests/test_atmp_forfaits_95_538.py`) : les autres forfaits ne sont lus
par aucune variable ; comme un test YAML n'asserte que des variables, ce test lit les paramètres aux
dates charnières, selon la convention déjà posée par `tests/test_atmp_95_538.py` — déclaré ici
comme le demande la convention.

**Dépendance aval (précis)** : ces paramètres doivent alimenter, par un générateur, les tableaux
faits main `tbl-atmp-forfaits`, `tbl-atmp-journees` et `tbl-atmp-modulation` de
`precis/fr/cotisations_sociales/_accidents_travail.qmd`. Ne régénérer qu'**après publication** de
cette version et relèvement de la borne de version côté précis (les montants en dinars se déduiront
des séries du SMIG et du SMAG). Un ticket côté précis doit consigner la dépendance.

Closes #471.

## Questions ouvertes

1. **Arborescence des variables des autres forfaits.** Seul l'article 6 est calculé. Restent à
   trancher, avant de modéliser les cotisations : l'**option irrévocable pour les salaires
   effectifs** (art. 4) ; le schéma d'entrée du **forfait agricole** (surfaces par type de culture,
   nombre de têtes, barques/unités de pêche, qualification) ; le **taux de branche** applicable aux
   forfaits des art. 5 et 7, que les articles ne désignent pas ; l'intégration **annuelle vs
   mensuelle** (art. 7 : « tout mois commencé compté pour un mois entier »).
2. **Modulation (art. 10 à 27).** Décisions individuelles de la CNSS. Les quotités (50 %, 100 %,
   25 %) sont versées ; leur application à un cas relèverait d'une variable d'entrée « taux modulé ».
   Hors périmètre probable (cf. #471) : à confirmer.
3. **Partage employeur/salarié.** Les art. 4 à 7 fixent une cotisation globale, non ventilée entre
   employeur et salarié.
4. **Modificatifs des art. 6 et 7 après 1999.** Aucun identifié, mais la recherche n'a porté que sur
   95-538, 99-1010 et 2000-1439 (recherche précis `r-atmp-assiette-modificatifs` ouverte).
5. **Numéro de PR** du lien CHANGELOG à fixer à l'ouverture.

## Contrôles

- `uv run pytest tests/test_atmp_forfaits_95_538.py` : 29 passés.
- `uv run openfisca test --country-package openfisca_tunisia tests/formulas/cotisations` : 69 passés
  (dont le nouveau forfait des employés de maison).
- `uv run ruff check .` : OK ; `compileall` : OK.
- `uv run yamllint` sur `atmp_forfaits`, `atmp_modulation` et le test YAML : OK.
- Suite complète `make test` et `make check-all-yaml` : à relancer en CI (trop longues dans
  l'environnement de préparation ; changements purement additifs, l'arbre charge).
