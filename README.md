# OpenFisca Tunisia

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-tunisia.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-tunisia)

## Presentation

[OpenFisca](http://www.openfisca.fr/) is a versatile microsimulation free software.
This is the source code of the Tunisia module.

Please consult http://www.openfisca.fr/presentation

## Documentation

Please consult http://www.openfisca.fr/documentation

## Installation

Please consult http://www.openfisca.fr/installation if you want to develop with OpenFisca on your computer.

## Contribute

OpenFisca is a free software project.
Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see COPYING).

Feel free to join the OpenFisca development team on [GitHub](https://github.com/openfisca) or contact us by email at
contact@openfisca.fr

## Use with the web API

To test with [curl](https://curl.haxx.se/) and [jq](https://stedolan.github.io/jq/):

```sh
curl "http://localhost:2001/api/1/calculate" -X POST --data @./api/test.json --header "content-type: application/json" | jq .
```