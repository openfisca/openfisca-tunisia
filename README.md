# OpenFisca Tunisia

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-tunisia.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-tunisia)

## Presentation

EN> [OpenFisca](https://www.openfisca.fr/en) is a versatile microsimulation free software.
This is the source code of the Tunisia module.

FR> [OpenFisca](http://www.openfisca.fr/) est un logiciel libre de micro-simulation.
Ceci est le code source du module dédié à la Tunisie.

## Documentation

* Documentation générale du projet OpenFisca (tous pays confondus) : https://doc.openfisca.fr
* Wiki OpenFisca-Tunisia : https://github.com/openfisca/openfisca-tunisia/wiki

## Installation

### Langage Python & Environnement virtuel

```
pip install --upgrade pip
pip install pew
```

### Installation minimale

```
pip install openfisca-tunisia
```

### Installation du code source
```
git clone https://github.com/openfisca/openfisca-tunisia.git
cd openfisca-tunisia
pip install -e .
```

## Test

### Test nose
### Test yaml
### Flake8

```
make test
```

## Contribution

OpenFisca is a free software project.
Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see COPYING).

Feel free to join the OpenFisca development team on [GitHub](https://github.com/openfisca) or contact us by email at
contact@openfisca.fr

## Web API

To test with [curl](https://curl.haxx.se/) and [jq](https://stedolan.github.io/jq/):

```sh
curl "http://localhost:2001/api/1/calculate" -X POST --data @./api/test.json --header "content-type: application/json" | jq .
```
