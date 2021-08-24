# Changelog

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
