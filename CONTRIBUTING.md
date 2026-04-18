# Contribuer à OpenFisca-Tunisia

> Ce fichier définit les règles à suivre pour contribuer à ce dépôt.
> Les règles proposées ici sont celles généralement utilisées pour les packages OpenFisca.

Avant tout, merci de votre volonté de contribuer à OpenFisca !

En bref : [GitHub Flow](https://guides.github.com/introduction/flow/), [SemVer](http://semver.org/).

## Pré-requis

```bash
git clone <repo-url>
cd openfisca-tunisia
uv sync
```

## Vérifications de code automatiques avec pre-commit

Avant chaque commit, des vérifications automatiques sont exécutées via [pre-commit](https://pre-commit.com/).

```bash
uv run pre-commit install
```

Exécuter les vérifications manuellement :

```bash
uv run pre-commit run --all-files
```

## Validation avec openfisca-ai

Ce dépôt utilise [openfisca-ai](https://github.com/benjello/openfisca-ai) comme toolkit de validation :

```bash
uv run openfisca-ai validate-parameters .
uv run openfisca-ai validate-units .
uv run openfisca-ai validate-code .
uv run openfisca-ai audit .
```

## Tests

```bash
uv run pytest
```

## Pull requests

Nous suivons le [GitHub Flow](https://guides.github.com/introduction/flow/) : toutes les contributions de code sont soumises via une pull request vers la branche `master`.

Ouvrir une Pull Request signifie que vous souhaitez que ce code soit intégré. Si vous souhaitez simplement en discuter, envoyez un lien vers votre branche accompagné de vos questions par le canal de communication de votre choix.

### Revue par les pairs

Toutes les pull requests doivent être relues par une personne autre que leur auteur·e.

> En l'absence de relecteur·e disponible, on peut se relire soi-même, mais uniquement après au moins 24 heures sans avoir travaillé sur le code à relire.

Pour faciliter la relecture, veillez à ajouter à votre PR une **explication claire en texte** de vos changements.

En cas de changements non rétrocompatibles, vous **devez** détailler les fonctionnalités dépréciées.

> Vous devez également fournir des indications pour aider les utilisateur·e·s à adapter leur code à la nouvelle version du package.

## Signaler les changements

### Numéro de version

Nous suivons le [versionnage sémantique](http://semver.org/) : chaque changement impacte le numéro de version, et le numéro de version communique la compatibilité de l'API **uniquement**.

Exemples :

#### Patch (correctif)

- Correction ou amélioration d'un calcul existant.

#### Mineur

- Ajout d'une variable au système socio-fiscal.

#### Majeur

- Renommage ou suppression d'une variable du système socio-fiscal.

### Changelog

Les évolutions d'OpenFisca-Tunisia doivent pouvoir être comprises par des réutilisateur·e·s qui n'interviennent pas nécessairement sur le code. Le CHANGELOG se doit donc d'être le plus explicite possible.

Chaque évolution sera documentée par les éléments suivants :

- Sur la première ligne figure en guise de titre le numéro de version, et un lien vers la Pull Request introduisant le changement. Le niveau de titre doit correspondre au niveau d'incrémentation de la version.

  > Par exemple :
  > # 13.0.0 [#671](https://github.com/openfisca/openfisca-tunisia/pull/671)
  >
  > ## 13.2.0 [#676](https://github.com/openfisca/openfisca-tunisia/pull/676)
  >
  > ### 13.1.5 [#684](https://github.com/openfisca/openfisca-tunisia/pull/684)

- La deuxième ligne indique de quel type de changement il s'agit. Les types possibles sont :
  - `Évolution du système socio-fiscal` : Amélioration, correction, mise à jour d'un calcul. Impacte les réutilisateur·e·s intéressé·e·s par les calculs.
  - `Amélioration technique` : Amélioration des performances, évolution de la procédure d'installation, de la syntaxe des formules… Impacte les réutilisateur·e·s rédigeant des règles et/ou déployant leur propre instance.
  - `Correction d'un crash` : Impacte tou·te·s les réutilisateur·e·s.
  - `Changement mineur` : Refactoring, métadonnées… N'a aucun impact sur les réutilisateur·e·s.

- **Dans le cas d'une `Évolution du système socio-fiscal`**, il est ensuite précisé :
  - Les périodes concernées par l'évolution. Les dates doivent être données au jour près pour lever toute ambiguïté : on écrira `au 01/01/2017` et non `pour 2017`.
  - Les zones du modèle de calcul impactées. Ces zones correspondent à l'arborescence des fichiers dans le modèle, sans l'extension `.py`.

  > Par exemple :
  > - Périodes concernées : Jusqu'au 31/12/2015.
  > - Zones impactées : `prestations/allocations_familiales`

- Enfin, dans tous les cas hors `Changement mineur`, les corrections apportées doivent être explicitées avec des détails donnés d'un point de vue fonctionnel.

Dans le cas où une Pull Request contient plusieurs évolutions distinctes, plusieurs paragraphes peuvent être ajoutés au CHANGELOG. Pour être correctement formatés en Markdown, ces paragraphes doivent être séparés par `<!-- -->`.

## Protection de branche et CI

Lorsque les versions Python supportées (ou autre matrice CI) changent dans `.github/workflows/workflow.yml`, mettez à jour les **Required status checks** du dépôt :

1. Ouvrir **Settings** → **Branches** → règle de protection de la branche `master`.
2. Dans **Require status checks to pass before merging**, retirer les checks obsolètes.
3. Après la prochaine exécution du nouveau workflow, ajouter les nouveaux noms de jobs si nécessaire.
