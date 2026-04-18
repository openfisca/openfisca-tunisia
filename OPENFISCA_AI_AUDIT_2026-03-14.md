# Audit OpenFisca AI - 2026-03-14

Audit execute depuis `openfisca-ai` avec les validateurs suivants:

- `check_package_baseline.py`
- `check_tooling.py`
- `validate_units.py`
- `validate_parameters.py`
- `validate_code.py`
- `validate_tests.py`

## Resume executif

`openfisca-tunisia` a une base de repository saine:

- structure generale bonne
- outillage moderne en place (`uv`, `ruff`, `yamllint`, CI)
- unites propres sur tous les parametres

Les problemes principaux ne sont pas structurels. Ils sont dans la qualite
metier du stock existant:

- metadonnees parametres incompletes (`label`, `reference`)
- variables calculees insuffisamment couvertes par les tests
- plusieurs constantes juridiques encore codees en Python
- plusieurs `TODO` encore presents dans le code

## Resultats par validateur

### 1. Baseline package

Resultat: utilisable, 1 warning.

Points valides:

- `pyproject.toml`
- `uv.lock`
- package `openfisca_tunisia`
- `parameters/index.yaml`
- `reforms/`
- `tests/`
- `Makefile`
- workflows CI

Warning:

- `openfisca_tunisia/situation_examples/` absent

Ce point n'est pas bloquant.

### 2. Tooling

Resultat: OK.

Points valides:

- `uv`
- `ruff`
- `.yamllint`
- tests YAML et Python presents

### 3. Unites

Resultat: OK.

Resume:

- 313 fichiers parametres controles
- 313 avec metadonnees d'unite
- 0 unite manquante
- 0 unite indefinie

Conclusion:

- la couche `units.yaml` est propre
- les validateurs d'unites ne doivent pas etre la priorite

### 4. Metadonnees des parametres

Resultat: 562 erreurs.

Repartition:

- 313 erreurs `missing_label`
- 249 erreurs `missing_reference`

Conclusion:

- la dette parametres est massive mais simple
- le vrai travail est une campagne systematique de normalisation des metadonnees

Domaines visiblement tres touches:

- `parameters/impot_revenu/`
- `parameters/produits_subventionnes/`
- `parameters/marche_travail/`
- `parameters/energie/`
- `parameters/prelevements_sociaux/`
- `parameters/retraite/`

### 5. Code Python

Resultat: 47 erreurs, 4 warnings.

Repartition des erreurs:

- 40 `hardcoded_numeric_value`
- 7 `todo_comment`

Warnings:

- 2 `if_statement_in_formula`
- 2 `comprehension_in_formula`

Interpretation:

- le signal principal est la presence de valeurs juridiques ou seuils encore en
  dur dans certaines formules
- les `TODO` confirment une dette de finition sur plusieurs modules
- les warnings ne sont pas necessairement des bugs, mais ils meritent revue

Fichiers les plus charges:

- `openfisca_tunisia/variables/prestations/contributives/prestations_familiales.py`
- `openfisca_tunisia/variables/prestations/non_contributives/amen_social.py`
- `openfisca_tunisia/variables/prestations/non_contributives/allocation_familiale.py`
- `openfisca_tunisia/variables/prelevements_obligatoires/cotisations_sociales.py`
- `openfisca_tunisia/variables/prelevements_obligatoires/impot_revenu/irpp.py`
- `openfisca_tunisia/variables/caracteristiques_socio_demographiques/etat_civil.py`
- `openfisca_tunisia/reforms/de_net_a_imposable.py`
- `openfisca_tunisia/reforms/de_net_a_salaire_de_base.py`

Exemples representatifs:

- `de_net_a_imposable.py`: `1.25`, `100`
- `de_net_a_salaire_de_base.py`: `1000`
- `prestations_familiales.py`: plusieurs ages, plafonds, coefficients et
  bornes numeriques
- `mesures.py`: `TODO`

### 6. Couverture de tests

Resultat: 47 variables calculees sans test correspondant detecte.

Resume:

- 111 variables avec `formula*` detectees
- 34 tests YAML detectes
- 2 tests Python detectes
- 47 variables calculees sans test correspondant trouve par heuristique

Interpretation:

- la couverture n'est pas catastrophique, mais elle est insuffisante pour les
  zones les plus sensibles
- le resultat est une heuristique de couverture par nommage et mention
  explicite, donc certaines variables peuvent etre testees indirectement
- malgre cette limite, le signal est assez fort pour conclure qu'il manque une
  campagne de tests sur plusieurs domaines

Variables/familles particulierement exposees:

- `prestations_familiales`
- `allocation_familiale_non_contributive`
- `amen_social`
- `cotisations_sociales`
- plusieurs sous-composants `irpp`
- plusieurs revenus categoriels (`bic`, `foncier`, `rvcm`, `etranger`)
- variables de mesures agragees

## Priorites recommandees

### Priorite 1: parametres

Lancer une campagne par domaine pour ajouter:

- `label`
- `reference`

Ordre recommande:

1. `impot_revenu`
2. `retraite`
3. `prelevements_sociaux`
4. `prestations`
5. `energie`
6. `produits_subventionnes`

### Priorite 2: nettoyage code

Nettoyer d'abord les fichiers les plus charges:

1. `prestations_familiales.py`
2. `amen_social.py`
3. `allocation_familiale.py`
4. `cotisations_sociales.py`
5. `irpp.py`

Objectifs:

- supprimer les `TODO`
- documenter les constantes purement techniques
- sortir les valeurs juridiques vers les parametres YAML

### Priorite 3: tests

Ajouter d'abord des tests pour:

1. `prestations_familiales`
2. `allocation_familiale_non_contributive`
3. `amen_social`
4. `cotisations_sociales`
5. deductions et sous-composants `irpp`

### Priorite 4: confort de repo

Optionnel:

- ajouter `situation_examples/`

Ce point peut attendre apres la dette metier.

## Conclusion

`openfisca-tunisia` n'a pas un probleme de socle technique. Le repository est
deja moderne et correctement outille.

La dette se concentre sur trois sujets:

- metadonnees parametres
- nettoyage de quelques modules Python
- couverture de tests des variables calculees

En pratique, la meilleure strategie est de traiter le stock par lots thematiques
et non fichier par fichier isole.
