# OpenFisca Tunisia - الجباية المفتوحة  تونس

[![CircleCI](https://circleci.com/gh/openfisca/openfisca-tunisia/tree/master.svg?style=svg)](https://circleci.com/gh/openfisca/openfisca-tunisia/tree/master)

## Presentation - التقديم

[OpenFisca](http://openfisca.org) est un logiciel libre de micro-simulation.
Ceci est le code source du module dédié à la Tunisie.

<p align='right'>الجباية المفتوحة برنامج حر لمحاكاة النظام الجبائي.
 هذا مصدر البرنامج للوحدة الخاصة بتونس</p>

[OpenFisca](http://openfisca.org) is a versatile microsimulation free software.
This is the source code of the Tunisia module.

## Demo - لعبة تجريبية

Un démonstrateur vous est proposé sous la forme d'un Notebook Jupyter.  
Vous serez redirigé vers celui-ci en cliquant sur le lien suivant (le chargement prendra quelques secondes) :  
<code><p align='center'>[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/openfisca/openfisca-tunisia/master?filepath=notebooks%2Fdemo.ipynb)</p></code>
Vous accédez ainsi à un démonstrateur modifiable où il vous est possible de tester openfisca-tunisia.   

<p align='right'>ستجدون لعبة تجريبية في شكل دفتر جوبيتر على الرابط التالي</p>

<code><p align='center'>[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/openfisca/openfisca-tunisia/master?filepath=notebooks%2Fdemo.ipynb)</p></code>
<p align='right'>يسمح هذا الدفتر بتجريب الجباية المفتوحة لتونس</p>

A demo is available in a Jupyter Notebook.  
You will be redirected to it by clicking on the following link (wait a few seconds to load it):  
<code><p align='center'>[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/openfisca/openfisca-tunisia/binder?filepath=notebooks%2Fdemo.ipynb)</p></code>
Then you will be in an interactive demo where you will be able to play with openfisca-tunisia.  


> This demo is available thanks to [Binder](https://mybinder.org/) and [Jupyter](http://jupyter.org) projects. 

## Contribution & Contact - المساهمة والاتصال بنا

OpenFisca est un projet de logiciel libre.

Son code source est distribué sous la licence [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 ou ultérieure (cf. [LICENSE](https://github.com/openfisca/openfisca-tunisia/blob/master/LICENSE)).

N'hésitez pas à rejoindre l'équipe de développement OpenFisca !
Pour en savoir plus, une [documentation](http://openfisca.org/doc/contribute/index.html) est à votre disposition.


<p align='right'> الجباية المفتوحة برنامج حر</p>

<p align='right'> تم توزيع مصدر هذا البرنامج تحت رخصة أفيرو العامة الثالثة أو ما أعلى</p>

<p align='right'>تعالوا انضموا إلى فريق الجباية المفتوحة و ساهموا في تطوير البرنامج! للمزيد من المعلومات، يرجى زيارة الموقع الإلكتروني الرسمي</p>


OpenFisca is a free software project.

Its source code is distributed under the [GNU Affero General Public Licence](http://www.gnu.org/licenses/agpl.html)
version 3 or later (see [LICENSE](https://github.com/openfisca/openfisca-tunisia/blob/master/LICENSE) file).

Feel free to join the OpenFisca development team!
See the [documentation](http://openfisca.org/doc/contribute/index.html) for more information.

## Documentation

* [Documentation générale](http://openfisca.org/doc/) du projet OpenFisca (tous pays confondus)
  - Et son [schéma des composants](http://openfisca.org/doc/#project-components) d'un projet OpenFisca
* [Explorateur de la législation](https://legislation.openfisca.tn) couverte par OpenFisca-Tunisia
* [Wiki](https://github.com/openfisca/openfisca-tunisia/wiki) OpenFisca-Tunisia
* [Google Drive public](https://drive.google.com/drive/folders/1xzrwEgZF2pEMUIHMQMWtlg7ubIFdy58N?usp=sharing) de références législatives

Par ailleurs, chaque module de la [famille OpenFisca sur GitHub](https://github.com/openfisca) dispose d'une documentation propre (voir `README.md` respectifs).

## Installation

Sous Unix/macOS/Linux, appliquez les étapes qui suivent dans votre Terminal.

Sous Windows, installez un émulateur de terminal avant de poursuivre.  
Nous vous conseillons en particulier l'émulateur BASH fourni avec le [gestionnaire de version GIT](https://git-for-windows.github.io).  
En l'intégrant à un outil tel que [Visual Studio Code](https://code.visualstudio.com), vous aurez un environnement fonctionnel pour travailler sur le code source.
Néanmoins, vous aurez à effectuer des vérifications complémentaires à ce qui est décrit ci-dessous (telles que vérifier la configuration de votre variable d'environnement `%PATH%`).

### Langage Python & Environnement virtuel

Ce projet nécessite l'installation préalable des éléments suivants :
* Le langage [Python 3.7](https://www.python.org/downloads/)
* Le gestionnaire de paquets [pip](https://pip.pypa.io/en/stable/installing/).

Vérifiez alors que la version de python appelée par défaut débute bien par `3.7` :

```
python --version
```

Et installez les éventuelles mises à jour pour la gestion de paquets python avec :

```
sudo pip install --upgrade pip wheel
```

Ensuite, afin de créer un environnement de travail propre et pour vous permettre de faire cohabiter plusieurs contextes de travail en python,
nous vous conseillons l'utilisation d'environnements virtuels, dits virtualenv.
Il vous faut alors installer un gestionnaire de virtualenv python (tel que [pew](https://github.com/berdario/pew)).

```
sudo pip install pew
```

Il vous est désormais possible de créer votre premier environnement dédié à OpenFisca-Tunisia. Nommons-le `openfisca` :

```
pew new openfisca --python=python3.7
# Si demandé, répondez "Y" à la question sur la modification du fichier de configuration de votre shell
```

Usage :
* Vous pouvez sortir du virtualenv en tapant `exit` (ou Ctrl-D)
* Vous pouvez le réactiver grâce à `pew workon openfisca`

### Installation du module OpenFisca-Tunisia

Deux options s'offrent à vous :
* Installer le module python pré-compilé dit [wheel python](https://pypi.org/project/OpenFisca-Tunisia/)
* Ou, installer le code source

#### Installer la wheel

Installer le module pré-compilé d'`OpenFisca-Tunisia` vous permet d'interroger le modèle socio-fiscal tunisien.

Nous supposons que vous avez activé votre environnement virtuel.  
Appliquez alors la commande suivante pour récupérer la wheel `OpenFisca-Tunisia` depuis la librairie de paquets Python [pypi](https://pypi.org) :

```sh
pip install openfisca-tunisia
```

:tada: Félicitations, vous avez désormais terminé l'installation d'OpenFisca Tunisia !

Vous pouvez vérifier sa présence dans votre environnement courant avec :
```sh
pip list
# Résultat attendu : Liste contenant OpenFisca-Tunisia et ses dépendances.
```

#### Installer le code source

Installer le code source d'`OpenFisca-Tunisia` sur votre ordinateur vous permet d'interroger ou de modifier le modèle socio-fiscal tunisien.

Nous supposons que vous avez activé votre environnement virtuel et que vous vous situez dans le répertoire où vous souhaitez placer le projet.
Appliquez alors les commandes suivantes pour récupérer les sources d'OpenFisca-Tunisia et configurer le projet (sans omettre le point en fin de ligne :slightly_smiling_face:) :

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

Un test rédigé en python peut être exécuté avec l'outil `nose`.
Celui-ci déroulera les fonctions python dont le nom commence par le mot `test`.

Ainsi, pour exécuter le test python `tests/test_simple.py`, utilisez la commande suivante :

```
nosetests tests/test_simple.py
```

Il vous est également possible de n'exécuter qu'un seul test d'un fichier. Dans l'exemple suivant, `test_1_parent` sera l'unique test déroulé du fichier `tests/core_tests.py` :

```
nosetests tests/core_tests.py:test_1_parent
```

### Test yaml

Le format d'un test yaml est décrit dans la [section YAML tests](http://openfisca.org/doc/coding-the-legislation/writing_yaml_tests.html) de la documentation officielle.
Ainsi, si vous souhaitez exécuter le test yaml `tests/formulas/irpp.yaml`, utilisez la commande :

```
openfisca-run-test -c openfisca_tunisia tests/formulas/irpp.yaml
```

Afin de le tester avec un debugger, ajoutez un point d'arrêt dans le code python appelé par le test avec :
```
import nose.tools; nose.tools.set_trace(); import ipdb; ipdb.set_trace()
```

Et exécutez à nouveau le test yaml.

### Tout tester

L'ensemble des tests et exemples définis dans OpenFisca-Tunisia peut être exécuté avec une commande. Néanmoins, cela nécessite l'installation de librairies complémentaires pour les exemples rédigés sous forme de [notebooks Jupyter](http://jupyter.org) :

```
pip install -e .[notebook]
```

Le tout peut ensuite être démarré grâce à la commande suivante :

```
make test
```

Pour en savoir plus, voir [la section Tests](http://openfisca.org/doc/contribute/tests.html) de la documentation officielle.

## Web API

L'API est issue du dépôt [GitHub du module central OpenFisca-Core](https://github.com/openfisca/openfisca-core).

Pour consulter sa version `v0.13.0`, il suffit d'interroger l'un de ses points d'entrée.   
La liste des paramètres est par exemple consultable à l'adresse suivante :
```
www.openfisca.tn/api/v0.13.0/parameters
```
Pour en savoir plus, nous vous conseillons la lecture de sa [documentation officielle](http://openfisca.org/doc/openfisca-web-api/preview-api.html).
