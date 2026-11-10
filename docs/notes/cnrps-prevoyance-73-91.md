# Prévoyance et assurance maladie CNRPS — dossier de lecture

Textes lus dans le corpus `~/projets/PDFs-legislation-tunisie` (édition française scannée ou en
police chiffrée → lue à l'image par `pdftoppm`).

## Décret n° 73-91 du 12 mars 1973 (JORT n° 10 des 9, 13, 16 mars 1973, p. 356)
- **Art. 14** : la cotisation de l'assuré **actif** ayant opté pour le régime des prestations en
  nature (régime de prévoyance du décret du 12 avril 1951) est fixée à **1 %**, assise sur la
  rémunération soumise à retenue pour pension.
- **Art. 15** : cotisation supplémentaire du régime facultatif d'assurance-maladie = 3 % (6 % pour
  les personnels à l'étranger) + contribution mensuelle forfaitaire conjoint/enfants. Dernier
  alinéa : **« La cotisation due par le retraité et la veuve de retraité titulaire d'une pension
  directe ou de reversion est fixée à 2 % de leur pension en principal. »**
- **Art. 18** : « prend effet à compter du 1er avril 1973 » → date d'effet **1973-04-01**.

## Décret n° 2007-1406 du 18 juin 2007 (JORT n° 49 du 19 juin 2007, pp. 2154-2162)
- **Art. 2** : assiette des pensionnés = **montant brut de la pension**.
- **Art. 3** : taux du régime de base d'assurance maladie des actifs = **6,75 %**, progressif.
- **Art. 4** (CNRPS actifs, **régime obligatoire de prévoyance**) : 2007 → 3 % = 2 % (employé, socle
  73-91) + 1 % (employeur) ; 2008 → 4,88 % (supplément 1,88 % = 1 % employeur + 0,88 % employé →
  cumul employé 2,88 %, employeur 2 %) ; 2009 → 6,75 % (supplément 1,87 % = 1 % employeur + 0,87 %
  employé → cumul employé 3,75 %, employeur 3 %).
- **Art. 5** (CNRPS actifs, **régime facultatif** d'assurance maladie, loi n° 72-2, décret n° 86-186
  à 6,5 % → 6,75 %) : 2007 → employeur 3 %, employé 3,75 % ; 2008 → employeur 3,5 %, employé 3,25 % ;
  2009 → employeur 4 %, employé 2,75 %.
- **Art. 12** : taux maladie des titulaires de pension = **4 %** (atteint en 2010).
- **Art. 13** (pensionnés CNRPS, régime obligatoire de prévoyance) : **1 % (2007) → 2 % (2008) →
  3 % (2009) → 4 % (2010)**.

## Correctif appliqué (sujet 2a)
`pensionne_cnrps/prevoyance_sociale.yaml` : ajout de **2 % au 1973-04-01** (décret 73-91, art. 15) ;
la rampe 1→4 % de 2007 est redocumentée comme le régime de base d'assurance maladie (art. 12-13).

## Constats non tranchés (Questions ouvertes de la PR)
- **Articulation prévoyance 2 % / maladie 2007** : succession (la maladie remplace la prévoyance, le
  taux passant de 2 % à 1 % en 2007 puis remontant) ou cumul ? Pour les actifs (art. 4) le 2 % est
  **intégré** au total maladie ; par analogie les pensionnés verraient la maladie absorber la
  prévoyance — mais l'art. 13 part de 1 %, sans reprendre le 2 %. Question posée à une spécialiste
  (fiche précis `r-cnrps-cotisation-retraites-1973-2007`).
- **Sujet 2b — `salarie_cnrps` maladie** : les valeurs du modèle (employé 1 %/1,88 %/2,75 % ;
  employeur 2 %/3 %/4 %) ne concordent proprement **ni** avec l'art. 4 (obligatoire : employé
  2 %/2,88 %/3,75 %, employeur 1 %/2 %/3 %) **ni** avec l'art. 5 (facultatif : employé
  3,75 %/3,25 %/2,75 %, employeur 3 %/3,5 %/4 %). Le 1,88 %/1,87 % du modèle paraît être le *taux de
  cotisations supplémentaire* de l'art. 4 pris pour un niveau. Reconciliation à arbitrer (régime
  obligatoire ou facultatif ?) avant de réécrire ces valeurs : non touché ici.
- Régime de 1951 (décret du 12 avril 1951, prévoyance à 0,50 % sous plafond) : non lu.
