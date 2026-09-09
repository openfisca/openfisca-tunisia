"""Les cotisations du secteur privé, à leurs dates et à leurs valeurs.

Deux choses sont gardées ici. D'abord les TOTAUX, qui sont le seul point sur lequel
le paramétrage se recoupe avec une source publiée : hors retraite complémentaire et hors
cotisation de perte d'emploi, le régime général doit rendre 9,18 % pour le salarié et
16,57 % pour l'employeur, chiffres de la CNSS — et ces totaux doivent survivre à la
datation. Ensuite les DATES elles-mêmes : aucune valeur du secteur privé ne peut porter
le 1er janvier 1960, la structure que ces valeurs décrivent n'existant pas avant 1997.
"""

import datetime
from pathlib import Path

import yaml

from openfisca_tunisia import TunisiaTaxBenefitSystem


tax_benefit_system = TunisiaTaxBenefitSystem()

PRIVE = "prelevements_sociaux.cotisations_sociales.secteur_prive"
RACINE = Path(__file__).parent.parent / "openfisca_tunisia" / "parameters"
DOSSIER_PRIVE = RACINE / "prelevements_sociaux" / "cotisations_sociales" / "secteur_prive"

# Écartées du total obligatoire : la complémentaire est facultative et conventionnelle,
# la perte d'emploi n'existe qu'à partir de 2025.
HORS_TOTAL = ("retraite_complementaire", "perte_d_emploi")


def _taux(chemin, date):
    noeud = tax_benefit_system.get_parameters_at_instant(date)
    for element in chemin.split("."):
        noeud = getattr(noeud, element)
    return noeud.rates[0]


def _total_cote(regime, cote, date):
    base = DOSSIER_PRIVE / regime / f"cotisations_{cote}"
    somme = 0.0
    for fichier in sorted(base.rglob("*.yaml")):
        if fichier.name == "index.yaml" or any(x in fichier.name for x in HORS_TOTAL):
            continue
        relatif = fichier.relative_to(base).with_suffix("")
        chemin = f"{PRIVE}.{regime}.cotisations_{cote}." + ".".join(relatif.parts)
        somme += _taux(chemin, date)
    return round(somme, 4)


def test_le_regime_general_rend_les_taux_publies_par_la_cnss():
    assert _total_cote("rsna", "salarie", "2024-06-30") == 0.0918
    assert _total_cote("rsna", "employeur", "2024-06-30") == 0.1657


def test_aucune_valeur_du_secteur_prive_ne_porte_plus_1960():
    fautifs = [
        str(f.relative_to(DOSSIER_PRIVE))
        for f in DOSSIER_PRIVE.rglob("*.yaml")
        if "1960-01-01" in f.read_text(encoding="utf-8")
    ]
    assert fautifs == [], (
        "La structure décrite par ces valeurs n'existe pas avant 1997 : "
        f"{fautifs}"
    )


def test_chaque_valeur_du_secteur_prive_porte_une_reference():
    sans_reference = []
    for fichier in sorted(DOSSIER_PRIVE.rglob("*.yaml")):
        if fichier.name == "index.yaml":
            continue
        contenu = yaml.safe_load(fichier.read_text(encoding="utf-8"))
        references = (contenu.get("metadata") or {}).get("reference")
        if not references:
            sans_reference.append(str(fichier.relative_to(DOSSIER_PRIVE)))
    assert sans_reference == [], sans_reference


def test_toutes_les_references_du_secteur_prive_pointent_vers_le_jort():
    hors_jort = []
    for fichier in sorted(DOSSIER_PRIVE.rglob("*.yaml")):
        contenu = yaml.safe_load(fichier.read_text(encoding="utf-8"))
        references = (contenu.get("metadata") or {}).get("reference") or {}
        # Deux formes coexistent : une référence datée (un dictionnaire de dates vers
        # des listes) et, sur les `index.yaml`, une référence unique sans date.
        entrees = []
        if "title" in references:
            entrees = [references]
        else:
            for valeur in references.values():
                entrees.extend(valeur if isinstance(valeur, list) else [valeur])
        for entree in entrees:
            if "pist.tn" not in entree.get("href", ""):
                hors_jort.append((str(fichier.relative_to(DOSSIER_PRIVE)), entree.get("href")))
    assert hors_jort == [], hors_jort


def test_la_cotisation_des_etudiants_commence_a_deux_dinars():
    montant = tax_benefit_system.get_parameters_at_instant("1995-01-01")
    for element in f"{PRIVE}.re.cotisation".split("."):
        montant = getattr(montant, element)
    assert montant == 2


def test_les_dates_retenues_sont_celles_des_textes():
    # Le taux global de 18 % vient de la loi n° 97-4, publiée le 4 février 1997 ; la
    # ventilation par branche n'est complète qu'avec le décret n° 2003-1212.
    assert _taux(f"{PRIVE}.rsna.cotisations_salarie.retraite", "2003-01-01") > 0
    assert _taux(f"{PRIVE}.rsna.cotisations_salarie.assurances_sociales.maladie", "1997-02-04") > 0
    # Le régime agricole amélioré prend effet au 1er octobre 1989 (loi n° 89-73, art. 4).
    assert _taux(f"{PRIVE}.rsaa.cotisations_salarie.retraite", "1989-10-01") > 0
    # Le fonds spécial de l'État date de la loi de finances 1975.
    assert _taux(f"{PRIVE}.rsna.cotisations_employeur.fonds_special_etat", "1975-01-01") > 0
    assert datetime.date(1975, 1, 1) < datetime.date.today()
