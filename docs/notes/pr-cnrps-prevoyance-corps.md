# Corps de PR — sujet 2 (branche `fix/cnrps-prevoyance-pensionnes-1973`, empilée sur le sujet 1)

> À relire par le propriétaire avant ouverture. Ne pas fusionner, attendre la CI.
> Branche empilée sur `fix/atmp-salaires-forfaitaires` : ouvrir d'abord la PR du sujet 1, ou cibler
> cette PR sur `master` une fois le sujet 1 fusionné. Numéro de PR du CHANGELOG (`#524`) à fixer.

## Titre

CNRPS : la prévoyance sur pension commence au 1er avril 1973 à 2 % (décret n° 73-91, art. 15)

## Corps

Le fichier `pensionne_cnrps/prevoyance_sociale.yaml` faisait commencer la cotisation de prévoyance
des titulaires de pension de la CNRPS en 2007. Le **décret n° 73-91 du 12 mars 1973**, article 15,
dernier alinéa, la fixe à **2 % de la pension en principal** pour le retraité et la veuve de
retraité, à compter du **1er avril 1973** (article 18). Lu à l'image (JORT n° 10, p. 356 ; édition
française scannée). La rampe de 1 % à 4 % de 2007 à 2010 déjà présente est le **régime de base
d'assurance maladie** des titulaires de pension (décret n° 2007-1406, articles 12 et 13), qui
succède à cette prévoyance ; sa référence et sa note sont complétées, et la note périmée invoquant
une date de 1959 « sans appui textuel » est corrigée.

Textes lus et valeurs : voir `docs/notes/cnrps-prevoyance-73-91.md`.

**Test** : `tests/test_cnrps_prevoyance_73_91.py` lit le barème aux bornes (aucune variable ne lit ce
paramètre ; convention de `test_atmp_95_538.py`), déclaré ici comme le demande la convention.

## Questions ouvertes

1. **Succession ou cumul ?** De 1973 à 2007 la prévoyance est de 2 %. En 2007 le régime de base
   d'assurance maladie part de 1 % (art. 13). Si ce régime **remplace** la prévoyance, le taux
   descend de 2 % à 1 % en 2007 puis remonte à 4 % — ce que représente le fichier (une seule ligne).
   S'il s'y **ajoute**, les deux prélèvements coexisteraient. Pour les actifs (art. 4) le 2 % est
   intégré au total ; par analogie la maladie des pensionnés absorberait la prévoyance, mais l'art. 13
   ne reprend pas le 2 %. **Question posée à une spécialiste** (fiche précis
   `r-cnrps-cotisation-retraites-1973-2007`). À trancher avant de figer l'interprétation.
2. **Sujet 2b — table `salarie_cnrps` maladie (non traité ici).** Les valeurs du modèle (employé
   1 %/1,88 %/2,75 %, employeur 2 %/3 %/4 %) ne concordent proprement ni avec l'**article 4** du
   décret n° 2007-1406 (régime obligatoire : employé 2 %/2,88 %/3,75 %, employeur 1 %/2 %/3 %) ni avec
   l'**article 5** (régime facultatif : employé 3,75 %/3,25 %/2,75 %, employeur 3 %/3,5 %/4 %). Le
   1,88 %/1,87 % du modèle semble être le *taux de cotisations supplémentaire* de l'art. 4 pris pour
   un niveau. Il faut décider quel régime (obligatoire ou facultatif) le modèle des salariés CNRPS
   représente avant de réécrire ces valeurs. Proposé en PR suivante, empilée, une fois l'arbitrage
   rendu.
3. **Régime de 1951** (décret du 12 avril 1951, prévoyance à 0,50 % sous plafond) : non lu ; antérieur
   au périmètre.
4. **Numéro de PR** du lien CHANGELOG à fixer à l'ouverture.

## Contrôles

- `uv run pytest tests/test_cnrps_prevoyance_73_91.py` : 3 passés.
- `uv run yamllint` sur le fichier modifié : OK.
- Suite complète `make test` / `make check-all-yaml` : à relancer en CI.
