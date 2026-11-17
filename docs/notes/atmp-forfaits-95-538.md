# Salaires forfaitaires et modulation AT/MP — dossier de lecture (issue #471)

Textes lus dans le corpus `~/projets/PDFs-legislation-tunisie` (base `jort_cache.db`).
Édition arabe lue à l'image, qui fait foi pour le décret n° 95-538 (arts 4 à 7).

## Sources (fascicules, PDF locaux)

| Décret | JORT | Pages FR | Pages AR | PDF local FR | effet |
|---|---|---|---|---|---|
| n° 95-538 du 1er avril 1995 | n° 30 du 14 avril 1995 | 690-693 | 691-692 (arts 4-7) | `PDFs/JORT/1995/fr/Jo03095.pdf` | 1er janvier 1995 (art. 28) |
| n° 99-1010 du 10 mai 1999 | n° 40 du 18 mai 1999 | 732-734 | 897-898 | `PDFs/JORT/1999/fr/Jo04099.pdf` | 1er avril 1999 (art. 2) |
| n° 2000-1439 du 27 juin 2000 | n° 52 du 30 juin 2000 | 1541 | — | `PDFs/JORT/2000/fr/Jo0522000.pdf` | 1er juillet 2000 (art. 4) |

URL pist.tn (édition de la langue) :
- 95-538 FR https://www.pist.tn/jort/1995/1995F/Jo03095.pdf ; AR https://www.pist.tn/jort/1995/1995A/Ja03095.pdf
- 99-1010 FR https://www.pist.tn/jort/1999/1999F/Jo04099.pdf ; AR https://www.pist.tn/jort/1999/1999A/Ja04099.pdf
- 2000-1439 FR https://www.pist.tn/jort/2000/2000F/Jo0522000.pdf ; AR https://www.pist.tn/jort/2000/2000A/Ja05200.pdf

Note d'outillage : les éditions FR 1999 et 2000 ont une couche texte en police chiffrée
(pdftotext illisible) ; lues au **rendu image** (`pdftoppm -r 110`), qui affiche les glyphes corrects.
L'édition AR 1995 est sans couche texte (scannée), lue à l'image.

## Décret n° 95-538 (1er janvier 1995)

### Art. 4 — forfait agricole et pêche à la part
- Champ : secteur agricole non régi par la loi n° 89-73 du 2 septembre 1989 ; pêcheurs sur bateaux
  de moins de 30 tonnes (AR : tonneaux de jauge) payés à la part ; pour les travailleurs payés **au
  plus 2 × SMAG**.
- Cotisation annuelle = **1 %** du SMAG journalier × coefficient **1,5** × nombre de journées de
  travail selon le type de culture/activité (tableau ci-dessous).
- Base des prestations/réparations : salaire forfaitaire annuel = SMAG × **300 jours** × coefficient
  **1** (ordinaires, pêcheurs), **1,5** (spécialisés, ramendeurs, mécaniciens, seconds de patrons),
  **2** (qualifiés, patrons de pêche).
- Option irrévocable pour les salaires effectifs (arts 1-3).

Tableau des journées (1995 / **1999** après décret n° 99-1010) — unité :
| Type | Unité | 1995 | 1999 |
|---|---|---|---|
| Céréales en sec | j/ha | 7 | 7 |
| Céréales en irrigué | j/ha | 15 | 15 |
| Légumineuses et autres grandes cultures en sec | j/ha | 15 | 15 |
| Cultures industrielles (betterave à sucre, coton) | j/ha | 70 | 70 |
| Maraîchères plein champ : solanacées/tomates (AR 1995 : tomates seules) | j/ha | 150 | 150 |
| Maraîchères plein champ : pommes de terre et autres | j/ha | 50 | 50 |
| Horticulture plein champ (AR : floriculture) | j/ha | — | 70 |
| Oliviers et amandiers | j/ha | 17 | 17 |
| Vigne de cuve (en sec) | j/ha | 20 | 20 |
| Vigne de table | j/ha | 40 | 40 |
| Agrumes | j/ha | 90 | 90 |
| Arboriculture en sec (AR : arbres fruitiers) | j/ha | 20 | 20 |
| Arboriculture en irrigué | j/ha | 60 | 60 |
| Palmier dattier | j/ha | 120 | 120 |
| Cultures sous serres | j/ha | 300 | 300 |
| Bananes sous serres | j/ha | 700 | 700 |
| Élevage : bovins (1995) ; bovins, équins et camélidés (1999) | j/tête | 30 | 30 |
| Élevage : ovins (AR : ovins et caprins) | j/tête | 5 | 5 |
| Aviculture | j/1000 volailles | 36 | 36 |
| Cuniculture | j/1000 lapins | — | 36 |
| Pêche côtière | j/barque | 500 | 500 |
| Pêche au chalut (AR : pêche au feu/aux lumières) | j/unité | 2000 | 2000 |

### Art. 5 — chauffeurs de louage et taxis ; « masseurs » des bains maures
- Assiette = SMIG régime 48 h × **2 400 heures/an** × coefficient **1,5**. Réparations même base.

### Art. 6 — employés de maison (base SMAG × 300 jours/an)
- Aides de ménage : **0,53 %**.
- Autres employés sauf chauffeurs : **0,75 %**.
- Conducteurs de voitures : **1 %** × coefficient **1,5**.

### Art. 7 — travailleurs temporaires auprès des particuliers
- Assiette = SMIG × **200 heures/mois** × coefficient **1** (ordinaires) ou **2** (qualifiés) ;
  tout mois commencé compté pour un mois entier. Taux = celui de la branche (non désigné par l'art.).

### Arts 10 à 27 — modulation
- Art. 17 : cotisation supplémentaire = **50 %** des cotisations principales ; doublée (100 %) si
  mesures non exécutées dans les 6 mois, ou récidive dans les 3 ans pour un risque de même nature.
- Art. 18 : portée à **100 %** si refus/négligence persiste 6 mois après la majoration de l'art. 17.
- Art. 24 : réduction plafonnée à **25 %** des cotisations principales.
- Décisions individuelles de la CNSS → relèveraient d'une variable d'entrée « taux modulé ».

## Décret n° 99-1010 (1er avril 1999) — art. 1er, art. 4 §2 (nouveau)
- Remplace le §2 de l'art. 4 : taux **1 % → 0,80 %** du SMAG journalier ; coefficient 1,5 inchangé ;
  base des réparations et option inchangées.
- Tableau des journées : ajoute **horticulture plein champ (70 j/ha)** et **cuniculture
  (36 j/1000 lapins)** ; ligne bovins étendue aux **équins et camélidés** ; autres valeurs identiques.
- (Le même art. 1er refond aussi l'échelle sectorielle, déjà versée en 0.115-0.118, PR #470.)

## Décret n° 2000-1439 (1er juillet 2000)
- Transport public de personnes par **taxi, louage et transport rural** : salaire forfaitaire =
  SMIG interprofessionnel garanti régime 48 h × **2 400 heures/an**, **sans coefficient**.
- Vaut pour les régimes de sécurité sociale **et** le régime AT/MP ; prestations/réparations même base.
- N'abroge pas nommément l'art. 5 de 95-538 : abroge « toutes dispositions antérieures contraires »
  (art. 3). Lecture retenue : au 1er juillet 2000, le coefficient 1,5 cesse pour taxi/louage, le
  transport rural entre dans le forfait, et les « masseurs » des bains maures (hors champ de 2000-1439)
  restent régis par l'art. 5 (coefficient 1,5).

## Lacunes / à trancher (reportées en Questions ouvertes de la PR)
- Arts 6 et 7 : aucune modification postérieure identifiée ; recherche non exhaustive (seuls 95-538,
  99-1010, 2000-1439 lus). Recherche précis `r-atmp-assiette-modificatifs` ouverte côté précis.
- Taux de branche applicable aux forfaits des arts 5 et 7 : non désigné par les articles.
- Arborescence des **variables** (option salaires effectifs, surfaces par culture, nombre de têtes,
  qualification) et intégration annuel/mensuel : décision de modélisation à arbitrer.
- Partage employeur/salarié du forfait : les arts 4-7 fixent une cotisation globale, non ventilée.
