"""Ce que chaque système socio-fiscal lit de l'arbre de paramètres.

Le dépôt porte UN SEUL arbre de paramètres, sous `openfisca_tunisia/parameters/`, et
plusieurs systèmes socio-fiscaux qui n'en lisent chacun qu'une partie. Les listes vivent ici,
ensemble, pour qu'un seul test les confronte à l'arbre : aucun sous-arbre orphelin, aucun
sous-arbre déclaré qui n'existe pas.

POURQUOI UNE LISTE, ET NON LE RÉPERTOIRE ENTIER. `load_parameters` charge tout ce qu'il
trouve. Dès qu'un sous-arbre propre à un autre système entre dans l'arbre commun, un
chargement du répertoire entier le lirait aussi, sans que rien ne le signale.
"""

import os

import yaml
from openfisca_core.parameters import ParameterNode

RACINE_PARAMETRES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parameters")

# Le système socio-fiscal : impôts, cotisations, prestations, rémunérations publiques.
SOUS_ARBRES_FISCAL = (
    "energie",
    "fiscalite_indirecte",
    "fonction_publique",
    "impot_revenu",
    "impot_societes",
    "marche_travail",
    "prelevements_sociaux",
    "prestations",
    "produits_subventionnes",
)

# Chaque système et ce qu'il lit. Un sous-arbre peut être lu par plusieurs systèmes : il
# reste un seul fichier, à une seule place.
SYSTEMES = {
    "fiscal": SOUS_ARBRES_FISCAL,
}


def charger_sous_ensemble(sous_arbres):
    """Construit la racine de l'arbre avec les seuls sous-arbres demandés.

    C'est l'équivalent de `load_parameters` restreint à une liste : la racine reprend la
    description et les métadonnées de `parameters/index.yaml`, et chaque sous-arbre est lu
    à sa place, sous le nom qu'il aurait eu dans un chargement complet.
    """
    with open(os.path.join(RACINE_PARAMETRES, "index.yaml"), encoding="utf-8") as f:
        index = yaml.safe_load(f) or {}
    racine = ParameterNode("", data=index)
    for nom in sous_arbres:
        chemin = os.path.join(RACINE_PARAMETRES, nom)
        if not os.path.isdir(chemin):
            msg = f"Sous-arbre de paramètres introuvable : « {nom} » ({chemin})."
            raise FileNotFoundError(msg)
        racine.add_child(nom, ParameterNode(nom, directory_path=chemin))
    return racine
