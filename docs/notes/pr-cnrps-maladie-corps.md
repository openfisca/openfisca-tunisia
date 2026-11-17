> PR empilée sur #524 (`fix/cnrps-prevoyance-pensionnes-1973`). Base : cette branche ; à rebaser sur `master` une fois #523 et #524 fusionnées.

Suite de #524. La table « maladie » des agents de la CNRPS en activité représente le **régime obligatoire de prévoyance sociale** puis le **régime de base d'assurance maladie** (décret n° 2007-1406, **article 4**) — choix du régime obligatoire retenu par le propriétaire.

**Correctif de datation.** La part employeur partait d'un `1959-02-01` **sans appui textuel**. Le **décret n° 73-91 du 12 mars 1973**, article 16, fixe la contribution de l'État à **1 %** (« La contribution de l'Etat aux régimes obligatoires des prestations en nature et de Prévoyance Sociale est fixée à 1 % »), à compter du 1er avril 1973 (article 18) ; lu à l'image (JORT n° 10, p. 356). La part employeur commence donc au 1er avril 1973 (nulle de 1959 à mars 1973), comme la part salariale (article 14, déjà datée de 1973).

**Références précisées.** Les deux parts citent désormais le socle du décret n° 73-91 (art. 14 salarié, art. 16 employeur) et la montée en charge de l'article 4 du décret n° 2007-1406 : total 3 % en 2007 (salarié 1 %, employeur 2 %), 4,88 % en 2008 (1,88 % / 3 %), 6,75 % en 2009 (2,75 % / 4 %). Les **taux à partir de 2007 sont inchangés** : le modèle les encodait déjà correctement (le « 2 % en application » de l'art. 4 est le total pré-2007 — 1 % salarié + 1 % employeur —, et les 1,88 %/1,87 % sont les relèvements répartis 1 % employeur + 0,88 %/0,87 % salarié).

Textes et valeurs : `docs/notes/cnrps-prevoyance-73-91.md`. Nouveau test `tests/formulas/cotisations/cnrps_maladie_salaries_2007_1406.yaml` (valeurs en clair tirées du droit).

## Questions ouvertes

1. **Régime facultatif (art. 5) non modélisé**, conformément au choix du régime obligatoire. S'il faut aussi porter le régime facultatif d'assurance maladie (loi n° 72-2, décret n° 86-186 à 6,5 % → 6,75 %, répartition employeur 3/3,5/4 %, salarié 3,75/3,25/2,75 %), ce serait une variable d'entrée « adhésion au régime facultatif » et une table parallèle — à décider.
2. **Socle salarial pré-2007 : 1 % ou 2 % ?** L'article 4 suppose « 2 % en application » en 2007 ; le modèle garde 1 % (art. 14 du décret n° 73-91) jusqu'en 2008, l'employeur portant l'autre 1 % (art. 16). La date exacte où la part salariale « en application » aurait atteint 2 % n'est pas identifiée. Interprétation conservatrice retenue.

## Contrôles

- `uv run openfisca test ... tests/formulas/cotisations/cnrps_maladie_salaries_2007_1406.yaml` : 5 passés.
- `make test` (suite complète) : relancé sur cette branche (voir fil).
- `uv run yamllint` sur les deux fichiers modifiés : propre.
