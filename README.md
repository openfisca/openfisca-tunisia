# OpenFisca Tunisia - الجباية المفتوحة  تونس

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-tunisia.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-tunisia)

## Presentation - تقديم

[OpenFisca](http://www.openfisca.fr/) est un logiciel libre de micro-simulation. Ceci est le code source du module dédié à la Tunisie.

<p align='right'>الجباية المفتوحة برنامج حر لمحاكاة النظام الجبائي. هذا هو مصدر البرنامج للوحدة الخاصة بتونس</p>

[OpenFisca](https://www.openfisca.fr/en) is a versatile microsimulation free software. This is the source code of the Tunisia module.

## Contribution & Contact - المساهمة والاتصال

OpenFisca est un projet de logiciel libre.

Son code source est distribué sous la licence [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 ou ultérieure (cf. [LICENSE](https://github.com/openfisca/openfisca-tunisia/blob/master/LICENSE)).

N'hésitez pas à rejoindre l'équipe de développement OpenFisca ! Pour en savoir plus, une [documentation](https://doc.openfisca.fr/contribute/index.html) est à votre disposition.


<p align='right'> الجباية المفتوحة برنامج حر</p>

<p align='right'> تم توزيع مصدر هذا البرنامج تحت رخصة أفيرو العامة الثالثة أو ما أعلى</p>

<p align='right'>تعالو انضمو إلى فريق الجباية المفتوحة و ساهمو في تطوير البرنامج! 
انظرو للموقع الرسمي للمزيد من المعلومات
https://doc.openfisca.fr/contribute/index.html
</p>


OpenFisca is a free software project.

Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see [LICENSE](https://github.com/openfisca/openfisca-tunisia/blob/master/LICENSE) file).

Feel free to join the OpenFisca development team! See the [documentation](https://doc.openfisca.fr/contribute/index.html) for more information.

## Documentation

* Documentation générale du projet OpenFisca (tous pays confondus) : https://doc.openfisca.fr
  - Et son [schéma des composants](https://doc.openfisca.fr/#project-components) d'un projet OpenFisca
* Explorateur de la législation couverte par OpenFisca-Tunisia : https://legislation.openfisca.tn
* Wiki OpenFisca-Tunisia : https://github.com/openfisca/openfisca-tunisia/wiki

Par ailleurs, chaque module de la [famille OpenFisca sur GitHub](https://github.com/openfisca) dispose d'une documentation propre (voir README.md respectifs).

## Installation

Sous Unix/macOS/Linux, appliquez les étapes qui suivent dans votre Terminal.

Sous Windows, installez un émulateur de terminal (tel que [ConEmu](https://conemu.github.io)) avant de poursuivre.

### Langage Python & Environnement virtuel

Ce projet nécessite l'installation préalable des éléments suivants :
* Le langage [Python 2.7](https://www.python.org/downloads/)
* Le gestionnaire de paquets [pip](https://pip.pypa.io/en/stable/installing/).

Vérifiez alors que la version de python appelée par défaut débute bien par `2.7` :

```
python --version
```

Et installez les éventuelles mises à jour pour la gestion de paquets python avec :

```
sudo pip install --upgrade pip wheel
```

Ensuite, afin de créer un environnement de travail propre et pour vous permettre de faire cohabiter plusieurs contextes de travail en python, nous vous conseillons vivement l'utilisation d'environnements virtuels, dits virtualenv. Il vous faut alors installer un gestionnaire de virtualenv python (tel que [pew](https://github.com/berdario/pew)).

```
sudo pip install pew
```

Il vous est désormais possible de créer votre premier environnement dédié à OpenFisca-Tunisia. Nommons-le `openfisca` :

```
pew new openfisca --python=python2.7
# Si demandé, répondez "Y" à la question sur la modification du fichier de configuration de votre shell
```

Usage :
* Vous pouvez sortir du virtualenv en tapant exit (ou Ctrl-D)
* Vous pouvez le réactiver grâce à `pew workon openfisca`

### Installation du code source

Afin d'interroger ou de modifier OpenFisca-Tunisia, il vous faut installer le code source en local sur votre ordinateur.

Nous supposons que vous avez activé votre environnement virtuel et que vous vous situez dans le répertoire où vous souhaitez placer le projet.

Appliquez alors les commandes suivantes pour récupérer les sources d'OpenFisca-Tunisia et configurer le projet (sans omettre le point en fin de ligne :slightly_smiling_face: ):

```
git clone https://github.com/openfisca/openfisca-tunisia.git
cd openfisca-tunisia
pip install -e .
```

:tada: Félicitations, vous avez désormais terminé l'installation d'OpenFisca Tunisia ! 

Vous pouvez vérifier que votre environnement fonctionne bien en démarrant les tests tel que décrit dans le paragraphe suivant.

## Test

Nous supposons que vous êtes dans le répertoire `openfisca-tunisia` et que votre environnement virtuel est activé.
Commencez par installer les outils de test avec :

```
pip install -e .[tests]
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

L'API principale est accessible sur [GitHub](https://github.com/openfisca/openfisca-web-api). Une [documentation générale des points de communication](https://doc.openfisca.fr/openfisca-web-api/endpoints.html) est également à votre disposition.

### Nouvelle API (en développement)

La nouvelle API est intégrée au projet [GitHub du module central OpenFisca-Core](https://github.com/openfisca/openfisca-core). Pour en savoir plus, nous vous conseillons la lecture de la [documentation officielle de l'API Preview](https://doc.openfisca.fr/openfisca-web-api/preview-api.html).
