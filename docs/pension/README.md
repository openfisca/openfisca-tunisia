# OpenFisca Tunisia Pension - الجباية المفتوحة  تونس، المنح

[![Build Status via Travis CI](https://travis-ci.org/openfisca/openfisca-tunisia-pension.svg?branch=master)](https://travis-ci.org/openfisca/openfisca-tunisia-pension)

## Presentation - التقديم

[OpenFisca](http://www.openfisca.fr/) est un logiciel libre et polyvalent de micro-simulation. Ceci est le code source du module Tunisien dédié aux pensions.

<p align='right'>الجباية المفتوحة برنامج حر و متعدد الكفاءات لمحاكاة النظام الجبائي. هذا هو مصدر البرنامج للوحدة التونسية الخاصة بالمنح </p>

[OpenFisca](https://www.openfisca.fr/en) is a versatile microsimulation free software. This is the source code of the Tunisian pension module.

## Contribution & Contact - المساهمة والاتصال بنا

OpenFisca est un projet de logiciel libre.

Son code source est distribué sous la licence [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 ou ultérieure (cf. [LICENSE](https://github.com/openfisca/openfisca-tunisia-pension/blob/master/LICENSE)).

N'hésitez pas à rejoindre l'équipe de développement OpenFisca ! Pour en savoir plus, une [documentation](https://doc.openfisca.fr/contribute/index.html) est à votre disposition.


<p align='right'> الجباية المفتوحة برنامج حر</p>

<p align='right'> تم توزيع مصدر هذا البرنامج تحت رخصة أفيرو العامة الثالثة أو ما أعلى</p>

<p align='right'>تعالو انضمو إلى فريق الجباية المفتوحة و ساهمو في تطوير البرنامج!
انظرو للموقع الرسمي للمزيد من المعلومات
</p>


OpenFisca is a free software project.

Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see [LICENSE](https://github.com/openfisca/openfisca-tunisia-pension/blob/master/LICENSE) file).

Feel free to join the OpenFisca development team! See the [documentation](https://doc.openfisca.fr/contribute/index.html) for more information.

## Documentation

* Documentation générale du projet OpenFisca (tous pays confondus) : https://doc.openfisca.fr
  - Et son [schéma des composants](https://doc.openfisca.fr/#project-components) d'un projet OpenFisca
* Explorateur de la législation couverte par OpenFisca-Tunisia : https://legislation.openfisca.tn
* Wiki OpenFisca-Tunisia Pension : https://github.com/openfisca/openfisca-tunisia-pension/wiki


## Installation

Sous Unix/macOS/Linux, appliquez les étapes qui suivent dans votre Terminal.

Sous Windows, installez un émulateur de terminal (tel que [ConEmu](https://conemu.github.io)) avant de poursuivre.

### Pré-requis : Langage Python & Gestionnaire d'environnement virtuel

Ce projet nécessite l'installation préalable des éléments suivants :
* Le langage [Python 2.7](https://www.python.org/downloads/)
* Le gestionnaire de paquets [pip](https://pip.pypa.io/en/stable/installing/).

Vérifiez alors que la version de python appelée par défaut débute bien par `2.7` :

```
python --version
```

Et pour ce qui suit, les droits d'administrateur pourront vous être demandés selon l'emplacement de l'installation (`sudo` optionnel).

Commencez par installer les éventuelles mises à jour pour la gestion de paquets python avec :

```
sudo pip install --upgrade pip wheel
```

Ensuite, afin de créer un environnement de travail propre et pour vous permettre de faire cohabiter plusieurs contextes de travail en python, nous vous conseillons l'utilisation d'environnements virtuels, dits virtualenv. Il vous faut alors installer un gestionnaire de virtualenv python tel que [pew](https://github.com/berdario/pew) :

```
sudo pip install pew
```

Il vous est désormais possible de créer votre premier environnement dédié à OpenFisca-Tunisia Pension.

### Création d'environnement virtuel

Il vous sera possible de répéter cette étape de multiples fois au cours de vos travaux sur vos projets python.
A chaque fois, vous choisirez un nouveau nom d'environnement.

Soit `pension` le nom que vous auriez choisi pour votre premier environnement virtuel OpenFisca-Tunisia Pension :

```
pew new pension --python=python2.7
# Si demandé, répondez "Y" à la question sur la modification du fichier de configuration de votre shell
```

Usage :
* Vous pouvez sortir du virtualenv en tapant exit (ou Ctrl-D)
* Vous pouvez le réactiver grâce à `pew workon pension`

### Installation du code source

Afin d'interroger ou de modifier OpenFisca-Tunisia Pension, il vous faut installer le code source en local sur votre ordinateur.

Nous supposons que vous avez activé votre environnement virtuel et que vous vous situez dans le répertoire où vous souhaitez placer le projet.

Appliquez alors les commandes suivantes pour récupérer les sources d'OpenFisca-Tunisia Pension et configurer le projet (sans omettre le point en fin de ligne :slightly_smiling_face:) :

```
git clone https://github.com/openfisca/openfisca-tunisia-pension.git
cd openfisca-tunisia-pension
pip install -e .
```

:tada: Félicitations, vous avez désormais terminé l'installation d'OpenFisca Tunisia Pension !

Vous pouvez vérifier que votre environnement fonctionne bien en démarrant les tests tel que décrit dans le paragraphe suivant.

## Test

Nous supposons que vous êtes dans le répertoire `openfisca-tunisia-pension` et que votre environnement virtuel est activé.
Commencez par installer les outils de test avec :

```
pip install -e .[tests]
```

### Test nose

Un test rédigé en python peut être exécuté avec l'outil `nose`. Celui-ci déroulera les fonctions python dont le nom commence par le mot `test`.

Ainsi, pour exécuter le test python `openfisca_tunisia_pension/tests/test_pension.py`, utilisez la commande suivante :

```
nosetests nosetests openfisca_tunisia_pension/tests/test_pension.py
```

Il vous est également possible de n'exécuter qu'un seul test d'un fichier. Dans l'exemple suivant, `test_rsna` sera l'unique test déroulé du fichier `openfisca_tunisia_pension/tests/test_pension.py` :

```
nosetests openfisca_tunisia_pension/tests/test_pension.py:test_rsna
```

### Test yaml

Le format d'un test yaml est décrit dans la [documentation officielle](https://doc.openfisca.fr/coding-the-legislation/writing_yaml_tests.html).

Ainsi, si vous souhaitez exécuter le test yaml `openfisca_tunisia_pension/tests/formulas/rsna_pension.yaml`, utilisez la commande :

```
openfisca-run-test -c openfisca_tunisia_pension openfisca_tunisia_pension/tests/formulas/rsna_pension.yaml
```

### Tout tester

L'ensemble des tests définis dans OpenFisca-Tunisia peut être démarré grâce à la commande suivante :

```
make test
```
