# OpenFisca Tunisia

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-tunisia.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-tunisia)

## Presentation

EN> [OpenFisca](https://www.openfisca.fr/en) is a versatile microsimulation free software.
This is the source code of the Tunisia module.

FR> [OpenFisca](http://www.openfisca.fr/) est un logiciel libre de micro-simulation.
Ceci est le code source du module dédié à la Tunisie.

## Contribution & Contact

OpenFisca is a free software project.
Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see COPYING).

Feel free to join the OpenFisca development team on [GitHub](https://github.com/openfisca) or contact us by email at
contact@openfisca.fr

## Documentation

* Documentation générale du projet OpenFisca (tous pays confondus) : https://doc.openfisca.fr
  - Et son [schéma des composants](https://doc.openfisca.fr/#project-components) d'un projet OpenFisca
* Explorateur de la législation couverte par OpenFisca-Tunisia : https://legislation.openfisca.tn
* Wiki OpenFisca-Tunisia : https://github.com/openfisca/openfisca-tunisia/wiki

Par ailleurs, chaque module de la [famille OpenFisca sur GitHub](https://github.com/openfisca) dispose d'une documentation propre (voir README.md respectifs).

## Installation

Sous Unix/macOS/Linux, appliquez les étapes qui suivent dans votre Terminal.
Sous Windows, nous vous conseillons d'installer un émulateur de terminal (tel que [ConEmu](https://conemu.github.io)) avant de poursuivre.

### Langage Python & Environnement virtuel

Ce projet nécessite l'installation du langage [Python 2.7](https://www.python.org/downloads/) et du gestionnaire de paquets [pip](https://pip.pypa.io/en/stable/installing/).

Vérifiez alors que la version de python appelée par défaut débute bien par `2.7` :
```
python --version
``
Et installez les éventuelles mises à jour pour la gestion de paquets python avec :
```
pip install --upgrade pip wheel
```

Ensuite, afin de créer un environnement de travail propre et pour vous permettre de faire cohabiter plusieurs contextes de travail en python, 
nous vous conseillons vivement l'utilisation d'environnements virtuels, dits virtualenv. Il vous faut alors installer un gestionnaire de virtualenv python (tel que [pew](https://github.com/berdario/pew).

```
pip install pew
```

Il vous est désormais possible de créer votre premier environnement dédié à OpenFisca-Tunisia. Nommons-le `openfisca` :
```
pew new openfisca --python=python2.7
# Si demandé, répondez "Y" à la question sur la modification du fichier de configuration de votre shell
```

Usage :
* Vous pouvez sortir du virtualenv en tapant exit (ou Ctrl-D)
* Vous pouvez le réactiver grâce à `pew workon openfisca`

### Installation minimale

Si vous souhaitez interroger la dernière version disponible d'OpenFisca-Tunisia sans en modifier les règles de calcul, l'installation minimale est faite pour vous.

Nous supposons que vous avez déjà activé votre environnement virtuel. Appliquez alors la commande suivante pour installer le dernier paquet officiel d'OpenFisca-Tunisia :

```
pip install openfisca-tunisia
```

### Installation du code source

Si vous souhaitez modifier ou étendre OpenFisca-Tunisia, il vous faut installer le code source en local sur votre ordinateur.

Nous supposons que vous avez activé votre environnement virtuel et que vous vous situez dans le répertoire où vous souhaitez placer le projet.
Appliquez alors les commandes suivantes pour récupérer les sources d'OpenFisca-Tunisia et configurer le projet :

```
git clone https://github.com/openfisca/openfisca-tunisia.git
cd openfisca-tunisia
pip install -e .
```

## Test

Nous supposons que vous êtes dans le répertoire `openfisca-tunisia` et que votre environnement virtuel est activé.
Commencez par installer les outils de test avec :

```
pip install -e .[test]
```

Différents formats de tests sont alors à votre disposition : la rédaction de tests est possible en python ou en yaml.

### Test nose

Un test rédigé en python peut être exécuté avec l'outil `nose`. Celui-ci déroulera les fonctions python dont le nom commence par le mot `test`.
Ainsi, pour exécuter le test python `openfisca_tunisia/tests/test_simple.py`, utilisez la commande suivante :

```
nosetests openfisca_tunisia/tests/test_simple.py
```

Il vous est également possible de n'exécuter qu'un seul test d'un fichier.
Par exemple, pour ne tester que le test nommé `test_1_parent` du fichier `openfisca_tunisia/tests/core_tests.py`, utilisez :
```
nosetests openfisca_tunisia/tests/core_tests.py:test_1_parent
```

### Test yaml

Le format d'un test yaml est décrit dans la [documentation officielle](https://doc.openfisca.fr/coding-the-legislation/writing_yaml_tests.html).
Ainsi, si vous souhaitez exécuter le test yaml `openfisca_tunisia/tests/formulas/irpp.yaml`, utilisez la commande :

```
openfisca-run-test -c openfisca_tunisia openfisca_tunisia/tests/formulas/irpp.yaml 
```

### Tout tester

L'ensemble des tests définis dans OpenFisca-Tunisia peut être démarré grâce à la commande suivante :

```
make test
```

## Web API

### API principale (en production)

Il existe une [documentation générale des points de communication](https://doc.openfisca.fr/openfisca-web-api/endpoints.html) de l'API officielle.
Celle-ci peut être testée avec [curl](https://curl.haxx.se/) et [jq](https://stedolan.github.io/jq/) :

```sh
curl "http://localhost:2001/api/1/calculate" -X POST --data @./api/test.json --header "content-type: application/json" | jq .
```

### Nouvelle API (en développement)

Voir la [documentation officielle de l'API Preview](https://doc.openfisca.fr/openfisca-web-api/preview-api.html).
