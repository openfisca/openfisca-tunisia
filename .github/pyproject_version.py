"""Affiche le numéro de version déclaré dans pyproject.toml.

Seul usage : `.github/is-version-number-acceptable.sh`. Ce script remplissait aussi une
recette conda à partir des contraintes d'openfisca-core et de numpy ; cette partie a été
retirée avec conda, que plus aucun workflow ne publiait.
"""

import argparse
import re


def version_du_paquet() -> str:
    with open("./pyproject.toml", encoding="utf-8") as fichier:
        contenu = fichier.read()
    trouve = re.search(r'^version\s*=\s*"([\d.]*)"', contenu, re.MULTILINE)
    if not trouve:
        raise SystemExit("Package version not found in pyproject.toml")
    return trouve.group(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Gardé pour ne pas casser l'appel de is-version-number-acceptable.sh : seul le numéro
    # de version est désormais affiché, quelle que soit sa valeur.
    parser.add_argument("-o", "--only_package_version", type=bool, default=True)
    parser.parse_args()
    print(version_du_paquet())  # noqa: T201
