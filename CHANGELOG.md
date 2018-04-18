# Changelog

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

## 0.16.2 - [#63](https://github.com/openfisca/openfisca-tunisia/pull/63)

* Add `notebooks/test_notebooks.py` script to execute .ipynb files
  * Add `Makefile` tag `nb` to test specified notebooks

## 0.16.1 - [#62](https://github.com/openfisca/openfisca-tunisia/pull/62)

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

## 0.14.1 - [#56](https://github.com/openfisca/openfisca-tunisia/pull/56)

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

## 0.10.2 - [#39](https://github.com/openfisca/openfisca-tunisia/pull/39)

* Add installation instructions
* Translate revenus/activite/non_salarie.py labels to arabic

## 0.10.1 - [#38](https://github.com/openfisca/openfisca-tunisia/pull/38)

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
